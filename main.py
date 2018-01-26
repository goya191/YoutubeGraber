import argparse
import os

#3rd party import! pytube
from pytube import YouTube
from pytube import cli
#3rd party import! pydub
from pydub import AudioSegment


def convert_to_mp3(stream, file_handle):
	"""
	uses pydub to convert webm format to mp3

	(Pdb) p stream
	<Stream: itag="171" mime_type="audio/webm" abr="128kbps" acodec="vorbis">
	(Pdb) p file_handle
	<open file 'D:\\test\\Rick and Morty - Evil Morty Theme Song (Trap Remix).webm', mode 'wb' at 0x00000000062CB030>

	"""
	print("post processing")
	file_handle.close()
	orig_filename = file_handle.name
	path, ext = os.path.splitext(orig_filename)
	new_filename = path + ".mp3"

	pytube_obj = AudioSegment.from_file(orig_filename)
	pytube_obj.export(new_filename, format="mp3", bitrate="256k")
	print("converted file: {} to mp3".format(new_filename))
	os.remove(orig_filename)


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
		print("downloading intermediate file to: {}".format(saved_file_path))
		stream.download(output_path=output_folder)
		# post process will happen on complete due to callback setup previously
	else:
		print("skipping: {} - file already exists!").format(stream.default_filename)
		return
	

def grab(urls, output_folder):
	for url in urls:
		try:
			yt_obj = YouTube(url)#, on_progress_callback=cli.on_progress)
			yt_obj.register_on_complete_callback(convert_to_mp3)
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
