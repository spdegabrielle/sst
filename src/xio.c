#include <stdlib.h>
#include <X11/Intrinsic.h>
#include <X11/StringDefs.h>
#include <X11/Shell.h>
#include <X11/Xaw/Box.h>
#include <X11/Xaw/Form.h>
#include <X11/Xaw/Command.h>
#include <X11/Xaw/AsciiText.h>
#include "sst.h"

static XtAppContext app_context;
static Widget toplevel, text, form; 
static Widget navigation, weapons, planets, misc; 
static Widget navlabel, weaplabel, planlabel, misclabel;

static String fallback[] = {
    "*text.resizable: true",
    "*text.resize: ResizeBoth",
    "*text.width: 640",
    "*text.height: 200",
    "*text.autoFill: True",
    "*text.scrollVertical: Always",
    "*text.scrollHorizontal: WhenNeeded",
    "*text.displayCaret: True",
    "*navigation.fromVert: text",
    "*navigation.borderWidth: 0",
    "*navlabel.label: Navigation:   ",
    "*navlabel.borderWidth: 0",
    "*weapons.fromVert: navigation",
    "*weapons.borderWidth: 0",
    "*weaplabel.label: Weapons:      ",
    "*weaplabel.borderWidth: 0",
    "*planets.fromVert: weapons",
    "*planets.borderWidth: 0",
    "*planlabel.label: Planets:      ",
    "*planlabel.borderWidth: 0",
    "*misc.fromVert: planets",
    "*misc.borderWidth: 0",
    "*misclabel.label: Miscellaneous:",
    "*misclabel.borderWidth: 0",
    NULL,
};

struct cmd_t {
    char *name;
    void (*callback)(Widget, XtPointer, XtPointer);
    Widget *parent;
    int enable;
    Widget widget;

};

static void quit_proc(Widget w, XtPointer client_data, XtPointer call_data)
{ 
    XtDestroyApplicationContext (app_context);
    exit (0);
}

static void noargs_proc(Widget w, XtPointer client_data, XtPointer call_data)
/* use this for commands that take no arguments */
{
    /* currently a stub */
    printf("Button %s pressed\n", XtName(w));
}

static struct cmd_t commands[] = {
    {"Move",		NULL,		&navigation,	0},
    {"Dock",		noargs_proc,	&navigation,	0},
    {"Chart",		noargs_proc,	&navigation,	0},
    {"Impulse",		NULL,		&navigation,	0},
    {"Rest",		NULL,		&navigation,	0},
    {"Warp",		NULL,		&navigation,	0},
    {"Probe",		NULL,		&navigation,	OPTION_PROBE},

    {"Phasers",		NULL,		&weapons,	0},
    {"Torpedo",		NULL,		&weapons,	0},
    {"Shields",		NULL,		&weapons,	0},
    {"Damages",		noargs_proc,	&weapons,	0},
    {"Abandon",		noargs_proc,	&weapons,	0},
    {"Destruct",	noargs_proc,	&weapons,	0},
    {"Deathray",	noargs_proc,	&weapons,	0},
    {"Mayday",		noargs_proc,	&weapons,	0},

    {"Sensors",		noargs_proc,	&planets,	OPTION_PLANETS},
    {"Orbit",		noargs_proc,	&planets,	OPTION_PLANETS},
    {"Transport",	noargs_proc,	&planets,	OPTION_PLANETS},
    {"Mine",		noargs_proc,	&planets,	OPTION_PLANETS},
    {"Crystals",	noargs_proc,	&planets,	OPTION_PLANETS},
    {"Shuttle",		noargs_proc,	&planets,	OPTION_PLANETS},
    {"Planets",		noargs_proc,	&planets,	OPTION_PLANETS},

    {"Score",		noargs_proc,	&misc,		0},
    {"Report",		noargs_proc,	&misc,		0},
    {"Computer",	noargs_proc,   	&misc,		0},
    {"Save",		NULL,		&misc,		0},
    {"Quit",		quit_proc,	&misc,		0},
    {"Help",		noargs_proc,	&misc,		0},
};

static void instantiate_main(int argc, char **argv)
{ 
    struct cmd_t *cp;

    toplevel = XtVaOpenApplication(&app_context, "sst2k", NULL, 0, &argc,
				    argv, fallback, 
				    applicationShellWidgetClass,
				    XtNallowShellResize, True, NULL);
    form = XtVaCreateManagedWidget("form", formWidgetClass, toplevel, NULL);
    /* the command window */
    text = XtVaCreateManagedWidget("text", 
				   asciiTextWidgetClass, form,
				   XtNeditType, XawtextEdit,
				   NULL);
    /* The button panels */
    navigation  = XtVaCreateManagedWidget("navigation", 
					  boxWidgetClass, form,
					  XtNorientation, XtorientHorizontal,
					  NULL); 
    navlabel  = XtVaCreateManagedWidget("navlabel", 
					labelWidgetClass, navigation,
					NULL); 
    weapons  = XtVaCreateManagedWidget("weapons", 
				       boxWidgetClass, form,
				       XtNorientation, XtorientHorizontal,
				       NULL); 
    weaplabel  = XtVaCreateManagedWidget("weaplabel", 
					 labelWidgetClass, weapons,
					 NULL); 
    planets  = XtVaCreateManagedWidget("planets", 
				       boxWidgetClass, form,
				       XtNorientation, XtorientHorizontal,
				       NULL); 
    planlabel  = XtVaCreateManagedWidget("planlabel", 
					 labelWidgetClass, planets,
					 XtNborderWidth, 0,
					 NULL); 
    misc  = XtVaCreateManagedWidget("misc", 
				       boxWidgetClass, form,
				       XtNorientation, XtorientHorizontal,
				       NULL); 
    misclabel  = XtVaCreateManagedWidget("misclabel", 
					 labelWidgetClass, misc,
					 NULL); 
    for (cp = commands; cp < commands + sizeof(commands)/sizeof(commands[0]); cp++) {
	cp->widget = XtVaCreateManagedWidget(cp->name, 
					     commandWidgetClass, 
					     *cp->parent, 
					     XtNlabel, cp->name,
					     NULL);
	if (cp->callback)
	    XtAddCallback (cp->widget, XtNcallback, cp->callback, NULL);
    }
    XtRealizeWidget(toplevel);
    XtAppMainLoop(app_context);
    /* loop may be interrupted */
    XtDestroyApplicationContext(app_context);
}

int main(int argc, char **argv)
{
    instantiate_main(argc, argv);
    exit(0);
}
