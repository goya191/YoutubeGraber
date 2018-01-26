import argparse
import os

#3rd party arg! pytube
from pytube import YouTube

def do_grab(stream, output_folder):
	"""
	Does the grab via pytube
	stream must be OGG!
	"""
	video_title = stream.player_config_args.get('title')
	print("downloading {}".format(video_title))
	# stream.player_config_args['length_seconds']
	saved_file_path = output_folder + os.sep + stream.default_filename
	if not os.path.exists(saved_file_path):
		stream.download(output_path=output_folder)
	else:
		print("skipping: {} - file already exists!").format(stream.default_filename)
		return
	new_filename = os.path.splitext(saved_file_path)[0] + ".ogg"
	os.rename(saved_file_path, new_filename)
	print("saved file to: {}".format(new_filename))

def grab(urls, output_folder):
	for url in urls:
		try:
			yt_obj = YouTube(url)
			yt_stream = yt_obj.streams.filter(adaptive=True, only_audio=True, audio_codec='vorbis').first()
			do_grab(yt_stream, output_folder)
		except ValueError as e:
			raise e

def parse():
	parser = argparse.ArgumentParser()
	parser.add_argument("output_folder")
	parser.add_argument("urls", nargs="*")
	args = parser.parse_args()
	if not os.path.isdir(getattr(args, 'output_folder')):
		raise ValueError("output folder must exist")
	return parser.parse_args()

def main():
	args = parse()
	grab(args.urls, args.output_folder)

if __name__ == "__main__":
	main()
