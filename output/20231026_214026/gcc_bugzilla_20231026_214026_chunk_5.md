### Total Bugs Detected: 4649
### Current Chunk: 5 of 30
### Bugs in this Chunk: 160 (From bug 641 to 800)
---


### compiler : `gcc`
### title : `Fails to do partial basic-block SLP`
### open_at : `2011-08-03T09:08:00Z`
### last_modified_date : `2023-08-08T12:38:59Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=49955
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.7.0`
### severity : `enhancement`
### contents :
410.bwaves in shell_lam.f has a lot of arrays with inner dimension 5 operated
on in loops that are either unrolled by early unrolling or manually unrolled
in source.  All but one loop in shell_lam.f are not vectorized.

One reason is that basic-block vectorization gives up if it sees
interleaving size that is not a multiple of a supported vectorization
factor.  Testcase:

double a[1024], b[1024];

void foo (int k)
{
  int j;
  a[k*5 + 0] = a[k*5 + 0] + b[k*5 + 0];
  a[k*5 + 1] = a[k*5 + 1] + b[k*5 + 1];
  a[k*5 + 2] = a[k*5 + 2] + b[k*5 + 2];
  a[k*5 + 3] = a[k*5 + 3] + b[k*5 + 3];
  a[k*5 + 4] = a[k*5 + 4] + b[k*5 + 4];
}

taken from the last loop in shell_lam.f which has its innermost loop unrolled
(and loop SLP refuses to vectorize as well, see separate bug).

For the above we get:

t.c:6: note: === vect_analyze_data_ref_accesses ===
t.c:6: note: Detected interleaving of size 5
t.c:6: note: Detected interleaving of size 5
t.c:6: note: Detected interleaving of size 5
t.c:6: note: Vectorizing an unaligned access.
t.c:6: note: Vectorizing an unaligned access.
t.c:6: note: Vectorizing an unaligned access.
t.c:6: note: === vect_analyze_slp ===
t.c:6: note: get vectype with 2 units of type double
t.c:6: note: vectype: vector(2) double
t.c:6: note: Build SLP failed: unrolling required in basic block SLP
t.c:6: note: Failed to SLP the basic block.
t.c:6: note: not vectorized: failed to find SLP opportunities in basic block.

but of course we could simply vectorize with an interleaving size of 4
leaving the excess operations unvectorized (with optimization opportunity
if we can pick a properly sized and aligned set of accesses).


---


### compiler : `gcc`
### title : `ABS pattern is not recognized`
### open_at : `2011-08-03T12:25:32Z`
### last_modified_date : `2023-05-08T07:41:53Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=49959
### status : `RESOLVED`
### tags : `missed-optimization, patch`
### component : `tree-optimization`
### version : `4.7.0`
### severity : `enhancement`
### contents :
Created attachment 24900
Simple test where ABS pattern is not recognized

Here is optimization opportunity for ABS pattern recognizer which does not catch all cases.

Here is a simple test for ABS computation:

#define ABS(X)    (((X)>0)?(X):-(X))
int
test_abs(int *cur)
{
  unsigned long sad = 0;
  sad = ABS(cur[0]);
  return sad;
}

GIMPLE for the test is good (phase optimized):

test_abs (int * cur)
{
  int D.2783;
  int D.2782;

<bb 2>:
  D.2782_3 = *cur_2(D);
  D.2783_4 = ABS_EXPR <D.2782_3>;
  return D.2783_4;
}

Now try to make a minor change in test:
#define ABS(X)    (((X)>0)?(X):-(X))
int
test_abs(int *cur)
{
  unsigned long sad = 0;
  sad += ABS(cur[0]);
  return sad;
}

GIMPLE becomes worse:

test_abs (int * cur)
{
  int D.2788;
  int D.2787;
  int D.2783;
  long unsigned int iftmp.0;

<bb 2>:
  D.2783_4 = *cur_3(D);
  if (D.2783_4 > 0)
    goto <bb 3>;
  else
    goto <bb 4>;

<bb 3>:
  iftmp.0_6 = (long unsigned int) D.2783_4;
  goto <bb 5>;

<bb 4>:
  D.2787_8 = -D.2783_4;
  iftmp.0_9 = (long unsigned int) D.2787_8;

<bb 5>:
  # iftmp.0_1 = PHI <iftmp.0_6(3), iftmp.0_9(4)>
  D.2788_11 = (int) iftmp.0_1;
  return D.2788_11;
}

Compiler used for tests:

Target: x86_64-unknown-linux-gnu
Configured with: ../gcc/configure --prefix=/export/gcc-build --enable-languages=c,c++,fortran
Thread model: posix
gcc version 4.7.0 20110707 (experimental) (GCC)
COLLECT_GCC_OPTIONS='-v' '-save-temps' '-O2' '-S' '-mtune=generic' '-march=x86-64'


---


### compiler : `gcc`
### title : `not vectorized: data ref analysis failed`
### open_at : `2011-08-03T17:23:03Z`
### last_modified_date : `2021-08-15T00:51:30Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=49969
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.7.0`
### severity : `normal`
### contents :
The following program does not vectorize. With Intel's ifort one gets the
message:

  PERMUTED LOOP WAS VECTORIZED

while GCC just prints:

test.f90:6: note: not vectorized: data ref analysis failed D.1566_33 = *iz_32(D)[D.1565_31];

test.f90:7: note: not vectorized: data ref analysis failed D.1566_33 = *iz_32(D)[D.1565_31];

test.f90:2: note: vectorized 0 loops in function.


In case of GCC, it does not depend on the loop order - permuting does not change anything. Also it is independent of the patch to PR 49957.


! From Polyhedron's ac.f90, line 746
      SUBROUTINE SUSCEP(L,Iz,Dsus)
      INTEGER L , Iz(L,L) , iznum
      DOUBLE PRECISION Dsus
      iznum = 0
      DO iy = 1 , L
        DO ix = 1 , L
          iznum = iznum + Iz(iy,ix)
        ENDDO
      ENDDO
      Dsus = DBLE(iznum)
      Dsus = Dsus*Dsus
      Dsus = Dsus/(L*L)
      END


---


### compiler : `gcc`
### title : `Unroll factor exceeds max trip count`
### open_at : `2011-08-10T14:43:58Z`
### last_modified_date : `2021-12-18T23:15:01Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=50037
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.7.0`
### severity : `normal`
### contents :
Created attachment 24971
Reproducer

Here is a small loop on which GCC performs inefficient unroll:

for ( count = ((*(hdrptr)) & 0xf) * 2; count > 0; count--, addr++ )
    sum += *addr;

This loop has maximum 30 iterations. If we use -O3 then this loop is vectorized. Resulting loop has maximum 30 / 8 = 3 iteration. Also vectorizer generates prologue and epilogue loops. Each of them has maximum 7 iterations.

If we add -funroll-loops option then each of 3 generated by vectorizer loops is unrolled with unroll factor 8. It creates a lot of code which is never executed and also decreases performance due to additional checks and branches.

Target: x86_64-unknown-linux-gnu
Configured with: ../gcc1/configure --prefix=/export/gcc-perf/install --enable-languages=c,c++,fortran
Thread model: posix
gcc version 4.7.0 20110615 (experimental) (GCC)
COLLECT_GCC_OPTIONS='-O3' '-funroll-loops' '-S' '-v' '-mtune=generic' '-march=x86-64'
 /export/gcc-perf/install/libexec/gcc/x86_64-unknown-linux-gnu/4.7.0/cc1 -quiet -v unroll_test.c -quiet -dumpbase unroll_test.c -mtune=generic -march=x86-64 -auxbase unroll_test -O3 -version -funroll-loops -o unroll_test.s
GNU C (GCC) version 4.7.0 20110615 (experimental) (x86_64-unknown-linux-gnu)
        compiled by GNU C version 4.4.3, GMP version 4.3.1, MPFR version 2.4.2, MPC version 0.8.1
GGC heuristics: --param ggc-min-expand=30 --param ggc-min-heapsize=4096


---


### compiler : `gcc`
### title : `[C++0x] Weird optimization anomaly with constexpr`
### open_at : `2011-08-15T12:48:17Z`
### last_modified_date : `2021-07-23T11:57:08Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=50087
### status : `NEW`
### tags : `missed-optimization`
### component : `c++`
### version : `4.6.1`
### severity : `normal`
### contents :
Created attachment 25014
runs_too_long runs in a very short period of time

I have two nearly identical programs. In one (small.joe.cpp), a function called 'runs_too_long' does not run too long. It is compiled down to returning a constant value.

In another, very slightly different program (small-nojoe.cpp), the function 'runs_too_long' does indeed run too long. It, in fact will not complete in any reasonable length of time.


---


### compiler : `gcc`
### title : `movzbl is generated instead of movl`
### open_at : `2011-08-15T13:02:30Z`
### last_modified_date : `2021-08-27T12:24:46Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=50088
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.7.0`
### severity : `normal`
### contents :
Created attachment 25016
Reproducer

When spilled register is going to be used in subreg expression then short load is generated to fill register.

Example:
    movl  %edx, 0x34(%esp)
    jz 0x1498 <Block 54>
  Block 34:
    movzxb  0x34(%esp), %ecx
    shl %cl, %eax

It is correct but may cause performance problems. I doubt there are situations when zero extended load is better than natural one.

On Atom processors (and probably some others) such situations cause stalls because store forwarding does not work for store/load pair using different access sizes.

For example EEMBC 2.0/huffde has ~6% performance improvement on Atom if we replace such movzbl with movl.

Attached reproducer demonstrates fills performed via movzbl.
Used compiler and options:

Target: x86_64-unknown-linux-gnu
Configured with: ../gcc1/configure --prefix=/export/users/gcc-perf/install --enable-languages=c,c++,fortran
Thread model: posix
gcc version 4.7.0 20110615 (experimental) (GCC)
COLLECT_GCC_OPTIONS='-O2' '-m32' '-S' '-v' '-mtune=generic' '-march=x86-64'
 /export/users/gcc-perf/install/libexec/gcc/x86_64-unknown-linux-gnu/4.7.0/cc1 -quiet -v -imultilib 32 test_movzbl.c -quiet -dumpbase test_movzbl.c -m32 -mtune=generic -march=x86-64 -auxbase test_movzbl -O2 -version -o test_movzbl.s
GNU C (GCC) version 4.7.0 20110615 (experimental) (x86_64-unknown-linux-gnu)
        compiled by GNU C version 4.4.3, GMP version 4.3.1, MPFR version 2.4.2, MPC version 0.8.1
GGC heuristics: --param ggc-min-expand=30 --param ggc-min-heapsize=4096


---


### compiler : `gcc`
### title : `[IRA, i386] allocates registers in very non-optimal way`
### open_at : `2011-08-17T13:41:32Z`
### last_modified_date : `2021-12-26T22:18:55Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=50107
### status : `RESOLVED`
### tags : `missed-optimization, ra`
### component : `rtl-optimization`
### version : `4.7.0`
### severity : `normal`
### contents :
Created attachment 25032
Patch, enabling MULX insn

Hi,
I am working on enabling of new MULX instruction for GCC.
It have to relax generic unsigned mult in two ways: no falgs are clobbered, and (the main) destination may be arbitrary 2 GPR's.

Patch is attached along with testcase.

Problem is that such relaxation leads to useless spills/fills.
Command line is:
./build-x86_64-linux/gcc/xgcc -B./build-x86_64-linux/gcc test.c -S -Ofast
Here is assembly with MULX:
test_mul_64:
.LFB0:
        movq    %rdi, %rdx
        pushq   %rbx              <--------
        mulx    %rsi, %rbx, %rcx
        addq    $3, %rcx
        adcq    $0, %rbx
        movq    %rcx, %rax
        movq    %rcx, k2(%rip)
        movq    %rbx, %rdx        <--------
        movq    %rbx, k2+8(%rip)
        popq    %rbx              <--------
        ret

You can see, that if we replace ebx usage with edx, instruction marked with arrows will dissapear. 

Maybe the problem is connected with my definition of MULX?
But it seems to me as IRA misoptimization.

BTW, r8, r9 etc. regs are caller-safe, so we may just use them without saving to stack? Why IRA doesn't do that?

Thanks, K


---


### compiler : `gcc`
### title : `Optimize x = -1 with "or" for -O`
### open_at : `2011-08-19T20:22:54Z`
### last_modified_date : `2021-12-15T01:34:39Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=50131
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.7.0`
### severity : `normal`
### contents :
[hjl@gnu-6 rtm-1]$ cat x.c
int
foo1 ()
{
  return -1;
}

short
foo2 ()
{
  return -1;
}

long long
foo3 ()
{
  return -1;
}
[hjl@gnu-6 rtm-1]$ gcc -S -Os x.c 
[hjl@gnu-6 rtm-1]$ cat x.s
	.file	"x.c"
	.text
	.globl	foo1
	.type	foo1, @function
foo1:
.LFB0:
	.cfi_startproc
	orl	$-1, %eax
	ret
	.cfi_endproc
.LFE0:
	.size	foo1, .-foo1
	.globl	foo2
	.type	foo2, @function
foo2:
.LFB1:
	.cfi_startproc
	orl	$-1, %eax
	ret
	.cfi_endproc
.LFE1:
	.size	foo2, .-foo2
	.globl	foo3
	.type	foo3, @function
foo3:
.LFB2:
	.cfi_startproc
	orq	$-1, %rax
	ret
	.cfi_endproc
.LFE2:
	.size	foo3, .-foo3
	.ident	"GCC: (GNU) 4.6.0 20110603 (Red Hat 4.6.0-10)"
	.section	.note.GNU-stack,"",@progbits
[hjl@gnu-6 rtm-1]$ gcc -S -O2 x.c 
[hjl@gnu-6 rtm-1]$ cat x.s
	.file	"x.c"
	.text
	.p2align 4,,15
	.globl	foo1
	.type	foo1, @function
foo1:
.LFB0:
	.cfi_startproc
	movl	$-1, %eax
	ret
	.cfi_endproc
.LFE0:
	.size	foo1, .-foo1
	.p2align 4,,15
	.globl	foo2
	.type	foo2, @function
foo2:
.LFB1:
	.cfi_startproc
	movl	$-1, %eax
	ret
	.cfi_endproc
.LFE1:
	.size	foo2, .-foo2
	.p2align 4,,15
	.globl	foo3
	.type	foo3, @function
foo3:
.LFB2:
	.cfi_startproc
	movq	$-1, %rax
	ret
	.cfi_endproc
.LFE2:
	.size	foo3, .-foo3
	.ident	"GCC: (GNU) 4.6.0 20110603 (Red Hat 4.6.0-10)"
	.section	.note.GNU-stack,"",@progbits
[hjl@gnu-6 rtm-1]$ 

I was expecting "or" for -O.


---


### compiler : `gcc`
### title : `Loop optimization.`
### open_at : `2011-08-20T05:45:27Z`
### last_modified_date : `2021-12-24T04:14:58Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=50135
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.6.0`
### severity : `normal`
### contents :
May be single-cycle should translate that:
C code:
for(unsigned int i=0; i<123456; i++)
or
for(unsigned int i=123456; i>0; i--)

Assembler code:
movq 123456, %rcx
L0:
   <some code there>
   loop LO


---


### compiler : `gcc`
### title : `__builtin_ctz() and intrinsics __bsr(), __bsf() generate extra sign extend on x86_64`
### open_at : `2011-08-23T16:38:51Z`
### last_modified_date : `2021-08-08T22:48:25Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=50168
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `unknown`
### severity : `normal`
### contents :
Testcase:

--------------------
#include <x86intrin.h>

static inline long my_bsfq(long x) __attribute__((__always_inline__));
static inline long my_bsfq(long x) {
    long result;
    asm(" bsfq %1, %0 \n"
        : "=r"(result)
        : "r"(x)
    );
    return result;
}

long c[64];

long f(long i) {
    return c[ __bsfq(i) ];
}

long g(long i) {
    return c[ __builtin_ctzll(i) ];
}

long h(long i) {
    return c[ my_bsfq(i) ];
}
----------------------



When I compile this with 'gcc -O3 -g testcase.c -c -o testcase.o
&& objdump -d testcase', I get



----------------------
0000000000000000 <f>:
   0:   48 0f bc ff             bsf    %rdi,%rdi
   4:   48 63 ff                movslq %edi,%rdi
   7:   48 8b 04 fd 00 00 00    mov    0x0(,%rdi,8),%rax
   e:   00 
   f:   c3                      retq   

0000000000000010 <g>:
  10:   48 0f bc ff             bsf    %rdi,%rdi
  14:   48 63 ff                movslq %edi,%rdi
  17:   48 8b 04 fd 00 00 00    mov    0x0(,%rdi,8),%rax
  1e:   00 
  1f:   c3                      retq   

0000000000000020 <h>:
  20:   48 0f bc ff             bsf    %rdi,%rdi
  24:   48 8b 04 fd 00 00 00    mov    0x0(,%rdi,8),%rax
  2b:   00 
  2c:   c3                      retq   
-----------------------



Please note the unneeded 32 to 64 bit conversion 'movslq ...' inserted by the compiler in functions f() and g(). It should look like h() instead.

I suspect the source is the prototype of the builtin, whose return type 'int' does not match the "natural" return type on x86_64, which is 64 bit, the same register size as the input register.

If I replace the builtin/intrinsic with the selfmade asm one, I get a nice speedup of 2% in my chessengine.


---


### compiler : `gcc`
### title : `A case that PRE optimization hurts performance`
### open_at : `2011-09-02T05:07:54Z`
### last_modified_date : `2021-07-26T20:54:42Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=50272
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.7.0`
### severity : `normal`
### contents :
For the following simple test case, PRE optimization hoists computation
(s!=1) into the default branch of the switch statement, and finally causes
very poor code generation. This problem occurs in both X86 and ARM, and I
believe it is also a problem for other targets. 

int f(char *t) {
    int s=0;

    while (*t && s != 1) {
        switch (s) {
        case 0:
            s = 2;
            break;
        case 2:
            s = 1;
            break;
        default:
            if (*t == '-') 
                s = 1;
            break;
        }
        t++;
    }

    return s;
}

Taking X86 as an example, with option "-O2" you may find 52 instructions
generated like below,

00000000 <f>:
   0:	55                   	push   %ebp
   1:	31 c0                	xor    %eax,%eax
   3:	89 e5                	mov    %esp,%ebp
   5:	57                   	push   %edi
   6:	56                   	push   %esi
   7:	53                   	push   %ebx
   8:	8b 55 08             	mov    0x8(%ebp),%edx
   b:	0f b6 0a             	movzbl (%edx),%ecx
   e:	84 c9                	test   %cl,%cl
  10:	74 50                	je     62 <f+0x62>
  12:	83 c2 01             	add    $0x1,%edx
  15:	85 c0                	test   %eax,%eax
  17:	75 23                	jne    3c <f+0x3c>
  19:	8d b4 26 00 00 00 00 	lea    0x0(%esi,%eiz,1),%esi
  20:	0f b6 0a             	movzbl (%edx),%ecx
  23:	84 c9                	test   %cl,%cl
  25:	0f 95 c0             	setne  %al
  28:	89 c7                	mov    %eax,%edi
  2a:	b8 02 00 00 00       	mov    $0x2,%eax
  2f:	89 fb                	mov    %edi,%ebx
  31:	83 c2 01             	add    $0x1,%edx
  34:	84 db                	test   %bl,%bl
  36:	74 2a                	je     62 <f+0x62>
  38:	85 c0                	test   %eax,%eax
  3a:	74 e4                	je     20 <f+0x20>
  3c:	83 f8 02             	cmp    $0x2,%eax
  3f:	74 1f                	je     60 <f+0x60>
  41:	80 f9 2d             	cmp    $0x2d,%cl
  44:	74 22                	je     68 <f+0x68>
  46:	0f b6 0a             	movzbl (%edx),%ecx
  49:	83 f8 01             	cmp    $0x1,%eax
  4c:	0f 95 c3             	setne  %bl
  4f:	89 df                	mov    %ebx,%edi
  51:	84 c9                	test   %cl,%cl
  53:	0f 95 c3             	setne  %bl
  56:	89 de                	mov    %ebx,%esi
  58:	21 f7                	and    %esi,%edi
  5a:	eb d3                	jmp    2f <f+0x2f>
  5c:	8d 74 26 00          	lea    0x0(%esi,%eiz,1),%esi
  60:	b0 01                	mov    $0x1,%al
  62:	5b                   	pop    %ebx
  63:	5e                   	pop    %esi
  64:	5f                   	pop    %edi
  65:	5d                   	pop    %ebp
  66:	c3                   	ret    
  67:	90                   	nop
  68:	b8 01 00 00 00       	mov    $0x1,%eax
  6d:	5b                   	pop    %ebx
  6e:	5e                   	pop    %esi
  6f:	5f                   	pop    %edi
  70:	5d                   	pop    %ebp
  71:	c3                   	ret    

But with command line option "-O2 -fno-tree-pre", there are only 12
instructions generated, and the code would be very clean like below,

00000000 <f>:
   0:	55                   	push   %ebp
   1:	31 c0                	xor    %eax,%eax
   3:	89 e5                	mov    %esp,%ebp
   5:	8b 55 08             	mov    0x8(%ebp),%edx
   8:	80 3a 00             	cmpb   $0x0,(%edx)
   b:	74 0e                	je     1b <f+0x1b>
   d:	80 7a 01 00          	cmpb   $0x0,0x1(%edx)
  11:	b0 02                	mov    $0x2,%al
  13:	ba 01 00 00 00       	mov    $0x1,%edx
  18:	0f 45 c2             	cmovne %edx,%eax
  1b:	5d                   	pop    %ebp
  1c:	c3                   	ret


---


### compiler : `gcc`
### title : `Missed optimization, fails to propagate bool`
### open_at : `2011-09-03T23:35:37Z`
### last_modified_date : `2023-05-30T19:18:07Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=50286
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.7.0`
### severity : `minor`
### contents :
GCC 4.7.0 (and prior) are unable to determine maximum loop counts in code that looks like:

#include <stdio.h>
int main(int argc, char **argv)
{
  int i;
  const int flag=argc>1;
  i=0;
  do{
    printf("%d\n",i*i);
  }while(++i<1+flag);
  return 0;
}

and so it doesn't unroll the loop.

If 1+flag is changed to 1+!!flag, 1+(bool)flag, or 1+(argc>1) then -O3 unrolls the loop.

Interestingly, making flag type bool doesn't fix it and also doesn't unroll in the 1+!!flag case.


---


### compiler : `gcc`
### title : `suboptimal register allocation for abs(__int128_t)`
### open_at : `2011-09-09T11:46:18Z`
### last_modified_date : `2023-01-19T23:24:25Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=50339
### status : `NEW`
### tags : `missed-optimization, ra`
### component : `rtl-optimization`
### version : `4.7.0`
### severity : `normal`
### contents :
This function:

__int128_t abs128(__int128_t a)
{
	return (a >= 0) ? a : -a;
}

Currently generates the following code (with -O3):
(linux x86_64, g++-4.7.0, SVN revision 178692)

   49 89 f9                mov    %rdi,%r9
   48 89 f7                mov    %rsi,%rdi
   49 89 f2                mov    %rsi,%r10
   48 c1 ff 3f             sar    $0x3f,%rdi
   48 89 f8                mov    %rdi,%rax
   48 89 fa                mov    %rdi,%rdx
   4c 31 c8                xor    %r9,%rax
   4c 31 d2                xor    %r10,%rdx
   48 29 f8                sub    %rdi,%rax
   48 19 fa                sbb    %rdi,%rdx
   c3                      retq   

But the following has 2 'mov' instructions less:

   48 89 f8                mov    %rdi,%rax
   48 89 f2                mov    %rsi,%rdx
   48 89 d1                mov    %rdx,%rcx
   48 c1 f9 3f             sar    $0x3f,%rcx
   48 31 c8                xor    %rcx,%rax
   48 31 ca                xor    %rcx,%rdx
   48 29 c8                sub    %rcx,%rax
   48 19 ca                sbb    %rcx,%rdx
   c3                      retq


---


### compiler : `gcc`
### title : `Function call foils VRP/jump-threading of redundant predicate on struct member`
### open_at : `2011-09-10T03:29:49Z`
### last_modified_date : `2021-08-11T04:31:03Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=50346
### status : `NEW`
### tags : `alias, missed-optimization`
### component : `tree-optimization`
### version : `4.6.1`
### severity : `enhancement`
### contents :
When compiling the following code with options `-O3 -DBUG' :

// === bug.cpp =======
struct foo {
    bool b;
    foo() : b(false) { }
    void baz();
};

bool bar();
void baz();

void test() {
    foo f;
    bool b = false;
    if (bar()) b = f.b = true;
#ifndef BUG
    if (f.b != b) __builtin_unreachable();
#endif
    if (f.b) f.baz();
}
// === end ==========

gcc fails to eliminate the second (redundant) if statement:

_Z4testv:
.LFB3:
        subq    $24, %rsp
        movb    $0, 15(%rsp)	<=== assign f.b = 0
        call    _Z3barv		<=== cannot access f.b
        testb   %al, %al
        je      .L2
        movb    $1, 15(%rsp)
.L3:
        leaq    15(%rsp), %rdi
        call    _ZN3foo3bazEv
        addq    $24, %rsp
        ret
.L2:
        cmpb    $0, 15(%rsp)	<=== always compares equal
        jne     .L3
        addq    $24, %rsp
        ret

Compiling with `-O3 -UBUG' gives the expected results:

_Z4testv:
.LFB3:
        subq    $24, %rsp
        movb    $0, 15(%rsp)
        call    _Z3barv
        testb   %al, %al
        je      .L1
        leaq    15(%rsp), %rdi
        movb    $1, 15(%rsp)
        call    _ZN3foo3bazEv
.L1:
        addq    $24, %rsp
        ret

This sort of scenario comes up a lot with RAII-related code, particularly when some code paths clean up the object manually before the destructor runs (obviating the need for the destructor to do it again).

While it should be possible to give hints using __builtin_unreachable(), it's not always easy to tell where to put it, and it may need to be placed multiple times to be effective.


---


### compiler : `gcc`
### title : `Support vectorization of min/max location pattern`
### open_at : `2011-09-13T07:48:19Z`
### last_modified_date : `2022-02-17T11:15:05Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=50374
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.7.0`
### severity : `enhancement`
### contents :
in reference to http://gcc.gnu.org/ml/gcc-patches/2010-08/msg00631.html
and the discussion in PR47860:
any chance to see "min/max location pattern" vectorization in 4.7?


---


### compiler : `gcc`
### title : `Reassoc doesn't optimize pointer arithmetics`
### open_at : `2011-09-13T12:44:12Z`
### last_modified_date : `2021-07-25T01:58:15Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=50382
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.7.0`
### severity : `enhancement`
### contents :
This is something I've noticed while writing strlen optimization.
Reassoc doesn't optimize:
typedef __UINTPTR_TYPE__ uintptr_t;

char *
foo (char *p, const char *q, const char *r)
{
  char *a = p + __builtin_strlen (p);
  char *b = __builtin_stpcpy (a, q);
  uintptr_t c = (uintptr_t) b - (uintptr_t) p;
  __builtin_memcpy (b, "abcd", 4);
  uintptr_t d = c + 4;
  return __builtin_stpcpy (p + d, r);
}

and only RTL passes figure out that p + d is b + 4.


---


### compiler : `gcc`
### title : `Returning std::array is not optimal`
### open_at : `2011-09-13T14:46:23Z`
### last_modified_date : `2021-08-16T00:58:48Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=50384
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.7.0`
### severity : `enhancement`
### contents :
#include <array>
typedef std::array<char,7> X;
X f(X,X);
X g(X a,X b){return f(a,b);}

I compiled this code on x86_64 with g++ -std=c++0x -Ofast and got:

_Z1gSt5arrayIcLm7EES0_:
.LFB837:
	.cfi_startproc
	pushq	%rbx
	.cfi_def_cfa_offset 16
	subq	$48, %rsp
	.cfi_def_cfa_offset 64
	.cfi_offset 3, -16
	call	_Z1fSt5arrayIcLm7EES0_
	movzbl	%ah, %edx
	movb	%al, (%rsp)
	movb	%dl, 1(%rsp)
	movq	%rax, %rdx
	shrq	$16, %rdx
	movb	%dl, 2(%rsp)
	movq	%rax, %rdx
	shrq	$24, %rdx
	movb	%dl, 3(%rsp)
	movq	%rax, %rdx
	movl	(%rsp), %ecx
	shrq	$32, %rdx
	movb	%dl, 4(%rsp)
	movq	%rax, %rdx
	shrq	$40, %rdx
	movl	%ecx, %esi
	movzbl	%cl, %ebx
	movb	%dl, 5(%rsp)
	movl	%ecx, %edx
	movzwl	4(%rsp), %edi
	shrl	$16, %edx
	movzbl	%ch, %ecx
	shrl	$24, %esi
	movzbl	%dl, %edx
	movb	%cl, %bh
	movzbl	%sil, %esi
	salq	$16, %rdx
	salq	$24, %rsi
	movabsq	$-1095216660481, %rcx
	orq	%rbx, %rdx
	movq	%rdi, %rbx
	addq	$48, %rsp
	.cfi_def_cfa_offset 16
	orq	%rsi, %rdx
	movzbl	%dil, %esi
	salq	$32, %rsi
	andq	%rcx, %rdx
	movzbl	%bh, %ecx
	orq	%rsi, %rdx
	movabsq	$-280375465082881, %rsi
	salq	$40, %rcx
	andq	%rsi, %rdx
	orq	%rcx, %rdx
	movabsq	$71776119061217280, %rcx
	andq	%rcx, %rax
	movabsq	$-71776119061217281, %rcx
	andq	%rcx, %rdx
	orq	%rax, %rdx
	movq	%rdx, %rax
	popq	%rbx
	.cfi_def_cfa_offset 8
	ret
	.cfi_endproc

Ideally I would have liked a single jmp, but in any case this seems a bit long... (the attribute((aligned)) in versions <= 4.2 did help)
Is that the best that can legally be done without alignment information?


---


### compiler : `gcc`
### title : `[11/12/13/14 regression]: memcpy with known alignment`
### open_at : `2011-09-15T08:49:31Z`
### last_modified_date : `2023-09-20T19:26:48Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=50417
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.7.0`
### severity : `normal`
### contents :
Consider these functions:

void copy1(char* d, const char* s) {
	memcpy(d, s, 256);
}
void copy2(short* d, const short* s) {
	memcpy(d, s, 256);
}
void copy3(int* d, const int* s) {
	memcpy(d, s, 256);
}
void copy4(long* d, const long* s) {
	memcpy(d, s, 256);
}

g++-4.5.2 is able to generate better code for the later functions. But when I test with a recent snapshot (SVN revision 178875 on linux x86_64) it generates the same code for all versions (same as copy1()).


---


### compiler : `gcc`
### title : `Casts to restrict pointers have no effect`
### open_at : `2011-09-15T14:14:07Z`
### last_modified_date : `2022-12-26T06:39:25Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=50419
### status : `NEW`
### tags : `alias, missed-optimization`
### component : `tree-optimization`
### version : `4.7.0`
### severity : `normal`
### contents :
% cat predcom-fail.c
#define INFTY       987654321
#define Ra /*__restrict*/
#define Rv __restrict
void
P7Viterbi(int * Ra _dc, int * Ra _mc, int * Ra _tpdd, int * Ra _tpmd, int M)
{
  int   i,k;
  int   sc;
  int * Rv dc = _dc;
  int * Rv mc = _mc;
  int * Rv tpdd = _tpdd;
  int * Rv tpmd = _tpmd;

  dc[0] = -INFTY;

  for (k = 1; k < M; k++) {
    dc[k] = dc[k-1] + tpdd[k-1];
    if ((sc = mc[k-1] + tpmd[k-1]) > dc[k]) dc[k] = sc;
    if (dc[k] < -INFTY) dc[k] = -INFTY;
  }
}

./cc1 -Ofast predcom-fail.c should be able to predcom the loop.  It doesn't
because it doesn't see that the (first) dc[] write doesn't conflict with the
mc/tpmd[] reads.  It should be able to see that because all the int pointers
are created with new restrict sets.  If you defined Ra as also __restrict
(making the arguments already restrict qualified) you get the transformation.

The problem is an interaction between creating the datarefs and the
disambiguator.  The data-ref base objects contain the casted inputs:

#(Data Ref:
#  bb: 4
#  stmt: D.2741_19 = *D.2740_18;
#  ref: *D.2740_18;
#  base_object: *(int * restrict) _dc_2(D);
#  Access function 0: {0B, +, 4}_1
#)
vs
#(Data Ref:
#  bb: 4
#  stmt: D.2743_24 = *D.2742_23;
#  ref: *D.2742_23;
#  base_object: *(int * restrict) _tpdd_6(D);
#  Access function 0: {0B, +, 4}_1
#)

The disambiguator used is ptr_derefs_may_alias_p on those two (casted)
pointers.  But the first thing it does is to remove all conversions.
Remembering the original type wouldn't help as we need to look into the
points-to info of the restrict qualified object (i.e. the LHS of that
conversion).

Hence when creating the data-ref we shouldn't look through such casts, that
introduce useful information.  I have a patch.


---


### compiler : `gcc`
### title : `Constructors of static external vars are throwed away leading to missed optimizations (and ipa-cp ICE).`
### open_at : `2011-09-16T10:33:00Z`
### last_modified_date : `2021-01-07T16:52:25Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=50430
### status : `NEW`
### tags : `lto, missed-optimization`
### component : `lto`
### version : `4.7.0`
### severity : `enhancement`
### contents :
The LTO streaming code deals only with ctors of finalized variables, however static external vars are useful for optimization. Vtables are common cases like this.  Current mainline dies building libreoffice at:
(gdb) bt
#0  useless_type_conversion_p (outer_type=0x7ffff53501f8, inner_type=0x66686e6973615f6e) at ../../gcc/tree-ssa.c:1292
#1  0x00000000005d77fc in fold_ctor_reference (type=0x7ffff53501f8, ctor=0x7ffff7ec0b10, offset=1088, size=64) at ../../gcc/gimple-fold.c:2880
#2  0x00000000005d7e38 in gimple_get_virt_method_for_binfo (token=15, known_binfo=0x7ffff2d39820) at ../../gcc/gimple-fold.c:3056
#3  0x0000000000ae6fde in devirtualization_time_bonus (node=<optimized out>, known_csts=0x3625de0, known_binfos=0x3625d80) at ../../gcc/ipa-cp.c:1170
#4  0x0000000000aeae9c in estimate_local_effects (node=<optimized out>) at ../../gcc/ipa-cp.c:1401
#5  propagate_constants_topo (topo=<optimized out>) at ../../gcc/ipa-cp.c:1548
#6  ipcp_propagate_stage (topo=<optimized out>) at ../../gcc/ipa-cp.c:1631
#7  ipcp_driver () at ../../gcc/ipa-cp.c:2434
#8  0x00000000006733b7 in execute_one_pass (pass=0x10946e0) at ../../gcc/passes.c:2063
#9  0x0000000000673b86 in execute_ipa_pass_list (pass=0x10946e0) at ../../gcc/passes.c:2430
#10 0x00000000004ab3c4 in do_whole_program_analysis () at ../../gcc/lto/lto.c:2670
#11 0x00000000004adf6d in lto_main () at ../../gcc/lto/lto.c:2796
#12 0x0000000000706d42 in compile_file () at ../../gcc/toplev.c:548
#13 do_compile () at ../../gcc/toplev.c:1886
#14 toplev_main (argc=171, argv=0x1201290) at ../../gcc/toplev.c:1962
#15 0x00007ffff63efbc6 in __libc_start_main () from /lib64/libc.so.6
#16 0x00000000004909e9 in _start () at ../sysdeps/x86_64/elf/start.S:113

ctor passed to ctor_reference is error_mark indicating that the value has not been streamed.

(gdb) p debug_tree (v)
 <var_decl 0x7fffe55dc140 _ZTV11SfxVoidItem
    type <array_type 0x7ffff5367e70
        type <pointer_type 0x7ffff53501f8 __vtbl_ptr_type type <function_type 0x7ffff53502a0>
            public unsigned DI
            size <integer_cst 0x7ffff7eb9ec0 constant 64>
            unit size <integer_cst 0x7ffff7eb9ee0 constant 8>
            align 64 symtab 0 alias set -1 canonical type 0x7ffff53591f8
            pointer_to_this <pointer_type 0x7ffff5350150>>
        BLK
        size <integer_cst 0x7ffff5366000 constant 1152>
        unit size <integer_cst 0x7ffff5366080 constant 144>
        align 64 symtab 0 alias set 2 canonical type 0x7ffff5367e70
        domain <integer_type 0x7ffff5367f18 type <integer_type 0x7ffff7ec9000 sizetype>
            DI size <integer_cst 0x7ffff7eb9ec0 64> unit size <integer_cst 0x7ffff7eb9ee0 8>
            align 64 symtab 0 alias set -1 canonical type 0x7ffff7ec9738 precision 64 min <integer_cst 0x7ffff7eb9f00 0> max <integer_cst 0x7ffff53660a0 17>>
        pointer_to_this <pointer_type 0x7ffff4f41738>>
    readonly public static ignored external virtual BLK file /abuild/jh/libreoffice/core/solver/unxlngx6.pro/inc/svl/poolitem.hxx line 352 col 0 size <integer_cst 0x7ffff5366000 1152> unit size <integer_cst 0x7ffff5366080 144>
    align 64 context <record_type 0x7ffff53bb2a0 SfxVoidItem> initial <error_mark 0x7ffff7ec0b10>>
$2 = void

I guess the following is correct fix for the ICE (to also avoid ICEs in case of invalid programs etc.)

jan@linux-7ldc:~/trunk/gcc> svn diff gimple-fold.c
Index: gimple-fold.c
===================================================================
--- gimple-fold.c       (revision 178905)
+++ gimple-fold.c       (working copy)
@@ -3048,7 +3048,8 @@ gimple_get_virt_method_for_binfo (HOST_W
 
   if (TREE_CODE (v) != VAR_DECL
       || !DECL_VIRTUAL_P (v)
-      || !DECL_INITIAL (v))
+      || !DECL_INITIAL (v)
+      || DECL_INITIAL (v) == error_mark_node)
     return NULL_TREE;
   gcc_checking_assert (TREE_CODE (TREE_TYPE (v)) == ARRAY_TYPE);
   size = tree_low_cst (TYPE_SIZE (TREE_TYPE (TREE_TYPE (v))), 1);


but then we are missing optimization here.  I guess extern static vars should go same way as extern inlines: i.e. be finalized to cgraph and then optimized out after devirtualization.

Honza


---


### compiler : `gcc`
### title : `128 bit unsigned int subtraction generates too many register moves`
### open_at : `2011-09-16T20:51:33Z`
### last_modified_date : `2022-02-28T13:45:28Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=50440
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.6.1`
### severity : `normal`
### contents :
I want to perform 128 bit integer arithmetic, and I am declaring my type like this:

{{{
typedef unsigned int uint128_t __attribute__((mode(TI)));
uint128_t add (uint128_t x, uint128_t y) { return x+y; }
uint128_t sub (uint128_t x, uint128_t y) { return x-y; }
}}}

This is on an Intel Xeon processor in x86_64 mode. I build with the command

gcc-4.6.1 -O3 -march=native -S sub128.c

and I find that, while the "add" routine looks optimal, the "sub" routine has several unnecessary register moves:

{{{
add:
	movq    %rdx, %rax
	movq    %rcx, %rdx
	addq    %rdi, %rax
	adcq    %rsi, %rdx
	ret
sub:
	movq    %rsi, %r10
	movq    %rdi, %rsi
	subq    %rdx, %rsi
	movq    %r10, %rdi
	sbbq    %rcx, %rdi
	movq    %rsi, %rax
	movq    %rdi, %rdx
	ret
}}}


---


### compiler : `gcc`
### title : `volatile forces load into register`
### open_at : `2011-10-09T12:51:31Z`
### last_modified_date : `2023-02-09T18:11:24Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=50677
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.7.0`
### severity : `enhancement`
### contents :
Compiling this simple program (-Ofast):

void f(int volatile*i){++*i;}

produces this code:

	movl	(%rdi), %eax
	addl	$1, %eax
	movl	%eax, (%rdi)

(or incl %eax for the central line with -Os).

However, if I remove "volatile", I get the nicer:

	addl	$1, (%rdi)

(or incl (%rdi) with -Os).

The second version seems legal to me even in the volatile case, is that wrong?

There might be a relation to this thread:
http://gcc.gnu.org/ml/gcc/2011-10/msg00006.html
(no volatile there, but a failure to fuse load+add+store)

This is particularly noticable because people (wrongly) use volatile for threaded code and the 3 instruction version is likely even more racy than the one with a single instruction.

(sorry if the category is wrong, I just picked one with "optimization" in the name...)


---


### compiler : `gcc`
### title : `SLP vs loop: code generated differs (SLP less efficient)`
### open_at : `2011-10-13T09:06:05Z`
### last_modified_date : `2021-08-16T05:24:32Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=50713
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.8.0`
### severity : `normal`
### contents :
in the following code 
for "float" 
the code generated by "dosum" and "dosuml" differs (dosum better)
for "complex" 
"sum" does not vectorize! (a problem in itself)
"dosum" excellent vectorization, dusuml: same issue that with floats

if you have time please have a look of what happens with aligned(32)
sse vs avx, float vs double… (not an urgent use case at the moment)

compiled with
c++ -Ofast -ftree-vectorizer-verbose=2 -c slp2.cc -mtune=corei7 -msse4.2

// typedef __complex__ float Value;
typedef float Value;
// typedef double Value;

struct A {
  Value a[4];
}   __attribute__ ((aligned(16)));

A a1, a2, a3;

A sum(A a, A b) {
  a.a[0]+=b.a[0];
  a.a[1]+=b.a[1];
  a.a[2]+=b.a[2];
  a.a[3]+=b.a[3];
  return a;
}

A suml(A a, A b) {
  for (int i=0;i!=4;++i) a.a[i]+=b.a[i];
  return a;
}


void dosum() {
  a1 = sum(a2,a3);
}

void dosuml() {
  a1 = suml(a2,a3);
}




float
========
sum(A, A):
        movq    %xmm2,0xc8(%rsp)
        movq    %xmm3,0xd0(%rsp)
        movq    %xmm0,0xd8(%rsp)
        movaps  0xc8(%rsp),%xmm0
        movq    %xmm1,0xe0(%rsp)
        addps   0xd8(%rsp),%xmm0
        movaps  %xmm0,0xa8(%rsp)
        movq    0xa8(%rsp),%rax
        movaps  %xmm0,0xe8(%rsp)
        movq    0xf0(%rsp),%xmm1
        movd    %rax,%xmm0
        ret
        nopl    (%rax)
suml(A, A):
        movq    %xmm2,0xc8(%rsp)
        movq    %xmm3,0xd0(%rsp)
        movq    %xmm0,0xd8(%rsp)
        movaps  0xc8(%rsp),%xmm0
        movq    %xmm1,0xe0(%rsp)
        addps   0xd8(%rsp),%xmm0
        movaps  %xmm0,0xa8(%rsp)
        movq    0xa8(%rsp),%rax
        movaps  %xmm0,0xd8(%rsp)
        movq    0xe0(%rsp),%xmm1
        movd    %rax,%xmm0
        ret
        nopl    (%rax)
dosum():
        movaps  _a2(%rip),%xmm0
        addps   _a3(%rip),%xmm0
        movaps  %xmm0,_a1(%rip)
        ret
        nopw    %cs:sum(A, A)(%rax,%rax)
dosuml():
        movq    _a2(%rip),%rax
        movq    %rax,0xb8(%rsp)
        movq    _a2+0x00000008(%rip),%rax
        movq    %rax,0xc0(%rsp)
        movq    _a3(%rip),%rax
        movq    %rax,0xc8(%rsp)
        movq    _a3+0x00000008(%rip),%rax
        movq    %rax,0xd0(%rsp)
        movaps  0xc8(%rsp),%xmm0
        addps   0xb8(%rsp),%xmm0
        movaps  %xmm0,0xa8(%rsp)
        movq    0xa8(%rsp),%rax
        movaps  %xmm0,0xb8(%rsp)
        movq    %rax,_a1(%rip)
        movq    0xc0(%rsp),%rax
        movq    %rax,_a1+0x00000008(%rip)
        ret


complex
==========

sum(A, A):
	movss	0x28(%rsp),%xmm7
	movq	%rdi,%rax
	movss	0x2c(%rsp),%xmm6
	movss	0x30(%rsp),%xmm5
	movss	0x34(%rsp),%xmm4
	movss	0x38(%rsp),%xmm3
	movss	0x3c(%rsp),%xmm2
	movss	0x40(%rsp),%xmm1
	movss	0x44(%rsp),%xmm0
	addss	0x08(%rsp),%xmm7
	addss	0x0c(%rsp),%xmm6
	addss	0x10(%rsp),%xmm5
	addss	0x14(%rsp),%xmm4
	movss	%xmm7,(%rdi)
	addss	0x18(%rsp),%xmm3
	movss	%xmm6,0x04(%rdi)
	addss	0x1c(%rsp),%xmm2
	movss	%xmm5,0x08(%rdi)
	addss	0x20(%rsp),%xmm1
	movss	%xmm4,0x0c(%rdi)
	addss	0x24(%rsp),%xmm0
	movss	%xmm3,0x10(%rdi)
	movss	%xmm2,0x14(%rdi)
	movss	%xmm1,0x18(%rdi)
	movss	%xmm0,0x1c(%rdi)
	ret
	nopl	sum(A, A)(%rax,%rax)
suml(A, A):
	movaps	0x08(%rsp),%xmm0
	movq	%rdi,%rax
	addps	0x28(%rsp),%xmm0
	movaps	%xmm0,0xe8(%rsp)
	movaps	%xmm0,0x08(%rsp)
	movaps	0x18(%rsp),%xmm0
	movq	0xe8(%rsp),%rcx
	addps	0x38(%rsp),%xmm0
	movaps	%xmm0,0xe8(%rsp)
	movq	0xe8(%rsp),%rdx
	movaps	%xmm0,0x18(%rsp)
	movq	%rcx,(%rdi)
	movq	0x10(%rsp),%rcx
	movq	%rdx,0x10(%rdi)
	movq	0x20(%rsp),%rdx
	movq	%rcx,0x08(%rdi)
	movq	%rdx,0x18(%rdi)
	ret
	nop
dosum():
	movaps	_a2+0x00000010(%rip),%xmm0
	movaps	_a2(%rip),%xmm1
	addps	_a3+0x00000010(%rip),%xmm0
	addps	_a3(%rip),%xmm1
	movaps	%xmm0,_a1+0x00000010(%rip)
	movaps	%xmm1,_a1(%rip)
	ret
	nopl	sum(A, A)(%rax,%rax)
dosuml():
	movq	_a2(%rip),%rax
	movq	%rax,0x98(%rsp)
	movq	_a2+0x00000008(%rip),%rax
	movq	%rax,0xa0(%rsp)
	movq	_a2+0x00000010(%rip),%rax
	movq	%rax,0xa8(%rsp)
	movq	_a2+0x00000018(%rip),%rax
	movq	%rax,0xb0(%rsp)
	movq	_a3(%rip),%rax
	movq	%rax,0xb8(%rsp)
	movq	_a3+0x00000008(%rip),%rax
	movq	%rax,0xc0(%rsp)
	movq	_a3+0x00000010(%rip),%rax
	movaps	0xb8(%rsp),%xmm0
	addps	0x98(%rsp),%xmm0
	movq	%rax,0xc8(%rsp)
	movq	_a3+0x00000018(%rip),%rax
	movaps	%xmm0,0x88(%rsp)
	movaps	%xmm0,0x98(%rsp)
	movaps	0xa8(%rsp),%xmm0
	movq	%rax,0xd0(%rsp)
	movq	0x88(%rsp),%rdx
	addps	0xc8(%rsp),%xmm0
	movaps	%xmm0,0x88(%rsp)
	movq	0x88(%rsp),%rax
	movaps	%xmm0,0xa8(%rsp)
	movq	%rdx,_a1(%rip)
	movq	0xa0(%rsp),%rdx
	movq	%rax,_a1+0x00000010(%rip)
	movq	0xb0(%rsp),%rax
	movq	%rdx,_a1+0x00000008(%rip)
	movq	%rax,_a1+0x00000018(%rip)
	ret


---


### compiler : `gcc`
### title : `Inefficient vector loads from aggregates passed by value`
### open_at : `2011-10-14T12:37:50Z`
### last_modified_date : `2021-07-26T21:16:52Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=50728
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.7.0`
### severity : `enhancement`
### contents :
For

typedef float Value;
struct A {
  Value a[4];
} __attribute__ ((aligned(16)));

A sum(A a, A b)
{
  a.a[0]+=b.a[0];
  a.a[1]+=b.a[1];
  a.a[2]+=b.a[2];
  a.a[3]+=b.a[3];
  return a;
}

due to the way the x86_64 ABI passes A by value generates horribly inefficient
code at -O3 when the vectorizer generates vector loads/stores from/to a and b.

Initial RTL expansion for the load from a is

(insn 2 11 3 2 (set (reg:DI 64)
        (reg:DI 21 xmm0 [ a ])) t.C:7 -1
     (nil))

(insn 3 2 6 2 (set (reg:DI 65)
        (reg:DI 22 xmm1 [ a+8 ])) t.C:7 -1
     (nil))

(insn 4 7 5 2 (set (mem/s/c:DI (plus:DI (reg/f:DI 54 virtual-stack-vars)
                (const_int -32 [0xffffffffffffffe0])) [2 a+0 S8 A128])
        (reg:DI 64)) t.C:7 -1
     (nil))

(insn 5 4 8 2 (set (mem/s/c:DI (plus:DI (reg/f:DI 54 virtual-stack-vars)
                (const_int -24 [0xffffffffffffffe8])) [2 a+8 S8 A64])
        (reg:DI 65)) t.C:7 -1
     (nil))

(insn 14 13 15 3 (parallel [
            (set (reg:DI 69)
                (plus:DI (reg/f:DI 54 virtual-stack-vars)
                    (const_int -32 [0xffffffffffffffe0])))
            (clobber (reg:CC 17 flags))
        ]) t.C:8 -1
     (nil))

(insn 15 14 16 3 (set (reg:V4SF 71)
        (mem/c:V4SF (reg:DI 69) [2 MEM[(struct A *)&a]+0 S16 A128])) t.C:8 -1
     (nil))

so it is forced to go through first general regs and then memory,
instead of a simple sequence of mov[hl]ps.

As this is probably hard to fix at RTL expansion time something later
should be able to fix this up - and as this is all memory the only
candidate seems to be (g)cse.


---


### compiler : `gcc`
### title : `Auto-inc-dec does not find subsequent contiguous mem accesses`
### open_at : `2011-10-16T20:28:50Z`
### last_modified_date : `2023-07-22T02:53:52Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=50749
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.7.0`
### severity : `enhancement`
### contents :
Post-increment addressing is generated only for the first
memory access. Any subsequent memory access does not use 
post-increment addressing.
The following two functions are reduced examples and result
in the same code being generated.
The problem exists with any number of memory accesses > 1
and at any optimization level.


int test_0 (char* p, int c)
{
  int r = 0;
  r += *p++;
  r += *p++;
  r += *p++;
  return r;
}

int test_1 (char* p, int c)
{
  int r = 0;
  r += p[0];
  r += p[1];
  r += p[2];
  return r;
}

compiled with -fno-ivopts -Os -m4-single -ml ... 

	mov	r4,r1
	mov.b	@r1+,r0
	add	#2,r4
	mov.b	@r1,r1
	add	r1,r0
	mov.b	@r4,r1
	rts	
	add	r1,r0

This could be done better ...

	mov.b	@r4+,r0
	mov.b	@r4+,r1
	add	r1,r0
	mov.b	@r4+,r1
	rts	
	add	r1,r0



Another example with a loop:

int test_func_1 (char* p, int c)
{
  int r = 0;
  do
  {
    r += *p++;
    r += *p++;
  } while (--c);
  return r;
}

compiled with -fno-ivopts -Os -m4-single -ml ... 

	mov	#0,r0
.L5:
	mov	r4,r1
	mov.b	@r1+,r2
	dt	r5
	mov.b	@r1,r1
	add	r2,r0
	add	#2,r4
	bf/s	.L5
	add	r1,r0
	rts	
	nop

would be better as:

	mov	#0, r0
.L5:
	mov.b	@r4+, r1
	dt	r5
	mov.b	@r4+, r2
	add	r1, r0
	bf/s	.L5
	add	r2, r0

	rts
	nop




Using built-in specs.
COLLECT_GCC=sh-elf-gcc
COLLECT_LTO_WRAPPER=/usr/local/libexec/gcc/sh-elf/4.7.0/lto-wrapper
Target: sh-elf
Configured with: ../gcc-trunk/configure --target=sh-elf --prefix=/usr/local --enable-languages=c,c++ --enable-multilib --disable-libssp --disable-nls --disable-werror --enable-lto --with-newlib --with-gnu-as --with-gnu-ld --with-system-zlib
Thread model: single
gcc version 4.7.0 20111016 (experimental) (GCC)


---


### compiler : `gcc`
### title : `request to better handle non-constant distance vectors to avoid unnecessary alias check`
### open_at : `2011-10-17T09:54:40Z`
### last_modified_date : `2021-08-07T22:38:50Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=50756
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.7.0`
### severity : `enhancement`
### contents :
this is a follow up to PR50698
this snippet

void loop(float *  x, int n) {
  for (int i=0;i!=n; ++i)
    x[i]=x[i+n]+x[i+2*n];
}

generates aliasing checks even if memory regions are clearly disjoint
(see analysis in comments 6 and 7 of PR50698)

I'm now experimenting with "structure of arrays" in place of "array of structures" to make better use of vectorization (and cpu-caches). Reducing unecessary aliasing will further improve performance (and reduce code size).It will also avoid the need to set --param vect-max-version-for-alias-checks=100 or so.


---


### compiler : `gcc`
### title : `Gather vectorization`
### open_at : `2011-10-19T07:49:49Z`
### last_modified_date : `2021-08-16T23:47:13Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=50789
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.7.0`
### severity : `enhancement`
### contents :
This is to track progress on vectorization using AVX2 v*gather* instructions.

The instructions allow plain unconditional gather, e.g.:
#define N 1024
float f[N];
int k[N];
float *l[N];
int **m[N];

float
f1 (void)
{
  int i;
  float g = 0.0;
  for (i = 0; i < N; i++)
    g += f[k[i]];
  return g;
}

float
f2 (float *p)
{
  int i;
  float g = 0.0;
  for (i = 0; i < N; i++)
    g += p[k[i]];
  return g;
}

float
f3 (void)
{
  int i;
  float g = 0.0;
  for (i = 0; i < N; i++)
    g += *l[i];
  return g;
}

int
f4 (void)
{
  int i;
  int g = 0;
  for (i = 0; i < N; i++)
    g += **m[i];
  return g;
}

should be able to vectorize all 4 loops.  In f1/f2 it would use non-zero base (the vector would contain just indexes into some array, which vgather sign extends and adds to base), in f3/f4 it would use zero base - the vectors would be vectors of pointers (resp. uintptr_t).

To vectorize the above I'm afraid we'd need to modify tree-data-ref.c as well as tree-vect-data-ref.c, because the memory accesses aren't affine and already
dr_analyze_innermost gives up on those, doesn't fill in any of the DR_* stuff.
Perhaps with some flag and when the base resp. offset has vdef in the same loop
we could mark it somehow and at least fill in the other fields.  It would probably make alias decisions (in tree-vect-data-ref.c?) harder.  Any ideas?

What is additionally possible is to conditionalize loads, either affine or not.
So something like:
for (i = 0; i < N; i++)
  {
    c = 6;
    if (a[i] > 24)
      c = b[i];
    d[i] = c + e[i];
  }
for the affine conditional accesses where the vector could be just { 0, 1, 2, 3, ... } but the mask from the comparison.


---


### compiler : `gcc`
### title : `ARM: suboptimal code for absolute difference calculation`
### open_at : `2011-10-24T14:52:40Z`
### last_modified_date : `2023-10-22T04:12:45Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=50856
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.7.0`
### severity : `enhancement`
### contents :
gcc generates suboptimal code on ARM for "abs(a - b)" type of operation, which is used for example in paeth png filter: http://www.w3.org/TR/PNG-Filters.html

Given the following test code:


int absolute_difference1(unsigned char a, unsigned char b)
{
    return a > b ? a - b : b - a;
}

int absolute_difference2(unsigned char a, unsigned char b)
{
    int tmp = a;
    if ((tmp -= b) < 0)
        tmp = -tmp;
    return tmp;
}


The current gcc svn trunk (r180383) generates the following code for -O2 and -Os optimizations:

        .cpu arm10tdmi
        .eabi_attribute 27, 3
        .eabi_attribute 28, 1
        .fpu vfp
        .eabi_attribute 20, 1
        .eabi_attribute 21, 1
        .eabi_attribute 23, 3
        .eabi_attribute 24, 1
        .eabi_attribute 25, 1
        .eabi_attribute 26, 2
        .eabi_attribute 30, 4
        .eabi_attribute 34, 0
        .eabi_attribute 18, 4
        .file   "test.c"
        .text
        .align  2
        .global absolute_difference1
        .type   absolute_difference1, %function
absolute_difference1:
        @ args = 0, pretend = 0, frame = 0
        @ frame_needed = 0, uses_anonymous_args = 0
        @ link register save eliminated.
        cmp     r0, r1
        rsbhi   r0, r1, r0
        rsbls   r0, r0, r1
        bx      lr
        .size   absolute_difference1, .-absolute_difference1
        .align  2
        .global absolute_difference2
        .type   absolute_difference2, %function
absolute_difference2:
        @ args = 0, pretend = 0, frame = 0
        @ frame_needed = 0, uses_anonymous_args = 0
        @ link register save eliminated.
        rsb     r0, r1, r0
        cmp     r0, #0
        rsblt   r0, r0, #0
        bx      lr
        .size   absolute_difference2, .-absolute_difference2
        .ident  "GCC: (GNU) 4.7.0 20111024 (experimental)"
        .section        .note.GNU-stack,"",%progbits

Even in the quite explicit second code variant ('absolute_difference2' function), gcc does not generate the expected SUBS + NEGLT pair of instructions. Also for ARMv6 capable processors even a single USAD8 instruction could be used here if both operands are known to have values in [0-255] range and if high latency of this instruction can be hidden.


---


### compiler : `gcc`
### title : `[ARM] Suboptimal optimization for small structures`
### open_at : `2011-10-27T11:53:48Z`
### last_modified_date : `2022-02-04T16:29:35Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=50883
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.6.2`
### severity : `enhancement`
### contents :
Compared to PowerPC the optimization for the attached test case is suboptimal.

Command line:

arm-eabi-gcc -O2 -march=armv7-m -mthumb -S test-1.c -o test-1-arm.s
powerpc-rtems4.11-gcc -O2 -S test-1.c -o test-1-ppc.s


---


### compiler : `gcc`
### title : `Register allocation depends on function return expression on x86 32-bits`
### open_at : `2011-10-28T12:59:52Z`
### last_modified_date : `2021-08-07T22:01:00Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=50898
### status : `RESOLVED`
### tags : `missed-optimization, ra`
### component : `rtl-optimization`
### version : `4.7.0`
### severity : `normal`
### contents :
Created attachment 25643
Testcase

This problem has been noticed during investigation for PR50164.
For attached test case allocator's assignment of registers in some piece of code depends on how return expression looks like. And it seems that there are no reasons for this.

For attached case we have following code snippet obtained by fresh compiler:

.L13:
        movzbl  (%esi), %ecx   
        leal    3(%esi), %ebp
        movb    %cl, 48(%esp)
        notb    48(%esp)
        movzbl  1(%esi), %ecx
        movzbl  2(%esi), %ebx
        notl    %ecx
        notl    %ebx
        cmpb    %cl, 48(%esp)
        movl    %ebp, %esi
        movb    %bl, 32(%esp)
        jb      .L18
        cmpb    %cl, 32(%esp)
        movzbl  32(%esp), %ebx
        cmova   %ecx, %ebx
        movl    %ebx, %edi
        jmp     .L10


But if return expression turn to "return 0" we will see following code which is actually more optimal:

.L13:
        movzbl  (%esi), %edx  <--- edx is used instead of ecx
        leal    3(%esi), %ebp
        movzbl  1(%esi), %ecx
        notl    %edx
        movzbl  2(%esi), %ebx
        notl    %ecx
        notl    %ebx
        cmpb    %cl, %dl
        movl    %ebp, %esi
        movb    %dl, 48(%esp)
        movb    %bl, 32(%esp)
        jb      .L18
        cmpb    %cl, 32(%esp)
        movzbl  32(%esp), %ebx
        cmova   %ecx, %ebx
        movl    %ebx, %edi
        jmp     .L10


 So for some reasons in the first case edx is not used and code contains more memory instructions.

 gcc -v:
Using built-in specs.
COLLECT_GCC=/export/users/izamyati/compiler/build/bin/gcc
COLLECT_LTO_WRAPPER=/export/users/izamyati/compiler/build/libexec/gcc/x86_64-unknown-linux-gnu/4.7.0/lto-wrapper
Target: x86_64-unknown-linux-gnu
Configured with: ../configure --disable-bootstrap --enable-languages=c,c++ --prefix=/export/users/izamyati/compiler/build/
Thread model: posix
gcc version 4.7.0 20111026 (experimental) (GCC) 

Options for slow code: " -m32  -march=atom -O2 -c"
Options for fast code: " -m32  -march=atom -O2 -DGOOD -c"


---


### compiler : `gcc`
### title : `Unoptimal code for vec-shift by scalar for integer (byte, short, long long) operands`
### open_at : `2011-10-30T09:09:40Z`
### last_modified_date : `2021-08-28T19:55:20Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=50918
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.7.0`
### severity : `normal`
### contents :
Following testcase:

--cut here--
#define N 8

short a[N] = { 1,2,3,4,10,20,30,90 };
short r[N];

void
test_var (int n)
{
  int i;

  for (i = 0; i < N; i++)
    r[i] = a[i] << n;
}

void
test_cst (void)
{
  int i;

  for (i = 0; i < N; i++)
    r[i] = a[i] << 3;
}
--cut here--

compiles to (-march=corei7 -O2 -ftree-vectorize):

test_var:
	movdqa	a(%rip), %xmm0
	movd	%edi, %xmm2
	pmovsxwd	%xmm0, %xmm1
	psrldq	$8, %xmm0
	pmovsxwd	%xmm0, %xmm0
	pslld	%xmm2, %xmm1
	pslld	%xmm2, %xmm0
	pshufb	.LC0(%rip), %xmm1
	pshufb	.LC1(%rip), %xmm0
	por	%xmm1, %xmm0
	movdqa	%xmm0, r(%rip)
	ret

test_cst:
	movdqa	a(%rip), %xmm0
	pmovsxwd	%xmm0, %xmm1
	psrldq	$8, %xmm0
	pmovsxwd	%xmm0, %xmm0
	pslld	$3, %xmm1
	pshufb	.LC0(%rip), %xmm1
	pslld	$3, %xmm0
	pshufb	.LC1(%rip), %xmm0
	por	%xmm1, %xmm0
	movdqa	%xmm0, r(%rip)
	ret

Why not psllw ?

The .optimized dump already shows:

test_var (int n)
{
  vector(8) short int vect_var_.16;
  vector(4) int vect_var_.15;
  vector(4) int vect_var_.14;
  vector(8) short int vect_var_.13;

<bb 2>:
  vect_var_.13_23 = MEM[(short int[8] *)&a];
  vect_var_.14_24 = [vec_unpack_lo_expr] vect_var_.13_23;
  vect_var_.14_25 = [vec_unpack_hi_expr] vect_var_.13_23;
  vect_var_.15_26 = vect_var_.14_24 << n_5(D);
  vect_var_.15_27 = vect_var_.14_25 << n_5(D);
  vect_var_.16_28 = VEC_PACK_TRUNC_EXPR <vect_var_.15_26, vect_var_.15_27>;
  MEM[(short int[8] *)&r] = vect_var_.16_28;
  return;

}


test_cst ()
{
  vector(8) short int vect_var_.36;
  vector(4) int vect_var_.35;
  vector(4) int vect_var_.34;
  vector(8) short int vect_var_.33;

<bb 2>:
  vect_var_.33_22 = MEM[(short int[8] *)&a];
  vect_var_.34_23 = [vec_unpack_lo_expr] vect_var_.33_22;
  vect_var_.34_24 = [vec_unpack_hi_expr] vect_var_.33_22;
  vect_var_.35_25 = vect_var_.34_23 << 3;
  vect_var_.35_26 = vect_var_.34_24 << 3;
  vect_var_.36_27 = VEC_PACK_TRUNC_EXPR <vect_var_.35_25, vect_var_.35_26>;
  MEM[(short int[8] *)&r] = vect_var_.36_27;
  return;

}

The same unoptimal code is generated for long-long and byte (-mxop target) signed and unsigned arguments, left and right shifts. OTOH, int arguments produce optimal code for left and right shifts:

test_var:
	movdqa	a(%rip), %xmm0
	movd	%edi, %xmm1
	pslld	%xmm1, %xmm0
	movdqa	%xmm0, r(%rip)
	ret

test_cst:
	movdqa	a(%rip), %xmm0
	pslld	$3, %xmm0
	movdqa	%xmm0, r(%rip)
	ret


---


### compiler : `gcc`
### title : `x86 alloca adds 15 twice`
### open_at : `2011-10-31T17:37:11Z`
### last_modified_date : `2021-09-09T23:32:26Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=50938
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.7.0`
### severity : `normal`
### contents :
Using alloca on x86 requires that the return value be aligned to a 16-byte (boundary).  So code needs to add 15 to the size and then do & ~15.  However, compile this file:

extern void bar (char *);
void
foo (int n)
{
  bar (__builtin_alloca (n));
}

The generated code adds 30, not 15.  That is, the adjustment is made twice.  This works but wastes stack space.

The code in allocate_dynamic_stack_space in explow.c has become rather convoluted and needs to be cleaned up to make this work.  E.g., it does #if defined (STACK_POINTER_OFFSET), but defaults.h ensures that STACK_POINTER_OFFSET is always defined.


---


### compiler : `gcc`
### title : `Boolean return value expression clears register too often`
### open_at : `2011-11-03T18:09:00Z`
### last_modified_date : `2022-11-26T18:26:30Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=50984
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.7.0`
### severity : `enhancement`
### contents :
Compile this code with the current HEAD gcc (or 4.5, I tried that as well) and you see less than optimal code:

int
f(int a, int b)
{
  return a & 8 && b & 4;
}

For x86-64 I see this asm code:
	xorl	%eax, %eax
	andl	$8, %edi
	je	.L2
	xorl	%eax, %eax      <----- Unnecessary !!!
	andl	$4, %esi
	setne	%al
.L2:
	rep
	ret

The compiler should realize that the second xor is unnecessary.


---


### compiler : `gcc`
### title : `[11/12/13/14 Regression] GCC performance regression (vs. 4.4/4.5), PRE/LIM increase register pressure too much`
### open_at : `2011-11-08T00:43:08Z`
### last_modified_date : `2023-07-07T10:29:38Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=51017
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.6.2`
### severity : `normal`
### contents :
GCC 4.6 happens to produce approx. 25% slower code on at least x86_64 than 4.4 and 4.5 did for John the Ripper 1.7.8's bitslice DES implementation.  To reproduce, download http://download.openwall.net/pub/projects/john/1.7.8/john-1.7.8.tar.bz2 and build it with "make linux-x86-64" (will use SSE2 intrinsics), "make linux-x86-64-avx" (will use AVX instead), or "make generic" (won't use any intrinsics).  Then run "../run/john -te=1".  With GCC 4.4 and 4.5, the "Traditional DES" benchmark reports a speed of around 2500K c/s for the "linux-x86-64" (SSE2) build on a 2.33 GHz Core 2 (this is using one core).  With 4.6, this drops to about 1850K c/s.  Similar slowdown was observed for AVX on Core i7-2600K when going from GCC 4.5.x to 4.6.x.  And it is reproducible for the without-intrinsics code as well, although that's of less practical importance (the intrinsics are so much faster).  Similar slowdown with GCC 4.6 was reported by a Mac OS X user.  It was also spotted by Phoronix in their recently published C compiler benchmarks, but misinterpreted as a GCC vs. clang difference.

Adding "-Os" to OPT_INLINE in the Makefile partially corrects the performance (to something like 2000K c/s - still 20% slower than GCC 4.4/4.5's).  Applying the OpenMP patch from http://download.openwall.net/pub/projects/john/1.7.8/john-1.7.8-omp-des-4.diff.gz and then running with OMP_NUM_THREADS=1 (for a fair comparison) corrects the performance almost fully.  Keeping the patch applied, but removing -fopenmp still keeps the performance at a good level.  So it's some change made to the source code by this patch that mitigates the GCC regression.  Similar behavior is seen with current CVS version of John the Ripper, even though it has OpenMP support for DES heavily revised and integrated into the tree.


---


### compiler : `gcc`
### title : `register allocation of SSE register in loop with across eh edges`
### open_at : `2011-11-08T22:19:05Z`
### last_modified_date : `2023-07-07T15:13:24Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=51041
### status : `NEW`
### tags : `EH, missed-optimization, ra`
### component : `rtl-optimization`
### version : `4.6.2`
### severity : `normal`
### contents :
The attached code repeatedly executes a vector * vector product to test the performance of the system. Compiled with

 g++ -Wall -O2 file.cpp

it results in a performance of about 1.7 Gflops on an Intel i5-750, ie
the output is

 adding:          0.059 s, 1.695 GFlops, sum=0.000000

However, when adding another printf (remove the comment in front of the
last printf) the performance deteriorates strongly (same compiler
options):

 adding:          0.195 s, 0.512 GFlops, sum=0.000000
 sum=0.000000

It seems the last printf confuses the compiler optimisation completely,
although it shouldn't make a difference at all, as the same variable
is already printed a few lines above.

This is worrying as it seems the compiler fails to fully optimise the
code under odd circumstances. I've used compiler version 4.6.2 as well as
4.4.1 which is the default compiler on the system.


$ gcc-4.6.2 --version
gcc-4.6.2 (GCC) 4.6.2

$ gcc --version
gcc (SUSE Linux) 4.4.1 [gcc-4_4-branch revision 150839]

$ uname -a
Linux localhost 2.6.31.14-0.8-desktop #1 SMP PREEMPT 2011-04-06 18:09:24 +0200 x86_64 x86_64 x86_64 GNU/Linux


---


### compiler : `gcc`
### title : `A regression caused by "Improve handling of conditional-branches on targets with high branch costs"`
### open_at : `2011-11-09T07:37:12Z`
### last_modified_date : `2023-08-03T05:12:55Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=51049
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.7.0`
### severity : `normal`
### contents :
int f(char *i, int j)
{
        if (*i && j!=2)
                return *i;
        else
                return j;
}

Before the check-in r180109, we have

  D.4710 = *i;
  D.4711 = D.4710 != 0;
  D.4712 = j != 2;
  D.4713 = D.4711 & D.4712;
  if (D.4713 != 0) goto <D.4714>; else goto <D.4715>;
  <D.4714>:
  D.4710 = *i;
  D.4716 = (int) D.4710;
  return D.4716;
  <D.4715>:
  D.4716 = j;
  return D.4716;

After check-in r180109, we have

  D.4711 = *i;
  if (D.4711 != 0) goto <D.4712>; else goto <D.4710>;
  <D.4712>:
  if (j != 2) goto <D.4713>; else goto <D.4710>;
  <D.4713>:
  D.4711 = *i;
  D.4714 = (int) D.4711;
  return D.4714;
  <D.4710>:
  D.4714 = j;
  return D.4714;

the code below in function fold_truth_andor makes difference,

      /* Transform (A AND-IF B) into (A AND B), or (A OR-IF B)	 into (A OR B).
	 For sequence point consistancy, we need to check for trapping,
	 and side-effects.  */
      else if (code == icode && simple_operand_p_2 (arg0)
               && simple_operand_p_2 (arg1))
         return fold_build2_loc (loc, ncode, type, arg0, arg1);

for "*i != 0" simple_operand_p(*i) returns false. Originally this is not checked by the code. 

Please refer to http://gcc.gnu.org/ml/gcc-patches/2011-10/msg02445.html for discussion details.

This change accidently made some benchmarks significantly improved due to some other reasons, but Michael gave the comments below.

======Michael's comment======

It's nice that it caused a benchmark to improve significantly, but that should be done via a proper analysis and patch, not as a side effect of a supposed non-change.

======End of Michael's comment======

The potential impact would be hurting other scenarios on performance.

The key point is for this small case I gave RHS doesn't have side effect at all, so the optimization of changing it to AND doesn't violate C specification. 

======Kai's comment======

As for the case that left-hand side has side-effects but right-hand not, we aren't allowed to do this AND/OR merge.  For example 'if ((f = foo ()) != 0 && f < 24)' we aren't allowed to make this transformation.

This shouldn't be that hard.  We need to provide to simple_operand_p_2 an additional argument for checking trapping or not.

======End of Kai's comment======

This optimization change is blocking some other optimizations I am working on in back-ends. For example, the problem I described at http://gcc.gnu.org/ml/gcc/2011-09/msg00175.html disappeared. But it is not a proper behavior.

Thanks,
-Jiangning


---


### compiler : `gcc`
### title : `SLP vectorization of dot (inner) product`
### open_at : `2011-11-09T14:44:44Z`
### last_modified_date : `2021-08-16T05:24:17Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=51062
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.0`
### severity : `enhancement`
### contents :
SLP is working nicely in 4.7
the most needed missing bit is the ability to vectorize a dot product (using for instance _mm_dp_ps for sse4)

Any chance to get this any time soon?

small test here
cat dot.cc 
struct V {
  float x,y,z,w;
};

V a;
V b;

float dot() {
  return a.x*b.x+a.y*b.y+a.z*b.z+a.w*b.w;
}

V sum() {
  V v=a;
  v.x+=b.x; v.y+=b.y; v.z+=b.z; v.w+=b.w;
  return v; 
}

c++ -Ofast -c dot.cc -march=corei7
otool -X -t -v -V dot.o | c++filt
dot():
	movss	_b+0x00000004(%rip),%xmm0
	movss	_b(%rip),%xmm1
	mulss	_a+0x00000004(%rip),%xmm0
	mulss	_a(%rip),%xmm1
	addss	%xmm1,%xmm0
	movss	_b+0x00000008(%rip),%xmm1
	mulss	_a+0x00000008(%rip),%xmm1
	addss	%xmm1,%xmm0
	movss	_b+0x0000000c(%rip),%xmm1
	mulss	_a+0x0000000c(%rip),%xmm1
	addss	%xmm1,%xmm0
	ret
	nopl	(%rax)
sum():
	movaps	_b(%rip),%xmm0
	addps	_a(%rip),%xmm0
	movaps	%xmm0,0xc8(%rsp)
	movq	0xc8(%rsp),%rax
	movaps	%xmm0,0xe8(%rsp)
	movq	_a(%rsp),%xmm1
	movd	%rax,%xmm0
	ret


---


### compiler : `gcc`
### title : `Forwarding functions can be optimized to aliases`
### open_at : `2011-11-09T16:53:02Z`
### last_modified_date : `2021-12-25T06:41:51Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=51065
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.7.0`
### severity : `enhancement`
### contents :
Given a couple of functions

void foo(int x, int y) { ... }
void bar(int x, int y) { foo(x, y}; }

we should take the opportunity, given target support and appropriate
binding of foo and bar, to optimize this to a same_body_alias rather
than merely a sibcall.


---


### compiler : `gcc`
### title : `No constant folding performed for VEC_PERM_EXPR, VEC_INTERLEAVE*EXPR, VEC_EXTRACT*EXPR`
### open_at : `2011-11-10T09:20:51Z`
### last_modified_date : `2021-07-21T02:49:51Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=51074
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.7.0`
### severity : `enhancement`
### contents :
We don't constant fold what could be constant folded, namely the above mentioned permutation trees if all the operands of them are VECTOR_CSTs:

-O2

#define vector(type, count) type __attribute__((vector_size (sizeof (type) * count)))

vector (short, 8) d;

void
foo ()
{
  vector (short, 8) a = { 0, 1, 2, 3, 4, 5, 6, 7 };
  vector (short, 8) b = { 8, 9, 10, 11, 12, 13, 14, 15 };
  vector (short, 8) c = { 0, 8, 1, 9, 2, 10, 3, 11 };
  d = __builtin_shuffle (a, b, c);
}

void
bar ()
{
  vector (short, 8) a = { 0, 1, 2, 3, 4, 5, 6, 7 };
  vector (short, 8) b = { 8, 9, 10, 11, 12, 13, 14, 15 };
  vector (short, 8) c = { 4, 12, 5, 13, 6, 14, 7, 15 };
  d = __builtin_shuffle (a, b, c);
}

or:

-O3 -fno-vect-cost-model -mavx:

char *a[1024];
extern char b[];

void
foo ()
{
  int i;
  for (i = 0; i < 1024; i += 16)
    {
      a[i] = b + 1;
      a[i + 15] = b + 2;
      a[i + 1] = b + 3;
      a[i + 14] = b + 4;
      a[i + 2] = b + 5;
      a[i + 13] = b + 6;
      a[i + 3] = b + 7;
      a[i + 12] = b + 8;
      a[i + 4] = b + 9;
      a[i + 11] = b + 10;
      a[i + 5] = b + 11;
      a[i + 10] = b + 12;
      a[i + 6] = b + 13;
      a[i + 9] = b + 14;
      a[i + 7] = b + 15;
      a[i + 8] = b + 16;
    }
}

I wonder if e.g. expand_vector_operations couldn't handle those (if all the arguments are either VECTOR_CSTs or SSA_NAMEs initialized to VECTOR_CSTs), there is of course a risk that if we create from very few VECTOR_CSTs in a loop many different VECTOR_CSTs then it increases register pressure, so perhaps we'd want to count how many VECTOR_CSTs we've created vs. how many we've got rid and allow the number to grow only by some small constant or something similar.

Plus, there is the question if the vectorizer shouldn't be aware of that too (e.g. in the second testcase the vectorizer could take it into the account when computing costs and e.g. for interleaved constant stores couldn't just do it right away.


---


### compiler : `gcc`
### title : `bounds checking not optimized to a single comparison`
### open_at : `2011-11-10T17:33:05Z`
### last_modified_date : `2021-11-27T09:59:21Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=51084
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.6.2`
### severity : `enhancement`
### contents :
Created attachment 25788
code for pure0 and pure1 is slower than for pure2 and pure3

I ran into this problem when tuning GNU Emacs; see
<http://lists.gnu.org/archive/html/emacs-devel/2011-11/msg00145.html>.
Emacs checks whether a pointer P points into an
array A by doing the equivalent of
(A <= P && P < &A[sizeof A]).  This can be
done with a subtraction followed by a single
comparison, but GCC generates slower code that does
two comparisons and a conditional branch.

The attached source code illustrates the problem.
When compiled using "gcc -O2 -S", the functions
pure0 and pure1 should generate code as fast as
that generated by pure2 and pure3.  But the slower
code is generated.


---


### compiler : `gcc`
### title : `Missed Optimization: IVOPTS don't handle unaligned memory access.`
### open_at : `2011-11-21T04:18:10Z`
### last_modified_date : `2021-08-16T23:46:45Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=51254
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.7.0`
### severity : `normal`
### contents :
IVOPTS don't handle unaligned memory access because http://gcc.gnu.org/bugzilla/show_bug.cgi?id=17949. but without this optimization, we may generate sub-optimal code.

here is a case from EEMBC autcor00:

fxpAutoCorrelation (
    e_s16 *InputData,
    e_s16 *AutoCorrData,
    e_s16 DataSize,
    e_s16 NumberOfLags,
    e_s16 Scale
)
{
    n_int i;
    n_int lag;
    n_int LastIndex;
    e_s32 Accumulator;


    for (lag = 0; lag < NumberOfLags; lag++) {
        Accumulator = 0;
        LastIndex = DataSize - lag;
        for (i = 0; i < LastIndex; i++) {
            Accumulator += ((e_s32) InputData[i] * (e_s32) InputData[i+lag]) >> Scale;
        }


        AutoCorrData[lag] = (e_s16) (Accumulator >> 16) ;
    }
}

Compile it with a arm cross-compiler
Compile flags:
-O3 -mfpu=neon -mfloat-abi=softfp 

the key vectorized loop is:

.L8:
	add	r7, ip, sl
	vldmia	ip, {d18-d19}
	vld1.16	{q8}, [r7]
	vmull.s16 q12, d18, d16
	vshl.s32	q12, q12, q11
	vmull.s16 q8, d19, d17
	add	r4, r4, #1
	vadd.i32	q10, q12, q10
	vshl.s32	q8, q8, q11
	cmp	r4, r8
	vadd.i32	q10, q8, q10
	add	ip, ip, #16
	bcc	.L8

  There are three ADD insn in it which used to calculate address and loop counter, but we can see we only need one ADD insn for calculating loop counter, other two can be optimized with address post increment operation.

  The root cause of this is because IVOPTS don't handle unaligned memory access. if we remove those check in find_interesting_uses_address, the result is:

.L8:
	vldmia	r6!, {d18-d19}
	vld1.16	{q8}, [r7]!
	vmull.s16 q12, d18, d16
	vshl.s32	q12, q12, q11
	vmull.s16 q8, d19, d17
	add	r4, r4, #1
	vadd.i32	q10, q12, q10
	vshl.s32	q8, q8, q11
	cmp	r4, sl
	vadd.i32	q10, q8, q10
	bcc	.L8

  This should be the result we want.

see http://gcc.gnu.org/ml/gcc/2011-11/msg00311.html for more details.


---


### compiler : `gcc`
### title : `CLOBBERS can be optimized if they are right before the return (or RESX)`
### open_at : `2011-11-22T23:42:06Z`
### last_modified_date : `2021-10-01T02:49:35Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=51275
### status : `NEW`
### tags : `internal-improvement, missed-optimization`
### component : `tree-optimization`
### version : `4.7.0`
### severity : `normal`
### contents :
Created attachment 25890
Patch which optimizes the clobbers

As mentioned in Bug #51264 comment #10, clobbers can be optimized but only after inlining.  I attached a patch which does the optimization in fold_all_builtins.  With this patch, most of the reason for adding -fno-exceptions to compiling GCC is gone (though inlining is still different).


---


### compiler : `gcc`
### title : `GCC fails to hoist stores in asm out of loop`
### open_at : `2011-11-23T05:07:34Z`
### last_modified_date : `2021-09-13T21:33:40Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=51281
### status : `NEW`
### tags : `inline-asm, missed-optimization`
### component : `tree-optimization`
### version : `4.7.0`
### severity : `normal`
### contents :
void foo( int *x )
{
    for(int i=0; i<100; i++) 
        asm("inc %0" :"+r"(*x));
}

This generates the following on gcc 4.5.3:

0000000000000000 <foo>:
   0:   b8 64 00 00 00          mov    eax,0x64
   5:   8b 17                   mov    edx,[rdi]
   7:   ff c2                   inc    edx
   9:   0f 1f 80 00 00 00 00    nop    dword[rax+0x0]
  10:   83 e8 01                sub    eax,0x1
  13:   89 17                   mov    [rdi],edx
  15:   75 f9                   jne    10 <foo+0x10>
  17:   f3 c3                   repz ret

And the following on gcc svn:

0000000000000000 <foo>:
   0:   b8 64 00 00 00          mov    eax,0x64
   5:   8b 17                   mov    edx,[rdi]
   7:   ff c2                   inc    edx
   9:   0f 1f 80 00 00 00 00    nop    dword[rax+0x0]
  10:   83 e8 01                sub    eax,0x1
  13:   89 17                   mov    [rdi],edx
  15:   75 f9                   jne    10 <foo+0x10>
  17:   f3 c3                   repz ret

gcc fails to hoist out the store, doing it on every loop iteration, despite being told to keep *x in a register.  This occurs in all versions of gcc, including latest svn.

This may seem like an utterly pointless test case, but this is causing significant performance degradation in actual code, where gcc repeatedly stores the outputs of inline assembly at the end of each loop iteration, instead of keeping them in registers as it should.  This causes insertion of huge numbers of redundant stores in certain cases.  I initially thought it was an aliasing issue of some sort, but this test case demonstrates that it happens even in the simplest of cases, which is rather bizarre.

Is this optimization supposed to happen, or is a missing optimization?


---


### compiler : `gcc`
### title : `Some code after SSA expand does nothing`
### open_at : `2011-12-05T23:52:42Z`
### last_modified_date : `2021-08-31T08:07:13Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=51428
### status : `ASSIGNED`
### tags : `internal-improvement, missed-optimization`
### component : `tree-optimization`
### version : `4.7.0`
### severity : `normal`
### contents :
While looking into PR 45416, I came across:
	/* Check for |= or &= of a bitfield of size one into another bitfield
	   of size 1.  In this case, (unless we need the result of the
	   assignment) we can do this more efficiently with a
	   test followed by an assignment, if necessary.

From what I am reading, this code does nothing any more as TREE_CODE (rhs) will never be BIT_IOR_EXPR or BIT_AND_EXPR.


---


### compiler : `gcc`
### title : `vectorizer does not support saturated arithmetic patterns`
### open_at : `2011-12-10T00:59:22Z`
### last_modified_date : `2021-08-25T03:54:21Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=51492
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.6.2`
### severity : `enhancement`
### contents :
Compile this code with 4.6.2 on a x86-64 machine with -O3:

#define SIZE 65536
#define WSIZE 64
unsigned short head[SIZE] __attribute__((aligned(64)));

void
f(void)
{
  for (unsigned n = 0; n < SIZE; ++n) {
    unsigned short m = head[n];
    head[n] = (unsigned short)(m >= WSIZE ? m-WSIZE : 0);
  }
}

The result I see is this:

0000000000000000 <f>:
   0:	66 0f ef d2          	pxor   %xmm2,%xmm2
   4:	b8 00 00 00 00       	mov    $0x0,%eax
			5: R_X86_64_32	head
   9:	66 0f 6f 25 00 00 00 	movdqa 0x0(%rip),%xmm4        # 11 <f+0x11>
  10:	00 
			d: R_X86_64_PC32	.LC0-0x4
  11:	66 0f 6f 1d 00 00 00 	movdqa 0x0(%rip),%xmm3        # 19 <f+0x19>
  18:	00 
			15: R_X86_64_PC32	.LC1-0x4
  19:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)
  20:	66 0f 6f 00          	movdqa (%rax),%xmm0
  24:	66 0f 6f c8          	movdqa %xmm0,%xmm1
  28:	66 0f d9 c4          	psubusw %xmm4,%xmm0
  2c:	66 0f 75 c2          	pcmpeqw %xmm2,%xmm0
  30:	66 0f fd cb          	paddw  %xmm3,%xmm1
  34:	66 0f df c1          	pandn  %xmm1,%xmm0
  38:	66 0f 7f 00          	movdqa %xmm0,(%rax)
  3c:	48 83 c0 10          	add    $0x10,%rax
  40:	48 3d 00 00 00 00    	cmp    $0x0,%rax
			42: R_X86_64_32S	head+0x20000
  46:	75 d8                	jne    20 <f+0x20>
  48:	f3 c3                	repz retq 


There is a lot of unnecessary code.  The psubusw instruction alone is sufficient.  The purpose of this instruction is to implement saturated subtraction.  Why does gcc create all this extra code?  The code should just be

   movdqa (%rax), %xmm0
   psubusw %xmm1, %xmm0
   movdqa %mm0, (%rax)

where %xmm1 has WSIZE in the 16-bit values.


---


### compiler : `gcc`
### title : `-Ofast does not vectorize while -O3 does.`
### open_at : `2011-12-10T18:13:35Z`
### last_modified_date : `2021-08-07T14:50:18Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=51499
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.6.2`
### severity : `enhancement`
### contents :
The sse vectorizer seems to miss one of the simplest cases:

#include <cstdio>
#include <cstdlib>

double loop(double a, size_t n){
   // initialise differently so compiler doesn't simplify
   double sum1=0.1, sum2=0.2, sum3=0.3, sum4=0.4, sum5=0.5, sum6=0.6;
   for(size_t i=0; i<n; i++){
      sum1+=a; sum2+=a; sum3+=a; sum4+=a; sum5+=a; sum6+=a;
   }
   return sum1+sum2+sum3+sum4+sum5+sum6-2.1-6.0*a*n;
}

int main(int argc, char** argv) {
   size_t n=1000000;
   double a=1.1;
   printf("res=%f\n", loop(a,n));
   return EXIT_SUCCESS;
}

g++-4.6.2 -Wall -O2 -ftree-vectorize -ftree-vectorizer-verbose=2 test.cpp

test.cpp:7: note: not vectorized: unsupported use in stmt.
test.cpp:4: note: vectorized 0 loops in function.

We get six addsd operations - whereas an optimisation should have
given us three addpd operations.

.L3:
	addq	$1, %rax
	addsd	%xmm0, %xmm6
	cmpq	%rdi, %rax
	addsd	%xmm0, %xmm5
	addsd	%xmm0, %xmm4
	addsd	%xmm0, %xmm3
	addsd	%xmm0, %xmm2
	addsd	%xmm0, %xmm1
	jne	.L3


---


### compiler : `gcc`
### title : `Inefficient neon intrinsic code sequence`
### open_at : `2011-12-12T07:25:34Z`
### last_modified_date : `2021-03-28T07:13:38Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=51509
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.7.0`
### severity : `normal`
### contents :
Compile the following code with options -march=armv7-a -mfloat-abi=softfp -mfpu=neon -mthumb -O2 -Wall -fpic

#include <arm_neon.h>
void simple_vld_intrin(uint8_t *src, uint8_t *dst)
{
  uint8x8x4_t x;
  uint8x8x2_t y;

  x = vld4_lane_u8(src, x, 0);

  y.val[0][0] = x.val[1][0];
 y.val[1][0] = x.val[2][0];

 vst2_lane_u8(dst, y, 0);
}

gcc 4.7 generates:


.LC0:
	.word	0
	.word	0
	.word	0
	.word	0
	.word	0
	.word	0
	.word	0
	.word	0
	.text
	.align	2
	.global	simple_vld_intrin
	.thumb
	.thumb_func
	.type	simple_vld_intrin, %function
simple_vld_intrin:
	@ args = 0, pretend = 0, frame = 32
	@ frame_needed = 0, uses_anonymous_args = 0
	@ link register save eliminated.
	ldr	r2, .L2
	sub	sp, sp, #32
.LPIC0:
	add	r2, pc
	vldmia	r2, {d18-d21}
	vmov.i32	d19, #0  @ v8qi
	vmov	d20, d19  @ v8qi
	vmov	q11, q9  @ ti
	vmov	q12, q10  @ ti
	vmov	d16, d19  @ v8qi
	vmov	d17, d19  @ v8qi
	vld4.8	{d22[0], d23[0], d24[0], d25[0]}, [r0]
	vstmia	sp, {d22-d25}
	ldrb	r2, [sp, #8]	@ zero_extendqisi2
	vmov.8	d16[0], r2
	vmov.u8	r3, d24[0]
	vmov.8	d17[0], r3
	vst2.8	{d16[0], d17[0]}, [r1]
	add	sp, sp, #32
	bx	lr
.L3:
	.align	2
.L2:
	.word	.LC0-(.LPIC0+4)


An ideal result should be:

	vld4.8	{d16[0], d17[0], d18[0], d19[0]}, [r0]
	vmov	d20, d17  @ v8qi
	vmov	d21, d18  @ v8qi
	vst2.8	{d20[0], d21[0]}, [r1]
	bx	lr


---


### compiler : `gcc`
### title : `Only partially optimizes away __builtin_unreachable switch default case`
### open_at : `2011-12-12T10:53:44Z`
### last_modified_date : `2020-04-17T18:31:42Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=51513
### status : `REOPENED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.6.2`
### severity : `enhancement`
### contents :
Hi,

I have code that looks like this:

pannekake:~> cat test.c
void foo();
void bar();
void baz();

void func(int i)
{
	switch (i) {
		case 0: foo(); break;
		case 1: bar(); break;
		case 2: baz(); break;
		case 3: baz(); break;
		case 4: bar(); break;
		case 5: foo(); break;
		case 6: foo(); break;
		case 7: bar(); break;
		case 8: baz(); break;
		case 9: baz(); break;
		case 10: bar(); break;
		default: __builtin_unreachable(); break;
	}
}

Compiling this yields:

pannekake:~> gcc-4.6 -O2 -c test.c && objdump --disassemble test.o
             
test.o:     file format elf64-x86-64


Disassembly of section .text:

0000000000000000 <func>:
   0:	83 ff 0a             	cmp    $0xa,%edi
   3:	76 03                	jbe    8 <func+0x8>
   5:	0f 1f 00             	nopl   (%rax)
   8:	89 ff                	mov    %edi,%edi
   a:	31 c0                	xor    %eax,%eax
   c:	ff 24 fd 00 00 00 00 	jmpq   *0x0(,%rdi,8)
  13:	0f 1f 44 00 00       	nopl   0x0(%rax,%rax,1)
  18:	e9 00 00 00 00       	jmpq   1d <func+0x1d>
  1d:	0f 1f 00             	nopl   (%rax)
  20:	e9 00 00 00 00       	jmpq   25 <func+0x25>
  25:	0f 1f 00             	nopl   (%rax)
  28:	e9 00 00 00 00       	jmpq   2d <func+0x2d>

The first compare is, as you can see, unneeded; the code for the default case itself (a repz ret) has been optimized away due to the __builtin_unreachable(), but the compare and branch remains.

I've also seen it sometimes be able to remove the jump instruction itself, but not the compare.


---


### compiler : `gcc`
### title : `No named return value optimization while adding a dummy scope`
### open_at : `2011-12-15T16:39:05Z`
### last_modified_date : `2023-10-17T10:29:23Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=51571
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `c++`
### version : `4.6.1`
### severity : `normal`
### contents :
Simple code snippet

#include <iostream>
int global;
struct A
{
   A(){}
   A(const A&x){
       ++global;
   }
   ~A(){}
};
A foo()
{  
     A a;
     return a;  
}
int main()
{
   A x = foo();
   std::cout << global;
}
Output : 0
 
When the definition of foo is changed to

A foo()
{ 
  { 
     A a;
     return a;  
  }
}
I get 1 as the output i.e copy c-tor gets called once.

Compiler is not optimizing the call to the copy c-tor in this case.


---


### compiler : `gcc`
### title : `armv7 target is not using unaligned access to packed fields sometimes (halfwords, loads?)`
### open_at : `2011-12-30T02:14:21Z`
### last_modified_date : `2023-02-25T06:49:38Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=51709
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.7.0`
### severity : `enhancement`
### contents :
armv7 target is not always producing unaligned access to packed fields using the appropriate half and full word instructions.  Rather sometimes it uses bytes accesses with shifts and or's.

Below is a program which produces the problem:

typedef unsigned char  uint8;
typedef unsigned short uint16;
typedef unsigned int uint32;

#define HALFWORD 1
#define ADD_BYTE 0
#define PACKED 1

#if HALFWORD
#define FIELD_T uint16
#else
#define FIELD_T uint32
#endif

#if PACKED
#define PACKED_ATTRIBUTE __attribute__ ((packed))
#else
#define PACKED_ATTRIBUTE
#endif

typedef struct PACKED_ATTRIBUTE {
#if ADD_BYTE
        uint8  field0;
#endif
        FIELD_T field1;
        FIELD_T field2;
} packed_struct_t;

typedef struct {
#if ADD_BYTE
        uint8  field0;
#endif
        FIELD_T field1;
        FIELD_T field2;
} natural_struct_t;

void
test_function(natural_struct_t *natural, packed_struct_t *packed)
{
        natural->field1 = packed->field1;
        packed->field2 = natural->field2;
}

This produces

test_function:
        @ args = 0, pretend = 0, frame = 0
        @ frame_needed = 0, uses_anonymous_args = 0
        @ link register save eliminated.
        ldrb    r3, [r1, #1]    @ zero_extendqisi2      @ tmp141,
        ldrb    ip, [r1, #0]    @ zero_extendqisi2      @ tmp140,* packed
        orr     r2, ip, r3, lsl #8      @, tmp143, tmp140, tmp141,
        ldrh    r3, [r0, #2]    @, natural_3(D)->field2
        strh    r2, [r0, #0]    @ movhi @ tmp143, natural_3(D)->field1
        strh    r3, [r1, #2]    @ unaligned     @ natural_3(D)->field2,
        bx      lr      @
        .size   test_function, .-test_function
        .ident  "GCC: (Sourcery CodeBench Lite 2011.09-69) 4.6.1"

The load from the packed structure is decomposed to byte accesses but note the stores are not.  Also if you try full words by changing the define HALFWORD the generated code is as expected.  Adding a byte to the beginning of the packed and natural structure by changing the define ADD_BYTE doesn't change the results.  It appears to only be the half word load that is having the problem.  

Note in the above assembly output, that the @unaligned is missing from the load though present on the store.  If you look at the assembly for the full word compile, the @unaligned is present on both the load and store.

I claim this is a sometimes result because I have looked at cases in my more complicated source and I can see that sometimes packed half word loads do not use byte accesses.


---


### compiler : `gcc`
### title : `Missed optimization for ==/!= comparison`
### open_at : `2012-01-07T10:46:18Z`
### last_modified_date : `2021-08-15T22:16:42Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=51780
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.7.0`
### severity : `enhancement`
### contents :
Hi,

optimization misses to eliminate addition for 'b' in following code:

extern unsigned int ar[256];

int foo (int a, unsigned int b)
{
  int c = ar[a] + b;
  int d = (int) b;
  return c != d;
}

compiled this code with -O2 we get tree-optimized as follwing:

;; Function foo (foo, funcdef_no=0, decl_uid=1600, cgraph_uid=0)

foo (int a, unsigned int b)
{
  int d;
  int c;
  _Bool D.2717;
  int D.2716;
  unsigned int D.2715;
  unsigned int D.2714;

<bb 2>:
  D.2714_2 = ar[a_1(D)];
  D.2715_4 = D.2714_2 + b_3(D);
  c_5 = (int) D.2715_4;
  d_6 = (int) b_3(D);
  D.2717_7 = c_5 != d_6;
  D.2716_8 = (int) D.2717_7;

<L0>:
  return D.2716_8;

}

but optimized variant should be:

;; Function foo (foo, funcdef_no=0, decl_uid=1709, cgraph_uid=0)

foo (int a, unsigned int b)
{
  _Bool D.1717;
  int D.1716;
  unsigned int D.1714;

<bb 2>:
  D.1714_2 = ar[a_1(D)];
  D.1717_7 = D.1714_2 != 0;
  D.1716_8 = (int) D.1717_7;
  return D.1716_8;

}


---


### compiler : `gcc`
### title : `Missed optimization for ==/!= comparison type-sinking`
### open_at : `2012-01-07T10:59:44Z`
### last_modified_date : `2023-05-15T04:09:08Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=51781
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.7.0`
### severity : `enhancement`
### contents :
The following code shows an issue about missed optimization for ==/!= comparisons.

extern unsigned char ar[256];

int foo (int x, int y)
{
  int i = (int) ar[x];
  return (i == (y & 0xff));
}

Compiled with 4.7 using -O2 we get the following optimized tree:

;; Function foo (foo, funcdef_no=0, decl_uid=1600, cgraph_uid=0)

foo (int x, int y)
{
  int i;
  _Bool D.2716;
  int D.2715;
  int D.2714;
  unsigned char D.2713;

<bb 2>:
  D.2713_2 = ar[x_1(D)];
  i_3 = (int) D.2713_2;
  D.2715_5 = y_4(D) & 255;
  D.2716_6 = D.2715_5 == i_3;
  D.2714_7 = (int) D.2716_6;
  return D.2714_7;

}

But to be expected would be:

;; Function foo (foo, funcdef_no=0, decl_uid=1709, cgraph_uid=0)

foo (int x, int y)
{
  unsigned char D.1719;
  _Bool D.1716;
  int D.1714;
  unsigned char D.1713;

<bb 2>:
  D.1713_2 = ar[x_1(D)];
  D.1719_9 = (unsigned char) y_4(D);
  D.1716_6 = D.1713_2 == D.1719_9;
  D.1714_7 = (int) D.1716_6;
  return D.1714_7;

}


---


### compiler : `gcc`
### title : `Missed optimization for X ==/!= (signed type) ((unsigned type) Y + Z)`
### open_at : `2012-01-07T12:09:12Z`
### last_modified_date : `2021-07-19T04:23:18Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=51783
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.7.0`
### severity : `normal`
### contents :
Hi,

for the following example shows the missed optimization

extern int ar[256];

int foo (int x, int y, unsigned int z)
{
  int c = (int) ((unsigned int) x + z);
  return y == c;
}

We produce in 4.7 for -O2 the following optimized gimple tree:

;; Function foo (foo, funcdef_no=0, decl_uid=1601, cgraph_uid=0)

foo (int x, int y, unsigned int z)
{
  int c;
  _Bool D.2717;
  int D.2716;
  unsigned int D.2715;
  unsigned int x.0;

<bb 2>:
  x.0_2 = (unsigned int) x_1(D);
  D.2715_4 = z_3(D) + x.0_2;
  c_5 = (int) D.2715_4;
  D.2717_7 = y_6(D) == c_5;
  D.2716_8 = (int) D.2717_7;
  return D.2716_8;

}

But we could expect in this case:

;; Function foo (foo, funcdef_no=0, decl_uid=1710, cgraph_uid=0)

foo (int x, int y, unsigned int z)
{
  int D.1720;
  int c;
  _Bool D.1717;
  int D.1716;

<bb 2>:
  D.1720_10 = (int) z_3(D);
  c_5 = x_1(D) + D.1720_10;
  D.1717_7 = y_6(D) == c_5;
  D.1716_8 = (int) D.1717_7;
  return D.1716_8;

}


---


### compiler : `gcc`
### title : `Arm backend missed the mls related optimization`
### open_at : `2012-01-09T08:45:16Z`
### last_modified_date : `2021-03-20T22:38:26Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=51797
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.7.0`
### severity : `enhancement`
### contents :
compile the following code with options -march=armv7-a -mthumb -Os


int t0i(int a, int b)
{
  return a - 368 * b;
}

GCC 4.7 generates:

t0i:
	ldr	r3, .L2
	mla	r0, r3, r1, r0
	bx	lr
.L3:
	.align	2
.L2:
	.word	-368


When compiled with -O3, gcc generates:

t0i:
	movw	r3, #65168
	movt	r3, 65535
	mla	r0, r3, r1, r0
	bx	lr


But an optimized result should be:

t0i:
     movw r3, 368
     mls  r0, r3, r1, r0
     bx   lr

It is faster and smaller than either of Os/O3 result.


---


### compiler : `gcc`
### title : `Use of result from 64*64->128 bit multiply via __uint128_t not optimized`
### open_at : `2012-01-12T19:23:24Z`
### last_modified_date : `2022-01-09T00:53:21Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=51837
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `target`
### version : `4.7.0`
### severity : `enhancement`
### contents :
unsigned long long foo(unsigned long long x, unsigned long long y)
{
	__uint128_t z = (__uint128_t)x * y;
	return z ^ (z >> 64);
}

Compiles into

mov    %rsi, %rax
mul    %rdi
mov    %rax, %r9
mov    %rdx, %rax
xor    %r9, %rax
retq

The final two mov instructions are not needed, and the above is equivalent to

mov    %rsi, %rax
mul    %rdi
xor    %rdx, %rax
retq


---


### compiler : `gcc`
### title : `Inefficient add of 128 bit quantity represented as 64 bit tuple to 128 bit integer.`
### open_at : `2012-01-12T19:29:40Z`
### last_modified_date : `2021-08-30T06:33:52Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=51838
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.7.0`
### severity : `enhancement`
### contents :
void foo(__uint128_t *x, unsigned long long y, unsigned long long z)
{
	*x += y + ((__uint128_t) z << 64);
}

Compiles into:

mov    %rdx,%r8
mov    %rsi,%rax
xor    %edx,%edx
add    (%rdi),%rax
mov    %rdi,%rcx
adc    0x8(%rdi),%rdx
xor    %esi,%esi
add    %rsi,%rax
adc    %r8,%rdx
mov    %rax,(%rcx)
mov    %rdx,0x8(%rcx)
retq 

The above can be optimized into:

add    %rsi, (%rdi)
adc    %rdx, 8(%rdi)
retq


---


### compiler : `gcc`
### title : `GCC not generating adc instruction for canonical multi-precision add sequence`
### open_at : `2012-01-12T19:35:38Z`
### last_modified_date : `2021-08-07T17:57:47Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=51839
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.7.0`
### severity : `enhancement`
### contents :
The multi-precision add

void foo(unsigned long long *x, unsigned long long y, unsigned long long z)
{
	x[0] += y;
	x[1] += z + (x[0] < y);
}

compiles into:

mov    %rsi,%rax
add    (%rdi),%rax
add    0x8(%rdi),%rdx
cmp    %rax,%rsi
mov    %rax,(%rdi)
seta   %al
movzbl %al,%eax
add    %rax,%rdx
mov    %rdx,0x8(%rdi)
retq

Instead, gcc could use the adc instruction, yielding the wanted:

add    %rsi, (%rdi)
adc    %rdx, 8(%rdi)
retq


---


### compiler : `gcc`
### title : `GCC generates inconsistent code for same sources calling builtin calls, like sqrtf`
### open_at : `2012-01-16T10:11:50Z`
### last_modified_date : `2022-01-06T03:42:00Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=51867
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.7.0`
### severity : `trivial`
### contents :
compile following program:
----------------------------------------------
#include <math.h>
int a(float x) {
     return sqrtf(x);
}
int b(float x) {
     return sqrtf(x);
}

With command:
arm-none-eabi-gcc -mthumb -mhard-float -mfpu=fpv4-sp-d16
-mcpu=cortex-m4 -O0 -S a.c -o a.S

The generated assembly codes is like:
----------------------------------------------
a:
       @ args = 0, pretend = 0, frame = 8
       @ frame_needed = 1, uses_anonymous_args = 0
       push    {r7, lr}
       sub     sp, sp, #8
       add     r7, sp, #0
       fsts    s0, [r7, #4]
       flds    s15, [r7, #4]
       fsqrts  s15, s15
       fcmps   s15, s15
       fmstat
       beq     .L2
       flds    s0, [r7, #4]
       bl      sqrtf
       fcpys   s15, s0
.L2:
       ftosizs s15, s15
       fmrs    r3, s15 @ int
       mov     r0, r3
       add     r7, r7, #8
       mov     sp, r7
       pop     {r7, pc}
       .size   a, .-a
       .align  2
       .global b
       .thumb
       .thumb_func
       .type   b, %function
b:
       @ args = 0, pretend = 0, frame = 8
       @ frame_needed = 1, uses_anonymous_args = 0
       push    {r7, lr}
       sub     sp, sp, #8
       add     r7, sp, #0
       fsts    s0, [r7, #4]
       flds    s0, [r7, #4]
       bl      sqrtf
       fcpys   s15, s0
       ftosizs s15, s15
       fmrs    r3, s15 @ int
       mov     r0, r3
       add     r7, r7, #8
       mov     sp, r7
       pop     {r7, pc}
       .size   b, .-b

The problem exists on trunk and triggered only by O0 optimization.
The problem stands for x86 target too.


---


### compiler : `gcc`
### title : `__int128_t (and long long on x86) negation can be optimized`
### open_at : `2012-01-22T23:55:42Z`
### last_modified_date : `2022-04-29T11:33:44Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=51954
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.7.0`
### severity : `enhancement`
### contents :
__int128_t neg(__int128_t x)
{
	return -x;
}

Compiles into with -O3 :

mov    %rdi, %rax
mov    %rsi, %rdx
neg    %rax
adc    $0x0, %rdx
neg    %rdx
retq

Note how the last three instructions before the return are dependent on each other.  This can be  slightly improved with slightly more inter-instruction parallelism:

mov    %rdi, %rax
mov    %rsi, %rdx
neg    %rdx
neg    %rax
sbb    $0x0, %rdx
retq


---


### compiler : `gcc`
### title : `Missed tail merging opportunity`
### open_at : `2012-01-23T13:32:09Z`
### last_modified_date : `2023-06-09T14:50:37Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=51964
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.7.0`
### severity : `enhancement`
### contents :
pr51879-5.c:
...
int bar (int);
void baz (int);
void foo2 (void);
void
foo (int y, int z)
{
  int a;
  if (y == 6)
    {
      if (z)
	foo2 ();
      a = bar (7);
    }
  else
    a = bar (7);
  baz (a);
}
...

compile:
...
gcc -O2 pr51879-5.c -S -fdump-tree-all-all
...

pr51879-5.c.094t.pre:
...
  # BLOCK 5 freq:4877
  # PRED: 8 [100.0%]  (fallthru) 4 [100.0%]  (fallthru,exec)
  # .MEMD.1719_6 = PHI <.MEMD.1719_8(D)(8), .MEMD.1719_9(4)>
  # .MEMD.1719_10 = VDEF <.MEMD.1719_6>
  # USE = nonlocal 
  # CLB = nonlocal 
  aD.1712_4 = barD.1703 (7);
  goto <bb 7>;
  # SUCC: 7 [100.0%]  (fallthru,exec)

  # BLOCK 6 freq:5123
  # PRED: 2 [51.2%]  (false,exec)
  # .MEMD.1719_11 = VDEF <.MEMD.1719_8(D)>
  # USE = nonlocal 
  # CLB = nonlocal 
  aD.1712_5 = barD.1703 (7);
  # SUCC: 7 [100.0%]  (fallthru,exec)

  # BLOCK 7 freq:10000
  # PRED: 5 [100.0%]  (fallthru,exec) 6 [100.0%]  (fallthru,exec)
  # aD.1712_1 = PHI <aD.1712_4(5), aD.1712_5(6)>
  # .MEMD.1719_7 = PHI <.MEMD.1719_10(5), .MEMD.1719_11(6)>
  # .MEMD.1719_12 = VDEF <.MEMD.1719_7>
  # USE = nonlocal 
  # CLB = nonlocal 
  bazD.1705 (aD.1712_1);
  # VUSE <.MEMD.1719_12>
  return;
  # SUCC: EXIT [100.0%] 
...

Blocks 5 and 6 are not merged by tail_merge_optimize (they are merged by rtl cross-jumping though).

The reason the blocks are not merged by tail_merge_optimize is that tail_merge_optimize uses value numbering to determine equivalence of blocks.
And since the calls have a different vuse (.MEMD.1719_6 and .MEMD.1719_8(D)) the results of the calls won't have the same value number (even after fixing PR51879).

However, the reason we can merge the calls is not because the calls have the same result. It's because the results are used in the same way. To detect this we should use a different comparison mechanism than the current.


---


### compiler : `gcc`
### title : `Shrink-wrapping opportunity`
### open_at : `2012-01-24T18:48:18Z`
### last_modified_date : `2023-10-03T10:29:17Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=51982
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.7.0`
### severity : `enhancement`
### contents :
Created attachment 26444
lookdict_string manually split equivalent to shrink-wrapping

I realize that the shrink-wrapping implementation in GCC is preliminary and conservative. I tested it on an example that presents a good opportunity for shrink-wrapping and a large perforamnce improvement, but the current implementation was not able to apply the optimization.

The attached file manually splits the CPython lookdict_string() into two functions where most of the prologue can be avoided on the slow path.


---


### compiler : `gcc`
### title : `cross-jumping drops MEM attributes even when it makes no changes to the code`
### open_at : `2012-01-25T19:17:48Z`
### last_modified_date : `2021-12-18T23:15:25Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=52000
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.7.0`
### severity : `enhancement`
### contents :
flow_find_cross_jump calls merge_memattrs for each pair of
instructions that it was thinking of merging, regardless of
whether the merge takes place.  This can cause mem attributes
to be dropped unnecessarily.  See:

    http://gcc.gnu.org/ml/gcc/2012-01/msg00015.html

for more discussion and context.


---


### compiler : `gcc`
### title : `__builtin_copysign optimization suboptimal`
### open_at : `2012-01-29T00:16:27Z`
### last_modified_date : `2023-09-21T14:04:53Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=52034
### status : `RESOLVED`
### tags : `missed-optimization, ra`
### component : `target`
### version : `4.6.2`
### severity : `enhancement`
### contents :
The most trivial __builtin_copysign optimization is not optimal:

double f(double a, double b)
{
  return __builtin_copysign(a,b);
}

With gcc 4.6.2 this gets compiled to

	movapd	%xmm1, %xmm2
	andpd	.LC0(%rip), %xmm0
	andpd	.LC1(%rip), %xmm2
	orpd	%xmm2, %xmm0
	ret

There is no reason for %xmm1 to be duplicated to %xmm2.  This is sufficient:

	andpd	.LC0(%rip), %xmm0
	andpd	.LC1(%rip), %xmm1
	orpd	%xmm1, %xmm0
	ret

The same happens with more complicated code sequences.


---


### compiler : `gcc`
### title : `Value-numbering does not enter translated expressions into the hash table`
### open_at : `2012-01-30T14:35:57Z`
### last_modified_date : `2021-07-30T05:05:37Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=52054
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.7.0`
### severity : `normal`
### contents :
When VN comes across

foo (struct S * p)
{
  struct S s;
  int D.1715;
  int D.1712;
  int D.1711;

<bb 2>:
  s = *p_2(D);
  D.1711_3 = s.i;
  D.1712_4 = p_2(D)->i;
  if (D.1711_3 != D.1712_4)

it does not enter p_2(D)->i valued D.1711_3 into the hashtables when
visiting D.1711_3 = s.i but only s.i valued D.1711_3.  It either should
insert both or the most translated expression (or even all the exprs
generated inbetween?  All but the most translated expressions are
compile-time savers only).

This way it can value-number D.1711_3 and D.1712_4 the same.

struct S { int i; int j; };
int foo (struct S *p)
{
  struct S s = *p;
  if (s.i != p->i)
    return 1;
  return 0;
}

see gnat.dg/pack9.ads for an Ada testcase that fails this way w/o SRA.


---


### compiler : `gcc`
### title : `load of 64-bit pointer reads 64 bits even when only 32 are used`
### open_at : `2012-01-30T18:51:52Z`
### last_modified_date : `2021-07-26T20:41:20Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=52055
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.6.1`
### severity : `enhancement`
### contents :
The following test program:

#include <stdint.h>
uint32_t rd32(uint64_t *i) { return *i; }

Compiles to this (-O3 -fomit-frame-pointer):

0000000000000000 <rd32>:
   0:	48 8b 07             	mov    rax,QWORD PTR [rdi]
   3:	c3                   	ret    

But Clang compiles to this, which seems correct, is one byte shorter and touches less memory:

0000000000000000 <rd32>:
   0:	8b 07                	mov    eax,DWORD PTR [rdi]
   2:	c3                   	ret


---


### compiler : `gcc`
### title : `missing integer comparison optimization`
### open_at : `2012-01-31T19:39:49Z`
### last_modified_date : `2023-07-01T11:21:01Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=52070
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.6.2`
### severity : `enhancement`
### contents :
Compile this code with gcc 4.6.2:

#include <stddef.h>
size_t b;
int f(size_t a)
{
  return b == 0 || a < b;
}

For x86-64 I see this result:

f:	movq	b(%rip), %rdx
	movl	$1, %eax
	testq	%rdx, %rdx
	je	.L2
	xorl	%eax, %eax
	cmpq	%rdi, %rdx
	seta	%al
.L2:	rep ret

This can be more done without a conditional jump:

f:	movq	b(%rip), %rdx
	xorl	%eax, %eax
	subq	$1, %rdx
	cmpq	%rdi, %rdx
	setae	%al
	rep ret

Unless the b==0 test is marked as likely I'd say this code is performing better on all architectures.


---


### compiler : `gcc`
### title : `Memory loads not rematerialized`
### open_at : `2012-02-01T10:30:28Z`
### last_modified_date : `2021-09-12T08:19:55Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=52082
### status : `NEW`
### tags : `missed-optimization, ra`
### component : `rtl-optimization`
### version : `4.7.0`
### severity : `enhancement`
### contents :
On the following testcase at -O2 (distilled from genautomata.c):

struct S { unsigned long *s1; struct S *s2; };
int v1 __attribute__((visibility ("hidden")));
struct T
{
  int a, b, c;
} *v2 __attribute__((visibility ("hidden")));
struct S **v3 __attribute__((visibility ("hidden")));
struct S **v4 __attribute__((visibility ("hidden")));

int __attribute__((noinline, noclone))
foo (unsigned long *x, unsigned long *y, int z)
{
  int j, k, l;
  unsigned int i;
  struct S *m;

  for (j = 0; j < v1; j++)
    if (y[j])
      for (i = 0; i < 8 * sizeof (unsigned long); i++)
  if ((y[j] >> i) & 1)
    {
      k = j * 8 * sizeof (unsigned long) + i;
      if (k >= v2->c)
        break;
      for (m = (z ? v4 [k] : v3 [k]); m != ((void *)0); m = m->s2)
        {
          for (l = 0; l < v1; l++)
            if ((x [l] & m->s1 [l]) != m->s1 [l] && m->s1 [l])
              break;
          if (l >= v1)
            return 0;
        }
    }
  return 1;
}

tree LIM moves the loads from v2/v3/v4 before the loop, but unfortunately the register pressure is high and the pseudos holding the v3/v4 pointers don't get a a hard register and are immediately spilled to the stack.  I wonder whether we couldn't instead just rematerialize them and put the original MEM loads into the loop (assuming they don't alias with anything on the way, but that must be the case here when LIM moved them there first, after all this loop doesn't have any MEM stores at all).


---


### compiler : `gcc`
### title : `Missing FRE because of sign change`
### open_at : `2012-02-07T20:24:17Z`
### last_modified_date : `2021-12-28T19:35:59Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=52157
### status : `NEW`
### tags : `missed-optimization, TREE`
### component : `tree-optimization`
### version : `4.7.0`
### severity : `enhancement`
### contents :
Take:
int f(int a)
{
  unsigned int t = a;
  t-=100;
  if (t <= 200 )
    return a-100;
  else
    return t;
}
--- CUT ---
We should able to simplify this function just to:
int f(int a)
{
  unsigned int t = a;
  t-=100;
  return t;
}


---


### compiler : `gcc`
### title : `memcmp/strcmp/strncmp can be optimized when the result is tested for [in]equality with 0`
### open_at : `2012-02-08T12:37:44Z`
### last_modified_date : `2022-05-24T13:32:51Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=52171
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.7.0`
### severity : `enhancement`
### contents :
On GIMPLE we should expand memcmp/strcmp/strncmp to inline integral compares
if the result is only tested against equality with 0.

See PR43052 where we hint at that these may be the only profitable cases
to inline for memcmp at least.


---


### compiler : `gcc`
### title : `An opportunity for x86 gcc vectorizer (gain up to 3 times)`
### open_at : `2012-02-14T22:41:45Z`
### last_modified_date : `2023-08-31T07:07:48Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=52252
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.7.0`
### severity : `enhancement`
### contents :
This is an example of byte conversion from RGB (Red Green Blue) to CMYK (Cyan Magenta Yellow blacK):

#define byte unsigned char
#define MIN(a, b) ((a) > (b)?(b):(a))

void convert_image(byte *in, byte *out, int size) {
    int i;
    for(i = 0; i < size; i++) {
        byte r = in[0];
        byte g = in[1];
        byte b = in[2];
        byte c, m, y, k, tmp;
        c = 255 - r;
        m = 255 - g;
        y = 255 - b;
        tmp = MIN(m, y);
        k = MIN(c, tmp);
        out[0] = c - k;
        out[1] = m - k;
        out[2] = y - k;
        out[3] = k;
        in += 3;
        out += 4;
    }
}

Here trunk gcc for Arm unrolls the loop by 2 and vectorizes it using neon; gcc for x86 does not vectorize it.

There are 2  tricky moments in this loop:
1)	It converts 3 bytes into 4
2)	We need to shuffle bytes after load:
Let 0123456789ABCDF be 16 bytes in “in” array (first rgb is 012, next 345…)
To count vector minimum we need to place 0,1,2 bytes into 3 different vectors.

Gcc for Arm does this by 2 special loads:
  vld3.8  {d16, d18, d20}, [r2]!
  vld3.8  {d17, d19, d21}, [r2]
putting 0 and 3 bytes into q8(d16, d17)
        1 and 4 bytes into q9(d18, d19)
        2 and 5 bytes into q10(d20, d21)

And after all vector transformations it stores by 2 special stores:

  vst4.8  {d8, d10, d12, d14}, [r3]!
  vst4.8  {d9, d11, d13, d15}, [r3]

However x86 gcc can do the same loads:
  movq (%edi),%mm5
  movq %mm5,%mm7
  movq %mm5,%mm6
  pshufb %mm3,%mm5 /*0x00ffffff03ffffff*/
  pshufb %mm2,%mm6 /*0x01ffffff04ffffff*/
  pshufb %mm1,%mm7 /*0x02ffffff05ffffff*/
  /* %mm5 – r, %mm6 – g, %mm7 – b */

And same stores:
  pslld  $0x8,%mm6
  pslld  $0x10,%mm7
  pslld  $0x18,%mm4
  pxor   %mm5,%mm6 
  pxor   %mm7,%mm4
  pxor   %mm6,%mm4
  pshufb %mm0,%mm4 /*0x000102030405060708*/ /*here redundant*/
  movq %mm4,(%esi)
  /* %mm5 – c, %mm6 – m, %mm7 – y, %mm4 - k */

pshufb here does not do anything, so could be removed, only in case we store less than 4 bytes we will need to shuffle them

Moreover x86 gcc can do unroll not only by 2, but by 4:
With the following loads:

  movdqu (%edi),%xmm5
  movdqa %xmm5,%xmm7
  movdqa %xmm5,%xmm6
  pshufb %xmm3,%xmm5 /*0x00ffffff03ffffff06ffffff09ffffff*/
  pshufb %xmm2,%xmm6 /*0x01ffffff04ffffff07ffffff0affffff*/
  pshufb %xmm1,%xmm7 /*0x02ffffff05ffffff08ffffff0bffffff*/
  /* %xmm5 – r, %xmm6 – g, %xmm7 – b */

And stores:
  pslld  $0x8,%xmm6
  pslld  $0x10,%xmm7
  pslld  $0x18,%xmm4
  pxor   %xmm5,%xmm6
  pxor   %xmm7,%xmm4
  pxor   %xmm6,%xmm4
  pshufb %xmm0,%xmm4 /*0x000102030405060708090a0b0c0d0e0f*/ /*here redundant*/
  movdqa %xmm4,(%esi)
  /* %xmm5 – c, %xmm6 – m, %xmm7 – y, %xmm4 - k */


---


### compiler : `gcc`
### title : `VRP does not fold (~a) & N to a ^ N if a has range [0, N]`
### open_at : `2012-02-15T00:21:43Z`
### last_modified_date : `2021-06-03T00:40:58Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=52254
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.7.0`
### severity : `enhancement`
### contents :
While working on moving fold-const.c bit expression optimizations to a SSA based optimization, I found that if we optimize (a^N)&N to ~a & N, VRP does not change that to just a ^ N.
Simple example:
/* { dg-do compile } */
/* { dg-options "-O2 -fno-tree-ccp -fdump-tree-vrp1" } */

int f(int x)
{
  if (x >= 0 && x <= 3)
    {
      x = (x ^ 3) & 3;
    }
  return x;
}

/* { dg-final { scan-tree-dump-times " & 3;" 0 "vrp1" { xfail *-*-* } } } */
/* { dg-final { cleanup-tree-dump "vrp1" } } */


---


### compiler : `gcc`
### title : `native tls support should be added for darwin11`
### open_at : `2012-02-16T03:51:56Z`
### last_modified_date : `2022-05-24T13:51:12Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=52268
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.7.0`
### severity : `enhancement`
### contents :
The clang compiler in clang 3.0 and Xcode 4.2 currently provides tis support on darwin11. This same ability to generate the required tis assembly for darwin11 should be added to FSF gcc.


---


### compiler : `gcc`
### title : `[11/12/13/14 Regression] libgcrypt _gcry_burn_stack slowdown`
### open_at : `2012-02-16T18:22:40Z`
### last_modified_date : `2023-07-07T10:29:42Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=52285
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.7.0`
### severity : `normal`
### contents :
#define wipememory2(_ptr,_set,_len) do { \
              volatile char *_vptr=(volatile char *)(_ptr); \
              unsigned long _vlen=(_len); \
              while(_vlen) { *_vptr=(_set); _vptr++; _vlen--; } \
                  } while(0)
#define wipememory(_ptr,_len) wipememory2(_ptr,0,_len)

__attribute__((noinline, noclone)) void
_gcry_burn_stack (int bytes)
{
  char buf[64];
    
    wipememory (buf, sizeof buf);
    bytes -= sizeof buf;
    if (bytes > 0)
        _gcry_burn_stack (bytes);
}

is one of the hot parts of gcrypt camellia256 ECB benchmark which apparently slowed down in 4.7 compared to 4.6.  The routine is called many times, usually with bytes equal to 372.

The above first slowed down the whole benchmark from ~ 2040ms to ~ 2400ms (-O2 -march=corei7-avx -fPIC) in http://gcc.gnu.org/viewcvs?root=gcc&view=rev&rev=178104
and then (somewhat surprisingly) became tiny bit faster again with
http://gcc.gnu.org/viewcvs?root=gcc&view=rev&rev=181172 , which no longer tail recursion optimizes the function (in this case suprisingly a win, but generally IMHO a mistake).


---


### compiler : `gcc`
### title : `shorter abs thumb2 code sequences`
### open_at : `2012-02-22T08:20:32Z`
### last_modified_date : `2021-09-12T06:05:59Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=52338
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.7.0`
### severity : `enhancement`
### contents :
Compile the following code with options -march=armv7-a -mthumb -Os


char placex[] = {1, 2, 3, 4};
char placey[] = {5, 6, 7, 8};

int t0k(int b, int w)
{
   int h1 = placex[b] - placex[w];
   int h2 = placey[b] - placey[w];
   if (h1 < 0) h1 = -h1;
   if (h2 < 0) h2 = -h2;
   return h1 + h2;
}


GCC 4.7 generates:


t0k:
	ldr	r3, .L2
	push	{r4, lr}
	ldrb	r4, [r3, r0]	@ zero_extendqisi2
	adds	r0, r3, r0
	ldrb	r2, [r3, r1]	@ zero_extendqisi2
	adds	r3, r3, r1
	ldrb	r0, [r0, #4]	@ zero_extendqisi2
	ldrb	r3, [r3, #4]	@ zero_extendqisi2
	subs	r2, r4, r2
	subs	r3, r0, r3
	eor	r0, r2, r2, asr #31    //  abs(h1)
	sub	r0, r0, r2, asr #31    //  abs(h1)
	cmp	r3, #0                 //  abs(h2)
	it	lt                     //  abs(h2)
	rsblt	r3, r3, #0             //  abs(h2)
	adds	r0, r0, r3
	pop	{r4, pc}


It's interesting that gcc generats two different code sequence for abs(h1) and abs(h2).

After carefully studying the insn pattern "*thumb2_abssi2", I got the impression that the selection of code sequence is depends on if the result register is same as source register. If they are same, the cmp code sequence is used, otherwise the pure arithmetic code sequence is used.

But the cmp code sequence can also be used when the source is not the same as target register, and may result in smaller code size, like in this case.

Another question is there any performance differences between these two different code sequences?


---


### compiler : `gcc`
### title : `Missed optimization dealing with bools`
### open_at : `2012-02-22T21:43:58Z`
### last_modified_date : `2023-09-17T01:49:23Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=52345
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.7.0`
### severity : `enhancement`
### contents :
Take the following three functions:
int f(int a, int b)
{
  int c = a != 0;
  int d = (c!=0|b!=0);
  return d;
}

int f1(int a, int b)
{
  int c = a != 0;
  int e = c!=0;
  int h = b!=0;
  int d = e|h;
  return d;
}

int f2(int a, int b)
{
  return (a!=0|b!=0);
}

--- CUT ---
Right now only f2 produces good code while the other two are not so good.


---


### compiler : `gcc`
### title : `Gcc failed to hoist loop invariant GOT load out of loop`
### open_at : `2012-02-27T08:25:18Z`
### last_modified_date : `2023-05-26T01:08:48Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=52396
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.7.0`
### severity : `enhancement`
### contents :
Compile the following source code with options -march=armv7-a -mthumb -Os -fpic

extern int array[];

int t0l(int len)
{
  int t = 0;
  int i;
  for (i=0; i<len; i++)
    t = t + array[i];
  return t;
}

ARM gcc 4.7 generates:


t0l:
	ldr	r1, .L4
	movs	r3, #0
	push	{r4, lr}
.LPIC8:
	add	r1, pc
	mov	r2, r3
	b	.L2
.L3:
	ldr	r4, .L4+4                // A
	ldr	r4, [r1, r4]             // B
	ldr	r4, [r4, r3, lsl #2]
	adds	r3, r3, #1
	adds	r2, r2, r4
.L2:
	cmp	r3, r0
	blt	.L3
	mov	r0, r2
	pop	{r4, pc}
.L5:
	.align	2
.L4:
	.word	_GLOBAL_OFFSET_TABLE_-(.LPIC8+4)
	.word	array(GOT)

Instructions AB are loop invariant, could be taken out of the loop without increase code size.

If I change -Os to -O2, ivopts can successfully do this optimization.


---


### compiler : `gcc`
### title : `BIT_FIELD_REF <MEM_REF <>> should be canonicalized for non-bitfield accesses`
### open_at : `2012-02-29T14:20:05Z`
### last_modified_date : `2021-12-08T01:55:59Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=52436
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.7.0`
### severity : `enhancement`
### contents :
typedef long long __m128i __attribute__ ((__vector_size__ (16),
                                          __may_alias__));
typedef struct
{
  __m128i b;
} s_1a;
typedef s_1a s_1m __attribute__((aligned(1)));
void
foo (s_1m *p)
{
  p->b[1] = 5;
}

Produces in .optimized

foo (struct s_1m * p)
{
<bb 2>:
  BIT_FIELD_REF <p_1(D)->b, 64, 64> = 5;
  return;

}

we should have canoncialized (aka fold_stmt'ed) the LHS to

  MEM <(__m128i *)p_1(D), 8> = 5;


---


### compiler : `gcc`
### title : `lower-subreg.c: code bloat of 300%-400% for multi-word memory splits`
### open_at : `2012-03-09T15:38:49Z`
### last_modified_date : `2023-05-16T23:53:16Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=52543
### status : `REOPENED`
### tags : `FIXME, missed-optimization`
### component : `rtl-optimization`
### version : `4.7.0`
### severity : `normal`
### contents :
lower-subreg.c causes extreme code bloat for some memory accesses because it does not take into account the additional costs caused by the split.

Example code for AVR address spaces:

long readx (const __memx long *p)
{
    return *p;
}

long read1 (const __flash1 long *p)
{
    return *p;
}

long read0 (const __flash long *p)
{
    return *p;
}

Reason is that read from these address spaces need one preparation sequence (set up segment register) per read. Thus:

For one 4-byte read there will be one preparation sequence.
For 4 one-byte reads there will be 4 preparation sequences.

For the __flash address space no preparation is needed, but a 32-bit read can use post-increment addressing whereas a split to 4 byte moves won't use post-increment because GCC is completely afraid of pre-/post-modify addressing.

The only place to hook in could be mode_dependent_address, however, that hook just passes the address down to the backend but omits the address space in use.
As all 16-bit address spaces (including generic) use HImode as pointer mode, the target cannot take a decision based on the address alone.

Configured with: ../../gcc.gnu.org/trunk/configure --target=avr --prefix=/local/gnu/install/gcc-4.7 --disable-nls --with-dwarf2 --enable-checking=yes,rtl --enable-languages=c,c++

gcc version 4.8.0 20120307 (experimental) (GCC)


---


### compiler : `gcc`
### title : `suboptimal assignment to avx element`
### open_at : `2012-03-12T22:49:57Z`
### last_modified_date : `2021-12-25T22:30:39Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=52572
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.7.0`
### severity : `enhancement`
### contents :
For the following program:
#include <x86intrin.h>
__m256d f(__m256d x){
  x[0]=0;
  return x;
}

gcc -O3 generates:
	vmovlpd	.LC0(%rip), %xmm0, %xmm1
	vinsertf128	$0x0, %xmm1, %ymm0, %ymm0
or with -Os:
	vxorps	%xmm2, %xmm2, %xmm2
	vmovsd	%xmm2, %xmm0, %xmm1
	vinsertf128	$0x0, %xmm1, %ymm0, %ymm0

If I understand correctly, it first constructs {0,x[1],0,0} and then merges it with the upper part of x. However, using the legacy movlpd instruction would avoid zeroing the upper 128 bits and thus the vinsertf128 wouldn't be needed.

Is there a policy not to generate the non-VEX instructions anymore, or is this a missed optimization?

Setting x[1] is similar. For x[2] or x[3], we get extract+mov+insert, but it might be better to do something with vblendpd.


---


### compiler : `gcc`
### title : `SH Target: Inefficient shift by T bit result`
### open_at : `2012-03-19T21:50:05Z`
### last_modified_date : `2023-07-22T03:06:41Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=52628
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `target`
### version : `4.8.0`
### severity : `enhancement`
### contents :
int test_01 (int a, int b, int c)
{
  return c << (a > b ? 1 : 0);
}

-m4 -O2:
        cmp/gt	r5,r4
        mov	r6,r0
        movt	r1
        rts	
        shld	r1,r0

better:
        cmp/gt	r5,r4
        bf	0f
        add     r6,r6     ! do not use shll because of T bit usage in shll
0:
        rts
        mov	r6,r0



int test_02 (int a, int b, int c)
{
  return c << (a > b ? 2 : 0);
}

-m4 -O2:
        cmp/gt	r5,r4
        mov	r6,r0
        movt	r1
        add	r1,r1
        rts	
        shld	r1,r0

better:
        cmp/gt	r5,r4
        bf	0f
        shll2	r6
0:
        rts
        mov	r6,r0


The same goes for other shift amounts like 8 and 16.
On SH4 the zero-displacement conditional branch code should be faster.


---


### compiler : `gcc`
### title : `Equality rewrites pessimizes code`
### open_at : `2012-03-31T00:29:50Z`
### last_modified_date : `2023-08-05T21:42:59Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=52802
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.8.0`
### severity : `enhancement`
### contents :
I have a function (in foo.c)

unsigned f(unsigned a, unsigned b)
{
        if (a < 8)
                return a;
        else if (a == 8)
                return b;
        else
                return 4711;
}

that GCC compiles to (x86_64, -Os)

        cmpl    $7, %edi        #, a
        movl    %edi, %eax      # a, a
        jbe     .L2     #,
        cmpl    $8, %edi        #, a
        movl    $4711, %eax     #, tmp63
        cmove   %esi, %eax      # b,, a
.L2:
        ret

Here it is confusing to see that it starts by doing a "cmp $7, %edi" and then goes on to do a "cmp $8, %edi" since I never said anything but 8, so the big question is why there are two compares.

The reason seems to be premature optimization. The C parser tries to minimize the value of all comparision values so that -fdump-tree-original shows

;; Function f (null)
;; enabled by -tree-original


{
  if (a <= 7)
    {
      return a;
    }
  else
    {
      if (a == 8)
        {
          return b;
        }
      else
        {
          return 4711;
        }
    }
}

and there the 7 have magically appeared.


---


### compiler : `gcc`
### title : `[x32] missed optimization for pointer return value`
### open_at : `2012-04-02T23:33:34Z`
### last_modified_date : `2021-08-30T02:08:06Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=52838
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.7.0`
### severity : `enhancement`
### contents :
The program test.c:

extern void *foo(void);
extern void bar(void*);

void test(void)
{
  bar(foo());
}

when compiled with
gcc-4.7 -mx32 -Os -S test.c
produces:
	.file	"test.c"
	.text
	.globl	test
	.type	test, @function
test:
.LFB0:
	.cfi_startproc
	pushq	%rax
	.cfi_def_cfa_offset 16
	call	foo
	popq	%rdx
	.cfi_def_cfa_offset 8
	movq	%rax, %rdi
	jmp	bar
	.cfi_endproc
.LFE0:
	.size	test, .-test
	.ident	"GCC: (Debian 4.7.0-1) 4.7.0"
	.section	.note.GNU-stack,"",@progbits

Here "movq %rax, %rdi" could be replaced by "movl %eax, %edi", saving one prefix byte 0x48.


---


### compiler : `gcc`
### title : `[x32] *load_tp_x32 in i386.md isn't necessary`
### open_at : `2012-04-03T18:12:55Z`
### last_modified_date : `2021-08-30T02:06:22Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=52848
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `target`
### version : `4.8.0`
### severity : `normal`
### contents :
Segment register %fs is used as thread pointer for x32 in 64bit hardware mode.
For a memory operand "%fs:address", its effective address is the base address
of %fs + address.  The base address of %fs are hidden and "mov %fs, %ax" only
accesses the visible part of %fs, which is the 16bit segment selector.

In x32, UNSPEC_TP refers to the base address of %fs.  To access the
base address of %fs, a system call is provided:

	int arch_prctl(int code, unsigned long long addr);
	int arch_prctl(int code, unsigned long long *addr);

       ARCH_SET_FS
              Set the 64-bit base for the FS register to addr.

       ARCH_GET_FS
              Return the 64-bit base value for the FS register of the
	      current thread in the unsigned long pointed to by addr.

We must use arch_prctl to update the base address of %fs,  To read
the base address of %fs, OS arranges that the base address of %fs points
to a struct:

typedef struct
{
  void *tcb;		/* Pointer to the TCB.  Not necessarily the
			   thread descriptor used by libpthread.  */
  ...
}

and sets up "tcb" == the base address of %fs so that the address of "%fs:0"
is the address of the tcb field.  For x32, the base address of %fs is
between 0 and 0xffffffff.  We can use

"mov{l}\t{%%fs:0, %k0|%k0, DWORD PTR fs:0}"

to move the base address of %fs into %r32 and %r64 directly.  In case
of %r32, we are loading "tcb", which is a 32bit memory.  For %r64, we
are loading "tcb" and zero-extend it to 64bit.  We can use

;; Load and add the thread base pointer from %<tp_seg>:0.
(define_insn "*load_tp_x32_<mode>"
  [(set (match_operand:SWI48x 0 "register_operand" "=r") 
        (unspec:SWI48x [(const_int 0)] UNSPEC_TP))]
  "TARGET_X32"
  "mov{l}\t{%%fs:0, %k0|%k0, DWORD PTR fs:0}"
  [(set_attr "type" "imov")
   (set_attr "modrm" "0")
   (set_attr "length" "7")
   (set_attr "memory" "load")
   (set_attr "imm_disp" "false")])

instead of

;; Load and add the thread base pointer from %<tp_seg>:0.
(define_insn "*load_tp_x32"
  [(set (match_operand:SI 0 "register_operand" "=r") 
        (unspec:SI [(const_int 0)] UNSPEC_TP))]
  "TARGET_X32"
  "mov{l}\t{%%fs:0, %0|%0, DWORD PTR fs:0}"
  [(set_attr "type" "imov")
   (set_attr "modrm" "0")
   (set_attr "length" "7")
   (set_attr "memory" "load")
   (set_attr "imm_disp" "false")])

(define_insn "*load_tp_x32_zext"
  [(set (match_operand:DI 0 "register_operand" "=r")
        (zero_extend:DI (unspec:SI [(const_int 0)] UNSPEC_TP)))]
  "TARGET_X32"
  "mov{l}\t{%%fs:0, %k0|%k0, DWORD PTR fs:0}"
  [(set_attr "type" "imov")
   (set_attr "modrm" "0")
   (set_attr "length" "7")
   (set_attr "memory" "load")
   (set_attr "imm_disp" "false")])


---


### compiler : `gcc`
### title : `-Wstrict-overflow false alarm with bounded loop`
### open_at : `2012-04-08T08:58:51Z`
### last_modified_date : `2021-09-14T07:09:21Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=52904
### status : `RESOLVED`
### tags : `diagnostic, missed-optimization, xfail`
### component : `tree-optimization`
### version : `4.7.0`
### severity : `normal`
### contents :
Created attachment 27113
simplified version of Emacs code, illustrating the bug

I ran into this problem when trying to build GNU Emacs with -Wstrict-overflow.

Compiling the attached program 'v.i' with the following command:

gcc -c -Wstrict-overflow -O2 v.i

generates the diagnostic:

v.i: In function 'wait_reading_process_output':
v.i:14:6: error: assuming signed overflow does not occur when simplifying conditional to constant [-Werror=strict-overflow]

The diagnostic is obviously incorrect, since the variable 'nfds' cannot possibly exceed 1024.

I will also attach the output of "gcc -v -c -Wstrict-overflow -O2 v.i".


---


### compiler : `gcc`
### title : `completely peel loops that do not run a constant time`
### open_at : `2012-04-19T14:40:42Z`
### last_modified_date : `2021-12-28T04:27:08Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=53044
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.0`
### severity : `enhancement`
### contents :
There exist loops where we do not know how many times they run.  Consider

int objects[2];

void foo (int n)
{
  int i;
  for (i = 0; i < n; ++i)
    objects[i] = i;
}

we do know the loop will run at most twice (due to undefined behavior
analysis, the info is accessible via max_loop_iterations (loop)).

It could be beneficial to completely peel such loops (retaining the
exit checks, of course).  At least for loops that do not run many
times (like at most once or twice, as in the above example).

int objects[1];

void foo (int n)
{
  int i;
  for (i = 0; i < n; ++i)
    objects[i] = i;
}

jump threading should handle the above case from VRP, but currently
VRP transforms the above to

<bb 2>:
  if (n_2(D) > 0)
    goto <bb 4>;
  else
    goto <bb 3>;

<bb 3>:
  return;

<bb 4>:

<bb 5>:
  ivtmp.5_1 = 0;
  i_9 = 0;
  MEM[(int[1] *)&objects] = 0;
  ivtmp.5_8 = 1;
  i_7 = 1;
  if (n_2(D) > 1)
    goto <bb 7>;
  else
    goto <bb 6>;

<bb 6>:
  goto <bb 3>;

<bb 7>:
  goto <bb 5>;

thus, a conditionally endless loop (ugh, a side-effect that we even preserve).


---


### compiler : `gcc`
### title : `insn-recog.c:recog calls predicates known to be false before matching bare RTL code`
### open_at : `2012-04-22T18:37:55Z`
### last_modified_date : `2021-09-15T01:55:00Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=53074
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.8.0`
### severity : `enhancement`
### contents :
The following was observed for gcc-4_7-branch r185763 as well as for trunk r186667.

The decision-tree in insn-recog.c, when generated from candidate patterns where one candidate (the first in file) pattern has a bare (label_ref ...) (without specified mode) and others (after the first in the file) has (match_operand:SI "operand_known_to_not_match_label_ref" ...) where operand_known_to_not_match_label_ref is for example, nonimmediate_operand or register_operand, inspects the mode of the operand of the insn being matched and calls the predicates despite it knowing they will fail.  After the calls, it will correctly match the insn to the first pattern.  This will not happen if the predicate is not known to fail or when no mode is specified for the second pattern (then there's the expected test for LABEL_REF).  It should instead always first check the operand to be LABEL_REF, matching the first pattern.

I'm labelling this as "missed optimization"; I can't make a strong case that the predicate call should be considered wrong-code, though the argument would be that it could assert, as there's no point calling it for a label_ref as the first pattern will always match.

It could be that this is a special-case and that inspecting mode and calling predicates is seen as cheaper than inspecting the actual operand code and matching any mode, but at face value it doesn't make sense, in particular as the rules are that the first pattern has to match.

See <http://gcc.gnu.org/ml/gcc/2012-04/msg00771.html> for actual generated code and further discussion.


---


### compiler : `gcc`
### title : `memcpy/memset loop recognition`
### open_at : `2012-04-23T04:51:31Z`
### last_modified_date : `2019-09-18T02:23:19Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=53081
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.0`
### severity : `normal`
### contents :
Both LLVM and icc recognize initialization and copy loop and synthesize calls to memcpy and memset.  memmove call can also be synthesized when src/target may overlap.

Option needs to provided to disable such optimization in signal handlers.

I consider this as optimization for benchmarking ;) For instance, the prime number finder program sieve.c is one of the benchmarks in LLVM. Both LLVM and icc beats gcc in this one because of the missing optimization.


#ifndef T
#define T int
#endif

T arr[1000];

void foo(int n)
{
  int i;
  for (i = 0; i < n; i++)
    {
      arr[i] = 0;
    }
}

void foo2(int n, T* p)
{
  int i;
  for (i = 0; i < n; i++)
    {
      *p++ = 0;
    }
}

#ifndef T
#define T int
#endif

T arr[1000];
T arr2[1000];

void foo(int n)
{
  int i;
  for (i = 0; i < n; i++)
    {
      arr[i] = arr2[i];
    }
}


// sieve.c

/* -*- mode: c -*-
 * $Id: sieve.c 36673 2007-05-03 16:55:46Z laurov $
 * http://www.bagley.org/~doug/shootout/
 */

#include <stdio.h>
#include <stdlib.h>

int
main(int argc, char *argv[]) {
#ifdef SMALL_PROBLEM_SIZE
#define LENGTH 17000
#else
#define LENGTH 170000
#endif
    int NUM = ((argc == 2) ? atoi(argv[1]) : LENGTH);
    static char flags[8192 + 1];
    long i, k;
    int count = 0;

    while (NUM--) {
        count = 0; 
        for (i=2; i <= 8192; i++) {
            flags[i] = 1;
        }
        for (i=2; i <= 8192; i++) {
            if (flags[i]) {
                /* remove all multiples of prime: i */
                for (k=i+i; k <= 8192; k+=i) {
                    flags[k] = 0;
                }
                count++;
            }
        }
    }
    printf("Count: %d\n", count);
    return(0);
}


---


### compiler : `gcc`
### title : `[c++0x] Missed optimization: lambda closure object could be smaller`
### open_at : `2012-04-24T00:59:20Z`
### last_modified_date : `2022-11-02T16:07:16Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=53097
### status : `NEW`
### tags : `c++-lambda, missed-optimization`
### component : `c++`
### version : `4.7.0`
### severity : `enhancement`
### contents :
This code:

include <stdio.h>

int main(int argc, char **argv)
{
  int a, b;
  auto foo = [&](){return a + b;};
  printf("%d\n", (int)sizeof(foo));
  return 0;
}

prints 16 (on x86-64) on gcc 4.6 and something quite close to 4.7 at -O2 and -Ofast.  This is as expected if the closure object is implemented as imagined in the spec.

In this particular case, accessing a from the lambda is defined behavior iff accessing b is defined (because either a and b are both in scope or both out of scope, so the lambda could be optimized based on the knowledge that a and b are at a fixed offset from each other.  This would give size 8.

(It sounds like this could be rather difficult.  clang++ 2.9 works the same way as g++.  I don't really expect to see this optimization implemented anytime soon.)


---


### compiler : `gcc`
### title : `Optimize __int128 with range information`
### open_at : `2012-04-24T07:07:36Z`
### last_modified_date : `2023-07-21T23:32:57Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=53100
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.0`
### severity : `enhancement`
### contents :
(not sure about the "component" field)

In the following program, on x86_64, the first version generates two imulq, while the second generates 4 imulq and 2 mulq. It would be convenient if I could just write the whole code with __int128 and let the compiler do the optimization by tracking the range of numbers.

int f(int a,int b,int c,int d,int e,int f){
#if 0
  long x=a;
  long y=b;
  long z=c;
  long t=d;
  long u=e;
  long v=f;
  return (z-x)*(__int128)(v-y) < (u-x)*(__int128)(t-y);
#else
  __int128 x=a;
  __int128 y=b;
  __int128 z=c;
  __int128 t=d;
  __int128 u=e;
  __int128 v=f;
  return (z-x)*(v-y) < (u-x)*(t-y);
#endif
}


---


### compiler : `gcc`
### title : `Recognize casts to sub-vectors`
### open_at : `2012-04-24T10:18:26Z`
### last_modified_date : `2021-08-19T19:49:20Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=53101
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.7.0`
### severity : `enhancement`
### contents :
Hello,

starting from an AVX __m256d vector x, getting its first element is best done with *(double*)&x, which is what x[0] internally does, and which generates no instruction (well, the following has vzeroupper, but let's forget that). However, *(__m128d*)&x generates 2 movs and I have to explicitly use _mm256_extractf128_pd to get the proper nop. Could the compiler be taught to recognize the casts between pointers to vectors of the same object type the same way it recognizes casts to pointers to that object type?

#include <x86intrin.h>
#if 0
typedef double T;
#else
typedef __m128d T;
#endif
T f(__m256d x){
  return *(T*)&x;
}

The closest report I found is PR 44551, which is quite different. PR 29881 shows that using a union is not an interesting alternative. I marked this one as target, but it may very well be that the recognition should be in the middle-end, or even that the front-end should mark the cast somehow.


---


### compiler : `gcc`
### title : `scheduling fail`
### open_at : `2012-04-25T01:19:27Z`
### last_modified_date : `2021-12-18T23:25:31Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=53107
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.7.0`
### severity : `normal`
### contents :
When generating code for testsuite/gcc.c-torture/execute/ieee/pr50310.c, I noticed that all the stores are pushed to the end where they can't execute simultaneously with other instructions.  I have tons of free execution slots around the stores, as the stores have to contend with a relatively narrow off-chip data path to memory.  The code looks something like:

;;   --------------- forward dependences: ------------ 

;;   --- Region Dependences --- b 2 bb 0 
;;      insn  code    bb   dep  prio  cost   reservation
;;      ----  ----    --   ---  ----  ----   -----------
;;       18   392     2     2     7     1   cmpcc       : 35 19 
;;       19  1633     2     2     6     1   movcc       : 20 
;;       20    80     2     2     5     5   stm_4       : 
;;       35  1633     2     2     6     1   movcc       : 36 
;;       36    80     2     2     5     5   stm_4       : 
;;       50   388     2     2     7     1   cmpcc       : 67 51 
;;       51  1633     2     2     6     1   movcc       : 52 
;;       52    80     2     2     5     5   stm_4       : 
;;       67  1633     2     2     6     1   movcc       : 68 
;;       68    80     2     2     5     5   stm_4       : 
;;       82   389     2     2     7     1   cmpcc       : 99 83 
;;       83  1633     2     2     6     1   movcc       : 84 
;;       84    80     2     2     5     5   stm_4       : 
;;       99  1633     2     2     6     1   movcc       : 100 
;;      100    80     2     2     5     5   stm_4       : 
[ repeated 10 more times]

with a sequence of 16 of the 3 instruction block as this is an -O3 compile.  Most of the costs associated with cmpcc and movcc would be free, if they were moved near the stm instructions.  The scheduling algorithm sorts and issues the insns based upon prio, so, all the 7s (cmpcc) go first, then all the 6s go next (movcc), and all the stores (stm_4) last.  This hurts, and the original ordering would have produced faster code.  :-(  I don't know the best way to fix this, as this is just a machine independent part of the algorithm that dates back to the original, this is how you schedule paper.  It is incomplete and is now overly simplistic for the types of cpus some people build.  The best fix is one that refines the costs in some way.  For example, cmpcc, movecc, stm_4 with the stm_4 staggered 1 group down, when run through the dfa, would come to the conclusion that the cmpcc and movecc instructions are free.  Presently the priority field is a simple addition of the individual costs of the insns, not taking into consideration that the dfa knows that simple addition is a poor substitute.


---


### compiler : `gcc`
### title : `Extra load store/instructions compared to gcc-3.4 on ARM`
### open_at : `2012-04-25T13:34:26Z`
### last_modified_date : `2021-10-01T02:50:32Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=53114
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `unknown`
### severity : `normal`
### contents :
Created attachment 27236
Shell sort function

Hi guys,
I have a test case (shell sort, see attached) compiled with different
ARM compilers:
GCC-4.6.3, GCC-3.4.6, and ARMCC.

Both ARMCC and GCC-3.4.6  generate quite optimal assembly while GCC-4.6.3
inserts extra load/store instructions compared to the other compilers.

Can the SSA representation usage in modern GCC be the reason for this?

If so, has anyone tried to do something about it?

% armcc
ARM C/C++ Compiler, 4.1 [Build 713]

The file has been compiled with following options:
for GCC:
-O3
for ARMCC:
-O3 -Otime


---


### compiler : `gcc`
### title : `missed-optimization: worse code for 'x <= 0' compared to 'x < 0'`
### open_at : `2012-04-25T14:20:53Z`
### last_modified_date : `2021-12-15T01:43:05Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=53117
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.8.0`
### severity : `enhancement`
### contents :
void f1(int* p) {
        p[1] -= 5;
        if (p[1] < 0) p[2] += 3;
}
void f2(int* p) {
        p[1] -= 5;
        if (p[1] <= 0) p[2] += 3;
}

The only difference between f1() and f2() is the comparison ('<' vs '<='). On x86_64 (and x86) gcc revision trunk@186808 generates more efficient code for f1() than for f2(). Here's the assembler output when compiled with -Os (but -O2 and -O3) show a similar difference:


0000000000000000 <_Z2f1Pi>:
   0:   83 6f 04 05             subl   $0x5,0x4(%rdi)
   4:   79 04                   jns    a <_Z2f1Pi+0xa>
   6:   83 47 08 03             addl   $0x3,0x8(%rdi)
   a:   c3                      retq   

000000000000000b <_Z2f2Pi>:
   b:   8b 47 04                mov    0x4(%rdi),%eax
   e:   83 e8 05                sub    $0x5,%eax
  11:   85 c0                   test   %eax,%eax
  13:   89 47 04                mov    %eax,0x4(%rdi)
  16:   7f 04                   jg     1c <_Z2f2Pi+0x11>
  18:   83 47 08 03             addl   $0x3,0x8(%rdi)
  1c:   c3                      retq 


gcc-4.6.1 generates the less efficient variant for both functions.


---


### compiler : `gcc`
### title : `XOR AL,AL to zero lower 8 bits of EAX/RAX causes partial register stall (Intel Core 2)`
### open_at : `2012-04-27T03:42:16Z`
### last_modified_date : `2021-08-15T05:20:50Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=53133
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.7.0`
### severity : `normal`
### contents :
Processor is Intel(R) Core(TM)2 Duo CPU E8400 @ 3.00GHz

#include <stdint.h>
#include <stdio.h>

uint32_t mem = 0;

int main(void) {
  uint64_t sum=0;
  for (uint32_t i=3000000000; i>0; --i) {
    asm volatile ("" : : : "memory"); //load data from memory each time
    uint64_t data = mem;

    //partial register stall
    sum += (data & UINT64_C(0xFFFFFFFFFFFFFF00)) >> 2;

    //no partial register stall
    //sum += (data >> 2) & UINT64_C(0xFFFFFFFFFFFFFFC0);
  }
  printf("sum is %llu\n", sum);
}

$ gcc-4.7 -O3 -std=gnu99 partial_register_stall.c && time ./a.out 
sum is 0

real	0m4.504s
user	0m4.500s
sys	0m0.000s

Each loop iteration is 4.5 cycles.

Relevant assembly code:

  400410:       8b 05 ee 04 20 00       mov    eax,DWORD PTR [rip+0x2004ee]        # 600904 <mem>
  400416:       30 c0                   xor    al,al
  400418:       48 c1 e8 02             shr    rax,0x2
  40041c:       48 01 c6                add    rsi,rax
  40041f:       83 ea 01                sub    edx,0x1
  400422:       75 ec                   jne    400410 <main+0x10>

mem is zero-extended into RAX. The lower 8 bits of RAX are zeroed via XOR AL, AL. The result is shifted down by two.

An equivalent way of computing this is to first shift down by two and then mask the lower six bits to zero. That is, replace the line:
   sum += (data & UINT64_C(0xFFFFFFFFFFFFFF00)) >> 2;
with:
   sum += (data >> 2) & UINT64_C(0xFFFFFFFFFFFFFFC0);

$ gcc-4.7 -O3 -std=gnu99 partial_register_stall.c && time ./a.out 
sum is 0

real	0m2.002s
user	0m2.000s
sys	0m0.000s

Each loop iteration is now 2 cycles.

Relevant assembly code:

  400410:       8b 05 fe 04 20 00       mov    eax,DWORD PTR [rip+0x2004fe]        # 600914 <mem>
  400416:       48 c1 e8 02             shr    rax,0x2
  40041a:       48 83 e0 c0             and    rax,0xffffffffffffffc0
  40041e:       48 01 c6                add    rsi,rax
  400421:       83 ea 01                sub    edx,0x1
  400424:       75 ea                   jne    400410 <main+0x10>


---


### compiler : `gcc`
### title : `Use vector comparisons for if cascades`
### open_at : `2012-05-05T04:06:33Z`
### last_modified_date : `2021-07-21T02:54:13Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=53243
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.0`
### severity : `enhancement`
### contents :
Created attachment 27312
Test program (compile with and without -DOLD)

The vector units can compare multiple comparisons concurrently but this is not used automatically in gcc in situations where it can lead to better performance.  Assume a function like this:

void
f(float a)
{
  if (a < 1.0)
    cb(1);
  else if (a < 2.0)
    cb(2);
  else if (a < 3.0)
    cb(3);
  else if (a < 4.0)
    cb(4);
  else if (a < 5.0)
    cb(5);
  else if (a < 6.0)
    cb(6);
  else if (a < 7.0)
    cb(7);
  else if (a < 8.0)
    cb(8);
  else
    ++o;
}

In this case the first or second if is not marked with __builtin_expect as likely, otherwise the following *might* not apply.

The routine can be rewritten for AVX machines like this:

void
f(float a)
{
  const __m256 fv = _mm256_set_ps(8.0,7.0,6.0,5.0,4.0,3.0,2.0,1.0);
  __m256 r = _mm256_cmp_ps(fv, _mm256_set1_ps(a), _CMP_LT_OS);
  int i = _mm256_movemask_ps(r);
  asm goto ("bsr %0, %0; jz %l[less1]; .pushsection .rodata; 1: .quad %l2, %l3, %l4, %l5, %l6, %l7, %l8, %l9; .popsection; jmp *1b(,%0,8)" : : "r" (i) : : less1, less2, less3, less4, less5, less6, less7, less8, gt8);
  __builtin_unreachable ();
 less1:
  cb(1);
  return;
 less2:
  cb(2);
  return;
 less3:
  cb(3);
  return;
 less4:
  cb(4);
  return;
 less5:
  cb(5);
  return;
 less6:
  cb(6);
  return;
 less7:
  cb(7);
  return;
 less8:
  cb(8);
  return;
 gt8:
  ++o;
}

This might not generate the absolute best code but it runs for the test program which I attach 20% faster.

The same technique can be applied to integer comparisons.  More complex if cascades can also be simplified a lot by masking the integer bsr result accordingly.  This should still be faster.


---


### compiler : `gcc`
### title : `Optimize out some exception code`
### open_at : `2012-05-09T10:37:04Z`
### last_modified_date : `2021-07-23T00:12:12Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=53294
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `c++`
### version : `4.8.0`
### severity : `enhancement`
### contents :
Hello,

it would be great if the compiler could transform code like:

  try {
    throw 42;
  } catch(...) {
  }

into nothing (or in practice into a simple goto, since there will be code around). It already knows to remove the code after "throw", it could statically check that the exception will be caught locally and thus skip the __cxa_throw, __cxa_begin_catch game.

Filed as C++ front-end, but it might be for the middle-end, since it would be best if this optimization happened after inlining.


---


### compiler : `gcc`
### title : `[4.6/4.7/4.8 Regression] Bad if conversion in cptrf2 of rnflow.f90`
### open_at : `2012-05-14T15:40:33Z`
### last_modified_date : `2023-04-20T10:20:16Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=53346
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.8.0`
### severity : `normal`
### contents :
At revision 187457 (i.e., with pr53340 fixed) on x86_64-apple-darwin10, after

[macbook] test/dbg_rnflow% gfc -c -O3 -ffast-math -funroll-loops timctr.f90 cmpcpt.f90 cptrf2.f90 dger.f90 dgetri.f90 dswap.f90 dtrsm.f90 evlrnf.f90 idamax.f90 main.f90 mattrs.f90 cmpmat.f90 dgemm.f90 dgetf2.f90 dlaswp.f90 dtrmm.f90 dtrti2.f90 extpic.f90 ilaenv.f90 matcnt.f90 reaseq.f90 xerbla.f90 cptrf1.f90 dgemv.f90 dgetrf.f90 dscal.f90 dtrmv.f90 dtrtri.f90 gentrs.f90 lsame.f90 matsim.f90
[macbook] test/dbg_rnflow% makeo ; time a.out > /dev/null                                                                                             23.872u 0.349s 0:24.22 99.9%	0+0k 0+0io 0pf+0w[macbook] test/dbg_rnflow% /opt/gcc/gcc4.8p-187339/bin/gfortran -c -O3 -ffast-math -funroll-loops evlrnf.f90
[macbook] test/dbg_rnflow% makeo ; time a.out > /dev/null
22.259u 0.346s 0:22.61 99.9%	0+0k 0+0io 0pf+0w
[macbook] test/dbg_rnflow% /opt/gcc/gcc4.8p-187291/bin/gfortran -c -O3 -ffast-math -funroll-loops idamax.f90
[macbook] test/dbg_rnflow% makeo ; time a.out > /dev/null
22.252u 0.345s 0:22.60 99.9%	0+0k 0+0io 0pf+0w
[macbook] test/dbg_rnflow% /opt/gcc/gcc4.8p-187102/bin/gfortran -c -O3 -ffast-math -funroll-loops idamax.f90
[macbook] test/dbg_rnflow% makeo ; time a.out > /dev/null
22.121u 0.346s 0:22.47 99.9%	0+0k 0+0io 0pf+0w

(i.e., working around prpr53342 and a regression for idamax.f90, see 
below), the compilation of cptrf2.f90 (source attached to pr53340) with the following flags yiels

optimization level      4.4.6   4.5.3   4.6.3   4.7.0   r187457

-O2                      27.8    28.2    28.2    21.8    21.8
-O2 -ftree-vectorize     27.8    28.2    28.2    27.9    27.9
-O3                      22.0    21.3    25.1    25.3    25.3
-O3 -fno-tree-vectorize  22.1    21.3    21.4    21.4    21.4

Note that 4.5/4.6/4.7 vectorize two loops (lines 21 and 29), while 4.8 vectorizes only the loop at line 21 (29: not vectorized: iteration count too small.).

Looking at my archives I have found that a first regression appeared 
between revisions 162456 and 164728

optimization level      4.6-162456 4.6p-164728

-O2                             28.2    28.3
-O2 -ftree-vectorize            28.1    28.3
-O3                             21.4    29.4
-O3 -fno-tree-vectorize         21.3    21.4
-O3 -ffast-math                 21.4    22.3
-O3 -ffast-math -funroll-loops  21.9    22.4

For the record, as said above the compilation of idamax regressed between 
revisions 187102 and 187291

[macbook] test/dbg_rnflow% /opt/gcc/gcc4.8p-187291/bin/gfortran -c -O3 -ffast-math -funroll-loops idamax.f90
[macbook] test/dbg_rnflow% makeo ; time a.out > /dev/null
22.252u 0.345s 0:22.60 99.9%	0+0k 0+0io 0pf+0w
[macbook] test/dbg_rnflow% /opt/gcc/gcc4.8p-187102/bin/gfortran -c -O3 -ffast-math -funroll-loops idamax.f90
[macbook] test/dbg_rnflow% makeo ; time a.out > /dev/null
22.121u 0.346s 0:22.47 99.9%	0+0k 0+0io 0pf+0w

Although the regression is slightly above the noise margin at the level of 
rnflow.f90, it could be worth to investigate it because:
(1) it is a LAPACK routine (may be slightly modified),
(2) there equivalent intrinsics in F90,
(3) the slowdown may be quite significant at the level of the proc itself.


---


### compiler : `gcc`
### title : `Autovectorization of a simple loop could be improved.`
### open_at : `2012-05-15T01:49:21Z`
### last_modified_date : `2021-07-21T03:24:51Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=53355
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.7.0`
### severity : `enhancement`
### contents :
The following simple function gets autovectorized by gcc-4.7 -O3

void foo(double *x)
{
	int i;

	for (i = 0; i < 100000; i++)
	{
		x[i] += 2.0;
	}
}

However, the generated code is rather poor:

foo:
.LFB0:
	.cfi_startproc
	movq	%rdi, %rax
	salq	$60, %rax
	sarq	$63, %rax
	movq	%rax, %rdx
	andl	$1, %edx
	testq	%rdx, %rdx
	movl	%edx, %ecx
	je	.L7
	movsd	.LC0(%rip), %xmm0
	movl	$99999, %r9d
	movl	$1, %r10d
	addsd	(%rdi), %xmm0
	movsd	%xmm0, (%rdi)
.L2:
	movl	$100000, %r8d
	andl	$1, %eax
	subl	%ecx, %r8d
	movl	%r8d, %esi
	shrl	%esi
	movl	%esi, %r11d
	addl	%r11d, %r11d
	je	.L3
	movapd	.LC1(%rip), %xmm1
	leaq	(%rdi,%rax,8), %rcx
	xorl	%edx, %edx
	xorl	%eax, %eax
	.p2align 4,,10
	.p2align 3
.L4:
	movapd	(%rcx,%rax), %xmm0
	addl	$1, %edx
	addpd	%xmm1, %xmm0
	movapd	%xmm0, (%rcx,%rax)
	addq	$16, %rax
	cmpl	%esi, %edx
	jb	.L4
	addl	%r11d, %r10d
	subl	%r11d, %r9d
	cmpl	%r11d, %r8d
	je	.L1
.L3:
	leal	-1(%r9), %edx
	movslq	%r10d, %r10
	leaq	(%rdi,%r10,8), %rax
	movsd	.LC0(%rip), %xmm1
	addq	%rdx, %r10
	leaq	8(%rdi,%r10,8), %rdx
	.p2align 4,,10
	.p2align 3
.L6:
	movsd	(%rax), %xmm0
	addsd	%xmm1, %xmm0
	movsd	%xmm0, (%rax)
	addq	$8, %rax
	cmpq	%rdx, %rax
	jne	.L6
.L1:
	rep
	ret
.L7:
	movl	$100000, %r9d
	xorl	%r10d, %r10d
	jmp	.L2


The first thing wrong is that the alignment test is rather clunky.  Instead, we can just do a "testq $8, %rdi" followed by a jump to the miss-aligned case.

The second thing wrong is that the code instead of falling-through to the aligned case, jumps down to L7 instead.  Forward jumps are predicted as not taken.

The inner loop is also longer than it should be.  It is possible to have one less increment statement inside.

Finally, after the main loop, the code again tests for miss-alignment.  This pessimizes the fast path.  Instead, it possible to move the slow miss-aligned case completely out with very little size penalty.

Doing the above optimizations yields:

	movapd 2_s, %xmm1
	testq $8, %rdi
	jne 2f
	
	lea 800000(%rdi), %rax

# The "Hot" inner loop
1:	movapd	(%rdi), %xmm0
	addq	$16, %rdi
	addpd	%xmm1, %xmm0
	movapd	%xmm0, (%rdi)
	cmpq	%rdi, %rax
	jne 1b
	rep ret

# The slow miss-aligned case	
2:      movsd	(%rdi), %xmm0
	addsd	%xmm1, %xmm0
	movsd	%xmm0, (%rdi)

	leaq 	(800000 - 16) (%rdi), %rax
	addq	$8, %rdi

3:	movapd	(%rdi), %xmm0
	addq	$16, %rdi
	addpd	%xmm1, %xmm0
	movapd	%xmm0, (%rdi)
	cmpq	%rdi, %rax
	jne 3b

	movsd	(%rdi), %xmm0
	addsd	%xmm1, %xmm0
	movsd	%xmm0, (%rdi)
	ret


---


### compiler : `gcc`
### title : `ia32/amd64: bsf can be used to test null memory, bsf sets zero flag`
### open_at : `2012-05-28T09:40:06Z`
### last_modified_date : `2021-11-29T09:02:00Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=53507
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.6.3`
### severity : `enhancement`
### contents :
Compiling:
int I;
void ifnull(void);
void testnull(void) {
  if (I == 0)
    ifnull();
}

void fct (unsigned u) {
  if (u != 0)
    I = __builtin_ffs(u) - 1;
}

result in for testnull():
	movl	I, %eax
	testl	%eax, %eax
	je	.L4
	rep
	ret
.L4:
	jmp	ifnull()
It would be shorter/quicker to replace the two first lines by:
        bsfl     I, %eax
        je       ifnull()
i.e. there is no need to load the memory variable into a register with bsf/bsr.

And result for fct():
	movl	4(%esp), %eax
	testl	%eax, %eax
	je	.L5
	bsfl	%eax, %eax
	movl	%eax, I
.L5:
	rep
	ret
It would be shorter/quicker to test if the parameter u is null by the bsf instruction:
	bsfl	4(%esp), %eax
	cmovne	%eax, I
.L5:
	rep
	ret


---


### compiler : `gcc`
### title : `[11/12/13/14 regression] vectorization causes loop unrolling test slowdown as measured by Adobe's C++Benchmark`
### open_at : `2012-05-31T00:53:01Z`
### last_modified_date : `2023-07-07T10:29:43Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=53533
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.7.1`
### severity : `normal`
### contents :
Comparing GCC versions, branches, and optimization levels on Adobe's C++Benchmark suite, I discovered that 4.7 has a major regression with their loop unrolling tests. I have captures the data here:

https://docs.google.com/spreadsheet/ccc?key=0Amu19eOay72HdE1xYVRPUTFYWU1TSld3Y2FEOEt5LXc

All compilers were fresh checkouts by me from their trunk revisions as of a few days ago. My configure command line:
/u/mhargett/src/gcc-4_7-branch/configure --program-suffix=-4.7 --prefix=/u/mhargett --enable-languages=c,c++,lto --enable-lto --with-build-config=bootstrap-lto --with-fpmath=sse --disable-libmudflap --disable-libssp --enable-build-with-cxx --enable-gold=yes --with-mpc=/u/mhargett --with-cloog=/u/mhargett/ --with-ppl=/u/mhargett/ --with-gmp=/u/mhargett/ --with-mpfr=/u/mhargett/ --enable-cloog-backend=isl --disable-cloog-version-check CC=gcc-4.7 CXX=g++-4.7

The 4.6 and 4.7 versions were both build against the same Cloog, ppl, mpfr, etc.

Going from "-O3 -floop-block -floop-strip-mine -floop-interchange -mtune=amdfam10" to "-Ofast -funsafe-loop-optimizations -funroll-loops -floop-block -floop-strip-mine -floop-interchange" didn't help.

Attached is a tar ball of the 4.6 and 4.7 -O3 optimized builds. 'make report' re-runs the tests, 'make clean && make' rebuilds.


---


### compiler : `gcc`
### title : `non-aligned memset on non-strict-alignment targets not optimized where aligned memset is`
### open_at : `2012-05-31T04:28:25Z`
### last_modified_date : `2022-05-21T18:35:37Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=53535
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.8.0`
### severity : `normal`
### contents :
The attached code is a modified gcc.dg/pr46647.c, which shows that memset isn't optimized on unaligned short (int-sized) data as it is for aligned data, even for non-strict-alignment targets, such as cris-* and x86_64-linux. Observe the emitted assembly code, which uses the same instructions for aligned and unaligned code as later optimizations cover up (for both cris-* and x86_64-linux). Hence, I guess this bug isn't really that important when it comes to just the generated code, just an annoying middle-end miss and annoyingly failing test-case.  (Whether the over-alignment-checks misses other optimization opportunities is another issue.)

Background: I stumbled upon this when changing the CRIS port to align global data by default. This made the always-before-failing gcc.dg/pr46647.c pass, for no good reason: alignment of data should not make a difference for emitted code (except for atomic support, WIP for CRIS).

This may be related to PR 52861.


---


### compiler : `gcc`
### title : `Register allocator doesn't tie return value register to output variable.`
### open_at : `2012-06-01T19:14:40Z`
### last_modified_date : `2022-02-06T09:39:57Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=53558
### status : `UNCONFIRMED`
### tags : `missed-optimization, ra`
### component : `rtl-optimization`
### version : `4.8.0`
### severity : `normal`
### contents :
Given the testcase below GCC generates extra moves to return value registers on ARM v7-a linux-gnueabi . Disabling the smax insn pattern or the "generic" 3 operand condition move to doesn't really help 

This also appears to be a problem on other architectures given the register allocator fails to merge the copy of the result value in to the result  .The *arm_smax_insn pattern looks like the following. Debuggging the register allocator showed that param 0,1, and 2 are in r1, r2 and r0 . However there is probably an easier fit with r0, r2 and r0 given r0 and r2 die as well in this instruction. I might be missing something here. 

(define_insn "*arm_smax_insn"
  [(set (match_operand:SI          0 "s_register_operand" "=r,r")
        (smax:SI (match_operand:SI 1 "s_register_operand"  "%0,?r")
                 (match_operand:SI 2 "arm_rhs_operand"    "rI,rI")))
   (clobber (reg:CC CC_REGNUM))]
  "TARGET_ARM"
  "@
   cmp\\t%1, %2\;movlt\\t%0, %2
   cmp\\t%1, %2\;movge\\t%0, %1\;movlt\\t%0, %2"
  [(set_attr "conds" "clob")
   (set_attr "length" "8,12")]
)






typedef unsigned int uint32_t;
typedef unsigned long long uint64_t;
typedef unsigned long uintptr_t;
typedef unsigned short uint16_t;
void f2(char *d, char const *s, int flags)
{
  uint32_t tmp0, tmp1;

  if (flags & 1)
    tmp0 = *s++;

  if (flags & 2)
    {
      uint16_t *ss = (void *)s;
      tmp1 = *ss++;
      s = (void *)ss;
    }

  if (flags & 1)
    *d++ = tmp0;

  if (flags & 2)
    {
      uint16_t *dd = (void *)d;
      *dd++ = tmp1;
      d = (void *)dd;
    }
}


---


### compiler : `gcc`
### title : `Suboptimal PC-relative addressing code on x86`
### open_at : `2012-06-09T00:23:19Z`
### last_modified_date : `2021-08-06T00:49:55Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=53617
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `target`
### version : `unknown`
### severity : `enhancement`
### contents :
Consider a function of the form:

int *foo()
{
    static int x;
    return &x;
}

When GCC compiles this, the result is similar to the following hand-written asm:

    call 1f
1:  pop %ecx
    add $_GLOBAL_OFFSET_TABLE_+[.-1b], %ecx
    lea x@GOTOFF(%ecx),%eax
    ret

i.e. it loads the address of the GOT in a register, then computes the GOT-relative address of the variable. This makes sense when the GOT address will be needed for more than one address lookup, but it's unnecessarily costly in the case where it's only used for a single variable, in which case the following code would be better:

    call 1f
1:  pop %eax
    add $[x-1b], %eax
    ret

The same principle applies to a great deal more code, and of course it works when __i686.get_pc_thunk.cx or similar is being used, too. Is there any way GCC could be enhanced to generate this superior code when possible?


---


### compiler : `gcc`
### title : `NRVO not applied where there are two different variables involved`
### open_at : `2012-06-11T19:29:05Z`
### last_modified_date : `2023-07-06T01:58:20Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=53637
### status : `NEW`
### tags : `missed-optimization`
### component : `c++`
### version : `4.7.0`
### severity : `enhancement`
### contents :
In the example below it should be possible to apply NRVO.  This situation is similar to, but more complicated than, the one reported in PR51571.

Note that while this is "just a missed optimization", NRVO can affect the way interfaces are designed, so aggressively covering all possible cases seems more important than with most optimizations.

$ cat nrvo.cc 
class Foo {
public:
  Foo() {}
  
  // Declare but don't define so that if NRVO doesn't kick in we
  // get a linker error.
  Foo(const Foo& other);
};

Foo bar(int i) {
  if (i > 1) {
    Foo result;
    return result;
  } else {
    Foo result;
    return result;
  }
}

int main(int argc, char* argv[]) {
  Foo f = bar(argc);
}

$ g++-4.7 -O2 nrvo.cc
/tmp/ccRlHce1.o: In function `bar(int)':
nrvo.cc:(.text+0xe): undefined reference to `Foo::Foo(Foo const&)'
collect2: error: ld returned 1 exit status
$ g++-4.7 --version
g++-4.7 (Ubuntu/Linaro 4.7.0-7ubuntu3) 4.7.0
Copyright (C) 2012 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.


---


### compiler : `gcc`
### title : `*andn* does not always get used with simd and loading from memory`
### open_at : `2012-06-13T06:49:06Z`
### last_modified_date : `2022-01-11T02:25:43Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=53652
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.7.0`
### severity : `enhancement`
### contents :
#define N 1024
long a[N], b[N], c[N];
int d[N], e[N], f[N];

void
foo (void)
{
  int i;
  for (i = 0; i < N; i++)
    a[i] = b[i] & ~c[i];
}

void
bar (void)
{
  int i;
  for (i = 0; i < N; i++)
    d[i] = e[i] & ~f[i];
}

doesn't use *andn* insns (e.g. vandnp[sd] for -O3 -mavx).  The problem is that
combiner doesn't help here, because
(insn 42 18 33 2 (set (reg:V4DI 94)
        (mem/u/c:V4DI (symbol_ref/u:DI ("*.LC0") [flags 0x2]) [2 S32 A256])) -1
     (expr_list:REG_EQUAL (const_vector:V4DI [
                (const_int -1 [0xffffffffffffffff])
                (const_int -1 [0xffffffffffffffff])
                (const_int -1 [0xffffffffffffffff])
                (const_int -1 [0xffffffffffffffff])
            ])
        (nil)))
is before the loop and thus in a different bb,
so the combiner doesn't substitute the all ones constant into the xor (which should fail, i?86 doesn't have a *not* SSE/AVX insn) and later on when the xor is substituted into the and (at that point it could figure that and (xor x -1) y
is andn).  Wonder if we should change the combiner somehow for the cases where REG_N_SETS == 1 pseudo has REG_EQUAL note, or if we want instead to handle this during expansion (introduce optional andnotM3 standard patterns?).


---


### compiler : `gcc`
### title : `suboptimal small switch - 3-way jump with only 1 comparison`
### open_at : `2012-06-14T11:05:05Z`
### last_modified_date : `2023-06-18T19:02:10Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=53669
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.8.0`
### severity : `enhancement`
### contents :
Hi,

The program below generates sub-optimal code for small (+dense) switch statements (small enough so that they are not implemented via jump-tables). The function foo() is the smallest example I could come up with that shows the problem. The function bar() shows the same problem in a slightly more realistic context.

The function foo() also shows a missed opportunity for jump-threading(?), should I file a separate bug report for this?

Tested on linux x86_64 with SVN revision thrunk@188550. Below I show the code generated with -Os, but -O2 and -O3 show the same missed optimization.

Wouter


-------8<---------8<---------8<--------8<--------8<-------

void f0();
void f1();
void f2();
void f3();


// Toy example to demonstrate the problem
void foo(int x) {
	switch (x) {
		case 0:  f0(); break;
		case 1:  f1(); break;
		default: f2(); break;
	}
}

// This is the code generated by 'g++-thrunk@188550 -Os'
// _Z3fooi: testl   %edi, %edi  <-- 1
//          je      .L5
//          decl    %edi        <-- 2 comparisons
//          jne     .L7
//          jmp     .L6         <-- why not immediately jump to _Z2f1v?
// .L5:     jmp     _Z2f0v
// .L6:     jmp     _Z2f1v
// .L7:     jmp     _Z2f2v

// This generates optimal(?) code
void my_foo(int x) {
	asm goto (
		"cmpl $1,%[x];"  // only 1 comparison
		"je   %l[l1];"
		"jb   %l[l0];"
		:: [x] "r" (x)
		:: l0, l1
	);
l2:	f2(); return;
l0:	f0(); return;
l1:	f1(); return;
}


// Bigger example in a slightly more realistic context:
//  e.g. a main loop that handles 4 elements per iteration and a switch
//       like this after that loop to handle the remaining elements.
void bar(int x) {
	switch (x & 3) {
		case 0: f0(); break;
		case 1: f1(); break;
		case 2: f2(); break;
		case 3: f3(); break;
	}
}

// This is the code generated by 'g++-thrunk@188550 -Os'
// _Z3bari: andl    $3, %edi
//          cmpl    $2, %edi    <-- 1
//          je      .L11
//          cmpl    $3, %edi    <-- 2
//          je      .L12
//          decl    %edi        <-- 3 comparisons
//          je      .L10
//          jmp     _Z2f0v
// .L10:    jmp     _Z2f1v
// .L11:    jmp     _Z2f2v
// .L12:    jmp     _Z2f3v

// This generates optimal(?) code
void my_bar(int x) {
	asm goto (
		"andl $3, %[x];" // implicit comparison with 0
		"je   %l[l0];"
		"cmpl $2, %[x];" // 1 explicit comparison
		"je   %l[l2];"
		"jb   %l[l1];"
		:: [x] "r" (x)
		:: l0, l1, l2
	);
l3:	f3(); return;
l0:	f0(); return;
l1:	f1(); return;
l2:	f2(); return;
}


---


### compiler : `gcc`
### title : `_mm_cmpistri generates redundant movslq %ecx,%rcx on x86-64`
### open_at : `2012-06-15T17:21:26Z`
### last_modified_date : `2019-01-18T19:05:36Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=53687
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `target`
### version : `4.8.0`
### severity : `enhancement`
### contents :
Compile the following strcmp() implementation with -O5 -march=corei7

#include <nmmintrin.h>

static inline int __strcmp(const char * cs, const char * ct)
{
	// Works for both 32-bit and 64-bit code

	// see http://www.strchr.com/strcmp_and_strlen_using_sse_4.2

	long diff = cs-ct;
	long nextbytes = 16;
	ct -= 16;

loop:
	__m128i ct16cs = _mm_loadu_si128( (const __m128i *) (ct += nextbytes) );
	int offset = _mm_cmpistri( ct16cs, * (const __m128i *) (ct+diff),   
                      _SIDD_CMP_EQUAL_EACH | _SIDD_NEGATIVE_POLARITY );
	__asm__ __volatile__ goto( "ja %l[loop] \n jc %l[not_equal]" : : :  
             "memory" : loop, not_equal );

	return 0;

not_equal:
	return ct[diff+offset] - ct[offset];
}

GCC generates the following code:
00000000004007c0 <strcmp>:
  4007c0:	48 29 f7             	sub    %rsi,%rdi
  4007c3:	48 83 ee 10          	sub    $0x10,%rsi
  4007c7:	48 83 c6 10          	add    $0x10,%rsi
  4007cb:	f3 0f 6f 06          	movdqu (%rsi),%xmm0
  4007cf:	66 0f 3a 63 04 3e 18 	pcmpistri $0x18,(%rsi,%rdi,1),%xmm0
  4007d6:	77 ef                	ja     4007c7 <strcmp+0x7>
  4007d8:	72 06                	jb     4007e0 <strcmp+0x20>
  4007da:	31 c0                	xor    %eax,%eax
  4007dc:	c3                   	retq   
  4007dd:	0f 1f 00             	nopl   (%rax)
* 4007e0:	48 63 c9             	movslq %ecx,%rcx
  4007e3:	48 01 f7             	add    %rsi,%rdi
  4007e6:	0f be 04 0f          	movsbl (%rdi,%rcx,1),%eax
  4007ea:	0f be 14 0e          	movsbl (%rsi,%rcx,1),%edx
  4007ee:	29 d0                	sub    %edx,%eax
  4007f0:	c3                   	retq   
  4007f1:	66 66 66 66 66 66 2e 	data32 data32 data32 data32 data32 nopw                                         
  4007f8:	0f 1f 84 00 00 00 00    %cs:0x0(%rax,%rax,1)
  4007ff:	00 

The "movslq" instruction is redundant, because pcmpistri clears the upper bits of RCX when generating an index (verified using gdb)


---


### compiler : `gcc`
### title : `Failed to combine load and jump on vtable`
### open_at : `2012-06-25T21:59:22Z`
### last_modified_date : `2021-08-19T05:20:18Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=53772
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.8.0`
### severity : `enhancement`
### contents :
[hjl@gnu-6 tmp]$ cat v.cc
struct Foo { virtual void f(); }; void f(Foo *f) { f->f(); }
[hjl@gnu-6 tmp]$ /opt/llvm/bin/clang -S -m64 -O2 -o clang64.s v.cc  
[hjl@gnu-6 tmp]$ cat clang64.s 
	.file	"v.cc"
	.text
	.globl	_Z1fP3Foo
	.align	16, 0x90
	.type	_Z1fP3Foo,@function
_Z1fP3Foo:                              # @_Z1fP3Foo
	.cfi_startproc
# BB#0:                                 # %entry
	movq	(%rdi), %rax
	jmpq	*(%rax)  # TAILCALL
.Ltmp0:
	.size	_Z1fP3Foo, .Ltmp0-_Z1fP3Foo
	.cfi_endproc


	.section	".note.GNU-stack","",@progbits
[hjl@gnu-6 tmp]$ /usr/gcc-4.7.2-x32/bin/gcc -S -O2 -m64 v.cc -o gcc64.s  
[hjl@gnu-6 tmp]$ cat gcc64.s
	.file	"v.cc"
	.text
	.p2align 4,,15
	.globl	_Z1fP3Foo
	.type	_Z1fP3Foo, @function
_Z1fP3Foo:
.LFB0:
	.cfi_startproc
	movq	(%rdi), %rax
	movq	(%rax), %rax
	jmp	*%rax
	.cfi_endproc
.LFE0:
	.size	_Z1fP3Foo, .-_Z1fP3Foo
	.ident	"GCC: (GNU) 4.7.2 20120622 (prerelease)"
	.section	.note.GNU-stack,"",@progbits
[hjl@gnu-6 tmp]$


---


### compiler : `gcc`
### title : `coalescing multiple static instances in function scope`
### open_at : `2012-06-27T06:48:58Z`
### last_modified_date : `2021-08-30T02:22:33Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=53785
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.0`
### severity : `enhancement`
### contents :
I come across this kind of pattern (repeated over and over in many functions)

    static const EvtId DM=EvtPDL::getId("D-");
    static const EvtId DP=EvtPDL::getId("D+");
    static const EvtId D0=EvtPDL::getId("D0");
    static const EvtId D0B=EvtPDL::getId("anti-D0");
    static const EvtId KM=EvtPDL::getId("K-");
    static const EvtId KP=EvtPDL::getId("K+");
    static const EvtId K0=EvtPDL::getId("K0");
    static const EvtId KB=EvtPDL::getId("anti-K0");
    static const EvtId KL=EvtPDL::getId("K_L0");
    static const EvtId KS=EvtPDL::getId("K_S0");
    static const EvtId PIM=EvtPDL::getId("pi-");
    static const EvtId PIP=EvtPDL::getId("pi+");
    static const EvtId PI0=EvtPDL::getId("pi0");

that materialized in
nm -C statics.so | grep " b "
0000000000003908 b guard variable for a1::bar(int)::D0
00000000000038e8 b guard variable for a1::bar(int)::DM
00000000000038f8 b guard variable for a1::bar(int)::DP
0000000000003948 b guard variable for a1::bar(int)::K0
0000000000003958 b guard variable for a1::bar(int)::KB
0000000000003968 b guard variable for a1::bar(int)::KL
0000000000003928 b guard variable for a1::bar(int)::KM
0000000000003938 b guard variable for a1::bar(int)::KP
0000000000003978 b guard variable for a1::bar(int)::KS
0000000000003918 b guard variable for a1::bar(int)::D0B
00000000000039a8 b guard variable for a1::bar(int)::PI0
0000000000003988 b guard variable for a1::bar(int)::PIM
0000000000003998 b guard variable for a1::bar(int)::PIP
0000000000003910 b a1::bar(int)::D0
00000000000038f0 b a1::bar(int)::DM
0000000000003900 b a1::bar(int)::DP
0000000000003950 b a1::bar(int)::K0
0000000000003960 b a1::bar(int)::KB
0000000000003970 b a1::bar(int)::KL
0000000000003930 b a1::bar(int)::KM
0000000000003940 b a1::bar(int)::KP
0000000000003980 b a1::bar(int)::KS
0000000000003920 b a1::bar(int)::D0B
00000000000039b0 b a1::bar(int)::PI0
0000000000003990 b a1::bar(int)::PIM
00000000000039a0 b a1::bar(int)::PIP


which generates a huge "bss" and most probably also a serious performance penalty due to all those gard variables

I worked around with this simple transformation
    static struct {
      const EvtId DM=EvtPDL::getId("D-");
      const EvtId DP=EvtPDL::getId("D+");
      const EvtId D0=EvtPDL::getId("D0");
      const EvtId D0B=EvtPDL::getId("anti-D0");
      const EvtId KM=EvtPDL::getId("K-");
      const EvtId KP=EvtPDL::getId("K+");
      const EvtId K0=EvtPDL::getId("K0");
      const EvtId KB=EvtPDL::getId("anti-K0");
      const EvtId KL=EvtPDL::getId("K_L0");
      const EvtId KS=EvtPDL::getId("K_S0");
      const EvtId PIM=EvtPDL::getId("pi-");
      const EvtId PIP=EvtPDL::getId("pi+");
      const EvtId PI0=EvtPDL::getId("pi0");
    } const parts;
  
so I am wandering if the complier would be able to do something similar,
recognizing that all those static objects can, after all, be guarded by just one variable (I think this will work no matter what side effects getId has)


---


### compiler : `gcc`
### title : `branch reordering missed optimization`
### open_at : `2012-06-29T10:36:33Z`
### last_modified_date : `2022-03-08T16:20:42Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=53804
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `unknown`
### severity : `enhancement`
### contents :
Consider this test case:

int
foo1 (int a, int b)
{
  if (a > 0)
    return 1;
  else if (b > 0 && a < 0)
    return -3;
  return 9;
}

int
foo2 (int a, int b)
{
  if (a > 0)
    return 1;
  else if (a < 0 && b > 0)
    return -3;
  return 9;
}


Ideally these two functions would be optimized to the same code, because they are semantically equivalent. The ideal form is foo2 because the result of the first comparison against "a" can be re-used for the second test, but GCC does not perform this optimization. The .227r.final dump looks like this on powerpc64-unknown-linux-gnu (all notes removed for readability):


;; Function foo1 (foo1, funcdef_no=0, decl_uid=1997, cgraph_uid=0)

   11 %7:CC=cmp(%3:SI,0)			# r7 = cmp(a,0)
    5 %9:DI=0x1					# r9 = 1
   12 pc={(%7:CC<=0)?L74:pc}			# if (r7 <= 0) goto L74
L20:
   26 %3:DI=%9:DI				# r3 = r9
   29 use %3:DI					# ..
   64 return					# return r3
i  63: barrier
L74:
   14 %7:CC=cmp(%4:SI,0)			# r7 = cmp (b,0)
    8 %9:DI=0x9					# r9 = 9
   15 pc={(%7:CC<=0)?L20:pc}			# if (r7 <= 0) goto L20
   53 %9:DI=-%3:DI==0				# r9 = -(r3==0)
   54 {%9:DI=%9:DI&0xc;clobber scratch;}	# r9 = r9 & 12
   55 %9:DI=%9:DI-0x3				# r9 = r9 - 3
   68 %3:DI=%9:DI				# r3 = r9
   69 use %3:DI					# ..
   70 return					# return r3
i  73: barrier

;; Function foo2 (foo2, funcdef_no=1, decl_uid=2001, cgraph_uid=1)

   11 %7:CC=cmp(%3:SI,0)			# r7 = cmp(a,0)
   12 pc={(%7:CC<=0)?L57:pc}			# if (r7 <= 0) goto L57
    5 %3:DI=0x1					# r3 = 1
   29 use %3:DI					# ..
   56 return					# return r3
i  55: barrier
L57:
   14 %7:CC=cmp(%3:DI,0)			# r7 = cmp(a,0) // ??? redundant
    8 %3:DI=0x9					# r3 = 9
   51 use %3:DI					# ..
   15 pc={(%7:CC==0)?return:pc}			# if (r7 == 0) return r3
   17 %7:CC=cmp(%4:SI,0)			# r7 = cmp(b,0)
   52 use %3:DI					# ..
   18 pc={(%7:CC<=0)?return:pc}			# if (r7 <= 0) return r3
    6 %3:DI=0xfffffffffffffffd			# r3 = -3
   53 use %3:DI					# ..
   54 return					# return r3
i  47: barrier


Note how foo1 needs two branches whereas foo2 only needs 1. 
(I'm not sure why there is the redundant compare in foo2:insn 14)


---


### compiler : `gcc`
### title : `Missed optimization (a<=b)&&(a>=b) with trapping`
### open_at : `2012-06-29T12:39:31Z`
### last_modified_date : `2023-08-04T22:34:57Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=53806
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.0`
### severity : `enhancement`
### contents :
Hello,

int f(double a,double b){
  if(a>=b) if(a<=b) return 1;
  return 0;
}

is optimized to:

  if(a==b) return 1;

only if I specify the flag -fno-trapping-math, not by default.

The test in combine_comparisons checks for any change in trapping behavior, whereas according to PR tree-optimization/53805 we are allowed to remove traps, just not add new ones (as would happen with ORD && UNLT -> LT for instance).


---


### compiler : `gcc`
### title : `Assignment of an array element from pointer is not taken as ARRAY_TYPE when expand_assignment`
### open_at : `2012-07-05T08:31:51Z`
### last_modified_date : `2021-12-19T00:35:29Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=53861
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.8.0`
### severity : `normal`
### contents :
In expr.c, there are comments and codes in function expand_assignment.

 /* Assignment of a structure component needs special treatment
     if the structure component's rtx is not simply a MEM.
     Assignment of an array element at a constant index, and assignment of
     an array element in an unaligned packed structure field, has the same
     problem.  Same for (partially) storing into a non-memory object.  */
  if (handled_component_p (to)
      || (TREE_CODE (to) == MEM_REF
          && mem_ref_refers_to_non_mem_p (to))
      || TREE_CODE (TREE_TYPE (to)) == ARRAY_TYPE)

But if an array element is accessed from a pointer, the condition check will fail. Here is an example:

void test1( unsigned char* t, unsigned char* t1);
void test (int i, int j)
{
  unsigned char *p;
  unsigned char a1[16];
  unsigned char a[8];
  p = &a;
  p[1] = 1;
  p[3] = 3;
  a1[2] = 6;
  test1(a, a1);
}

Compile it with -O2/Os. The t.c.149t.optimized is like:

;; Function test (test, funcdef_no=0, decl_uid=4059, cgraph_uid=0)
test (int i, int j)
{
  unsigned char a[8];
  unsigned char a1[16];
<bb 2>:
  MEM[(unsigned char *)&a + 1B] = 1;
  MEM[(unsigned char *)&a + 3B] = 3;
  a1[2] = 6;
  test1 (&a, &a1);
  a1 ={v} {CLOBBER};
  a ={v} {CLOBBER};
  return;
}

The MEM_REF is not taken as an array element access. Then their address will be simplified based on the sp during expanding. But in some targets (like ARM THUMB1), sp can not be used in some sore instructions, we have to reset the base address from sp before each reference.

If we take the MEM_REF as ARRAY_TYPE (by tracing its operand's TREE_TYPE, we can find it is from ARRAY_TYPE), we can keep the index mode during expanding.

After that, if the targets support sp used in store instructions (like X86, MIPS, ARM THUMB2 etc), fwprop1 can optimized it. Otherwise, just keep the index mode, then we need only set the base address once.


---


### compiler : `gcc`
### title : `[meta-bug] vectorizer missed-optimizations`
### open_at : `2012-07-13T08:29:00Z`
### last_modified_date : `2023-10-23T09:00:03Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=53947
### status : `NEW`
### tags : `meta-bug, missed-optimization`
### component : `tree-optimization`
### version : `4.8.0`
### severity : `enhancement`
### contents :



---


### compiler : `gcc`
### title : `((a ^ b) | a) not optimized to (a | b)`
### open_at : `2012-07-16T10:41:16Z`
### last_modified_date : `2021-07-28T22:19:54Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=53979
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.0`
### severity : `enhancement`
### contents :
The following 3 functions should ideally generate identical code (and they do
when using clang).

int f1(int a, int b) {
	int c = b;
	return (a ^ b ^ c) | (a ^ b) | a;
}
int f2(int a, int b) {
	return (a ^ b) | a;
}
int f3(int a, int b) {
	return a | b;
}

I tested gcc revision trunk@189510 and it shows 2 missed optimizations:

1) (a ^ b ^ b) not simplified to (a)
Normally gcc performs this optimization, but I *guess* it misses it here
because of the CSE opportunity with (a ^ b).

2) ((a ^ b) | a) not simplified to (a | b)


Of course in this example it's easy to manually rewrite the code. But in my
original code this function was actually a template and for some instantiations
the expression for the variable 'c' simplified to just 'b'. So the first missed
optimization is something I saw in real code. The second missed optimization
only occurs in this (much) simplified variant of the function.


---


### compiler : `gcc`
### title : `missed optimization opportunities for bool struct/class members`
### open_at : `2012-07-18T09:27:32Z`
### last_modified_date : `2021-07-23T21:52:41Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=54011
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.7.1`
### severity : `normal`
### contents :
Hi, when taking the following code (or on http://tinyurl.com/bs2qa3h to easier play with (leads to gcc explorer, might of course be inactive after some time))

#define BSET //:1
struct A
{
  bool b0 BSET;
  bool b1 BSET;
  bool b2 BSET;
  bool b3 BSET;
  bool b4 BSET;
  bool b5 BSET;
  bool b6 BSET;
  bool b7 BSET;
};
  //#define TO (__LINE__%2)
  #define TO 0
 void foo( A& a )
  {
    a.b0 = TO;
    a.b1 = TO;
    a.b2 = TO;
    a.b3 = TO;
   #if 1
    a.b4 = TO;
    a.b5 = TO;
    a.b6 = TO;
    a.b7 = TO;
    #endif
  }

I see some missed opportunities for optimization. While clang compiles this to:

	movq	$0, (%rdi)
	ret

gcc will compile this to:

	movb	$0, (%rdi)
	movb	$0, 1(%rdi)
	movb	$0, 2(%rdi)
	movb	$0, 3(%rdi)
	movb	$0, 4(%rdi)
	movb	$0, 5(%rdi)
	movb	$0, 6(%rdi)
	movb	$0, 7(%rdi)
	ret

What I think a good debugger should do is:

In case of bool being one byte, determine the longest "chain" of values being set, group them into useful operation sizes (2/4/8/16 bytes maybe) and create an appropriate value to store to that location. In the case of the bools being bitset members (above BSET define to try it out) gcc already seems to do this quite fine (things will get the appropriate and/or bitwise operations applied).


---


### compiler : `gcc`
### title : `Loop with control flow not vectorized`
### open_at : `2012-07-18T11:09:04Z`
### last_modified_date : `2023-10-20T21:41:23Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=54013
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.0`
### severity : `enhancement`
### contents :
ICC manages to vectorize the following loop which happens in Polyhedron mp_prop_design.

int foo (float x, float *tab)
{
  int i;
  for (i = 2; i < 45; ++i)
    if (x < tab[i])
      break;
  return i - 1;
}


---


### compiler : `gcc`
### title : `[SH] Tail calls with -fPIC use bsrf instead of braf`
### open_at : `2012-07-18T19:14:37Z`
### last_modified_date : `2021-09-12T22:26:44Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=54019
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.8.0`
### severity : `enhancement`
### contents :
The following function:

int a, b;

int bleh (int x, int y);

int foo (void)
{
  return bleh (a + b, a - b);
}

compiled with -m4 -O2 -ml -fPIC:

        mov.l   r12,@-r15       ! 42	movsi_ie/11	[length = 2]
        mova    .L3,r0          ! 44	mova	[length = 2]
        mov.l   .L3,r12         ! 45	movsi_ie/1	[length = 2]
        sts.l   pr,@-r15        ! 43	movsi_ie/13	[length = 2]
        add     r0,r12          ! 46	*addsi3_compact	[length = 2]
        mov.l   .L4,r0          ! 5	movsi_ie/1	[length = 2]
        mov.l   @(r0,r12),r2    ! 7	movsi_ie/7	[length = 2]
        mov.l   .L5,r0          ! 34	movsi_ie/1	[length = 2]
        mov.l   @r2,r5          ! 8	movsi_ie/7	[length = 2]
        mov.l   @(r0,r12),r1    ! 11	movsi_ie/7	[length = 2]
        mov     r5,r4           ! 37	movsi_ie/2	[length = 2]
        mov.l   @r1,r1          ! 12	movsi_ie/7	[length = 2]
        add     r1,r4           ! 15	*addsi3_compact	[length = 2]
        sub     r1,r5           ! 16	*subsi3_internal	[length = 2]
        mov.l   .L6,r1          ! 39	movsi_ie/1	[length = 2]
        bsrf    r1              ! 41	call_valuei_pcrel	[length = 4]
.LPCS0:
        nop
        lds.l   @r15+,pr        ! 55	movsi_ie/17	[length = 2]
        rts                     ! 58	*return_i	[length = 2]
        mov.l   @r15+,r12       ! 56	movsi_ie/7	[length = 2]
.L7:
        .align 2
.L3:
        .long   _GLOBAL_OFFSET_TABLE_
.L4:
        .long   _a@GOT
.L5:
        .long   _b@GOT
.L6:
	.long   __Z4blehii@PLT-(.LPCS0+2-.)
	.cfi_endproc

Instead of 'bsrf' the 'braf' instruction could be used.
Maybe this is a side effect of PR 12306.


---


### compiler : `gcc`
### title : `[11/12/13/14 regression] on powerpc64 gcc 4.9/8 generates larger code for global variable accesses than gcc 4.7`
### open_at : `2012-07-21T12:04:52Z`
### last_modified_date : `2023-07-07T10:29:45Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=54063
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `target`
### version : `4.8.0`
### severity : `normal`
### contents :
Consider this trivial test case, which scans for an element in a doubly-linked list that uses a separate sentinel object to represent the head and tail of the list:

struct list {
    struct list *next, *prev;
    int k;
} head = { &head, &head, 0 };

int lookup(int k)
{
    struct list *list = head.next;
    while (list != &head) {
        if (list->k == k)
            return 1;
        list = list->next;
    }
    return 0;
}

The code generated by gcc 4.8 and 4.7 on powerpc64-linux for this test case is similar, except gcc 4.8 generates an additional instruction at the start of the function when computing the address of the global variable 'head':

@@ -11,25 +11,26 @@
        .previous
        .type   lookup, @function
 .L.lookup:
+       addis 10,2,.LANCHOR0@toc@ha
        addis 8,2,.LANCHOR0@toc@ha
-       ld 9,.LANCHOR0@toc@l(8)
+       ld 9,.LANCHOR0@toc@l(10)
        addi 8,8,.LANCHOR0@toc@l
        cmpd 7,9,8

The rest is the same, modulo the numbers chosen for the labels.

The test case is reduced from similar code in the Linux kernel, see PR54062.


---


### compiler : `gcc`
### title : `[4.7 Regression] SciMark Monte Carlo test performance has seriously decreased in recent GCC releases`
### open_at : `2012-07-23T15:25:14Z`
### last_modified_date : `2023-05-17T00:11:32Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=54073
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.7.2`
### severity : `normal`
### contents :
Created attachment 27860
Sci Mark Monte Carlo test

On an Intel Core i7 CPU (see the attached screenshot):

GCC 4.2.x - 380
GCC 4.7.x - 265

i.e. 44% slower.

SciMark 2.0 sources can be fetched here: http://math.nist.gov/scimark2/download_c.html


---


### compiler : `gcc`
### title : `Bytemark ASSIGNMENT 10% slower with g++`
### open_at : `2012-07-24T12:38:15Z`
### last_modified_date : `2021-08-16T05:20:27Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=54081
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.7.1`
### severity : `normal`
### contents :
Bytemark is 10% slower if compiled with g++ than with gcc
gcc
ASSIGNMENT          :           63.36  :     241.10  :      62.53
g++
ASSIGNMENT          :          57.411  :     218.46  :      56.66

CFLAGS = -s -Wall -O3 -g0 -march=core2 -fomit-frame-pointer -funroll-loops -ffast-math -mssse3 -fno-PIE -fno-exceptions -fno-stack-protector

http://www.tux.org/~mayer/linux/nbench-byte-2.2.3.tar.gz


---


### compiler : `gcc`
### title : `[SH] Refactor shift patterns`
### open_at : `2012-07-24T23:41:46Z`
### last_modified_date : `2023-10-15T01:06:22Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=54089
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `target`
### version : `4.8.0`
### severity : `enhancement`
### contents :
The code related to shift patterns in sh.c / sh.md maybe could use some improvements here and there.  In some places clobbers and scratch regs could be avoided.
There is also a large part that deals with minimizing and-shift/shift-and sequences, but there are no test cases to verify that those actually work.
It would also be interesting to see, whether some of the and-shift/shift-and combine code could be reduced due to improvements in the middle-end.


---


### compiler : `gcc`
### title : `suboptimal code for tight loops`
### open_at : `2012-07-29T09:09:02Z`
### last_modified_date : `2021-08-07T05:39:30Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=54116
### status : `WAITING`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.7.1`
### severity : `normal`
### contents :
Consider following loop.

int recal(int *x){int i;
  for(i=0;;i+=4){
    if(__builtin_expect((x[i]|x[i+1])|(x[i+2]|x[i+3]),0))
      break;
  }
  return (x[i]|x[i+1])*(x[i+2]|x[i+3]);
}

On x64 orl instruction is destructive. Gcc saves intermediate result to
register instead recalculating it at end of loop, making loop run slower.

Relevant assembly output is following:

gcc-4.7 -O3 -S
        .file   "recal.c"
        .text
        .p2align 4,,15
        .globl  recal
        .type   recal, @function
recal:
.LFB0:
        .cfi_startproc
        movl    12(%rdi), %edx
        orl     8(%rdi), %edx
        movl    4(%rdi), %ecx
        orl     (%rdi), %ecx
        movl    %edx, %eax
        orl     %ecx, %eax
        jne     .L2
        leaq    16(%rdi), %rax
        .p2align 4,,10
        .p2align 3
.L3:
        movl    12(%rax), %edx
        orl     8(%rax), %edx
        movl    4(%rax), %ecx
        orl     (%rax), %ecx
        addq    $16, %rax
        movl    %edx, %esi
        orl     %ecx, %esi
        je      .L3
.L2:
        movl    %ecx, %eax
        imull   %edx, %eax
        ret
        .cfi_endproc
.LFE0:
        .size   recal, .-recal
        .ident  "GCC: (Debian 4.7.1-2) 4.7.1"
        .section        .note.GNU-stack,"",@progbits
--


---


### compiler : `gcc`
### title : `cprop_hardreg generates redundant instructions`
### open_at : `2012-08-01T14:33:43Z`
### last_modified_date : `2022-01-17T04:22:22Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=54154
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.6.3`
### severity : `enhancement`
### contents :
Created attachment 27922
Before cprop_hardreg

Hello,

I have touched this subject before:
* http://gcc.gnu.org/ml/gcc/2010-08/msg00347.html
* http://gcc.gnu.org/ml/gcc/2011-03/msg00214.html

and it looks like a long standing issue so I am wary of reporting a bug but I think I did find the culprit code. So, unless you consider this a feature somehow I reckon it's a bug.

cprop_hardreg grabs an insn chain and through forward propagation of registers ends up generating redundant passes where the src and dest are the same (same regnumber, same mode).

Consider the program (obtained using creduce):
int a;
int fn1 ();
void fn2 ();
int fn3 ();
int
fn4 ()
{
    if (fn1 ())
        return 0;
    a = fn3 ();
    if (a != (1 << (32 - (9 + 9))) - 1)
        fn2 (0, a);
    return (1 << (32 - (9 + 9))) - 1;
}

Now, after compiling for my backend with -Os I get before cprop_hardreg (after ce3) [real logs attached]:

#8     reg AL <- call fn1
#50/51 if_then_else AL != 0
         goto label 34

#12    AL <- call fn3
#13    AH <- AL
#14    mem sym a <- AH
#48/49 if_then_else AH == 16383
         goto label 38

#17    AL <- 0
#19    call fn2
#4     AL <- 16383
#43    jump label 20

label 34:
#3     AL <- 0
#45    jump label 20

label 38:
#5     AL <- AH

label 20:
       return

the number after '#' is the insn number.

cprop_hardreg decided to replace AH with AL so the top of cprop_hardreg shows:
rescanning insn with uid = 14.
deleting insn with uid = 14.
insn 14: replaced reg 0 with 1
insn 48: replaced reg 0 with 1
rescanning insn with uid = 48.
deleting insn with uid = 48.
rescanning insn with uid = 5.
deleting insn with uid = 5.
insn 5: replaced reg 0 with 1

reg 0 is AH and reg 1 is AL. 
When you replace in insn 5, AH by AL you get the insn AL <- AL and that's #5 after cprop_hardreg.

I find it strange that there's no code checking if set dest is equal to replacement and if it is, simply remove insn.

I think this is a bug and should be fixed.


---


### compiler : `gcc`
### title : `excessive alignment`
### open_at : `2012-08-03T15:03:04Z`
### last_modified_date : `2021-09-12T07:47:18Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=54167
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.8.0`
### severity : `normal`
### contents :
Compile the following code:

struct c
{
  int a, b;
  /*constexpr*/ c() : a(1), b(2) { }
};

c v;


The variable v will be defined with:

	.bss
	.align 16
	.type	v, @object
	.size	v, 8
v:
	.zero	8

The variable has alignment 16!

If you uncomment the constexpr and compile with -std=gnu++11 it can be seen that the compiler does know what the correct alignment is:

	.globl	v
	.data
	.align 4
	.type	v, @object
	.size	v, 8
v:
	.long	1
	.long	2


This happens with the current svn version as well as with 4.7.0.


---


### compiler : `gcc`
### title : `Missed optimization: Unnecessary vmovaps generated for __builtin_ia32_vextractf128_ps256(v, 0)`
### open_at : `2012-08-04T17:58:03Z`
### last_modified_date : `2021-08-23T11:28:48Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=54174
### status : `NEW`
### tags : `missed-optimization, ra`
### component : `target`
### version : `4.7.0`
### severity : `enhancement`
### contents :
Pasting the following test code into test.c and compiling with gcc -Wall -O -mavx -S test.c

----
typedef float v4sf __attribute__ ((vector_size (4*4)));
typedef float v8sf __attribute__ ((vector_size (4*8)));

v4sf add(v8sf v)
{
  v4sf a = __builtin_ia32_vextractf128_ps256(v, 0);
  v4sf b = __builtin_ia32_vextractf128_ps256(v, 1);
  return a + b;
}
----

makes gcc generate the following code:

	vmovaps	%xmm0, %xmm1
	vextractf128	$0x1, %ymm0, %xmm0
	vaddps	%xmm0, %xmm1, %xmm0

However if the statements for a and b are swapped, i.e.

  v4sf b = __builtin_ia32_vextractf128_ps256(v, 1);
  v4sf a = __builtin_ia32_vextractf128_ps256(v, 0);

then gcc is able to optimize away the vmovaps instruction:

	vextractf128	$0x1, %ymm0, %xmm1
	vaddps	%xmm1, %xmm0, %xmm0

It thus seems like optimization rules are in place to make __builtin_ia32_vextractf128_ps256(v, 0) a noop, however regardless of this a vmovaps is generated (or perhaps rather not optimized away) in most cases.


---


### compiler : `gcc`
### title : `XMM constant duplicated`
### open_at : `2012-08-08T11:31:14Z`
### last_modified_date : `2021-08-21T23:28:08Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=54201
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.6.3`
### severity : `normal`
### contents :
Created attachment 27960
Reduced testcase

When compiling the following small function (command line used "gcc -std=c99 -Wall -Wextra -Werror -O3 -save-temps -c pcmpeqb.c"):

#include <emmintrin.h>

__m128i test(__m128i value)
{
	__m128i mask = _mm_set1_epi8(1);
	return _mm_cmpeq_epi8(_mm_and_si128(value, mask), mask);
}

gcc creates two identical copies of the "mask" constant, one with repeated .quad, the other with repeated .byte:

[...]
	pand	.LC0(%rip), %xmm0
	pcmpeqb	.LC1(%rip), %xmm0
[...]
	.align 16
.LC0:
	.quad	72340172838076673
	.quad	72340172838076673
	.align 16
.LC1:
	.byte	1
	.byte	1
[...]

It should create and use only one copy of the constant.

With more complex code in which "test" is a inline function called several times, gcc uses two registers instead of one for the constant; it seems it cannot see it is the same value, even though it is explicitly the same value in the source code.

$ gcc -v
Using built-in specs.
COLLECT_GCC=gcc
COLLECT_LTO_WRAPPER=/usr/libexec/gcc/x86_64-redhat-linux/4.6.3/lto-wrapper
Target: x86_64-redhat-linux
Configured with: ../configure --prefix=/usr --mandir=/usr/share/man --infodir=/usr/share/info --with-bugurl=http://bugzilla.redhat.com/bugzilla --enable-bootstrap --enable-shared --enable-threads=posix --enable-checking=release --with-system-zlib --enable-__cxa_atexit --disable-libunwind-exceptions --enable-gnu-unique-object --enable-linker-build-id --enable-languages=c,c++,objc,obj-c++,java,fortran,ada,go,lto --enable-plugin --enable-java-awt=gtk --disable-dssi --with-java-home=/usr/lib/jvm/java-1.5.0-gcj-1.5.0.0/jre --enable-libgcj-multifile --enable-java-maintainer-mode --with-ecj-jar=/usr/share/java/eclipse-ecj.jar --disable-libjava-multilib --with-ppl --with-cloog --with-tune=generic --with-arch_32=i686 --build=x86_64-redhat-linux
Thread model: posix
gcc version 4.6.3 20120306 (Red Hat 4.6.3-2) (GCC)


---


### compiler : `gcc`
### title : `[SH] Improve addc and subc insn utilization`
### open_at : `2012-08-12T22:25:32Z`
### last_modified_date : `2023-07-22T03:07:22Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=54236
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `target`
### version : `4.8.0`
### severity : `enhancement`
### contents :
There are currently a couple of cases, where it would be better if addc or subc insns were used.  For example:

int test00 (int a, int b)
{
  return a + b + 1;
}


gets compiled to:

        mov     r4,r0   ! MT
        add     r5,r0   ! EX
        rts
        add     #1,r0   ! EX

could be better as:

        mov     r4,r0   ! MT
        sett    r5,r0   ! MT (SH4)
        rts
        addc    #1,r0   ! EX

As a proof of concept, I've applied the following to handle the above case:

Index: gcc/config/sh/sh.md
===================================================================
--- gcc/config/sh/sh.md	(revision 190326)
+++ gcc/config/sh/sh.md	(working copy)
@@ -1465,7 +1465,7 @@
 
 (define_insn "addc"
   [(set (match_operand:SI 0 "arith_reg_dest" "=r")
-	(plus:SI (plus:SI (match_operand:SI 1 "arith_reg_operand" "0")
+	(plus:SI (plus:SI (match_operand:SI 1 "arith_reg_operand" "%0")
 			  (match_operand:SI 2 "arith_reg_operand" "r"))
 		 (reg:SI T_REG)))
    (set (reg:SI T_REG)
@@ -1516,6 +1516,24 @@
   "add	%2,%0"
   [(set_attr "type" "arith")])
 
+(define_insn_and_split "*addsi3_compact"
+  [(set (match_operand:SI 0 "arith_reg_dest" "")
+	(plus:SI (plus:SI (match_operand:SI 1 "arith_reg_operand" "")
+		 	  (match_operand:SI 2 "arith_reg_operand" ""))
+		 (const_int 1)))
+   (clobber (reg:SI T_REG))]
+  "TARGET_SH1"
+  "#"
+  "&& 1"
+  [(set (reg:SI T_REG) (const_int 1))
+   (parallel [(set (match_dup 0)
+		   (plus:SI (plus:SI (match_dup 1)
+				     (match_dup 2))
+			    (reg:SI T_REG)))
+	      (set (reg:SI T_REG)
+		   (ltu:SI (plus:SI (match_dup 1) (match_dup 2))
+			   (match_dup 1)))])])
+
 ;; -------------------------------------------------------------------------
 ;; Subtraction instructions
 ;; -------------------------------------------------------------------------

.. and observed some code from the CSiBE set for -O2 -m4-single -ml -mpretend-cmove.  It doesn't affect code size that much (some incs/decs here and there), but more importantly it does this (libmpeg2/motion_comp.c):

_MC_avg_o_16_c:            --> 
        mov.b   @r5,r1			mov.b	@r5,r2
.L16:				.L16:
        mov.b   @r4,r2                  sett
        extu.b  r1,r1                   mov.b	@r4,r1
        extu.b  r2,r2                   extu.b	r2,r2
        add     r2,r1                   extu.b	r1,r1
        add     #1,r1                   addc	r2,r1
        shar    r1                      shar	r1
        mov.b   r1,@r4                  mov.b	r1,@r4
        mov.b   @(1,r5),r0              sett
        extu.b  r0,r1                   mov.b	@(1,r5),r0
        mov.b   @(1,r4),r0              extu.b	r0,r1
        extu.b  r0,r0                   mov.b	@(1,r4),r0
        add     r0,r1                   extu.b	r0,r0
        add     #1,r1                   addc	r1,r0
        shar    r1                      shar	r0
        mov     r1,r0                   mov.b	r0,@(1,r4)
        mov.b   r0,@(1,r4)

In such cases, the sett,addc sequence can be scheduled much better and in most cases the sett insn can be executed in parallel with some other insn.
Unfortunately, on SH4A the sett insn has been moved from MT group to EX group, but still it seems beneficial.  I've also seen a couple of places, where sett-subc sequences would be better.


---


### compiler : `gcc`
### title : `[SH] Add support for addv / subv instructions`
### open_at : `2012-08-15T16:02:51Z`
### last_modified_date : `2021-08-17T00:00:57Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=54272
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `target`
### version : `4.8.0`
### severity : `enhancement`
### contents :
The addv and subv instructions can be used for at least two things:

1) Implementing trapping signed integer arithmetic (-ftrapv)

   Currently, for the SH target, trapping insns (e.g. addvsi3) are
   supposed to be implemented by library functions in libgcc.
   However, it seems that for addvsi3 and subvsi3 normal addsi3 and
   subsi3 patterns are expanded by the middle-end, which is wrong.
   Probably PR 35412 is related to this.
   After adding the addvsi3 pattern to sh.md, the middle-end picks it up
   as expected.
   However, I'm unsure how to realize the actual trapping part.
   The library functions in libgcc just invoke 'abort ()' on overflow.
   I think the trapa instruction could be used here to get relatively
   compact code, like:
           addv  r4,r5
           bf    0f
           trapa #???
         0:
   However, I have no idea which trapa immediate value would be
   suitable for this, especially for GNU/Linux environments.
   Maybe it's better to make this user configurable through an -m option?

2) Saturating arithmetic

   E.g. the pattern ssaddsi3 can be implemented with the following
   sequence (if I'm not mistaken):
          mov.l  .Lintmin, r1  ! r1 = 0x80000000
          cmp/pz r4      ! only one sign matters in case of overflow 
          negc   r1,r2   ! r5 = 0 - r1 - T
          addv   r4,r5
          bf     0f
          mov    r2,r5
      0:
   However, I don't know how to make the middle-end expand patterns that
   contain 'ss_plus'.  It seems that other targets provide the ssaddsi3
   pattern through target specific built-in functions only...


---


### compiler : `gcc`
### title : `combine permutations`
### open_at : `2012-08-21T14:02:09Z`
### last_modified_date : `2022-10-25T05:53:24Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=54346
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.0`
### severity : `enhancement`
### contents :
Hello,

when we have two VEC_PERM_EXPR with constant mask, where one is the only user of the result of the other one, it would be good to compose/merge them into a single VEC_PERM_EXPR. However, it is too hard for backends to always generate optimal code for shuffles, so we want to do the optimization only if we know it actually helps. Currently this means when the composed permutation is the identity. In the future, it could mean asking the backend.

See the conversation that started at:
http://gcc.gnu.org/ml/gcc-patches/2012-08/msg00676.html

and around this message for cost hooks (which could also help the vectorizer):
http://gcc.gnu.org/ml/gcc-patches/2012-08/msg00973.html

Related bug is http://gcc.gnu.org/bugzilla/show_bug.cgi?id=43147 but that one is about RTL (unless x86 eventually follows ARM and decides to implement _mm_* functions in terms of __builtin_shuffle).


---


### compiler : `gcc`
### title : `recognize vector reductions`
### open_at : `2012-08-29T06:10:00Z`
### last_modified_date : `2021-09-13T21:54:40Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=54400
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.8.0`
### severity : `normal`
### contents :
Hello,

for this program:

#include <x86intrin.h>
double f(__m128d v){return v[1]+v[0];}

gcc -O3 -msse4 (same with -Os) generates:

	movapd	%xmm0, %xmm2
	unpckhpd	%xmm2, %xmm2
	movapd	%xmm2, %xmm1
	addsd	%xmm0, %xmm1
	movapd	%xmm1, %xmm0

(yes, the number of mov instructions is a bit high...)

Looking at the x86 backend, it can expand reduc_splus_v2df and __builtin_ia32_haddpd, but it doesn't provide any pattern that could be recognized. hsubpd is even less present.

It seems to me that, considering only the low part of the result of haddpd, the pattern should be small enough to be matched: (plus (vec_select (match_operand 1) const_a) (vec_select (match_dup 1) const_b)) where a and b are 0 and 1 in any order.


---


### compiler : `gcc`
### title : `Recognize (vec_)cond_expr in mask operation`
### open_at : `2012-09-08T12:02:36Z`
### last_modified_date : `2023-08-23T02:55:06Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=54525
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.8.0`
### severity : `enhancement`
### contents :
Hello,

it would be nice to recognize cond_expr and vec_cond_expr in (a&mask)|(b&~mask) where mask is (a vector of) 0 or -1. It would be particularly useful for vectors, for which we don't have any explicit way (yet?) to ask for a vec_cond_expr.

unsigned f(unsigned x,unsigned y,_Bool b){
  unsigned m=b?-1:0;
  return (x&m)|(y&~m);
}
unsigned g(unsigned x,unsigned y,_Bool b){
  return b?x:y;
}

typedef long vec __attribute__((vector_size(16)));
vec h(vec x, vec y, vec z, vec t){
  vec m=(z<t);
  return (x&m)|(y&~m);
}

compiled on x86_64 with -Ofast -mavx2, gives for f:

	movzbl	%dl, %edx
	negl	%edx
	movl	%edx, %eax
	andl	%edx, %edi
	notl	%eax
	andl	%esi, %eax
	orl	%edi, %eax

for g:

	movl	%edi, %eax
	testb	%dl, %dl
	cmove	%esi, %eax

and for h:

	vpcmpgtq	%xmm2, %xmm3, %xmm2
	vpcmpeqd	%xmm3, %xmm3, %xmm3
	vpxor	%xmm3, %xmm2, %xmm3
	vpand	%xmm0, %xmm2, %xmm2
	vpand	%xmm1, %xmm3, %xmm1
	vpor	%xmm2, %xmm1, %xmm0

(also notice that for some reason all comparisons (I tried < <= > >= and even with a ~ in front) generate a combination of gt and eq, never just gt)

while avx has vpblendvb.


---


### compiler : `gcc`
### title : `__builtin_shuffle: use psrldq+pslldq+por for rotations`
### open_at : `2012-09-13T12:46:27Z`
### last_modified_date : `2021-08-16T08:03:07Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=54566
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.8.0`
### severity : `enhancement`
### contents :
Hello,

this PR is based on those 2 emails:
http://gcc.gnu.org/ml/libstdc++/2012-09/msg00048.html
http://gcc.gnu.org/ml/libstdc++/2012-09/msg00050.html

which say that permutations that are rotations (like {1,2,3,4,5,6,7,0}) should more often be based on the rotation instructions (as in _mm_srli_si128 and _mm_slli_si128). Whether it is better than pshufb is not for me to say, but it could at least help where pshufb is not available. (256 bit AVX2 versions are also possible, although they require an additional lane swap)


---


### compiler : `gcc`
### title : `Missed optimization converting between bit sets`
### open_at : `2012-09-13T21:24:54Z`
### last_modified_date : `2023-06-07T15:20:26Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=54571
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.8.0`
### severity : `enhancement`
### contents :
When converting a bit set from one domain to another,code such as

  if (old & OLD_X) new |= NEW_X;
  if (old & OLD_Y) new |= NEW_Y;

is common.  If OLD_X and NEW_X are single bits, then this conversion
need not include any conditional code.  One can mask out OLD_X and
shift it left or right to become NEW_X.  Or, vice versa, shift left
or right and then mask out NEW_X.

Indeed, it's probably preferable to perform the mask with the smaller
of OLD_X and NEW_X in order to maximize the possibility of having a
valid immediate operand to the logical insn.

A test case that would seem to cover the all the cases, including 
converting logical not to bitwise not, would seem to be

int f1(int x, int y) { if (x & 1) y |= 1; return y; }
int f2(int x, int y) { if (x & 1) y |= 2; return y; }
int f3(int x, int y) { if (x & 2) y |= 1; return y; }
int g1(int x, int y) { if (!(x & 1)) y |= 1; return y; }
int g2(int x, int y) { if (!(x & 1)) y |= 2; return y; }
int g3(int x, int y) { if (!(x & 2)) y |= 1; return y; }

I'll also note that on the (presumably) preferred alternatives:

int h1(int x, int y) { return (x & 1) | y; }
int h2(int x, int y) { return ((x & 1) << 1) | y; }
int h3(int x, int y) { return ((x & 2) >> 1) | y; }
int k1(int x, int y) { return (~x & 1) | y; }
int k2(int x, int y) { return ((~x & 1) << 1) | y; }
int k3(int x, int y) { return ((~x >> 1) & 1) | y; }

there's some less-than-optimial code generated for k1 and k2.


---


### compiler : `gcc`
### title : `stack space allocated but never used when calling functions that return structs in registers`
### open_at : `2012-09-14T21:10:42Z`
### last_modified_date : `2021-12-18T23:59:46Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=54585
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.7.2`
### severity : `enhancement`
### contents :
Now that bug #44194 is fixed, and a returned structure used as a parameter is no longer stored unnecessarily, a new bug is visible: a stack frame is being allocated that is entirely unused.  On x86_64 target with the fix for 44194 backported to the 4.7 branch, this code:


#include <stdint.h>

struct blargh { uint32_t a, b, c; } foo();
void bar(uint32_t a, uint32_t b, uint32_t c);

void func() {
  struct blargh s = foo();
  bar(s.a, s.b, s.c);
}


no longer uses any stack memory at all, but still the function call reserves 24 bytes with "subq $24,%rsp" and promptly returns it with "addq $24,%rsp".   The generated code looks like this:

 func:
        .cfi_startproc
        xorl    %eax, %eax
        subq    $24, %rsp
        .cfi_def_cfa_offset 32
        call    foo
        movq    %rax, %rsi
        movl    %eax, %edi
        addq    $24, %rsp
        .cfi_def_cfa_offset 8
        shrq    $32, %rsi
        jmp     bar
        .cfi_endproc


---


### compiler : `gcc`
### title : `struct offset add should be folded into address calculation`
### open_at : `2012-09-15T13:36:51Z`
### last_modified_date : `2022-01-10T08:13:04Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=54589
### status : `REOPENED`
### tags : `missed-optimization`
### component : `target`
### version : `4.8.0`
### severity : `normal`
### contents :
Hi,

I found this in 4.4 (Ubuntu 10.04), and have confirmed it's still there in

  gcc (Debian 20120820-1) 4.8.0 20120820 (experimental) [trunk revision 190537]

This code:

  #include <emmintrin.h>

  struct param {
          int a, b, c, d;
          __m128i array[256];
  };

  void func(struct param *p, unsigned char *src, int *dst)
  {
          __m128i x = p->array[*src];
          *dst = _mm_cvtsi128_si32(x);
  }

compiles with -O2 on x86-64 to this assembler:

  0000000000000000 <func>:
     0:	0f b6 06             	movzbl (%rsi),%eax
     3:	48 83 c0 01          	add    $0x1,%rax
     7:	48 c1 e0 04          	shl    $0x4,%rax
     b:	8b 04 07             	mov    (%rdi,%rax,1),%eax
     e:	89 02                	mov    %eax,(%rdx)
    10:	c3                   	retq   

The add should be folded into the address calculation here. (The shl can't, because it's too big.) Curiously enough, if I misalign the struct element by removing c and d, and declaring the struct __attribute__((packed)), GCC will do that; the mov will then be from $8(%rdi,%rax,1),%eax and there is no redundant add.


---


### compiler : `gcc`
### title : `[SH] Unnecessary sign extension of logical operation results`
### open_at : `2012-09-22T23:12:31Z`
### last_modified_date : `2023-07-22T03:06:00Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=54673
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `target`
### version : `4.8.0`
### severity : `enhancement`
### contents :
Logical operations already sign extended values as inputs cause additional sign extensions of intermediate values.  For example:

int test00 (char* a, short* b, int c)
{
  return a[0] ^ a[1] ^ c;
}

becomes:
  mov.b    @(1,r4),r0
  mov.b    @r4,r1
  xor      r1,r0
  exts.b   r0,r0
  rts
  xor      r6,r0


int test01 (char* a, short* b, int c)
{
  return a[0] | a[1] | c;
}

becomes:
  mov.b    @(1,r4),r0
  mov.b    @r4,r1
  or       r1,r0
  exts.b   r0,r0
  rts
  or       r6,r0


int test02 (char* a, short* b, int c)
{
  return a[0] & a[1] & c;
}

becomes:
  mov.b    @(1,r4),r0
  mov.b    @r4,r1
  and      r1,r0
  exts.b   r0,r0
  rts
  and      r6,r0


This seems to be caused by the fact that patterns for xorsi3, iorsi3 and andsi3 allow matching 'subreg' in their operands.  In the combine pass it can be observed that it tries combinations such as:
Failed to match this instruction:
(set (reg:SI 173 [ D.1867 ])
    (sign_extend:SI (subreg:QI (xor:SI (subreg:SI (mem:QI (plus:SI (reg/v/f:SI 166 [ a ])
                            (const_int 1 [0x1])) [0 MEM[(char *)a_2(D) + 1B]+0 S1 A8]) 0)
                (subreg:SI (reg:QI 171 [ *a_2(D) ]) 0)) 3)))

which doesn't go anywhere.
I have quickly tried out prohibiting subreg in the operands of the *xorsi3_compact insn and the sign extension (as well as the subreg orgy in combine) disappeared.  However, I guess that not matching 'subreg' in the logical patterns will cause problems with DImode logical ops, since they are split into SImode ops working on subregs.


---


### compiler : `gcc`
### title : `sibling call optimization is not applied where it ought to be`
### open_at : `2012-10-01T19:14:04Z`
### last_modified_date : `2021-08-21T20:32:47Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=54770
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.5.2`
### severity : `enhancement`
### contents :
Created attachment 28317
Source file

"g++ -O2 -Wall -Wextra" fails to apply the sibling call optimization in the attached program.  The interesting portion is shown below:

struct MainNode : Node
{
  MainNode(NodePtr const & arg_) : Node(), arg(arg_) {}
  virtual ~MainNode() {}
  NodePtr arg;
  virtual void H()
  {
    // Extra scope guarantees there are no destructors following the tail call.
    {
      NodePtr tmp(arg);
      this->~Node();
      new(this) MainNode(tmp);
    }
    this->H(); // sibling call
  }
};

NodePtr is a class type.  If it is simply changed to Node *, then the optimization is applied.


---


### compiler : `gcc`
### title : `split FRAME variables back into pieces`
### open_at : `2012-10-02T10:11:28Z`
### last_modified_date : `2019-03-26T09:35:04Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=54779
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `enhancement`
### contents :
Created attachment 28323
Original implementation

When nested functions access local variables of their parent, the compiler 
creates a special FRAME local variable in the parent, which represents the 
non-local frame, and puts into it all the variables accessed non-locally.

If these nested functions are later inlined into their parent, these FRAME 
variables generally remain unmodified and this has various drawbacks:
 1) the frame of the parent is unnecessarily large,
 2) scalarization of aggregates put into the FRAME variables is hindered,
 3) debug info for scalars put into the FRAME variables is poor since VTA only 
works on GIMPLE registers.

The attached patch makes it so that the compiler splits FRAME variables back 
into pieces when all the nested functions have been inlined.  The transformation
is implemented as a sub-pass of execute_update_addresses_taken.  It also comes with a testcase.  Prerequisite is revision 191970.


        * gimple.c (gimple_ior_addresses_taken_1): Handle non-local frame
        structures specially.
        * tree-ssa.c (lookup_decl_for_field): New static function.
        (split_nonlocal_frames_op): Likewise.
        (execute_update_addresses_taken): Break up non-local frame structures
        into variables when possible.


---


### compiler : `gcc`
### title : `Trivial code changes result in different assembly with respect to rotations and bswap.`
### open_at : `2012-10-03T23:18:40Z`
### last_modified_date : `2022-02-01T12:43:54Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=54802
### status : `RESOLVED`
### tags : `missed-optimization, needs-bisection`
### component : `middle-end`
### version : `4.8.0`
### severity : `enhancement`
### contents :
Created attachment 28347
Code files

In some C code, manually inlining constants changes whether or not gcc compiles things to rotations or to bswaps.  In particular, the following code

uint64_t reverse0(uint64_t v) {
  v = ((v >> 1) & 0x5555555555555555ULL) | ((v & 0x5555555555555555ULL) << 1);
  v = ((v >> 2) & 0x3333333333333333ULL) | ((v & 0x3333333333333333ULL) << 2);
  v = ((v >> 4) & 0x0F0F0F0F0F0F0F0FULL) | ((v & 0x0F0F0F0F0F0F0F0FULL) << 4);
  v = ((v >> 8) & 0x00FF00FF00FF00FFULL) | ((v & 0x00FF00FF00FF00FFULL) << 8);
  v = ((v >> 16) & 0x0000FFFF0000FFFFULL) | ((v & 0x0000FFFF0000FFFFULL) << 16);
  const uint64_t
      va = ((v >> 32) & 0x00000000FFFFFFFFULL),
      vb = ((v & 0x00000000FFFFFFFFULL) << 32);
  v = va | vb;
  return v;
}

uint64_t reverse1(uint64_t v) {
  v = ((v >> 1) & 0x5555555555555555ULL) | ((v & 0x5555555555555555ULL) << 1);
  v = ((v >> 2) & 0x3333333333333333ULL) | ((v & 0x3333333333333333ULL) << 2);
  v = ((v >> 4) & 0x0F0F0F0F0F0F0F0FULL) | ((v & 0x0F0F0F0F0F0F0F0FULL) << 4);
  v = ((v >> 8) & 0x00FF00FF00FF00FFULL) | ((v & 0x00FF00FF00FF00FFULL) << 8);
  v = ((v >> 16) & 0x0000FFFF0000FFFFULL) | ((v & 0x0000FFFF0000FFFFULL) << 16);
  v = ((v >> 32) & 0x00000000FFFFFFFFULL) | ((v & 0x00000000FFFFFFFFULL) << 32);
  return v;
}

compiles to 

reverse0:
.LFB8:
	.cfi_startproc
	movq	%rdi, %rdx
	movabsq	$6148914691236517205, %rax
	movabsq	$3689348814741910323, %rcx
	shrq	%rdx
	andq	%rax, %rdx
	andq	%rdi, %rax
	addq	%rax, %rax
	orq	%rdx, %rax
	movq	%rax, %rdx
	andq	%rcx, %rax
	shrq	$2, %rdx
	salq	$2, %rax
	andq	%rcx, %rdx
	movabsq	$1085102592571150095, %rcx
	orq	%rdx, %rax
	movq	%rax, %rdx
	andq	%rcx, %rax
	shrq	$4, %rdx
	salq	$4, %rax
	andq	%rcx, %rdx
	orq	%rdx, %rax
	bswap	%rax
	ret
	.cfi_endproc
.LFE8:
	.size	reverse0, .-reverse0
	.p2align 4,,15
	.globl	reverse1
	.type	reverse1, @function
reverse1:
.LFB9:
	.cfi_startproc
	movq	%rdi, %rdx
	movabsq	$6148914691236517205, %rax
	movabsq	$3689348814741910323, %rcx
	shrq	%rdx
	andq	%rax, %rdx
	andq	%rdi, %rax
	addq	%rax, %rax
	orq	%rdx, %rax
	movq	%rax, %rdx
	andq	%rcx, %rax
	shrq	$2, %rdx
	salq	$2, %rax
	andq	%rcx, %rdx
	movabsq	$1085102592571150095, %rcx
	orq	%rdx, %rax
	movq	%rax, %rdx
	andq	%rcx, %rax
	shrq	$4, %rdx
	salq	$4, %rax
	andq	%rcx, %rdx
	movabsq	$71777214294589695, %rcx
	orq	%rdx, %rax
	movq	%rax, %rdx
	andq	%rcx, %rax
	shrq	$8, %rdx
	salq	$8, %rax
	andq	%rcx, %rdx
	movabsq	$281470681808895, %rcx
	orq	%rdx, %rax
	movq	%rax, %rdx
	andq	%rcx, %rax
	shrq	$16, %rdx
	salq	$16, %rax
	andq	%rcx, %rdx
	orq	%rdx, %rax
	rorq	$32, %rax
	ret
	.cfi_endproc
.LFE9:
	.size	reverse1, .-reverse1
	.p2align 4,,15
	.globl	reverse2
	.type	reverse2, @function


In the code that I'm using this in, reverse0 is 30% faster than reverse1.  I don't think that manual constant inlining, when each constant is used exactly once, should change the assembly code that gcc compiles to.

The relevant (.c, .i, .s, and a log of the command line) files are attached.


---


### compiler : `gcc`
### title : `Rotates are not vectorized`
### open_at : `2012-10-04T00:00:21Z`
### last_modified_date : `2021-08-24T22:50:50Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=54803
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.0`
### severity : `enhancement`
### contents :
Created attachment 28348
code files

Manually unfolding constants sometimes prevents vectorization.

For example, these loops vectorize:

void multi_left_shift0(uint64_t *const array, size_t len, size_t num_bits) {
  for (size_t i = 0; i < len; i++) {
    array[i] = (array[i] >> 31) | (array[i] << 31);
  }
}

void multi_left_shift2(uint64_t *const array, size_t len, size_t num_bits) {
  for (size_t i = 0; i < len; i++) {
    const uint64_t tempa = array[i] >> 32;
    const uint64_t tempb = array[i] << 32;
    array[i] = tempa | tempb;
  }
}


but this loops does not:

void multi_left_shiftb0(uint64_t *const array, size_t len, size_t num_bits) {
  for (size_t i = 0; i < len; i++) {
    array[i] = (array[i] >> 32) | (array[i] << 32);
  }
}


See attached file for the code, preprocessed code, gcc command line log, and assembly.


---


### compiler : `gcc`
### title : `[avr] shift is better than widening mul`
### open_at : `2012-10-04T18:27:57Z`
### last_modified_date : `2023-04-22T20:02:57Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=54816
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.8.0`
### severity : `normal`
### contents :
The following C test case 

int wmul (char a, char b)
{
    return a * (char) (b << 3);
}

$ avr-gcc wmul.c -S -Os -mmcu=atmega8 -dp

produces with current avr-gcc:


wmul:
	ldi r25,lo8(8)	 ;  25	movqi_insn/2	[length = 1]
	muls r22,r25	 ;  26	mulqihi3	[length = 3]
	movw r22,r0
	clr __zero_reg__
	muls r24,r22	 ;  17	mulqihi3	[length = 3]
	movw r24,r0
	clr __zero_reg__
	ret	 ;  29	return	[length = 1]
	.ident	"GCC: (GNU) 4.8.0 20121004 (experimental)"


avr-gcc-4.7 was smarter with its code:

wmul:
	lsl r22	 ;  10	*ashlqi3/5	[length = 3]
	lsl r22
	lsl r22
	muls r24,r22	 ;  12	mulqihi3	[length = 3]
	movw r22,r0
	clr __zero_reg__
	movw r24,r22	 ;  31	*movhi/1	[length = 1]
	ret	 ;  30	return	[length = 1]
	.ident	"GCC: (GNU) 4.7.2"


The 4.7 code is faster, smaller and has smaller register pressure.


---


### compiler : `gcc`
### title : `Large mode constant live in a register not used to optimize smaller mode constants`
### open_at : `2012-10-11T19:53:42Z`
### last_modified_date : `2023-07-22T06:14:36Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=54904
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.7.2`
### severity : `normal`
### contents :
void
foo (char *p)
{
  __builtin_memset (p, 0x11, 23);
}

results in terrible code on x86_64-linux at -O2:
        movabsq $1229782938247303441, %rax
        movl    $286331153, 16(%rdi)
        movb    $17, 22(%rdi)
        movq    %rax, (%rdi)
        movq    %rax, 8(%rdi)
        movl    $4369, %eax
        movw    %ax, 20(%rdi)
        ret
E.g.
        movabsq $1229782938247303441, %rax
        movl    %eax, 16(%rdi)
        movb    %al, 22(%rdi)
        movq    %rax, (%rdi)
        movq    %rax, 8(%rdi)
        movw    %ax, 20(%rdi)
        ret
would be 10 bytes shorter.  Guess we don't want to do this kind of optimizations before RA, it might increase register preassure, but somewhere close to final would be nice.  Use a register instead of immediate if it is available, makes the insn smaller and not slower.


---


### compiler : `gcc`
### title : `ARM: Missed optimization of very simple ctz function`
### open_at : `2012-10-12T14:02:54Z`
### last_modified_date : `2021-08-16T05:24:06Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=54910
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.7.2`
### severity : `enhancement`
### contents :
Given the following function:

/* Number of trailing zero bits in x. */
unsigned __attribute__((const))
ctz(unsigned x)
{
	static unsigned char const ctz_table[16] = {
		4, 0, 1, 0,  2, 0, 1, 0,
		3, 0, 1, 0,  2, 0, 1, 0
	};
	int bit = 28;

	if (x << 16)  x <<= 16, bit -= 16;
	if (x <<  8)  x <<=  8, bit -=  8;
	if (x <<  4)  x <<=  4, bit -=  4;
	return bit + ctz_table[x >> 28];
}
And the command line:

arm-linux-gnueabi-gcc-4.7 -W -Wall -O2 -mcpu=arm7tdmi -mthumb-interwork -marm -S baz.c

I get the following ARM code (-O2, -mthumb-interwork):

	.align	2
	.global	ctz
	.type	ctz, %function
ctz:
	@ Function supports interworking.
	@ args = 0, pretend = 0, frame = 0
	@ frame_needed = 0, uses_anonymous_args = 0
	@ link register save eliminated.
	movs	r3, r0, asl #16
	moveq	r3, r0
	movne	r2, #12
	moveq	r2, #28
	movs	r1, r3, asl #8
	movne	r3, r1
	subne	r2, r2, #8
	movs	r1, r3, asl #4
	movne	r3, r1
	ldr	r1, .L18
	ldrb	r0, [r1, r3, lsr #28]	@ zero_extendqisi2
	subne	r2, r2, #4
	add	r0, r0, r2
	bx	lr
.L19:
	.align	2
.L18:
	.word	.LANCHOR0
	.size	ctz, .-ctz
	.section	.rodata
	.align	2
.LANCHOR0 = . + 0
	.type	ctz_table.4122, %object
	.size	ctz_table.4122, 16
ctz_table.4122:
	.byte	4, 0, 1, 0, 2, 0, 1, 0, 3, 0, 1, 0, 2, 0, 1, 0
	.ident	"GCC: (Debian 4.7.2-1) 4.7.2"


What strikes me as strange about this code is that it uses 4-byte pointer
at .L18 to access an 16-byte table at .LANCHOR0.  Why the heck not just put
the table at .L18 directly and replace the ldr with an adr?  Save space and
time.


The thumb code is similar, but also fails to save the link register save,
despite the fact that this is an extremely simple leaf function:

	.align	2
	.global	ctz
	.code	16
	.thumb_func
	.type	ctz, %function
ctz:
	push	{lr}
	lsl	r3, r0, #16
	mov	r2, #12
	cmp	r3, #0
	bne	.L8
	mov	r3, r0
	mov	r2, #28
.L8:
	lsl	r1, r3, #8
	beq	.L9
	sub	r2, r2, #8
	mov	r3, r1
.L9:
	lsl	r1, r3, #4
	beq	.L10
	sub	r2, r2, #4
	mov	r3, r1
.L10:
	ldr	r1, .L18
	lsr	r3, r3, #28
	ldrb	r0, [r1, r3]
	@ sp needed for prologue
	add	r0, r0, r2
	pop	{r1}
	bx	r1


---


### compiler : `gcc`
### title : `No way to do if converison`
### open_at : `2012-10-15T13:25:47Z`
### last_modified_date : `2021-07-21T03:25:16Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=54935
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.0`
### severity : `enhancement`
### contents :
In a process of analyzing of gcc peformance on x86 including vectorization we found out that on spec2006/462.libquantum (e.g.file gates.c, routine quantum_cnot) vectorization of simple loop is not performed since if-conversion has not happened even if we pass explicit option to if-convert store stmt aka   "-ftree-loop-if-convert-stores". I can illustrate it on the following simple test-case:

extern int a[100], b[100];
void foo(int n)
{
  int i;
  
  for (i=1; i<n;i++) {
    if (a[i] != b[i])
	a[i] = b[i] + 1;
  }
}

Note that if I insert into loop "a[0] = 0;" stmt if conversion will happen but this is not suitable for the whole benchmark. I also tried to use lto that could detect writable memory access but without any success. I assume that we can detect writable accesses without having unconditional write to that memory but simple through object type specification of a given object. BTW I don't know how array a[] with external declaration must be defined to put in read-only section. Please, also check gcc external definition of "-ftree-loop-if-convert-stores" option that does not match with the following commentary:

/* Return true when the memory references of STMT won't trap in the
   if-converted code.  There are two things that we have to check for:

   - writes to memory occur to writable memory: if-conversion of
   memory writes transforms the conditional memory writes into
   unconditional writes, i.e. "if (cond) A[i] = foo" is transformed
   into "A[i] = cond ? foo : A[i]", and as the write to memory may not
   be executed at all in the original code, it may be a readonly
   memory.  To check that A is not const-qualified, we check that
   there exists at least an unconditional write to A in the current
   function.

   - reads or writes to memory are valid memory accesses for every
   iteration.  To check that the memory accesses are correctly formed
   and that we are allowed to read and write in these locations, we
   check that the memory accesses to be if-converted occur at every
   iteration unconditionally.  */

static bool
ifcvt_memrefs_wont_trap (gimple stmt, VEC (data_reference_p, heap) *refs)
{
  return write_memrefs_written_at_least_once (stmt, refs)
    && memrefs_read_or_written_unconditionally (stmt, refs);
}


---


### compiler : `gcc`
### title : `Bitfield test not optimised at -Os.`
### open_at : `2012-10-18T08:40:24Z`
### last_modified_date : `2022-01-05T10:26:31Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=54969
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.7.2`
### severity : `enhancement`
### contents :
Compiling with -Os, the compiler fails to detect that this loop will always execute at least once:

unsigned get (void);
void go (void)
{
    unsigned f;
    for (f = 1; f & 1; f = get());
}

The relevant assembly output:

	jmp	.L2
.L3:
	call	get
.L2:
	testb	$1, %al
	jne	.L3

With -O2 gcc does better, and removes the first jmp, giving:

.L2:
	call	get
	testb	$1, %al
	jne	.L2

This happens both on x86-64 and arm:

gcc (GCC) 4.7.2 20120921 (Red Hat 4.7.2-2)

arm-linux-gnu-gcc (GCC) 4.7.1 20120606 (Red Hat 4.7.1-0.1.20120606)


---


### compiler : `gcc`
### title : `Handle VEC_COND_EXPR better in tree-vect-generic.c`
### open_at : `2012-10-20T18:38:31Z`
### last_modified_date : `2022-02-14T07:14:23Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=55001
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.0`
### severity : `enhancement`
### contents :
Created attachment 28497
Old patch

Hello,

the code in tree-vect-generic.c to handle vector operations not provided by the target doesn't know VEC_COND_EXPR. That didn't matter when the vectorizer was the only producer, but front-ends are going to produce them as well any day now.

Attaching the patch I was using when experimenting, but IIRC it wasn't in a state for submission, and its assumption that the first argument can't be an SSA_NAME or a constant is now wrong.


---


### compiler : `gcc`
### title : `Useless stores generated for structures passed by value`
### open_at : `2012-10-22T16:38:48Z`
### last_modified_date : `2021-08-16T23:11:48Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=55026
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.8.0`
### severity : `enhancement`
### contents :
Multiple targets (including ARM, HPPA, and MIPS) generate inefficient code in functions taking struct arguments by value.  Consider this code:

struct foo {
    int a;
    int b;
};

int f(struct foo x)
{
    return x.a + x.b;
}

On ARM, this compiles to the following at -O3 optimisation:

f:
        @ args = 0, pretend = 0, frame = 8
        @ frame_needed = 0, uses_anonymous_args = 0
        @ link register save eliminated.
        sub     sp, sp, #8
        add     r3, sp, #8
        stmdb   r3, {r0, r1}
        ldmia   sp, {r0, r3}
        add     r0, r0, r3
        add     sp, sp, #8
        @ sp needed
        bx      lr

Note the entirely unnecessary (and inefficiently done to boot) storing and loading of the argument registers to/from the stack.

The x86_64 and SH4 targets do not show this behaviour.


---


### compiler : `gcc`
### title : `The options -flto and -On do not behave as described in GCC docs`
### open_at : `2012-10-27T19:27:38Z`
### last_modified_date : `2018-11-15T14:35:50Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=55102
### status : `RESOLVED`
### tags : `documentation, lto, missed-optimization`
### component : `lto`
### version : `4.8.0`
### severity : `normal`
### contents :
> Additionally, the optimization flags used to compile
> individual files are not necessarily related to those
> used at link time.  For instance,
>
>         gcc -c -O0 -flto foo.c
>         gcc -c -O0 -flto bar.c
>         gcc -o myprog -flto -O3 foo.o bar.o
>
> This produces individual object files with unoptimized
> assembler code, but the resulting binary myprog is
> optimized at -O3.  If, instead, the final binary is
> generated without -flto, then myprog is not optimized.

In fact, when you use -O3 when linking the .o files, it is already too late, the resulting binary will not be fully optimized. You need to compile the .c files with at least -O1. Thus, there is a bug either in GCC itself or in the documentation.

====== 8< ======
int foo(void)
{
  return 0;
}

int main(void)
{
  return foo();
}
====== >8 ======

$ gcc -flto -O0 -c foo.c -o foo-O0.o
$ gcc -flto -O1 -c foo.c -o foo-O1.o
$ gcc -flto -O0 foo-O0.o -o prog-O0-O0
$ gcc -flto -O3 foo-O0.o -o prog-O0-O3
$ gcc -flto -O0 foo-O1.o -o prog-O1-O0
$ gcc -flto -O3 foo-O1.o -o prog-O1-O3
$ nm -A prog-O0-O0 prog-O0-O3 prog-O1-O0 prog-O1-O3 | grep foo
prog-O0-O0:080483f0 t foo.2337
prog-O0-O3:080483f0 t foo.2337
prog-O1-O0:080483f0 t foo.2337

GCC 4.6 gives a slight different result:

$ nm -A prog-O0-O0 prog-O0-O3 prog-O1-O0 prog-O1-O3 | grep foo
prog-O0-O0:08048381 t foo.1988
prog-O0-O3:08048380 t foo.1988

(GCC 4.5 crashes.)


---


### compiler : `gcc`
### title : `Missed VRP with != 0 and multiply`
### open_at : `2012-10-31T21:51:35Z`
### last_modified_date : `2022-11-08T18:26:29Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=55157
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.0`
### severity : `enhancement`
### contents :
Testcase:
void gg(void);
int f(unsigned t)
{
  unsigned g = t*16;
  if (g==0)  return 1;
  gg();
  gg();
  gg();
  gg();
  gg();
  gg();
  if (g<=4)  return 1;
  return 0;
}

In the end there should only be one check for t == 0.
Yes this shows up in real code (well with the autovectorizer); See PR 55155


---


### compiler : `gcc`
### title : `missed optimizations with __builtin_bswap`
### open_at : `2012-11-02T09:59:31Z`
### last_modified_date : `2023-09-21T13:55:55Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=55177
### status : `RESOLVED`
### tags : `missed-optimization, TREE`
### component : `tree-optimization`
### version : `4.7.2`
### severity : `enhancement`
### contents :
extern int x;

void foo(void)
{
  int a = __builtin_bswap32(x);
  a &= 0x5a5b5c5d;
  x = __builtin_bswap32(a);
}

With GCC 4.7.2 (x86_64 Fedora) this compiles to:
foo:
.LFB0:
	.cfi_startproc
	movl	x(%rip), %eax
	bswap	%eax
	andl	$-1515936861, %eax
	bswap	%eax
	movl	%eax, x(%rip)
	ret
	.cfi_endproc


Surely the actual swap should be optimised out, and the 0x5a5b5c5d constant mask should be swapped instead so we just load, mask with 0x5d5c5b5a and store without any runtime swapping?

(See also PR42586 which may be related)


---


### compiler : `gcc`
### title : `[10/11/12/13/14 Regression] Expensive shift loop where a bit-testing instruction could be used`
### open_at : `2012-11-02T16:05:57Z`
### last_modified_date : `2023-05-20T05:08:36Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=55181
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.7.0`
### severity : `normal`
### contents :
The following C code:

unsigned char lfsr (unsigned long number)
{
  unsigned char b = 0;
  if (number & (1L << 29)) b++;
  if (number & (1L << 13)) b++;

  return b;
}

compiles to a right shift 29 bits of number which is very expensive because AVR has no barrel shifter.  Instead, a bit-testing instruction could be used which takes just a few cycles and not more than 100 like with the right shift.

4.6.2 uses a bit testing instruction.

== Command line ==


---


### compiler : `gcc`
### title : `vectorizer ignores __restrict__`
### open_at : `2012-11-05T11:51:24Z`
### last_modified_date : `2023-02-24T05:23:25Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=55213
### status : `UNCONFIRMED`
### tags : `alias, missed-optimization`
### component : `tree-optimization`
### version : `4.8.0`
### severity : `enhancement`
### contents :
I raised this issue before, still I think that with vectorization becoming more and more common aliasing starts to become an issue for both code-size and speed.

for all the loops below the compiler emits alias checks.
My desire would be that foo produces optimal code (possibly with much less __restrict__ in the code than what I used below), 
still even in the others functions __restrict__ is ignored

compiled as
c++ -Ofast -c soa.cc -std=gnu++11 -ftree-vectorizer-verbose=1 -Wall -march=corei7
with gcc version 4.8.0 20121028 (experimental) [trunk revision 192889] (GCC) 

#include<cstdint>
struct Soa {

  uint32_t * mem;
  uint32_t ns;
  uint32_t cp;
  int const * __restrict__   i() const  __restrict__ { return (int const* __restrict__)(mem);}
  float const * __restrict__ f() const  __restrict__ { return (float const* __restrict__)(mem+cp);}
  float const * __restrict__ g() const  __restrict__ { return (float const* __restrict__)(mem+2*cp);}

};


void foo(Soa const &  __restrict__  soa, float * __restrict__ res) {
  for(std::size_t i=0; i!=soa.ns; ++i)
    res[i] = soa.f()[i]+soa.g()[i];
}

void bar(Soa const & __restrict__ soa, float * __restrict__ res) {
  float const * __restrict__ f = soa.f(); float const * __restrict__ g = soa.g();
  int n = soa.ns; for(int i=0; i!=n; ++i)
    res[i] = f[i]+g[i];
}


inline
void add(float const * __restrict__ f, float const * __restrict__ g,float * __restrict__ res,int n) {
  for(int i=0; i!=n; ++i)
    res[i] = f[i]+g[i];
}

void add(Soa const & __restrict__ soa, float * __restrict__ res) {
   add(soa.f(),soa.g(),res,soa.ns);
}


---


### compiler : `gcc`
### title : `armv6 doesn't use unaligned access for packed structures`
### open_at : `2012-11-05T22:00:21Z`
### last_modified_date : `2023-02-25T06:50:04Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=55218
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.7.1`
### severity : `normal`
### contents :
Created attachment 28622
Test case

The GCC ARM target uses the armv6 and above unaligned loads for packed structures and block copies.  This works correctly for -march=armv7-a and -march=armv6t2, but generates the old byte-by-byte field access for -march=armv6.

The block copy is fine.  readelf -A shows that the compiler intended to use unaligned access.  I'm suspicious that GCC is using the extv pattern to extract the field, and this pattern is only available on cores with Thumb-2 support.


---


### compiler : `gcc`
### title : `[11/12/13/14 Regression] Botan performance regressions, other compilers generate better code than gcc`
### open_at : `2012-11-11T23:53:56Z`
### last_modified_date : `2023-07-07T10:29:49Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=55278
### status : `NEW`
### tags : `missed-optimization, ra`
### component : `rtl-optimization`
### version : `4.8.0`
### severity : `normal`
### contents :
Botan regressed significantly around October 23-25 when LRA was merged as can be seen http://gcc.opensuse.org/c++bench/botan/botan-summary.txt-1-0.html
Those are all quite straighforward internal loops so it may be easy enough to analyze what is going wrong.


---


### compiler : `gcc`
### title : `Make combine emit converted logical right shifts`
### open_at : `2012-11-13T01:12:40Z`
### last_modified_date : `2021-09-12T20:10:49Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=55306
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.8.0`
### severity : `enhancement`
### contents :
As of rev 193423 the combine pass can successfully convert arithmetic right shifts into logical right shifts, but will not split / emit them as individual insns if ...
* the target has arith. right shift patterns defined that match the shift
* the target does not have an insn that combine came up with, which inlcudes
  the logical shift.

There are some targets (SH, ARC, see PR 54089) where logical right shifts are cheaper than arithmetic right shifts.
Since combine already has shift conversion integrated, it would probably make sense to extend it, instead of replicating it in some separate pass or doing fancy stuff in the target code.
Ideally, whenever combine converts a arith shift into a logical shift it should look at the costs of the shifts and always split out the cheaper shift insn (if the target has a pattern for the logical shift).


---


### compiler : `gcc`
### title : `[TileGX] Passing structure by value on stack needlessly writes to and reads from memory`
### open_at : `2012-11-16T20:53:52Z`
### last_modified_date : `2022-11-09T15:59:31Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=55360
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.7.2`
### severity : `enhancement`
### contents :
#include <stdint.h>

struct bar { uint8_t a, b, c, d; };
struct bla { unsigned long a:8, b:8, c:8, d:8; };

uint64_t bar(struct bar);
uint64_t bla(struct bla);

uint64_t foo(uint8_t a, uint8_t b, uint8_t c, uint8_t d)
{ return bar((struct bar) { a, b, c, d }); }
 
uint64_t baz(uint8_t a, uint8_t b, uint8_t c, uint8_t d)
{ return bla((struct bla) { a, b, c, d }); }

when compiled with "gcc -Wall -std=gnu99 -O3 -S pbv.c" produces:

	.file	"pbv.c"
	.text
	.align 8
.global foo
	.type	foo, @function
foo:
.LFB0:
	.cfi_startproc
	{
	st	sp, lr
	.cfi_offset 55, 0
	move	r29, sp
	addi	r28, sp, -16
	}
	addi	sp, sp, -24
	.cfi_def_cfa_offset 24
	{
	st	r28, r29
	addi	r11, sp, 21
	addi	r10, sp, 20
	}
	{
	st1	r11, r1
	addi	r11, sp, 22
	}
	{
	st1	r11, r2
	addi	r11, sp, 23
	}
	{
	st1	r10, r0
	movei	r0, 0
	}
	st1	r11, r3
	ld4u	r10, r10
	{
	bfins	r0, r10, 0, 0+32-1
	jal	bar
	}
	addi	r29, sp, 24
	ld	lr, r29
	{
	
	addi	sp, sp, 24
	.cfi_restore 54
	.cfi_restore 55
	.cfi_def_cfa_offset 0
	jrp	lr
	}
	.cfi_endproc
.LFE0:
	.size	foo, .-foo
	.align 8
.global baz
	.type	baz, @function
baz:
.LFB1:
	.cfi_startproc
	{
	movei	r10, 0
	st	sp, lr
	.cfi_offset 55, 0
	move	r29, sp
	}
	{
	bfins	r10, r0, 0, 7
	addi	r28, sp, -8
	}
	{
	bfins	r10, r1, 8, 8+8-1
	addi	sp, sp, -16
	}
	.cfi_def_cfa_offset 16
	{
	bfins	r10, r2, 16, 16+8-1
	st	r28, r29
	}
	bfins	r10, r3, 24, 24+8-1
	{
	move	r0, r10
	jal	bla
	}
	addi	r29, sp, 16
	ld	lr, r29
	{
	
	addi	sp, sp, 16
	.cfi_restore 54
	.cfi_restore 55
	.cfi_def_cfa_offset 0
	jrp	lr
	}
	.cfi_endproc
.LFE1:
	.size	baz, .-baz
	.ident	"GCC: (GNU) 4.7.2"
	.section	.note.GNU-stack,"",@progbits

My expectation is that the foo and baz should compile identically, and should use the bfins bit-arithmetic functions like baz does, rather than redundant stores and loads to stack like foo does.

This is with a vanilla GCC 4.7.2 build on a Tilempower system (roughly CentOS 5.7).

The problem does not occur on Debian x86-64 with either GCC 4.4.6 or GCC 4.7.2.

Possibly related to http://gcc.gnu.org/bugzilla/show_bug.cgi?id=7061 (however that case seems to be fixed in 4.7.2).


---


### compiler : `gcc`
### title : `Extended shift instruction on x86-64 is not used, producing unoptimal code`
### open_at : `2012-12-04T00:06:00Z`
### last_modified_date : `2022-11-01T03:24:05Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=55583
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.8.0`
### severity : `enhancement`
### contents :
Created attachment 28866
Source code demonstrating bad code generation

On x86-64, extended shift instruction is not generated for some reason.
Combined with other problems this creates very bad code.

Test functions included for signed and unsigned 16,32,64-bit types for both left and right shifts and for constant n and function parameter n.

Code of this form:
  unsigned int a, b; const int n = 2;
  void test32l (void) { b = (b << n) | (a >> (32 - n)); }

expected code:
  mov     a(%rip),%eax
  shld    $0x2,%eax,b(%rip)
  ret

produced code:
  mov    b(%rip), %edx   ; Size of register used here depends on gcc version
  mov    a(%rip), %eax   ; Size of register used here depends on gcc version
  sal    $2, %edx        ; Size of register used here depends on gcc version
  shr    $25, %eax
  or     %edx, %eax
  mov    %eax, b(%rip)
  ret


Tested with:
COLLECT_GCC_OPTIONS='-v' '-c' '-save-temps' '-O2' '-Wall' '-W' '-o' 'gcc_shld_not_used' '-mtune=generic'

I tried gcc versions:
GNU C (Debian 4.7.2-4) version 4.7.2 (x86_64-linux-gnu)
GNU C (Debian 4.6.3-11) version 4.6.3 (x86_64-linux-gnu)
GNU C (Debian 4.5.3-9) version 4.5.3 (x86_64-linux-gnu)
GNU C (Debian 4.4.7-2) version 4.4.7 (x86_64-linux-gnu)
GNU C (GCC) version 4.8.0 20121203 (experimental) [trunk revision 194106] (x86_64-unknown-linux-gnu)

All produce the same code modulo register size differences mentioned above. gcc HEAD changes sal to leal (,%rcx,4),%eax


---


### compiler : `gcc`
### title : `excessive size of vectorized code`
### open_at : `2012-12-05T00:34:00Z`
### last_modified_date : `2021-08-07T23:09:57Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=55600
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `target`
### version : `4.8.0`
### severity : `normal`
### contents :
Consider following code:

int sum(int *s){long i;
  int su=0;
  for(i=0;i<128;i+=2) su+=s[i]*s[i+1];
  return su;
}

When compiled by latest gcc with -O3 then generated assembly has 1099 bytes.


---


### compiler : `gcc`
### title : `Missed value numbering to a constant`
### open_at : `2012-12-09T15:54:29Z`
### last_modified_date : `2023-08-08T06:56:18Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=55629
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.0`
### severity : `enhancement`
### contents :
Consider a classic example of non-distributivity of constant propagation:

int foo (int);
int foo (int c) {
  int a, b;
  if (c) { a = 3; b = 2; }
  else { a = 2; b = 3; }
  return a + b;
}

Value numbering should be able to determine that a+b=5. GCC successfully
optimizes the test case to just "return 5" with -ftree-pre, but with "only"
-ftree-fre (-O1) the equivalence is not noticed.


---


### compiler : `gcc`
### title : `bitfields and __attribute__((packed)) generate horrible code on x86_64`
### open_at : `2012-12-12T05:54:10Z`
### last_modified_date : `2023-07-19T04:11:33Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=55658
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.7.1`
### severity : `enhancement`
### contents :
Created attachment 28932
Simple source code to exhibit the problem; disassembly (as produced by objdump -d)

I have a structure defined as:

struct D {
  uint64_t id_ : 63;
  bool x_ : 1;
} __attribute__((packed));

uint64_t D_id(const struct D* p) { return p->id_; }

The generated code for D_id (using gcc 4.7.1 -O2 on Linux x86_64) builds the return value byte by byte and masks out the most significant bit from the last byte.

Removing __attribute__((packed)) and/or changing the structure so it is no longer a bitfield generates sane code.

This happens in both C and C++ (unsurprisingly).


---
