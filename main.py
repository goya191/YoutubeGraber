import argparse
import os


def parse():
	parser = argparse.ArgumentParser()
	parser.add_argument("output_folder")
	args = parser.parse_args()
	if not os.path.isdir(getattr(args, 'output_folder')):
		raise ValueError("output folder must exist")


def main():
	args = parse()


if __name__ == "__main__":
	main()
