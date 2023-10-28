import sys
import os
import glob
import cv2 as cv
import numpy as np
import datetime
import pytesseract
import json
import itertools
from PIL import Image


now = datetime.datetime.now()
print(f"\n\nSTART, {now}")
print(cv.__version__)

letters = ['x'] + [hex(i)[2:] for i in range(0, 16)]
letter_imgs = dict([(i, cv.imread(f"samples/{i}.png")) for i in letters])

def occurrences(img, sample): # returns list of (x, y) coords of occurences
    mat = cv.matchTemplate(img, sample, cv.TM_CCOEFF_NORMED)
    loc = np.where(mat >= 0.95)
    return list(zip(*loc[::-1]))

#xm = cv.matchTemplate(img, letter_imgs['4'], cv.TM_CCOEFF_NORMED)
#loc = np.where(xm >= 0.95)
#for pt in zip(*loc[::-1]):
#    print(f"[{pt[0]}, {pt[1]}]")
#    cv.rectangle(img, pt, (pt[0] + 100, pt[1] + 100), (0,0,255), 2)

def get_message_from_file(image_filename): # gets message from flags
    img = cv.imread(image_filename)
    r = []
    for k, v in letter_imgs.items():
        r = r + [(o[1], k) for o in occurrences(img, v)]
    return ''.join([x[1] for x in sorted(r, key=lambda t: t[0])])


# ocr - timestamp and ship ID tuple
def get_data(image_filename): # (timestamp, ship ID)
    ocr = pytesseract.image_to_string(Image.open(image_filename))

    ts = None
    ship_id = None

    for line in ocr.split('\n'):
        if line.startswith('Ship object ID'):
            ship_id = int(line.split(':')[1].strip().split()[0]) # take the part after ':' and clean it
        if line.startswith('Timestamp'):
            ts = line[10:].strip()
    return (ts, ship_id)


#oc = occurrences(img, letter_imgs['6'])
#print(oc)
#for pt in oc:
    #cv.rectangle(img, pt, (pt[0] + 100, pt[1] + 100), (0,0,255), 2)

##crop
#sub = img[100:660, 100:600]

## displaying
#window_name = "dw"
#cv.namedWindow(window_name)#, cv.cv_window_autosize)
#cv.startWindowThread()
#cv.imshow(window_name, img)
#k = cv.waitKey(0)
#print(f"pressed {k}/{chr(k)}")

#cv.destroyAllWindows()


def extract_to_json(image_filename):
    json_filename = image_filename.replace(".png", ".json")
    if os.path.exists(json_filename):
        print(f"{json_filename} already exists, skipping")
        return
    # extract info
    data = get_data(image_filename)
    message = get_message_from_file(image_filename)
    # store into json
    with open(json_filename, "w") as json_file:
        json.dump({"ship_id": data[1], "timestamp": data[0], "message": message}, json_file)
        

# all signalizations:
if len(sys.argv) < 2:
    print("Please provide a command (extract/get-messages)")
else:
    command = sys.argv[1]
    if command == "extract":
        print("Extracting data...")
        to_process = glob.glob("signalization*.png")
        for i, filename in zip(range(len(to_process)), to_process):
            print(f"{i + 1}/{len(to_process)}: {filename}")
            extract_to_json(filename)
    elif command == "get-messages":
        to_process = glob.glob("signalization*.json")
        all_data = []
        for fn in to_process:
            with open(fn, "r") as file:
                data = json.load(file)
                all_data = all_data + [data]

        # group by ship_id, order by timestamp, filter by 0x, concat
        get_ship_id = lambda j: j["ship_id"]
        by_ship = itertools.groupby(sorted(all_data, key=get_ship_id), get_ship_id)
        for ship_id, ship_data in by_ship:
            by_timestamp = sorted(ship_data, key=lambda j: datetime.datetime.strptime(j["timestamp"][:23], "%Z %Y-%m-%d %H:%M:%S"))
            msgs = ''.join([j["message"][2:] for j in by_timestamp if j["message"].startswith("0x")])

            message = bytes.fromhex(msgs).decode('utf-8')
            print(f"[ship_id={ship_id}]: {message}")
    else:
        print("unknown command")

print("bye")

