import box, compare, read_csv
import google_vision as gv
import json

MEDIA_FOLDER_ID = 44111513325
def create_vision_output(vision_data):
	vout = {}
	for v in vision_data:
		name = v['piece_number']
		vout[name] = {}
		vout[name]['name'] = v['piece_name']
		for x in range(len(v['picture_attributes'])):
			vout[name][v['picture_attributes'][x]] = v['picture_attributes_scores'][x]

	with open('vision.json', 'a+') as f:
		f.write(json.dumps(vout, indent=4))

def main():
	response = box.items(MEDIA_FOLDER_ID)
	entries = response['entries']
	
	vision_data = []
	human_data = []
	for entry in entries:
		name = entry['name'].lower()
		if '.jpg' in name or '.png' in name or '.jpeg' in name:
			vision_data.append(box.send_to_vision(name, entry['id']))
		elif '.xlsx' in name or '.csv' in name:
			human_data += box.parse_excel(entry['id'])

	# gv.output_to_file(json_data)

	print('Vision Results: ' + str(len(vision_data)))
	print('Human Results: ' + str(len(human_data)))
	compare.compare(human_data, vision_data)

	'''
	Revised main.py control flow:
	1. Iterate through box directories and send to appropriate process:
		Respondent_Data/
			Rescuee Folder/
				Rescuee1/
					images/		** send these images through google vision when we get here
						*.jpg
				...
				R_*_codes.xlsx 	** send these through read_csv when we get here
			Official Rescuer Folder/
			Volunteer Rescuer Folder/
	2. Compare results
		Step 1 automatically outputs
		compare.py just needs to be run (it will pull from human.json and vision.json and produce output.json)

	Notes:
		read_csv.py and send_to_vision() always append (this means that if you run them on the same picture twice, the output will show up twice in json)
		this is hard to test because box is set up to our developer account which doesn't have any of the data
		I added a method (box.items(folder_id)) in box to view folder contents in box that I use to walk the file system. Looks something like the following:
			get folder_id
			call box.items(folder_id)
			this returns a box response object
			get entries using response['entries']
			entries is a dict with keys for 'id' (folder_id or file_id), 'name' (ex: obama.jpeg), and 'type' (folder or file)
		I was planning on hard coding the folder ids for the top level respondent type folders (Rescuee Folder, etc) to avoid some box network calls
		While we still have a small sample size, I think it is okay if we just erase human/vision/output.json each time and just always grab all the contents. We can get smarter about it later to only get new files
	'''

if __name__ == '__main__':
	main()
