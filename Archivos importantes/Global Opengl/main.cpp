#include <iostream>
#include <GL/glut.h>
#include <cmath>
#include "BitmapReader.h"
#include "Matrix.h"
using namespace std;

void DrawBox();
void DrawAxes();
void Render();
void Reshape(int,int);
void Keyboard(unsigned char key, int x, int y);
void LoadTexture(char *file);
void Mouse(int key, int state, int x, int y);
void Motion(int x, int y);

int prev_x,prev_y;
float anglex=0, angley=0, CamDist = 7;
float rotx=0,roty=0, prev_rotx=0,prev_roty=0;
GLuint texture;
float BoxTrans[16];


int main(int argc, char *argv[])
{
	glutInit(&argc, argv);
	glutInitDisplayMode(GLUT_RGB|GLUT_DOUBLE|GLUT_DEPTH);
	glutInitWindowPosition(450,100);
	glutInitWindowSize(400,400);
	glutCreateWindow("Render");

	glutDisplayFunc(Render);
	glutIdleFunc(Render);
	glutReshapeFunc(Reshape);
	glutKeyboardFunc(Keyboard);
	glutMouseFunc(Mouse);
	glutMotionFunc(Motion);

	glEnable(GL_DEPTH_TEST);

	char file[80];
	cout<<"Enter Filename: ";
	cin.getline(file,79);
	LoadTexture(file);
	MatrixIdentity(BoxTrans);


	glutMainLoop();
	return 0;
}


void Render()
{
	glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT);
	glLoadIdentity();

	float ex,ey,ez;
	ex = CamDist*sin(angley);
	ey = CamDist*sin(anglex);
	ez = CamDist*cos(anglex)*cos(angley);
	gluLookAt(ex,ey,ez, 0,0,0, 0,1,0);

	/*
	//calculating box transformation: Local
	float trans[16];
	float temp[16];
	MatrixIdentity(temp);
	if(prev_rotx-rotx) MatrixRotateX(temp, rotx-prev_rotx);
	if(prev_roty-roty) MatrixRotateY(temp, roty-prev_roty);
	MatrixMult(BoxTrans,temp,trans); //applying saved transformation
	MatrixCopy(trans,BoxTrans);  //saving last transformation
	MatrixTranspose(trans); //making row-major for openGL
	*/

	//calculating box transformation: Global
	float trans[16];
	MatrixCopy(BoxTrans,trans);
	if(prev_rotx-rotx) MatrixRotateX(trans, rotx-prev_rotx);
	if(prev_roty-roty) MatrixRotateY(trans, roty-prev_roty);
	MatrixCopy(trans,BoxTrans);  //saving last transformation
	MatrixTranspose(trans); //making row-major for openGL



	prev_rotx = rotx;
	prev_roty = roty;


	//Drawing Local axes
	DrawAxes();

	glMultMatrixf(trans);
	DrawBox();

	//Drawing Local axes
	//DrawAxes();

	glutSwapBuffers();
}

void LoadTexture(char *file)
{	
	BMP inp = ReadBitmap(file);
	glGenTextures(1, &texture);
	glBindTexture(GL_TEXTURE_2D, texture);
	glTexImage2D(GL_TEXTURE_2D,0,GL_RGB,inp.width,inp.height,0,GL_RGB, GL_UNSIGNED_BYTE, inp.data);

	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
}

void Keyboard(unsigned char key, int x, int y)
{
	switch(key){
	case 'A':
	case 'a':
		angley -= 0.05;
		break;

	case 'd':
	case 'D':
		angley += 0.05;
		break;

	case 'w':
	case 'W':
		anglex += 0.05;
		break;

	case 's':
	case 'S':
		anglex -=0.05;
		break;
	}
}

bool LeftDown=false;
bool MidDown=false;
void Mouse(int key, int state, int x, int y)
{
	if((key==GLUT_LEFT_BUTTON)&&(state==GLUT_DOWN)) LeftDown = true;  else LeftDown = false;
	if((key==GLUT_MIDDLE_BUTTON)&&(state==GLUT_DOWN)) MidDown = true;  else MidDown = false;
	prev_x = x;
	prev_y = y;
}

void Motion(int x, int y)
{
	if(LeftDown) roty += (x-prev_x)*0.5;
	if(MidDown) rotx += (y-prev_y)*0.5;

	prev_x = x;
	prev_y = y;
}

void Reshape(int w, int h)
{
	if(h==0) h=1;
	float aspect = w*1.0/h;
	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();
	glViewport(0,0,w,h);
	gluPerspective(45,aspect,0.001,100);
	glMatrixMode(GL_MODELVIEW);
}

void DrawBox()
{
	glEnable(GL_TEXTURE_2D);
	glColor3f(1,1,1);
	//glBindTexture(GL_TEXTURE_2D, texture);
	glPushMatrix();
		for(int i=0; i<4; i++){
			glPushMatrix();
			glRotatef(i*90, 0,1,0);	
			glTranslatef(0,0,1);		
			glBegin(GL_QUADS);	

				glTexCoord2f(0,0);
				glVertex3f(-1,-1,0);

				glTexCoord2f(1,0);
				glVertex3f(1,-1,0);

				glTexCoord2f(1,1);
				glVertex3f(1,1,0);

				glTexCoord2f(0,1);
				glVertex3f(-1,1,0);
			glEnd();
			glPopMatrix();
		}

		for(int i=0; i<2; i++){
			glPushMatrix();
			glRotatef(i*180+90, 1,0,0);	
			glTranslatef(0,0,1);		
			glBegin(GL_QUADS);	

				glTexCoord2f(0,0);
				glVertex3f(-1,-1,0);

				glTexCoord2f(1,0);
				glVertex3f(1,-1,0);

				glTexCoord2f(1,1);
				glVertex3f(1,1,0);

				glTexCoord2f(0,1);
				glVertex3f(-1,1,0);
			glEnd();
			glPopMatrix();
		}

	glPopMatrix();
	glDisable(GL_TEXTURE_2D);
}

void DrawAxes()
{
	glBegin(GL_LINES);
		glColor3f(1,0,0);
		glVertex3f(0,0,0);
		glVertex3f(2,0,0);

		glColor3f(0,0,1);
		glVertex3f(0,0,0);
		glVertex3f(0,0,2);

		glColor3f(0,1,0);
		glVertex3f(0,0,0);
		glVertex3f(0,2,0);
	glEnd();
}
