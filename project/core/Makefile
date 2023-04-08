#####################
# Makefile for Core #
#####################

# Programs, flags, etc.
CXX =		g++
CXXFLAGS =	-fPIC -shared
RLCFLAGS =	-I /usr/local/include/ -L /usr/local/lib/ -lrelic

# This Program
CLIENT =	libclient.so
SERVER =	libserver.so
SRCS =		include/const.cpp \
			lib/method.cpp
CSRCS = 	$(SRCS) \
			client/client.cpp
SSRCS = 	$(SRCS) \
			server/server.cpp

# All Phony Targets
.PHONY : everything client server all clean

# Default starting position
everything : client server

client : $(CLIENT)

server : $(SERVER)

all : clean everything

clean :
	rm -f $(OBJS) $(CLIENT) $(SERVER)


$(CLIENT) : $(CSRCS)
	$(CXX) $(CSRCS) $(CXXFLAGS) -o $(CLIENT)

$(SERVER) : $(SSRCS)
	$(CXX) $(SSRCS) $(CXXFLAGS) -o $(SERVER)

