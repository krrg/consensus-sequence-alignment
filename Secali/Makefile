CXX=		g++ $(CCFLAGS)

SECALI=		main.o secali.o
OBJS=		$(SECALI)

CCFLAGS=	-O3 --std=c++11


all:		secali

secali:		$(SECALI)
		$(CXX) $(SECALI)

clean:		
		rm --f $(OBJS) $(OBJS:.o=.d)

realclean:
		rm -f $(OBJS) $(OBJS:.o=.d) secali a.out

%.d:	%.cpp
	$(SHELL) -ec '$(CC) -M $(CXXFLAGS) $< \
		| sed '\''s/\($*\)\.o[ :]*/\1.o $@ : /g'\'' > $@; \
		[ -s $@ ] || rm -f $@'

include $(OBJS:.o=.d)
