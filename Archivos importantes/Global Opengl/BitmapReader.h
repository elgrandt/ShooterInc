#pragma once

struct BMP{
	int width,height;
	unsigned char *data;
};

BMP ReadBitmap(char *file);
void ShowBMP(BMP image);