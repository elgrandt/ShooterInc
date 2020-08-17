#include "BitmapReader.h"
#include <cstdio>
#include <iostream>
#include <Windows.h>
#include <cmath>
using namespace std;

BMP ReadBitmap(char *file)
{
	BMP image;
	FILE *fp = fopen(file,"rb");
	if(!fp){
		cout<<"\aFailed to read file"<<endl;
		while(1);
	}

	tagBITMAPFILEHEADER FH;
	tagBITMAPINFOHEADER InfoH;
	fread(&FH, sizeof(FH), 1, fp);
	fread(&InfoH, sizeof(InfoH), 1, fp);
	if(InfoH.biBitCount !=24){
		cout<<"\aTry using 24bit Bitmap file!"<<endl;
		while(1);
	}
	
	image.width = InfoH.biWidth;
	image.height = abs(InfoH.biHeight);
	image.data = new unsigned char[image.width*image.height*3];
	fread(image.data, image.width*image.height*3, 1, fp);

	//swap R<->B channels
	unsigned char temp;
	for(int i=0; i<image.height; i++){
		for(int j=0; j<image.width; j++){
			temp = image.data[ i*image.width*3 + j*3 + 0 ];
			image.data[ i*image.width*3 + j*3 + 0 ] = image.data[ i*image.width*3 + j*3 + 2 ];
			image.data[ i*image.width*3 + j*3 + 2 ] = temp;
		}
	}
	return image;
}

void ShowBMP(BMP image)
{
	for(int i=0; i<image.height; i++){
		for(int j=0; j<image.width; j++){
			cout<<"[ ";
			for(int k=0; k<3; k++){
				cout.width(4);
				cout<<(int)image.data[ i*image.width*3 + j*3 + k ];
			}
			cout<<"] ";
		}
		cout<<endl;
	}
}