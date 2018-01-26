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
	out_file = video_title + ".ogg"
	print("downloading {}".format(video_title))
	# stream.player_config_args['length_seconds']
	stream.download(output_path=output_folder, filename=out_file)


def grab(urls, output_folder):
	print urls
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
