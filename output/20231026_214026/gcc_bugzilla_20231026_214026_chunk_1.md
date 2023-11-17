### Total Bugs Detected: 4649
### Current Chunk: 1 of 30
### Bugs in this Chunk: 160 (From bug 1 to 160)
---


### compiler : `gcc`
### title : `String literals don't obey -fdata-sections`
### open_at : `2000-05-02T19:46:01Z`
### last_modified_date : `2020-09-15T22:15:18Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=192
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `2.95.2`
### severity : `enhancement`
### contents :
I'm pushing the envelope in order to use gcc's flags -ffunction-sections and
-fdata-sections with ld's --gc-sections for dead function elimination in the
Linux kernel.

I've encountered a problem with constant strings from unused functions not
being optimised away along with the function. In other words, the unused
functions get optimised away, but the strings they used do not. I've verified
this is a problem at least for PowerPC and x86 targets, and I suspect all
others too.

The problem occurs because even with -fdata-sections specified, strings go in
section ".rodata". To be optimised away by ld with --gc-sections, they need to
go in a section like ".rodata.something". Noting that string literals don't
have globally unique names, the "something" may need to be the function name
it appeared in, or derived from the string contents perhaps via a hash.
Either option would allow the section containing unused strings to be
optimised away correctly by the linker.

Similarly, with -fwritable-strings and -fdata-sections, the string data ends
up in ".data", not ".data.something" where I would have expected it.

Here's a trivial example showing the problem:
    char *function()
    {
        return "unused string";
    }

Running this through the latest gcc snapshot on:
    http://www.codesourcery.com/gcc-compile.html
with options:
    -ffunction-sections -fdata-sections -fwritable-strings
yeilds:

        .file   "@2566.1"
        .version        "01.01"
gcc2_compiled.:
.data                                   #### Oh-oh! Plain old .data
.LC0:
        .string "unused string"
        .section        .text.function,"ax",@progbits
        .align 4
.globl function
        .type    function,@function
function:
        pushl   %ebp
        movl    %esp, %ebp
        movl    $.LC0, %eax
        popl    %ebp
        ret
.Lfe1:
        .size    function,.Lfe1-function
        .ident  "GCC: (GNU) 2.96 20000418 (experimental)

Release:
2.95.2

Environment:
Red Hat Linux 6.2


---


### compiler : `gcc`
### title : `gcc lays down two copies of constructors`
### open_at : `2001-06-14T11:46:02Z`
### last_modified_date : `2022-01-07T06:20:55Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=3187
### status : `RESOLVED`
### tags : `ABI, missed-optimization`
### component : `c++`
### version : `3.0`
### severity : `enhancement`
### contents :
Two (sometimes three) identical copies of constructors and destructors are laid down. The linker doesn't fail this, but the binaries produced are 20% bigger (on our real-world example) than necessary.

Release:
gcc version 3.0 20010614 (prerelease)

Environment:
PC Linux host, ARM Linux cross-compiler

Configured with: ../gcc/configure --prefix=/home/peter --host=i686-linux --build=i686-linux --target=arm-cvs-linux --enable-languages=c,c++ --enable-static

How-To-Repeat:
arm-cvs-linux-g++ -S aubergine.cpp -o aubergine2.s

The aubergine2.s file clearly contains two identical constructors and two identical destructors.


---


### compiler : `gcc`
### title : `volatile forces load into register`
### open_at : `2001-07-01T09:06:00Z`
### last_modified_date : `2023-02-16T17:27:16Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=3506
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `3.0`
### severity : `enhancement`
### contents :
[ Reported to the Debian BTS as report #89949.
  Please CC 89949-quiet@bugs.debian.org on replies.
  Log of report can be found at http://bugs.debian.org/89949 ]
 	
gcc generates non-intuitive code when one tries to increment a volatile int.

extern int x;
extern volatile int y;

void f() {
	x++;
	y++;
}

The move into %eax seems pointless.

----------------------------------- 
gcc-3.0 and gcc CVS HEAD 20010701: 
        .file   "bug-89949.i" 
        .text 
        .align 2 
.globl f 
        .type   f,@function 
f: 
        pushl   %ebp 
        movl    %esp, %ebp 
        incl    x 
        movl    y, %eax 
        incl    %eax 
        movl    %eax, y 
        popl    %ebp 
        ret 
.Lfe1: 
        .size   f,.Lfe1-f 
        .ident  "GCC: (GNU) 3.1 20010701 (experimental)" 
----------------------------------- 
gcc-3.0 and gcc CVS HEAD 20010701 -O2: 
        .file   "bug-89949.i" 
        .text 
        .align 2 
        .p2align 2,,3 
.globl f 
        .type   f,@function 
f: 
        pushl   %ebp 
        movl    y, %eax 
        movl    %esp, %ebp 
        incl    %eax 
        incl    x 
        popl    %ebp 
        movl    %eax, y 
        ret 
.Lfe1: 
        .size   f,.Lfe1-f 
        .ident  "GCC: (GNU) 3.1 20010701 (experimental)" 
-----------------------------------

Release:
3.0 (Debian GNU/Linux) and HEAD 20010701

Environment:
System: Debian GNU/Linux (testing/unstable)
Architecture: i686
	
host: i386-linux
build: i386-linux
target: i386-linux
configured with: ../src/configure -v --enable-languages=c,c++,java,f77,proto,objc --prefix=/usr --infodir=/share/info --mandir=/share/man --enable-shared --with-gnu-as --with-gnu-ld --with-system-zlib --enable-long-long --enable-nls --without-included-gettext --disable-checking --enable-threads=posix --enable-java-gc=boehm --with-cpp-install-dir=bin --enable-objc-gc i386-linux


---


### compiler : `gcc`
### title : `appalling optimisation with sub/cmp on multiple targets`
### open_at : `2001-07-01T09:16:00Z`
### last_modified_date : `2023-09-21T13:55:49Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=3507
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `3.0`
### severity : `enhancement`
### contents :
[ Reported to the Debian BTS as report #75773.
  Please CC 75773-quiet@bugs.debian.org on replies.
  Log of report can be found at http://bugs.debian.org/75773 ]
 	

For the file

unsigned long foo(unsigned long a, unsigned long b) {
	unsigned long c = a - b;

	if (a < b) {
		c += 100;
	}

	return c;
}

gcc -O2 -S generates (The cmpl after the subl is unnecessary):

        .file   "bug-75773.c"
        .text
        .align 2
        .p2align 2,,3
.globl foo
        .type   foo,@function
foo:
        pushl   %ebp
        movl    %esp, %ebp
        movl    8(%ebp), %edx
        movl    12(%ebp), %eax
        movl    %edx, %ecx
        subl    %eax, %ecx
        cmpl    %eax, %edx
        jae     .L2
        addl    $100, %ecx
.L2:
        movl    %ecx, %eax
        popl    %ebp
        ret
.Lfe1:
        .size   foo,.Lfe1-foo
        .ident  "GCC: (GNU) 3.1 20010701 (experimental)"

Release:
3.0 (Debian GNU/Linux) and HEAD 20010701

Environment:
System: Debian GNU/Linux (testing/unstable)
Architecture: i686
	
host: i386-linux
build: i386-linux
target: i386-linux
configured with: ../src/configure -v --enable-languages=c,c++,java,f77,proto,objc --prefix=/usr --infodir=/share/info --mandir=/share/man --enable-shared --with-gnu-as --with-gnu-ld --with-system-zlib --enable-long-long --enable-nls --without-included-gettext --disable-checking --enable-threads=posix --enable-java-gc=boehm --with-cpp-install-dir=bin --enable-objc-gc i386-linux


---


### compiler : `gcc`
### title : `unnecessary register move on simple code`
### open_at : `2001-08-22T06:16:01Z`
### last_modified_date : `2023-05-16T23:46:40Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=4079
### status : `RESOLVED`
### tags : `missed-optimization, ra`
### component : `rtl-optimization`
### version : `3.0.1`
### severity : `enhancement`
### contents :
This code:

unsigned mulh(unsigned a, unsigned b)
{
        return ((unsigned long long)a * (unsigned long long)b) >> 32;
}

produces this:

   0:   7d 23 20 16     mulhwu  r9,r3,r4
   4:   7d 2a 4b 78     mr      r10,r9
   8:   7d 43 53 78     mr      r3,r10
   c:   4e 80 00 20     blr

when compiled with -O2.
I would have expected mulhwu r3,r3,r4; blr

Release:
gcc-3.0.1 for powerpc-unknown-linux-gnu

Environment:
powerpc-unknown-linux-gnu (YDL 1.2.1)

How-To-Repeat:
gcc -O2 -c mulh.c
with gcc-3.0.1 for ppc (-mcpu=<target> changes nothing)


---


### compiler : `gcc`
### title : `The C++ compiler doesn't place a const class object to ".rodata" section with non trivial constructor`
### open_at : `2001-08-26T09:46:01Z`
### last_modified_date : `2023-08-06T23:36:37Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=4131
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `2.95`
### severity : `enhancement`
### contents :
I want to use a 'fixed-pointed-value' as a replacement of 'floating-point-value'.
But the const instance of my class never be placed to ".rodata" section.
They seem to need ".ctors" , however the constructing code has only a constant instructions to store a certain value.
I think it dosen't need any codes , and needs only few bytes of ".rodata" section.
I tried same test on some compilers , but no one generate the codes I want.
These can be a headache on machines that have little RAM.

Please excuse my poor english typing.(I am a Japanese.)

Release:
unknown-2.9

Environment:
various

How-To-Repeat:
// compile the following with maximam optimization.
class T
{
	int raw; 
public:
	enum { BASE = (1<< 8) };
	template<class value_type> T(value_type opr) : raw(static_cast<int>(opr * BASE)) {}
	template<class value_type> operator value_type() const { return static_cast<value_type>(raw) / BASE; }
};

const T t1 = 1.0;
const int i1 = static_cast<int>(1.0 * T::BASE);

int main(void)
{
	return i1 ^ static_cast<int>(t1);
}


---


### compiler : `gcc`
### title : `Missed code hoisting opportunity`
### open_at : `2002-02-20T13:56:01Z`
### last_modified_date : `2021-08-21T21:55:33Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=5738
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `3.3`
### severity : `enhancement`
### contents :
GCSE not working

The following code: 


struct foo 
{
  unsigned short *p;
};


void
func (struct foo *s, unsigned int *coord, _Bool delta)
{
  unsigned short change;

  if (delta) {
    change = *((s)->p++);
    *coord += change;
  } else {
    change = *((s)->p++);
    *coord += change;
    *coord += *((s)->p++) << 8;
  }
}

generates when compiled with gcc from CVS on SPARC (with -O2)

func:
        !#PROLOGUE# 0
        !#PROLOGUE# 1
        andcc   %o2, 0xff, %g0
        mov     %o0, %o5
        be      .LL2
        mov     %o1, %o4
        ld      [%o0], %o0
        ld      [%o1], %o2
        lduh    [%o0], %o3
        sll     %o3, 16, %o1
        srl     %o1, 16, %o1
        add     %o2, %o1, %o2
        add     %o0, 2, %o0
        st      %o0, [%o5]
        b       .LL1
        st      %o2, [%o4]
.LL2:
        ld      [%o0], %o0
        lduh    [%o0], %o3
        ld      [%o1], %o2
        add     %o0, 2, %o0
        lduh    [%o0], %o1
        add     %o2, %o3, %o2
        sll     %o1, 8, %o1
        add     %o2, %o1, %o2
        add     %o0, 2, %o0
        st      %o2, [%o4]
        st      %o0, [%o5]
.LL1:
        retl
        nop

GCSE should be able to realize that
The sequence:
    change = *((s)->p++);
    *coord += change;

occurs on both branches of the conditional and move it before.

Release:
CVS

Environment:
sparc-sun-solaris2.8

How-To-Repeat:
Compile the code above with -O2 and look at the assembly,
one branch of the conditional should be empty.


---


### compiler : `gcc`
### title : `"const" and "pure" function attributes pessimize code due to poor RA`
### open_at : `2002-02-20T14:16:00Z`
### last_modified_date : `2021-12-03T20:35:58Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=5739
### status : `NEW`
### tags : `missed-optimization, ra`
### component : `rtl-optimization`
### version : `3.3`
### severity : `normal`
### contents :
"const" and "pure" function attributes pessimize code

The following code: 

#ifdef MY_PURE
extern  double mycos (double) __attribute__ ((pure));
extern  double mysin (double) __attribute__ ((pure));
#elif defined MY_CONST
extern  double mycos (double) __attribute__ ((const));
extern  double mysin (double) __attribute__ ((const));
#else
extern  double mycos (double);
extern  double mysin (double);
#endif

struct my_complex
{
  double re;
  double im;
};


int main(void) {

  struct my_complex u[2048];
  int i;
  for (i = 0; i < 2048; ++i)
    {
      u[i].re = 1.0;
      u[i].im = 0.0;
    }
               
  for (i = 0; i < 2048; ++i) {
    struct my_complex *p = u;
    unsigned int j;
    for (j = 0; j < 2048; ++j) {
      double ur = p->re;
      double ui = p->im;
      double u2 = ur * ur + ui * ui;             
      double cosv = mycos (u2);
      double sinv = mysin (u2);
      p->re = p->re * cosv - p->im * sinv;
      p->im = p->im * sinv +  p->re * cosv;
      ++p;
    } 
  }
}

generates worse code when compiled with -O2 -DMY_PURE or
-O2 -DMY_CONST than when compiled with -O2 on SPARC with
GCC from CVS on sparc

Attached is an sdiff of the assembly files resulted when compiling with -O2 (left) and -O2 -DMY_CONST (right)

Release:
CVS

Environment:
sparc-sun-solaris2.8

How-To-Repeat:
Compile the above code with -O2 and -O2 -DMY_CONST and 
look at the assembly files.


---


### compiler : `gcc`
### title : `Access of bytes in struct parameters`
### open_at : `2002-06-17T16:46:01Z`
### last_modified_date : `2022-06-27T06:49:24Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=7061
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `3.2`
### severity : `enhancement`
### contents :
struct s1 { unsigned char a, b; };
unsigned long f1(struct s1 x) {
    return x.a + x.b;
}
struct s2 { unsigned a: 8, b: 8; };
unsigned long f2(struct s2 x) {
    return x.a + x.b;
}

compiled with -O3 -mcpu=pca56 gives:

f1:	lda     sp,-16(sp)
	stw     a0,0(sp)
	ldbu    t1,0(sp)
	ldbu    t2,1(sp)
	addq    t1,t2,v0
	lda     sp,16(sp)
	ret

f2:	mov     a0,t0
	and     a0,0xff,t1
	extbl   t0,0x1,t2
	addq    t1,t2,v0
	ret

In the second case, gcc generates pretty much optimal code[1], whereas
in the first case, it spills the struct to the stack just to re-read
it in single bytes. While this doesn't look too terrible, it gets
really ugly with -mcpu=ev4 (which is default in most distributions),
which has no byte read/write opcodes.

It would be nice if for the first case similar code could be generated
as for the second case.

[1] Well, except for the spurious mov, and it could generate
    zap a0,0x03,v0; perr a0,v0,v0, but I don't expect it to :)

Release:
3.2 20020607 (experimental)

Environment:
System: Linux borkum 2.4.18 #6 Wed Apr 24 22:18:43 CEST 2002 alpha unknown
Architecture: alpha

	
host: alphapca56-unknown-linux-gnu
build: alphapca56-unknown-linux-gnu
target: alphapca56-unknown-linux-gnu
configured with: ../configure --enable-languages=c


---


### compiler : `gcc`
### title : `gcc pessimized 64-bit % operator on hppa2.0`
### open_at : `2002-08-18T04:36:00Z`
### last_modified_date : `2022-01-20T11:31:16Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=7625
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `3.2`
### severity : `normal`
### contents :
GCC seems to compile code for the 64-bit "%" operator that is about 6 times
slower that the HP native compiler on HPPA2.0 machines, even with -march=2.0.

This was noticed affecting OpenSSL DSA operations and identified by Deron
Meranda . For background, please see
http://marc.theaimsgroup.com/?l=openssh-unix-dev&m=102646106016694&w=2

$ cat logmodtest.c
#include <stdio.h>

int
main()
{
        unsigned long long i, a=0;

        for(i=2000000; i; --i)
                a += (i+10) % i;

        printf("Result=%llu\n", a);
        exit(0);
}

$ cc +O3 longmodtest.c
$ time ./a.out
Result=19999913

real    0m0.649s
user    0m0.650s
sys     0m0.000s

$ gcc -O3 -march=2.0 longmodtest.c
$ time ./a.out
Result=19999913

real    0m3.712s
user    0m3.700s
sys     0m0.020s

Release:
3.2

Environment:
System: HP-UX c240 B.11.00 A 9000/782 2007058445 two-user license

host: hppa2.0w-hp-hpux11.00
build: hppa2.0w-hp-hpux11.00
target: hppa2.0w-hp-hpux11.00
configured with: ../gcc-3.2/configure --with-as=/usr/local/hppa2.0w-hp-hpux11.00/bin/as --with-gnu-as --with-ld=/usr/ccs/bin/ld --enable-languages=c,c++

How-To-Repeat:
$ gcc -O3 -march=2.0 -v -save-temps longmodtest.c
Reading specs from /usr/local/lib/gcc-lib/hppa2.0w-hp-hpux11.00/3.2/specs
Configured with: ../gcc-3.2/configure --with-as=/usr/local/hppa2.0w-hp-hpux11.00/bin/as --with-gnu-as --with-ld=/usr/ccs/bin/ld --enable-languages=c,c++
Thread model: single
gcc version 3.2
 /usr/local/lib/gcc-lib/hppa2.0w-hp-hpux11.00/3.2/cpp0 -lang-c -v -D__GNUC__=3 -D__GNUC_MINOR__=2 -D__GNUC_PATCHLEVEL__=0 -D__GXX_ABI_VERSION=102 -Dhppa -Dhp9000s800 -D__hp9000s800 -Dhp9k8 -DPWB -Dhpux -Dunix -D__hppa__ -D__hp9000s800__ -D__hp9000s800 -D__hp9k8__ -D__PWB__ -D__hpux__ -D__unix__ -D__hppa -D__hp9000s800 -D__hp9k8 -D__PWB -D__hpux -D__unix -Asystem=unix -Asystem=hpux -Acpu=hppa -Amachine=hppa -D__OPTIMIZE__ -D__STDC_HOSTED__=1 -D_PA_RISC1_1 -D__hp9000s700 -D_HPUX_SOURCE -D_HIUX_SOURCE -D__STDC_EXT__ -D_INCLUDE_LONGLONG longmodtest.c longmodtest.i
GNU CPP version 3.2 (cpplib) (hppa)
ignoring nonexistent directory "NONE/include"
ignoring nonexistent directory "/usr/local/hppa2.0w-hp-hpux11.00/include"
#include "..." search starts here:
#include <...> search starts here:
 /usr/local/include
 /usr/local/lib/gcc-lib/hppa2.0w-hp-hpux11.00/3.2/include
 /usr/include
End of search list.
 /usr/local/lib/gcc-lib/hppa2.0w-hp-hpux11.00/3.2/cc1 -fpreprocessed longmodtest.i -quiet -dumpbase longmodtest.c -march=2.0 -O3 -version -o longmodtest.s
GNU CPP version 3.2 (cpplib) (hppa)
GNU C version 3.2 (hppa2.0w-hp-hpux11.00)
        compiled by GNU C version 3.2.
 /usr/local/hppa2.0w-hp-hpux11.00/bin/as --traditional-format -o longmodtest.o longmodtest.s
 /usr/local/lib/gcc-lib/hppa2.0w-hp-hpux11.00/3.2/collect2 -L/lib/pa1.1 -L/usr/lib/pa1.1 -z -u main /usr/ccs/lib/crt0.o -L/usr/local/lib/gcc-lib/hppa2.0w-hp-hpux11.00/3.2 -L/usr/ccs/bin -L/usr/ccs/lib -L/opt/langtools/lib -L/usr/local/lib/gcc-lib/hppa2.0w-hp-hpux11.00/3.2/../../.. longmodtest.o -lgcc -lgcc_eh -lc -lgcc -lgcc_eh

See attachments for longmodtest.i.bz2

For comparison, if you split the "%" operation out into a separate source
file:

unsigned long long longmod(unsigned long long a, unsigned long long b)
{
        return(a % b);
}

the HP compiler produces the following assembler output:

        .LEVEL  2.0N

        .SPACE  $TEXT$,SORT=8
        .SUBSPA $CODE$,QUAD=0,ALIGN=4,ACCESS=0x2c,CODE_ONLY,SORT=24
longmod
        .PROC
        .CALLINFO FRAME=0,ARGS_SAVED,ORDERING_AWARE
        .ENTRY
        DEPD    %r25,31,32,%r26 ;offset 0x0
        DEPD    %r23,31,32,%r24 ;offset 0x4
        EXTRD,U %r26,31,32,%r25 ;offset 0x8
        .CALL   ;in=23,24,25,26;out=21,22,28,29; (MILLICALL)
        B,L     $$rem2U,%r31    ;offset 0xc
        EXTRD,U %r24,31,32,%r23 ;offset 0x10
        DEPD    %r28,31,32,%r29 ;offset 0x14
$00000002
$L0
        BVE     (%r2)   ;offset 0x18
        .EXIT
        EXTRD,U %r29,31,32,%r28 ;offset 0x1c
        .PROCEND        ;in=23,25;out=28,29;fpin=105,107;

        .SPACE  $TEXT$
        .SUBSPA $CODE$
        .SPACE  $PRIVATE$,SORT=16
        .SPACE  $TEXT$
        .SUBSPA $CODE$
        .EXPORT longmod,ENTRY,PRIV_LEV=3,ARGW0=GR,ARGW1=GR,ARGW2=GR,ARGW3=GR,RTNVAL=GR,LONG_RETURN
        .IMPORT $$rem2U,MILLICODE
        .END


---


### compiler : `gcc`
### title : `[arm] gcc-20030127 misses an optimization opportunity`
### open_at : `2003-02-11T17:06:00Z`
### last_modified_date : `2019-06-06T15:15:15Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=9663
### status : `RESOLVED`
### tags : `missed-optimization, patch`
### component : `target`
### version : `3.3`
### severity : `enhancement`
### contents :
The following two lines:

cmp r0, #0
mov lr, r0

should be replaced with:

subs lr, r0, #0

in the asm output.

20020503-1.i:
---
# 1 "20020503-1.c"
# 1 "<built-in>"
# 1 "<command line>"
# 1 "20020503-1.c"



 
void abort (void);
static char *
inttostr (long i, char buf[128])
{
  unsigned long ui = i;
  char *p = buf + 127;
  *p = '\0';
  if (i < 0)
    ui = -ui;
  do
    *--p = '0' + ui % 10;
  while ((ui /= 10) != 0);
  if (i < 0)
    *--p = '-';
  return p;
}

int
main ()
{
  char buf[128], *p;

  p = inttostr (-1, buf);
  if (*p != '-')
    abort ();
  return 0;
}

Release:
gcc version 3.3 20030127 (prerelease)

Environment:
Built on: Linux 2.4.20 i686 unknown
Configured with: /home/gertom/gcc/src/gcc-20030127/configure --target=arm-elf --prefix=/home/gertom/gcc/build/install-20030127-arm-elf-orgn --enable-target-optspace --with-newlib --with-headers --disable-nls --disable-threads --disable-shared --disable-libgcj --disable-multilib --with-gnu-as --with-gnu-ld --enable-languages=c,c++
Thread model: single

How-To-Repeat:
just compile with -O2


---


### compiler : `gcc`
### title : `With -Os optimization increases size if the loop contains array element access`
### open_at : `2003-02-17T15:26:00Z`
### last_modified_date : `2019-03-06T07:52:00Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=9723
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `3.3`
### severity : `enhancement`
### contents :
When an array element is accessed in a loop, gcc makes the following optimization: it counts the address of the first array element before the loop, and then in/decreases this value by the element size within the loop. This makes the loop faster and shorter than in the case of -O1, but the overall size increases (as opposit to the purpose of -Os).

Compare the result of arm-elf-gcc -S -g0 -Os with the output created using arm-elf-gcc -S -g0 -O1. GCC should produce the later kind of output with -Os.

Release:
gcc version 3.3 20030210 (prerelease)

Environment:
BUILD & HOST: Linux 2.4.20 i686 unknown
TARGET: arm-unknown-elf

How-To-Repeat:
arm-elf-gcc -S -g0 -Os

// 01.c:

# 1 "01.c"
# 1 "<built-in>"
# 1 "<command line>"
# 1 "01.c"
typedef struct {
        int si1;
        short ss1;
        char sc1;
        int si2;
        char sc2;
        short ss2;
        short ss3;
} st;

int f1(st* p, int c, int n)
{
  int i;
  for (i = c-1; i >= 0; i--) {
    if (p[i].si1 == n) {
      return 1;
    }
  }
  return 0;
}


---


### compiler : `gcc`
### title : `[arm] Combine cannot do its job because immediate operand is used instead of register`
### open_at : `2003-02-19T17:06:00Z`
### last_modified_date : `2021-07-26T07:29:31Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=9760
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `3.3`
### severity : `enhancement`
### contents :
Combine cannot combine a shift and arithmetic insn into one insn in ARM target, because immediate is used as the second operand of the arithmetic and the combined ARM instruction can use only register for the source operand.

Release:
gcc version 3.3 20030217 (prerelease)

Environment:
BUILD & HOST: Linux 2.4.20 i686 unknown
TARGET: arm-unknown-elf

How-To-Repeat:
gcc -Os -S 01.c

// 01.c

void func(char c, int t)
{
  ;
}
void foo(int u)
{
  func ( 8, (u >> 24) & 0xffL );
  func ( 8, (u >> 16) & 0xffL );
  func ( 8, (u >> 8) & 0xffL );
}


---


### compiler : `gcc`
### title : `[ARM] Peephole for multiple load/store could be more effective.`
### open_at : `2003-02-24T15:26:00Z`
### last_modified_date : `2019-05-17T22:16:11Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=9831
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `3.3`
### severity : `enhancement`
### contents :
In the case of subsequent loads from subsequent memory locations, if the base address is not loaded into a register (e.g. the loads use a label, that will be converted to pc relative loads), the corresponding peephole patterns will not optimize. The pattern will match, but multiple load instruction will not be generated. The same apply to stores.

In the attached modified assembly code the 4 load instructions are replaced by an address computation and a multiple load (note that no additional register is required).

Release:
gcc version 3.3 20030217 (prerelease)

Environment:
BUILD & HOST: Linux 2.4.20 i686 unknown
TARGET: arm-unknown-elf

How-To-Repeat:
gcc -S -Os 01.i

// 01.i

# 1 "01.c"
# 1 "<built-in>"
# 1 "<command line>"
# 1 "01.c"
int f(int, int, int, int);

void foo ()
{
  f(12345,238764,2345234, 83746556);
}


---


### compiler : `gcc`
### title : `ifcvt is not smart enough`
### open_at : `2003-03-12T21:06:00Z`
### last_modified_date : `2023-05-26T01:01:43Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=10050
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `unknown`
### severity : `enhancement`
### contents :
Given these functions using the options -O2 -m4 -S:

int flag;

int func1(char *a)

{
        int b[3];

        b[0] = func();
        b[1] = b[0] * 2;

        a[0] = b[0];
        a[1] = b[1];

        return a[0] + b[1] + a[1];
}

int func2(int *a)

{
        int b[3];

        b[0] = func();
        b[1] = b[0] * 2;

        if (flag) {
                a[0] = b[0];
                a[1] = b[1];
        }

        return a[0] + b[1] + a[1];
}

int func3(int *a)

{
        int b[3];
        int temp0, temp1;

        b[0] = func();
        b[1] = b[0] * 2;

        temp0 = a[0];
        temp1 = a[1];

        if (flag) {
                temp0 = b[0];
                temp1 = b[1];
        }

        a[0] = temp0;
        a[1] = temp1;

        return a[0] + b[1] + a[1];
}

GCC is able to keep b[x] in registers for func1:

_func1:
        mov.l   r8,@-r15
        mov     r4,r8
        mov.l   r14,@-r15
        sts.l   pr,@-r15
        mov.l   .L2,r0
        add     #-12,r15
        jsr     @r0
        mov     r15,r14
        mov     r8,r1
        mov.b   r0,@r8
        mov     r0,r2
        add     #1,r1
        add     r2,r2
        mov.b   r2,@r1
        add     #12,r14
        mov.b   @r8,r0
        add     r2,r0
        exts.b  r2,r2
        add     r2,r0
        mov     r14,r15
        lds.l   @r15+,pr
        mov.l   @r15+,r14
        rts

However, gcc generates fairly weak code for func2. It is unable
to retain the values in registers and generates memory writes
within the conditional block:

_func2:
        mov.l   r8,@-r15
        mov     r4,r8
        mov.l   r14,@-r15
        sts.l   pr,@-r15
        mov.l   .L7,r0
        add     #-12,r15
        jsr     @r0
        mov     r15,r14
        mov.l   .L8,r1
        mov     r0,r2
        add     r2,r2
        mov.l   r0,@r14
        mov.l   @r1,r1
        tst     r1,r1
        bt/s    .L5
        mov.l   r2,@(4,r14)	<- (delay slot)
        mov.l   r0,@r8		<- conditional writes
        mov.l   r2,@(4,r8)	<- conditional writes
.L5:
        mov.l   @(4,r14),r1
        add     #12,r14
        mov.l   @r8,r0
        add     r1,r0
        mov.l   @(4,r8),r1
        add     r1,r0
        mov     r14,r15
        lds.l   @r15+,pr
        mov.l   @r15+,r14
        rts
        mov.l   @r15+,r8

To elicit the desired assembly output where no writes are emitted 
in the conditional block, it is necessary to hand-massage the
C source to something like func3, which gives this code:

func3:
        mov.l   r8,@-r15
        mov     r4,r8
        mov.l   r14,@-r15
        sts.l   pr,@-r15
        mov.l   .L12,r0
        add     #-12,r15
        jsr     @r0
        mov     r15,r14
        mov.l   .L13,r1
        mov     r0,r7
        add     r7,r7
        mov     r0,r3
        mov.l   @r1,r1
        mov.l   r0,@r14
        tst     r1,r1
        mov.l   r7,@(4,r14)
        mov.l   @r8,r2
        bt/s    .L11
        mov.l   @(4,r8),r0	(delay slot)
        mov     r3,r2		<- no memory write
        mov     r7,r0		<- no memory write
.L11:
        mov.l   r2,@r8
        add     r7,r2
        mov.l   r0,@(4,r8)
        add     #12,r14
        add     r2,r0
        mov     r14,r15
        lds.l   @r15+,pr
        mov.l   @r15+,r14
        rts
        mov.l   @r15+,r8

Toshi

Release:
unknown

Environment:
i386-linux cross sh-elf, but probably all targets

How-To-Repeat:
See above.


---


### compiler : `gcc`
### title : `induction variable analysis not used to eliminate comparisons`
### open_at : `2003-04-28T13:06:01Z`
### last_modified_date : `2023-02-18T04:10:27Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=10520
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `3.2`
### severity : `enhancement`
### contents :
When I compile the following loop (please don't mind the excess of casts etcetera - this is generated code):

unsigned int _tmp0= /* ... */;

int* buf_fast= /* ... */;

unsigned int n_in=0;
unsigned int n_out=0;
unsigned int n_in1=1;
unsigned int n_out1=1;
for(0;((n_in < _tmp0  && n_out < _tmp0) && n_in1 < _tmp0) && n_out1 < _tmp0;(((((n_in +=4,n_out +=2)),n_in1 +=4)),n_out1 +=2)){
  buf_fast[(int)n_out]=buf_fast[(int)n_in];
  buf_fast[(int)n_out1]=buf_fast[(int)n_in1];
}

The assembler output for arch=pentium4 is:

.L27:
	movl	-72(%ebp), %eax
	movl	(%edi,%eax,4), %eax
	movl	%eax, (%edi,%ecx,4)
	movl	(%edi,%esi,4), %eax
	addl	$4, -72(%ebp)
	movl	%eax, (%edi,%edx,4)
	addl	$2, %ecx
	addl	$4, %esi
	addl	$2, %edx
	cmpl	%ebx, -72(%ebp)
	jae	.L23
	cmpl	%ebx, %ecx
	jae	.L23
	cmpl	%ebx, %esi
	jae	.L23
	cmpl	%ebx, %edx
	jb	.L27

This loop contains a LOT of compares, which means that GCC doesn't induce that during the loop, the following things hold (with n = the iteration number):

n_in = 0 + 4 * n
n_in1 = 1 + 4 * n
n_out = 0 + 2 * n
n_out1 = 1 + 4 * n

and therefore:

n_in < n_in1
n_out <= n_in
n_out1 <= n_in1

Because of these relations, it would be possible for GCC to induce that if n_in1 <  _tmp0, then also n_in < _tmp0, n_out < _tmp0 and n_out1 < _tmp0. However, GCC doesn't seem to see the relationships between the variables.

Oh, before you ask: no, I can't remove the unnecessary loop conditions. :( These are part of the compiled Cyclone code and are required by the Cyclone compiler so that it can optimize away the bounds checks on the array accesses. Optimizing away these inefficiencies is a back-end job, which is why I'm reporting this to GCC.

Release:
gcc-3.2.3

Environment:
Debian unstable as of 28/04/03


---


### compiler : `gcc`
### title : `Trivial Bit Twiddling Optimizations Not Performed`
### open_at : `2003-05-23T01:55:37Z`
### last_modified_date : `2021-06-03T01:13:28Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=10945
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `3.3`
### severity : `enhancement`
### contents :
[05/22/2003 Thu 06:48.45 PM stl@nuwen ~/temp]
> ls
revised2.c  revised.c  simple2.c  simple.c

[05/22/2003 Thu 06:48.49 PM stl@nuwen ~/temp]
> gcc -O3 -fomit-frame-pointer -S *.c

[05/22/2003 Thu 06:48.58 PM stl@nuwen ~/temp]
> cat simple.c
unsigned long f(unsigned long b, unsigned long c, unsigned long d) {
        return b & c | b & d | c & d;
}

[05/22/2003 Thu 06:49.03 PM stl@nuwen ~/temp]
> cat revised.c
unsigned long g(unsigned long b, unsigned long c, unsigned long d) {
        return b & c | d & (b | c);
}

[05/22/2003 Thu 06:49.08 PM stl@nuwen ~/temp]
> cat simple.s
        .file   "simple.c"
        .text
        .p2align 4,,15
.globl f
        .type   f, @function
f:
        movl    8(%esp), %edx
        movl    12(%esp), %ecx
        movl    %edx, %eax
        orl     %ecx, %eax
        andl    %ecx, %edx
        andl    4(%esp), %eax
        orl     %edx, %eax
        ret
        .size   f, .-f
        .ident  "GCC: (GNU) 3.3"

[05/22/2003 Thu 06:49.10 PM stl@nuwen ~/temp]
> cat revised.s
        .file   "revised.c"
        .text
        .p2align 4,,15
.globl g
        .type   g, @function
g:
        movl    4(%esp), %edx
        movl    8(%esp), %ecx
        movl    %edx, %eax
        andl    %ecx, %eax
        orl     %ecx, %edx
        movl    12(%esp), %ecx
        andl    %ecx, %edx
        orl     %edx, %eax
        ret
        .size   g, .-g
        .ident  "GCC: (GNU) 3.3"

[05/22/2003 Thu 06:49.12 PM stl@nuwen ~/temp]
> cat simple2.c
unsigned long x(unsigned long b, unsigned long c, unsigned long d) {
        return b & c | ~b & d;
}

[05/22/2003 Thu 06:49.14 PM stl@nuwen ~/temp]
> cat revised2.c
unsigned long y(unsigned long b, unsigned long c, unsigned long d) {
        return d ^ b & (c ^ d);
}

[05/22/2003 Thu 06:49.17 PM stl@nuwen ~/temp]
> cat simple2.s
        .file   "simple2.c"
        .text
        .p2align 4,,15
.globl x
        .type   x, @function
x:
        movl    4(%esp), %edx
        movl    8(%esp), %ecx
        movl    %edx, %eax
        andl    %ecx, %eax
        notl    %edx
        movl    12(%esp), %ecx
        andl    %ecx, %edx
        orl     %edx, %eax
        ret
        .size   x, .-x
        .ident  "GCC: (GNU) 3.3"

[05/22/2003 Thu 06:49.19 PM stl@nuwen ~/temp]
> cat revised2.s
        .file   "revised2.c"
        .text
        .p2align 4,,15
.globl y
        .type   y, @function
y:
        movl    12(%esp), %eax
        movl    8(%esp), %edx
        movl    4(%esp), %ecx
        xorl    %eax, %edx
        andl    %ecx, %edx
        xorl    %edx, %eax
        ret
        .size   y, .-y
        .ident  "GCC: (GNU) 3.3"

[05/22/2003 Thu 06:49.22 PM stl@nuwen ~/temp]
>

The functions in simple.c and revised.c compute the same thing, yet gcc -O3 
emits different assembly instructions for them. Similarly for simple2.c and 
revised2.c. I don't know assembly, but my profiling indicates that revised.c 
may be faster than simple.c and that revised2.c is substantially faster than 
simple2.c.

I believe that these optimizations are trivial enough for the compiler to 
perform. These expressions occur in real code; they're used in the inner loop 
of the Secure Hash Standard's SHA-1.

Thanks,
Stephan T. Lavavej


---


### compiler : `gcc`
### title : `[avr-gcc] Optimization decrease performance of struct assignment.`
### open_at : `2003-06-13T02:35:59Z`
### last_modified_date : `2023-06-21T03:54:04Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=11180
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `3.3.1`
### severity : `normal`
### contents :
Any optimization level increase size and decrease speed 
for next program: 
 
	typedef struct { long lo; int in; } lo_in; 
	lo_in foo (void) 
	{ 
	    lo_in x; 
	    x.lo = 1; 
	    x.in = 2; 
	    return x; 
	} 
 
"avr-gcc -W -Wall -S -O0" produced: 
	/* File "lo_in.c": code   75 = 0x004b (  40), prologues  18, epilogues  17 */ 
"avr-gcc -W -Wall -S -Os" produced: 
	/* File "lo_in.c": code   80 = 0x0050 (  29), prologues  26, epilogues  25 */ 
"avr-gcc -W -Wall -S -O3" produced: 
	/* File "lo_in.c": code   79 = 0x004f (  28), prologues  26, epilogues  25 */ 
 
Compiler: 
	avr-gcc (GCC) 3.3.1 20030519 (prerelease)


---


### compiler : `gcc`
### title : `Weak code generated for JPEG compression`
### open_at : `2003-06-20T00:55:53Z`
### last_modified_date : `2021-11-29T00:06:43Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=11261
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `3.4.0`
### severity : `normal`
### contents :
GCC generates particularly awful code for jpeg_idct_float from the JPEG package,
which is the same code used in the EEMBC benchmark.

For the tail end of jpeg_idct_float(), there exists this code:

    outptr[0] = range_limit[(int) (( ( (INT32) (tmp0 + tmp7) ) + (((INT32) 1) 
<< ((  3 )-1)) ) >> (    3  ))
                            & (255  * 4 + 3) ];
    outptr[7] = range_limit[(int) (( ( (INT32) (tmp0 - tmp7) ) + (((INT32) 1) 
<< ((  3 )-1)) ) >> (    3  ))
                            & (255  * 4 + 3) ];
    outptr[1] = range_limit[(int) (( ( (INT32) (tmp1 + tmp6) ) + (((INT32) 1) 
<< ((  3 )-1)) ) >> (    3  ))
                            & (255  * 4 + 3) ];
    outptr[6] = range_limit[(int) (( ( (INT32) (tmp1 - tmp6) ) + (((INT32) 1) 
<< ((  3 )-1)) ) >> (    3  ))
                            & (255  * 4 + 3) ];
    outptr[2] = range_limit[(int) (( ( (INT32) (tmp2 + tmp5) ) + (((INT32) 1) 
<< ((  3 )-1)) ) >> (    3  ))
                            & (255  * 4 + 3) ];
    outptr[5] = range_limit[(int) (( ( (INT32) (tmp2 - tmp5) ) + (((INT32) 1) 
<< ((  3 )-1)) ) >> (    3  ))
                            & (255  * 4 + 3) ];
    outptr[4] = range_limit[(int) (( ( (INT32) (tmp3 + tmp4) ) + (((INT32) 1) 
<< ((  3 )-1)) ) >> (    3  ))
                            & (255  * 4 + 3) ];
    outptr[3] = range_limit[(int) (( ( (INT32) (tmp3 - tmp4) ) + (((INT32) 1) 
<< ((  3 )-1)) ) >> (    3  ))
                            & (255  * 4 + 3) ];

Unfortunately, GCC chooses to use the @(r0,rm) addressing mode for the read of
range_limit[] which causes the resulting code to be only single-issuable because
there are dependencies on r0:

        add     #4,r0
        shad    r4,r0
        and     r6,r0
        mov.b   @(r0,r7),r1
        sts     fpul,r0
        ftrc    fr1,fpul
        mov.b   r1,@r3
        add     #5,r3
        fmov    fr11,fr1
        fadd    fr6,fr1
        add     #4,r0
        fsub    fr6,fr11
        shad    r4,r0
        and     r6,r0
        mov.b   @(r0,r7),r1
        sts     fpul,r0
        ftrc    fr10,fpul
        mov.b   r1,@r3
        add     #-4,r3
        add     #4,r0
        shad    r4,r0
        and     r6,r0
        mov.b   @(r0,r7),r1
        sts     fpul,r0
        ftrc    fr1,fpul
        mov.b   r1,@r3

The instruction scheduler has very little freedom to reorder instructions
because of the overdependency on the r0 register.

This should be addressed because similar if not identical code is in the EEMBC
benchmark.

Toshi


---


### compiler : `gcc`
### title : `Pre-regalloc scheduling severely worsens performance`
### open_at : `2003-07-10T14:05:19Z`
### last_modified_date : `2023-01-16T02:38:54Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=11488
### status : `NEW`
### tags : `missed-optimization, ra`
### component : `rtl-optimization`
### version : `3.4.0`
### severity : `normal`
### contents :
This is a known problem, but there doesn't seem to be any good test case in the
database, and I think it's one of our worst performance problems currently.
Here's a nice test case:

gcc version 3.4 20030705 (experimental)

% gcc -O3 idct3.c && time ./a.out                    
./a.out  3.30s user 0.04s system 99% cpu 3.347 total    

% gcc -fno-schedule-insns -O3 idct3.c && time ./a.out
./a.out  1.19s user 0.00s system 101% cpu 1.171 total                       

i.e., slowdown of factor 2.7.

The new register allocator doesn't help a lot:

% gcc -O3 -fnew-ra idct3.c && time ./a.out
./a.out  3.09s user 0.04s system 100% cpu 3.128 total            

% gcc -fno-schedule-insns -fnew-ra -O3 idct3.c && time ./a.out
./a.out  1.24s user 0.00s system 97% cpu 1.276 total

The problem is that scheduling introduces false dependencies, which leads to
excessive spilling.


---


### compiler : `gcc`
### title : `Formulated jumps for switch`
### open_at : `2003-08-06T08:19:46Z`
### last_modified_date : `2021-11-04T01:40:44Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=11822
### status : `SUSPENDED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `3.4.0`
### severity : `enhancement`
### contents :
In some cases the jump table used for implementing a C switch statement could be
replaced with a jump to a calculated address. This can be done if the jump table
contains an appropriate pattern which can be formulated into a
function/calculation.
A simple example is the case when the code sizes of case blocks are equal and
each case label is addressable with one data processing instruction. In this
case GCC could compute the size of case blocks and multiply them by the switch
condition value and modify pc with this value.
It could also be possible to rearrange the jump table into regions with this
"formulated jumps" mechanism.
GCC should use this mechanism when optimizing for size.

--- example ---
// arm-elf-gcc -S -g0 -Os -o form-jump.s form-jump.c
void func (int);
void foo (int a)
{
  switch(a)
  {
    case 15:
     func(5);
    case 16:
     func(59);
    case 17:
     func(515);
    case 18:
     func(65);
    case 19:
     func(8);
    case 20:
     func(15);
  }
}

--- arm code ---
foo:
 mov ip, sp
 sub r0, r0, #15
 stmfd sp!, {fp, ip, lr, pc}
 sub fp, ip, #4
 cmp r0, #5
 ldrls pc, [pc, r0, asl #2]
 b .L1
 .p2align 2
.L9:
 .word .L3
 .word .L4
 .word .L5
 .word .L6
 .word .L7
 .word .L8
.L3:
 mov r0, #5
 bl func
.L4:
 mov r0, #59
 bl func
.L5:
 ldr r0, .L10
 bl func
.L6:
 mov r0, #65
 bl func
.L7:
 mov r0, #8
 bl func
.L8:
 mov r0, #15
 ldmea fp, {fp, sp, lr}
 b func
.L1:
 ldmea fp, {fp, sp, pc} 

--- possible solution ---
foo:
 mov ip, sp
 sub r0, r0, #15
 stmfd sp!, {fp, ip, lr, pc}
 sub fp, ip, #4
 cmp r0, #5
 addls pc, pc, r0, asl #3
 b .L1
.L3:
 mov r0, #5
 bl func
.L4:
 mov r0, #59
 bl func
.L5:
 ldr r0, .L10
 bl func
.L6:
 mov r0, #65
 bl func
.L7:
 mov r0, #8
 bl func
.L8:
 mov r0, #15
 ldmea fp, {fp, sp, lr}
 b func
.L1:
 ldmea fp, {fp, sp, pc}


---


### compiler : `gcc`
### title : `[ARM] ifcvt: Logical expression evaluation with condition fields`
### open_at : `2003-08-06T09:35:41Z`
### last_modified_date : `2023-05-27T07:30:12Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=11831
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `3.4.0`
### severity : `enhancement`
### contents :
For translating a compound logical expression GCC uses an ldm instruction to
interrupt the evaluation of conditions fields. When optimizing for size
it would be promising to use condition fields instead of the ldm, if possible.

--- c example ---
int func(char*);
int foo (char* name)
{
   int n = func (name);
   return
      (name[n-4] == 'a' &&
       name[n-3] == 'b' &&
       name[n-2] == 'c' &&
       name[n-1] == 'd');
}

--- arm code ---
foo:
 mov ip, sp
 stmfd sp!, {r4, fp, ip, lr, pc}
 sub fp, ip, #4
 mov r4, r0
 bl func
 add r4, r4, r0
 ldrb r3, [r4, #-4]
 cmp r3, #97
 mov r0, #0 <- OLD
 ldmneea fp, {r4, fp, sp, pc} <- OLD
 ldrb r3, [r4, #-3] <- OLD
 cmp r3, #98 <- OLD
 ldmneea fp, {r4, fp, sp, pc} <- OLD
 ldrb r3, [r4, #-2] <- OLD
 cmp r3, #99 <- OLD
 ldmneea fp, {r4, fp, sp, pc} <- OLD
 ldrb r3, [r4, #-1] <- OLD
 cmp r3, #100 <- OLD
 movne r0, #0
 moveq r0, #1
 ldmea fp, {r4, fp, sp, pc}

--- possible solution ---
foo:
 mov ip, sp
 stmfd sp!, {r4, fp, ip, lr, pc}
 sub fp, ip, #4
 mov r4, r0
 bl func
 add r4, r4, r0
 ldrb r3, [r4, #-4]
 cmp r3, #97
 ldreqb r3, [r4, #-3] <- NEW
 cmpeq r3, #98 <- NEW
 ldreqb r3, [r4, #-2] <- NEW
 cmpeq r3, #99 <- NEW
 ldreqb r3, [r4, #-1] <- NEW
 cmpeq r3, #100 <- NEW
 movne r0, #0
 moveq r0, #1
 ldmea fp, {r4, fp, sp, pc}


---


### compiler : `gcc`
### title : `Optimization of common stores in switch statements`
### open_at : `2003-08-06T09:45:08Z`
### last_modified_date : `2021-11-04T01:40:25Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=11832
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `3.4.0`
### severity : `enhancement`
### contents :
If a C switch statement contains common code among certain case branches,
GCC isn't able to combine the common code.
Reorganization of the switch may solve this problem.

--- c example ---
int a, b, e;
unsigned char *c;
void foo()
{
  int d = 13;
  b = -1;   
  switch (e) {
    case 1:
      b++; c[b] = (unsigned char)d;
      break;
    case 2:
      b++; c[b] = (unsigned char)d;
      b++; c[b] = (unsigned char)d;
      break;
    case 3:
      b++; c[b] = (unsigned char)d;
      b++; c[b] = (unsigned char)d;
      b++; c[b] = (unsigned char)d;
      break;
    default:
      a = 1;
      b++; c[b] = (unsigned char)d;
      b++; c[b] = (unsigned char)d;
      b++; c[b] = (unsigned char)d;
      b++; c[b] = (unsigned char)d;
  }
}

--- arm code ---
foo:
 stmfd sp!, {r4, lr}
 ldr r3, .L10
 ldr r2, [r3, #0]
 ldr lr, .L10+4
 mvn r3, #0
 cmp r2, #2
 str r3, [lr, #0]
 mov r4, #13
 beq .L4
 bgt .L7
 cmp r2, #1
 beq .L3
 b .L6
.L7:
 cmp r2, #3
 beq .L5
 b .L6
.L3:
 ldr r3, .L10+8
 ldr r2, [r3, #0]
 mov r3, #0
 str r3, [lr, #0]
 strb r4, [r2, #0]
 ldmfd sp!, {r4, pc}
.L4:
 ldr r1, .L10+8
 ldr r2, [r1, #0]
 mov r3, #0
 str r3, [lr, #0]
 strb r4, [r2, #0]
 ldr r3, [lr, #0]
 ldr r2, [r1, #0]
 b .L8
.L5:
 ldr r2, .L10+8
 ldr r1, [r2, #0]
 mov r3, #0
 str r3, [lr, #0]
 strb r4, [r1, #0]
 ldr r3, [lr, #0]
 ldr r1, [r2, #0]
 add r3, r3, #1
 str r3, [lr, #0]
 strb r4, [r1, r3]
 ldr r3, [lr, #0]
 ldr r2, [r2, #0]
.L8:
 add r3, r3, #1
.L9:
 str r3, [lr, #0]
 strb r4, [r2, r3]
 ldmfd sp!, {r4, pc}
.L6:
 ldr r0, .L10+8
 ldr r2, [lr, #0]
 ldr ip, [r0, #0]
 ldr r3, .L10+12
 mov r1, #1
 add r2, r2, #1
 str r2, [lr, #0]
 str r1, [r3, #0]
 strb r4, [ip, r2]
 ldr r3, [lr, #0]
 ldr r2, [r0, #0]
 add r3, r3, r1
 str r3, [lr, #0]
 strb r4, [r2, r3]
 ldr r3, [lr, #0]
 ldr r2, [r0, #0]
 add r3, r3, r1
 str r3, [lr, #0]
 strb r4, [r2, r3]
 ldr r3, [lr, #0]
 ldr r2, [r0, #0]
 add r3, r3, r1
 b .L9


---


### compiler : `gcc`
### title : `memcmp(i,j,4) should use word (SI) subtraction`
### open_at : `2003-08-28T03:00:40Z`
### last_modified_date : `2020-08-13T19:36:53Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=12086
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `3.4.0`
### severity : `enhancement`
### contents :
It would be nice if memcmp is inlined for small n's
It would be nice if these two functions are the same:
int g(int *j,int *l)  {  return memcmp(j,l,4);  }
int h(int *j, int *l) {  return *j - *l;                   }
This save space (not in this function on PPC because of sibcall but it could because gcc 
does not have to spill to much more to go over the function call) and time (because no 
function overhead on targets where memcmp is not inlined like PPC).


---


### compiler : `gcc`
### title : `eliminate and warn on dynamic casts with known NULL results`
### open_at : `2003-09-14T16:40:17Z`
### last_modified_date : `2021-10-01T10:22:44Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=12277
### status : `NEW`
### tags : `diagnostic, missed-optimization`
### component : `c++`
### version : `3.4.0`
### severity : `enhancement`
### contents :
While this can not be done generally - if the inheritence relation between the
type being cast from and the type being cast to is known at the time of use,
there are some cases where a dynamic cast can be sure to return NULL.  I can not
think of any valid use of a dynamic cast which will always return NULL - so
therefore I suggest that a warning be given.
The specific case which bothered me (and hence why i'm writing this) is
upcasting through private inheritence always gives NULL for dynamic cast.


---


### compiler : `gcc`
### title : `GOT pointer (r12) reloaded unnecessarily`
### open_at : `2003-09-16T22:19:18Z`
### last_modified_date : `2021-09-12T22:26:44Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=12306
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `3.4.0`
### severity : `enhancement`
### contents :
On the Renesas SH, the register r12 is fixed and reserved for the pointer to the
GOT. However, the code emitted saves r12 and reloads r12.

int a, b; int foo(void) { return a + b; }

compiled with -O2 -m4 -fPIC -S produces:

_foo:
        mov.l   r12,@-r15		<- r12 saved to stack
        mova    .L3,r0
        mov.l   .L3,r12
        mov.l   r14,@-r15
        add     r0,r12			<- r12 (GOT pointer) rebuilt
        mov.l   .L4,r0
        sts.l   pr,@-r15
        mov.l   @(r0,r12),r1
        mov     r12,r0
        mov     r15,r14
        mov.l   @r1,r2
        mov.l   .L5,r1
        mov.l   @(r0,r1),r1
        mov.l   @r1,r1
        add     r1,r2
        mov     r2,r0
        mov     r14,r15
        lds.l   @r15+,pr
        mov.l   @r15+,r14
        rts
        mov.l   @r15+,r12		<- r12 restored


---


### compiler : `gcc`
### title : `Suboptimal code with global variables`
### open_at : `2003-09-24T23:17:50Z`
### last_modified_date : `2021-08-23T06:58:00Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=12395
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `3.4.0`
### severity : `enhancement`
### contents :
Consider this tiny function:

void foo() {
        extern int a;
        if(++a) ++a;
}

It produces the following assembly with 3.4 (experimental) and 3.2 (Red Hat 9)
at -O2 and better:

        .file   "t.c"
        .text
.globl foo
        .type   foo, @function
foo:
        movl    a, %eax
        incl    %eax
        testl   %eax, %eax
        movl    %eax, a
        je      .L1
        incl    %eax
        movl    %eax, a
.L1:
        ret
        .size   foo, .-foo
        .section        .note.GNU-stack,"",@progbits
        .ident  "GCC: (GNU) 3.5-tree-ssa 20030924 (merged 20030817)"

This is subobtimal. The optimal code should be:

foo:
        addl    $1,a
        je      .L1
        addl    $1,a
.L1:
        ret


---


### compiler : `gcc`
### title : `testing divisibility by constant`
### open_at : `2003-10-30T22:06:22Z`
### last_modified_date : `2019-05-31T21:10:25Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=12849
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `3.3.2`
### severity : `enhancement`
### contents :
I believe tests of divisibility by a constant (ie. n % d == 0, where d
is a compile-time constant) can be improved by the technique described
in section 9 of "Division by Invariant Integers using Multiplication"
by Granlund and Montgomery.

	ftp://ftp.cwi.nl/pub/pmontgom/divcnst.psa4.gz

(This section of this paper is what's currently used in gcc for exact
division by a constant arising from pointer subtraction, but the
divisibility tests managed to escape implementation. :-)

Environment:
System: Linux blah 2.2.15 #1 Tue Apr 25 17:13:48 EST 2000 i586 unknown unknown GNU/Linux
Architecture: i586
	<machine, os, target, libraries (multiple lines)>
host: i486-pc-linux-gnu
build: i486-pc-linux-gnu
target: i486-pc-linux-gnu
configured with: ../src/configure -v --enable-languages=c,c++,java,f77,pascal,objc,ada,treelang --prefix=/usr --mandir=/usr/share/man --infodir=/usr/share/info --with-gxx-include-dir=/usr/include/c++/3.3 --enable-shared --with-system-zlib --enable-nls --without-included-gettext --enable-__cxa_atexit --enable-clocale=gnu --enable-debug --enable-java-gc=boehm --enable-java-awt=xlib --enable-objc-gc i486-linux

How-To-Repeat:
A little function like,

	void
	bar (unsigned n)
	{
	  if (n % 3 == 0)
	    true ();
	  else
	    false ();
	}

compiled with

	gcc -march=athlon -mcpu=athlon -O3 -fomit-frame-pointer -S dive.c

currently comes out with

        movl    4(%esp), %ecx
        movl    $1639179445, %edx
        movl    %ecx, %eax
        mull    %edx
        shrl    $16, %edx
        imull   $171717, %edx, %edx
        cmpl    %edx, %ecx
	...

I believe instead this could be something like

        movl    4(%esp), %ecx
	imull	$0x4B45300D, %ecx
	cmpl	$0x61B3, %ecx
	...

Notice there's only one low-half multiply, as opposed to a high-half
plus a low-half above.

An even divisor will require an extra rotl (or a separate test of some
low bits), but still ought to be smaller and faster in all cases.


If the actual value of the remainder is wanted then this technique
wouldn't help, it's only for a test for == 0 (or particular values).

When the input does prove to be divisible, then the mul shown gives
the quotient.  Maybe that could be noted on the corresponding side of
the branch, in case it allowed for some CSE.


---


### compiler : `gcc`
### title : `if-conversion not agressive enough`
### open_at : `2004-01-04T17:02:01Z`
### last_modified_date : `2023-06-09T14:50:37Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=13563
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `3.4.0`
### severity : `enhancement`
### contents :
bar could be optimized to baz.
current mainline uses a jump for bar,
but baz uses setcc

void foo (int);

int
bar (int a)
{
  if (a)
    foo (1);
  else
    foo (0);
}

int
baz (int a)
{
  foo (!!a);
}


---


### compiler : `gcc`
### title : `[tree-ssa] make "fold" use alias information to optimize pointer comparisons`
### open_at : `2004-02-01T18:22:50Z`
### last_modified_date : `2023-06-05T06:46:06Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=13962
### status : `ASSIGNED`
### tags : `alias, missed-optimization, xfail`
### component : `tree-optimization`
### version : `tree-ssa`
### severity : `enhancement`
### contents :
Given 2 pointers p and q, if the alias information says that p and q 
cannot alias, then comparisons like p == q and p != q can be optimized away.

There are quite a few examples in:

testsuite/gcc.dg/tree-ssa/ssa-ccp-3.c


---


### compiler : `gcc`
### title : `Unneeded C++ types are output in debug info due to use of static constants`
### open_at : `2004-02-17T04:50:33Z`
### last_modified_date : `2020-12-07T22:27:44Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=14167
### status : `WAITING`
### tags : `missed-optimization, wrong-debug`
### component : `c++`
### version : `3.4.0`
### severity : `normal`
### contents :
Take this testcase:
class Class1 {
  static const int var1 = 1;
  static const int var2 = var1;
};

class Class2 {
  static const int var1 = 1;
  static const int var2 = 1;
};

Compile it with -gdwarf-2.  Debug information for Class2 will not be emitted,
which is OK, because Class2 is unused.  Debug information for Class1 will be
emitted, because Class1::var1 is marked as used in the initializer for Class1::var2,
which causes Class1::var1 to be emitted, which causes all of Class1 to be emitted.

It gets marked used in finish_id_expression as I expected:
2581          if (TREE_CODE (decl) == VAR_DECL
2582              || TREE_CODE (decl) == PARM_DECL
2583              || TREE_CODE (decl) == RESULT_DECL)
2584            mark_used (decl);

Is the used marker necessary in integral constant-expressions?  Where else?

This is the source of about 60% of the (60k!) debug information emitted for the
"trivial" C++ program:
#include <iostream>
int main() { return 0; }


---


### compiler : `gcc`
### title : `GCC generates pessimizes code for integer division`
### open_at : `2004-02-20T11:38:42Z`
### last_modified_date : `2021-06-08T08:59:01Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=14224
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `3.3.3`
### severity : `enhancement`
### contents :
When dividing a 64 bit integer by a 32 bit integer (normal division or
remainder), gcc uses __umoddi3 even though the intel instruction 'div' can do
this natively.

On my machine, this bad assembly has a speed impact of at least 1.5* by simply
replacing the call with 'div' and no further optimizations applied.

These types of operations (multiplication and then modulus division) are very
common in cryptography and coding theory. It is quite possible that fixing this
bug would greatly improve gcc's performance in these areas.

I have confirmed that this bug applies to versions 3.5, 3.4, and 2.95.4 in
addition to the 3.3.3 against which it is filed.

The example program is:

#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
 
int main(int argc, char** argv)
{
        int i = 0;
        uint32_t x = atol(argv[1]), y = atol(argv[2]), z = 0;
         
        for (i = 0; i < 1000000000; ++i)
        {
                z += ((uint64_t)x*(uint64_t)y) % 3221225473UL;
                ++x; ++y;
        }
         
        printf("%d\n", z);
         
        return 0;
}

Compile with gcc -O2 foo.c -o foo (version 3.3.3).
Then generate the assembly gcc -O2 foo.c -o foo.s and apply this patch:

47,54c47,64
<       movl    %eax, (%esp)
<       xorl    %eax, %eax
<       movl    %edx, 4(%esp)
<       movl    $-1073741823, %edx
<       movl    %edx, 8(%esp)
<       movl    %eax, 12(%esp)
<       call    __umoddi3
<       addl    %eax, -16(%ebp)
---
>
> // stuff from gcc:
> //    movl    %eax, (%esp)
> //    xorl    %eax, %eax
> //    movl    %edx, 4(%esp)
> //    movl    $-1073741823, %edx
> //    movl    %edx, 8(%esp)
> //    movl    %eax, 12(%esp)
> //    call    __umoddi3
> //    addl    %eax, -16(%ebp)
>
> // my custom assembly:
>       movl    $-1073741823, %ecx
>       div     %ecx
>       addl    %edx, -16(%ebp)
>
> // --- end changes
>

Now compile the assembly (gcc foo.s -o foo2) and compare the results and the
speed difference. It is quite likely that gcc could do an even better job
through good pipelining and better register assignment. Furthermore, in this
particular example code, the divisor is a constant which might allow gcc to even
optimize away the div altogether. However, I have no idea what the performance
impact of this would be.


---


### compiler : `gcc`
### title : `[tree-ssa] copy propagation for aggregates`
### open_at : `2004-02-25T17:37:49Z`
### last_modified_date : `2022-01-06T00:12:12Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=14295
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `tree-ssa`
### severity : `enhancement`
### contents :
This is a (possible?) enhancement request. 
There already is a testcase in the testsuite for this: 20031106-6.c

struct s
{
  char d;
  int a, b;
  double m;
};

struct s foo (struct s r)
{
  struct s temp_struct1;
  struct s temp_struct2;
  struct s temp_struct3;
  temp_struct1 = r;
  temp_struct2 = temp_struct1;
  temp_struct3 = temp_struct2;
  return temp_struct3;
}

The .optimized dump is: 

foo (r)
{
  double r$m;
  int r$b;
  int r$a;
  struct s temp_struct3;

<bb 0>:
  r$a = r.a;
  r$b = r.b;
  r$m = r.m;
  temp_struct3.d = r.d;
  temp_struct3.a = r$a;
  temp_struct3.b = r$b;
  temp_struct3.m = r$m;
  return temp_struct3;
}

It would be nice if it would be just "return r;"

SRA could take care of things like this, but that might be much more work, plus
it precludes from using more optimized memory copy sequences for 
aggregate copying instead of series of loads and store. 

BTW, the above code seems strange too, temporaries are created for r.a, r.b 
and r.m, but not for r.d 

Another compiler produces the following assembly:

        mov     eax, DWORD PTR $T552[esp-4]
        push    esi
        push    edi
        mov     ecx, 6
        lea     esi, DWORD PTR _r$[esp+4]
        mov     edi, eax
        rep movsd
        pop     edi
        pop     esi


---


### compiler : `gcc`
### title : `Unnecessary loads and stores for tail call`
### open_at : `2004-03-03T21:11:13Z`
### last_modified_date : `2021-07-19T23:44:51Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=14418
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `3.3`
### severity : `normal`
### contents :
In a certain case on i386, when a tail call to a function is made
giving the same arguments as the calling function had, those arguments
are loaded from the stack and then stored back, whereas since they're
unchanged I believe there's no need to do that.

Environment:
System: Linux blah 2.2.15 #1 Tue Apr 25 17:13:48 EST 2000 i586 unknown unknown GNU/Linux
Architecture: i586
	<machine, os, target, libraries (multiple lines)>
host: i486-pc-linux-gnu
build: i486-pc-linux-gnu
target: i486-pc-linux-gnu
configured with: ../src/configure -v --enable-languages=c,c++,java,f77,pascal,objc,ada,treelang --prefix=/usr --mandir=/usr/share/man --infodir=/usr/share/info --with-gxx-include-dir=/usr/include/c++/3.3 --enable-shared --with-system-zlib --enable-nls --without-included-gettext --enable-__cxa_atexit --enable-clocale=gnu --enable-debug --enable-java-gc=boehm --enable-java-awt=xlib --enable-objc-gc i486-linux

How-To-Repeat:
A file foo.c,

	void
	foo (int x, int y)
	{
	  bar (2*x);
	  quux (x, y);
	}

compiled with

	gcc -O3 -fomit-frame-pointer -S foo.c

produces foo.s,

foo:
        subl    $28, %esp
        movl    %ebx, 20(%esp)
        movl    32(%esp), %ebx
        movl    %esi, 24(%esp)
        movl    36(%esp), %esi
        leal    (%ebx,%ebx), %edx
        movl    %edx, (%esp)
        call    bar
        movl    %esi, 36(%esp)
        movl    24(%esp), %esi
        movl    %ebx, 32(%esp)
        movl    20(%esp), %ebx
        addl    $28, %esp
        jmp     quux

Notice parameters x and y are loaded from 32(%esp) and 36(%esp) into
ebx and esi, and then stored back to the exact same locations for the
tail call to quux.  I believe this should be unnecessary.

No doubt when parameters are changed around then some juggling is
necessary, but it'd be nice if gcc could notice when the locations
it's filling already contain the values wanted.

For what it's worth I noticed this in a bit of code in GMP not unlike
the above.


---


### compiler : `gcc`
### title : `[tree-ssa] missed sib calling when types change`
### open_at : `2004-03-05T06:22:42Z`
### last_modified_date : `2022-11-01T19:50:22Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=14441
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `tree-ssa`
### severity : `enhancement`
### contents :
Sib calling can happen on some targets (like the PPC) when the types are always 
sign_extended when they are returned like from short to int.
short t();
int f()
{
 return t();
}


---


### compiler : `gcc`
### title : `Structs that cannot alias are not SRA'd`
### open_at : `2004-03-06T04:31:02Z`
### last_modified_date : `2019-03-04T13:03:31Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=14455
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `tree-ssa`
### severity : `enhancement`
### contents :
Often in inner loops (no child functions called, big loop count), there will be several (many!) Altivec 
registers left unused.

The attached file demonstrates the problem, when built with tree-ssa with:

%PREFIX/bin/g++ -Winline -mdynamic-no-pic -fno-exceptions -O3 -maltivec -fstrict-aliasing 
-finline-functions -finline-limit=1000000000 -falign-loops=16 --param large-function-
growth=1000000 --param inline-unit-growth=1000 iterator_10.cpp -S -o /tmp/iterator_10.s

In my real world code, this is a big problem since I'm have code that does:

    - long computation for some answer
    - compute some address to ADD to the answer to (and the address is almost never in cache)
    - load from answer address
    - start on next loop
    - add answer and old answer and store

The problem is that the compiler totally blows the approach since it immediately stores the loaded 
old answer to the stack, causing a stall waiting for the load to complete (and thus preventing any 
asynchrony with the load and the computation in the next loop).


---


### compiler : `gcc`
### title : `More aggressive compare insn elimination`
### open_at : `2004-03-08T16:47:56Z`
### last_modified_date : `2023-08-08T01:14:44Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=14483
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.0.0`
### severity : `enhancement`
### contents :
Consider:

void bar_0 (void);
void bar_1 (void);

void
foo (int a)
{
  if (a == 1)
    goto L0;
  if (a == 0)
    goto L1;
  return;

 L0:
  bar_0 ();
  return;

 L1:
  bar_1 ();
  return;
}

./cc1 -O2 -fomit-frame-pointer generates

foo:
	movl	4(%esp), %eax
	cmpl	$1, %eax
	je	.L2
	testl	%eax, %eax      <- sort of redundant
	je	.L4
	ret
	.p2align 2,,3
.L4:
	jmp	bar_1
	.p2align 2,,3
.L2:
	jmp	bar_0

At point where "testl" is, we still have the result of the last cmpl.
So we could do:

foo:
	movl	4(%esp), %eax
	cmpl	$1, %eax
	je	.L2
	jb	.L4          <- Notice, no "testl"!
	ret
	.p2align 2,,3
.L4:
	jmp	bar_1
	.p2align 2,,3
.L2:
	jmp	bar_0


---


### compiler : `gcc`
### title : `Missed Bit Twiddling Optimization`
### open_at : `2004-03-09T17:16:58Z`
### last_modified_date : `2019-03-06T05:14:43Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=14504
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `3.3.2`
### severity : `enhancement`
### contents :
g++ 3.3.2 on i686-pc-linux-gnu with -s -O3 -fomit-frame-pointer compiles:

unsigned long cond_mask(bool flag, unsigned long mask, unsigned long target) {
    return flag ? target | mask : target & ~mask;
}

into:

cmpb    $0, 4(%esp)
movl    8(%esp), %eax
movl    12(%esp), %edx
je      .L2
orl     %edx, %eax
ret
.L2:
notl    %eax
andl    %edx, %eax
ret

This appears to be a straightforward translation of the code into assembly. 
With the same options, this:

unsigned long cond_mask(bool flag, unsigned long mask, unsigned long target) {
    return (mask | target ^ 0xFFFFFFFFUL + flag) ^ 0xFFFFFFFFUL + flag;
}

is compiled into:

movzbl  4(%esp), %edx
movl    12(%esp), %eax
movl    8(%esp), %ecx
decl    %edx
xorl    %edx, %eax
orl     %ecx, %eax
xorl    %edx, %eax
ret

Again this appears to be a straightforward translation of the code into 
assembly (instead of flag + 0xFFFFFFFFUL, it uses static_cast<unsigned long>
(flag) - 1, which is the same thing).

However, the rewritten code lacks a branch yet does the exact same thing.

g++ ought to be able to perform this reasonably simple transformation on its 
own - if, indeed, the transformation is desirable (which I think it is).

NB:
I do not know assembly, so I may have deleted important information from g++'s 
output. I don't think I have, however.

This case was suggested by ryanm@microsoft.com, who said "this is something I 
will never expect a compiler to be able to optimize for me.  ^_^". I wrote the 
transformed code; perhaps there is a cleverer way to transform it which I am 
not aware of.


---


### compiler : `gcc`
### title : `__builtin_constant_p(__func__) is not true`
### open_at : `2004-03-09T18:21:33Z`
### last_modified_date : `2022-11-29T02:35:31Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=14505
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `3.3`
### severity : `enhancement`
### contents :
The following code emits "non constant" but conceptually should emit "constant". The type of __func__ 
is "static const char *" so either fold_builtin_constant_p needs to be relaxed a bit or fname_decl should 
be building STRING_CST.

int main(int argc, char **argv)
{ 
  puts (__builtin_constant_p(__func__) ? "constant" : "non constant");
}


---


### compiler : `gcc`
### title : `new/delete much slower than malloc/free because of sjlj exceptions`
### open_at : `2004-03-12T23:36:06Z`
### last_modified_date : `2021-02-21T17:41:13Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=14563
### status : `RESOLVED`
### tags : `EH, missed-optimization, sjlj-eh`
### component : `target`
### version : `3.3.3`
### severity : `normal`
### contents :
I am sorry if this report is imprecise and probably unhelpful but several
contributers to octave lists have failed to identify where the problem lies.

The problem is simply stated and is unique to builds of octave-2.1.xx under
latest version of Cygwin: interpreted octave programmes run 6-7 times slower
when compiled and linked with gcc-3.3.3 and its libraries, compared with 3.2.3.

Note that (i) This is problem is not present in Linux and (ii) is not dependent
on which continent one is in!  ie. This problem is reproducible.

Beyond this, a variety of optimisation levels, architecture settings and so on
were tried, to no avail.


---


### compiler : `gcc`
### title : `[tree-ssa] suboptimal code ('0' <= c && c <= '9') ? c - '0' : 0`
### open_at : `2004-03-17T09:03:15Z`
### last_modified_date : `2023-05-05T06:36:58Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=14617
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `tree-ssa`
### severity : `enhancement`
### contents :
Here is what I get with the current tree-ssa:

int
foo (char c)
{
  return ('0' <= c && c <= '9') ? c - '0' : 0;
}
/*
	movzbl	4(%esp), %ecx
	xorl	%eax, %eax
	movb	%cl, %dl
	subb	$48, %dl
	cmpb	$9, %dl
	ja	.L4
	movsbl	%cl,%eax      ; extending again (but this time sign-ext)?
	subl	$48, %eax     ; again subtracting 48 (but in different mode)?
.L4:
	ret
*/

int
bar (char c)
{
  c -= '0';
  return ((unsigned char) c <= 9) ? c : 0;
}
/*
	movzbl	4(%esp), %ecx
	xorl	%eax, %eax
	subb	$48, %cl
	movsbl	%cl,%edx      ; extending again (but this time sign-ext)?
	cmpb	$10, %cl
	cmovb	%edx, %eax
*/

int
baz (char c)
{
  int tem = c;
  tem -= '0';
  return ((unsigned char) tem <= 9) ? tem : 0;
}
/*
	movsbl	4(%esp), %edx
	xorl	%eax, %eax
	subl	$48, %edx
	cmpb	$10, %dl
	cmovb	%edx, %eax
*/

For "foo", here is what I get right before TER:

foo (c)
{
  unsigned int tem;
  unsigned char T.6;
  int iftmp.5;
  unsigned char c.4;
  int T.3;
  unsigned char T.2;
  char T.1;
  int iftmp.0;

<bb 0>:
  T.1_3 = c_2 - 48;
  T.2_4 = (unsigned char)T.1_3;
  if (T.2_4 <= 9) goto <L0>; else goto <L2>;

<L0>:;
  T.3_7 = (int)c_2;
  iftmp.0_8 = T.3_7 - 48;

  # iftmp.0_1 = PHI <0(0), iftmp.0_8(1)>;
<L2>:;
  return iftmp.0_1;

}

Note that if we extended c_2 earlier and did all the computation in int
wherever possible, it would be pretty easy to avoid subtracting of 48 twice.
The idea of extending everything first comes from a paper

Effective Sign Extension Elimination
Kawahito, Komatsu, and Nakatani
http://www.trl.ibm.com/projects/jit/paper/sxt.pdf


---


### compiler : `gcc`
### title : `[ix86] tail call optimization missed with stdcall attribute`
### open_at : `2004-03-18T00:45:29Z`
### last_modified_date : `2022-01-06T00:04:07Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=14625
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `3.4.0`
### severity : `enhancement`
### contents :
On x86, when the regparm and stdcall attributes are used the compiler misses
some optimizations to perform tail calls.  Example: 
                                                                     
static int
__attribute__ ((noinline, stdcall, regparm (3)))
foo (int a, int b, int c, int d, int e)
{
  return a + b + c + d + e;
}
int
__attribute__ ((regparm (3)))
bar (int a, int b)
{
  return foo (a, b, 1, 2, 3);
}

The code generated with

  gcc -O2 -fomit-frame-pointer -mpreferred-stack-boundary=2

is (only bar is interesting):

00000010 <bar>:
  10:   6a 02                   push   $0x2
  12:   6a 01                   push   $0x1
  14:   e8 e7 ff ff ff          call   0 <foo>
  19:   c3                      ret

If the code would be generated like

        movl (%esp), %ecx
        subl $8, %esp
        movl $3, 8(%esp)
        movl %ecx, (%esp)
        movl $2, 4(%esp)
        movl $1, %ecx
        jmp foo

the tail call is possible.  You could also use

       pop %ecx
       pushl $3
       pushl $2
       pushl %ecx
       movl $1, %ecx
       jmp foo

which would be shorter.

The same problem from a different angle: if you remove the attribute from foo,
gcc generates this code:

  10:   8b 44 24 04             mov    0x4(%esp,1),%eax
  14:   8b 54 24 08             mov    0x8(%esp,1),%edx
  18:   6a 03                   push   $0x3
  1a:   b9 01 00 00 00          mov    $0x1,%ecx
  1f:   6a 02                   push   $0x2
  21:   e8 da ff ff ff          call   0 <foo>
  26:   c3                      ret

In this case the optimized code could look like this:

        movl 4(%esp), %eax
        movl 8(%esp), %edx
        movl $1, %ecx
        movl $2, 4(%esp)
        movl $3, 8(%esp)
        jmp foo


Both cases are quite frequent when stdcall + regparm is used (e.g., in glibc). 
The latter one is used in exported interfaces which are simple wrappers around
internal interfaces.


---


### compiler : `gcc`
### title : `jump optimization involving a sibling call within a jump table`
### open_at : `2004-03-24T17:42:07Z`
### last_modified_date : `2021-08-19T03:39:18Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=14721
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.0.0`
### severity : `enhancement`
### contents :
We could put a function address in a jump table.

void bar0 (void);
void bar1 (void);
void bar2 (void);
void bar3 (void);
void bar4 (void);

void
foo (int i)
{
  switch (i)
    {
    case 0: bar0 (); break;
    case 1: bar1 (); break;
    case 2: bar2 (); break;
    case 3: bar3 (); break;
    case 4: bar4 (); break;
    }
}

Here is what I get on i686-pc-linux-gnu.

foo:
	movl	4(%esp), %eax
	cmpl	$4, %eax
	ja	.L1
	jmp	*.L8(,%eax,4)
	.section	.rodata
	.align 4
	.align 4
.L8:
	.long	.L3
	.long	.L4
	.long	.L5
	.long	.L6
	.long	.L7
	.text
	.p2align 2,,3
.L1:
	ret
.L7:
	jmp	bar4
.L3:
	jmp	bar0
.L4:
	jmp	bar1
.L5:
	jmp	bar2
.L6:
	jmp	bar3

It would be nice if I can get something like:

foo:
	movl	4(%esp), %eax
	cmpl	$4, %eax
	ja	.L1
	jmp	*.L8(,%eax,4)
	.section	.rodata
	.align 4
	.align 4
.L8:
	.long	bar0
	.long	bar1
	.long	bar2
	.long	bar3
	.long	bar4
	.text
	.p2align 2,,3
.L1:
	ret


---


### compiler : `gcc`
### title : `[tree-ssa] some missed forward propagation opportunities`
### open_at : `2004-03-27T16:13:47Z`
### last_modified_date : `2023-06-07T00:40:53Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=14753
### status : `NEW`
### tags : `missed-optimization, TREE`
### component : `tree-optimization`
### version : `tree-ssa`
### severity : `enhancement`
### contents :
void bar (void);

void
foo (unsigned int a)
{
  /* This one is equivalent to a >= (3 << 2).  */
  if ((a >> 2) >= 3)
    bar ();
}

void
baz (unsigned int a)
{
  /* This one is equivalent to a <= 7.  */
  if ((a & ~7) == 0)
    bar ();
}

The last tree in SSA form looks like:

;; Function foo (foo)

foo (a)
{
  unsigned int T.0;

<bb 0>:
  T.0_2 = a_1 >> 2;
  if (T.0_2 > 2) goto <L0>; else goto <L1>;

<L0>:;
  bar () [tail call];

<L1>:;
  return;

}



;; Function baz (baz)

baz (a)
{
  unsigned int T.1;

<bb 0>:
  T.1_2 = a_1 & 0fffffff8;
  if (T.1_2 == 0) goto <L0>; else goto <L1>;

<L0>:;
  bar () [tail call];

<L1>:;
  return;

}

Note that in baz(), if "a" were of int, we would first have to create
a temporary variable holding unsigned version of "a" before we can
use an ordered comparison.


---


### compiler : `gcc`
### title : `[tree-ssa] convert a sequence of "if"s to a "switch" statement`
### open_at : `2004-03-31T11:24:48Z`
### last_modified_date : `2020-12-01T10:52:15Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=14799
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `tree-ssa`
### severity : `enhancement`
### contents :
void bar (void);

void
foo (int a)
{
  if (a == 30)
    bar ();
  else if (a == 31)
    bar ();
  else if (a == 53)
    bar ();
  else if (a == 23)
    bar ();
}

The idea comes from LLVM.
Of course we should do this only if switch statements are expanded in
an (almost?) optimal way.


---


### compiler : `gcc`
### title : `[tree-ssa] missed tail call optimization in presence of a const function`
### open_at : `2004-04-01T04:40:59Z`
### last_modified_date : `2021-07-26T02:33:45Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=14806
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `tree-ssa`
### severity : `enhancement`
### contents :
int bar (int) __attribute__((const));

int g;

int
foo (int a)
{
  int b = bar (b);
  g = 0;
  return b;
}

Note that we can move "g = 0;" to before "bar (b)".


---


### compiler : `gcc`
### title : `Another way of expanding a switch statement`
### open_at : `2004-04-04T10:00:41Z`
### last_modified_date : `2021-07-26T19:35:52Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=14842
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.0.0`
### severity : `enhancement`
### contents :
Convert foo() to baz() (at expand time or very late in tree optimization):

void bar (void);

void
foo (int a)
{
  switch (a)
    {
    case 5:
    case 7:
      bar ();
    }
}

void
baz (int a)
{
  if ((a & ~2) == 5)
    bar ();
}

On i686-pc-linux-gnu with -O2 -fomit-frame-pointer, I get:

	.text
	.p2align 2,,3
.globl foo
	.type	foo, @function
foo:
	movl	4(%esp), %eax	# 3	*movsi_1/1	[length = 4]
	cmpl	$5, %eax	# 9	*cmpsi_1_insn/1	[length = 3]
	je	.L3	# 10	*jcc_1	[length = 2]
	cmpl	$7, %eax	# 11	*cmpsi_1_insn/1	[length = 3]
	je	.L3	# 12	*jcc_1	[length = 2]
	ret	# 35	return_internal	[length = 1]
	.p2align 2,,3
.L3:
	jmp	bar	# 19	*call_0	[length = 5]
	.size	foo, .-foo
	.p2align 2,,3
.globl baz
	.type	baz, @function
baz:
	movl	4(%esp), %eax	# 29	*movsi_1/1	[length = 4]
	andl	$-3, %eax	# 9	*andsi_1/1	[length = 3]
	cmpl	$5, %eax	# 10	*cmpsi_1_insn/1	[length = 3]
	je	.L8	# 11	*jcc_1	[length = 2]
	ret	# 32	return_internal	[length = 1]
	.p2align 2,,3
.L8:
	jmp	bar	# 16	*call_0	[length = 5]
	.size	baz, .-baz

Comparing baz() to foo(), aside from the small size reduction,
notice that we have eliminated one conditional jump.
(If we need to preserve the value of "a", we don't get
the size reduction anymore because we need to make a copy of "a", but
we can still eliminate one conditional jump.)

Depending on a situation, we can either entirely replace the binary tree
expansion of the switch statement (like this case) or replace a part of
the binary tree.

If we think of this problem as minimizing a circuit recognizing 5 and 7,
we can use Quine-McCluskey minimization to make (a & ~2) == 5,
but a sequential program is different from a circuit, so the result of 
Quine-McCluskey minimization is not always optimal on a sequential machine.
It may not be a bad idea to just specialize for a small case involving only two
cases like this one.


---


### compiler : `gcc`
### title : `[tree-ssa] narrow types if wide result is not needed for unsigned types or when wrapping is true`
### open_at : `2004-04-04T16:15:55Z`
### last_modified_date : `2019-03-04T13:11:36Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=14844
### status : `RESOLVED`
### tags : `missed-optimization, TREE`
### component : `tree-optimization`
### version : `tree-ssa`
### severity : `enhancement`
### contents :
Consider:

int
foo (int a, int b)
{
  long long aa = a;
  long long bb = b;
  return aa + bb;
}

The last tree looks like:

foo (a, b)
{
<bb 0>:
  return (int)(long long int)a + (int)(long long int)b;

}

We may be able to solve this problem by propagating narrowing casts backward.


---


### compiler : `gcc`
### title : `strength reduction on floating point`
### open_at : `2004-04-08T03:52:55Z`
### last_modified_date : `2021-12-28T04:01:12Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=14886
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.0.0`
### severity : `enhancement`
### contents :
/* I found an interesting xlc strength reduction optimization recently,
   that had xlc producing fp code that ran over twice as fast as gcc
   code on a powerpc benchmark.  Some improvement on the benchmark code
   was due to xlc using floating multiply-add more aggressively, but the
   main improvement was converting code as in f1 to as in f2.  */

float bar;

void f1 (void)
{
  int i;
  for (i = 0; i < 500; i++)
    __asm__ __volatile__ ("# %0" : : "f" (i * bar));
}

void f2 (void)
{
  register long i;
  register float f, bar2 = bar;
  for (i = 500, f = 0.0; --i >= 0;)
    {
      __asm__ __volatile__ ("# %0" : : "f" (f));
      f += bar2;
    }
}

/* On ppc32, the f1 loop generates
.L9:
        xoris 0,9,0x8000
        stw 11,8(1)
        stw 0,12(1)
        lfd 0,8(1)
        fsub 0,0,13
        frsp 0,0
        fmuls 0,0,12
#APP
        # 0
#NO_APP
        addi 9,9,1
        bdnz .L9

the f2 loop is
.L19:
#APP
        # 0
#NO_APP
        fadds 0,0,13
        bdnz .L19
*/


---


### compiler : `gcc`
### title : `[tree-ssa] Convert a <= 7 && b <= 7 into (a | b) <= 7.`
### open_at : `2004-05-01T12:58:33Z`
### last_modified_date : `2019-03-04T12:38:53Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=15241
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `tree-ssa`
### severity : `enhancement`
### contents :
We should convert foo into bar (if profitable).

void baz ();

unsigned int
foo (unsigned int a, unsigned int b)
{
  if (a <= 7 && b <= 7)
    baz ();
}

unsigned int
bar (unsigned int a, unsigned int b)
{
  if ((a | b) <= 7)
    baz ();
}

The last SSA form looks like:

;; Function foo (foo)

foo (a, b)
{
  _Bool T.2;
  _Bool T.1;
  _Bool T.0;

<bb 0>:
  T.0_2 = a_1 <= 7;
  T.1_4 = b_3 <= 7;
  T.2_5 = T.0_2 && T.1_4;
  if (T.2_5) goto <L0>; else goto <L1>;

<L0>:;
  baz () [tail call];

<L1>:;
  return;

}



;; Function bar (bar)

bar (a, b)
{
  unsigned int T.3;

<bb 0>:
  T.3_3 = a_1 | b_2;
  if (T.3_3 <= 7) goto <L0>; else goto <L1>;

<L0>:;
  baz () [tail call];

<L1>:;
  return;

}

On i686-pc-linux-gnu, I get:

foo:
	cmpl	$7, 4(%esp)
	setbe	%dl
	cmpl	$7, 8(%esp)
	setbe	%al
	testb	%al, %dl
	jne	.L5
	rep ; ret
	.p2align 4,,7
.L5:
	jmp	baz
	.size	foo, .-foo
	.p2align 4,,15
.globl bar
	.type	bar, @function
bar:
	movl	8(%esp), %eax
	orl	4(%esp), %eax
	cmpl	$7, %eax
	jbe	.L9
	rep ; ret
	.p2align 4,,7
.L9:
	jmp	baz


---


### compiler : `gcc`
### title : `[tree-ssa] Convert (x < 0) || (y < 0) into (x | y) < 0.`
### open_at : `2004-05-09T19:30:50Z`
### last_modified_date : `2020-04-24T16:03:43Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=15348
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `tree-ssa`
### severity : `enhancement`
### contents :
Convert foo() into baz().

void bar (void);

int
foo (int x, int y)
{
  int t1 = x < 0;
  int t2 = y < 0;
  return t1 || t2;
}

int
baz (int x, int y)
{
  return (x | y) < 0;
}

Needless to mention, we should do this fairly late in SSA optimizations.


---


### compiler : `gcc`
### title : `Sibcall optimization for libcalls.`
### open_at : `2004-05-16T10:02:00Z`
### last_modified_date : `2021-08-16T06:39:48Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=15473
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `6.0`
### severity : `enhancement`
### contents :
Consider:

long long
foo (long long a, long long b)
{
  return a / b;
}

I get:

foo (a, b)
{
<bb 0>:
  return a_1 / b_2;

}

with the assembly code being

foo:
	subl	$12, %esp
	pushl	28(%esp)
	pushl	28(%esp)
	pushl	28(%esp)
	pushl	28(%esp)
	call	__divdi3
	addl	$28, %esp
	ret

Note that the sequence of 4 pushl instructions simply copy 16 bytes
from one location of the stack to another.

If I create a (non-libcall) function with the same arguments like so

long long div64 (long long a, long long b);

long long
bar (long long a, long long b)
{
  return div64 (a, b);
}

I get:

bar (a, b)
{
  long long int T.0;

<bb 0>:
  T.0_3 = div64 (a_1, b_2) [tail call];
  return T.0_3;

}

with the assembly code being

bar:
	jmp	div64


---


### compiler : `gcc`
### title : `[tree-ssa] bool and short function arguments promoted to int`
### open_at : `2004-05-17T04:33:08Z`
### last_modified_date : `2019-06-26T05:06:52Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=15484
### status : `RESOLVED`
### tags : `memory-hog, missed-optimization`
### component : `tree-optimization`
### version : `4.0.0`
### severity : `normal`
### contents :
This code: 

_Bool bar (_Bool a);
_Bool foo1 (_Bool a)
{
  if (bar(a))     return 1;
  else            return 0;
}

static short barshort (short a);
short foo1short (short a)
{
  if (barshort(a))     return 1;
  else                 return 0;
}

is transformed to: (when using -O -fdump-tree-generic)

foo1 (a)
{
  int T.17;
  _Bool T.18;

  T.17 = (int)a; <------ this is not needed
  T.18 = bar (T.17);
  if (T.18 != 0)
    {
      return 1;
    }
  else
    {
      return 0;
    }
}

foo1short (a)
{
  int T.19;
  short int T.20;

  T.19 = (int)a; <------ this is not needed
  T.20 = barshort (T.19);
  if (T.20 != 0)
    {
      return 1;
    }
  else
    {
      return 0;
    }
}

the promotions shown are not needed, at least not at this point in the
compilation process.


---


### compiler : `gcc`
### title : `Use of regparm inhibits tail call optimization`
### open_at : `2004-05-18T22:56:53Z`
### last_modified_date : `2022-01-06T00:04:07Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=15529
### status : `NEW`
### tags : `FIXME, missed-optimization`
### component : `target`
### version : `4.0.0`
### severity : `enhancement`
### contents :
(I would have put this in the right optimization component if I knew which of
them applies. Worse, bugzilla requires it. Let me take a guess... 50/50
chance... RTL?)

This is bug 14909 plus regparm. The testcase of bug 14909 works as expected.

When compiling:
//void g(void (*f)(void)) { f(); }
#define regparm __attribute__((regparm(3)))
void regparm g(void (regparm *f)()) { f(); }

With:
gcc -W -Wall -O3 -ffast-math -fomit-frame-pointer -fexpensive-optimizations
-save-temps -march=athlon -c
(most switches probably a red herring, didn't reduce the command line)

The result is:
	.file	"testcase.c"
	.text
	.align 4
	.p2align 4,,15
.globl g
	.type	g, @function
g:
	subl	$12, %esp
	call	*%eax
	addl	$12, %esp
	ret
	.size	g, .-g
	.ident	"GCC: (GNU) 3.5.0 20040502 (experimental)"
	.section	.note.GNU-stack,"",@progbits

It should be:
g:
	jmp *%eax

The use of regparm is superfluous in  this case, but the bug happens also in the
slightly less reduced testcase:

#define regparm __attribute__((regparm(3)))
void regparm g(void (regparm *f)(unsigned)) { f(0); }

Output:
	.file	"testcase2.c"
	.text
	.align 4
	.p2align 4,,15
.globl g
	.type	g, @function
g:
	subl	$12, %esp
	movl	%eax, %edx
	xorl	%eax, %eax
	call	*%edx
	addl	$12, %esp
	ret
	.size	g, .-g
	.ident	"GCC: (GNU) 3.5.0 20040502 (experimental)"
	.section	.note.GNU-stack,"",@progbits

The same happens when returning other than void (original testcase used
unsigned) -- same as bug 14909 in fact.

Reading specs from /usr/lib/gcc-snapshot/lib/gcc/i486-linux/3.5.0/specs
Configured with: ../src/configure -v
--enable-languages=c,c++,java,f77,objc,ada,treelang
--prefix=/usr/lib/gcc-snapshot --enable-shared --with-system-zlib --enable-nls
--enable-threads=posix --without-included-gettext --disable-werror
--enable-__cxa_atexit --enable-clocale=gnu --enable-libstdcxx-debug
--enable-java-gc=boehm --enable-java-awt=gtk i486-linux
Thread model: posix
gcc version 3.5.0 20040502 (experimental)


---


### compiler : `gcc`
### title : `Missed move to partial register`
### open_at : `2004-05-19T01:25:26Z`
### last_modified_date : `2021-10-11T08:34:32Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=15533
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.0.0`
### severity : `enhancement`
### contents :
When compiling:
#include <stdint.h>
#define regparm __attribute__((regparm(3)))
uint8_t a;
uint16_t regparm fn(uint16_t b)
{ return (b & ~0xFF) | a; }

With:
gcc -W -Wall -O3 -ffast-math -fomit-frame-pointer -fexpensive-optimizations
-save-temps -march=athlon -c

The result is:
	.file	"testcase.c"
	.text
	.align 4
	.p2align 4,,15
.globl fn
	.type	fn, @function
fn:
	movzbw	a, %dx
	xorb	%al, %al
	orl	%edx, %eax
	movzwl	%ax, %eax
	ret
	.size	fn, .-fn
	.comm	a,1,1
	.ident	"GCC: (GNU) 3.5.0 20040502 (experimental)"
	.section	.note.GNU-stack,"",@progbits

The expected result would be:
fn:
	movb a, %al
	ret

(I assume the correct ABI for regparm would be for the caller to do all the
sign/zero extension work, since it could be done as side effects of calculations
there, so there is no need to do any extension inside fn. If I'm wrong, just add
an extra movzwl	%ax, %eax somewhere)

Reading specs from /usr/lib/gcc-snapshot/lib/gcc/i486-linux/3.5.0/specs
Configured with: ../src/configure -v
--enable-languages=c,c++,java,f77,objc,ada,treelang
--prefix=/usr/lib/gcc-snapshot --enable-shared --with-system-zlib --enable-nls
--enable-threads=posix --without-included-gettext --disable-werror
--enable-__cxa_atexit --enable-clocale=gnu --enable-libstdcxx-debug
--enable-java-gc=boehm --enable-java-awt=gtk i486-linux
Thread model: posix
gcc version 3.5.0 20040502 (experimental)


---


### compiler : `gcc`
### title : `[11/12/13/14 Regression] Missed optimization with bitfields with return value`
### open_at : `2004-05-22T22:37:54Z`
### last_modified_date : `2023-07-07T10:11:25Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=15596
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.0.0`
### severity : `minor`
### contents :
Source:
typedef struct {
  int a : 20;
  int b : 1;
  int c : 1;
  int d : 1;
} bitstr;

bitstr fun(int s, int l)
{
  bitstr res;
  res.a  = s;
  res.b  = 1;
  res.c  = 0;
  res.d  = l;
  return res;
}

This is caused by the nrv optimization.


---


### compiler : `gcc`
### title : `missed subreg optimization`
### open_at : `2004-06-03T04:27:27Z`
### last_modified_date : `2023-05-15T05:34:12Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=15792
### status : `RESOLVED`
### tags : `missed-optimization, ra`
### component : `rtl-optimization`
### version : `4.0.0`
### severity : `enhancement`
### contents :
int test(unsigned long long x) {
int g = (int)x|((int)(x>>32));
  if (g) gh();
}
int test1(unsigned long long x) {
  if (x) gh();
}

These two functions should produce the same asm but test produces better asm.
I noticed this when looking PR 11873.


---


### compiler : `gcc`
### title : `don't use "if" to extract a single bit bit-field.`
### open_at : `2004-06-04T18:55:52Z`
### last_modified_date : `2020-04-19T18:28:19Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=15826
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.0.0`
### severity : `enhancement`
### contents :
Transform foo() into bar().

struct s {
  unsigned int bit : 1;
};

unsigned int
foo (struct s *p)
{
  if (p->bit)
    return 1;
  else
    return 0;
}

unsigned int
bar (struct s *p)
{
  return (unsigned int) (p->bit);
}

Currently, the last tree-ssa form I get looks like so:

;; Function foo (foo)

foo (p)
{
  int T.1;
  unsigned int T.0;

<bb 0>:
  T.0_2 = p_1->bit;
  if (T.0_2 != 0) goto <L0>; else goto <L1>;

<L0>:;
  return 1;

<L1>:;
  return 0;

}



;; Function bar (bar)

bar (p)
{
<bb 0>:
  return p_1->bit;

}

The assembly code:

        .p2align 2,,3
.globl foo
        .type   foo, @function
foo:
        testb   $1, (%eax)      # 43    *testqi_1/3     [length = 3]
        setne   %al     # 40    *setcc_1        [length = 3]
        movzbl  %al, %eax       # 45    *zero_extendqisi2_movzbw        [length
= 3]
        ret     # 48    return_internal [length = 1]
        .size   foo, .-foo
        .p2align 2,,3
.globl bar
        .type   bar, @function
bar:
        movzbl  (%eax), %eax    # 28    *zero_extendqisi2_movzbw        [length
= 3]
        andl    $1, %eax        # 12    *andsi_1/1      [length = 3]
        ret     # 31    return_internal [length = 1]
        .size   bar, .-bar

Note that alias.i.t50.tailc contains:

<L22>:;
  T.1776_58 = x_2->unchanging;
  if (T.1776_58 != 0) goto <L25>; else goto <L26>;

<L25>:;
  return 0;

<L26>:;
  return 1;


---


### compiler : `gcc`
### title : `a & b & ~a & ~b not optimized at the tree level`
### open_at : `2004-06-08T18:36:38Z`
### last_modified_date : `2023-09-22T18:53:47Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=15878
### status : `RESOLVED`
### tags : `missed-optimization, TREE`
### component : `tree-optimization`
### version : `4.0.0`
### severity : `enhancement`
### contents :
From looking at bugs which were fixed for 3.5.0 which were done on the RTL, I noticed this one (From 
PR 5263).

int f(int a,int b) { return a&b~a&~b; }


---


### compiler : `gcc`
### title : `gcc fails to optimize redundant expression (reassocation)`
### open_at : `2004-06-23T13:36:09Z`
### last_modified_date : `2021-08-20T00:28:34Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=16157
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.0.0`
### severity : `enhancement`
### contents :
extern int a0, a1, a2, a3, a4;
void f ()
{
	/* this can be optimized to four additions... */
	a4 = a4 + a3 + a2 + a1 + a0;
	a3 = a3 + a2 + a1 + a0;
	a2 = a2 + a1 + a0;
	a1 = a1 + a0;
}

...but gcc does nothing with this function.


---


### compiler : `gcc`
### title : `simple function generates an memmove() call instead of inlining`
### open_at : `2004-06-24T07:24:09Z`
### last_modified_date : `2022-12-01T03:35:46Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=16172
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.0.0`
### severity : `enhancement`
### contents :
compiling http://www.zip.com.au/~akpm/linux/patches/stuff/fib_hash.i

with

/usr/local/gcc-cvs/bin/gcc -Wp,-MD,net/ipv4/.fib_hash.o.d -nostdinc -iwithprefix
include -D__KERNEL__ -Iinclude  -Wall -Wstrict-prototypes -Wno-trigraphs
-fno-strict-aliasing -fno-common -pipe -msoft-float -mpreferred-stack-boundary=2
-fno-unit-at-a-time -march=i686 -mregparm=3 -Iinclude/asm-i386/mach-default
-gdwarf-2 -O1 -Os -g -Wdeclaration-after-statement    -DKBUILD_BASENAME=fib_hash
-DKBUILD_MODNAME=fib_hash -c -o net/ipv4/.tmp_fib_hash.o net/ipv4/fib_hash.c

causes the fn_hash() function to generate a call to memmove().  It seems
inappropriate, as that function deals with little scalars.


---


### compiler : `gcc`
### title : `PowerPC - redundant compare`
### open_at : `2004-07-09T17:53:38Z`
### last_modified_date : `2018-12-21T04:45:42Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=16458
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.0.0`
### severity : `enhancement`
### contents :
Description:
A non-optimal compare sequence is illustrated.  Two compares are being
done, one signed and the other unsigned.  One unsigned compare would
suffice.  Duplicate using gcc 3.5 and command line:

gcc -O3 -m64 -c test.c

Testcase:
unsigned int a, b;

int foo ()
{
  if (a == b) return 1;
  if (a > b)  return 2;
  if (a < b)  return 3;
  if (a != b) return 4;
  return 0;
}

Assembly:
      ld 9,.LC1@toc(2)
      li 3,1
      ld 11,.LC0@toc(2)
      lwz 10,0(9)
      lwz 0,0(11)
      cmpw 7,0,10   - signed compare of a and b
      cmplw 6,0,10  - unsigned compare of a and b
      beqlr- 7      - (a == b uses signed compare)
      li 3,2
      bgtlr- 6      - (a > b uses unsigned compare)
      li 3,4
      bgelr- 6      - (a != b uses unsigned compare)
      li 3,3
      blr




---


### compiler : `gcc`
### title : `Dead stack adjustion code not removed`
### open_at : `2004-07-21T12:32:06Z`
### last_modified_date : `2021-08-16T01:16:25Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=16657
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.0.0`
### severity : `enhancement`
### contents :
struct s2 { unsigned long a, b; };
unsigned long f8(struct s2 x) { return x.a + x.b; }

gets compiled to

	addq    a1,a0,v0
	lda     sp,-16(sp)
	lda     sp,16(sp)
	ret

The reason is probably that the structs get spilled to the stack, and
then the store/load is optimized out, but the stack adjustion remains.

Similar to the fixed PR 6882.


---


### compiler : `gcc`
### title : `Opportunity to remove unnecessary load instructions`
### open_at : `2004-07-28T17:00:38Z`
### last_modified_date : `2019-06-26T05:06:52Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=16797
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.0.0`
### severity : `enhancement`
### contents :
Description:
A non-optimal code sequence is illustraded.  Values are being loaded from storage unecessarily.   Duplicate using gcc 3.5 and command line:

gcc -O3 -m64 -c test.c

Testcase:
long int i, j;
int foo ()
{

  j = (i>>52);

  if (j< 0) {
    i = 10;
  } else {
    i = 20;
  };

  return i;

}

Assembly:
.foo:
	ld 11,.LC0@toc(2)
	ld 9,.LC1@toc(2)
	ld 0,0(11)
	sradi 0,0,52
	cmpdi 7,0,0
	std 0,0(9)
	blt- 7,.L7
	li 0,20     <-- Load directly into register 3 here...
	std 0,0(11)
	lwa 3,4(11) <-- ... and eliminate this load.
	blr
.L7:
	li 0,10     <-- Load directly into register 3 here...
	std 0,0(11)
	lwa 3,4(11) <-- ... and eliminate this load.
	blr




---


### compiler : `gcc`
### title : `PowerPC - Opportunity to use recording form instruction.`
### open_at : `2004-07-28T17:00:38Z`
### last_modified_date : `2022-03-08T16:20:44Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=16798
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.0.0`
### severity : `enhancement`
### contents :
Description:
A non-optimal code sequence is illustraded.  The recording form of an instruction could be used allowing for the elimination of a compare.  Duplicate using gcc 3.5 and command line:

gcc -O3 -m64 -c test.c


Testcase:
long int i, j;
int foo ()
{

  j = (i>>52);

  if (j< 0) {
    i = 10;
  } else {
    i = 20;
  };

  return i;

}

Assembly:
.foo:
	ld 11,.LC0@toc(2)
	ld 9,.LC1@toc(2)
	ld 0,0(11)
	sradi 0,0,52 <-- Use the recording form of sradi
	cmpdi 7,0,0  <-- and eliminate this compare.
	std 0,0(9)
	blt- 7,.L7
	li 0,20
	std 0,0(11)
	lwa 3,4(11)
	blr
.L7:
	li 0,10
	std 0,0(11)
	lwa 3,4(11)
	blr




---


### compiler : `gcc`
### title : `PowerPC - Unnecessary extsw`
### open_at : `2004-07-28T17:00:38Z`
### last_modified_date : `2019-06-26T05:06:52Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=16802
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.0.0`
### severity : `enhancement`
### contents :
Description:
A non-optimal code sequence is illustrated.  The extsw prior to the branch to return from the procedure is not necessary.  Duplicate using gcc 3.5 and command line:

gcc -O3 -m64 -c test.c

Testcase:
int b,d;

int logic_func1() {
  return (d< b);
}

Assembly:
.logic_func1:
	ld 9,.LC1@toc(2)
	li 3,1
	ld 11,.LC0@toc(2)
	lwz 10,0(9)
	lwz 0,0(11)
	cmpw 7,0,10
	blt- 7,.L2
	li 3,0
.L2:
	extsw 3,3 <-- Unnecessary.
	blr




---


### compiler : `gcc`
### title : `Opportunity to improve code generated for complex logical expression`
### open_at : `2004-08-19T14:59:11Z`
### last_modified_date : `2022-11-11T20:27:14Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=17107
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.0.0`
### severity : `enhancement`
### contents :
Description:
A non-optimal code sequence is illustraded.    Duplicate using gcc 3.5 and
command line:

gcc -O3 -m64 -c test.c


Testcase:
int i;
void foo(int a, int b, int c) {

  i = (a > b && a < c);

}

Assembly:
Currently gcc 3.5 generates the following code which always results
in the execution of the compare/branch for the right side of the
expression (i.e. a < c):

.foo:
      cmpw 7,4,3
      cmpw 6,3,5
      ld 11,.LC0@toc(2)
      li 9,1
      blt- 7,.L2
      li 9,0
.L2:
      li 0,1
      blt- 6,.L3
      li 0,0
.L3:
      and 0,9,0
      stw 0,0(11)
      blr

Execution of the second compare/branch may be avoided by
restructuring the code.  This also eliminates the need for
the 'and':

.foo:
      cmpw 7,4,3
      ld 11,.LC0@toc(2)
      li 9,0
      bng- 7,.L2
      cmpw 6,3,5
      bnl- 6,.L2
      li 9,1
.L2:
      stw 9,0(11)
      blr




---


### compiler : `gcc`
### title : `Store with update not generated for a simple loop`
### open_at : `2004-08-19T14:59:11Z`
### last_modified_date : `2022-03-08T16:20:45Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=17108
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.0.0`
### severity : `enhancement`
### contents :
Description:
A non-optimal code sequence is illustraded.    Duplicate using gcc 3.5 and
command line:

gcc -O3 -m64 -c test.c


Testcase:
void foo(float *data, float d) {
   long i;

   for (i = 0; i < 8; i++)
      data[i] = d;
}

Assembly:
Code generated by gcc 3.5:

.foo:
      li 0,8
      li 9,0
      mtctr 0
.L2:
      sldi 0,9,2
      addi 9,9,1
      stfsx 1,3,0
      bdnz .L2
      blr

We can eliminate the multiply(shift) as well as the increment of "i" and
use
a store with update form to simplify the loop to this:

.foo:
      ai 3,3,-4
      li 0,8
      mtctr 0
.L2:
      stfsu 1,3,4
      bdnz .L2
      blr





---


### compiler : `gcc`
### title : `not removing removal of nested structs`
### open_at : `2004-08-27T18:55:55Z`
### last_modified_date : `2021-09-03T06:13:20Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=17217
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.0.0`
### severity : `enhancement`
### contents :
gcc -O3 and you will see that the load and store to the struct is still there for j.
int h(int *a);
int f(int i, int j)
{
  int t = i;
  int t1 = j;
  int g()
  {
     return h(&t) + t1;
  }
  return g() + t1;
}

I found this when looking at facerec which uses nested functions.


---


### compiler : `gcc`
### title : `if-conversion problem`
### open_at : `2004-08-30T05:26:11Z`
### last_modified_date : `2021-06-08T09:04:14Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=17234
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.0.0`
### severity : `normal`
### contents :
Compiling 

void foo (unsigned *, unsigned *, unsigned);
unsigned *baz (unsigned) __attribute__ ((const));

struct COST
{
  unsigned *cost;

  unsigned maxWeakConstraintLevel;
};

unsigned * bar(struct COST *c)
{
  unsigned *valp;
  if(c->maxWeakConstraintLevel == 0)
    valp =0;
  else
    {
      valp = baz (4 * 33);
      foo (valp, c->cost, c->maxWeakConstraintLevel * sizeof(unsigned));
    }
  return valp;
}

with -O2 -fomit-frame-pointer on x86 generates:

bar:
        subl    $28, %esp
        movl    %edi, 24(%esp)
        movl    32(%esp), %edi
        movl    %esi, 20(%esp)
        xorl    %esi, %esi            <- [1] this should not be here
        movl    %ebx, 16(%esp)
        movl    4(%edi), %ebx
        testl   %ebx, %ebx
        jne     .L6                 
        movl    %esi, %eax             <- it should be before this instruction
        movl    16(%esp), %ebx
        movl    20(%esp), %esi
        movl    24(%esp), %edi
        addl    $28, %esp
        ret
        .p2align 4,,7
.L6:
        movl    $132, (%esp)
        call    baz
        movl    %eax, %esi         <- %esi is not used on this branch, 
                                    so [1] is partially dead code

The instruction [1] is put there by the if-conversion pass, when compiling
with -fno-ifconversion [1] appears only on one branch. 

gcc-3.3.3 does not have this problem, so this is a regression.


---


### compiler : `gcc`
### title : `variable rotate and unsigned long long rotate should be better optimized`
### open_at : `2004-10-08T00:04:25Z`
### last_modified_date : `2023-10-10T18:38:53Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=17886
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.0.0`
### severity : `enhancement`
### contents :
gcc can detect the (x << y)|(x >> (bitwidth-y)) idiom for rotate and convert
it into the machine rotate instruction. But it only works when y is a constant
and is not long long.

Enhancement request is to handle it for long long too (on 32bit) and
to handle variable shifts.

The attached test case should use rol in f1-f4


---


### compiler : `gcc`
### title : `Two consecutive movzbl are generated`
### open_at : `2004-10-11T16:38:42Z`
### last_modified_date : `2021-09-06T08:29:45Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=17935
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.0.0`
### severity : `enhancement`
### contents :
Consider:

struct flags {
  unsigned f0 : 1;
};

_Bool
bar (struct flags *p, struct flags *q)
{
  return (!p->f0 && !q->f0);
}

With "cc1 -O2 -fomit-frame-pointer -march=i386", I get

bar:
	movl	4(%esp), %eax
	testb	$1, (%eax)
	jne	.L9
	movl	8(%esp), %eax
	testb	$1, (%eax)
	sete	%al
	movzbl	%al, %eax
	movzbl	%al, %eax
	ret
	.p2align 2,,3
.L9:
	xorl	%eax, %eax
	movzbl	%al, %eax
	ret

Note the two consecutive movzbl.  We don't need the second one.

Also note the xorl followed by movzbl.  We don't need the movzbl.


---


### compiler : `gcc`
### title : `expand_divmod fails to optimize division of 64-bit quantity by small constant when BITS_PER_WORD is 32`
### open_at : `2004-10-12T22:48:16Z`
### last_modified_date : `2021-08-15T12:14:19Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=17958
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.0.0`
### severity : `enhancement`
### contents :
expand_divmod cannot optimize code such as

long long div10(long long n) { return n / 10; }

when BITS_PER_WORD is 32.  A call to __divdi3 gets generated.  By contrast, when
BITS_PER_WORD is 64, this is optimized to a multiply and a shift.  I noticed
this problem on powerpc32, but it ought to affect any 32-bit target.


---


### compiler : `gcc`
### title : `OR of two single-bit bitfields is inefficient`
### open_at : `2004-10-17T16:36:05Z`
### last_modified_date : `2018-11-06T08:42:41Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=18041
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `unknown`
### severity : `enhancement`
### contents :
Consider:

struct B {
  unsigned bit0 : 1;
  unsigned bit1 : 1;
};

void
foo (struct B *b)
{
  b->bit0 = b->bit0 | b->bit1;
}

./cc1 -O2 -fomit-frame-pointer -mregparm=3 generates

foo:
	movb	(%eax), %dl  <- one load
	movb	%dl, %cl
	shrb	%cl
	orl	%edx, %ecx
	andl	$1, %ecx
	movl	(%eax), %edx <- another load from the same place
	andl	$-2, %edx
	orl	%ecx, %edx   <- the second OR
	movl	%edx, (%eax)
	ret

We could do something like

	movb	(%eax), %cl
	movb	%cl, %dl
	shrb	%dl
	andl	$1, %edx
	orl	%ecx, %edx
	movb	%dl, (%eax)
	ret

or

	movb	(%eax), %dl
	testb	$2, %dl
	je	.L6
	orl	$1, %edx
	movb	%dl, (%eax)
.L6:
	ret

expr.c actually has code intended to emit the second suggestion
(look for "Check for |= or &= of a bitfield" in expr.c), but it is
practically disabled because we get tree like this

  b->bit0 = (<unnamed type>) (unsigned char)
              ((signed char) b->bit0 | (signed char) b->bit1)

whereas the code in expr.c expects

  b->bit0 = b->bit0 | b->bit1;

The code is not triggered even in gcc-3.3.  Probably it is practically
disabled for a long time.


---


### compiler : `gcc`
### title : `Inefficient max/min code for PowerPC`
### open_at : `2004-10-26T04:17:52Z`
### last_modified_date : `2022-03-08T16:20:51Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=18154
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.0.0`
### severity : `enhancement`
### contents :
int min(int a, int b) {
  if (a < b)
    return a;
  else
    return b;
}

should produce

        rlwinm  r2,r3,1,31,31
        subfc   r0,r4,r3
        rlwinm  r0,r4,1,31,31
        subfe   r0,r2,r0
        andc    r2,r4,r0
        and     r0,r3,r0
        or      r3,r0,r2
        blr

but instead produces a branch sequence

         mr r0,r3
         mr r3,r4
         cmpw cr7,r0,r4
         bgelr- cr7
         mr r3,r0
         blr

with unnecessary dependencies.


---


### compiler : `gcc`
### title : `extraneous inc/dec pair`
### open_at : `2004-10-30T19:15:42Z`
### last_modified_date : `2021-07-26T01:46:01Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=18233
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.0.0`
### severity : `enhancement`
### contents :
The attached code produces the following assembler
foo:
        pushl   %ebp
        movl    %esp, %ebp
        movl    8(%ebp), %eax
        testl   %eax, %eax
        jne     .L7
        leave
        ret
        .p2align 2,,3
.L7:
        xorl    %edx, %edx
        bsfl    %eax, %eax
        sete    %dl
        negl    %edx
        orl     %edx, %eax
        incl    %eax
        decl    %eax
        leave
        ret

There are two issues
1) the incl/decl pair fails to be eliminated.  I presume this is because the
define_insn_and_split that i86 uses gets split too late for CSE to fold in the
subsequent decrement of the source code.  Perhaps it could be partially split
earlier, leaving the conditional move stuff to later.  I've not examined it in
greate detal.

2) Possibly much harder.  The ffs expansion has no knowledge that its input is
nonzero, and therefore need not deal with that case.  I gues this will be
systemic to other targets.  I wonder what can be done about that -- possibly
duplicate FFS_NON_ZERO_EXPR and FFS_MAYBE_ZERO_EXPR nodes?


---


### compiler : `gcc`
### title : `Missed IV optimization`
### open_at : `2004-11-06T16:39:46Z`
### last_modified_date : `2019-03-05T11:50:20Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=18316
### status : `ASSIGNED`
### tags : `missed-optimization, ra`
### component : `tree-optimization`
### version : `4.0.0`
### severity : `enhancement`
### contents :
The following test case from Briggs' optimization test suite is 
missed by tree IV opts (and nothing on RTL catches this either): 
 
void 
strength_test2(int *data) 
{ 
  int k = data[0]; 
  int i = 0; 
  do { 
    data[data[2]] = 2; 
    i = i + 1; 
  } while (i * k < data[1]); 
} 
 
void 
strength_result2(int *data) 
{ 
  int k = data[0]; 
  int i = 0; 
  do { 
    data[data[2]] = 2; 
    i = i + k; 
  } while (i < data[1]); 
}


---


### compiler : `gcc`
### title : `[meta-bug] Argument and return value marshalling at tree level`
### open_at : `2004-11-08T13:55:04Z`
### last_modified_date : `2019-09-26T11:20:20Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=18374
### status : `RESOLVED`
### tags : `meta-bug, missed-optimization`
### component : `tree-optimization`
### version : `4.0.0`
### severity : `enhancement`
### contents :
This is a catch-all report to mention that we should really be doing ABI
mandated argument and return value marshalling at the tree level. These
operations can involve sign/zero extension (at the very least) and should be
exposed to the tree optimizers.


---


### compiler : `gcc`
### title : `[meta-bug] combine needs to be templatized like a peepholer`
### open_at : `2004-11-09T12:48:58Z`
### last_modified_date : `2020-11-09T02:16:21Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=18395
### status : `NEW`
### tags : `meta-bug, missed-optimization`
### component : `rtl-optimization`
### version : `4.0.0`
### severity : `enhancement`
### contents :
This is a catch all bug report to document failures in combine.

There are at least two problems with combine.

1) It only combines chains of instructions that have no other uses of the
intermediate results.

2) It functions by generating promising patterns and then seeing if they exist.
 This is wasteful, in that it generates many patterns  that don't exist on the
particular target, and it is blind in that it doesn't spot any special cases the
target might have.

Really combine, which is a generic peepholer, needs some kind of templatizing on
the target machine.   What's needed is something like pre-reg-alloc peepholes. 
That of course would be a large amount of work.


---


### compiler : `gcc`
### title : `vectorizer failed for matrix multiplication`
### open_at : `2004-11-12T01:22:16Z`
### last_modified_date : `2023-08-04T20:20:16Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=18437
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.0.0`
### severity : `enhancement`
### contents :
Vectorizer fails to handle this:

----------------------------------------------------
#define align(x) __attribute__((align(x)))
typedef float align(16) MATRIX[3][3];

void RotateMatrix(MATRIX ret, MATRIX a, MATRIX b)
{
  int i, j;

  for (j = 0; j < 3; j++)
    for (i = 0; i < 3; i++)
      ret[j][i] =   a[j][0] * b[0][i]
                  + a[j][1] * b[1][i]
                  + a[j][2] * b[2][i];
}
----------------------------------------------------

loop at bench.cc:33: not vectorized: unsupported scalar cycle.
loop at bench.cc:33: bad scalar cycle.


---


### compiler : `gcc`
### title : `vectorizer failed for vector matrix multiplication`
### open_at : `2004-11-12T01:29:03Z`
### last_modified_date : `2023-09-23T21:13:17Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=18438
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.0.0`
### severity : `enhancement`
### contents :
Vectorizer fails to handle this:


------------------------------------------------------------
#define NUMPOINTS 50000

#define align(x) __attribute__((align(x)))

typedef float align(16) MATRIX[3][3];

static float points[NUMPOINTS][4];
static align(16) float opoints[NUMPOINTS][4];
static bool flags[NUMPOINTS];
static MATRIX gmatrix;


void RotateVectors (void)
{
  int i, r;

  for (r = 0; r < 4; r++)
  {
    for (i = 0; i < NUMPOINTS; i++)
    {
      opoints[i][0] =     gmatrix[0][0] * points[i][0]
                        + gmatrix[0][1] * points[i][1]
                        + gmatrix[0][2] * points[i][2];
      opoints[i][1] =     gmatrix[1][0] * points[i][0]
                        + gmatrix[1][1] * points[i][1]
                        + gmatrix[1][2] * points[i][2];
      opoints[i][2] =     gmatrix[2][0] * points[i][0]
                        + gmatrix[2][1] * points[i][1]
                        + gmatrix[2][2] * points[i][2];
      flags[i] = true;
    }
  }
}
------------------------------------------------------------
loop at bench.cc:52: not vectorized: complicated access pattern.
loop at bench.cc:52: bad data access.


---


### compiler : `gcc`
### title : `vectorizer failed for vector normalization`
### open_at : `2004-11-12T01:33:52Z`
### last_modified_date : `2018-11-11T18:54:22Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=18439
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.0.0`
### severity : `enhancement`
### contents :
Vectorizer fails to handle this:

-----------------------------------------------------
extern "C" double sqrt(double);

#define NUMPOINTS 50000

static float points[NUMPOINTS][4];
static float opoints[NUMPOINTS][4];
static bool flags[NUMPOINTS];

void NormalizeVectors (void)
{
  int i, r;
  float s, x, y, z;
  static float d = 0.0;

  d += 0.2;
  if (d > 4) d = 0.0;

  for (r=0; r<4; r++)
  {
    for (i=0; i<NUMPOINTS; i++)
    {
      x = points[i][0];
      y = points[i][1];
      z = points[i][2];
      s = x * x
        + y * y
        + z * z;
      s = d / sqrt (s);
      opoints[i][0] = x * s;
      opoints[i][1] = y * s;
      opoints[i][2] = z * s;
      flags[i] = true;
    }
  }
}
-----------------------------------------------------

loop at bench.cc:79: not vectorized: unhandled data ref: d.0_36 = d
loop at bench.cc:79: bad data references.



This is a bit more complex than the other two I posted, I guess. Anyway, the 
first problem seems related to the static variable.


---


### compiler : `gcc`
### title : `We need to distinguish value extension and value truncation`
### open_at : `2004-11-12T09:42:26Z`
### last_modified_date : `2023-06-02T05:32:57Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=18446
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.0.0`
### severity : `enhancement`
### contents :
We use zero_extend and sign_extend in two different circumstances.  One is well
defined and one is conditionally undefined.

a) When extending a valid value in one representation to a valid value in a
longer representation.  For instance when converting a short to a long.  This is
well defined.

b) When truncating a possibly value from a longer representation to a shorter
one, where the value is possibly out of range of the shorter value.  (1) If this
is a straight type conversion, the operation is implementation defined (in C and
C++). (2) If, however, it this is the result of performing an operation at a
longer precision and then converting the result back to the orginal precision,
it is undefined.  For instance on 64bit hardware we might implement 32-bit
integer addition at 64 bits, followed by a truncation back to 32 bits.

Because we cannot later distinguish b2 from b1, we fail to optimize loops as
best we could.  In addition we have explicit extension operations that are nops
in a well formed program.

This is undoubtably a special case of annotating the regular mathematical
operations as wrap,undefined,dont-care on overflow.

I suspect this needs addressing at both the tree-level and the rtl-level


---


### compiler : `gcc`
### title : `SSE constant vector initialization produces dead constant values on stack`
### open_at : `2004-11-19T08:48:40Z`
### last_modified_date : `2021-07-26T02:43:29Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=18562
### status : `RESOLVED`
### tags : `missed-optimization, ssemmx`
### component : `target`
### version : `4.0.0`
### severity : `enhancement`
### contents :
Compiling this testcase with '-O2 -msse' an unoptimal code is produced. 'val1'
is merged into vector at compile time, but it is still loaded onto stack. Gcc
does not detect that 'val1' value on stack is sitting there unused.

#include <xmmintrin.h>
#include <stdio.h>

int main(void) {
	float val1 = 1.3f;
	float result[4];
	__m128 A;

	A = _mm_load1_ps(&val1);
	_mm_storeu_ps(result, A);

	printf("%f %f %f %f\n", result[0], result[1], result[2], result[3]);
	return 0;
}

This code is produced:
...
.LC2:                       <- merged vector
        .long   1067869798
        .long   0
        .long   0
        .long   0
        .text
        .p2align 4,,15
.globl main
        .type   main, @function
main:
        pushl   %ebp
        movl    %esp, %ebp
        subl    $72, %esp
        movss   .LC2, %xmm0           <- vector is loaded into %xmm0
        andl    $-16, %esp
        subl    $16, %esp
        movl    $0x3fa66666, -4(%ebp) <- 'val1' is put on stack here
        shufps  $0, %xmm0, %xmm0
        movl    $.LC1, (%esp)
        movups  %xmm0, -20(%ebp)
        flds    -8(%ebp)
        fstpl   28(%esp)
        flds    -12(%ebp)
        fstpl   20(%esp)
        flds    -16(%ebp)
        fstpl   12(%esp)
        flds    -20(%ebp)
        fstpl   4(%esp)
        call    printf
        xorl    %eax, %eax
        leave
        ret

Even worser situation arises with:

int main(void) {
	float val1[4] = {1.3f, 1.4f, 1.5f, 1.6f};
	float result[4];
	__m128 A;

	A = _mm_loadu_ps(val1);
	_mm_storeu_ps(result, A);

	printf("%f %f %f %f\n", result[0], result[1], result[2], result[3]);
	return 0;

Following asm code is produced:
main:
        pushl   %ebp
        movl    %esp, %ebp
        subl    $72, %esp
        andl    $-16, %esp
        movl    $0x3fa66666, -16(%ebp)
        subl    $16, %esp
        movl    $0x3fb33333, -12(%ebp)
        movl    $0x3fc00000, -8(%ebp)
        movl    $0x3fcccccd, -4(%ebp)
        movups  -16(%ebp), %xmm0
        movups  %xmm0, -32(%ebp)
        flds    -20(%ebp)
        fstpl   28(%esp)
        flds    -24(%ebp)
        fstpl   20(%esp)
        flds    -28(%ebp)
        fstpl   12(%esp)
        flds    -32(%ebp)
        fstpl   4(%esp)
        movl    $.LC4, (%esp)
        call    printf
        xorl    %eax, %eax
        leave
        ret

The constant values are not merged into vector at compile time, the vector is
built on the stack and then loaded into %xmm register. Value on stack is again
left unused after vector initialization.

Uros.


---


### compiler : `gcc`
### title : `Loop is not vectorized when it should be (VRP)`
### open_at : `2004-12-11T18:47:42Z`
### last_modified_date : `2023-08-07T07:55:43Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=18940
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.0.0`
### severity : `enhancement`
### contents :
Here is another case which my tree combiner confuses the other tree optimizations but it should not.
I get in .vect: "not vectorized: number of iterations cannot be computed.".
If I change D1360 to be just n, it works.
If I change "n <= 1" to be "D1360 <= 0" It works (on the mainline without my tree combiner which is 
the opposite of what my tree combiner does).


typedef float afloat __attribute__ ((__aligned__(16)));
int
main1 (int n , afloat * __restrict__ pa, afloat * __restrict__ pb)
{
  int i;
  int ivtmp51;
  int ivtmp35;
  int D1360 = n/2;
  
  if (n <= 1) return 0;
  
  ivtmp35 = 1;

  do {
    ivtmp51 = ivtmp35;
    pa[ivtmp51] = pb[ivtmp51];
    ivtmp35 = ivtmp51 + 1;
  }  while (D1360 > ivtmp51);
  
  return 0;
}


---


### compiler : `gcc`
### title : `HPPA64 does not support TImode`
### open_at : `2005-01-08T20:29:16Z`
### last_modified_date : `2022-01-20T17:22:35Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=19336
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.0.0`
### severity : `enhancement`
### contents :
Executing on host: /test/gnu/gcc-3.3/objdir/gcc/xgcc -B/test/gnu/gcc-3.3/objdir/
gcc/ /test/gnu/gcc-3.3/gcc/gcc/testsuite/gcc.dg/titype-1.c    -ansi -pedantic-er
rors  -lm   -o ./titype-1.exe    (timeout = 300)
/test/gnu/gcc-3.3/gcc/gcc/testsuite/gcc.dg/titype-1.c:5: error: unable to emulat
e 'TI'
compiler exited with status 1
output is:
/test/gnu/gcc-3.3/gcc/gcc/testsuite/gcc.dg/titype-1.c:5: error: unable to emulat
e 'TI'

We also have the following fail for the same reason:

FAIL: gcc.dg/uninit-C.c (test for excess errors)

TImode is not currently supported on hppa64.  Partly, this is because the
runtime documentation doesn't specifically document the alignment and calling
conventions for 128-bit scalar ints.  On the other hand, it does document the
conventions for long doubles (128 bit) and aggregates larger than 64 bits.
Both have the same alignment and calling conventions.

It appears we can support TImode if we presume that it should follow the same 
rules as long double.  HP libc has a signed long double to signed "quad" int.
However it lacks a function to do unsigned conversion.


---


### compiler : `gcc`
### title : `Invariant load not moved out of loop`
### open_at : `2005-01-09T10:50:41Z`
### last_modified_date : `2021-09-12T08:21:10Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=19347
### status : `NEW`
### tags : `alias, missed-optimization`
### component : `tree-optimization`
### version : `4.0.0`
### severity : `enhancement`
### contents :
In mesa benchmark (osmesa.c:678) 

         GLuint i, n, *ptr4;
         n = osmesa->rowlength * osmesa->height;
         ptr4 = (GLuint *) osmesa->buffer;
         for (i=0;i<n;i++) {
            *ptr4++ = osmesa->clearpixel;
         }   

The load of osmesa->clearpixel is not taken outside the loop by LIM because of 
aliasing limitations. This in turn also prevents vectorization.

In this particular case we can actually get the load moved out of the loop even 
without resolving the aliasing issue (which requires whole-program), on 
account that even if the store aliases the load, it will not alter the value 
loaded (because we store the same value that we loaded).

I'm looking into this in the context of the vectorizer.


---


### compiler : `gcc`
### title : `[meta-bug] bit-fields are non optimal`
### open_at : `2005-01-16T01:31:47Z`
### last_modified_date : `2023-10-09T20:41:11Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=19466
### status : `ASSIGNED`
### tags : `meta-bug, missed-optimization`
### component : `middle-end`
### version : `4.0.0`
### severity : `enhancement`
### contents :
Just a place holder for referencing all of the missed-optimizations with bit-fields.


---


### compiler : `gcc`
### title : `unnecessary atexit calls emitted for static objects with empty destructors`
### open_at : `2005-01-27T22:24:28Z`
### last_modified_date : `2023-03-24T00:54:56Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=19661
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `3.4.2`
### severity : `enhancement`
### contents :
When some object having empty destructor is declared as static in the local
context of some function g++ still inserts <atexit> call with the empty handler
like <__tcf_0> below.

It may seem like minor issue but redundant instructions increase chances for
I-cache misses and worthen processor pipeline.

Yuri


08048800 <__tcf_0>:
 8048800:       55                      push   %ebp
 8048801:       89 e5                   mov    %esp,%ebp
 8048803:       5d                      pop    %ebp
 8048804:       c3                      ret


--testcase--
begin 644 case-empty-atexit.tgz
M'XL(`.1G^4$``^V6VVJ#0!"&O=ZG&-*;))!D/:Q>)!1"GV31:2.83=`U&$KZ
M[!U-BI)#<U%)"YT/85?\]Z#C/[.Q+G""ZZW=3[3%*K4SIW>D#&2D%+5*JLBG
M5DHW4$U[PG&E&X5>Z(>^YTC7#X/(`=7_5BXI"ZMS`&=?YNEWN@1WF&VVC]C2
M(XDOXE]-7WI>0[I2AD%P,_X4^:_XUW\`Z0//"QV0/>_C*O\\_D(\I2;.R@1A
M4$U7`R&PLI@;V&W2!,H"AZ.Y$/2-;!K#$C3=B+5.S7`$[P(@WI06%@L8H*%1
M@[J+)LGF].@TMJ/)4.^PHSF(WWY[YIK_5SVO<<__7NM_GZ2-_U7$_G\$'?\O
MTDUA<]3K9U$6J7D#H]=8;'6,4-BDR0)Y&5O*`K7SEW4&:+V]I*XY"C!I/0X'
MDC:IY-6<#Z`$<:[\.,XZ&W=D"5Y..YZ1_##G_/%CKOA_0H'I]0QPM_Y+U=;_
M*"*]HHO]_PANE?]CJ6\/`8WGN\<``#VM/<UEG&$8AF$8AF$8AF$8AF$8AF$8
-AF'^#)_;GM5=`"@`````
`
end


---


### compiler : `gcc`
### title : `Loop optimizer fails to reverse simple loop`
### open_at : `2005-01-28T19:08:39Z`
### last_modified_date : `2021-11-29T05:42:19Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=19676
### status : `RESOLVED`
### tags : `missed-optimization, TREE`
### component : `tree-optimization`
### version : `4.0.0`
### severity : `minor`
### contents :
AVR Target 20041205 snapshot

gcc version 4.0.0 20041205 (experimental)
 /avrdev/libexec/gcc/avr/4.0.0/cc1.exe -quiet -v looprv.c -quiet -dumpbase
looprv.c -mmcu=atmega169 -auxbase looprv -Os -Wall -version -funsigned-char
-funsigned-bitfields -fpack-struct -fshort-enums -o looprv.s


Loop optimiser fails to reverse simple loop. Example

void testloop5(void)
{
	int i;
	for (i=0;i<100;i++)
	{
		if (!value)
		{
			foo();
		} 
	}
}

generates RTL setting index to 100 then using decrement/branch at end of loop as
expected. However, adding any kind of while/for loop inside outer loop leaves
index unoptimised. For example

void testloop3(void)
{
	int i;
	for (i=0;i<100;i++)
	{
		while (!value)
		{
		foo();
		}
	}
	
}

Here index starts at 0 and increments to 99.

Problem seems to be related to "maybe_multiple" being set in loop scan. However,
since 'i' is never used inside loop there would seem to be no need to check for
multiple setting.

This was tested with AVR target but looks like it will affect any target - I can
provide RTL etc on demand.


---


### compiler : `gcc`
### title : `sub-optimial register allocation with sse`
### open_at : `2005-01-28T23:34:16Z`
### last_modified_date : `2021-09-13T22:08:07Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=19680
### status : `NEW`
### tags : `missed-optimization, ra`
### component : `rtl-optimization`
### version : `4.0.0`
### severity : `enhancement`
### contents :
When comparing the kind of code ICC outputs vs gcc, it's really obvious gcc
could make a better use of x86 baroque addressing modes.
More specifically i rarely ever see it using the *8 scale factor, even when
addressing nicely power-of-2 sized stuff, and that's definitely a performance
problem when dealing with those large SSE vectors.

In that testcase the *8 scale factor is only used once and even if it's
questionnable the use a of a fancier mode would help in this particular
testcase, there's no doubt it would in Real World.

Also, take note of the horrible code for massage48; in Real World it's even worse:
  4012a6:       mov    $0x30,%edx
  4012af:       imul   %edx,%eax
That's not from the testcase, that's in a loop and edx get reloaded each time.

Tested with today's cvs and something like -O3 -march=k8 -fomit-frame-pointer
-mfpmath=sse and -O3 -march=pentium4 -fomit-frame-pointer -mfpmath=sse.


---


### compiler : `gcc`
### title : `Recognize common Fortran usages of copysign.`
### open_at : `2005-01-30T09:06:07Z`
### last_modified_date : `2021-05-14T10:48:33Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=19706
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.0.0`
### severity : `enhancement`
### contents :
While looking through LAPACK I notices a few patterns. For example, in drotg,
"r = dsign(1.0d0,x)*y".  This is really "r = y ^ (x & sign-bit)".  Compare this
with "r = (1.0 | (x & sign-bit)) * y" when expanding copysign on most systems.

Note that this can get kinda complex.  See slasv2.f,

      IF( PMAX.EQ.1 )
     $   TSIGN = SIGN( ONE, CSR )*SIGN( ONE, CSL )*SIGN( ONE, F )
      IF( PMAX.EQ.2 )
     $   TSIGN = SIGN( ONE, SNR )*SIGN( ONE, CSL )*SIGN( ONE, G )
      IF( PMAX.EQ.3 )
     $   TSIGN = SIGN( ONE, SNR )*SIGN( ONE, SNL )*SIGN( ONE, H )
      SSMAX = SIGN( SSMAX, TSIGN )
      SSMIN = SIGN( SSMIN, TSIGN*SIGN( ONE, F )*SIGN( ONE, H ) )

Note that this is, depending on how you count, either 3 or 11 sequential
copysign-of-one-and-mult operations.


---


### compiler : `gcc`
### title : `IBM 128bit long double format is not constant folded.`
### open_at : `2005-02-03T15:47:57Z`
### last_modified_date : `2022-12-19T20:38:00Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=19779
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.0.0`
### severity : `enhancement`
### contents :
This is the new bug for PR 19405. Keeping track of that we no longer constant fold long doubles in the 
IBM 128bit long double format.


---


### compiler : `gcc`
### title : `Missed optimizations due to signedness in the way`
### open_at : `2005-02-06T13:50:36Z`
### last_modified_date : `2021-03-15T00:43:15Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=19792
### status : `NEW`
### tags : `missed-optimization, TREE`
### component : `tree-optimization`
### version : `unknown`
### severity : `enhancement`
### contents :
Consider:

extern unsigned char size_lookup[257];

int
foo (unsigned int t)
{
  return (size_lookup [(int) t] == size_lookup[t]);
}

int
bar (unsigned int t)
{
  int a = t;
  return a == t;
}

Both functions should return 1, and in fact that's what the RTL optimizers
notice, but the tree optimizers don't.

This is somewhat related to PR 19790.


---


### compiler : `gcc`
### title : `Missed pure/const optimization`
### open_at : `2005-02-08T18:31:21Z`
### last_modified_date : `2021-07-26T03:04:07Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=19827
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.0.0`
### severity : `enhancement`
### contents :
The following two function should produce the same asm because we can skip the second call to f:
int f(void) __attribute__((const,pure));

int g(int i, int j)
{
  int k = 0;
  if(i)
    k = f();
  if (j)
    k = f();
  return k;
}
int h(int i, int j)
{
  int k = 0;
  if(i)
    k = f();
  else if (j)
    k = f();
  return k;
}


---


### compiler : `gcc`
### title : `Missing DSE/malloc/free optimization`
### open_at : `2005-02-08T21:35:13Z`
### last_modified_date : `2021-06-21T17:50:16Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=19831
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.0.0`
### severity : `enhancement`
### contents :
The following function really should be compiled to an empty function (DSE should first remove the 
store and then free of a malloc with no change inbetween and we should remove both calls).
void *malloc(__SIZE_TYPE__);
void free(void*);
int f(void)
{
  char *i = malloc(1);
  *i = 1;
  free (i);
}

This is something which is useful when we want to much higer level optimizations.


---


### compiler : `gcc`
### title : `don't remove an if when we know the value is the same as with the if (subtraction)`
### open_at : `2005-02-08T23:17:58Z`
### last_modified_date : `2023-09-01T12:23:14Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=19832
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.0.0`
### severity : `enhancement`
### contents :
According to Andrew Pinski , the following patch is useless because gcc should 
be able to find the optimisation by itself.



Description : function preferable in cse.c can be simplified if we notice
that, at the end of the function :
   if (regcost_a != regcost_b)
     return regcost_a - regcost_b;
   return 0;

So, if regcost_a == regcost_b, we return 0, but in this case (regcost_a -
regcost_b) is also = 0.
There is no need for the test, and (return regcost_a - regcost_b;) wins in
all cases.



This patch remove 3 572 566 useless tests (if regcost_a != regcost_b) when
doing a full bootstrap.



Bootstrap on a cygwin machine based on snapshot from 20050130.


2005-02-08  Christophe Jaillet <christophe.jaillet@wanadoo.fr>

    * cse.c (preferable): simplify last test to speed up



*** gcc-4.0-20050130/gcc/cse.c Tue Feb  8 23:39:30 2005
--- my_patch/cse.c Tue Feb  8 23:55:02 2005
*************** preferable (int cost_a, int regcost_a, i
*** 836,845 ****
    /* Normal operation costs take precedence.  */
    if (cost_a != cost_b)
      return cost_a - cost_b;
    /* Only if these are identical consider effects on register pressure.
*/
!   if (regcost_a != regcost_b)
!     return regcost_a - regcost_b;
!   return 0;
  }

  /* Internal function, to compute cost when X is not a register; called
--- 836,844 ----
    /* Normal operation costs take precedence.  */
    if (cost_a != cost_b)
      return cost_a - cost_b;
+
    /* Only if these are identical consider effects on register pressure.
*/
!   return regcost_a - regcost_b;
  }

  /* Internal function, to compute cost when X is not a register; called


---


### compiler : `gcc`
### title : `xor is enclosed in loop, and exectuted on each iteration of for statement`
### open_at : `2005-02-12T14:07:34Z`
### last_modified_date : `2021-07-26T01:58:34Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=19922
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.0.0`
### severity : `normal`
### contents :
#include <stdlib.h> 
 
void dupa() 
{ 
        double* wagi; 
        unsigned int i,synapsy=100; 
 
        wagi = (double*)malloc(100*synapsy); 
 
        for( i=0;i<synapsy;i++ ) { 
                wagi[i] = 0; 
        } 
 
} 
 
Simple test case, if compiled with 4.0 
gcc-4.0 (GCC) 4.0.0 20050212 (experimental) 
g++-4.0 -pedantic --save-temps -ftree-vectorize -O3 -Wall -mtune=pentium3 -c 
test.c 
 
essencialy I get: 
.LFB15: 
        pushl   %ebp 
.LCFI0: 
        movl    %esp, %ebp 
.LCFI1: 
        subl    $8, %esp 
.LCFI2: 
        movl    $10000, (%esp) 
        call    malloc 
        movl    $1, %edx 
        .p2align 4,,15 
.L2: 
        xorl    %ecx, %ecx 
        movl    %ecx, -8(%eax,%edx,8) 
        xorl    %ecx, %ecx 
        movl    %ecx, -4(%eax,%edx,8) 
        incl    %edx 
        cmpl    $101, %edx 
        jne     .L2 
        leave 
        ret 
so xor on ecx is executed twice! inside the loop. 
Looks simmilar with 3.4 
 
L5: 
        movl    $0, (%eax,%edx,8) 
        xorl    %ecx, %ecx 
        movl    %ecx, 4(%eax,%edx,8) 
        incl    %edx 
        cmpl    $100, %edx 
        jb      .L5 
 
 
on ultrasparc: 
.LLFB18: 
        save    %sp, -104, %sp 
.LLCFI0: 
        sethi   %hi(9216), %o0 
        call    malloc, 0 
         or     %o0, 784, %o0 
        mov     0, %g1 
.LL2: 
        add     %g1, %o0, %g2 
        add     %g1, 8, %g1 
        st      %g0, [%g2] 
        cmp     %g1, 800 
        bne     .LL2 
         st     %g0, [%g2+4] 
        jmp     %i7+8 
         restore 
 
It's odd because I do specify -O3 just to make sure code will be as fast as 
possible :) 
 
-O0 uses float point instructions to zero it, that's extremly slow than. 
and -O1 uses float point too, but code is 3x smaller and neater: 
        fldz 
.L2: 
        fstl    -8(%eax,%edx,8) 
        incl    %edx 
        cmpl    $101, %edx 
        jne     .L2 
        fstp    %st(0)


---


### compiler : `gcc`
### title : `[meta-bug] fold missing optimizations (compared to RTL)`
### open_at : `2005-02-15T22:07:03Z`
### last_modified_date : `2021-12-25T09:10:24Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=19986
### status : `NEW`
### tags : `meta-bug, missed-optimization, TREE`
### component : `middle-end`
### version : `4.0.0`
### severity : `enhancement`
### contents :
Just a meta-bug for all the missing fold which are missing which are in the RTL version of simplify_*.


---


### compiler : `gcc`
### title : `[meta-bug] fold missing optimizations in general`
### open_at : `2005-02-15T22:24:51Z`
### last_modified_date : `2023-09-22T16:38:07Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=19987
### status : `NEW`
### tags : `meta-bug, missed-optimization`
### component : `middle-end`
### version : `4.0.0`
### severity : `enhancement`
### contents :
Just a meta-bug for missing fold optimizations.


---


### compiler : `gcc`
### title : `x86_64 - 128 bit structs not targeted to TImode`
### open_at : `2005-02-17T03:35:41Z`
### last_modified_date : `2021-05-18T07:01:13Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=20020
### status : `RESOLVED`
### tags : `ABI, missed-optimization`
### component : `target`
### version : `4.0.0`
### severity : `enhancement`
### contents :
[Also posted to the GCC mailing list, http://gcc.gnu.org/ml/gcc/2005-
02/msg00692.html]


Given,

struct shared_ptr_struct
  {
    unsigned int phase  : 24;
    unsigned short thread : 16;
    void *addr;
  };

On the x86_64 (ie, Opteron[tm]) platform, GCC appears to designate the
underlying mode of this type as a BLKmode, instead of a TImode.  This
has implications in terms of the quality of the code that is generated
to copy and manipulate 128 bit structures (as defined in the example
above).

The decision to commit this type to a BLKmode value, originates
in this logic in mode_for_size():

      if (limit && size > MAX_FIXED_MODE_SIZE)
         return BLKmode;

On the x86 platform, there appears to be no target definition for
MAX_FIELD_SIZE. Thus, the default in stor-layout.c applies:

#ifndef MAX_FIXED_MODE_SIZE
#define MAX_FIXED_MODE_SIZE GET_MODE_BITSIZE (DImode)
#endif

Other 64 bit targets define MAX_FIXED_MODE_SIZE along these lines
(some line wrapping may occur below):

config/i960/i960.h:#define    MAX_FIXED_MODE_SIZE GET_MODE_BITSIZE
(TImode)
config/ia64/ia64.h:#define MAX_FIXED_MODE_SIZE GET_MODE_BITSIZE (TImode)
config/mips/mips.h:#define MAX_FIXED_MODE_SIZE LONG_DOUBLE_TYPE_SIZE
config/sh/sh.h:#define MAX_FIXED_MODE_SIZE (TARGET_SH5 ? 128 : 64)

on MIPS, LONG_DOUBLE_TYPE_SIZE is defined as follows:

/* A C expression for the size in bits of the type `long double' on
   the target machine.  If you don't define this, the default is two
   words.  */
#define LONG_DOUBLE_TYPE_SIZE \
  (mips_abi == ABI_N32 || mips_abi == ABI_64 ? 128 : 64)

In the 'dev' tree, the s390 defines MAX_FIXED_MODE_SIZE as follows:

config/s390/s390.h:#define MAX_FIXED_MODE_SIZE GET_MODE_BITSIZE
(TARGET_64BIT ? TImode : DImode)

(Arguably, the s390 variant might be a better default value to be defined
in stor-layout.c)


---


### compiler : `gcc`
### title : `If-conversion can't match equivalent code, and cross-jumping only works for literal matches`
### open_at : `2005-02-19T03:29:03Z`
### last_modified_date : `2019-03-06T05:01:09Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=20070
### status : `ASSIGNED`
### tags : `missed-optimization, patch`
### component : `rtl-optimization`
### version : `3.3`
### severity : `enhancement`
### contents :
If-conversion currently lacks the ability to merge two
basic blocks that are identical except for an input register
that can be set up using a conditional move, and possibly some
different local registers.

Cross-jumping lacks the ability to recognize that two blocks are
equivalent when there are different local registers, and (for -Os)
to find opportunities where setting up input registers will allow
to do cross jumping.

The problem has been discussed here:
http://gcc.gnu.org/ml/gcc-patches/2004-01/msg03281.html
http://gcc.gnu.org/ml/gcc-patches/2005-01/msg00672.html

A patch against 4.0 20050218 has been posted here:
http://gcc.gnu.org/ml/gcc-patches/2005-02/msg01066.html


---


### compiler : `gcc`
### title : `Missed optimization with conditional and basically ||`
### open_at : `2005-02-19T16:50:55Z`
### last_modified_date : `2023-06-07T02:45:56Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=20083
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.0.0`
### severity : `enhancement`
### contents :
The following three functions should result in the same assembly (the last is the best, branchless and 
only does one compare):
int f(int i, int j, int l)
{
  int k = 0;
  if (i)
   k = 1;
  if (j)
   k = 1; 
  if (l)
    k = 1;
  return k;
}
int f1(int i, int j, int l)
{
  int k = 0;
  if (i)
   k = 1;
  else if (j)
   k = 1; 
  else if (l)
   k = 1;
  return k;
}
int f2(int i, int j, int l)
{
  return i||j||l;
}

Note I came up with this testcase after adding code like the above code to gcc and I was wondering how 
we optimizated it.


---


### compiler : `gcc`
### title : `missed optimization with conditional and loads and cross jumping`
### open_at : `2005-02-19T16:58:35Z`
### last_modified_date : `2023-08-07T08:05:39Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=20084
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.0.0`
### severity : `enhancement`
### contents :
Like PR 20083 but a slightly different case, in a way this is missed jump crossing.
The following three functions should produce the same assembly code, f2 is the most optimal code.
Right now on the tcb only f1 and f2 are the same.

int f(int *i, int *j, int *l)
{
  int k = 0;
  if (*i)
   k = 1;
  if (*j)
   k = 1;
  if (*l)
    k = 1;
  return k;
}
int f1(int *i, int *j, int *l)
{
  int k = 0;
  if (*i)
   k = 1;
  else if (*j)
   k = 1;
  else if (*l)
   k = 1;
  return k;
}
int f2(int *i, int *j, int *l)
{
  int k = 0;
  if (*i)
   return 1;
  if (*j)
   return 1;
  return (*l)!=0;
}


---


### compiler : `gcc`
### title : `autoincrement generation is poor`
### open_at : `2005-02-25T16:19:12Z`
### last_modified_date : `2019-03-05T15:29:23Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=20211
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `2.95`
### severity : `enhancement`
### contents :
When a processor does not allow register+offset addressing for a register
class, as for the floating point registers on the SH3E / SH4, the way to
avoid excessive reloads and to expose the issue to the rtl optimizers is
to disallow this addressing mode for the machine modes for which pseudo
registers are usually allocated to the register class in question, i.e.
SFmode / DFmode in our example.
Thus, when there is a structure access to a member with such a mode and a
non-zero offset, the address cannot be expressed directly, and thus,
during rtl expansion, the sum is calculated into a pseudo register first.
cse typically places these additions together at the start of a basic
block; the idea there is that we might find some cse opportunities, and
if not, combine can do something with these sums.  However, that doesn't
work when these sums are used as addresses and the machine mode of the
access does not allow reg+offset addressing.  The auto-increment generation
is flow can't do anything useful with these sums either, since the auto-inc
generation in flow only looks for cases where a memory access already matches
an exitsing add.  Thus we end up with lots of adds and sky-high register
pressure.  On two-address machines, there i an added problem that the
adds are so arranged that (at least, not counting reloads...) a
two-instruction sequence is needed to do the additions.

What is required is an optimization pass that finds all the uses of a sum
of a base register and an offset in a basic block, and figures out where an
auto-increment addressing mode can be profitably used, and also to reduce the
register pressure and number of reg-reg copies.

A patch against 4.0 20050218 is here:
http://gcc.gnu.org/ml/gcc-patches/2005-02/msg01612.html


---


### compiler : `gcc`
### title : `missed optimization of loop IV modulus`
### open_at : `2005-02-27T06:53:40Z`
### last_modified_date : `2022-12-01T03:41:42Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=20231
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.1.0`
### severity : `enhancement`
### contents :
[zebes:~] astrange% /usr/local/bin/gcc -v
Using built-in specs.
Target: powerpc-apple-darwin7.7.0
Configured with: ../configure --enable-threads=posix --with-threads=posix
Thread model: posix
gcc version 4.1.0 20050226 (experimental)

Command line: /usr/local/bin/gcc -O3 -mcpu=7400 -mtune=7400 -fdump-tree-optimized -c 
mod_loop.c

Code:
void mod_loop(unsigned char *array, int len, unsigned char repeat)
{
        unsigned char i;
        for (i = 0; i < len; i++) array[i] = i%repeat;
}

void mod_loop2(unsigned char *array, int len, unsigned char repeat)
{
        unsigned char i,i2=0;
        for (i = 0; i < len; i++) {array[i] = i2++; if (i2 == repeat) i2 = 0;}
}

Although the two functions are equivalent and mod_loop2 is better (avoiding an expensive divide), GCC 
doesn't transform the first into the second.


---


### compiler : `gcc`
### title : `optimising muldiv() type operations`
### open_at : `2005-03-02T14:25:42Z`
### last_modified_date : `2021-08-11T07:39:28Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=20283
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.2.1`
### severity : `enhancement`
### contents :
Reading specs from /usr/lib/gcc-lib/i586-suse-linux/3.3.4/specs
Configured with: ../configure --enable-threads=posix --prefix=/usr
--with-local-prefix=/usr/local --infodir=/usr/share/info --mandir=/usr/share/man
--enable-languages=c,c++,f77,objc,java,ada --disable-checking --libdir=/usr/lib
--enable-libgcj --with-gxx-include-dir=/usr/include/g++ --with-slibdir=/lib
--with-system-zlib --enable-shared --enable-__cxa_atexit i586-suse-linux
Thread model: posix
gcc version 3.3.4 (pre 3.3.5 20040809)
 /usr/lib/gcc-lib/i586-suse-linux/3.3.4/cc1 -E -quiet -v -D__GNUC__=3
-D__GNUC_MINOR__=3 -D__GNUC_PATCHLEVEL__=4 muldiv.c -march=pentium -O3 muldiv.i
#include "..." search starts here:
#include <...> search starts here:
 /usr/local/include
 /usr/lib/gcc-lib/i586-suse-linux/3.3.4/include
 /usr/i586-suse-linux/include
 /usr/include
End of search list.
 /usr/lib/gcc-lib/i586-suse-linux/3.3.4/cc1 -fpreprocessed muldiv.i -quiet
-dumpbase muldiv.c -march=pentium -auxbase muldiv -O3 -version -o muldiv.s
GNU C version 3.3.4 (pre 3.3.5 20040809) (i586-suse-linux)
        compiled by GNU C version 3.3.4 (pre 3.3.5 20040809).
GGC heuristics: --param ggc-min-expand=63 --param ggc-min-heapsize=63486

When compiling the following function:

gcc -O3 -S -march=pentium

int vat(int a)
{
  return a * 47 / 40;
}

optimising misses the trick of combining the multiply and divide into a single
multiply and shift arithmetic right.

# assume value is already in EAX
movl 1261646643,%ecx
imul %ecx
sarl $30 # I mean shift %edx,%eax pair right by 30 bits

I realise I haven't chosen the value properly to give the same results as an
overflow when multiplying by 47, but is that defined in the standard?


---


### compiler : `gcc`
### title : `Unnecessary code generated for empty structs`
### open_at : `2005-03-10T15:48:14Z`
### last_modified_date : `2021-02-12T02:30:16Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=20408
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.1.0`
### severity : `normal`
### contents :
Given an empty struct (ie struct X { };), even at high optimisation levels g++
will insist on always allocating and zeroing some memory for empty structs.

This actually effects C++ code, including libstdc++-v3, as empty structs are
often used as a means of passing around functions.

EXAMPLE
------------------
struct X {};

void foo(X);

void call_foo()
{ foo(X()); }
------------------

generates (from -O3, t70.final_cleanup is:)
-------------------------------------------------
;; Function void call_foo() (_Z8call_foov)

void call_foo() ()
{
  struct X D.1597;

<bb 0>:
  D.1597 = 0;
  foo (D.1597) [tail call];
  return;

}
---------------------------------------------


---


### compiler : `gcc`
### title : `complex reciprocal has too many operations`
### open_at : `2005-03-11T21:17:24Z`
### last_modified_date : `2021-08-15T00:53:13Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=20432
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.1.0`
### severity : `normal`
### contents :
#include <math.h>
#include <complex.h>

int main()
{
    float complex c,d;
    foo(&c);
    d=1.0/c;
    return creal(d)+cimag(d)<0;
}
$ gcc -S -O -fdump-tree-optimized recip.c
$ tail -25 recip.c.t66.optimized
<bb 0>:
  foo (&c);
  SR.24 = (double) REALPART_EXPR <c>;
  SR.23 = (double) IMAGPART_EXPR <c>;
  if (ABS_EXPR <SR.24> < ABS_EXPR <SR.23>) goto <L1>; else goto <L2>;

<L1>:;
  D.2387 = SR.24 / SR.23;
  D.2389 = SR.23 + SR.24 * D.2387;
  SR.25 = (D.2387 + 0.0) / D.2389;
  SR.26 = (D.2387 * 0.0 - 1.0e+0) / D.2389;
  goto <bb 3>;

<L2>:;
  D.2395 = SR.23 / SR.24;
  D.2397 = SR.24 + SR.23 * D.2395;
  SR.25 = (D.2395 * 0.0 + 1.0e+0) / D.2397;
  SR.26 = (0.0 - D.2395) / D.2397;

<bb 3>:
  return (double) (float) SR.25 + (double) (float) SR.26 < 0.0;

}

$ gcc -v
Using built-in specs.
Target: i686-pc-linux-gnu
Configured with: ../gcc-4.1/configure --prefix=/home/ig25 --enable-languages=c,f95
Thread model: posix
gcc version 4.1.0 20050311 (experimental)

I can't see a reason why the +0 and *0 operations should
be necessary.  

Thomas


---


### compiler : `gcc`
### title : `hoisting of label out of jumptable would take place at cse, should happen at trees`
### open_at : `2005-03-17T08:21:32Z`
### last_modified_date : `2023-08-05T03:09:54Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=20514
### status : `ASSIGNED`
### tags : `missed-optimization, TREE`
### component : `tree-optimization`
### version : `4.0.0`
### severity : `enhancement`
### contents :
The following testcase from bug 18628 exposes a case in which cse would have
folded a load from a jump table into a label.  Jeff suspects this should have
happened earlier, in the tree level, so he asked me to file this bug.  Here's
the testcase:

int i;
int main()
{
  for (;;)
  {
    switch (i)
    {
      case 0:
      case 1:
        return 1;

      case 2:
      case 3:
        return 0;

      case 5:
        --i;
    }
  }
}


---


### compiler : `gcc`
### title : `bit shift/mask optimization potential`
### open_at : `2005-03-17T13:17:18Z`
### last_modified_date : `2021-06-27T23:26:13Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=20517
### status : `RESOLVED`
### tags : `missed-optimization, TREE`
### component : `tree-optimization`
### version : `4.1.0`
### severity : `enhancement`
### contents :
$ cat shift.c
#include <stdio.h>

#define OFFSET 4
#define MASK 0xf0

int main()
{
    unsigned int f,g;
    scanf("%u",&f);
    if ((f & MASK) >> OFFSET == 1) {
        printf("success\n");
    }
    return 0;
}
$ gcc -S -O2 -fdump-tree-optimized shift.c
$ tail -20 shift.c.t66.optimized
  unsigned int g;
  unsigned int f;
  int D.1807;
  unsigned int D.1806;
  unsigned int D.1805;
  unsigned int f.10;

<bb 0>:
  scanf (&"%u"[0], &f);
  if ((f & 240) >> 4 == 1) goto <L0>; else goto <L1>;

<L0>:;
  printf (&"success\n"[0]);

<L1>:;
  return 0;

}


$ gcc -v
Using built-in specs.
Target: ia64-unknown-linux-gnu
Configured with: ../gcc-4.1-20050306/configure --prefix=/home/zfkts
--enable-languages=c,f95 --disable-optimization
Thread model: posix
gcc version 4.1.0 20050306 (experimental)

The expression (f & 0xf0) >> 4 == 1 could be optimized
to f & 0xf == 1 << 4.

Code like that occurs in the libgfortan library.


---


### compiler : `gcc`
### title : `Poor bit-field code generation`
### open_at : `2005-03-28T19:25:17Z`
### last_modified_date : `2021-07-21T00:41:01Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=20671
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.0.0`
### severity : `enhancement`
### contents :
This test simulates the process of clearing the "present" bit
in an x86 page table entry.  The code *should* load the PTE,
clear the present bit, and store the PTE.  On x86, it is
possible to perform these 3 steps in a single instruction, i.e.
AND memory with immediate operand.  The code should also be
preceede with a null check for the access object.

package Bit_Test is

  type Page_Frame_Number is
    mod 2 ** 20;

  type Page_Table_Entry is
    record
      P   : Boolean;
      RW  : Boolean;
      U   : Boolean;
      PWT : Boolean;
      PCD : Boolean;
      A   : Boolean;
      D   : Boolean;
      PSE : Boolean;
      G   : Boolean;
      PFN : Page_Frame_Number;
    end record;

  for Page_Table_Entry use
    record
      P   at 0 range  0 ..  0;
      RW  at 0 range  1 ..  1;
      U   at 0 range  2 ..  2;
      PWT at 0 range  3 ..  3;
      PCD at 0 range  4 ..  4;
      A   at 0 range  5 ..  5;
      D   at 0 range  6 ..  6;
      PSE at 0 range  7 ..  7;
      G   at 0 range  8 ..  8;
      PFN at 0 range 12 .. 31;
    end record;

  type Page_Table_Entry_Access is
    access Page_Table_Entry;

  procedure Invalidate_PTE (
    PTE : in Page_Table_Entry_Access
    );

end Bit_Test;

package body Bit_Test is

  procedure Invalidate_PTE (
    PTE : in Page_Table_Entry_Access
    ) is
  begin
    PTE.all := (
      P   => False,
      RW  => PTE.RW,
      U   => PTE.U,
      PWT => PTE.PWT,
      PCD => PTE.PCD,
      A   => PTE.A,
      D   => PTE.D,
      PSE => PTE.PSE,
      G   => PTE.G,
      PFN => PTE.PFN
    );
  end Invalidate_PTE;

end Bit_Test;

Code generated for Invalidate_PTR:

000000a0 <bit_test__invalidate_pte>:
  a0:   55                      push   %ebp
  a1:   89 e5                   mov    %esp,%ebp
  a3:   57                      push   %edi
  a4:   56                      push   %esi
  a5:   53                      push   %ebx
  a6:   83 ec 1c                sub    $0x1c,%esp
  a9:   8b 7d 08                mov    0x8(%ebp),%edi
  ac:   85 ff                   test   %edi,%edi
  ae:   0f 84 e0 00 00 00       je     194 <bit_test__invalidate_pte+0xf4>
  b4:   0f b6 07                movzbl (%edi),%eax
  b7:   88 c2                   mov    %al,%dl
  b9:   88 c1                   mov    %al,%cl
  bb:   d0 ea                   shr    %dl
  bd:   88 c3                   mov    %al,%bl
  bf:   80 e2 01                and    $0x1,%dl
  c2:   88 55 eb                mov    %dl,0xffffffeb(%ebp)
  c5:   88 c2                   mov    %al,%dl
  c7:   c0 ea 04                shr    $0x4,%dl
  ca:   80 e2 01                and    $0x1,%dl
  cd:   88 55 ef                mov    %dl,0xffffffef(%ebp)
  d0:   88 c2                   mov    %al,%dl
  d2:   c0 ea 05                shr    $0x5,%dl
  d5:   80 e2 01                and    $0x1,%dl
  d8:   88 55 f0                mov    %dl,0xfffffff0(%ebp)
  db:   88 c2                   mov    %al,%dl
  dd:   c0 ea 06                shr    $0x6,%dl
  e0:   80 e2 01                and    $0x1,%dl
  e3:   88 55 f1                mov    %dl,0xfffffff1(%ebp)
  e6:   88 c2                   mov    %al,%dl
  e8:   24 fe                   and    $0xfe,%al
  ea:   c0 ea 07                shr    $0x7,%dl
  ed:   88 55 f2                mov    %dl,0xfffffff2(%ebp)
  f0:   c0 e9 02                shr    $0x2,%cl
  f3:   0f b6 57 01             movzbl 0x1(%edi),%edx
  f7:   80 e1 01                and    $0x1,%cl
  fa:   c0 eb 03                shr    $0x3,%bl
  fd:   80 e3 01                and    $0x1,%bl
 100:   80 e2 01                and    $0x1,%dl
 103:   88 55 f3                mov    %dl,0xfffffff3(%ebp)
 106:   8b 37                   mov    (%edi),%esi
 108:   88 07                   mov    %al,(%edi)
 10a:   0f b6 55 eb             movzbl 0xffffffeb(%ebp),%edx
 10e:   8b 07                   mov    (%edi),%eax
 110:   01 d2                   add    %edx,%edx
 112:   83 e0 fd                and    $0xfffffffd,%eax
 115:   09 d0                   or     %edx,%eax
 117:   0f b6 d1                movzbl %cl,%edx
 11a:   89 07                   mov    %eax,(%edi)
 11c:   c1 e2 02                shl    $0x2,%edx
 11f:   83 e0 fb                and    $0xfffffffb,%eax
 122:   09 d0                   or     %edx,%eax
 124:   0f b6 d3                movzbl %bl,%edx
 127:   89 07                   mov    %eax,(%edi)
 129:   c1 e2 03                shl    $0x3,%edx
 12c:   83 e0 f7                and    $0xfffffff7,%eax
 12f:   09 d0                   or     %edx,%eax
 131:   89 07                   mov    %eax,(%edi)
 133:   83 e0 ef                and    $0xffffffef,%eax
 136:   0f b6 55 ef             movzbl 0xffffffef(%ebp),%edx
 13a:   c1 e2 04                shl    $0x4,%edx
 13d:   09 d0                   or     %edx,%eax
 13f:   89 07                   mov    %eax,(%edi)
 141:   83 e0 df                and    $0xffffffdf,%eax
 144:   0f b6 55 f0             movzbl 0xfffffff0(%ebp),%edx
 148:   c1 e2 05                shl    $0x5,%edx
 14b:   09 d0                   or     %edx,%eax
 14d:   89 07                   mov    %eax,(%edi)
 14b:   09 d0                   or     %edx,%eax
 14d:   89 07                   mov    %eax,(%edi)
 14f:   83 e0 bf                and    $0xffffffbf,%eax
 152:   0f b6 55 f1             movzbl 0xfffffff1(%ebp),%edx
 156:   c1 e2 06                shl    $0x6,%edx
 159:   09 d0                   or     %edx,%eax
 15b:   89 07                   mov    %eax,(%edi)
 15d:   0f b6 55 f2             movzbl 0xfffffff2(%ebp),%edx
 161:   c1 e2 07                shl    $0x7,%edx
 164:   25 7f ff ff ff          and    $0xffffff7f,%eax
 169:   09 d0                   or     %edx,%eax
 16b:   81 e6 00 f0 ff ff       and    $0xfffff000,%esi
 171:   89 07                   mov    %eax,(%edi)
 173:   25 ff fe ff ff          and    $0xfffffeff,%eax
 178:   0f b6 55 f3             movzbl 0xfffffff3(%ebp),%edx
 17c:   c1 e2 08                shl    $0x8,%edx
 17f:   09 d0                   or     %edx,%eax
 181:   89 07                   mov    %eax,(%edi)
 183:   25 ff 0f 00 00          and    $0xfff,%eax
 188:   09 f0                   or     %esi,%eax
 18a:   89 07                   mov    %eax,(%edi)
 18c:   83 c4 1c                add    $0x1c,%esp
 18f:   5b                      pop    %ebx
 190:   5e                      pop    %esi
 191:   5f                      pop    %edi
 192:   5d                      pop    %ebp
 193:   c3                      ret


---


### compiler : `gcc`
### title : `unrolling does not take target register pressure into account.`
### open_at : `2005-04-12T15:42:15Z`
### last_modified_date : `2019-03-05T15:48:52Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=20969
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.1.0`
### severity : `normal`
### contents :
When a loop contains multiple labels inside, unrolling it increases the
target register pressure on targets that need target registers to do
branches.  This gets quickly so bad that the unrolled loop performs worse
than a non-unrolled loop, because of the number of target register spills.


---


### compiler : `gcc`
### title : `move memory allocation out of a loop`
### open_at : `2005-04-15T12:41:56Z`
### last_modified_date : `2023-10-23T05:50:45Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=21046
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.1.0`
### severity : `enhancement`
### contents :
Consider the following program fragment:

  char *p;
  int i;

  for (i=0; i<10; i++)
    {
      p = malloc(20);
      foo(p,i);
      free(p);
    }
}

The loop could be simplified into

  p = malloc(20);
  for (i=0; i<10; i++)
    foo(p,i);

  free(p);

This would reduce the overhead for memory allocation
considerably.

A more challenging case is to change

  for (i=0; i<10; i++)
    {
      p = malloc(2*i+2);
      foo(p,i);
      free(p);
    }

into

  p = malloc(20);
  for (i=0; i<10; i++)
      foo(p,i);

  free(p);

because the amount of memory allocated has an upper bound.

This is probably not a big win for straight C code.  For languages
which generate temporary arrays at runtime, such as Fortran, it
could mean a significant reduction in memory management overhead.


---


### compiler : `gcc`
### title : `missed tail call optimization when local address could escape`
### open_at : `2005-04-18T19:53:57Z`
### last_modified_date : `2021-08-22T02:14:48Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=21093
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.1.0`
### severity : `enhancement`
### contents :
Missed tail call optimization when local address could escape but not on the condition:
void f(void);
void f1(int *);

void g(int i, int j)
{
  if (j)
    return f();
  return f1(&i);
}

This might be a reduced testcase from fold_binary to fold_build2 where we have this issue, but I have 
not looked through all of the conditionals to see if this is true.


---


### compiler : `gcc`
### title : `Convert (a >> 2) & 1 != 0 into a & 4 != 0`
### open_at : `2005-04-21T00:47:02Z`
### last_modified_date : `2022-08-13T14:03:43Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=21137
### status : `RESOLVED`
### tags : `missed-optimization, TREE`
### component : `tree-optimization`
### version : `unknown`
### severity : `enhancement`
### contents :
At tree level, we would like to canonicalize (a >> 2) & 1 != 0 into a & 4 != 0.

Currently,

void bar (void);

void
foo (int a)
{
  if ((a >> 2) & 1)
    bar ();
}

turns into

foo (a)
{
  int D.1235;
  int D.1236;
  _Bool D.1237;

  D.1235 = a >> 2;
  D.1236 = D.1235 & 1;
  D.1237 = (_Bool) D.1236;
  if (D.1237)
    {
      bar ();
    }
  else
    {
      
    }
}


---


### compiler : `gcc`
### title : `Suboptimal byte extraction from 64bits`
### open_at : `2005-04-21T13:10:10Z`
### last_modified_date : `2021-07-25T00:51:24Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=21150
### status : `RESOLVED`
### tags : `missed-optimization, ra`
### component : `rtl-optimization`
### version : `3.4.3`
### severity : `normal`
### contents :
Bytes are typically extracted from e.g. u64's by something like

#define D5(v) (((v) >> 40) & 0xff)

Testcase shows that gcc does not optimize this "good enough".


---


### compiler : `gcc`
### title : `[11/12/13/14 Regression] gcc can use registers but uses stack instead`
### open_at : `2005-04-23T22:30:32Z`
### last_modified_date : `2023-07-15T07:36:04Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=21182
### status : `NEW`
### tags : `missed-optimization, ra`
### component : `rtl-optimization`
### version : `3.4.3`
### severity : `normal`
### contents :
in this long but relatively simple function gcc
can store all frequently used local variables in registers,
but it fails to do so.

gcc can be forced to do this optimization by asm("reg") modifiers.
Resulting code is ~1k smaller.

# gcc -v
Reading specs from
/.share/usr/app/gcc-3.4.3/bin/../lib/gcc/i386-pc-linux-gnu/3.4.3/specs
Configured with: ../gcc-3.4.3/configure --prefix=/usr/app/gcc-3.4.3
--exec-prefix=/usr/app/gcc-3.4.3 --bindir=/usr/bin --sbindir=/usr/sbin
--libexecdir=/usr/app/gcc-3.4.3/libexec --datadir=/usr/app/gcc-3.4.3/share
--sysconfdir=/etc --sharedstatedir=/usr/app/gcc-3.4.3/var/com
--localstatedir=/usr/app/gcc-3.4.3/var --libdir=/usr/lib
--includedir=/usr/include --infodir=/usr/info --mandir=/usr/man
--with-slibdir=/usr/app/gcc-3.4.3/lib --with-local-prefix=/usr/local
--with-gxx-include-dir=/usr/app/gcc-3.4.3/include/g++-v3
--enable-languages=c,c++ --with-system-zlib --disable-nls --enable-threads=posix
i386-pc-linux-gnu
Thread model: posix
gcc version 3.4.3


---


### compiler : `gcc`
### title : `Move maximum out of a loop`
### open_at : `2005-04-29T08:17:33Z`
### last_modified_date : `2023-06-09T15:41:24Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=21278
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.1.0`
### severity : `enhancement`
### contents :
This could help in reducing the amount of work for bounds
checking.

$ cat mymax.c
#include <stdlib.h>
#include <stdio.h>

int main()
{
  char *p;
  int i,j,n;

  scanf("%d",&n);
  j = 0;
  for (i=0; i<n; i++)
    {
        if (j < i)
            j = i;
    }
    printf("%d\n",j);
    return 0;
}
$ gcc -g -funroll-all-loops -S -O3 -fdump-tree-optimized  mymax.c

still does the do loop:

<L13>:;
  j = 0;
  i = 0;

<L0>:;
  j = MAX_EXPR <j, i>;
  i = i + 1;
  if (i != n.10) goto <L0>; else goto <L4>;

when the loop could be optimized to

    if (n <= 0)
        j = 0;
    else
        j = n-1;


---


### compiler : `gcc`
### title : `missed optimizations when comparing address to NULL`
### open_at : `2005-05-09T17:22:15Z`
### last_modified_date : `2023-06-25T21:00:45Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=21474
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.1.0`
### severity : `enhancement`
### contents :
The program below gives some expressions which gcc could, but does not, evaluate
to true.  E.g. gcc considers &p->a true, even when a is the first element
of the struct (is this a bug?), but does not consider &p->b[3] to be true.

struct foo {int a, b[10];};
 
int subr(int i, struct foo *p)
{
    int x[10];
 
#if 0
    // gcc folds this
    if (&p->a) return 1;
#else
    // but not these
    if (&p->b[3]) return 1;
 
    if (&x[3] != 0) return 1;
    if (&x[i] != 0) return 1;  // not sure if this one is safe to fold
#endif
    return 0;
}


---


### compiler : `gcc`
### title : `[11/12/13/14 Regression] missed load PRE, PRE makes i?88/9/10/11/12 suck`
### open_at : `2005-05-10T09:03:36Z`
### last_modified_date : `2023-07-07T10:28:27Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=21485
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.0.0`
### severity : `normal`
### contents :
I've found a major performance regression in gcc 4.0.0's optimization of the
BYTEmark numsort benchmark.  I've boiled it down to a testcase that I think will
suit you... it outputs a single number representing the number of iterations run
(higher is better).  On my machine I get 900ish under 4.0.0 and around 1530 on
3.4.3.

Both were compiled and run in a Gentoo test partition, if that makes a difference:
3.4.3: gcc version 3.4.3-20050110 (Gentoo Linux 3.4.3.20050110-r2,
ssp-3.4.3.20050110-0, pie-8.7.7)
4.0.0: gcc version 4.0.0 (Gentoo Linux 4.0.0)


---


### compiler : `gcc`
### title : `missed optimization due with const function and pulling out of loops`
### open_at : `2005-05-22T19:18:03Z`
### last_modified_date : `2021-07-26T02:22:10Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=21712
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.0.0`
### severity : `enhancement`
### contents :
gcc -v
Lecture des spécification à partir de /usr/lib/gcc-lib/powerpc-linux/3.3.6/specs
Configuré avec: ../src/configure -v
--enable-languages=c,c++,java,f77,pascal,objc,ada --prefix=/usr
--mandir=/usr/share/man --infodir=/usr/share/info
--with-gxx-include-dir=/usr/include/c++/3.3 --enable-shared
--enable-__cxa_atexit --with-system-zlib --enable-nls --without-included-gettext
--enable-clocale=gnu --enable-debug --enable-java-gc=boehm
--enable-java-awt=xlib --enable-objc-gc --disable-multilib powerpc-linux
Modèle de thread: posix
version gcc 3.3.6 (Debian 1:3.3.6-5)


BEGIN_CODE
#define CONST __attribute__((const))

int get_type1(void) CONST;
int get_type2(void) CONST;

void* cast(void*, int) CONST;

void do_something(void*);

void baz(void* p)
{
	while(1)
	{
		do_something(cast(p, get_type1()));
		do_something(cast(p, get_type2()));
	}
}
END_CODE


gcc-4.0 -Wall -O3 -S

BEGIN_ASM
baz:
        mflr 0
        stwu 1,-16(1)
        stw 30,8(1)
        mr 30,3
        stw 31,12(1)
        stw 0,20(1)
        bl get_type1
        mr 4,3
        mr 3,30
        bl cast
        mr 31,3
.L3:
        mr 3,31
        bl do_something
        bl get_type2
        mr 4,3
        mr 3,30
        bl cast
        bl do_something
        b .L3
END_ASM


why the call to get_type2() and cast() are not moved outside the loop just like
get_type1() and the first call to cast() ?
Thanks.


---


### compiler : `gcc`
### title : `libgcc could use some ia32/x86_64 specific optimizations`
### open_at : `2005-05-30T05:23:43Z`
### last_modified_date : `2021-07-21T04:33:00Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=21812
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `unknown`
### severity : `enhancement`
### contents :
libgcc is currently contains pure C functions with simple (i.e. non-optimal
implementations). Allowing individual targets to provide their own versions of
the functions could boost performance.

i.e. comparing the libgcc C implementation of __popcountdi2 to the assembly
version provided in the Opteron optimization manual, we find that the AMD
supplied version is half the instructions, branchless, uses no data tables (and
thus causes no cache misses), and runs in about 1/3 to 1/2 less time.


---


### compiler : `gcc`
### title : `unroll misses simple elimination - works with manual unroll`
### open_at : `2005-05-30T18:37:49Z`
### last_modified_date : `2023-05-26T00:30:44Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=21827
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `3.4.3`
### severity : `enhancement`
### contents :
Using gentoo gcc 3.4.3

This could look like http://gcc.gnu.org/bugzilla/show_bug.cgi?id=11707
(and they might be the same. However I think I had the problem with 3.3.4 too)

I have also had this problem in other older versions. In 2 projects I have been
on this has been really annoying. I think that if a loop is unrolled and the
variable is eliminated it should be replaced with a constant (and then always
false ifs should be removed) 

That is not the case:
int test(int v)
{
  int x = 0;
  for (int u=0;u<2;u++)
  {
    if (u>v)  // v is input-arg the compiler can't deside at compiletime
    {
      if (u%2==1) // can only happen for u==1 (so loops for 0 and 2 does not do
        x++;      // anything. Hoped gcc would notice when unrolling.
    }
  }  
  return x;
}

g++ -O3 -unroll-loops -S simple_test.cpp 

gives me the following code:
	.text
	.align 2
	.p2align 4,,15
.globl _Z4testi
	.type	_Z4testi, @function
_Z4testi:
.LFB2:
	pushl	%ebp
.LCFI0:
	xorl	%edx, %edx
	movl	%esp, %ebp
.LCFI1:
	xorl	%eax, %eax
	incl	%eax
	cmpl	8(%ebp), %eax
	jle	.L4
	testb	$1, %al
	setne	%cl
	movzbl	%cl, %eax
	addl	%eax, %edx
.L4:
	popl	%ebp
	movl	%edx, %eax
	ret
.LFE2:
	.size	_Z4testi, .-_Z4testi
	.section	.note.GNU-stack,"",@progbits
	.ident	"GCC: (GNU) 3.4.3-20050110 (Gentoo 3.4.3.20050110-r2,
ssp-3.4.3.20050110-0, pie-8.7.7)"

If I manually unroll like :

int test(int v)
{
  int x = 0;

  if (0>v)
  {
    if (0%2==1)
      x++;
  }
  if (1>v)
  {
    if (1%2==1)
      x++;
  }
  if (2>v)
  {
    if (2%2==1)
      x++;
  }  
  
  return x;
}

And then just with O3 I get the much nicer :
	.text
	.align 2
	.p2align 4,,15
.globl _Z4testi
	.type	_Z4testi, @function
_Z4testi:
.LFB2:
	pushl	%ebp
.LCFI0:
	xorl	%eax, %eax
	movl	%esp, %ebp
.LCFI1:
	cmpl	$0, 8(%ebp)
	popl	%ebp
	setle	%al
	ret
.LFE2:
	.size	_Z4testi, .-_Z4testi
	.section	.note.GNU-stack,"",@progbits
	.ident	"GCC: (GNU) 3.4.3-20050110 (Gentoo 3.4.3.20050110-r2,
ssp-3.4.3.20050110-0, pie-8.7.7)"

I have had too cases where this optimization is very important. One is if you a
kind of program a chessboard "from within". The other case were a raytracer I
wrote with a friend. In that situation we had to seattle with a not that fast
switch (since we did not wanted to pollute out code with a manual unroll.)

The chessboard example (here a simple case - how many knightsmove does white
have. We do not consider check, pins or that pieces can be in the way)

int knight_square_count(unsigned char* board)
{
  int count = 0;
  for (int bp=0;bp<64;bp++)
  {
    if (board[bp]==WHITE_KNIGHT)
    {
      if (bp%8>1 && bp/8>0) count++;
      if (bp%8>0 && bp/8>1) count++;
      if (bp%8<6 && bp/8>0) count++;
      if (bp%8<7 && bp/8>1) count++;
      if (bp%8>1 && bp/8<7) count++;
      if (bp%8>0 && bp/8<6) count++;
      if (bp%8<6 && bp/8<7) count++;
      if (bp%8<7 && bp/8<6) count++;
    }
  }
  return count;
}

In the above situation a manual unroll (with O3) is more than 400% faster.
(I have timed it and it is close to 500%) I thought that one of the main ideas
of unrolling loops was to make a kind of every loop "its own" (Without making
ugly code)

regards and thanks for the best (free) compiler
Bsc Computer Science 
Thorbjørn Martsum

PS : There might also be a reason for things being as they are. Then I just
don't understand why - please explain then


---


### compiler : `gcc`
### title : `GCC should combine adjacent stdio calls`
### open_at : `2005-06-09T12:56:53Z`
### last_modified_date : `2019-03-04T17:23:42Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=21982
### status : `WAITING`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.1.0`
### severity : `enhancement`
### contents :
GCC should optimize adjacent stdio calls.  For example:

  printf("foo %d %d\n", i, j);
  printf("bar %d %d\n", x, y);

could instead be emitted as:

  printf("foo %d %d\nbar %d %d\n", i, j, x, y);

More generally, you simply concatenate the format arguments and append all of 
the remaining first printf's arguments and then all of the second printf's 
arguments.

You can also combine adjacent printf/puts and printf/putc:
printf("format", args...); puts(s); -> printf("format%s\n", args..., s);
printf("format", args...); putc(c); -> printf "format%c", args..., c);

You can also combine adjacent f* variants of these stdio calls (fprintf, fputs, 
fputc) if the supplied streams are equivalent.

One caveat, some format specifiers need special care.  E.g. position speficiers 
must be adjusted.  The %n specifier may preclude the optimization entirely.  
There might be other examples.


---


### compiler : `gcc`
### title : `GCC should transform printf("%s",foo) and printf("foo") into fputs(foo,stdout)`
### open_at : `2005-06-09T17:50:43Z`
### last_modified_date : `2019-03-03T04:15:44Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=21988
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.1.0`
### severity : `enhancement`
### contents :
GCC should optimize printf("%s",foo) and printf("foo") into fputs(foo,stdout) 
and fputs("foo",stdout) respectively.  As noted here:

http://gcc.gnu.org/ml/gcc-patches/2000-09/msg00859.html

We can capture stdout in an inline function using fixincl, perhaps adding the 
__always_inline__ attribute.  Then do the above transformation.

In at least the printf("%s", foo) case, the result fputs(foo,stdout) has the 
same number of arguments, so it might not even be a -Os problem.


---


### compiler : `gcc`
### title : `(cond ? result1 : result2) is vectorized, where equivalent if-syntax isn't (store)`
### open_at : `2005-06-10T13:21:59Z`
### last_modified_date : `2023-08-04T20:36:50Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=21998
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.1.0`
### severity : `enhancement`
### contents :
The following two procedures are functionally equivalent, but the first (more
complicated) syntax is vectorized though the second isn't.

typedef int __attribute ((aligned (16))) aint;
void test(aint * __restrict a1, int const v1, int const v2) {
	for (int i=0; i<640; ++i)
		a1[i] = (a1[i] == v1 ? v2 : a1[i]);
}
void test2(aint * __restrict a1, int const v1, int const v2) {
	for (int i=0; i<640; ++i)
		if (a1[i] == v1) a1[i] = v2;
}

vecttest.cpp:7: note: === vect_analyze_loop_form ===
vecttest.cpp:7: note: not vectorized: too many BBs in loop.
vecttest.cpp:6: note: bad loop form.
vecttest.cpp:6: note: vectorized 0 loops in function.

Using built-in specs.
Target: i686-pc-linux-gnu
Configured with: /esat/alexandria1/sderoeck/src/gcc/main/configure
--prefix=/esat/olympia/install --program-suffix=-cvs --enable-languages=c,c++ :
(reconfigured) /esat/alexandria1/sderoeck/src/gcc/main/configure
--prefix=/esat/olympia/install --program-suffix=-cvs --enable-languages=c,c++ :
(reconfigured) /esat/alexandria1/sderoeck/src/gcc/main/configure
--prefix=/esat/olympia/install --program-suffix=-cvs --enable-languages=c,c++
--no-create --no-recursion : (reconfigured)
/esat/alexandria1/sderoeck/src/gcc/main/configure --prefix=/esat/olympia/install
--program-suffix=-cvs --enable-languages=c,c++ --no-create --no-recursion
Thread model: posix
gcc version 4.1.0 20050610 (experimental)
 /esat/olympia/install/libexec/gcc/i686-pc-linux-gnu/4.1.0/cc1plus -quiet -v
-D_GNU_SOURCE vecttest.cpp -quiet -dumpbase vecttest.cpp -march=pentium4
-auxbase-strip vecttest-gcc.s -O9 -version -fverbose-asm -ftree-vectorize
-fdump-tree-vect-details -fdump-tree-vect-stats -o vecttest-gcc.s
-- cut --
GNU C++ version 4.1.0 20050610 (experimental) (i686-pc-linux-gnu)
        compiled by GNU C version 3.4.4 (Gentoo 3.4.4, ssp-3.4.4-1.0, pie-8.7.8).
GGC heuristics: --param ggc-min-expand=30 --param ggc-min-heapsize=4096
Compiler executable checksum: 3cb76b13917ca148a15d77c9a1fb678d


---


### compiler : `gcc`
### title : `Reverse loop IV order for increased efficiency`
### open_at : `2005-06-12T20:57:47Z`
### last_modified_date : `2021-03-03T18:47:42Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=22041
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.1.0`
### severity : `enhancement`
### contents :
The loop in the following code

$ cat stride.c
void foo(float *a, float *b, int n, int stride_a, int stride_b)
{
  int i;
  for (i=0; i<n; i++)
    {
      a[i*stride_a] = b[i*stride_b];
    }
}

is translated with "gcc -O3 -fdump-tree-optimized -S stride.c" into

<L0>:;
  *(float *) ivtmp.14 = *(float *) ivtmp.12;
  i = i + 1;
  ivtmp.12 = ivtmp.12 + ivtmp.18;
  ivtmp.14 = ivtmp.14 + ivtmp.17;
  if (n != i) goto <L0>; else goto <L2>;

and (on i686-pc-linux-gnu):

.L4:
        movl    (%ecx), %eax
        incl    %ebx
        addl    %edi, %ecx
        movl    %eax, (%edx)
        addl    %esi, %edx
        cmpl    %ebx, 16(%ebp)
        jne     .L4

The code

$ cat stride2.c
void foo(float *a, float *b, int n, int stride_a, int stride_b)
{
  int i;
  for (i=n; i>0; i--)
    {
      a[(n-i)*stride_a] = b[(n-i)*stride_b];
    }
}

is translated to

<L0>:;
  *(float *) ivtmp.16 = *(float *) ivtmp.14;
  i = i - 1;
  ivtmp.14 = ivtmp.14 + ivtmp.20;
  ivtmp.16 = ivtmp.16 + ivtmp.19;
  if (i != 0) goto <L0>; else goto <L2>;

and further

.L4:
        movl    (%ebx), %eax
        addl    %edi, %ebx
        movl    %eax, (%ecx)
        addl    %esi, %ecx
        decl    %edx
        jne     .L4

which saves one instruction and one load from memory.


---


### compiler : `gcc`
### title : `[4.0/4.1/4.2/4.3 Regression] bit-field copying regressed`
### open_at : `2005-06-23T05:02:43Z`
### last_modified_date : `2020-05-11T05:26:58Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=22156
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.1.0`
### severity : `minor`
### contents :
Take the following code:
struct s
{
  int i1:1;
  int i2:1;
  int i3:1;
};
void f(struct s *x, struct s *y) { *x = *y; }

In 3.4.0 (and currently with the C++ compiler too), we were able to get optimal code:
        movl    8(%esp), %eax
        movl    (%eax), %edx
        movl    4(%esp), %eax
        movl    %edx, (%eax)
        ret

But in (and after) 4.0.0 and the C compiler we get:
f:
        pushl   %esi
        pushl   %ebx
        movl    16(%esp), %eax
        movl    12(%esp), %esi
        movzbl  (%eax), %eax
        movb    %al, %dl
        movb    %al, %bl
        salb    $5, %al
        sarb    $7, %al
        movzbl  %al, %ecx
        movl    (%esi), %eax
        salb    $6, %dl
        andl    $1, %ecx
        sarb    $7, %dl
        movzbl  %dl, %edx
        salb    $7, %bl
        andl    $-7, %eax
        sall    $2, %ecx
        andl    $1, %edx
        sarb    $7, %bl
        addl    %edx, %edx
        orl     %ecx, %eax
        orl     %edx, %eax
        movzbl  %bl, %edx
        andl    $1, %edx
        andl    $-2, %eax
        orl     %edx, %eax
        movl    %eax, (%esi)
        popl    %ebx
        popl    %esi
        ret

Which is much worse


---


### compiler : `gcc`
### title : `Missed back prop`
### open_at : `2005-06-26T20:15:04Z`
### last_modified_date : `2021-12-23T08:01:23Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=22196
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.1.0`
### severity : `enhancement`
### contents :
The following two functions should be equal:
unsigned f(int i, unsigned x)
{
  unsigned y;
  if (i)
    y = 1024;
  else
    y = 1024*1024;
  return x/y ;
}

unsigned f1(int i, unsigned x)
{
  unsigned y;
  if (i)
    y = x/ 1024;
  else
    y = x/(1024*1024);
  return y ;
}


---


### compiler : `gcc`
### title : `fold does not optimize (int)ABS_EXPR<(long long)(int_var)>`
### open_at : `2005-06-27T15:04:44Z`
### last_modified_date : `2021-06-03T03:37:43Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=22199
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.1.0`
### severity : `enhancement`
### contents :
$ cat labs.c
extern long int labs (long int __x) __attribute__ ((__const__));

int main()
{
    int a,b;
    foo(&a, &b);
    if (labs(a) > b)
        return 1;
    else
        return 0;
}

is translated with

$ gcc -O3 -fdump-tree-optimized -S labs.c

into

<bb 0>:
  foo (&a, &b);
  return (int) (ABS_EXPR <(long int) a> > (long int) b);

The casts aren't necessary in this case.


---


### compiler : `gcc`
### title : `vectorization library`
### open_at : `2005-06-28T20:53:15Z`
### last_modified_date : `2022-03-08T16:20:44Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=22226
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.1.0`
### severity : `enhancement`
### contents :
GCC generic vector support should call IBM MASSV and Intel VML vector libraries.


---


### compiler : `gcc`
### title : `promotions (from float to double) are not removed when they should be able to`
### open_at : `2005-07-06T15:40:19Z`
### last_modified_date : `2023-06-03T17:57:43Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=22326
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.1.0`
### severity : `enhancement`
### contents :
Take the following code:
#include <math.h>

float foo(float f, float x, float y) {
return (fabs(f)*x+y);
}

on PPC, we should be able to produce:
        fabs f1,f1
        fmadds f1,f1,f2,f3
        blr

But right now we produce:
        fabs f1,f1
        fmadd f1,f1,f2,f3
        frsp f1,f1
        blr

This is because we don't remove promotions we should be able to remove.
If we do:
#include <math.h>

float foo(float f, float x, float y) {
return (fabs(f)*x);
}

The promotions are removed.


---


### compiler : `gcc`
### title : `Should use cmov in some stituations`
### open_at : `2005-07-20T13:46:33Z`
### last_modified_date : `2023-06-09T17:21:47Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=22568
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `unknown`
### severity : `enhancement`
### contents :
With (ulong a, ulong b) and code like
if ( a<b )  { ulong t=a; a=b; b=t; }
gcc should (if a and b are in registers already)
not emit a conditional jump but code like
MOV a, t;
CMP a, b;
CMOVcc b, a;
CMOVcc t, b;

Other such examples are easily found.  If I got it correctly, gcc
emits CMOVcc in just one situation, the conditional assignment.

Machine is AMD64, OS is SuSE Linux 9.3
gcc (GCC) 3.3.5 20050117 (prerelease) (SUSE Linux)


---


### compiler : `gcc`
### title : `extra XORs  generated on i686`
### open_at : `2005-07-27T22:00:13Z`
### last_modified_date : `2021-07-26T02:44:41Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=23102
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.1.0`
### severity : `enhancement`
### contents :
Compiling the code below (extracted from xterm-202) with
 -fno-inline -O2 -march=i686

typedef unsigned int Cardinal;
typedef unsigned long Pixel;
typedef char *String;

typedef struct {
 String resource;
 Pixel value;
 int mode;
} ColorRes;

typedef struct {
 ColorRes Acolors[(256 +4)];
 int startHRow, startHCol,
   endHRow, endHCol,
   startHCoord, endHCoord;
 Cardinal selection_count;
} TScreen;

static void
ResetSelectionState(TScreen * screen)
{
    screen->selection_count = 0;
    screen->startHRow = screen->startHCol = 0;
    screen->endHRow = screen->endHCol = 0;
}

void foo (TScreen *scr)
{
  ResetSelectionState (scr);
}

generates: 
ResetSelectionState:
        pushl   %ebp
        xorl    %edx, %edx
        movl    %esp, %ebp
        xorl    %ecx, %ecx
        popl    %ebp
        movl    %edx, 3144(%eax)
        xorl    %edx, %edx
        movl    %ecx, 3124(%eax)
        xorl    %ecx, %ecx   ;; this is not needed, ecx is already 0 
        movl    %edx, 3120(%eax)
        xorl    %edx, %edx    ;; so is edx
        movl    %ecx, 3132(%eax)  
        movl    %edx, 3128(%eax)
        ret

when using -march=i386 the code looks better:

ResetSelectionState:
        pushl   %ebp
        movl    %esp, %ebp
        movl    $0, 3144(%eax)
        movl    $0, 3124(%eax)
        movl    $0, 3120(%eax)
        movl    $0, 3132(%eax)
        movl    $0, 3128(%eax)
        leave
        ret


---


### compiler : `gcc`
### title : `builtin array operator new is not marked with malloc attribute`
### open_at : `2005-08-14T05:39:14Z`
### last_modified_date : `2023-06-09T14:37:03Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=23383
### status : `RESOLVED`
### tags : `alias, missed-optimization`
### component : `c++`
### version : `4.1.0`
### severity : `enhancement`
### contents :
Testcase:
int f(void)
{
  int t;
  int *a = new int[1024];
  int *b = new int[1024];
  *a = 1;
  *b = 2;
  t = *a;
  delete a;
  delete b;
  return t;
}

the return is not turned into 1 but still have "return t" in the final_cleanup.


---


### compiler : `gcc`
### title : `escaped set should be flow sensitive`
### open_at : `2005-08-14T06:17:14Z`
### last_modified_date : `2022-12-24T20:14:28Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=23384
### status : `NEW`
### tags : `alias, missed-optimization`
### component : `tree-optimization`
### version : `4.1.0`
### severity : `enhancement`
### contents :
Take the following code:
struct f
{
  int i;
  int j;
};
void g(void);
void i(struct f*);

int kk(void)
{
  struct f a;
  int j;
  a.i = 1;
  a.j =2 ;
  g();
  j = a.i;
  i(&a);
  return j;
}

---
j should be changed to 1 as the address of a is not escape until after the call to i so g should not get a 
call clobbered for the SFT's of a.


---


### compiler : `gcc`
### title : `a*a (for signed ints with -fno-wrapv) is always postive`
### open_at : `2005-08-18T23:50:36Z`
### last_modified_date : `2021-08-29T08:18:46Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=23471
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.1.0`
### severity : `enhancement`
### contents :
Hmm, this is both a VRP bug and a folding bug.  Even though a is VARYING, we know the that a*a will 
always be postive (this with -fno-wrapv which is default for C, C++ and fortran).
void link_error(void);
void f(int a)
{
  int b = a;
  b*=a;
  if (b < 0)
   link_error();
}

---
There should be no references to link_error().

There is another way of fixing this via the fold:
void link_error(void);
void f(int a)
{
  if (a*a < 0)
   link_error();
}

But that will miss:
void link_error(void);
void f(int a)
{
  if (a*a*a*a*a*a < 0)
   link_error();
}

---
Yes that is most likely to overflow but that is the whole point of -fno-wrapv.

Also ICC does not do this optimization at all.


---


### compiler : `gcc`
### title : `Fold does not reduce C - ~a into a + (C+1)`
### open_at : `2005-09-01T01:42:08Z`
### last_modified_date : `2023-08-05T17:15:37Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=23666
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.1.0`
### severity : `enhancement`
### contents :
The asm for the following two functions should be the same.
int f(int a)
{
  return 10 - ~a;
}
int f1(int a)
{
  return a + 11;
}


Found while reading LLVM's instruction combiner.


---


### compiler : `gcc`
### title : `Missed optimization for PIC code with internal visibility`
### open_at : `2005-09-06T20:40:48Z`
### last_modified_date : `2021-09-17T00:26:30Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=23756
### status : `NEW`
### tags : `missed-optimization, visibility`
### component : `target`
### version : `4.0.2`
### severity : `enhancement`
### contents :
This bug-report is in fact a wishlist for an optimization described in GCC
manual, yet not implemented unfortunately (at least not for x86). About the
"internal" visibility of a symbol, the manual states: "By indicating that a
symbol cannot be called from outside the module, GCC may for instance omit the
load of a PIC register since it is known that the calling function loaded the
correct value."

This is a great idea, since loading the GOT register on x86 is a costly
operation. Even with "-march=pentium3" (it prevents the return address predictor
of the processor from going into lalaland because of the load), the PIC version
of the testcase still runs twice as slow. Although g() has already loaded the
GOT address in the %ebx callee-save register, f() will load it once again in %ecx.

The optimization described for the "internal" visibility would prevent such a
reload, since GCC would have complete control over the callers. I did not see
anything in the psABI that would disallow such an optimization. Hence this
wishlist. This was tested with GCC 4.0.2 and compiled by "gcc -O -fPIC" (or -fpic).

Testcase:

        extern int a;

        __attribute__((visibility("internal")))
        void f(void) { ++a; }

        void g(void) { a = 0; f(); }


Excerpt from the generated assembly code:

080483c9 <g>:
 80483c9:       55                      push   %ebp
 80483ca:       89 e5                   mov    %esp,%ebp
 80483cc:       53                      push   %ebx
 80483cd:       e8 00 00 00 00          call   80483d2 <g+0x9>  \
 80483d2:       5b                      pop    %ebx              | first load
 80483d3:       81 c3 2e 12 00 00       add    $0x122e,%ebx     /
 80483d9:       8b 83 f8 ff ff ff       mov    0xfffffff8(%ebx),%eax
 80483df:       c7 00 00 00 00 00       movl   $0x0,(%eax)
 80483e5:       e8 c6 ff ff ff          call   80483b0 <f>
 ...
080483b0 <f>:
 80483b0:       55                      push   %ebp
 80483b1:       89 e5                   mov    %esp,%ebp
 80483b3:       e8 00 00 00 00          call   80483b8 <f+0x8>  \
 80483b8:       59                      pop    %ecx              | second load
 80483b9:       81 c1 48 12 00 00       add    $0x1248,%ecx     /
 80483bf:       8b 81 f8 ff ff ff       mov    0xfffffff8(%ecx),%eax
 80483c5:       ff 00                   incl   (%eax)
 80483c7:       5d                      pop    %ebp
 80483c8:       c3                      ret


Note: it is impossible to specify both the "internal" visibility and the
"static" qualifier (GCC complains). And using only "static" does not help here
either.

$ gcc -v
Using built-in specs.
Target: i486-linux-gnu
Configured with: ../src/configure -v
--enable-languages=c,c++,java,f95,objc,ada,treelang --prefix=/usr
--enable-shared --with-system-zlib --libexecdir=/usr/lib --enable-nls
--without-included-gettext --enable-threads=posix --program-suffix=-4.0
--enable-__cxa_atexit --enable-libstdcxx-allocator=mt --enable-clocale=gnu
--enable-libstdcxx-debug --enable-java-gc=boehm --enable-java-awt=gtk
--enable-gtk-cairo --with-java-home=/usr/lib/jvm/java-1.4.2-gcj-4.0-1.4.2.0/jre
--enable-mpfr --disable-werror --enable-checking=release i486-linux-gnu
Thread model: posix
gcc version 4.0.2 20050821 (prerelease) (Debian 4.0.1-6)


---


### compiler : `gcc`
### title : `SRA pessimizes passing structures by value at -Os (+22% code size)`
### open_at : `2005-09-08T17:08:11Z`
### last_modified_date : `2021-08-16T00:55:28Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=23782
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.0.2`
### severity : `normal`
### contents :
etienne@cygne:~/projet/gujin$ gcc -v
Using built-in specs.
Target: i486-linux-gnu
Configured with: ../src/configure -v --enable-
languages=c,c++,java,f95,objc,ada,treelang --prefix=/usr --enable-shared --
with-system-zlib --libexecdir=/usr/lib --enable-nls --without-included-
gettext --enable-threads=posix --program-suffix=-4.0 --enable-__cxa_atexit --
enable-libstdcxx-allocator=mt --enable-clocale=gnu --enable-libstdcxx-debug --
enable-java-gc=boehm --enable-java-awt=gtk --enable-gtk-cairo --with-java-
home=/usr/lib/jvm/java-1.4.2-gcj-4.0-1.4.2.0/jre --enable-mpfr --disable-
werror --enable-checking=release i486-linux-gnu
Thread model: posix
gcc version 4.0.2 20050821 (prerelease) (Debian 4.0.1-6)
etienne@cygne:~/projet/gujin$ gcc -Os -c -o tmp.o tmp.c && size tmp.o
   text    data     bss     dec     hex filename
    281       0       0     281     119 tmp.o
etienne@cygne:~/projet/gujin$ ../toolchain-3.4.4-2.16/bin/gcc -v
Reading specs from /home/etienne/projet/toolchain-3.4.4-
2.16/bin/../lib/gcc/i686-pc-linux-gnu/3.4.4/specs
Configured with: ../configure --prefix=/home/etienne/projet/toolchain --enable-
languages=c
Thread model: posix
gcc version 3.4.4
etienne@cygne:~/projet/gujin$ ../toolchain-3.4.4-2.16/bin/gcc -Os -c -o tmp.o 
tmp.c && size tmp.o
   text    data     bss     dec     hex filename
    230       0       0     230      e6 tmp.o
etienne@cygne:~/projet/gujin$ cat tmp.c
typedef struct {
    unsigned short x, y;        /* x should be the easyest to read */
    } __attribute__ ((packed)) coord;

#define FASTCALL        __attribute__ (( fastcall ))

struct user_interface_fct_str {
     void     (*setpixel) (coord xy, unsigned color) FASTCALL;
     void     (*plotHline) (coord xy, unsigned short xend, unsigned color);
     } function;

extern inline void
UI_plotHline (coord xy, unsigned short xend, unsigned color) {
  function.plotHline (xy, xend, color);
  }
extern inline void
UI_setpixel (coord xy, unsigned color) {
  function.setpixel (xy, color);
  }

extern unsigned stack_limit;

extern inline void bound_stack (void)
  {
  asm volatile (" bound %%esp,%0 " : : "m" (stack_limit) );
  }

void drawbutton (coord    upperleft, coord  lowerright,
            unsigned upperleftcolor, unsigned lowerrightrcolor,
            unsigned fillcolor, unsigned drawbackground)
  {bound_stack();{
  /* Enlarge the button by few pixels: */
  upperleft.x -= 2;
  lowerright.x += 2;
  lowerright.y -= 1; /* do not overlap two consecutive lines */

  UI_plotHline (upperleft, lowerright.x, upperleftcolor);       /* top line */
  /* do not change VESA1 banks too often, process horizontally,
     left to right, line per line */
  for (;;) {
      upperleft.y += 1;
      if (upperleft.y >= lowerright.y)
          break;
      UI_setpixel (upperleft, upperleftcolor);
      if (drawbackground)
          UI_plotHline (((coord) { .x = upperleft.x + 1, .y = upperleft.y }),
                        lowerright.x - 1, fillcolor);
      UI_setpixel (((coord) { .x = lowerright.x - 1, .y = upperleft.y }),
                        lowerrightrcolor);
      }

  UI_plotHline (upperleft, lowerright.x, lowerrightrcolor);     /* bottom line 
*/
  }}
etienne@cygne:~/projet/gujin$ 

  Doing the commands:
../toolchain-3.4.4-2.16/bin/gcc -Os -S -o tmp.a tmp.c
gcc -Os -S -o tmp.b tmp.c
diff -y tmp.a tmp.b
  does not give me a clear idea of the reason...


---


### compiler : `gcc`
### title : `missed 64-bit shift+mask optimizations on 32-bit arch`
### open_at : `2005-09-11T00:18:46Z`
### last_modified_date : `2021-07-26T19:43:33Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=23810
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.1.0`
### severity : `enhancement`
### contents :


(Sources are from CVS as of about 6AM US/Eastern time today.)

I'm testing out how well gcc optimizes some code for reversing bit
strings.  It appears that on x86 at least, double-word shifts followed
by masks that zero out all the bits that crossed the word boundary are
not optimized as well as they could be.

In the included file, compiled with "-O9 -fomit-frame-pointer",
functions rt and rt2 both result in assembly code including a
double-word shift, bringing two bits from the upper half of the
argument into the top of the lower half of the double-word value, then
masks that word with 0x33333333, which zeros out those bits:

    rt:
	    movl	8(%esp), %edx
	    movl	4(%esp), %eax
	    shrdl	$2, %edx, %eax
	    shrl	$2, %edx
	    andl	$858993459, %eax
	    andl	$858993459, %edx
	    ret

Okay, in this case, the only optimization would be to make the shift
not reference both %edx and %eax, and drop the reference to the upper
half flom the RTL during optimization.  To highlight the issue a
little more, rt4 is like rt but only returns the lower half.  Still,
the upper half is read in from memory (and shifted!) needlessly:

    rt4:
	    movl	8(%esp), %edx
	    movl	4(%esp), %eax
	    shrdl	$2, %edx, %eax
	    andl	$858993459, %eax
	    shrl	$2, %edx
	    ret

Function left shows the same problem, shifting in the opposite
direction:

    left:
	    movl	4(%esp), %eax
	    movl	8(%esp), %edx
	    shldl	$2, %eax, %edx
	    sall	$2, %eax
	    andl	$-858993460, %edx
	    andl	$-858993460, %eax
	    ret

The "andl" of %edx with 0xcccccccc will clobber the bits brought in
from %eax.

I haven't got the hang of reading ppc assembly yet, but I think the
Mac OS X compiler (10.4.2 = "gcc version 4.0.0 (Apple Computer,
Inc. build 5026)") is missing similar optimizations.  I haven't tried
the cvs code on ppc.

Environment:
System: Linux kal-el 2.4.17 #4 SMP Sun Apr 6 16:25:37 EDT 2003 i686 GNU/Linux
Architecture: i686

	
host: i686-pc-linux-gnu
build: i686-pc-linux-gnu
target: i686-pc-linux-gnu
configured with: ../src/configure --enable-maintainer-mode --prefix=/u3/raeburn/gcc/linux/Install --enable-languages=c,c++,java,objc --no-create --no-recursion : (reconfigured) ../src/configure --prefix=/u3/raeburn/gcc/linux/Install

How-To-Repeat:

typedef unsigned long long uint64_t;
typedef unsigned long uint32_t;

uint64_t rt (uint64_t n) { return (n >> 2) & 0x3333333333333333ULL; }
uint64_t rt2 (uint64_t n) { return (n & (0x3333333333333333ULL << 2)) >> 2; }
uint32_t rt4 (uint64_t n) { return (n >> 2) & 0x33333333; }
uint64_t left(uint64_t n) {
  return (n << 2) & (0xFFFFFFFFFFFFFFFFULL & ~0x3333333333333333ULL);
}


---


### compiler : `gcc`
### title : `redundant register assignments not eliminated`
### open_at : `2005-09-11T02:10:12Z`
### last_modified_date : `2021-07-26T03:45:48Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=23813
### status : `RESOLVED`
### tags : `missed-optimization, ra`
### component : `target`
### version : `unknown`
### severity : `normal`
### contents :
(CVS sources from ~6AM today US/Eastern, i.e., about 16 hours before submission)

Compiling source below with -O9 -fomit-frame-pointer, there are cases where registers are assigned 
multiple times without any labels in between; a register assigned zero, used in an inclusive-or, then 
overwritten; another register assigned zero and never used.

This 64-bit byteswap routine also exhibits the problems I submitted in 23810, 23811, 23812, but I 
think one or two of these might be separate problems from those.

typedef unsigned long long uint64_t;
typedef unsigned long uint32_t;
uint64_t bitreverse (uint64_t n) {
  /* Dr. Dobbs Journal 1983, reported in Sean Eron Anderson's "bit
     twiddling hacks" web site,
     http://graphics.stanford.edu/~seander/bithacks.html .  */
#define REV64_STEP(VAR, SHIFT, MASK) \
  VAR = (((VAR >> SHIFT) & MASK) | ((VAR << SHIFT) & (0xFFFFFFFFFFFFFFFFULL & ~MASK)))

  REV64_STEP(n,  1, 0x5555555555555555ULL); /* odd/even bits */
  REV64_STEP(n,  2, 0x3333333333333333ULL); /* bitpairs */
  REV64_STEP(n,  4, 0x0F0F0F0F0F0F0F0FULL); /* nibbles */
  REV64_STEP(n,  8, 0x00FF00FF00FF00FFULL); /* bytes */
  REV64_STEP(n, 16, 0x0000FFFF0000FFFFULL); /* halfwords */
  REV64_STEP(n, 32, 0x00000000FFFFFFFFULL); /* full words */
  return n;
}

assembly generated:

bitreverse:
        pushl   %edi
        pushl   %esi
        pushl   %ebx
        movl    16(%esp), %eax
        movl    20(%esp), %edx
        movl    %eax, %ecx
        movl    %edx, %ebx
        shrdl   $1, %ebx, %ecx
        shldl   $1, %eax, %edx
        addl    %eax, %eax
        shrl    %ebx
        andl    $-1431655766, %eax
        andl    $-1431655766, %edx
        andl    $1431655765, %ecx
        andl    $1431655765, %ebx
        orl     %eax, %ecx
        orl     %edx, %ebx
        movl    %ecx, %eax
        movl    %ebx, %edi
        movl    %ecx, %esi
        movl    %ebx, %edx
        shrdl   $2, %edi, %esi
        shldl   $2, %eax, %edx
        andl    $858993459, %esi
        shrl    $2, %edi
        andl    $-858993460, %edx
        sall    $2, %eax
        andl    $858993459, %edi
        andl    $-858993460, %eax
        orl     %edx, %edi
        orl     %eax, %esi
        movl    %edi, %ebx
        movl    %esi, %eax
        movl    %esi, %ecx
        movl    %edi, %edx
        shrdl   $4, %ebx, %ecx
        shldl   $4, %eax, %edx
        andl    $252645135, %ecx
        shrl    $4, %ebx
        andl    $-252645136, %edx
        sall    $4, %eax
        andl    $252645135, %ebx
        andl    $-252645136, %eax
        orl     %edx, %ebx
        orl     %eax, %ecx
        movl    %ebx, %edi
        movl    %ecx, %esi
        movl    %ecx, %eax
        shrdl   $8, %edi, %esi
        movl    %ebx, %edx
        shrl    $8, %edi
        andl    $16711935, %esi
        andl    $16711935, %edi
        shldl   $8, %eax, %edx
        sall    $8, %eax
        andl    $-16711936, %edx
        andl    $-16711936, %eax
        orl     %edx, %edi
        orl     %eax, %esi
            # we're about to copy this from esi to eax then clear esi;
            # wouldn't putting output in eax be better?
        movl    %edi, %ebx
        movl    %esi, %eax
        movl    %esi, %ecx
        movl    %edi, %edx
        xorl    %esi, %esi # esi set to zero
        # PRs 23810, 23811 look at this code:
        shrdl   $16, %ebx, %ecx
        shldl   $16, %eax, %edx
        andl    $65535, %ecx
        shrl    $16, %ebx
        andl    $-65536, %edx
        andl    $65535, %ebx
        sall    $16, %eax
        orl     %edx, %ebx
        andl    $-65536, %eax
        movl    %ebx, %edx
        orl     %eax, %ecx # output to ecx then move to eax, instead of just output to eax?
        movl    %ecx, %ebx # ebx only used to ior into edx, while ecx value still live
        movl    %ecx, %eax # assign eax twice??
        movl    %edx, %eax
        xorl    %edx, %edx # clear edx twice??
        xorl    %edx, %edx
        orl     %esi, %eax # esi still zero
        orl     %ebx, %edx
        movl    $0, %ecx # why? insn note shows REG_UNUSED
        popl    %ebx
        popl    %esi
        popl    %edi
        ret

A version of this swap routine that splits the 64-bit value into two 32-bit chunks, performs bit-
reversals on the chunks, and puts the two chunks back together in reverse order, comes out shorter, 
despite still showing the PR23810/23811 problems, but it does the same work as this function should.

I suspect at least some of these come from preserving DImode operations until fairly late, e.g., 
assigning a DImode to eax/edx, then shifting right 32 (eax:=edx, edx:=0), stuff like that.  I haven't 
figured out the esi and ecx bits yet though.


---


### compiler : `gcc`
### title : `loop header should also be pulled out of the inner loop too`
### open_at : `2005-09-13T09:46:45Z`
### last_modified_date : `2021-07-26T03:36:03Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=23855
### status : `RESOLVED`
### tags : `missed-optimization, patch`
### component : `tree-optimization`
### version : `4.1.0`
### severity : `enhancement`
### contents :
void bar(void);
void foo(int ie, int je)
{
  int i, j;
  for (j=0; j<je; ++j)
    for (i=0; i<ie; ++i)
      bar();
}

should _not_ be transformed to

foo (ie, je)
{ 
  int j;
  int i;
  
<bb 0>:
  if (je > 0) goto <L23>; else goto <L5>;
  
<L23>:;
  j = 0;
  goto <bb 3> (<L2>);

<L22>:;
  i = 0;

<L1>:;
  bar ();
  i = i + 1;
  if (ie != i) goto <L1>; else goto <L3>;

<L3>:;
  j = j + 1;
  if (je != j) goto <L2>; else goto <L5>;

<L2>:;
  if (ie > 0) goto <L22>; else goto <L3>;

<L5>:;
  return;

}

i.e. containing an loop-invariant check if (ie > 0).

Both DOM and copy-header do this transformation.  Disabling both
we get

;; Function foo (foo)
  
foo (ie, je)
{
  int j;
  int i;

<bb 0>:
  j = 0;
  goto <bb 4> (<L4>);

<L1>:;
  bar ();
  i = i + 1;

<L2>:;
  if (i < ie) goto <L1>; else goto <L3>;

<L3>:;
  j = j + 1;

<L4>:;
  if (j < je) goto <L8>; else goto <L5>;

<L8>:;
  i = 0;
  goto <bb 2> (<L2>);

<L5>:;
  return;

}

which is a _lot_ faster for small ie.  Optimally we would hoist the
loop invariant check out of the j loop.


---


### compiler : `gcc`
### title : `loop-invariant-motion is not doing it's work`
### open_at : `2005-09-19T18:52:12Z`
### last_modified_date : `2023-09-01T09:17:52Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=23970
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.1.0`
### severity : `enhancement`
### contents :
void Ekin(double *e, int *stridee,
          double *vx, int *stridevx,
          double *vy, int *stridevy,
          double *vz, int *stridevz,
          int *sz)
{
  int i1 = sz[0];
  int j1 = sz[1];
  int k1 = sz[2];
  int i, j, k;
  for (k=0; k<k1; ++k)
   for (j=0; j<j1; ++j)
    for (i=0; i<i1; ++i)
     {
       e[i + j * stridee[1] + k * stridee[2]]
        = 0.128 * (
            ((vx[i + j * stridevx[1] + k * stridevx[2]]
              + vx[i+1 + j * stridevx[1] + k * stridevx[2]])
             * (vx[i + j * stridevx[1] + k * stridevx[2]]
                + vx[i+1 + j * stridevx[1] + k * stridevx[2]]))
          + ((vy[i + j * stridevy[1] + k * stridevy[2]]
              + vy[i + (j+1) * stridevy[1] + k * stridevy[2]])
             * (vy[i + j * stridevy[1] + k * stridevy[2]]
                + vy[i + (j+1) * stridevy[1] + k * stridevy[2]]))
          + ((vz[i + j * stridevz[1] + k * stridevz[2]]
              + vz[i + j * stridevz[1] + (k+1) * stridevz[2]])
             * (vz[i + j * stridevz[1] + k * stridevz[2]]
                + vz[i + j * stridevz[1] + (k+1) * stridevz[2]])));

     }
}

lim moves all the j*stridev?[1] and k*stridev?[2] to the j-loop but
does not move the k*stridev?[2] to the k-loop.  This results in the
following asm.

Ekin:
        pushl   %ebp
        movl    %esp, %ebp
        pushl   %edi
        pushl   %esi
        pushl   %ebx
        subl    $44, %esp
        movl    40(%ebp), %eax
        movl    $0, -24(%ebp)
        movl    (%eax), %edx
        movl    4(%eax), %ecx
        movl    8(%eax), %eax
        movl    %edx, -40(%ebp)
        movl    %ecx, -36(%ebp)
        testl   %eax, %eax
        movl    %eax, -32(%ebp)
        jle     .L13
.L4:
        movl    -24(%ebp), %edx
        movl    -36(%ebp), %eax
        incl    %edx
        testl   %eax, %eax
        movl    %edx, -48(%ebp)
        jle     .L7
        movl    -40(%ebp), %ecx
        movl    $0, -16(%ebp)
        testl   %ecx, %ecx
        jle     .L17
.L10:
        movl    28(%ebp), %eax
        movl    -24(%ebp), %ebx
        movl    -16(%ebp), %edi
        movl    $0, -56(%ebp)
        fldl    .LC0
        movl    8(%eax), %edx
        movl    4(%eax), %ecx
        incl    %edi
        movl    %edi, -28(%ebp)
        movl    -16(%ebp), %edi
        imull   %edx, %ebx
        movl    36(%ebp), %edx
        movl    4(%edx), %eax
        movl    8(%edx), %esi
        movl    12(%ebp), %edx
        imull   %eax, %edi
        movl    -16(%ebp), %eax
        movl    %edi, -44(%ebp)
        movl    4(%edx), %edi
        movl    -24(%ebp), %edx
        imull   %edi, %eax
        movl    12(%ebp), %edi
        imull   8(%edi), %edx
        addl    %edx, %eax
        movl    -16(%ebp), %edx
        sall    $3, %eax
        movl    %eax, -20(%ebp)
        movl    20(%ebp), %eax
        movl    4(%eax), %edi
        movl    -24(%ebp), %eax
        imull   %edi, %edx
        movl    20(%ebp), %edi
        imull   8(%edi), %eax
        addl    %eax, %edx
        movl    -16(%ebp), %eax
        imull   %ecx, %eax
        addl    %ebx, %eax
        leal    0(,%eax,8), %edi
        movl    -28(%ebp), %eax
        imull   %eax, %ecx
        movl    -24(%ebp), %eax
        addl    %ecx, %ebx
        movl    -44(%ebp), %ecx
        imull   %esi, %eax
        sall    $3, %ebx
        addl    %ecx, %eax
        movl    -48(%ebp), %ecx
        sall    $3, %eax
        movl    %eax, -52(%ebp)
        imull   %ecx, %esi
        movl    -44(%ebp), %ecx
        addl    %esi, %ecx
        leal    0(,%ecx,8), %esi
        .p2align 4,,15
.L5:
        movl    16(%ebp), %eax
        movl    24(%ebp), %ecx
        incl    -56(%ebp)
        fldl    (%eax,%edx,8)
        faddl   8(%eax,%edx,8)
        incl    %edx
        movl    -52(%ebp), %eax
        addl    $8, -52(%ebp)
        fldl    (%edi,%ecx)
        addl    $8, %edi
        faddl   (%ecx,%ebx)
        addl    $8, %ebx
        movl    32(%ebp), %ecx
        fldl    (%eax,%ecx)
        faddl   (%ecx,%esi)
        fxch    %st(2)
        addl    $8, %esi
        movl    -20(%ebp), %eax
        movl    8(%ebp), %ecx
        fmul    %st(0), %st
        fxch    %st(1)
        fmul    %st(0), %st
        faddp   %st, %st(1)
        fxch    %st(1)
        fmul    %st(0), %st
        faddp   %st, %st(1)
        fmul    %st(1), %st
        fstpl   (%eax,%ecx)
        addl    $8, %eax
        movl    %eax, -20(%ebp)
        movl    -56(%ebp), %eax
        cmpl    %eax, -40(%ebp)
        jne     .L5
        fstp    %st(0)
        movl    -28(%ebp), %edx
        cmpl    %edx, -36(%ebp)
        jle     .L7
.L18:
        movl    -40(%ebp), %ecx
        movl    %edx, -16(%ebp)
        testl   %ecx, %ecx
        jg      .L10
.L17:
        movl    -16(%ebp), %ecx
        incl    %ecx
        movl    %ecx, -28(%ebp)
        movl    -28(%ebp), %edx
        cmpl    %edx, -36(%ebp)
        jg      .L18
.L7:
        movl    -48(%ebp), %eax
        cmpl    %eax, -32(%ebp)
        movl    %eax, -24(%ebp)
        jne     .L4
.L13:
        addl    $44, %esp
        popl    %ebx
        popl    %esi
        popl    %edi
        popl    %ebp
        ret


---


### compiler : `gcc`
### title : `VRP does not work with floating points`
### open_at : `2005-09-22T20:59:19Z`
### last_modified_date : `2022-11-28T22:15:45Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=24021
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.1.0`
### severity : `enhancement`
### contents :
Take the following example:
double BG_SplineLength ()
{
  double lastPoint;
  double i;

  for (i = 0.01;i<=1;i+=0.1f)
    if (!(i != 0.0))
      {
	lastPoint = i;
      }
    else
      {
        lastPoint = 2;
      }
  return lastPoint;
}

The loop is useless and we should remove the loop and make the function just return 2.0;


---


### compiler : `gcc`
### title : `(vector float){a, b, 0, 0} code gen is not good`
### open_at : `2005-09-27T04:06:02Z`
### last_modified_date : `2021-08-21T21:28:49Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=24073
### status : `RESOLVED`
### tags : `missed-optimization, ssemmx`
### component : `target`
### version : `4.1.0`
### severity : `enhancement`
### contents :
Take the following example:
#define vector __attribute__((vector_size(16)))

float a; float b;
vector float f(void) { return (vector float){ a, b, 0.0, 0.0}; }
---
Currently we get:
        subl    $12, %esp
        movss   _b, %xmm0
        movss   _a, %xmm1
        unpcklps        %xmm0, %xmm1
        movaps  %xmm1, %xmm0
        xorl    %eax, %eax
        xorl    %edx, %edx
        movl    %eax, (%esp)
        movl    %edx, 4(%esp)
        xorps   %xmm1, %xmm1
        movlhps %xmm1, %xmm0
        addl    $12, %esp

------
We should be able to produce:
movss _b, %xmm0
movss _a, %xmm1
shufps 60, /*[0, 3, 3, 0]*/, %xmm1, %xmm0 // _a, 0, 0, _b
shufps 201, /*[3, 0, 2, 1]*/, %xmm0, %xmm0 // _a, _b, 0, 0

This is from Nathan Begeman.


---


### compiler : `gcc`
### title : `(vector float){0, 0, b, a} code gen as not good as it should be`
### open_at : `2005-09-27T04:22:05Z`
### last_modified_date : `2021-08-22T02:18:58Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=24074
### status : `NEW`
### tags : `missed-optimization, ssemmx`
### component : `target`
### version : `4.1.0`
### severity : `enhancement`
### contents :
Take the following code:
#define vector __attribute__((vector_size(16)))

float a; float b;
vector float fb(void) { return (vector float){ 0,0,b,a};}
--------
Currently we produce:
        movss   _a, %xmm1
        movss   _b, %xmm0
        unpcklps        %xmm1, %xmm0
        movaps  %xmm0, %xmm1
        xorps   %xmm0, %xmm0
        movlhps %xmm1, %xmm0
        ret
-----

But from what I hear the xorps and movlhps are useless instructions because those bits are already 
zero.


---


### compiler : `gcc`
### title : `sibling call with -O2 copies parameters twice`
### open_at : `2005-10-01T00:40:44Z`
### last_modified_date : `2021-08-02T21:12:26Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=24156
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `3.4.4`
### severity : `enhancement`
### contents :
When compiling with -O2, a sibling call will sometimes copy all the arguments
twice: first into temporaries at the beginning of the function, then back to
their original places before the call.

Here's a test case that demonstrates it:

extern void f2(), f3();
void f(int a,int b,int c,int d,int e,int ff,int g,int h,int i,int j) {
  f2();
  f3(a,b,c,d,e,ff,g,h,i,j);
}

(the problem only shows up if there's other stuff in the function besides the
sibling call)


---


### compiler : `gcc`
### title : `Potential problems with HOT_TEXT_SECTION_NAME`
### open_at : `2005-10-04T21:45:31Z`
### last_modified_date : `2021-09-12T21:01:29Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=24201
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.0.3`
### severity : `minor`
### contents :
We have

#define HOT_TEXT_SECTION_NAME ".text.hot"
#define UNLIKELY_EXECUTED_TEXT_SECTION_NAME ".text.unlikely"

There is a little potential for confusion, for example suppose we have a very
hot function with the unlikely name of "unlikely" or a very cold function
called "hot". With -ffunction-sections, we got

[hjl@gnu-13 hot]$ cat x.c
void hot () { }

void unlikely () { }
[hjl@gnu-13 hot]$ gcc -c x.c -ffunction-sections
[hjl@gnu-13 hot]$ readelf --wide -S x.o | grep text
  [ 1] .text             PROGBITS        0000000000000000 000040 000000 00  AX  0   0  4
  [ 4] .text.hot         PROGBITS        0000000000000000 000040 000006 00  AX  0   0  1
  [ 5] .text.unlikely    PROGBITS        0000000000000000 000046 000006 00  AX  0   0  1

Should we use a slightly different standard naming scheme so as to distinguish
the special names such as huge, hot and unlikely from the function naming
cheme?


---


### compiler : `gcc`
### title : `missed div optimizations`
### open_at : `2005-10-12T15:39:08Z`
### last_modified_date : `2021-09-02T00:24:32Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=24333
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.1.0`
### severity : `enhancement`
### contents :
unsigned foo(const unsigned x) {  return (x / x); }
double bar(const double x) { return (x / x); }

$ gcc -Wall -O2 -mregparm=3 -fomit-frame-pointer tmp.c -S

foo:    xorl    %edx, %edx
        divl    %eax
        ret

bar:    fldl    4(%esp)
        fdiv    %st(0), %st
        ret

I think optimizer should return 1 for both cases.


---


### compiler : `gcc`
### title : `[11/12/13/14 Regression] get_varargs_alias_set returns 0 always`
### open_at : `2005-10-18T19:56:03Z`
### last_modified_date : `2023-07-07T10:28:40Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=24434
### status : `NEW`
### tags : `alias, FIXME, missed-optimization`
### component : `middle-end`
### version : `4.1.0`
### severity : `minor`
### contents :
With the following change:
2004-06-08  Jason Merrill  <jason@redhat.com>

        Gimplify VA_ARG_EXPR into simpler forms.

get_varargs_alias_set will always return 0, which causes us to miss some loads/store elimination and such at the rtl level (and tree level also).

The comment in alias.c is:
  /* We now lower VA_ARG_EXPR, and there's currently no way to attach the
     varargs alias set to an INDIRECT_REF (FIXME!), so we can't
     consistently use the varargs alias set for loads from the varargs
     area.  So don't use it anywhere.  */


---


### compiler : `gcc`
### title : `[meta-bug] Missed optimization: trivialization of silly code`
### open_at : `2005-10-28T16:15:30Z`
### last_modified_date : `2021-07-27T02:41:39Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=24568
### status : `RESOLVED`
### tags : `meta-bug, missed-optimization`
### component : `tree-optimization`
### version : `4.1.0`
### severity : `enhancement`
### contents :
xgcc (GCC) 4.1.0 20051020 (experimental)
can't optimize the following code (from <http://thedailywtf.com>):

int convertToMinutes(long milliDiff)
{
  int negative = 0;
  int minutesDiff = -1;

  if (milliDiff < 0)
  {
    negative = 1;
    milliDiff = -milliDiff; // Make positive (is easier)
  }

  if (milliDiff == 0) // Watch out for exceptional value 0
    minutesDiff = 0;
  else
    minutesDiff = (int) (milliDiff / 1000) / 60;

  if (negative) minutesDiff = -minutesDiff; // Make it negative again

  return minutesDiff;
}

The code should simplify to
int convertToMinutes (long i)
{
   return i / 60000;
}

But the final tree dump contains the complete logic even in the case of high optimization levels.

An interesting peculiarity from the assembly:
        .file   "milli.c"
        .text
        .p2align 4,,15
.globl convertToMinutes
        .type   convertToMinutes, @function
convertToMinutes:
        pushl   %ebp
        movl    %esp, %ebp
        subl    $8, %esp
        movl    %esi, 4(%esp)
        movl    8(%ebp), %esi
        movl    %ebx, (%esp)
        xorl    %ebx, %ebx
        testl   %esi, %esi
        js      .L12          ;;;;; jump from here
.L4:
        xorl    %ecx, %ecx
        testl   %esi, %esi
        je      .L7
        movl    $1172812403, %eax
        imull   %esi
        movl    %esi, %eax
        sarl    $31, %eax
        movl    %edx, %ecx
        sarl    $14, %ecx
        subl    %eax, %ecx
.L7:
        testl   %ebx, %ebx
        je      .L8
        negl    %ecx
.L8:
        movl    (%esp), %ebx
        movl    %ecx, %eax
        movl    4(%esp), %esi
        movl    %ebp, %esp
        popl    %ebp
        ret
        .p2align 4,,7
.L12:    ;;;;;;;;;;; all the way down here, probably out of the prefetch buffer
        negl    %esi
        movl    $1, %ebx
        jmp     .L4
        .size   convertToMinutes, .-convertToMinutes
        .ident  "GCC: (GNU) 4.1.0 20051020 (experimental)"
        .section        .note.GNU-stack,"",@progbits


---


### compiler : `gcc`
### title : `two copies of a constant in two different registers`
### open_at : `2005-11-03T01:15:13Z`
### last_modified_date : `2019-03-06T08:43:27Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=24647
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.1.0`
### severity : `normal`
### contents :
Take the following code:
int f(void)
{
  static int i;
  int i1;
  i1 = i;
  if (i1 == 0)
    i = i1 = 2;
  return i1;
}
----
Currently we generate:
f:
    movl i.1285, %eax
    pushl   %ebp
    movl %esp, %ebp
    testl   %eax, %eax
    jne .L7
    movl $2, %ecx
    movl $2, %eax
    movl %ecx, i.1285
.L7:
    popl %ebp
    ret


Why is 2 in two different registers (I think the issue here is really a target issue)?  But should postreload CSE detect this or postreload GCSE?


---


### compiler : `gcc`
### title : `missing optimization in comparison of results of bit operations`
### open_at : `2005-11-06T17:06:19Z`
### last_modified_date : `2021-07-26T19:29:17Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=24696
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.0.2`
### severity : `enhancement`
### contents :
Take this little program:

int
f (unsigned long a, unsigned long b, unsigned long c)
{
  return (a & (c - 1)) != 0 || (b & (c - 1)) != 0;
}

Compiled on x86-64 with gcc 4.0.2 (but I think also with the current mainline) yields with -O2 the following code:

0000000000000000 <f>:
   0:   48 ff ca                dec    %rdx
   3:   48 85 d7                test   %rdx,%rdi
   6:   75 07                   jne    f <f+0xf>
   8:   31 c0                   xor    %eax,%eax
   a:   48 85 d6                test   %rdx,%rsi
   d:   74 05                   je     14 <f+0x14>
   f:   b8 01 00 00 00          mov    $0x1,%eax
  14:   f3 c3                   repz retq

As can be seen, both comparisons are executed individually.  This is unnecessarily slow.  Since the right operand for & is the same and this is a pure bit-test it is perfectly fine to compile the code to the equivalent of

int
f (unsigned long a, unsigned long b, unsigned long c)
{
  return ((a | b) & (c - 1)) != 0;
}

This would be significantly faster.  On archs like x86-64 no conditional jump (just a setne) would be needed.


---


### compiler : `gcc`
### title : `Missing warning on questionable use of parameter to initialize static`
### open_at : `2005-11-11T06:28:13Z`
### last_modified_date : `2020-05-20T21:59:10Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=24786
### status : `RESOLVED`
### tags : `diagnostic, missed-optimization`
### component : `middle-end`
### version : `6.0`
### severity : `enhancement`
### contents :
gcc only warns on blah1 on the following code:

const char *blah1() {
   char x = 7;
   return &x;
}

const char *blah2() {
   char x = 7;
   static const char *names[1] = { &x }; 
   return names[0];
}

returnlocal.cc: In function 'const char* blah1()':
returnlocal.cc:2: warning: address of local variable 'x' returned

Shouldn't it warn on blah2 as well?
Or is that asking too much?


---


### compiler : `gcc`
### title : `loop unrolling ends up with too much reg+index addressing`
### open_at : `2005-11-11T21:01:49Z`
### last_modified_date : `2021-12-19T00:38:31Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=24815
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.1.0`
### severity : `normal`
### contents :
 


---


### compiler : `gcc`
### title : `static const objects should go to .rodata`
### open_at : `2005-11-18T00:32:02Z`
### last_modified_date : `2023-08-22T04:53:58Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=24928
### status : `NEW`
### tags : `missed-optimization`
### component : `c++`
### version : `4.0.2`
### severity : `enhancement`
### contents :
If a class has a trivial constructor that can be completely inlined and consists of simply initializing member variables, then static const instances of this class can be initialized at compile time and placed into .rodata. This would be the same behaviour that C has for static const structs and arrays. Example:

struct A {
public:
    inline A (int v) : m_v (v) {}
private:
    int m_v;
};

int main (void)
{
    static const A s_v (42);
    return (0);
}

Compiles to (with -fno-threadsafe-statics):

.globl main
        .type   main, @function
main:
.LFB5:
        cmpb    $0, _ZGVZ4mainE3s_v
        jne     .L2
        movl    $42, _ZZ4mainE3s_v
        movb    $1, _ZGVZ4mainE3s_v
.L2:
        xorl    %eax, %eax
        ret

With the object being initialized at runtime as if it mattered. Because the values of the member variables can not be changed after initialization, there is no reason to do this at runtime. Because the constructor doesn't do anything, this would not conflict with C++'s create-on-call mandate.

Because of this behaviour there is no way to create compiled-in const objects just like creating const structs or arrays in C.


---


### compiler : `gcc`
### title : `long long shift/mask operations should be better optimized`
### open_at : `2005-11-18T02:30:07Z`
### last_modified_date : `2021-08-29T22:39:06Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=24929
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.1.0`
### severity : `enhancement`
### contents :
shift/mask operations on long long like (x << 8) | ((y >> 48) & 0xffull) could be further optimized for x86. Please see comments in the attached test case (posted earlier in PR 17886).


---


### compiler : `gcc`
### title : `(short)(((int)short_var) <<1) should be folded so that the shift is done in the short type`
### open_at : `2005-11-30T18:20:59Z`
### last_modified_date : `2023-04-22T08:06:50Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=25186
### status : `RESOLVED`
### tags : `easyhack, missed-optimization, TREE`
### component : `middle-end`
### version : `4.2.0`
### severity : `enhancement`
### contents :
Take the following example:
short *a;

int f(void)
{
  *a  = (short)(((int)*a) << 1);
}

the Shift should be done in the same type as *a.
This is done in simplify_subreg on the RTL level but we really should be able to do it in fold also.


---
