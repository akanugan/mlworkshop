# ------------------------------------------------------------------------------
# build shared library lib$(libname)s
# created: Thu Mar 15 00:35:28 2018 by dnnwrite.py v1.0.0
# ------------------------------------------------------------------------------
ifndef ROOTSYS
	$(error *** Please set up Root)
endif
# ----------------------------------------------------------------------------
dnndir  := DNN
name	:= DNN
srcdir	:= src
libdir	:= lib
incdir  := include

# create directories 
$(shell mkdir -p $(srcdir) $(libdir) $(incdir))

# get lists of sources
SRCS:=	$(srcdir)/dnn_vbf_ggf.cc 

CINTSRCS:= $(wildcard $(srcdir)/*_dict.cc)

OTHERSRCS:= $(filter-out $(CINTSRCS) $(SRCS),$(wildcard $(srcdir)/*.cc))

# list of dictionaries to be created
DICTIONARIES:= $(SRCS:.cc=_dict.cc)

# get list of objects
OBJECTS		:= $(OTHERSRCS:.cc=.o) $(DICTIONARIES:.cc=.o)
# ----------------------------------------------------------------------------
ROOTCINT	:= rootcint
CXX	:= g++
LD	:= g++
CPPFLAGS:= -I. $(shell root-config --cflags)

ifeq ($(WITH_PYTHON),1)
CPPFLAGS+= -DWITH_PYTHON $(shell python-config --cflags)
endif

CXXFLAGS:= -O2 -Wall -fPIC -ansi -Wshadow -Wextra 
LDFLAGS	:=
# ----------------------------------------------------------------------------
# which operating system?
OS := $(shell uname -s)
ifeq ($(OS),Darwin)
	LDFLAGS += -dynamiclib
	LDEXT	:= .so
else
	LDFLAGS	+= -shared
	LDEXT	:= .so
endif
LDFLAGS += $(shell root-config --ldflags) -Wl,-rpath,$(ROOTSYS)/lib

ifeq ($(WITH_PYTHON),1)
LDFLAGS += $(shell python-config --ldflags)
endif

# libraries
LIBS	:= $(shell root-config --libs)
LIBRARY	:= $(libdir)/lib$(name)$(LDEXT)
# ----------------------------------------------------------------------------
all: $(LIBRARY)

$(LIBRARY)	: $(OBJECTS)
	@echo ""
	@echo "=> Linking shared library $@"
	$(LD) $(LDFLAGS) $^ $(LIBS)  -o $@

$(OBJECTS)	: %.o	: %.cc
	@echo ""
	@echo "=> Compiling $<"
	$(CXX) $(CXXFLAGS) $(CPPFLAGS) -c $< -o $@

$(DICTIONARIES)	: $(srcdir)/%_dict.cc	: $(srcdir)/%.cc $(incdir)/linkdef.h
	@echo ""
	@echo "=> Building dictionary $@"
	$(ROOTCINT) -f $@ -c $(CPPFLAGS) $+
	find $(srcdir) -name "*.pcm" -exec mv {} $(libdir) \;

tidy:
	rm -rf $(srcdir)/*_dict*.* $(srcdir)/*.o 

clean:
	rm -rf $(libdir)/* $(srcdir)/*_dict*.* $(srcdir)/*.o 
