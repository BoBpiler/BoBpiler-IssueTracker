### Total Bugs Detected: 4649
### Current Chunk: 7 of 30
### Bugs in this Chunk: 160 (From bug 961 to 1120)
---


### compiler : `gcc`
### title : `inefficient vectorization of compare into bytes on amd64`
### open_at : `2014-03-18T21:40:54Z`
### last_modified_date : `2021-08-15T22:51:59Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=60575
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.0`
### severity : `enhancement`
### contents :
this code comparing shorts into chars:

void __attribute__((optimize("O3"))) f(char * a_, short * b_) 
{
    char * restrict a = __builtin_assume_aligned(a_, 16);
    short * restrict b = __builtin_assume_aligned(b_, 16);
    for (int i = 0; i < 1024; i++) {
        a[i] = 6 < b[i];
    }   
}

vectorizes with gcc 4.8.2 (gcc file.c -c -std=c99) too:

  22:	movdqa (%rsi,%rax,2),%xmm0
  27:	movdqa 0x10(%rsi,%rax,2),%xmm1
  2d:	pcmpgtw %xmm4,%xmm0
  31:	pcmpgtw %xmm4,%xmm1
  35:	pand   %xmm3,%xmm0
  39:	pand   %xmm3,%xmm1
  3d:	movdqa %xmm0,%xmm2
  41:	punpcklbw %xmm1,%xmm0
  45:	punpckhbw %xmm1,%xmm2
  49:	movdqa %xmm0,%xmm1
  4d:	punpcklbw %xmm2,%xmm0
  51:	punpckhbw %xmm2,%xmm1
  55:	movdqa %xmm0,%xmm2
  59:	punpcklbw %xmm1,%xmm0
  5d:	punpckhbw %xmm1,%xmm2
  61:	punpcklbw %xmm2,%xmm0
  65:	movdqa %xmm0,(%rdi,%rax,1)
  6a:	add    $0x10,%rax
  6e:	cmp    $0x400,%rax
  74:	jne    22 <f+0x22>

which is relatively inefficient compared to using pack instructions which would look about like this (unrolled twice):

  b3:	movdqa (%rsi,%rax,2),%xmm1
  b8:	movdqa 0x10(%rsi,%rax,2),%xmm0
  be:	pcmpgtw %xmm2,%xmm1
  c2:	pcmpgtw %xmm2,%xmm0
  c6:	packsswb %xmm0,%xmm1
  ca:	pand   %xmm3,%xmm1
  ce:	movdqa %xmm1,(%rdi,%rax,1)
  d3:	add    $0x10,%rax
  d7:	cmp    $0x400,%rax
  dd:	jne    b3 <g+0x16>

this can also be applied to larger sizes including floating point by adding more packs.


---


### compiler : `gcc`
### title : `Converting ushort to offset on x86_64 generates double movzwl`
### open_at : `2014-03-24T20:59:08Z`
### last_modified_date : `2021-08-19T05:25:52Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=60641
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.7.3`
### severity : `enhancement`
### contents :
The following test cases produce sub-optimal assembly output.
This was verified with these three versions of gcc:
gcc (Ubuntu/Linaro 4.6.3-1ubuntu5) 4.6.3
gcc (SUSE Linux) 4.7.3
gcc (Debian 4.8.2-16) 4.8.2


#include <stdlib.h>
unsigned short
foo (const unsigned short *start, const unsigned char *mask)
{
   unsigned short r = 0;
   unsigned short ux = *start;
   if (mask[ux])
     r = ux;
   return r;
}
void bar(unsigned int *s, unsigned short a)
{
  s[a] = a;
}


Compile with, e.g., 

gcc -std=c99 -g -W -Wall -O3 -c movzwl.c

The effect also occurs when using -O2 instead.

The foo() function contains:
   0x0000000000000000 <+0>:     movzwl (%rdi),%edx
   0x0000000000000003 <+3>:     xor    %eax,%eax
   0x0000000000000005 <+5>:     movzwl %dx,%ecx
   0x0000000000000008 <+8>:     cmpb   $0x0,(%rsi,%rcx,1)


The foo() function is:
   0x0000000000000010 <+0>:     movzwl %si,%eax
   0x0000000000000013 <+3>:     movzwl %si,%esi
   0x0000000000000016 <+6>:     mov    %esi,(%rdi,%rax,4)
   0x0000000000000019 <+9>:     retq   


In both cases, an unnecessary movzwl instruction is generated. This may be the same issue as #36873, which was rejected because the test cases used volatile accesses. These test cases here show that the duplicate movzwl occurs without volatile as well.


---


### compiler : `gcc`
### title : `Investigate improved complex division algorithms`
### open_at : `2014-03-25T08:13:42Z`
### last_modified_date : `2021-08-16T08:31:06Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=60646
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `unknown`
### severity : `enhancement`
### contents :
The paper http://arxiv.org/abs/1210.4539 analyzes several algorithms for complex division. Currently GFortran IIRC uses the Smith (1962) algorithm. We should investigate whether GFortran could switch to one of the improved algorithms without compromising performance too much.


---


### compiler : `gcc`
### title : `VRP misses asserts for some already defined statements`
### open_at : `2014-03-26T12:13:37Z`
### last_modified_date : `2021-11-15T08:30:50Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=60669
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `enhancement`
### contents :
Take (derived from gcc.dg/tree-ssa/vrp65.c):
extern void link_error (void);

void
f7 (int s)
{
  unsigned t = s;
  if ((s & 0x3cc0) == 0x3cc0)
    {
      if (t <= 0x3cbf)
	link_error ();
    }
  else
    {
      if (t + 64 <= 63)
	link_error ();
    }
}

--- CUT ---
Notice how VRP does not insert an assert for t in either side of the if statement even though it could figure out its range.

This shows up when I was adding a pass which takes common code and hoists them up.


---


### compiler : `gcc`
### title : `"restrict" qualifier ignored on local variable`
### open_at : `2014-03-30T17:51:43Z`
### last_modified_date : `2022-12-26T06:39:53Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=60712
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.2`
### severity : `normal`
### contents :
Created attachment 32490
Test case

Version: x86_64-w64-mingw32-gcc 4.8.2 (standard Cygwin binaries)
Flags: gcc -std=c99 -O3

sum()'s loop is optimized into a single multiply, as it should.

But when inlined automatically by the compiler or "manually" by applying restrict qualifiers to local variables, the optimization fails.

This is might be the same as bug 58526. However, -fdump-tree-alias shows that inlining removed all restrict qualifiers, whereas they are still present in the type information of bug_when_local_variable(), so perhaps there are two distinct bugs here.


---


### compiler : `gcc`
### title : `combine is overly cautious when operating on volatile memory references`
### open_at : `2014-04-03T15:41:42Z`
### last_modified_date : `2023-09-25T07:09:27Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=60749
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.9.0`
### severity : `normal`
### contents :
Curtesy of volatile_ok / init_recog_no_volatile, combine will
reject any combination that involves a volatile memref in the combined
pattern.

In particular, if any narrow memory location is read on a WORD_REGISTER_OPERATIONS target, the zero/sign extension can't be combined
with a memory read, even if a suitably extending memory load instruction is
available - unless that pattern gets specifically written to accept
volatile memrefs, shunning the standard memory_operand and
general_operand predicates.

combine already needs to do special checks to make sure it doesn't
slip up when handling such patterns (E.g. see PR51374), so what good
does init_recog_non_volatile do combine these days?

At the very least, I think we should allow combinations involving a single
memref with unchanged mode before and after combination - that woud cover
the zero and sign extending loads.


---


### compiler : `gcc`
### title : `shift not folded into shift on x86-64`
### open_at : `2014-04-07T16:00:57Z`
### last_modified_date : `2021-09-27T08:22:14Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=60778
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.9.0`
### severity : `enhancement`
### contents :
On this C code:

double mem[4096];
double foo(long x) {
  return mem[x>>3];
}

GCC emits this x86-64 code:

        sarq    $3, %rdi
        movsd   mem(,%rdi,8), %xmm0

The following x86-64 code would be preferrable:

        andq    $-8, %rdi
        movsd   mem(%rdi), %xmm0

since it has smaller code size, and avoids using a scaled index which costs an extra micro-op on some microarchitectures.

The same situation arrises on 32-bit x86 also.

This was observed on all GCC versions currently on the GCC Explorer website [0], with the latest at this time being 4.9.0 20130909.

[0] http://gcc.godbolt.org/


---


### compiler : `gcc`
### title : `inefficient code for vector xor on SSE2`
### open_at : `2014-04-11T18:08:59Z`
### last_modified_date : `2021-07-26T22:03:30Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=60826
### status : `RESOLVED`
### tags : `missed-optimization, ra`
### component : `target`
### version : `4.9.0`
### severity : `normal`
### contents :
On the following C testcase:

#include <stdint.h>

typedef double v2f64 __attribute__((__vector_size__(16), may_alias));
typedef int64_t v2i64 __attribute__((__vector_size__(16), may_alias));

static inline v2f64 f_and   (v2f64 l, v2f64 r) { return (v2f64)((v2i64)l & (v2i64)r); }
static inline v2f64 f_xor   (v2f64 l, v2f64 r) { return (v2f64)((v2i64)l ^ (v2i64)r); }
static inline double vector_to_scalar(v2f64 v) { return v[0]; }

double test(v2f64 w, v2f64 x, v2f64 z)
{
    v2f64 y = f_and(w, x);

    return vector_to_scalar(f_xor(z, y));
}

GCC emits this code:

	andpd	%xmm1, %xmm0
	movdqa	%xmm0, %xmm3
	pxor	%xmm2, %xmm3
	movdqa	%xmm3, -24(%rsp)
	movsd	-24(%rsp), %xmm0
	ret

GCC should move the result of the xor to the return register directly instead of spilling it. Also, it should avoid the first movdqa, which is an unnecessary copy.

Also, this should ideally use xorpd instead of pxor, to avoid a domain-crossing penalty on Nehalem and other micro-architectures (or xorps if domain-crossing doesn't matter, since its smaller).


---


### compiler : `gcc`
### title : `Wrong decision in decide_alg in i386.c`
### open_at : `2014-04-18T00:33:02Z`
### last_modified_date : `2021-08-28T19:02:34Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=60879
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `5.0`
### severity : `normal`
### contents :
decide_alg has

  /* Very tiny blocks are best handled via the loop, REP is expensive to
     setup.  */
  else if (expected_size != -1 && expected_size < 4)
    return loop_1_byte;

We use 1-byte loop on fixed size 1, 2 and 3.  We should simply unroll
loop.


---


### compiler : `gcc`
### title : `x86 vector widen multiplication by constant is not replaced with shift and sub`
### open_at : `2014-04-18T15:28:23Z`
### last_modified_date : `2021-08-21T18:47:21Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=60888
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `5.0`
### severity : `enhancement`
### contents :
Created attachment 32631
test case

For the following test case:

void
foo(char *out, char *in)
{
  int i;
  for(i = 0; i < 1024; i++)
    out[i] = (in[i] * 32767) >> 15;
}

compiled with:
-O3 -m32 -msse2 -S -fdump-tree-vect-details

Generates the following code at 114t.vect:

  vect_cst_.16_106 = { 32767, 32767, 32767, 32767, 32767, 32767, 32767, 32767 }; 
  ...
  vect_patt_24.15_107 = WIDEN_MULT_LO_EXPR <vect__25.14_104, vect_cst_.16_106>;
  vect_patt_24.15_108 = WIDEN_MULT_HI_EXPR <vect__25.14_104, vect_cst_.16_106>;
  vect_patt_24.15_109 = WIDEN_MULT_LO_EXPR <vect__25.14_105, vect_cst_.16_106>;
  vect_patt_24.15_110 = WIDEN_MULT_HI_EXPR <vect__25.14_105, vect_cst_.16_106>;

These 4 multiplications stay till final assembler:
...
  punpcklbw  %xmm0, %xmm2
  punpckhbw  %xmm0, %xmm5
  pmullw     %xmm2, %xmm1 
  movdqa     %xmm1, %xmm0 
  pmulhw     %xmm3, %xmm2
...

However:

 out[i] = ((in[i] << 15) - in[i]) >> 15;

is faster and calculating the same.


---


### compiler : `gcc`
### title : `-Os generate much bigger code`
### open_at : `2014-04-18T16:50:43Z`
### last_modified_date : `2021-09-27T00:37:33Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=60889
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `5.0`
### severity : `normal`
### contents :
On Linux/x86-64:

[hjl@gnu-6 gcc]$ cat /tmp/space.i
typedef float __v4sf __attribute__ ((__vector_size__ (16)));
typedef float __m128 __attribute__ ((__vector_size__ (16), __may_alias__));
struct S
{
  __m128 a, b;
};

struct T
{
  int a;
  struct S s;
};


void foo (struct T *p, __m128 v)
{
  struct S s;

  s = p->s;
  s.b = (__m128) __builtin_ia32_addps ((__v4sf)s.b, (__v4sf)v);
  p->s = s;
}
[hjl@gnu-6 gcc]$ ./xgcc -B./ -S -O2 /tmp/space.i 
[hjl@gnu-6 gcc]$ cat space.s 
	.file	"space.i"
	.section	.text.unlikely,"ax",@progbits
.LCOLDB0:
	.text
.LHOTB0:
	.p2align 4,,15
	.globl	foo
	.type	foo, @function
foo:
.LFB0:
	.cfi_startproc
	addps	32(%rdi), %xmm0
	movaps	%xmm0, 32(%rdi)
	ret
	.cfi_endproc
.LFE0:
	.size	foo, .-foo
	.section	.text.unlikely
.LCOLDE0:
	.text
.LHOTE0:
	.ident	"GCC: (GNU) 4.9.0 20140409 (experimental)"
	.section	.note.GNU-stack,"",@progbits
[hjl@gnu-6 gcc]$ ./xgcc -B./ -S -Os /tmp/space.i 
[hjl@gnu-6 gcc]$ cat space.s 
	.file	"space.i"
	.section	.text.unlikely,"ax",@progbits
.LCOLDB0:
	.text
.LHOTB0:
	.globl	foo
	.type	foo, @function
foo:
.LFB0:
	.cfi_startproc
	movq	%rdi, %rax
	movl	$8, %ecx
	leaq	-40(%rsp), %rdi
	leaq	16(%rax), %rsi
	rep movsl
	addps	32(%rax), %xmm0
	leaq	16(%rax), %rdi
	leaq	-40(%rsp), %rsi
	movb	$8, %cl
	movaps	%xmm0, -24(%rsp)
	rep movsl
	ret
	.cfi_endproc
.LFE0:
	.size	foo, .-foo
	.section	.text.unlikely
.LCOLDE0:
	.text
.LHOTE0:
	.ident	"GCC: (GNU) 4.9.0 20140409 (experimental)"
	.section	.note.GNU-stack,"",@progbits
[hjl@gnu-6 gcc]$ 

analyze_all_variable_accesses in tree-sra.c has

  max_total_scalarization_size = UNITS_PER_WORD * BITS_PER_UNIT
    * MOVE_RATIO (optimize_function_for_speed_p (cfun));

-Os sets MOVE_RATIO to 3.  Should we have a different parameter
to control SRA?


---


### compiler : `gcc`
### title : `[arm] gcc fails to tail call __builtin_ffsll`
### open_at : `2014-04-22T09:59:01Z`
### last_modified_date : `2021-08-16T06:39:48Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=60919
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.9.0`
### severity : `enhancement`
### contents :
The following code compiled with gcc 4.9 at -O2:

int
__ffsll (long long int x)
{
  return __builtin_ffsll (x);
}

Generates:

00000000 <__ffs>:
   0:	b508      	push	{r3, lr}
   2:	f7ff fffe 	bl	0 <__ffsdi2>
   6:	bd08      	pop	{r3, pc}

This looks like it would be much better to just tail call __ffsdi2.


---


### compiler : `gcc`
### title : `-Os -fprofile-arcs breaks __attribute__((error()))`
### open_at : `2014-04-23T11:50:16Z`
### last_modified_date : `2021-12-09T09:23:42Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=60937
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.8.2`
### severity : `normal`
### contents :
Created attachment 32660
Reduced test case

Use of -Os and -fprofile-arcs break __attribute__((error())) behavior on attached test case. It false-positively triggers compile time error:

$ gcc -Wall -Os -fprofile-arcs -c -o mm/.tmp_gup.o gup.i
gup.i: In function ‘__get_user_pages’:
gup.i:29:44: error: call to ‘__compiletime_assert’ declared with attribute error: BUILD_BUG failed
                        __compiletime_assert();

Switching to other optimization level (above 0) or remove -fprofile-arcs does not lead to that:

$ gcc -Wall -O1 -fprofile-arcs -c -o mm/.tmp_gup.o gup.i
$ gcc -Wall -Os -c -o mm/.tmp_gup.o gup.i


---


### compiler : `gcc`
### title : `b+(-2.f)*a generates multiplication instruction while b-2.f*a simplifies to addition&subtraction`
### open_at : `2014-04-25T10:39:08Z`
### last_modified_date : `2021-12-25T09:44:59Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=60962
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.8.1`
### severity : `enhancement`
### contents :
Created attachment 32681
A procedure compilable into assembly to reproduce the bug

I've tried the following with -O3 -ffast-math -fassociative-math options (here all operands are floats):

float lap0= point[-1]+point[1] + (-2.f)*point[0];

This part of code (compilable into assembly version attached) generates mulss/addss code (adding a constant in .rodata and reading it before) , which leads to 6% slowdown compared to this version:

float lap0= point[-1]+point[1] - 2.f*point[0];

, which generates addss/subss code.

My g++ version is g++ (Ubuntu 4.8.1-2ubuntu1~12.04) 4.8.1. The full command line is:

g++ -O3 -ffast-math -fassociative-math -o test1.s -S -masm=intel test.cpp

The problem also reproduces with g++ 4.5.


---


### compiler : `gcc`
### title : `Bad code (I.e. needless insns) with option momit-leaf-frame-pointer; side-effect on non-leaf functions`
### open_at : `2014-04-29T07:12:53Z`
### last_modified_date : `2021-09-27T01:49:09Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=60996
### status : `WAITING`
### tags : `missed-optimization`
### component : `target`
### version : `4.8.2`
### severity : `minor`
### contents :
Using the option '-momit-leaf-frame-pointer' (with -fno-omit-frame-pointer) has a side-effect on non-leaf functions. The code-snippets afterwards (produced with an i386-elf cross-compiler for an IA32-target) will show the difference:

A) Without the option momit-leaf-frame-pointer:

Example1:
  pushl %ebp
  movl  %esp, %ebp
  pushl %ebx
  subl  $8, %esp
  movl  (%eax), %ebx
  pushl 12(%ebp)
  pushl 8(%ebp)
  pushl %ecx
  pushl %edx
  pushl %eax
  call  *12(%ebx)
  movl  -4(%ebp), %ebx
  leave
  ret

B) Option '-momit-leaf-frame-pointer' used:

Example1:
  pushl %ebp
  movl  %esp, %ebp
  pushl %ebx
  subl  $8, %esp
  movl  (%eax), %ebx
  pushl 12(%ebp)
  pushl 8(%ebp)
  pushl %ecx
  pushl %edx
  pushl %eax
  call  *12(%ebx)
  addl  $24, %esp
  movl  -4(%ebp), %ebx
  leave
  ret

In this case there'a an additional stack-adjustment (addl $24, %esp) before the "final" stack-leave instruction. Some other examples with less forwarded call-arguments have shown a few pop-insn instead of an 'add'.
These additional instruction(s) directly before reverting the stack-frame has no functional effect, but will consume a few CPU-cycles.


---


### compiler : `gcc`
### title : `No loop interchange for inner loop along the slow index`
### open_at : `2014-04-29T13:00:11Z`
### last_modified_date : `2019-08-19T05:10:18Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=61000
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `5.0`
### severity : `normal`
### contents :
Graphite is unable to do the loop interchange when the inner loop is along the slow index of an array:

[Book15] Fortran/omp_tst% cat loop.f90
module parms
implicit none
private
integer, parameter, public :: num = 1024
integer, parameter, public :: dp = kind(0.0d0)

end module parms

program loops
use parms
implicit none
real(kind=dp), dimension(:, :), &
allocatable :: a, c
integer :: i, j, k, n_iter=100
integer(8) :: start, finish, counts
allocate(a(num,num),c(num,num))

call random_number(a)
c = 0
call system_clock (start, counts)
do k=1,n_iter
  do i=1,num
!    c(i,1) = 0.5*(a(i,2) - a(i,num))
!    c(i,num) = 0.5*(a(i,1) - a(i,num-1))
    do j=2,num-1
      c(i,j) = 0.5*(a(i,j+1) - a(i,j-1))
    end do
  end do
end do
call system_clock (finish)
print *, sum(abs(c)) ! To ensure computation
print *, "Elapsed time =" ,&
(finish - start) / real(counts, kind=8), "seconds"

c = 0
call system_clock (start, counts)
do k=1,n_iter
!  do i=1,num
!    c(i,1) = 0.5*(a(i,2) - a(i,num))
!    c(i,num) = 0.5*(a(i,1) - a(i,num-1))
!  end do
  do j=2,num-1
    do i=1,num
      c(i,j) = 0.5*(a(i,j+1) - a(i,j-1))
    end do
  end do
end do
call system_clock (finish)
print *, sum(abs(c)) ! To ensure computation
print *, "Elapsed time =" ,&
(finish - start) / real(counts, kind=8), "seconds"

end program loops
[Book15] Fortran/omp_tst% gfc -Ofast -floop-interchange loop.f90 
[Book15] Fortran/omp_tst% time a.out
   174350.51293227341     
 Elapsed time =   2.1943769999999998      seconds
   174350.51293227341     
 Elapsed time =  0.14006299999999999      seconds
2.347u 0.011s 0:02.36 99.5%	0+0k 0+0io 30pf+0w

This may be a duplicate of pr36011, but the timings are not affected by adding -fno-tree-pre -fno-tree-loop-im. Note that gcc with -floop-interchange is able to optimize the matrix product (see pr14741 and pr60997).

This also affects the polyhedron test air.f90. With the following patch

--- air.f90	2009-08-28 14:22:26.000000000 +0200
+++ air_va.f90	2014-04-19 13:10:44.000000000 +0200
@@ -400,8 +400,8 @@
 !
 ! COMPUTE THE FLUX TERMS
 !
-      DO i = 1 , MXPx
-         DO j = 1 , MXPy
+      DO j = 1 , MXPy
+         DO i = 1 , MXPx
 !
 ! compute vanleer fluxes
 !
@@ -657,8 +657,8 @@
       ENDDO
 !
 ! COMPUTE THE FLUX TERMS
-      DO i = 1 , MXPx
-         DO j = 1 , MXPy
+      DO j = 1 , MXPy
+         DO i = 1 , MXPx
 !
 ! compute vanleer fluxes
 !

the execution time goes from 3.2s to 2.7s (with -Ofast, with/without -floop-interchange).


---


### compiler : `gcc`
### title : `PowerPC 128 bit integer divide`
### open_at : `2014-05-01T17:51:56Z`
### last_modified_date : `2022-03-08T16:20:42Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=61030
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `5.0`
### severity : `enhancement`
### contents :
The rs6000 port should use divde to implement GCC named pattern divmodtidi4 and divdeu to for udivmodtidi4. Similarly, divwe and divweu can implement divmoddisi4 and udivmoddisi4.


---


### compiler : `gcc`
### title : `Duplicated instructions in both conditional branches`
### open_at : `2014-05-04T04:14:42Z`
### last_modified_date : `2021-07-18T21:12:10Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=61051
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `5.0`
### severity : `normal`
### contents :
Source code:

extern int* foo1 ( long* );
extern int *foo2 ( long *, long *);
extern void foo3 (long, long);

void bar()
{
    long d, f, x, s, r;
    int *p;

    d = 1;
    if (foo1(&r))
    {
            p = foo2( &d, &x);

            if( x != *p )
                    s = 1;
            else
                    s = 2;

            if( r > 0 )
                    f = 1 + d;
            else
                    f = d;

            foo3 (f, d);
            *p = s;
    }
}


Compile it with options -O2 -m64 -mcpu=power8, gcc generates:


bar:
0:	addis 2,12,.TOC.-0b@ha
	addi 2,2,.TOC.-0b@l
	.localentry	bar,.-bar
	mflr 0
	std 30,-16(1)
	std 31,-8(1)
	li 9,1
	std 0,16(1)
	stdu 1,-80(1)
	addi 3,1,32
	std 9,48(1)
	bl foo1
	nop
	cmpdi 7,3,0
	beq 7,.L1
	addi 3,1,48
	addi 4,1,40
	bl foo2
	nop
	ld 10,40(1)
	li 30,1
	lwa 9,0(3)
	mr 31,3
	cmpd 7,9,10
	beq 7,.L12       // C
	ld 9,32(1)       // A1
	cmpdi 7,9,0      // A2
	ble 7,.L4
.L13:
	ld 4,48(1)
	addi 3,4,1
.L5:
	bl foo3
	nop
	stw 30,0(31)
.L1:
	addi 1,1,80
	ld 0,16(1)
	ld 30,-16(1)
	ld 31,-8(1)
	mtlr 0
	blr
	.p2align 4,,15
.L12:
	ld 9,32(1)       // B1
	li 30,2
	cmpdi 7,9,0      // B2
	bgt 7,.L13
.L4:
	ld 3,48(1)
	mr 4,3
	b .L5
	.long 0
	.byte 0,0,0,1,128,2,0,0
	.size	bar,.-bar


Instruction C is a conditional branch. In both branches A1 and B1 are same instructions, they can be moved to before C. If we use a different conditional register, instructions A2 and B2 can also be moved before C.


---


### compiler : `gcc`
### title : `Simplify value_replacement in phiopt`
### open_at : `2014-05-08T13:40:45Z`
### last_modified_date : `2019-11-22T05:31:31Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=61110
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `5.0`
### severity : `enhancement`
### contents :
The patch for PR 59100 introduced 2 functions neutral_element_p and absorbing_element_p. I don't know why I did that. When we see:
(x != 0) ? x + y : y
instead of asking if 0 is a neutral element of + on the left, it is easier to try to fold "0 + y" (I replaced x with the rhs of the comparison) and check if that matches "y". This handles neutral and absorbing as a single case and is even more general (we could also do it for the non-constant case: (x!=y) ? x|y : x). We could even imagine generalizing it to the case where middle_bb has 2 or 3 statements (but the cost analysis may need to be refined then).

I probably won't do it immediately (the current code works) but I didn't want this idea to be forgotten.


---


### compiler : `gcc`
### title : `Mark private methods hidden automatically`
### open_at : `2014-05-08T14:19:35Z`
### last_modified_date : `2021-12-08T15:27:02Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=61113
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `c++`
### version : `4.8.2`
### severity : `enhancement`
### contents :
Suppose you compile a class defined like this using -fvisibility=hidden:

class __attribute__ ((visibility("default"))) Thing final {
public:
  void publicFunc();

private:
  void privateFunc();
};

Dumping the .so file with nm -C -D gives this:

0000000000001626 T Thing::publicFunc()
000000000000166c T Thing::privateFunc()

That is, both the private and public methods are exported in the symbol table. The latter is wasteful because private methods can only be called from within the class and those methods are always in the same .so (or maybe there are pathological cases why someone might want to split class implementation over multiple .so files, but it seems unlikely).

This also inhibits compiler optimizations as described on the Gcc visibility wiki page.

You can hide the method manually by declaring it like this:

void __attribute__ ((visibility("hidden"))) privateFunc();

If your code base is big, this a lot of work to do manually. Therefore it would be nice if there was a way to hide private methods automatically. Alternatives include a compiler flag such as -fvisibility-private-hidden or a heuristic that tags private methods hidden if -fvisibility=hidden is specified on the command line and the method's visibility has not been specified explicitly (so that people can expose their private methods if they really want to).


---


### compiler : `gcc`
### title : `LIM not pulling out non-aliased non-depednent load and stores (outside of loop bounds)`
### open_at : `2014-05-13T13:20:29Z`
### last_modified_date : `2021-08-21T04:24:32Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=61175
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `enhancement`
### contents :
of these three function only "oneOk"  vectorize.

float px[1024];
float vx[1024];
unsigned int N=1024;


void one(unsigned int i) {
   for (auto j=i+1; j<N; ++j) {
      auto ax = px[j]-px[i];
      vx[i]-=ax;
      vx[j]+=ax;
   }
}

void oneOK(unsigned int k) {
  auto tmp = vx[k];
   for (auto j=0; j<k-1; ++j) {
      auto ax = px[j]-px[k];
      tmp-=ax;
      vx[j]+=ax;
   }
   vx[k]=tmp;
}


void oneNope(unsigned int k) {
   for (auto j=0; j<k-1; ++j) {
      auto ax = px[j]-px[k];
      vx[k]-=ax;
      vx[j]+=ax;
   }
}


---


### compiler : `gcc`
### title : `[7 Regression] Incorrect warning "integer overflow in expression" on pointer-pointer subtraction`
### open_at : `2014-05-19T23:10:17Z`
### last_modified_date : `2019-11-14T09:10:21Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=61240
### status : `RESOLVED`
### tags : `diagnostic, missed-optimization`
### component : `c`
### version : `4.8.0`
### severity : `normal`
### contents :
Credit goes to "Lumbering Lummox", the author of this Stack Overflow post:
http://stackoverflow.com/q/23747641/827263

I see this problem with gcc versions 4.8.0 and 4.9.0, both compiled from source, on Linux Mint 14 on x86_64.

Source program:

int main(void) {
    int i;
    int *p = &i;
    int *q = &i + 1;
    p - (p - 1);
    q - (q - 1);
}

Compiler output:

% /usr/local/apps/gcc-4.8.0/bin/gcc gcc-bug-integer-overflow.c
gcc-bug-integer-overflow.c: In function ‘main’:
gcc-bug-integer-overflow.c:5:7: warning: integer overflow in expression [-Woverflow]
     p - (p - 1);
       ^
gcc-bug-integer-overflow.c:6:7: warning: integer overflow in expression [-Woverflow]
     q - (q - 1);
       ^

A warning would be appropriate for "p - (p - 1)", since (p - 1) has undefined behavior -- but since it's pointer arithmetic, not integer arithmetic, the "integer overflow" warning is at least incorrectly worded. Furthermore, the error message points to the first "-", which is not the problem.

As for "q - (q - 1)", no warning should be issued at all, since both "(q - 1)" and "q - (q - 1)" are valid expressions with well defined behavior (yielding &i and (ptrdiff_t)1, respectively).

This might be related to bug #48267.


---


### compiler : `gcc`
### title : `built-in memset makes the caller function slower`
### open_at : `2014-05-20T01:33:49Z`
### last_modified_date : `2021-08-22T08:45:07Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=61241
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `target`
### version : `5.0`
### severity : `normal`
### contents :
Compiled with  -O2, 

#include <string.h>
extern int off;
void *test(char *a1, char* a2)
{
        memset(a2, 123, 123);
        return a2 + off;
}

gives a result as following.

        mov     ip, r1
        mov     r1, #123
        stmfd   sp!, {r3, lr}
        mov     r0, ip
        mov     r2, r1
        bl      memset
        movw    r3, #:lower16:off
        movt    r3, #:upper16:off
        mov     ip, r0
        ldr     r0, [r3]
        add     r0, ip, r0
        ldmfd   sp!, {r3, pc}

After adding -fno-builtin, the assemble code becomes shorter.

        stmfd   sp!, {r4, lr}
        mov     r4, r1
        mov     r1, #123
        mov     r0, r4
        mov     r2, r1
        bl      memset
        movw    r3, #:lower16:off
        movt    r3, #:upper16:off
        ldr     r0, [r3]
        add     r0, r4, r0
        ldmfd   sp!, {r4, pc}

One reason is that arm_eabi must align stack to 8 bytes, so it push a meaningless r3. But that is not the most important reason.

When using built-in memset, ira can know that memset does not change the value of r0. Then choosing r0 instead of ip is clearly more profitable, because this choice can get rid of the redundant "mov ip,r0; mov r0,ip;" pair.

For this rtl sequence:

(insn 7 8 9 2 (set (reg:SI 0 r0)
        (reg/v/f:SI 115 [ a2 ])) open_test.c:5 186 {*arm_movsi_insn}
     (nil))
(insn 9 7 10 2 (set (reg:SI 2 r2)
        (reg:SI 1 r1)) open_test.c:5 186 {*arm_movsi_insn}
     (expr_list:REG_EQUAL (const_int 123 [0x7b])
        (nil)))
(call_insn 10 9 24 2 (parallel [
            (set (reg:SI 0 r0)
                (call (mem:SI (symbol_ref:SI ("memset") [flags 0x41]  <function_decl 0xb7d72500 memset>) [0 __builtin_memset S4 A32])
                    (const_int 0 [0])))
            (use (const_int 0 [0]))
            (clobber (reg:SI 14 lr))
        ]) open_test.c:5 251 {*call_value_symbol}
     (expr_list:REG_RETURNED (reg/v/f:SI 115 [ a2 ])
        (expr_list:REG_DEAD (reg:SI 2 r2)
            (expr_list:REG_DEAD (reg:SI 1 r1)
                (expr_list:REG_UNUSED (reg:SI 0 r0)
                    (expr_list:REG_EH_REGION (const_int 0 [0])
                        (nil))))))
    (expr_list:REG_CFA_WINDOW_SAVE (set (reg:SI 0 r0)
            (reg:SI 0 r0))
        (expr_list:REG_CFA_WINDOW_SAVE (use (reg:SI 2 r2))
            (expr_list:REG_CFA_WINDOW_SAVE (use (reg:SI 1 r1))
                (expr_list:REG_CFA_WINDOW_SAVE (use (reg:SI 0 r0))
                    (nil))))))

Assigning r0 to r115 was blocked by two pieces of code in process_bb_node_lives(In ira-lives.c).

1:
	  call_p = CALL_P (insn);
	  for (def_rec = DF_INSN_DEFS (insn); *def_rec; def_rec++)
	    if (!call_p || !DF_REF_FLAGS_IS_SET (*def_rec, DF_REF_MAY_CLOBBER))
	      mark_ref_live (*def_rec);
2:
	  /* Mark each used value as live.  */
	  for (use_rec = DF_INSN_USES (insn); *use_rec; use_rec++)
	    mark_ref_live (*use_rec);

In piece 1, "set (reg:SI 0 )  (reg/v/f:SI 115)" will make r0 conflict with 
r115 when r115 is living. This is not necessary as "set (reg:SI 0) (reg:SI 0)" will not hurt any other instruction. Making r0 conflict with all living pseudo registers will lose the chance to optimize a set instruction. I think at least for a simple single set, we should not make the source register conflict with the dest register when one of them is hard register and the other is not.

In piece 2, after call memset, r0 will become living and then conflict with living r115. This code neglect that r115 is the result of find_call_crossed_cheap_reg, and in fact r115 is the same as r0.

As discussed above, the two pieces of code block the ira to do a more profitable choice.I have build a patch to fix this problem. After the patch, the assemble code with built-in memset become shorter than normal memset.

        mov     r0, r1
        mov     r1, #123
        stmfd   sp!, {r3, lr}
        mov     r2, r1
        bl      memset
        movw    r3, #:lower16:off
        movt    r3, #:upper16:off
        ldr     r3, [r3]
        add     r0, r0, r3
        ldmfd   sp!, {r3, pc}

I have done a "bootstrap" and "make check" on x86, nothing change after the patch. Is that patch OK for trunk?


---


### compiler : `gcc`
### title : `#pragma GCC ivdep is handled incorrectly inside templates`
### open_at : `2014-05-20T07:28:55Z`
### last_modified_date : `2021-08-02T06:45:52Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=61245
### status : `NEW`
### tags : `missed-optimization`
### component : `c++`
### version : `4.9.0`
### severity : `normal`
### contents :
apologize for not reducing (trivial reduction (bar below) works)
given 
cat NaiveDod.cc
#include<array>
#include<vector>
#include<utility>

unsigned int N;
float * a, *b, *c;

void bar() {
#pragma GCC ivdep
  for (auto i=0U; i<N; ++i)
    a[i] = b[i]*c[i];
}



template<int N>
struct SoA {
  using s_t = unsigned int;   
  using Ind = unsigned int;

  auto size() const { return m_n;}

  float & operator()(Ind i, Ind j) { return data[j][i];}
  float const & operator()(Ind i, Ind j) const { return data[j][i];}

  std::array<std::vector<float>,N> data;
  s_t m_n=0;
};


template<int N>
void doT(SoA<N> & soa) {
#pragma GCC ivdep
  for (auto i=0U; i<soa.size(); ++i)
    soa(i,0) = soa(i,1)*soa(i,2);
}


void doIt(SoA<3> & soa) {
  doT(soa);
}


produces

c++ -std=c++1y -Ofast -Wall -fopt-info-vec -fno-tree-slp-vectorize -march=nehalem -S NaiveDod.cc
NaiveDod.cc:10:17: note: loop vectorized
NaiveDod.cc:10:17: note: loop peeled for vectorization to enhance alignment
NaiveDod.cc: In function 'void doIt(SoA<3>&)':
NaiveDod.cc:34:17: internal compiler error: in expand_ANNOTATE, at internal-fn.c:127
   for (auto i=0U; i<soa.size(); ++i)
                 ^
0x9e9a97 expand_ANNOTATE
	../../gcc-trunk/gcc/internal-fn.c:127
0x820a7a expand_call_stmt
	../../gcc-trunk/gcc/cfgexpand.c:2236
0x820a7a expand_gimple_stmt_1
	../../gcc-trunk/gcc/cfgexpand.c:3202
0x820a7a expand_gimple_stmt
	../../gcc-trunk/gcc/cfgexpand.c:3354
0x821aee expand_gimple_basic_block
	../../gcc-trunk/gcc/cfgexpand.c:5194
0x823746 execute
	../../gcc-trunk/gcc/cfgexpand.c:5803
Please submit a full bug report,
with preprocessed source if appropriate.
Please include the complete backtrace with any bug report.
See <http://gcc.gnu.org/bugs.html> for instructions.


c++ -v
Using built-in specs.
COLLECT_GCC=c++
COLLECT_LTO_WRAPPER=/afs/cern.ch/user/i/innocent/w4/libexec/gcc/x86_64-unknown-linux-gnu/4.10.0/lto-wrapper
Target: x86_64-unknown-linux-gnu
Configured with: ../gcc-trunk//configure --prefix=/afs/cern.ch/user/i/innocent/w4 --enable-languages=c,c++,lto,fortran -enable-gold=yes --enable-lto --with-gmp-lib=/usr/local/lib64 --with-mpfr-lib=/usr/local/lib64 -with-mpc-lib=/usr/local/lib64 --enable-cloog-backend=isl --with-cloog=/usr/local --with-ppl-lib=/usr/local/lib64 -enable-libitm -disable-multilib
Thread model: posix
gcc version 4.10.0 20140520 (experimental) [trunk revision 210630] (GCC)


---


### compiler : `gcc`
### title : `vectorization fails for unsigned is used for IV but casted to int before using as the index (and then casted for internal type)`
### open_at : `2014-05-20T07:40:27Z`
### last_modified_date : `2021-02-27T16:58:00Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=61247
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `enhancement`
### contents :
in the following example
cat uintLoop.cc
unsigned int N;
float * a, *b, *c;

using Ind = /*unsigned*/ int;
inline
float & val(float * x, Ind i) { return x[i];}
inline
float const & val(float const * x, Ind i) { return x[i];}

void foo() {
#pragma GCC ivdep
  for (auto i=0U; i<N; ++i)
    val(a,i) = val(b,i)*val(c,i);
}


using Ind = /*unsigned*/ int;
does not vectorize with
c++ -std=c++1y -Ofast -Wall -fopt-info-vec-missed -fno-tree-slp-vectorize -march=nehalem -S uintLoop.cc
uintLoop.cc:12:17: note: not vectorized: not suitable for gather load _8 = *_17;

uintLoop.cc:12:17: note: bad data references.


using Ind = unsigned int;
vectorize fine


minor, just annoying


---


### compiler : `gcc`
### title : `excessive code size with large-unit-insns`
### open_at : `2014-05-21T15:27:34Z`
### last_modified_date : `2021-08-16T08:01:21Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=61274
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.9.0`
### severity : `normal`
### contents :
according to docs inline-unit-growth limit is effective only when unit size is above large-unit-insns, which means if application consists of many small units with many inlineable functions, application size can be excessive if inline-unit-growth wasn't applied

there should be some limit also for small units below large-unit-insns 
or 
large-unit-insns should be set to lower value e.g. 1000 instead of 10,000
or
large-unit-insns should be removed, which means inline-unit-growth is always applied


---


### compiler : `gcc`
### title : `[4.9/4.10 Regression] Performance regression for the SIMD rotate operation with GCC vector extensions`
### open_at : `2014-05-24T01:24:40Z`
### last_modified_date : `2021-08-30T02:38:26Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=61299
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `normal`
### contents :
A small test:

/**************/
typedef unsigned int uint32x4 __attribute__ ((vector_size(16)));
typedef struct { uint32x4 a, b; } prng_t;
void foo(prng_t *x)
{
        x->a ^= ((x->b << 17) ^ (x->b >> (32 - 17)));
}
/**************/

Gets compiled into the following slow code with GCC 4.9 (CFLAGS="-O3"):

0000000000000000 <foo>:
   0:   66 0f 6f 47 10          movdqa 0x10(%rdi),%xmm0
   5:   66 0f 70 c8 55          pshufd $0x55,%xmm0,%xmm1
   a:   66 0f 7e c0             movd   %xmm0,%eax
   e:   c1 c8 0f                ror    $0xf,%eax
  11:   89 44 24 e8             mov    %eax,-0x18(%rsp)
  15:   66 0f 7e c8             movd   %xmm1,%eax
  19:   66 0f 6f c8             movdqa %xmm0,%xmm1
  1d:   c1 c8 0f                ror    $0xf,%eax
  20:   66 0f 6a c8             punpckhdq %xmm0,%xmm1
  24:   89 44 24 ec             mov    %eax,-0x14(%rsp)
  28:   66 0f 70 c0 ff          pshufd $0xff,%xmm0,%xmm0
  2d:   66 0f 6e 5c 24 ec       movd   -0x14(%rsp),%xmm3
  33:   66 0f 7e c8             movd   %xmm1,%eax
  37:   c1 c8 0f                ror    $0xf,%eax
  3a:   89 44 24 f0             mov    %eax,-0x10(%rsp)
  3e:   66 0f 7e c0             movd   %xmm0,%eax
  42:   66 0f 6e 44 24 e8       movd   -0x18(%rsp),%xmm0
  48:   66 0f 6e 4c 24 f0       movd   -0x10(%rsp),%xmm1
  4e:   c1 c8 0f                ror    $0xf,%eax
  51:   66 0f 62 c3             punpckldq %xmm3,%xmm0
  55:   89 44 24 f4             mov    %eax,-0xc(%rsp)
  59:   66 0f 6e 54 24 f4       movd   -0xc(%rsp),%xmm2
  5f:   66 0f 62 ca             punpckldq %xmm2,%xmm1
  63:   66 0f 6c c1             punpcklqdq %xmm1,%xmm0
  67:   66 0f ef 07             pxor   (%rdi),%xmm0
  6b:   0f 29 07                movaps %xmm0,(%rdi)
  6e:   c3                      retq   

It used to be a lot better with GCC 4.8 (CFLAGS="-O3"):

0000000000000000 <foo>:
   0:   66 0f 6f 4f 10          movdqa 0x10(%rdi),%xmm1
   5:   66 0f 6f c1             movdqa %xmm1,%xmm0
   9:   66 0f 72 d1 0f          psrld  $0xf,%xmm1
   e:   66 0f 72 f0 11          pslld  $0x11,%xmm0
  13:   66 0f ef c1             pxor   %xmm1,%xmm0
  17:   66 0f ef 07             pxor   (%rdi),%xmm0
  1b:   66 0f 7f 07             movdqa %xmm0,(%rdi)
  1f:   c3                      retq


---


### compiler : `gcc`
### title : `missed optimization of move if vector passed by reference`
### open_at : `2014-05-24T08:32:34Z`
### last_modified_date : `2021-08-19T18:25:19Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=61301
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `enhancement`
### contents :
in the following test shuffle2 generates not optimized moves.
the other two are ok.
the problem occurs in real life when the vector is a data member of a class
and the function is a method, as in "foo"

typedef float __attribute__( ( vector_size( 16 ) ) ) float32x4_t;
typedef int   __attribute__( ( vector_size( 16 ) ) ) int32x4_t;


float32x4_t shuffle1(float32x4_t x) {
   return float32x4_t{x[1],x[0],x[3],x[2]};
}

 
float32x4_t shuffle2(float32x4_t const & x) {
   return float32x4_t{x[1],x[0],x[3],x[2]};
}

float32x4_t shuffle3(float32x4_t const & x) {
   return __builtin_shuffle(x,int32x4_t{1,0,3,2});
}

struct foo {
  float32x4_t x;
  float32x4_t shuffle2() const;
  float32x4_t shuffle3() const;
};

float32x4_t foo::shuffle2() const {
  return float32x4_t{x[1],x[0],x[3],x[2]};
}
float32x4_t foo::shuffle3() const {
   return __builtin_shuffle(x,int32x4_t{1,0,3,2});
}


compiled with

c++ -std=c++11 -Ofast -march=nehalem  -S shuffle.cc; cat shuffle.s
generates:
__Z8shuffle1U8__vectorf:
LFB0:
	shufps	$177, %xmm0, %xmm0
	ret

__Z8shuffle2RKU8__vectorf:
LFB1:
	movss	12(%rdi), %xmm1
	insertps	$0x10, 8(%rdi), %xmm1
	movss	4(%rdi), %xmm0
	insertps	$0x10, (%rdi), %xmm0
	movlhps	%xmm1, %xmm0
	ret

__Z8shuffle3RKU8__vectorf:
LFB2:
	movaps	(%rdi), %xmm0
	shufps	$177, %xmm0, %xmm0
	ret


---


### compiler : `gcc`
### title : `Missed vectorization: control flow in loop`
### open_at : `2014-05-24T14:46:23Z`
### last_modified_date : `2023-10-20T21:41:30Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=61304
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `5.0`
### severity : `normal`
### contents :
(taken from a stackoverflow question about a bug in llvm, replace -1 with -2 if you want to test llvm and avoid the bug)

gcc -O3 fails to vectorize the following program because it sees control flow in the loop. If I move i++ before the "if", which becomes i == 0, we still fail to vectorize because we get confused about the number of iterations. Finally, if I stop at i == 2048, we do vectorize, but the generated code could do with some improvements (that would be for a different PR though).

#include <stdint.h>
#include <string.h>

int main()
{
    uint32_t i = 0;
    uint32_t count = 0;

    while (1)
    {
        float n;
        memcpy(&n, &i, sizeof(float));
        if(n >= 0.0f && n <= 1.0f)
            count++;
        if (i == -1)
            break;
        i++;
    }

    return count;
}


---


### compiler : `gcc`
### title : `too many permutation in a vectorized "reverse loop"`
### open_at : `2014-05-28T09:12:09Z`
### last_modified_date : `2020-03-16T08:49:22Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=61338
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `enhancement`
### contents :
in this example gcc generates 4 permutations for foo (while none is required)
On the positive side the code for bar (which is a more realistic use case) seems optimal.

float x[1024];
float y[1024];
float z[1024];

void foo() {
  for (int i=0; i<512; ++i)
    x[1023-i] += y[1023-i]*z[512-i];
}


void bar() {
  for (int i=0; i<512; ++i)
    x[1023-i] += y[i]*z[i+512];
}

c++ -Ofast -march=haswell -S revloop.cc; cat revloop.s

__Z3foov:
LFB0:
	vmovdqa	LC0(%rip), %ymm2
	xorl	%eax, %eax
	leaq	4064+_x(%rip), %rdx
	leaq	4064+_y(%rip), %rsi
	leaq	2020+_z(%rip), %rcx
	.align 4,0x90
L2:
	vpermd	(%rdx,%rax), %ymm2, %ymm0
	vpermd	(%rcx,%rax), %ymm2, %ymm1
	vpermd	(%rsi,%rax), %ymm2, %ymm3
	vfmadd231ps	%ymm1, %ymm3, %ymm0
	vpermd	%ymm0, %ymm2, %ymm0
	vmovaps	%ymm0, (%rdx,%rax)
	subq	$32, %rax
	cmpq	$-2048, %rax
	jne	L2
	vzeroupper
	ret
LFE0:
	.section __TEXT,__text_cold,regular,pure_instructions
LCOLDE1:
	.text
LHOTE1:
	.section __TEXT,__text_cold,regular,pure_instructions
LCOLDB2:
	.text
LHOTB2:
	.align 4,0x90
	.globl __Z3barv
__Z3barv:
LFB1:
	vmovdqa	LC0(%rip), %ymm1
	leaq	2048+_z(%rip), %rdx
	leaq	_y(%rip), %rcx
	leaq	4064+_x(%rip), %rax
	leaq	4096+_z(%rip), %rsi
	.align 4,0x90
L6:
	vmovaps	(%rdx), %ymm2
	addq	$32, %rdx
	vpermd	(%rax), %ymm1, %ymm0
	addq	$32, %rcx
	vfmadd231ps	-32(%rcx), %ymm2, %ymm0
	subq	$32, %rax
	vpermd	%ymm0, %ymm1, %ymm0
	vmovaps	%ymm0, 32(%rax)
	cmpq	%rsi, %rdx
	jne	L6
	vzeroupper
	ret
LFE1:


---


### compiler : `gcc`
### title : `Poor optimization of simple small-sized matrix routines with constant data`
### open_at : `2014-06-12T02:37:23Z`
### last_modified_date : `2021-12-25T07:46:43Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=61481
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `5.0`
### severity : `enhancement`
### contents :
Created attachment 32927
Output of the

The following function does some simple matrix operations.  All of the data is constant, and N is small.  The function optimizes to a return statement for N=1 and N=2.  For N=3, optimization is incomplete after tree optimizations but benifits significantly from later optimizations.  For N=4, the final result is not good.

template<int N>
int foo()
{
    int x[N*N],y[N*N],z[N*N];
    for(int i=0;i<N*N;i++) x[i]=0;
    for(int i=0;i<N*N;i++) y[i]=0;
    for(int i=0;i<N*N;i++) z[i]=0;
    for(int i=0;i<N;i++) x[i*(N+1)]=1;
    for(int i=0;i<N;i++) y[i*(N+1)]=2;
    for(int i=0;i<N;i++) for(int j=0;j<N;j++) for(int k=0;k<N;k++) z[i*N+j]+=x[i*N+k]*y[k*N+j];
    int ret=0;
    for(int i=0;i<N;i++) ret+=z[i*(N+1)];
    return ret;
}
template int foo<1>();
template int foo<2>();
template int foo<3>();
template int foo<4>();


Compiled with: g++ test.cpp -c -S -O3

The full test.s file is attached, but the most immediate bits are summarized below.

=== Asm produced for foo<1>(); ===

movl $2, %eax
ret

=== Asm produced for foo<2>(); ===

movl $4, %eax
ret

=== Asm produced for foo<3>(); ===

subq $32, %rsp
.cfi_def_cfa_offset 40
movl $6, %eax
addq $32, %rsp
.cfi_def_cfa_offset 8
ret

=== Asm produced for foo<4>(); ===

subq $96, %rsp
.cfi_def_cfa_offset 104
xorl %eax, %eax
movl $8, %ecx
leaq -104(%rsp), %rdx
pxor %xmm7, %xmm7
pxor %xmm10, %xmm10
movq %rdx, %rdi
rep; stosq
movl $1, -104(%rsp)
movl $1, -84(%rsp)
movl $1, -64(%rsp)
movl $1, -44(%rsp)
movdqa %xmm7, %xmm11
shufps $136, %xmm7, %xmm11
movdqa -104(%rsp), %xmm0
shufps $221, %xmm7, %xmm7
movdqa -88(%rsp), %xmm3
... lots and lots of SSE instructions ...
movdqa %xmm2, %xmm0
punpckhdq %xmm5, %xmm2
punpckldq %xmm5, %xmm0
movaps %xmm6, -120(%rsp)
movl -120(%rsp), %eax
addl 44(%rsp), %eax
movaps %xmm0, 56(%rsp)
movaps %xmm2, 72(%rsp)
addl 64(%rsp), %eax
addl 84(%rsp), %eax
addq $96, %rsp
.cfi_def_cfa_offset 8
ret


---


### compiler : `gcc`
### title : `[NEON] alter costs to allow use of post-indexed addressing modes for VLD{2..4}/VST{2..4}`
### open_at : `2014-06-18T14:25:06Z`
### last_modified_date : `2020-09-22T17:34:53Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=61551
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `5.0`
### severity : `enhancement`
### contents :
Created attachment 32967
test for NEON addressing modes

The attached test case demonstrates that GCC does not exploit the post-indexed addressing mode for NEON structure loads and stores: VLDn, VSTn where n>=2.

Generated code for VLD1/VST1 (using desired post-indexed addressing)

test_ld1:
        @ args = 0, pretend = 0, frame = 0
        @ frame_needed = 0, uses_anonymous_args = 0
        @ link register save eliminated.
        vld1.8  {d16}, [r0], r1
        vst1.8  {d16}, [r0], r1
        vld1.8  {d16}, [r0], r1
        vst1.8  {d16}, [r0], r1
        vld1.8  {d16}, [r0], r1
        vst1.8  {d16}, [r0]
        bx      lr

Generated code for VLD2:
test_ld2:
        @ args = 0, pretend = 0, frame = 0
        @ frame_needed = 0, uses_anonymous_args = 0
        @ link register save eliminated.
        adds    r3, r0, r1
        vld2.8  {d16-d17}, [r0]
        adds    r0, r3, r1
        adds    r2, r0, r1
        vst2.8  {d16-d17}, [r3]
        adds    r3, r2, r1
        vld2.8  {d16-d17}, [r0]
        add     r1, r1, r3
        vst2.8  {d16-d17}, [r2]
        vld2.8  {d16-d17}, [r3]
        vst2.8  {d16-d17}, [r1]
        bx      lr


A proof of concept patch is posted at:
https://gcc.gnu.org/ml/gcc-patches/2014-06/msg01361.html


---


### compiler : `gcc`
### title : `better 387 code for float x == (int)x`
### open_at : `2014-06-19T15:47:36Z`
### last_modified_date : `2021-08-02T20:08:43Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=61563
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `target`
### version : `unknown`
### severity : `enhancement`
### contents :
I get this with GCC 4.10.0 20140619 (experimental):

$ gcc -mno-sse -O3 -S -o - -x c - <<<"int f(float x) { return x == (int)x; }"
...
f:
	fnstcw	-2(%rsp)
	movzwl	-2(%rsp), %eax
	flds	8(%rsp)
	movl	$0, %edx
	orb	$12, %ah
	movw	%ax, -4(%rsp)
	xorl	%eax, %eax
	fldcw	-4(%rsp)
	fistl	-12(%rsp)
	fldcw	-2(%rsp)
	fildl	-12(%rsp)
	fucomip	%st(1), %st
	fstp	%st(0)
	setnp	%al
	cmovne	%edx, %eax
	ret

All the fnstcw and fldcw stuff is unnecessary, because when we convert x to int, it doesn't matter what rounding mode we use; all that matters is whether it is already an exact int value or not.

I think the x == (int)x pattern is fairly common, and it would be nice if GCC generated better 387 code for it.


---


### compiler : `gcc`
### title : `Normal enum switch slower than test case.`
### open_at : `2014-06-26T15:24:47Z`
### last_modified_date : `2021-06-20T09:58:25Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=61621
### status : `WAITING`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.8.2`
### severity : `normal`
### contents :
I detected that a normal enum switch is 1.5 up to 3 times slower than a 'double' enum switch. Below I created a test case for you. Unkomment the marked lines to get better performace results.


### Compiler options
/usr/bin/g++ -O3 -Wall -std=c++11 test-case.cpp

###  test-case.cpp

#include <iostream>
#include <vector>
#include <chrono>


enum InstructionType
{
   UNDEFINED,
   INT32,
   UINT32,
   NUMBER,
   STRING,
   NULL_OBJECT,
   OBJECT,
   BOOLEAN_OBJECT,
   NUMBER_OBJECT,
   STRING_OBJECT,
   ARRAY_OBJECT,
   DATE_OBJECT,
   REGEX_OBJECT,
   FUNCTION_OBJECT,
   ADDRESS,
   NOP,
   RESULT,
   JUMP_IF_ZERO,
   MULTIPLICATION_EXPRESSION,
   DIVISION_EXPRESSION,
   REMAINDER_EXPRESSION,
   ADDITION_EXPRESSION,
   SUBTRACTION_EXPRESSION,
   LESS_EXPRESSION,
   RETURN_STATEMENT,

};

int
run (const std::vector <InstructionType> & instructions)
{
   int value = 0;

   for (size_t i = 0, size = instructions .size (); i < size; ++ i)
   {
      switch (instructions [i])
      {
         case UNDEFINED:
         case INT32:
         case UINT32:
         case NUMBER:
         case STRING:
         case NULL_OBJECT:
         case OBJECT:
         case BOOLEAN_OBJECT:
         case NUMBER_OBJECT:
         case STRING_OBJECT:
         case ARRAY_OBJECT:
         case DATE_OBJECT:
         case REGEX_OBJECT:
         case FUNCTION_OBJECT:
         case ADDRESS:
            value += 1;
            break;
// UNCOMMENT THE FOLLOWING LINES TO GET BETTER PERFORMANCE
//         default:
//         {
//            switch (instructions [i])
//            {
               case NOP:
                  break;
               case RESULT:
                  value += 2;
                  break;
               case JUMP_IF_ZERO:
                  value ++;
                  break;
               case MULTIPLICATION_EXPRESSION:
                  value += 3;
                  break;
               case DIVISION_EXPRESSION:
                  value += 4;
                  break;
               case REMAINDER_EXPRESSION:
                  value += 5;
                  break;
               case ADDITION_EXPRESSION:
                  value += 6;
                  break;
               case SUBTRACTION_EXPRESSION:
                  value += 7;
                  break;
               case LESS_EXPRESSION:
                  value += 8;
                  break;
               case RETURN_STATEMENT:
                  value += 9;
                  break;
// UNCOMMENT THE FOLLOWING LINES TO GET BETTER PERFORMANCE
//               default:
//                  break;
//            }
//         }
      }
   }

   return value;
}

inline
double
now ()
{
   using namespace std::chrono;

   return duration_cast <duration <double>> (high_resolution_clock::now () .time_since_epoch ()) .count ();
}

int
main (int argc, char **argv)
{
   std::cout << "Enum switch performance test!" << std::endl;

   std::vector <InstructionType> instructions = {
      UNDEFINED,
      INT32,
      UINT32,
      NUMBER,
      STRING,
      NULL_OBJECT,
      OBJECT,
      BOOLEAN_OBJECT,
      NUMBER_OBJECT,
      STRING_OBJECT,
      ARRAY_OBJECT,
      DATE_OBJECT,
      REGEX_OBJECT,
      FUNCTION_OBJECT,
      ADDRESS,
      NOP,
      RESULT,
      JUMP_IF_ZERO,
      MULTIPLICATION_EXPRESSION,
      DIVISION_EXPRESSION,
      REMAINDER_EXPRESSION,
      ADDITION_EXPRESSION,
      SUBTRACTION_EXPRESSION,
      LESS_EXPRESSION,
      RETURN_STATEMENT,
   };

   int  value = 0;
   auto t0    = now ();

   for (int i = 0; i < 100000000; ++ i)
      value += run (instructions);

   std::cout << "value: " << value << std::endl;
   std::cout << "time:  " << now () - t0 << " s" << std::endl;

   return 0;
}


################

holger@qualle:~$ gcc -v
Using built-in specs.
COLLECT_GCC=gcc
COLLECT_LTO_WRAPPER=/usr/lib/gcc/x86_64-linux-gnu/4.8/lto-wrapper
Target: x86_64-linux-gnu
Configured with: ../src/configure -v --with-pkgversion='Ubuntu 4.8.2-19ubuntu1' --with-bugurl=file:///usr/share/doc/gcc-4.8/README.Bugs --enable-languages=c,c++,java,go,d,fortran,objc,obj-c++ --prefix=/usr --program-suffix=-4.8 --enable-shared --enable-linker-build-id --libexecdir=/usr/lib --without-included-gettext --enable-threads=posix --with-gxx-include-dir=/usr/include/c++/4.8 --libdir=/usr/lib --enable-nls --with-sysroot=/ --enable-clocale=gnu --enable-libstdcxx-debug --enable-libstdcxx-time=yes --enable-gnu-unique-object --disable-libmudflap --enable-plugin --with-system-zlib --disable-browser-plugin --enable-java-awt=gtk --enable-gtk-cairo --with-java-home=/usr/lib/jvm/java-1.5.0-gcj-4.8-amd64/jre --enable-java-home --with-jvm-root-dir=/usr/lib/jvm/java-1.5.0-gcj-4.8-amd64 --with-jvm-jar-dir=/usr/lib/jvm-exports/java-1.5.0-gcj-4.8-amd64 --with-arch-directory=amd64 --with-ecj-jar=/usr/share/java/eclipse-ecj.jar --enable-objc-gc --enable-multiarch --disable-werror --with-arch-32=i686 --with-abi=m64 --with-multilib-list=m32,m64,mx32 --with-tune=generic --enable-checking=release --build=x86_64-linux-gnu --host=x86_64-linux-gnu --target=x86_64-linux-gnu
Thread model: posix
gcc version 4.8.2 (Ubuntu 4.8.2-19ubuntu1)


---


### compiler : `gcc`
### title : `False positive with -Wmaybe-uninitialized (predicate analysis, VRP)`
### open_at : `2014-07-02T22:23:46Z`
### last_modified_date : `2022-08-29T14:26:27Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=61677
### status : `NEW`
### tags : `diagnostic, missed-optimization, needs-reduction`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `normal`
### contents :
Created attachment 33055
Test case for false positive in -Wmaybe-uninitialized

With the attached file bug.i:

$ gcc -Wall -O2 -c bug.i -o /dev/null
In file included from scripts/kconfig/zconf.tab.c:2537:0:
scripts/kconfig/menu.c: In function ‘get_symbol_str’:
scripts/kconfig/menu.c:590:18: warning: ‘jump’ may be used uninitialized in this function [-Wmaybe-uninitialized]
In file included from scripts/kconfig/zconf.tab.c:2537:0:
scripts/kconfig/menu.c:551:19: note: ‘jump’ was declared here

The warning occurs in get_prompt_str, which initializes jump if (head && location), and subsequently uses jump if (head && location && ...).

gcc --version says "gcc (Debian 4.9.0-9) 4.9.0"


---


### compiler : `gcc`
### title : `[ 4.9 ] gcc sometimes does not optimise movaps with movups`
### open_at : `2014-07-05T15:57:32Z`
### last_modified_date : `2021-08-06T04:22:04Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=61722
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `enhancement`
### contents :
I have two functions that use unaligned moving of __m128 ( instruction movups ).
The first one is optimized well, but in the second function gcc does not eliminate unneeded movaps in the while loop.
Code:
typedef float __m128 __attribute__ ((__vector_size__ (16), __may_alias__));

void __test_fill_1( __m128 *dst, __m128 v, int count )
{
    while ( count-- )
       {
           __builtin_ia32_storeups((float*)(dst++),v);
           __builtin_ia32_storeups((float*)(dst++),v);
       }
}

void __test_fill_2( __m128 *dst, long long _v, int count )
{
    __m128 v;
    ((long long*)&v)[0]=((long long*)&v)[1]=_v;
    while ( count-- )
       {
           __builtin_ia32_storeups((float*)(dst++),v);
           __builtin_ia32_storeups((float*)(dst++),v);
       }
}

Compilation:
$ gcc -O3 test_fill.c -o test_fill -S            
$ cat test_fill
        .file   "test_fill.c"
        .section        .text.unlikely,"ax",@progbits
.LCOLDB0:
        .text
.LHOTB0:
        .p2align 4,,15
        .globl  __test_fill_1
        .type   __test_fill_1, @function
__test_fill_1: <------------ first function, optimisation works well here
.LFB0:
        .cfi_startproc
        testl   %esi, %esi
        je      .L1
        subl    $1, %esi
        leaq    16(%rdi), %rax
        salq    $5, %rsi
        leaq    48(%rdi,%rsi), %rdx
        .p2align 4,,10
        .p2align 3
.L3:              v----------------------- well-optimized while loop
        movups  %xmm0, -16(%rax)
        addq    $32, %rax
        movups  %xmm0, -32(%rax)
        cmpq    %rdx, %rax
        jne     .L3
.L1:
        rep ret
        .cfi_endproc
.LFE0:
        .size   __test_fill_1, .-__test_fill_1
        .section        .text.unlikely
.LCOLDE0:
        .text
.LHOTE0:
        .section        .text.unlikely
.LCOLDB1:
        .text
.LHOTB1:
        .p2align 4,,15
        .globl  __test_fill_2
        .type   __test_fill_2, @function
__test_fill_2: <------------ second function, problem with optimizing while loop
.LFB1:
        .cfi_startproc
        testl   %edx, %edx
        movq    %rsi, -16(%rsp)
        movq    %rsi, -24(%rsp)
        je      .L7
        subl    $1, %edx
        leaq    16(%rdi), %rax
        salq    $5, %rdx
        leaq    48(%rdi,%rdx), %rdx
        .p2align 4,,10
        .p2align 3
.L9:
        movaps  -24(%rsp), %xmm0 <-------- why movaps here?
        addq    $32, %rax
        movups  %xmm0, -48(%rax)
        movaps  -24(%rsp), %xmm1 <-------- why movaps here?
        movups  %xmm1, -32(%rax)
        cmpq    %rdx, %rax
        jne     .L9
.L7:
        rep ret
        .cfi_endproc
.LFE1:
        .size   __test_fill_2, .-__test_fill_2
        .section        .text.unlikely
.LCOLDE1:
        .text
.LHOTE1:
        .ident  "GCC: (GNU) 4.9.0 20140604 (prerelease)"
        .section        .note.GNU-stack,"",@progbits


---


### compiler : `gcc`
### title : `Some loops not vectorized`
### open_at : `2014-07-05T19:47:08Z`
### last_modified_date : `2021-08-07T05:09:49Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=61724
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.7.2`
### severity : `normal`
### contents :
Created attachment 33075
Test code

Some loops inside C++ classes are not vectorised by the tree-vectorise driver. Attached is an example. In it, the pairs {A::f(), A::h()} and {A::g(), A::k()} are twins, with subtle differences in how they are implemented:
- A::f() uses condition on this->size; A::g() reads this->size into the register variable n
- A::g() reads data from this->y (std::unique_ptr); A::k() copies the same pointer to a local T * variable.

In both cases only the loop within the second pair member is vectorised.
Here is the compiler output.

$ g++ -std=c++11 -fPIC -O3 -ftree-vectorizer-verbose=6 test.cpp 

Analyzing loop at test.cpp:44

44: versioning for alias required: can't determine dependence between *D.24505_63 and *D.24502_62
44: mark for run-time aliasing test between *D.24505_63 and *D.24502_62
44: Vectorizing an unaligned access.
44: Vectorizing an unaligned access.
44: vect_model_load_cost: unaligned supported by hardware.
44: vect_model_load_cost: inside_cost = 2, outside_cost = 0 .
44: vect_model_store_cost: unaligned supported by hardware.
44: vect_model_store_cost: inside_cost = 2, outside_cost = 0 .
44: cost model: Adding cost of checks for loop versioning aliasing.

44: cost model: epilogue peel iters set to vf/2 because loop iterations are unknown .
44: Cost model analysis: 
  Vector inside of loop cost: 4
  Vector outside of loop cost: 26
  Scalar iteration cost: 2
  Scalar outside cost: 1
  prologue iterations: 0
  epilogue iterations: 8
  Calculated minimum iters for profitability: 14

44:   Profitability threshold = 15


Vectorizing loop at test.cpp:44

44: Profitability threshold is 15 loop iterations.
44: create runtime check for data references *D.24505_63 and *D.24502_62
44: created 1 versioning for alias checks.

44: LOOP VECTORIZED.
Analyzing loop at test.cpp:22

22: versioning for alias required: can't determine dependence between *D.24457_38 and *D.24458_37
22: mark for run-time aliasing test between *D.24457_38 and *D.24458_37
22: Vectorizing an unaligned access.
22: Vectorizing an unaligned access.
22: vect_model_load_cost: unaligned supported by hardware.
22: vect_model_load_cost: inside_cost = 2, outside_cost = 0 .
22: vect_model_store_cost: unaligned supported by hardware.
22: vect_model_store_cost: inside_cost = 2, outside_cost = 0 .
22: cost model: Adding cost of checks for loop versioning aliasing.

22: cost model: epilogue peel iters set to vf/2 because loop iterations are unknown .
22: Cost model analysis: 
  Vector inside of loop cost: 4
  Vector outside of loop cost: 26
  Scalar iteration cost: 2
  Scalar outside cost: 1
  prologue iterations: 0
  epilogue iterations: 8
  Calculated minimum iters for profitability: 14

22:   Profitability threshold = 15


Vectorizing loop at test.cpp:22

22: Profitability threshold is 15 loop iterations.
22: create runtime check for data references *D.24457_38 and *D.24458_37
22: created 1 versioning for alias checks.

22: LOOP VECTORIZED.
Analyzing loop at test.cpp:34

34: not vectorized: not suitable for gather D.24489_53 = *D.24485_52;

Analyzing loop at test.cpp:12

12: not vectorized: number of iterations cannot be computed.
test.cpp:49: note: vectorized 2 loops in function.


---


### compiler : `gcc`
### title : `[5 Regression] Complete unroll is not happened for loops with short upper bound`
### open_at : `2014-07-08T08:50:53Z`
### last_modified_date : `2019-09-07T04:18:48Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=61743
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `5.0`
### severity : `normal`
### contents :
We discovered significant performance regression on one important benchmark from eembc2.0 suite after r211625. It turned out that complete unroll didn't happen.
I prepared simple reproducer that exhibits the problem. If we compile it with '-Dbtype=int' both innermost loops are unrolled completely by latest trunk compiler:
test.c:20:5: note: loop with 8 iterations completely unrolled
test.c:11:5: note: loop with 8 iterations completely unrolled
but if '-Dbtype=e_u8' unroll does not happen.
Note also that for this particular test-case compiler built before r211625 performs curoll only for one loop.


---


### compiler : `gcc`
### title : `min,max pattern not always properly optimized (for sse4 targets)`
### open_at : `2014-07-08T13:34:41Z`
### last_modified_date : `2023-07-21T06:21:17Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=61747
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `enhancement`
### contents :
I was expecting gcc to substitute min/max instruction for (a>/<b) ? a : b;
even for "O2".
This is not always the case, only Ofast provides consistently optimized code (even if sometimes with a redundant move). -ffinite-math-only makes the code worse for vector arguments...

cat vmin.cc 
typedef float __attribute__( ( vector_size( 16 ) ) ) float32x4_t;

  template<typename V1>
  V1 vmax(V1 a, V1 b) {
    return (a>b) ? a : b;
  }
  template<typename V1>
  V1 vmin(V1 a, V1 b) {
    return (a<b) ? a : b;
  }
 

float foo(float a, float b, float c) {
  return vmin(vmax(a,b),c);
}

float32x4_t foo(float32x4_t a, float32x4_t b, float32x4_t c) {
  return vmin(vmax(a,b),c);
}

template<typename Float>
Float bart(Float a) { 
  constexpr Float zero{0.f};
  constexpr Float it = zero+4.f;
  constexpr Float zt = zero-3.f;
  return vmin(vmax(a,zt),it);
}


float bar(float a) {
   return bart(a);
}
float32x4_t bar(float32x4_t a) {
   return bart(a);
}

I see
c++ -std=c++11 -O2  -msse4.2 -s vmin.cc -S; cat vmin.s

__Z3foofff:
LFB2:
	maxss	%xmm1, %xmm0
	minss	%xmm2, %xmm0
	ret

__Z3fooDv4_fS_S_:
LFB3:
	maxps	%xmm1, %xmm0
	minps	%xmm2, %xmm0
	ret

__Z3barf:
LFB5:
	ucomiss	LC3(%rip), %xmm0
	jbe	L12
	minss	LC2(%rip), %xmm0
	ret
	.align 4,0x90
L12:
	movss	LC3(%rip), %xmm0
	ret

__Z3barDv4_f:
LFB6:
	movaps	LC5(%rip), %xmm1
	movaps	%xmm0, %xmm2
	movaps	%xmm1, %xmm0
	cmpltps	%xmm2, %xmm0
	blendvps	%xmm0, %xmm2, %xmm1
	movaps	LC6(%rip), %xmm2
	movaps	%xmm1, %xmm0
	cmpltps	%xmm2, %xmm0
	blendvps	%xmm0, %xmm1, %xmm2
	movaps	%xmm2, %xmm0
	ret

-----------------
c++ -std=c++11 -O2  -msse4.2 -s vmin.cc -S -ffinite-math-only; cat vmin.s
__Z3foofff:
LFB2:
	maxss	%xmm0, %xmm1
	minss	%xmm2, %xmm1
	movaps	%xmm1, %xmm0
	ret
__Z3fooDv4_fS_S_:
LFB3:
	maxps	%xmm1, %xmm0
	movaps	%xmm0, %xmm1
	movaps	%xmm2, %xmm0
	cmpleps	%xmm1, %xmm0
	blendvps	%xmm0, %xmm2, %xmm1
	movaps	%xmm1, %xmm0
	ret

__Z3barf:
LFB5:
	maxss	LC2(%rip), %xmm0
	minss	LC3(%rip), %xmm0
	ret

__Z3barDv4_f:
LFB6:
	movaps	LC5(%rip), %xmm1
	movaps	%xmm0, %xmm2
	movaps	%xmm1, %xmm0
	cmpltps	%xmm2, %xmm0
	blendvps	%xmm0, %xmm2, %xmm1
	movaps	LC6(%rip), %xmm2
	movaps	%xmm1, %xmm0
	cmpltps	%xmm2, %xmm0
	blendvps	%xmm0, %xmm1, %xmm2
	movaps	%xmm2, %xmm0
	ret
LFE6:

--------------
eventually
c++ -std=c++11 -Ofast  -msse4.2 -s vmin.cc -S; cat vmin.s

__Z3foofff:
LFB2:
	maxss	%xmm0, %xmm1
	minss	%xmm2, %xmm1
	movaps	%xmm1, %xmm0
	ret

__Z3fooDv4_fS_S_:
LFB3:
	maxps	%xmm0, %xmm1
	minps	%xmm2, %xmm1
	movaps	%xmm1, %xmm0
	ret

__Z3barf:
LFB5:
	maxss	LC2(%rip), %xmm0
	minss	LC3(%rip), %xmm0
	ret
__Z3barDv4_f:
LFB6:
	maxps	LC5(%rip), %xmm0
	minps	LC6(%rip), %xmm0
	ret


---


### compiler : `gcc`
### title : `init-regs.c papers over issues elsewhere`
### open_at : `2014-07-15T13:07:35Z`
### last_modified_date : `2023-10-01T03:32:17Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=61810
### status : `NEW`
### tags : `missed-optimization, wrong-code`
### component : `target`
### version : `5.0`
### severity : `normal`
### contents :
Earlier this year Uli complained about undefined uses generating
code in the context of implementing _mm_undefined x86 intrinsics
in the "GCC way".  Example:

extern __inline __m128d __attribute__((__gnu_inline__, __always_inline__,
__artificial__))
_mm_undefined_pd (void)
{ 
  __m128d __Y = __Y;
  return __Y;
}
 
and the culprit was found to be the init-regs pass which initializes
all must-undefined but used pseudos with zero.  That has been
introduced with the dataflow-merge with some big handwaving
comment (and no testcase as far as we could see):

/* Check all of the uses of pseudo variables.  If any use that is MUST
   uninitialized, add a store of 0 immediately before it.  For
   subregs, this makes combine happy.  For full word regs, this makes
   other optimizations, like the register allocator and the reg-stack
   happy as well as papers over some problems on the arm and other
   processors where certain isa constraints cannot be handled by gcc.
   These are of the form where two operands to an insn my not be the
   same.  The ra will only make them the same if they do not
   interfere, and this can only happen if one is not initialized.

   There is also the unfortunate consequence that this may mask some
   buggy programs where people forget to initialize stack variable.
   Any programmer with half a brain would look at the uninitialized
   variable warnings.  */

Of course earlier this year it wasn't the appropriate time to
kill off init-regs (which doesn't run at -O0 btw...).  But now
it is.

All of the issues in the comment at the top of init-regs.c
point to issues elsewhere - papering over them by means
of init-regs.c isn't a correct solution - especially as
passes between init-regs and $issue may expose must-undefined
but used pseudos (if-conversion for example).

Disabling init-regs.c by adjusting its gate to always return 0 causes

FAIL: gcc.dg/vect/vect-strided-a-u8-i8-gap7.c execution test

on x86_64 and

FAIL: gcc.dg/vect/vect-strided-a-u16-i4.c execution test
FAIL: gcc.dg/vect/vect-strided-a-u8-i8-gap7.c execution test
FAIL: gcc.dg/vect/vect-strided-u8-i8-gap7-big-array.c execution test
FAIL: gcc.dg/vect/vect-strided-a-u16-i4.c -flto -ffat-lto-objects execution test
FAIL: gcc.dg/vect/vect-strided-a-u8-i8-gap7.c -flto -ffat-lto-objects execution 
test

on x86_64 -m32

no other FAILs (the comment hints at more issues on other targets).


Patch to disable init-regs (apart from the above bootstraps/tests ok
on x86_64)

Index: gcc/init-regs.c
=================================================================== 
--- gcc/init-regs.c     (revision 212520)
+++ gcc/init-regs.c     (working copy)
@@ -147,7 +147,7 @@ public:
   {}
   
   /* opt_pass methods: */
-  virtual bool gate (function *) { return optimize > 0; }
+  virtual bool gate (function *) { return 0; }
   virtual unsigned int execute (function *)
     {
       initialize_uninitialized_regs ();


---


### compiler : `gcc`
### title : `unused code fails to be removed after dom1, thread updated`
### open_at : `2014-07-16T09:55:26Z`
### last_modified_date : `2021-12-26T21:28:16Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=61818
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.1`
### severity : `normal`
### contents :
I found the following code:
#include <stddef.h>
#define container_of(ptr, type, member) ({			\
	const typeof( ((type *)0)->member ) *__mptr = (ptr);	\
	(type *)( (char *)__mptr - offsetof(type,member) );})

struct Node
{
    Node* m_next;
    int m_val;
};

void setLast(Node* n, int val)
{
    Node** ppnode = &n;

    while (*ppnode) {
        ppnode = &(*ppnode)->m_next;
    }

    // This if statement should be removed    
    if (ppnode == &n)
        return;
    Node* n2 = container_of(ppnode, Node, m_next);
    n2->m_val = val;
}

generates wired assembly codes:
_Z7setLastP4Nodei:
.LFB0:
	.cfi_startproc
	testq	%rdi, %rdi
	movq	%rdi, -8(%rsp)
	jne	.L3
	jmp	.L9
	.p2align 4,,10
	.p2align 3
.L4:
	movq	%rax, %rdi
.L3:
	movq	(%rdi), %rax
	testq	%rax, %rax
	jne	.L4
=>	leaq	-8(%rsp), %rax
=>	cmpq	%rax, %rdi
=>	je	.L1
	movl	%esi, 8(%rdi)
.L1:
	rep ret
.L9:
	rep ret

note that the marked assembly codes should not even exist. The value stored in -8(%rsp) remains not used.

After further debugging. I find
	.cfi_startproc
	testq	%rdi, %rdi
	movq	%rdi, -8(%rsp)
	jne	.L3
	jmp	.L9
is generated by "ch" pass (copy_loop_headers). That makes sense.

And that jump to the exist block is threaded in dom1 pass, and it makes sense too.

But gimpl codes:
  # n2_9 = PHI <n2_5(4)>
  if (&nD.2229 == n2_9)
    goto <bb 7>;
  else
    goto <bb 6>;

remain to the end, and get "cleverly" optimized into the following form:
  if (&nD.2229 == n2_5)
    goto <bb 7>;
  else
    goto <bb 6>;

That does not make any sense.

GCC should have a pass to remove this code. 
Is that because currently pointer analysis is not flow-aware?


---


### compiler : `gcc`
### title : `missed loop invariant expression optimization`
### open_at : `2014-07-18T00:40:51Z`
### last_modified_date : `2021-08-12T02:17:34Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=61837
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `5.0`
### severity : `enhancement`
### contents :
Compile following code with trunk compiler and options -O2 -m64 -mcpu=power8

void foo(int *p1, char *p2, int s)
{
  int n, v, i;

  v = 0;
  for (n = 0; n <= 100; n++) {
     for (i = 0; i < s; i++)
        if (p2[i] == n)
           p1[i] = v;
     v += 88;
  }
}

I got

foo:
	addi 9,5,-1
	cmpwi 5,5,0
	rldicl 9,9,0,32
	li 6,0
	li 7,0
	add 5,4,9
	.p2align 4,,15
.L2:
	ble 5,.L6
	addi 8,4,-1
	mr 10,3
	subf 9,8,5     // A
	mtctr 9
	b .L4
	.p2align 4,,15
.L3:
	addi 10,10,4
	bdz .L6
.L4:
	lbzu 9,1(8)
	cmpw 7,9,7
	bne 7,.L3
	stw 6,0(10)
	addi 10,10,4
	bdnz .L4
.L6:
	addi 6,6,88
	addi 7,7,1
	cmpwi 7,6,8888
	extsw 7,7
	extsw 6,6
	bne 7,.L2
	blr

Instruction A computes the inner loop counter, it is loop invariant for the outer loop, so it can be hoisted out of the outer loop.


---


### compiler : `gcc`
### title : `const-anchor optimisation is sensitive to ordering`
### open_at : `2014-07-27T09:43:54Z`
### last_modified_date : `2020-01-27T23:41:16Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=61926
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `unknown`
### severity : `enhancement`
### contents :
gcc.target/mips/const-anchor-1.c tests that cse uses constant anchors for:

  g (0x1233ffff, 0x12340001);

But this does not work for:

  g (0x12340001, 0x1233ffff);

since the constant that provides the 0x12340000 anchor then comes after
the constant that requires it.  Maybe this could fixed by doing the
anchor optimisation in gcse.c instead, although that probably isn't
trivial.

Related to PR33699.


---


### compiler : `gcc`
### title : `[SH] SImode addressing modes not used when storing SFmode values via SImode regs`
### open_at : `2014-07-27T20:05:14Z`
### last_modified_date : `2023-07-22T02:50:51Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=61930
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `target`
### version : `5.0`
### severity : `normal`
### contents :
The following

void foo (float a[])
{
  a[1] = 123;
  a[4] = 123;
  a[2] = 123;
  a[3] = 123;
}

compiled with -O2 -m4-single results in:

        mov.l   .L3,r1  ! 8     movsf_ie/8      [length = 2]
        mov     r4,r2   ! 28    movsi_ie/2      [length = 2]
        add     #4,r2   ! 7     *addsi3_compact [length = 2]
        mov.l   r1,@r2  ! 9     movsf_ie/10     [length = 2]
        add     #12,r2  ! 11    *addsi3_compact [length = 2]
        mov.l   r1,@r2  ! 13    movsf_ie/10     [length = 2]
        add     #-8,r2  ! 15    *addsi3_compact [length = 2]
        mov.l   r1,@r2  ! 17    movsf_ie/10     [length = 2]
        add     #12,r4  ! 19    *addsi3_compact [length = 2]
        rts             ! 36    *return_i       [length = 2]
        mov.l   r1,@r4  ! 21    movsf_ie/10     [length = 2]
.L4:
        .align 2
.L3:
        .long   1123418112

In this case the displacement addressing modes could be used.  For loads/stores to/from FP regs there are no displacement addressing modes available (on non-SH2A).  Since the stores are SFmode stores it thinks that displacement addressing mode is not legitimate.
The problem is that it's only known after register allocation that the SFmode value will be stored via an SImode reg.

Storing a different SFmode value (which can be loaded efficiently into an SFmode reg):

void foo (float a[])
{
  a[1] = 1;
  a[4] = 1;
  a[2] = 1;
  a[3] = 1;
}

results in:
        mov     r4,r1   ! 28    movsi_ie/2      [length = 2]
        add     #4,r1   ! 7     *addsi3_compact [length = 2]
        fldi1   fr1     ! 8     movsf_ie/4      [length = 2]
        fmov.s  fr1,@r1 ! 9     movsf_ie/7      [length = 2]
        add     #12,r1  ! 11    *addsi3_compact [length = 2]
        fmov.s  fr1,@r1 ! 13    movsf_ie/7      [length = 2]
        add     #-8,r1  ! 15    *addsi3_compact [length = 2]
        fmov.s  fr1,@r1 ! 17    movsf_ie/7      [length = 2]
        add     #12,r4  ! 19    *addsi3_compact [length = 2]
        rts             ! 36    *return_i       [length = 2]
        fmov.s  fr1,@r4 ! 21    movsf_ie/7      [length = 2]

A possible solution to this problem could be splitting out constant loads before RA/reload as much as possible.  Doing so would load the SFmode constant 123.0 into an SFmode reg.  However, using SImode regs for the above sequence is better in this case.  Maybe on SH it's better to convert SFmode loads/stores to true SImode loads/stores before register allocation.  The question is how and where to decide that such a transformation would be beneficial.

Possibly related: PR 54429


---


### compiler : `gcc`
### title : `Optimizer does not eliminate stores to destroyed objects`
### open_at : `2014-07-31T18:54:14Z`
### last_modified_date : `2021-07-23T18:35:44Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=61982
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `c++`
### version : `4.9.1`
### severity : `minor`
### contents :
After a destructor is run, access to the object is forbidden; the object is turned into a pile of bytes.  Yet the generated code for:


struct X { 
  int i; 
  void clear() { i = 0; } 
}; 

void f(X* x) { 
  x->clear(); 
  x->~X(); 
} 

void g(X* x) {
  x->clear();
  delete x;
}

contains a store for each of f() and g(), stores that should have been eliminated:

0000000000000000 <f(X*)>:
   0:	c7 07 00 00 00 00    	movl   $0x0,(%rdi)
   6:	c3                   	retq   
   7:	66 0f 1f 84 00 00 00 	nopw   0x0(%rax,%rax,1)
   e:	00 00 

0000000000000010 <g(X*)>:
  10:	c7 07 00 00 00 00    	movl   $0x0,(%rdi)
  16:	e9 00 00 00 00       	jmpq   1b <g(X*)+0xb>
			17: R_X86_64_PC32	operator delete(void*)-0x4


To be clear, the generated code is correct, but not optimal.


---


### compiler : `gcc`
### title : `False Data Dependency in popcnt instruction`
### open_at : `2014-08-04T14:29:52Z`
### last_modified_date : `2022-11-15T10:39:29Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=62011
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `unknown`
### severity : `normal`
### contents :
On Sandy/Ivy Bridge and Haswell processors, the instruction:

popcnt src, dest

appears to have a false dependency on the destination register dest. Even though the instruction only writes to it, the instruction will wait until dest is ready before executing.

This causes a loss in performance as explained here:
http://stackoverflow.com/questions/25078285/replacing-a-32-bit-loop-count-variable-with-64-bit-introduces-crazy-performance


---


### compiler : `gcc`
### title : `vector fneg codegen uses a subtract instead of an xor (x86-64)`
### open_at : `2014-08-06T19:06:09Z`
### last_modified_date : `2019-06-11T12:52:15Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=62041
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `normal`
### contents :
$ cat fneg.c
#include <xmmintrin.h>

__m128 fneg4(__m128 x) {
	return _mm_sub_ps(_mm_set1_ps(-0.0), x);
}

$ ~gcc49/local/bin/gcc -march=core-avx2 -O2 -S fneg.c -o - 
...
_fneg4:
LFB513:
	vmovaps	LC0(%rip), %xmm1
	vsubps	%xmm0, %xmm1, %xmm0
	ret
...
LC0:
	.long	2147483648
	.long	2147483648
	.long	2147483648
	.long	2147483648

------------------------------------

Instead of generating 'vsubps' here, it would be better to generate 'vxorps' because we know we're just flipping the sign bit of each element. This is what gcc does for the scalar version of this code.

Note that there is no difference if I use -ffast-math with this testcase. With -ffast-math enabled, we should generate the same 'xorps' code even if the "-0.0" is "+0.0". Again, that's what the scalar codegen does, so I think this is just a deficiency when generating vector code.

I can file the -ffast-math case as a separate bug if that would be better.


---


### compiler : `gcc`
### title : `missed optimization: recognize fnabs (FP negative absolute value) (x86-64)`
### open_at : `2014-08-07T19:17:10Z`
### last_modified_date : `2019-06-17T18:43:26Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=62055
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.9.0`
### severity : `normal`
### contents :
$ cat fnabs.c
#include <math.h>
float foo(float a) {
	return -fabsf(a);
}
$ gcc49 -O1 fnabs.c -S -o -
	.text
	.globl _foo
_foo:
LFB19:
	movss	LC0(%rip), %xmm1
	andps	%xmm1, %xmm0
	movss	LC1(%rip), %xmm1
	xorps	%xmm1, %xmm0
	ret
LFE19:
	.literal16
	.align 4
LC0:
	.long	2147483647
	.long	0
	.long	0
	.long	0
	.align 4
LC1:
	.long	2147483648
	.long	0
	.long	0
	.long	0

---------------------------------------------------

That's a lot of constant pool data and instructions to turn on a single bit.

I think there are 2 steps to improving this. First, recognize that -(fabs(a)) can be transformed into an 'or' op:

	movss	LC0(%rip), %xmm1
    	orps	%xmm1, %xmm0

LC0:
	.long	2147483648

Second, I don't think we need the extra 0 longs here; movss only loads 4 bytes. This may require understanding that the upper vector elements for the 'orps' are don't cares?


---


### compiler : `gcc`
### title : `Missed optimization: write ptr reloaded in each loop iteration`
### open_at : `2014-08-08T12:34:13Z`
### last_modified_date : `2021-06-20T10:05:40Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=62062
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.9.2`
### severity : `enhancement`
### contents :
When developing a binary i/o lib, I ran into some performance degradation in the writer functions. My investigation revealed that the write pointer was loaded/stored in each loop iteration. Although this can be dodged by hand-tuning the code via local variables kept in registers, the resulting code is longer, less clear, harder to maintain, etc. 

For this report, I recompiled w/ 4.9.2, but earlier versions in 4.x give the same results. The test box is an AMD FX w/ Debian Jessie.

gcc compiled from git commit f964b16:
g++-4.9.2 -v
Using built-in specs.
COLLECT_GCC=g++-4.9.2
COLLECT_LTO_WRAPPER=/usr/local/libexec/gcc/x86_64-unknown-linux-gnu/4.9.2/lto-wrapper
Target: x86_64-unknown-linux-gnu
Configured with: ./configure --enable-languages=c,c++ --disable-multilib --program-suffix=-4.9.2
Thread model: posix
gcc version 4.9.2 20140808 (prerelease) (GCC)

compiler/linker flags used:
g++-4.9.2 -c 20140725-reg_vs_mem.cpp -g -std=c++11 -Wall -Wextra -Werror -Wundef -Wshadow -O3 -fno-tree-vectorize
g++-4.9.2 -o 20140725-reg_vs_mem 20140725-reg_vs_mem.o -g

Tried with less optimization, too, but made no difference.

-fno-tree-vectorize was used because otherwise the code generated for the encoder functions used the vector registers, which resulted in serious code size bloat and ~2-3x runtimes, opposed to the ~1.5x runtime increase due to the redundant loads/stores.

For the tests, I made two versions for each function: one that expects a ptr ref (baseline version), and another one that expects a buffer object (w/ beg/end ptrs for advanced functionality, which is not used here). As expected, the same code is generated for these two.

I ruled out the aliasing rules first: I use int ptrs in this test, so that the 'char* aliases everything' rule is dodged. To prove my case:

write_run_char_ptr_ref() loads/stores the char ptr in each loop, since the character written invalidates the pointer itself:
   0x0000000000400570 <+0>:     sub    $0x1,%edx
   0x0000000000400573 <+3>:     js     0x40058d <write_run_char_ptr_ref(char*&, int, int)+29>
   0x0000000000400575 <+5>:     nopl   (%rax)
   0x0000000000400578 <+8>:     mov    (%rdi),%rax      # loop beg, load ptr
   0x000000000040057b <+11>:    sub    $0x1,%edx
   0x000000000040057e <+14>:    cmp    $0xffffffff,%edx
   0x0000000000400581 <+17>:    lea    0x1(%rax),%rcx
   0x0000000000400585 <+21>:    mov    %rcx,(%rdi)      # store updated ptr
   0x0000000000400588 <+24>:    mov    %sil,(%rax)
   0x000000000040058b <+27>:    jne    0x400578 <write_run_char_ptr_ref(char*&, int, int)+8>
   0x000000000040058d <+29>:    repz retq 

write_run_char_ptr_ref_unaliased() keeps the ptr in a register, but this was achieved w/ some platform dependent asm trickery, see unaliased_storeb() [btw, some platform independent builtin would be nice for this], I use this in the production code, which writes bytes at the lowest level.
   0x0000000000400590 <+0>:     test   %edx,%edx
   0x0000000000400592 <+2>:     jle    0x4005af <write_run_char_ptr_ref_unaliased(char*&, int, int)+31>
   0x0000000000400594 <+4>:     mov    (%rdi),%rax           # load ptr
   0x0000000000400597 <+7>:     sub    $0x1,%edx
   0x000000000040059a <+10>:    lea    0x1(%rax,%rdx,1),%rdx # end ptr
   0x000000000040059f <+15>:    nop
   0x00000000004005a0 <+16>:    mov    %sil,(%rax)           # loop body, no ptr load/store
   0x00000000004005a3 <+19>:    add    $0x1,%rax
   0x00000000004005a7 <+23>:    cmp    %rdx,%rax
   0x00000000004005aa <+26>:    jne    0x4005a0 <write_run_char_ptr_ref_unaliased(char*&, int, int)+16>
   0x00000000004005ac <+28>:    mov    %rax,(%rdi)           # store ptr after the loop
   0x00000000004005af <+31>:    repz retq 

write_run_ptr_ref() uses int ptr, and the ptr is kept in a register for the loop, without any trickery. The disassembly is the same as write_run_char_ptr_ref_unaliased() above, except ints are written. write_run_buf() is exactly the same. So far so good.

The next step is a variable length encoder, encode_ptr_ref(). This is not a real working encoding, just for demonstration. Since the probabilities are implied from the encoding lengths, the if conditions are peppered with builtin_expect's. Again, the ptr ref and buf object versions are exactly the same. However, I noticed that the ptr is written back multiple times, depending on which 'if' becomes true. For the most likely case, it doesn't matter: only one write is performed, but before the conditional jump. For the last two less likely cases, two redundant writes are performed. Moreover, for the 3rd 'if' block the actual useful ptr write is performed inside the block, and not before the conditional jump as with the 1st and 2nd if's. Since the last two if's are not likely, the performance impact of the redundant writes probably don't matter much, but since this ticket is about redundant loads/stores, it might have something to do with the core issue.
   0x0000000000400720 <+0>:     mov    (%rdi),%rax      # ptr load
   0x0000000000400723 <+3>:     cmp    $0xff,%esi
   0x0000000000400729 <+9>:     lea    0x4(%rax),%rdx
   0x000000000040072d <+13>:    mov    %rdx,(%rdi)      # store before the cond
   0x0000000000400730 <+16>:    jg     0x400738 <encode_buf(OutBuf&, int)+24>
   0x0000000000400732 <+18>:    mov    %esi,(%rax)      # most likely branch
   0x0000000000400734 <+20>:    retq   
   0x0000000000400735 <+21>:    nopl   (%rax)
   0x0000000000400738 <+24>:    lea    0x8(%rax),%rdx
   0x000000000040073c <+28>:    cmp    $0xffff,%esi
   0x0000000000400742 <+34>:    movl   $0x0,(%rax)
   0x0000000000400748 <+40>:    mov    %rdx,(%rdi)      # store again
   0x000000000040074b <+43>:    jg     0x400751 <encode_buf(OutBuf&, int)+49>
   0x000000000040074d <+45>:    mov    %esi,0x4(%rax)   # 2nd most likely br
   0x0000000000400750 <+48>:    retq   
   0x0000000000400751 <+49>:    cmp    $0xffffff,%esi
   0x0000000000400757 <+55>:    movl   $0x0,0x4(%rax)
   0x000000000040075e <+62>:    jg     0x40076b <encode_buf(OutBuf&, int)+75>
   0x0000000000400760 <+64>:    lea    0xc(%rax),%rdx   # 3rd most likely br
   0x0000000000400764 <+68>:    mov    %rdx,(%rdi)      # ptr stored after the cond
   0x0000000000400767 <+71>:    mov    %esi,0x8(%rax)
   0x000000000040076a <+74>:    retq   
   0x000000000040076b <+75>:    lea    0x10(%rax),%rdx  # least likely br
   0x000000000040076f <+79>:    movl   $0x0,0x8(%rax)
   0x0000000000400776 <+86>:    mov    %rdx,(%rdi)      # store
   0x0000000000400779 <+89>:    mov    %esi,0xc(%rax)
   0x000000000040077c <+92>:    retq   

encode_ptr_ref_tmp() is the same as encode_ptr_ref(), but the ptr is loaded into a local variable by hand, and written back to the reference in each branch before return. The generated code is effectively the same, same size, only the insn order is different: no redundant writes, all ptr writes are inside the corresponding if block.
   0x00000000004006c0 <+0>:     cmp    $0xff,%esi
   0x00000000004006c6 <+6>:     mov    (%rdi),%rax      # ptr load
   0x00000000004006c9 <+9>:     jg     0x4006d8 <encode_ptr_ref_tmp(unsigned int*&, int)+24>
   0x00000000004006cb <+11>:    mov    %esi,(%rax)
   0x00000000004006cd <+13>:    add    $0x4,%rax
   0x00000000004006d1 <+17>:    mov    %rax,(%rdi)      # ptr store
   0x00000000004006d4 <+20>:    retq   
   0x00000000004006d5 <+21>:    nopl   (%rax)
   0x00000000004006d8 <+24>:    cmp    $0xffff,%esi
   0x00000000004006de <+30>:    movl   $0x0,(%rax)
   0x00000000004006e4 <+36>:    jg     0x4006f1 <encode_ptr_ref_tmp(unsigned int*&, int)+49>
   0x00000000004006e6 <+38>:    mov    %esi,0x4(%rax)
   0x00000000004006e9 <+41>:    add    $0x8,%rax
   0x00000000004006ed <+45>:    mov    %rax,(%rdi)      # ptr store
   0x00000000004006f0 <+48>:    retq   
   0x00000000004006f1 <+49>:    cmp    $0xffffff,%esi
   0x00000000004006f7 <+55>:    movl   $0x0,0x4(%rax)
   0x00000000004006fe <+62>:    jg     0x40070b <encode_ptr_ref_tmp(unsigned int*&, int)+75>
   0x0000000000400700 <+64>:    mov    %esi,0x8(%rax)
   0x0000000000400703 <+67>:    add    $0xc,%rax
   0x0000000000400707 <+71>:    mov    %rax,(%rdi)      # ptr store
   0x000000000040070a <+74>:    retq   
   0x000000000040070b <+75>:    movl   $0x0,0x8(%rax)
   0x0000000000400712 <+82>:    mov    %esi,0xc(%rax)
   0x0000000000400715 <+85>:    add    $0x10,%rax
   0x0000000000400719 <+89>:    mov    %rax,(%rdi)      # ptr store
   0x000000000040071c <+92>:    retq   

Again, the ptr ref and buf object versions are exactly the same (encode_buf(), encode_buf_tmp()).

Now we arrived to the core issue: test_encode_ptr_ref() calls the above encode_ptr_ref() in a loop, and encodes an array of ints. encode_ptr_ref() is not called, but inlined, no other calls are made, so the compiler/optimizer should optimize away the loads/stores, but unfortunately, it doesn't: in every loop iteration, the write ptr is loaded/stored.
   0x00000000004008f0 <+0>:     jmp    0x4008fa <test_encode_ptr_ref(unsigned int*&, int const*, int)+10>
   0x00000000004008f2 <+2>:     nopw   0x0(%rax,%rax,1)
   0x00000000004008f8 <+8>:     mov    %eax,(%rcx)     # inner loop head: store value
   0x00000000004008fa <+10>:    sub    $0x1,%edx
   0x00000000004008fd <+13>:    js     0x400938 <test_encode_ptr_ref(unsigned int*&, int const*, int)+72>
   0x00000000004008ff <+15>:    add    $0x4,%rsi
   0x0000000000400903 <+19>:    mov    (%rdi),%rcx     # load ptr
   0x0000000000400906 <+22>:    mov    -0x4(%rsi),%eax # load value
   0x0000000000400909 <+25>:    lea    0x4(%rcx),%r8
   0x000000000040090d <+29>:    cmp    $0xff,%eax
   0x0000000000400912 <+34>:    mov    %r8,(%rdi)      # store ptr
   0x0000000000400915 <+37>:    jle    0x4008f8 <test_encode_ptr_ref(unsigned int*&, int const*, int)+8>
   0x0000000000400917 <+39>:    lea    0x8(%rcx),%r8
   0x000000000040091b <+43>:    cmp    $0xffff,%eax
   0x0000000000400920 <+48>:    movl   $0x0,(%rcx)
   0x0000000000400926 <+54>:    mov    %r8,(%rdi)      # store ptr
   0x0000000000400929 <+57>:    jg     0x40093a <test_encode_ptr_ref(unsigned int*&, int const*, int)+74>
   0x000000000040092b <+59>:    sub    $0x1,%edx
   0x000000000040092e <+62>:    mov    %eax,0x4(%rcx)
   0x0000000000400931 <+65>:    jns    0x4008ff <test_encode_ptr_ref(unsigned int*&, int const*, int)+15>
   0x0000000000400933 <+67>:    nopl   0x0(%rax,%rax,1)
   0x0000000000400938 <+72>:    repz retq 
   0x000000000040093a <+74>:    cmp    $0xffffff,%eax
   0x000000000040093f <+79>:    movl   $0x0,0x4(%rcx)
   0x0000000000400946 <+86>:    jg     0x400954 <test_encode_ptr_ref(unsigned int*&, int const*, int)+100>
   0x0000000000400948 <+88>:    lea    0xc(%rcx),%r8
   0x000000000040094c <+92>:    mov    %r8,(%rdi)    # store ptr
   0x000000000040094f <+95>:    mov    %eax,0x8(%rcx)
   0x0000000000400952 <+98>:    jmp    0x4008fa <test_encode_ptr_ref(unsigned int*&, int const*, int)+10>
   0x0000000000400954 <+100>:   lea    0x10(%rcx),%r8
   0x0000000000400958 <+104>:   movl   $0x0,0x8(%rcx)
   0x000000000040095f <+111>:   mov    %r8,(%rdi)    # store ptr
   0x0000000000400962 <+114>:   mov    %eax,0xc(%rcx)
   0x0000000000400965 <+117>:   jmp    0x4008fa <test_encode_ptr_ref(unsigned int*&, int const*, int)+10>

The generated code for write_run_ptr_ref() loaded the ptr before the loop, the loop used the reg and stored back after the loop. Why can't the same be done for test_encode_ptr_ref()?

I got a hunch that maybe the 'if' blocks are related, so I wrote a simple fn that copies n ints from a src ptr to a dst ptr, passed as ref: copy_ptr_ref()
   0x00000000004005e0 <+0>:     test   %edx,%edx
   0x00000000004005e2 <+2>:     jle    0x400607 <copy_ptr_ref(unsigned int*&, int const*, int)+39>
   0x00000000004005e4 <+4>:     mov    (%rdi),%r8          # load dst
   0x00000000004005e7 <+7>:     sub    $0x1,%edx
   0x00000000004005ea <+10>:    xor    %eax,%eax
   0x00000000004005ec <+12>:    add    $0x1,%rdx
   0x00000000004005f0 <+16>:    mov    (%rsi,%rax,4),%ecx  # load int
   0x00000000004005f3 <+19>:    mov    %ecx,(%r8,%rax,4)   # store int
   0x00000000004005f7 <+23>:    add    $0x1,%rax
   0x00000000004005fb <+27>:    cmp    %rdx,%rax
   0x00000000004005fe <+30>:    jne    0x4005f0 <copy_ptr_ref(unsigned int*&, int const*, int)+16>
   0x0000000000400600 <+32>:    lea    (%r8,%rax,4),%rax
   0x0000000000400604 <+36>:    mov    %rax,(%rdi)         # store dst
   0x0000000000400607 <+39>:    repz retq 

No redundant loads/stores in the loop. The next step was to introduce a condition: the int is copied only if it is not divisible by a given number: copy_ptr_ref_pred(). GOTCHA! The dst load/store appeared in the loop:
   0x0000000000400610 <+0>:     mov    %edx,%r9d
   0x0000000000400613 <+3>:     nopl   0x0(%rax,%rax,1)
   0x0000000000400618 <+8>:     sub    $0x1,%r9d        # loop beg
   0x000000000040061c <+12>:    js     0x400643 <copy_ptr_ref_pred(unsigned int*&, int const*, int, int)+51>
   0x000000000040061e <+14>:    add    $0x4,%rsi
   0x0000000000400622 <+18>:    mov    -0x4(%rsi),%r8d  # load int
   0x0000000000400626 <+22>:    mov    %r8d,%eax
   0x0000000000400629 <+25>:    cltd   
   0x000000000040062a <+26>:    idiv   %ecx
   0x000000000040062c <+28>:    test   %edx,%edx
   0x000000000040062e <+30>:    je     0x400618 <copy_ptr_ref_pred(unsigned int*&, int const*, int, int)+8>
   0x0000000000400630 <+32>:    mov    (%rdi),%rax      # load dst
   0x0000000000400633 <+35>:    sub    $0x1,%r9d
   0x0000000000400637 <+39>:    lea    0x4(%rax),%rdx
   0x000000000040063b <+43>:    mov    %rdx,(%rdi)      # store dst
   0x000000000040063e <+46>:    mov    %r8d,(%rax)      # store int
   0x0000000000400641 <+49>:    jns    0x40061e <copy_ptr_ref_pred(unsigned int*&, int const*, int, int)+14>
   0x0000000000400643 <+51>:    repz retq 

If I load the dst into a local variable, it gets a register allocated, and the load/store in each iteration is eliminated. However, the compiler should do this automatically, imho. copy_ptr_ref_pred_tmp():
   0x0000000000400650 <+0>:     test   %edx,%edx
   0x0000000000400652 <+2>:     jle    0x400686 <copy_ptr_ref_pred_tmp(unsigned int*&, int const*, int, int)+54>
   0x0000000000400654 <+4>:     movslq %edx,%rdx
   0x0000000000400657 <+7>:     mov    (%rdi),%r9       # load dst once
   0x000000000040065a <+10>:    lea    (%rsi,%rdx,4),%r10
   0x000000000040065e <+14>:    xchg   %ax,%ax
   0x0000000000400660 <+16>:    cmp    %r10,%rsi
   0x0000000000400663 <+19>:    je     0x400683 <copy_ptr_ref_pred_tmp(unsigned int*&, int const*, int, int)+51>
   0x0000000000400665 <+21>:    add    $0x4,%rsi
   0x0000000000400669 <+25>:    mov    -0x4(%rsi),%r8d  # load int
   0x000000000040066d <+29>:    mov    %r8d,%eax
   0x0000000000400670 <+32>:    cltd   
   0x0000000000400671 <+33>:    idiv   %ecx
   0x0000000000400673 <+35>:    test   %edx,%edx
   0x0000000000400675 <+37>:    je     0x400660 <copy_ptr_ref_pred_tmp(unsigned int*&, int const*, int, int)+16>
   0x0000000000400677 <+39>:    mov    %r8d,(%r9)       # store int
   0x000000000040067a <+42>:    add    $0x4,%r9
   0x000000000040067e <+46>:    cmp    %r10,%rsi
   0x0000000000400681 <+49>:    jne    0x400665 <copy_ptr_ref_pred_tmp(unsigned int*&, int const*, int, int)+21>
   0x0000000000400683 <+51>:    mov    %r9,(%rdi)       # store dst once
   0x0000000000400686 <+54>:    repz retq 

There are more complex cases, where eg the encoder fn is split into two parts: the most likely case, which should be inlined, and the rest, which should be called. See test_encode_ptr_ref_inline(). For this fn, the ideal code would be the one that loads the dst ptr into a register, and uses the reg for the inlined encoder code, and if the out-of-line part should be called, it stores the reg back to the ref, calls the ool part, then loads back the reg from the ref. This way the most likely parts of the basic encoders could be inlined into the main encoder loop, and the most likely path would run without unnecessary loads/stores.

Regards, Peter


---


### compiler : `gcc`
### title : `Suboptimal code generation with eigen library`
### open_at : `2014-08-10T10:20:39Z`
### last_modified_date : `2021-07-18T21:18:19Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=62080
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.8.3`
### severity : `normal`
### contents :
Created attachment 33281
Source code used to get the provided assembly

I'm currently optimizing some code using the eigen library and I'm stumbling over an interesting problem. 
I have a function, which I wrote in two different ways (the attributes are there to provide some optimization barriers, dimEigen is a member variable of the containing class): 


void eigenClamp(Eigen::Vector4i& vec) __attribute__((noinline, noclone))
{
	vec = vec.array().min(dimEigen.array()).max(Eigen::Array4i::Zero());
}

void eigenClamp2(Eigen::Vector4i& vec) __attribute__((noinline, noclone))
{
	vec = vec.array().min(dimEigen.array());
	vec = vec.array().max(Eigen::Array4i::Zero());
}

I'm compiling this on a core i7 920 using -O2 -fno-exceptions -fno-rtti -std=c++11 -march=native

The first function generates this assembly, which looks great: 

movdqu	(%rsi), %xmm1
movdqu	(%rdi), %xmm0
pminsd	%xmm1, %xmm0
pxor	%xmm1, %xmm1
pmaxsd	%xmm1, %xmm0
movdqa	%xmm0, (%rsi)

The second version does this: 

movdqa	(%rsi), %xmm0
pminsd	(%rdi), %xmm0
movdqa	%xmm0, (%rsi) <-- 
pxor	%xmm0, %xmm0
movdqu	(%rsi), %xmm1 <-- 
pmaxsd	%xmm1, %xmm0
movdqa	%xmm0, (%rsi)

It seems, because there are two lines in the original source code, the result of the first expression is written to memory and then two instructions later, read back from memory. This makes this function almost 50% slower in what I can measure. As I find the latter code much easier to read as the former, it would be great if the same assembly would be generated. 

Also, I note that in the second version, the pminsd is executed directly from the memory source, while in the first version, it is read to a register and then pminsd is called. Thus, I'd love to see this code: 

movdqu	(%rsi), %xmm1
pminsd	(%rdi), %xmm1
pxor	%xmm1, %xmm1
pmaxsd	%xmm1, %xmm0
movdqa	%xmm0, (%rsi)

As a reference, I'm attaching the complete source code and the generated assembly


---


### compiler : `gcc`
### title : `Poor code generation (x86-64)`
### open_at : `2014-08-18T01:57:13Z`
### last_modified_date : `2021-09-26T22:38:35Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=62166
### status : `NEW`
### tags : `missed-optimization, ra`
### component : `target`
### version : `5.0`
### severity : `enhancement`
### contents :
$ gcc-snapshot.sh --version
gcc (Debian 20140814-1) 4.10.0 20140814 (experimental) [trunk revision 213954]

weird_code_gen.c:

#include <stdint.h>

typedef void (*f_t)(uint64_t rdi, uint64_t rsi, uint64_t rdx, uint64_t rcx);
void weird_code_gen(uint64_t rdi, uint64_t rsi, uint64_t rdx, uint64_t rcx);
f_t dispatch[] = {&weird_code_gen};

void weird_code_gen(uint64_t rdi, uint64_t rsi, uint64_t rdx, uint64_t rcx) {
  int64_t s8 = (int8_t) rcx;
  uint32_t u8 = (uint8_t) (rcx >> 8);
  //asm volatile ("" : "+r" (rcx));
  rdx += s8;
  rcx >>= 16;
  dispatch[u8](rdi, rsi, rdx, rcx);
}

int main(void) {
  return 0;
}

$ gcc-snapshot.sh -O3 weird_code_gen.c && objdump -d -m i386:x86-64:intel a.out |less

00000000004004c0 <weird_code_gen>:
  4004c0:       48 89 c8                mov    rax,rcx
  4004c3:       53                      push   rbx
  4004c4:       0f b6 dd                movzx  ebx,ch
  4004c7:       48 0f be c0             movsx  rax,al
  4004cb:       48 c1 e9 10             shr    rcx,0x10
  4004cf:       48 01 c2                add    rdx,rax
  4004d2:       48 8b 04 dd d8 08 60    mov    rax,QWORD PTR [rbx*8+0x6008d8]
  4004d9:       00 
  4004da:       5b                      pop    rbx
  4004db:       ff e0                   jmp    rax


Code generation with asm volatile uncommented:

00000000004004c0 <weird_code_gen>:
  4004c0:       4c 0f be c1             movsx  r8,cl
  4004c4:       0f b6 c5                movzx  eax,ch
  4004c7:       89 c0                   mov    eax,eax
  4004c9:       48 c1 e9 10             shr    rcx,0x10
  4004cd:       4c 01 c2                add    rdx,r8
  4004d0:       ff 24 c5 d0 08 60 00    jmp    QWORD PTR [rax*8+0x6008d0]

The asm volatile workaround fails if u8 is of type uint64_t.


---


### compiler : `gcc`
### title : `std::string==const char* could compare sizes first`
### open_at : `2014-08-19T13:21:24Z`
### last_modified_date : `2022-06-14T20:20:49Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=62187
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `libstdc++`
### version : `5.0`
### severity : `enhancement`
### contents :
Hello,

when I compare 2 basic_string with ==, libstdc++ only uses the optimization of first checking that the sizes are the same (before calling compare) if __is_char<_CharT> and the traits and allocator are the default ones. I don't understand why, but assuming there is a good reason, I believe the optimization should still apply when comparing std::string and const char*.

(this applies to __vstring as well)

This was noticed in PR 62156, where we also see that std::string("foo") does a memcpy of size 3 then sets the 4th char to '\0', where a single memcpy of size 4 would make sense.


---


### compiler : `gcc`
### title : `extra shift generated for vector integer division by constant 2`
### open_at : `2014-08-19T18:24:06Z`
### last_modified_date : `2020-09-03T20:50:28Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=62191
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.9.0`
### severity : `enhancement`
### contents :
Using gcc 4.9:

$ cat sdiv.c
typedef int vecint __attribute__((vector_size(16))); 
vecint f(vecint x) { 
	return x/2;
} 

$ gcc -O2 sdiv.c -S -o  -
...
	movdqa	%xmm0, %xmm1
	psrad	$31, %xmm1    <--- splat the sign bit
	psrld	$31, %xmm1    <--- then shift sign bit down to LSB
	paddd	%xmm1, %xmm0  <--- add sign bit to quotient
	psrad	$1, %xmm0     <--- div via alg shift right
	ret

--------------------------------------------------------------

I don't think the first shift right algebraic is necessary. We splat the sign bit and then shift that right logically, so the upper bits are all zero'd anyway. 

This is a special case for signed integer division by 2. You need that first 'psrad' for any other power of 2 because the subsequent logical shift would not also be a shift of 31.


---


### compiler : `gcc`
### title : `missed optimization wrt module for loop variable`
### open_at : `2014-08-21T22:39:53Z`
### last_modified_date : `2021-12-25T07:48:30Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=62220
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `5.0`
### severity : `enhancement`
### contents :
Created attachment 33376
program to measure difference of the original and proposed optimized code

I've optimized some prominent code bases by hand to achieve significant speedup but this optimization could have been performed by gcc.  The problem is that some program authors underestimate the price of integer module operations.  I attaching a test program (x86-64) below and the time difference I see about 1500%.

The general pattern is:

   loop index variable I with upper limit L

      for (I = <?>; I < L; ++I)

   inside loop use I % M where M is loop in-variant

      e.g.: var[I % M]

This could be optimized to

   compute LL = L - L % M

   loop index variable I with upper limit LL; nested second loop

     J = <?> % M
     for (I = <?>; I < LL; ) {
       for (; J < M; ++I, ++J) {

          ... loop body ...

          ... e.g., var[J]
          ... instead of var[I % M]
       }
       J = 0;
     }


---


### compiler : `gcc`
### title : `[DR535] Templated move not elided`
### open_at : `2014-08-22T11:36:53Z`
### last_modified_date : `2021-08-23T00:28:37Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=62227
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `c++`
### version : `4.8.0`
### severity : `enhancement`
### contents :
#include <stdio.h>

struct S {
  S(int) {}
  S(const S&) = default;   // (1)
  template <class = void>  // (2)
  S(S&& other) {
    puts("move");
  }
};

int main() {
  S s = 42;
  (void)s;
}

This program unexpectedly prints "move". The expected output is empty (move is elided).

The program prints nothing (as expected) if any of the following is done:

  - Line (1) is removed.
  - Line (2) is removed.
  - The program is compiled with clang.


---


### compiler : `gcc`
### title : `[11/12/13/14 Regression] gcc.dg/graphite/vect-pr43423.c XFAILed`
### open_at : `2014-09-01T13:21:37Z`
### last_modified_date : `2023-07-07T10:30:24Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=62630
### status : `NEW`
### tags : `missed-optimization, testsuite-fail, xfail`
### component : `tree-optimization`
### version : `5.0`
### severity : `normal`
### contents :
Since ca. 20140818 (r214099), gcc.dg/graphite/vect-pr43423.c on SPARC.  I'm
attaching the tree dump.

  Rainer


---


### compiler : `gcc`
### title : `unnecessary calls to __dynamic_cast`
### open_at : `2014-09-04T12:02:12Z`
### last_modified_date : `2022-04-28T17:33:08Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=63164
### status : `NEW`
### tags : `missed-optimization`
### component : `c++`
### version : `4.9.1`
### severity : `enhancement`
### contents :
The code

  struct A {
    virtual ~A() {}
  };

  struct B final : A {
    virtual ~B() {}
  };

  B* dc(A* a) {
    return dynamic_cast<B*>(a);
  }

compiles into the following assembly, which contains a call (jump) to __dynamic_cast:

0000000000000000 <dc(A*)>:
   0:	48 85 ff             	test   %rdi,%rdi
   3:	74 1b                	je     20 <dc(A*)+0x20>
   5:	31 c9                	xor    %ecx,%ecx
   7:	ba 00 00 00 00       	mov    $0x0,%edx
			8: R_X86_64_32	typeinfo for B
   c:	be 00 00 00 00       	mov    $0x0,%esi
			d: R_X86_64_32	typeinfo for A
  11:	e9 00 00 00 00       	jmpq   16 <dc(A*)+0x16>
			12: R_X86_64_PC32	__dynamic_cast-0x4
  16:	66 2e 0f 1f 84 00 00 	nopw   %cs:0x0(%rax,%rax,1)
  1d:	00 00 00 
  20:	31 c0                	xor    %eax,%eax
  22:	c3                   	retq   


However, since B is declared final, a simple compare of a's typeinfo with B's would suffice.  This is a missed optimization opportunity.


---


### compiler : `gcc`
### title : `[9/10/11/12 Regression] Fails to simplify comparison`
### open_at : `2014-09-05T08:32:53Z`
### last_modified_date : `2021-09-06T07:48:48Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=63184
### status : `RESOLVED`
### tags : `deferred, missed-optimization, patch, TREE`
### component : `middle-end`
### version : `4.9.1`
### severity : `minor`
### contents :
c-c++-common/pr19807-2.c

/* { dg-do link } */

extern void link_error(void);
int i;
int main()
{
  int a[4];
  if ((char*)&a[1] + 4*i + 4 != (char*)&a[i+2])
    link_error();
  return 0;
}

Fails with all optimization levels for all compilers.

c-c++-common/pr19807-3.c

/* { dg-do link } */

extern void link_error(void);
int i;
int main()
{
  int a[4];
  if (&a[1] + i + 1 != &a[i+2])
    link_error();
  return 0;
}

gcc 4.7 passes with -O[01] but fails with -O2+
gcc 4.8 and 4.9 fail with -O0 but passes with -O1+ (thanks to SLSR)
gcc 5.0 since the fix for PR63148 fails

which is a regression.

We don't seem to systematically use sth like the tree-affine.c framework
to simplify address comparisons and the fact that tree-reassoc.c doesn't
in any way associate pointer arithmetic doesn't help either.


---


### compiler : `gcc`
### title : `Improve DSE with branches`
### open_at : `2014-09-05T10:51:52Z`
### last_modified_date : `2021-09-25T11:02:56Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=63185
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `5.0`
### severity : `enhancement`
### contents :
#include <stdlib.h>
#include <string.h>
void g();
void f(int n){
  char*p=malloc(1024);
  memset(p,8,1024);
  if(n)g();
}

We do not manage to remove the dead store (memset) because there is a PHI that doesn't post-dominate the statement.


---


### compiler : `gcc`
### title : `tree vectorizer does not make use of alignment information from VRP/CCP`
### open_at : `2014-09-08T04:05:09Z`
### last_modified_date : `2023-06-14T22:03:36Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=63202
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `5.0`
### severity : `enhancement`
### contents :
char b[100];

void alignment(int *p)
{
        if ((uintptr_t)p & 15) __builtin_unreachable();
        int i;
        for (i = 0; i < 64; i++)
                b[i] = p[i] ^ 0x1f;
}

-O3 results in 

        leaq    256(%rdi), %rax
        cmpq    $b, %rax
        jbe     .L9
        cmpq    $b+64, %rdi
        jb      .L5
.L9:
        movdqu  (%rdi), %xmm0
        movdqu  16(%rdi), %xmm2
        movdqa  %xmm0, %xmm1
        punpcklwd       %xmm2, %xmm0
        movdqu  48(%rdi), %xmm3
        punpckhwd       %xmm2, %xmm1
        movdqu  112(%rdi), %xmm4
...

.L5:
        xorl    %eax, %eax
        .p2align 4,,10
        .p2align 3
.L8:
        movzbl  (%rdi,%rax,4), %edx
        addq    $1, %rax
        xorl    $31, %edx
        movb    %dl, b-1(%rax)
        cmpq    $64, %rax
        jne     .L8
        rep ret


The extra loop for the unaligned case shouldn't be needed because VRP or CCP can prove that the pointer is always aligned from the builtin_unreachable test.

vrp1 doesn't handle this

p_3(D): VARYING
p.0_4: [0, +INF]

it only is known in vrp2, which is too late for the vectorizer?

p_1: ~[0B, 0B]  EQUIVALENCES: { p_3(D) } (1 elements)

Also the vectorizer uses a different variable which does not inherit the known alignment:

 <bb 2>:
  p.0_4 = (long unsigned int) p_3(D);
  _5 = p.0_4 & 15;
  if (_5 != 0)
    goto <bb 3>;
  else
    goto <bb 4>;

  <bb 3>:
  __builtin_unreachable ();

p.0_4 is unknown range again

p.0_4: [0, +INF]

Fixing this would allow implementing an __assume() macro behaving similar to VC++


---


### compiler : `gcc`
### title : `Detecting byteswap sequence`
### open_at : `2014-09-13T17:41:42Z`
### last_modified_date : `2018-11-19T13:22:30Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=63259
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.1`
### severity : `normal`
### contents :
This is just silly. GCC optimizes the first function into single opcode (bswap), but not the other. For Clang, it's the other way around.

unsigned byteswap_gcc(unsigned result)
{
    result = ((result & 0xFFFF0000u) >>16) | ((result & 0x0000FFFFu) <<16);
    result = ((result & 0xFF00FF00u) >> 8) | ((result & 0x00FF00FFu) << 8);
    return result;
}
unsigned byteswap_clang(unsigned result)
{
    result = ((result & 0xFF00FF00u) >> 8) | ((result & 0x00FF00FFu) << 8);
    result = ((result & 0xFFFF0000u) >>16) | ((result & 0x0000FFFFu) <<16);
    return result;
}

unsigned byteswap(unsigned v)
{
    #ifdef __clang__
     return byteswap_clang(v);
    #else
     return byteswap_gcc(v);
    #endif
}

GCC output:

    byteswap_gcc:
        movl    %edi, %eax
        bswap   %eax
        ret

    byteswap_clang:
        movl    %edi, %eax
        andl    $-16711936, %eax
        shrl    $8, %eax
        movl    %eax, %edx
        movl    %edi, %eax
        andl    $16711935, %eax
        sall    $8, %eax
        orl     %edx, %eax
        roll    $16, %eax
        ret

    byteswap:
        movl    %edi, %eax
        bswap   %eax
        ret

Clang output:

    byteswap_gcc:                           # @byteswap_gcc
        roll    $16, %edi
        movl    %edi, %eax
        shrl    $8, %eax
        andl    $16711935, %eax         # imm = 0xFF00FF
        shll    $8, %edi
        andl    $-16711936, %edi        # imm = 0xFFFFFFFFFF00FF00
        orl     %eax, %edi
        movl    %edi, %eax
        retq

    byteswap_clang:                         # @byteswap_clang
        bswapl  %edi
        movl    %edi, %eax
        retq
    
    byteswap:                               # @byteswap
        bswapl  %edi
        movl    %edi, %eax
        retq


Tested both -m32 and -m64, with options: -Ofast -S
Tested versions:
- gcc (Debian 4.9.1-11) 4.9.1  Target: x86_64-linux-gnu
- Debian clang version 3.5.0-+rc1-2 (tags/RELEASE_35/rc1) (based on LLVM 3.5.0)  Target: x86_64-pc-linux-gnu


---


### compiler : `gcc`
### title : `Should commute arithmetic with vector load`
### open_at : `2014-09-15T18:53:30Z`
### last_modified_date : `2021-08-15T22:34:00Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=63271
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.1`
### severity : `enhancement`
### contents :
Consider

    #include <emmintrin.h>

    __m128i foo(char C)
    {
      return _mm_set_epi8(   0,    C,  2*C,  3*C,
                           4*C,  5*C,  6*C,  7*C,
                           8*C,  9*C, 10*C, 11*C,
                          12*C, 13*C, 14*C, 15*C);
    }

    __m128i bar(char C)
    {
      __m128i v = _mm_set_epi8(0, 1, 2, 3, 4, 5, 6, 7,
                               8, 9,10,11,12,13,14,15);
      v *= C;
      return v;
    }

I *believe* these functions compute the same value, and should therefore generate identical code, but with gcc 4.9 foo() generates considerably larger and slower code.

The test case is expressed in terms of x86 <emmintrin.h> but I have no reason to believe it isn't a generic missed optimization in the tree-level vectorizer.


---


### compiler : `gcc`
### title : `ARM - NEON excessive use of vmov for vtbl2 / uint8x8x2 for shuffling data unnecessarily around`
### open_at : `2014-09-16T12:07:08Z`
### last_modified_date : `2019-09-12T04:23:22Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=63277
### status : `NEW`
### tags : `missed-optimization, ra`
### component : `rtl-optimization`
### version : `5.0`
### severity : `normal`
### contents :
Created attachment 33500
small example source code

armv7a-hardfloat-linux-gnueabi-gcc-5.0.0 -v                      
Using built-in specs.
COLLECT_GCC=/opt/gcc/bin/armv7a-hardfloat-linux-gnueabi-gcc-5.0.0
COLLECT_LTO_WRAPPER=/opt/gcc/libexec/gcc/armv7a-hardfloat-linux-gnueabi/5.0.0/lto-wrapper
Target: armv7a-hardfloat-linux-gnueabi
Configured with: /home/janne/src/gcc-trunk/configure --host=x86_64-pc-linux-gnu --target=armv7a-hardfloat-linux-gnueabi --build=x86_64-pc-linux-gnu --prefix=/opt/gcc/ --enable-languages=c,c++,fortran --enable-obsolete --enable-secureplt --disable-werror --with-system-zlib --enable-nls --without-included-gettext --enable-checking=release --enable-libstdcxx-time --enable-poison-system-directories --with-sysroot=/usr/armv7a-hardfloat-linux-gnueabi --disable-bootstrap --enable-__cxa_atexit --enable-clocale=gnu --disable-multilib --disable-altivec --disable-fixed-point --with-float=hard --with-arch=armv7-a --with-float=hard --with-fpu=neon --disable-libgcj --enable-libgomp --disable-libmudflap --disable-libssp --enable-lto --without-cloog
Thread model: posix
gcc version 5.0.0 20140916 (experimental) (GCC) 

armv7a-hardfloat-linux-gnueabi-gcc-5.0.0 -march=armv7-a -mfpu=neon -O3 -S arm_neon_excessive_vmov.c -o -
        .arch armv7-a
        .eabi_attribute 27, 3
        .eabi_attribute 28, 1
        .fpu neon
        .eabi_attribute 20, 1
        .eabi_attribute 21, 1
        .eabi_attribute 23, 3
        .eabi_attribute 24, 1
        .eabi_attribute 25, 1
        .eabi_attribute 26, 2
        .eabi_attribute 30, 2
        .eabi_attribute 34, 1
        .eabi_attribute 18, 4
        .file   "arm_neon_excessive_vmov.c"
        .text
        .align  2
        .global gf_w8_split_multiply_region_neon
        .type   gf_w8_split_multiply_region_neon, %function
gf_w8_split_multiply_region_neon:
        @ args = 4, pretend = 0, frame = 0
        @ frame_needed = 0, uses_anonymous_args = 0
        str     lr, [sp, #-4]!
        mov     r3, r3, asl #4
        ldr     ip, [sp, #4]
        add     lr, r0, #4096
        add     lr, lr, r3
        add     r0, r0, r3
        vmov.i8 q15, #15  @ v16qi
        add     ip, r2, ip, lsl #4
        vld1.8  {d18-d19}, [lr]
        cmp     r1, ip
        vld1.8  {d16-d17}, [r0]
        ldrcs   pc, [sp], #4
        vmov    d27, d18  @ v8qi
        vmov    d26, d19  @ v8qi
        vmov    d25, d16  @ v8qi
        vmov    d24, d17  @ v8qi
.L3:
        vld1.8  {d18-d19}, [r1]
        vmov    d20, d25  @ v8qi
        vmov    d21, d24  @ v8qi
        add     r1, r1, #16
        vshr.u8 q14, q9, #4
        cmp     r1, ip
        vmov    d22, d27  @ v8qi
        vmov    d23, d26  @ v8qi
        vtbl.8  d16, {d20, d21}, d28
        vand    q9, q9, q15
        vtbl.8  d28, {d20, d21}, d29
        vtbl.8  d17, {d22, d23}, d18
        vmov    d29, d28  @ v8qi
        vmov    d28, d16  @ v8qi
        vtbl.8  d16, {d22, d23}, d19
        vswp    d16, d17
        veor    q8, q8, q14
        vst1.8  {d16-d17}, [r2]
        add     r2, r2, #16
        bcc     .L3
        ldr     pc, [sp], #4
        .size   gf_w8_split_multiply_region_neon, .-gf_w8_split_multiply_region_neon
        .ident  "GCC: (GNU) 5.0.0 20140916 (experimental)"
        .section        .note.GNU-stack,"",%progbits

There is no need for the vmovs/vswp and clang 3.4 generates from the same source file assembly without them.


---


### compiler : `gcc`
### title : `Fails to compute loop bound from constant string`
### open_at : `2014-09-16T14:03:43Z`
### last_modified_date : `2021-08-11T04:35:17Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=63278
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.1`
### severity : `enhancement`
### contents :
For

inline constexpr size_t hashString(const char* str, size_t hash = 5381)
{
return (*str) ? hashString(str + 1, hash + (hash << 5) + *str) : hash;
}
 
inline size_t hashString2(const char* str) __attribute__ ((pure));
size_t hashString2(const char* str)
{
size_t hash = 5381;
while (*str) {
hash += (hash << 5) + *str;
str++;
}
return hash;
}

size_t foo()
{
  return hashString("foo") + hashString2("foo");
}

that is, the loop created by tail-recursion and the manual loop we fail
to compute the number of iterations and thus fail to unroll them.
Both look like

  <bb 2>:

  <bb 3>:
  # str_28 = PHI <"foo"(2), str_10(4)>
  # _29 = PHI <102(2), _4(4)>
  # hash_30 = PHI <5381(2), hash_9(4)>
  _6 = hash_30 << 5;
  _8 = (long unsigned int) _29;
  _23 = _6 + _8;
  hash_9 = _23 + hash_30;
  str_10 = str_28 + 1;
  _4 = *str_10;
  if (_4 != 0)
    goto <bb 4>;
  else
    goto <bb 8>;

  <bb 4>:
  goto <bb 3>;

Similar cases may occur when iterating over a constant initializer
guarded by a NULL pointer.

SCEV cannot handle the above (obviously), but eventually hacking up
some special-case code may be worth the trouble.


---


### compiler : `gcc`
### title : `powerpc64le creates 64 bit constants from scratch instead of loading them`
### open_at : `2014-09-16T23:01:09Z`
### last_modified_date : `2022-03-08T16:20:41Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=63281
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `5.0`
### severity : `enhancement`
### contents :
The following testcase:

#define CONST1 0x1234567812345678
#define CONST2 0x2345678123456781
#define CONST3 0x3456781234567812
#define CONST4 0x4567812345678123
#define CONST5 0x5678123456781234
#define CONST6 0x6781234567812345
#define CONST7 0x7812345678123456
#define CONST8 0x8123456781234567

void foo(unsigned long *a, unsigned long *b, unsigned long *c,
         unsigned long *d, unsigned long *e, unsigned long *f,
         unsigned long *g, unsigned long *h)
{
        *a = CONST1;
        *b = CONST2;
        *c = CONST3;
        *d = CONST4;
        *e = CONST5;
        *f = CONST6;
        *g = CONST7;
        *h = CONST8;
}

produces some pretty horrible code. We really should be loading the constants. This looks to be present on 4.8, 4.9 and 5.0.

foo:
	std 27,-40(1)
	std 28,-32(1)
	lis 27,0x1234
	lis 28,0x2345
	std 29,-24(1)
	std 30,-16(1)
	lis 29,0x3456
	lis 30,0x4567
	std 31,-8(1)
	lis 31,0x5678
	ori 27,27,0x5678
	ori 28,28,0x6781
	ori 29,29,0x7812
	ori 30,30,0x8123
	ori 31,31,0x1234
	sldi 27,27,32
	sldi 28,28,32
	sldi 29,29,32
	sldi 30,30,32
	sldi 31,31,32
	lis 12,0x6781
	lis 0,0x7812
	lis 11,0x8123
	oris 27,27,0x1234
	oris 28,28,0x2345
	oris 29,29,0x3456
	oris 30,30,0x4567
	oris 31,31,0x5678
	ori 27,27,0x5678
	ori 28,28,0x6781
	ori 29,29,0x7812
	ori 30,30,0x8123
	ori 31,31,0x1234
	std 27,0(3)
	ld 27,-40(1)
	ori 12,12,0x2345
	ori 0,0,0x3456
	std 28,0(4)
	std 29,0(5)
	ori 11,11,0x4567
	sldi 12,12,32
	std 30,0(6)
	ld 28,-32(1)
	ld 29,-24(1)
	sldi 0,0,32
	sldi 11,11,32
	std 31,0(7)
	ld 30,-16(1)
	ld 31,-8(1)
	oris 12,12,0x6781
	oris 0,0,0x7812
	oris 11,11,0x8123
	ori 12,12,0x2345
	ori 0,0,0x3456
	ori 11,11,0x4567
	std 12,0(8)
	std 0,0(9)
	std 11,0(10)
	blr


---


### compiler : `gcc`
### title : `vector shuffle resembling vector shift not expanded optimally`
### open_at : `2014-09-22T11:56:31Z`
### last_modified_date : `2022-03-08T16:20:55Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=63330
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.9.1`
### severity : `enhancement`
### contents :
typedef int v4si __attribute__((vector_size(16)));
v4si foo (v4si x)
{
  return __builtin_shuffle (x, (v4si){ 0, 0, 0, 0 },
                             (v4si){4, 3, 2, 1 });
}

and similar shuffles "shifting" a vector by whole-element amounts
left/right and inserting zeros are not expanded optimally (while
the target has at least a vec_shr optab which suggests sth would
be available).

With -mavx2 I get for the above

        vpxor   %xmm1, %xmm1, %xmm1
        vpalignr        $4, %xmm0, %xmm1, %xmm0
        vpshufd $27, %xmm0, %xmm0

while I expected sth like

        psrldq %xmm0, $4

__builtin_shuffle (x, (v4si) { -1, -1, -1, -1 }, ... )

Arbitrary constants "shifted in" could be handled the same by IORing
the shifted in value after the psrldq in the appropriate elements
for the cost of an extra vector constant.


---


### compiler : `gcc`
### title : `compare one character to many: faster`
### open_at : `2014-10-05T21:28:15Z`
### last_modified_date : `2023-10-25T19:02:17Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=63464
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `5.0`
### severity : `enhancement`
### contents :
This is inspired by reading this post:

http://stackoverflow.com/questions/26124620/why-does-msvc-emit-a-useless-movsx-before-performing-this-bit-test

which shows that bit testing can provide a very efficient lookup table for small sizes, and in particular when we want to test if a character belongs to a predefined set.

char*f1(char*s){
  while (*s == ' ' || *s == ',' || *s == '\r' || *s == '\n')
    ++s;
  return s;
}
char*f2(char*s){
  long n = (1L << ' ') | (1L << ',') | (1L << '\r') | (1L << '\n');
  int m = max(max(' ',','),max('\r','\n'));
  while(*s <= m && (n & (1L << *s)))
    ++s;
  return s;
}

On x86_64, the first one compiles to a bunch of cmpb+sete, combined with orl. The second one has one cmpb+jg but uses btq+jc for the main job. A simple benchmark on a string full of ',' shows running times of 158 vs 32, a very large win for f2 (suspicious actually, but if I only test ' ', ',' and '\r', I get the less surprising 50 for f1, which still shows f2 far ahead).

As is, it only works with characters less than 64, but more general versions are possible with a bit more overhead (like applying the same to *s-64 after testing its sign, or looking up the (*s/64)th element in a regular lookup table and bit testing against that, etc).

The running time of 32 is exactly the same I get with a larger lookup table:
char issep[256]={0,0,...};
while(issep[*s])...

In this particular case, vectorization might also be an option, either the loop kind if the string is likely to be long, but we don't even try because we can't compute the number of iterations, or the slp kind by broadcasting *s, comparing to all chars at once and reducing.

This PR is a bit vague and we cannot implement every weird optimization, but I expect this type of comparison might be common enough that it would be worth looking at. If you disagree, feel free to close, I never write code like that myself ;-)


---


### compiler : `gcc`
### title : `The AArch64 backend doesn't define REG_ALLOC_ORDER.`
### open_at : `2014-10-13T08:17:33Z`
### last_modified_date : `2021-05-04T14:39:17Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=63521
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `unknown`
### severity : `normal`
### contents :
Andrew Pinski reported that we have not defined REG_ALLOC_ORDER for the AArch64 backend. It would be useful during spill cost computations for this to be defined appropriately


---


### compiler : `gcc`
### title : `unnecessary reloads generated in loop`
### open_at : `2014-10-13T16:46:53Z`
### last_modified_date : `2021-07-26T22:27:49Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=63525
### status : `RESOLVED`
### tags : `missed-optimization, ra`
### component : `target`
### version : `5.0`
### severity : `normal`
### contents :
Created attachment 33700
testcase 1.cxx

For the testcase 1.cxx attached, trunk (r214579) generates an addpd with mem operand and one extra reload insn in kernel loop. For g++ before r204274, it generate less insns in the kernel loop.

~/workarea/gcc-r214579/build/install/bin/g++ -O2 -S 1.cxx -o 1.s
kernel loop:
.L3:
       pxor    %xmm0, %xmm0
       cvtsi2sd        %eax, %xmm0
       addl    $1, %eax
       cmpl    %edx, %eax
       unpcklpd        %xmm0, %xmm0
       addpd   -24(%rsp), %xmm0             ===> mem operand used
       movaps  %xmm0, -24(%rsp)           ===> reload
       jne     .L3

~/workarea/gcc-r199418/build/install/bin/g++ -O2 -S 1.cxx -o 2.s
kernel loop:
.L3:
       xorpd   %xmm1, %xmm1
       cvtsi2sd        %eax, %xmm1
       addl    $1, %eax
       unpcklpd        %xmm1, %xmm1
       addpd   %xmm1, %xmm0
       cmpl    %edx, %eax
       jne     .L3


The reload insns in trunk are generated because of following steps:

With r204274, the IR after expand like this:
Loop:
...
(insn 15 14 16 5 (set (reg/v:V2DF 83 [ v ])
       (plus:V2DF (reg/v:V2DF 83 [ v ])
           (reg:V2DF 92 [ D.5005 ]))) 1.cxx:14 -1
    (nil))
...
end Loop.
(insn 23 22 24 7 (set (reg/v:TI 90 [ tmp ])
       (subreg:TI (reg/v:V2DF 83 [ v ]) 0)) /usr/local/google/home/wmi/workarea/gcc-r212442/build/install/lib/gcc/x86_64-unknown-linux-gnu/4.10.0/include/emmintrin.h:157 -1
    (nil))
(insn 24 23 25 7 (set (mem/c:DF (symbol_ref:DI ("x") [flags 0x2]  <var_decl 0x7ffff5c6d5a0 x>) [2 x+0 S8 A64])
       (subreg:DF (reg/v:TI 90 [ tmp ]) 0)) 1.cxx:17 -1
    (nil))
(insn 25 24 0 7 (set (mem/c:DF (symbol_ref:DI ("y") [flags 0x2]  <var_decl 0x7ffff5c6d630 y>) [2 y+0 S8 A64])
       (subreg:DF (reg/v:TI 90 [ tmp ]) 8)) 1.cxx:18 -1
    (nil))

forward propagation will propagate reg 90 from insn 23 to insn 24 and insn 25, and remove subreg:TI, so we get the IR before IRA like this:

Loop:
...
(insn 15 14 16 4 (set (reg/v:V2DF 83 [ v ])
       (plus:V2DF (reg/v:V2DF 83 [ v ])
           (reg:V2DF 92 [ D.5005 ]))) 1.cxx:14 1263 {*addv2df3}
    (expr_list:REG_DEAD (reg:V2DF 92 [ D.5005 ])
       (nil)))
...
end Loop.
(insn 24 22 25 5 (set (mem/c:DF (symbol_ref:DI ("x") [flags 0x2]  <var_decl 0x7ffff5c6d5a0 x>) [2 x+0 S8 A64])
       (subreg:DF (reg/v:V2DF 83 [ v ]) 0)) 1.cxx:17 128 {*movdf_internal}
    (nil))
(insn 25 24 0 5 (set (mem/c:DF (symbol_ref:DI ("y") [flags 0x2]  <var_decl 0x7ffff5c6d630 y>) [2 y+0 S8 A64])
       (subreg:DF (reg/v:V2DF 83 [ v ]) 8)) 1.cxx:18 128 {*movdf_internal}
    (expr_list:REG_DEAD (reg/v:V2DF 83 [ v ])
       (nil)))

ix86_cannot_change_mode_class doesn't allow such subreg: "subreg:DF (reg/v:V2DF 83 [ v ]) 8)" in insn 25, so reg 83 will be added in invalid_mode_changes by record_subregs_of_mode and will be allocated NO_REGS regclass.

reg 83 has NO_REGS regclass while plus:V2DF requires the target operand to be xmm register in insn 15, so reload insns are needed. The kernel loop has low register pressure and it doesn't form a separate IRA region, so live range splitting on region boarder doesn't kick in here.

Without r204274, IR after expand is like this:
Loop:
...
(insn 15 14 16 5 (set (reg/v:V2DF 61 [ v ])
       (plus:V2DF (reg/v:V2DF 61 [ v ])
           (reg:V2DF 68 [ D.4966 ]))) 1.cxx:14 -1
    (nil))
...
End Loop.
(insn 25 24 26 7 (set (subreg:V2DF (reg/v:TI 66 [ tmp ]) 0)
       (reg/v:V2DF 61 [ v ])) /usr/local/google/home/wmi/workarea/gcc-r199418/build/install/lib/gcc/x86_64-unknown-linux-gnu/4.9.0/include/emmintrin.h:147 -1
    (nil))
(insn 26 25 27 7 (set (mem/c:DF (symbol_ref:DI ("x") [flags 0x2]  <var_decl 0x7ffff5e80be0 x>) [2 x+0 S8 A64])
       (subreg:DF (reg/v:TI 66 [ tmp ]) 0)) 1.cxx:17 -1
    (nil))
(insn 27 26 0 7 (set (mem/c:DF (symbol_ref:DI ("y") [flags 0x2]  <var_decl 0x7ffff5e80c78 y>) [2 y+0 S8 A64])
       (subreg:DF (reg/v:TI 66 [ tmp ]) 8)) 1.cxx:18 -1
    (nil))

Because the subreg is on the left handside of insn 25, it is impossible for forward propagation to merge insn 25 to insn 26 and insn 27. reg 61 will not have reference like this: "subreg:DF (reg/v:V2DF 61 [ v ]) 8)", so it gets SSE regclass and will not introduce extra reload insns in kernel loop.

r204274 just enables more forward propagations and exposes the problem here.


---


### compiler : `gcc`
### title : `redundent reload in loop after removing regmove`
### open_at : `2014-10-15T22:08:20Z`
### last_modified_date : `2019-04-10T15:08:05Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=63548
### status : `UNCONFIRMED`
### tags : `missed-optimization, ra`
### component : `rtl-optimization`
### version : `5.0`
### severity : `normal`
### contents :
Created attachment 33730
testcase 1.c

For program with many insns like "a = b + c", where operands "b" and "c" are both dead immediately after the add insn, the hardreg preference heuristic seems not perfect.

Here is a testcase 1.c,

For gcc after r204212, they generates two redundent reload insns caused by imperfect hardreg preference heuristic in IRA. 

~/workarea/gcc-r214579/build/install/bin/gcc -O2 -S 1.c

.L5:
        movl    %ebx, %edi
        call    goo
        leal    2(%rbx), %edi
        movl    %eax, %r13d
        call    goo
        leal    4(%rbx), %edi
        movl    %eax, %r12d
        call    goo
        leal    6(%rbx), %edi
        movl    %eax, %ebp
        addl    $1, %ebx
        call    goo
        movl    %eax, %edx         // redundent mov
        movl    %r13d, %eax        // redundent mov
        imull   %r12d, %eax
        imull   %ebp, %eax
        imull   %edx, %eax
        addl    %eax, total(%rip)
        cmpl    %ebx, M(%rip)
        jg      .L5

For old gcc with regmove, it happens to be better than hardreg preference heuristic and generates one redundent reload.

~/workarea/gcc-r199418/build/install/bin/gcc -O2 -S 1.c
.L3:
        movl    %ebx, %edi
        call    goo
        leal    2(%rbx), %edi
        movl    %eax, %r13d
        call    goo
        leal    4(%rbx), %edi
        movl    %eax, %r12d
        call    goo
        leal    6(%rbx), %edi
        movl    %eax, %ebp
        addl    $1, %ebx
        call    goo
        movl    %r13d, %edx        // redundent mov
        imull   %r12d, %edx
        imull   %ebp, %edx
        imull   %eax, %edx
        addl    %edx, total(%rip)
        cmpl    %ebx, M(%rip)
        jg      .L3

llvm generates no redundent move insn.

clang-r217862 -O2 -S 1.c
.LBB0_2:                       
        movl    %ebx, %edi
        callq   goo
        movl    %eax, %r14d
        leal    2(%rbx), %edi
        callq   goo
        movl    %eax, %ebp
        leal    4(%rbx), %edi
        callq   goo
        movl    %eax, %r15d
        leal    6(%rbx), %edi
        callq   goo
        imull   %r14d, %ebp
        imull   %r15d, %ebp
        imull   %eax, %ebp
        addl    %ebp, total(%rip)
        incl    %ebx
        cmpl    M(%rip), %ebx
        jl      .LBB0_2


---


### compiler : `gcc`
### title : `gcc should dedup string postfixes`
### open_at : `2014-10-16T08:53:49Z`
### last_modified_date : `2021-08-16T23:48:41Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=63556
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.9.2`
### severity : `enhancement`
### contents :
With this code:

extern void func(char *a, char *b);

void f(void)
{
        func("abc", "xabc");
        func("abc", "abc");
}

we get:

.LC0:
        .string "xabc"
.LC1:
        .string "abc"

So the "abc"s get deduped. But it could also dedup the postfix by pointing "abc" to "xabc" + 1. This would save some space.


---


### compiler : `gcc`
### title : `Missed optimization (a & ~mask) | (b & mask) = a ^ ((a ^ b) & mask)`
### open_at : `2014-10-16T23:55:17Z`
### last_modified_date : `2023-09-04T18:02:07Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=63568
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `5.0`
### severity : `normal`
### contents :
As of 216350, compiling the following example on SH with -O2

unsigned int test (unsigned int a, unsigned int b, unsigned int m)
{
  return (a & ~m) | (b & m);
}

results in:
        not     r6,r0
        and     r0,r4
        and     r6,r5
        mov     r4,r0
        rts
        or      r5,r0

A shorter way is to do the same is:
        xor     r4,r5
        and     r5,r6
        mov     r6,r0
        rts
        xor     r4,r0

If this kind of stuff is done as part of tree optimization, then this is probably not SH specific, although I haven't checked with other targets.


---


### compiler : `gcc`
### title : `Missed late memory CSE`
### open_at : `2014-11-14T10:29:35Z`
### last_modified_date : `2021-12-12T12:50:03Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=63864
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `5.0`
### severity : `enhancement`
### contents :
Hi,

In my code I replaced some 'manual' vector/matrix calculations with
(inlined) function calls using vector/matrix types. When using clang
both approaches result in nearly identical generated code. But when
using gcc the code becomes much worse.

I don't know too much about compiler internals, but if I had to make a
guess I'd say that for some reason SRA doesn't work in this case.

See the code below: 'test_ok()' is the original function,
'test_slow()' is the rewritten version. I tried to simplify the code
as much as possible while not making it too simple (so that neither
compiler starts vectorizing the code).

Tested with:
  g++ (GCC) 5.0.0 20141114 (experimental)

Wouter

 - - - 8< - - - 8< - - - 8< - - - 8< - - - 8< - - - 8< - - - 8< - - -

// Original code with 'manual' matrix multiplication
float test_ok(float m[3][3], float x, float y, float z, float s, float b) {
	float p = x*s + b;
	float q = y*s + b;
	float r = z*s + b;

	float u = m[0][0]*p + m[1][0]*q + m[2][0]*r;
	float v = m[0][1]*p + m[1][1]*q + m[2][1]*r;
	float w = m[0][2]*p + m[1][2]*q + m[2][2]*r;

	return u + v + w;
}

// (Much simplified) vec3/mat3 types
struct vec3 {
	vec3() {}
	vec3(float x, float y, float z) { e[0] = x; e[1] = y; e[2] = z; }
	float  operator[](int i) const { return e[i]; }
	float& operator[](int i)       { return e[i]; }
private:
	float e[3];
};
struct mat3 { vec3 c[3]; };

inline vec3 operator+(const vec3& x, const vec3& y) {
	vec3 r;
	for (int i = 0; i < 3; ++i) r[i] = x[i] + y[i];
	return r;
}

inline vec3 operator*(const vec3& x, float y) {
	vec3 r;
	for (int i = 0; i < 3; ++i) r[i] = x[i] * y;
	return r;
}

inline vec3 operator*(const vec3& x, const vec3& y) {
	vec3 r;
	for (int i = 0; i < 3; ++i) r[i] = x[i] * y[i];
	return r;
}

inline vec3 operator*(const mat3& m, const vec3& v) {
	return m.c[0] * v[0] + m.c[1] * v[1] + m.c[2] * v[2];
}

// Rewritten version of the original function
float test_slow(mat3& m, float x, float y, float z, float s, float b) {
	vec3 t = m * (vec3(x,y,z) * s + vec3(b,b,b));
	return t[0] + t[1] + t[2];
}


---


### compiler : `gcc`
### title : `Missing vectorization optimization`
### open_at : `2014-11-19T02:34:21Z`
### last_modified_date : `2019-10-16T18:08:39Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=63945
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.1`
### severity : `enhancement`
### contents :
(Reporting this for Bruno Turcksin <bruno.turcksin@gmail.com>.)

The loop in the following testcase cannot be vectorized, we get the error:

note: not vectorized: latch block not empty.
note: bad loop form.

The reason is that val is a member of the class, is evaluated in the if, and is used in the loop that should be vectorized. If these three conditions are satisfied the loop cannot be vectorized.

...............................

#include <vector>

class TEST
{
  public :
    TEST();
    void test();

  private :
    const double val;
};

TEST::TEST()
  :
  val(2.)
{}

void TEST::test()
{
  const unsigned int n(1000);
  std::vector<double> a(n);
  std::vector<double> b(n);
  std::vector<double> c(n);

  for (unsigned int i=0; i<n; ++i)
  {
    a[i] = 1.;
    b[i] = 1.;
  }

  if (val<100.)
  {
#pragma omp simd
    for (unsigned int i=0; i<n; ++i)
      c[i] = val*a[i]+b[i];
  }
}
int main ()
{
  TEST a;
  a.test();
}
...................................


---


### compiler : `gcc`
### title : `Remove pr51879-12.c xfail`
### open_at : `2014-11-19T11:16:38Z`
### last_modified_date : `2021-08-10T17:30:41Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=63955
### status : `NEW`
### tags : `missed-optimization, xfail`
### component : `tree-optimization`
### version : `5.0`
### severity : `normal`
### contents :
The fix for PR 62167 - '[4.8 Regression][tail-merge] dead type-unsafe load replaces type-safe load' adds an xfail for pr51879-12.c.

We want the test to pass again.

pr51879-12.c:
...
/* { dg-do compile } */
/* { dg-options "-O2 -fdump-tree-pre" } */

__attribute__((pure)) int bar (int);
__attribute__((pure)) int bar2 (int);
void baz (int);

int x, z;

void
foo (int y)
{
  int a = 0;
  if (y == 6)
    {
      a += bar (7);
      a += bar2 (6);
    }
  else
    {
      a += bar2 (6);
      a += bar (7);
    }
  baz (a);
}

/* { dg-final { scan-tree-dump-times "bar \\(" 1 "pre" { xfail *-*-* } } } */
/* { dg-final { scan-tree-dump-times "bar2 \\(" 1 "pre" { xfail *-*-* } } } */
/* { dg-final { cleanup-tree-dump "pre" } } */
...


---


### compiler : `gcc`
### title : `tree-ssa-strlen.c doesn't handle constant pointer plus and array refs if constant offset is smaller than known constant string length`
### open_at : `2014-11-20T09:31:16Z`
### last_modified_date : `2022-01-09T00:45:45Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=63989
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `5.0`
### severity : `normal`
### contents :
+++ This bug was initially created as a clone of Bug #61773 +++

char *foo (void)
{
  char *p = __builtin_malloc (64);
  char *q = __builtin_malloc (64);
  __builtin_strcat (q, "abcde");
  __builtin_strcat (p, "ab");
  p[1] = q[3];
  __builtin_strcat (p, q);
  return q;
}

gives

> ../../obj2/gcc/cc1 -quiet -O2 t.c
t.c: In function ‘foo’:
t.c:1:7: internal compiler error: in get_string_length, at tree-ssa-strlen.c:417
 char *foo (void)
       ^
0x876c3d2 get_string_length
        /space/rguenther/tramp3d/trunk/gcc/tree-ssa-strlen.c:417
0x8772b02 get_string_length
        /space/rguenther/tramp3d/trunk/gcc/tree.h:2731
0x8772b02 handle_builtin_strlen
        /space/rguenther/tramp3d/trunk/gcc/tree-ssa-strlen.c:899

(gdb) up
#1  0x0876c3d3 in get_string_length (si=0x3c)
    at /space/rguenther/tramp3d/trunk/gcc/tree-ssa-strlen.c:417
417           gcc_assert (builtin_decl_implicit_p (BUILT_IN_STPCPY));


while trying to write a testcase that shows that handle_char_store should
handle a character copy from a known non-zero value.  Well, while really
trying to incrementally teach handle_char_store to handle arbitrary
stores.


---


### compiler : `gcc`
### title : `(un-)conditional execution state is not preserved by PRE/sink`
### open_at : `2014-11-23T12:59:40Z`
### last_modified_date : `2023-07-27T13:47:03Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=64031
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.3`
### severity : `enhancement`
### contents :
The following code is sucessfully vectorized (using the minps instruction):

const int SIZE = 1<<15;

void test9(float * b)
{
  unsigned i;
  
  float *y =__builtin_assume_aligned(b, 16);
  
  for (i = 0; i < SIZE; i++)
  {
    float f = y[i];
    float f2 = f < f*f ? f : f*f;
    y[i] = f2;
  }
}

But not the following slightly modified version:

void test9(float * b)
{
  unsigned i;
  
  float *y =__builtin_assume_aligned(b, 16);
  
  for (i = 0; i < SIZE; i++)
  {
    float f = y[i];
    float f2 = f < f*f ? f : f*f;
    y[i] = f2*f2;
  }
}

Actually, it seems like vectorization of max/min operations fails as soon as some computation is done with the result of this min/max operation.


---


### compiler : `gcc`
### title : `[11/12/13/14 Regression] r217828 prevents RTL loop unroll`
### open_at : `2014-11-26T08:56:25Z`
### last_modified_date : `2023-07-07T10:13:25Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=64081
### status : `NEW`
### tags : `deferred, missed-optimization, needs-bisection, patch`
### component : `rtl-optimization`
### version : `5.0`
### severity : `normal`
### contents :
Created attachment 34123
reproducer

Noticed that for the attached test no RTL loop unroll started to happen.
It is because of changes in dom - namely, I see in dumps that dom2 complicates loop structure. (probably because of changes in lookup_avail_expr?)
Looks like r217827 doesn't mean this :)

Options that should be used - just "-O2  -funroll-loops"


---


### compiler : `gcc`
### title : `virtual register elimination doing bad for local array`
### open_at : `2014-11-26T11:04:38Z`
### last_modified_date : `2021-08-18T23:34:02Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=64082
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `5.0`
### severity : `minor`
### contents :
this ticket is seperated from 62173, for background please see there.

and given Pinski's simple testcase

void bar(int i)
{
  char A[10];
  g(A);
  f(A[i]);
}

both ARM and AArch64 are generating similar sub-optimal code.

for example, for AArch64, we are generating:

bar:
        stp     x29, x30, [sp, -48]!
        add     x29, sp, 0
        str     x19, [sp, 16]
        mov     w19, w0
        add     x0, x29, 32
        bl      g
        add     x0, x29, 48  <-------
        add     x19, x0, x19, sxtw   |  A
        ldrb    w0, [x19, -16] <----- 
        bl      f
        ldr     x19, [sp, 16]
        ldp     x29, x30, [sp], 48
        ret

code sequence A is generated from

  add     x19, virtual_stack_vars_rtx, x19, sxtw
  ldrb    w0, [x19, -16]

the elimination of virtual_stack_vars_rtx generated the extra "add     x0, x29, 48", while if the elimination pass if smart enough, then it could eliminate above into

  add     x19, x29, x19, sxtw
  ldrb    w0, [x19, 32]

given x19 REG_DEAD after ldrb (if not may need some multi propagation).

current elimination pass in lra-elimination.c only optimize one special case which is (virtual_reg + const_imm), we need to handle above two insns pattern.


---


### compiler : `gcc`
### title : `enable fipa-ra for Thumb1`
### open_at : `2014-12-02T17:17:44Z`
### last_modified_date : `2022-01-10T00:21:10Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=64154
### status : `NEW`
### tags : `FIXME, missed-optimization`
### component : `target`
### version : `5.0`
### severity : `enhancement`
### contents :
For PR 63718, we disabled -fuse-caller-save for Thumb1 in arm.c:
...
  /* In Thumb1 mode, we emit the epilogue in RTL, but the last insn
     - epilogue_insns - does not accurately model the corresponding insns
     emitted in the asm file.  In particular, see the comment in thumb_exit
     'Find out how many of the (return) argument registers we can corrupt'.
     As a consequence, the epilogue may clobber registers without
     fuse-caller-save finding out about it.  Therefore, disable fuse-caller-save
     in Thumb1 mode.
     TODO: Accurately model clobbers for epilogue_insns and reenable
     fuse-caller-save.  */
  if (TARGET_THUMB1)
    flag_use_caller_save = 0;
...

We want to fix the target to properly model the clobbers in the rtl insn epilogue_insns, such that we can re-enable -fuse-caller-save.


---


### compiler : `gcc`
### title : `[4.9/5/6 Regression] one more stack slot used due to one less inlining level`
### open_at : `2014-12-03T09:33:34Z`
### last_modified_date : `2021-12-19T04:24:10Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=64164
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `5.0`
### severity : `normal`
### contents :
Created attachment 34178
testcase

$ cc -O2 -S -o stm.s stm.c
$ cc -O2 -DOPT -S -o stm-opt.s stm.c

if you compare the 2 outputs, stm_load function is using one more slot on the stack.
The difference is only this:

static inline size_t
AO_myload2(const volatile size_t *addr)
{
  return *(size_t *)addr;
}
static inline size_t
AO_myload(const volatile size_t *addr)
{
#ifdef OPT
  size_t result = AO_myload2(addr);
#else
  size_t result = *(size_t *)addr;
#endif
  return result;
}

Having one more inlined function should have the same optimization not a better one.
4.8 does not have the problem and the code generated is the same.


---


### compiler : `gcc`
### title : `-Os misses an opportunity to merge two ret instructions`
### open_at : `2014-12-07T23:36:05Z`
### last_modified_date : `2023-10-08T01:20:20Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=64215
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.8.2`
### severity : `enhancement`
### contents :
The following code:

int find_mismatch(const char *s, const char *t)
{
  int n;
  for (n = 0; s[n] == t[n]; ++n) if (s[n] == 0) return -1;
  return n;
}

optimized for space, by version 4.8.2-19ubuntu1,
produces the following amd64 assembly code:

0000000000000000 <find_mismatch>:
   0:	31 c0                	xor    %eax,%eax
   2:	8a 14 07             	mov    (%rdi,%rax,1),%dl
   5:	3a 14 06             	cmp    (%rsi,%rax,1),%dl
   8:	75 0b                	jne    15 <find_mismatch+0x15>
   a:	48 ff c0             	inc    %rax
   d:	84 d2                	test   %dl,%dl
   f:	75 f1                	jne    2 <find_mismatch+0x2>
  11:	83 c8 ff             	or     $0xffffffff,%eax
  14:	c3                   	retq   
  15:	c3                   	retq   

The last two instructions could be merged, saving a grand total of 1 byte.


$ gcc -v -Os -c parse.c
Using built-in specs.
COLLECT_GCC=gcc
Target: x86_64-linux-gnu
Configured with: ../src/configure -v --with-pkgversion='Ubuntu 4.8.2-19ubuntu1' --with-bugurl=file:///usr/share/doc/gcc-4.8/README.Bugs --enable-languages=c,c++,java,go,d,fortran,objc,obj-c++ --prefix=/usr --program-suffix=-4.8 --enable-shared --enable-linker-build-id --libexecdir=/usr/lib --without-included-gettext --enable-threads=posix --with-gxx-include-dir=/usr/include/c++/4.8 --libdir=/usr/lib --enable-nls --with-sysroot=/ --enable-clocale=gnu --enable-libstdcxx-debug --enable-libstdcxx-time=yes --enable-gnu-unique-object --disable-libmudflap --enable-plugin --with-system-zlib --disable-browser-plugin --enable-java-awt=gtk --enable-gtk-cairo --with-java-home=/usr/lib/jvm/java-1.5.0-gcj-4.8-amd64/jre --enable-java-home --with-jvm-root-dir=/usr/lib/jvm/java-1.5.0-gcj-4.8-amd64 --with-jvm-jar-dir=/usr/lib/jvm-exports/java-1.5.0-gcj-4.8-amd64 --with-arch-directory=amd64 --with-ecj-jar=/usr/share/java/eclipse-ecj.jar --enable-objc-gc --enable-multiarch --disable-werror --with-arch-32=i686 --with-abi=m64 --with-multilib-list=m32,m64,mx32 --with-tune=generic --enable-checking=release --build=x86_64-linux-gnu --host=x86_64-linux-gnu --target=x86_64-linux-gnu
Thread model: posix
gcc version 4.8.2 (Ubuntu 4.8.2-19ubuntu1) 
COLLECT_GCC_OPTIONS='-v' '-Os' '-c' '-mtune=generic' '-march=x86-64'
 /usr/lib/gcc/x86_64-linux-gnu/4.8/cc1 -quiet -v -imultiarch x86_64-linux-gnu parse.c -quiet -dumpbase parse.c -mtune=generic -march=x86-64 -auxbase parse -Os -version -fstack-protector -Wformat -Wformat-security -o /tmp/ccZIGWnY.s
GNU C (Ubuntu 4.8.2-19ubuntu1) version 4.8.2 (x86_64-linux-gnu)
	compiled by GNU C version 4.8.2, GMP version 5.1.3, MPFR version 3.1.2-p3, MPC version 1.0.1
GGC heuristics: --param ggc-min-expand=97 --param ggc-min-heapsize=127216
ignoring nonexistent directory "/usr/local/include/x86_64-linux-gnu"
ignoring nonexistent directory "/usr/lib/gcc/x86_64-linux-gnu/4.8/../../../../x86_64-linux-gnu/include"
#include "..." search starts here:
#include <...> search starts here:
 /usr/lib/gcc/x86_64-linux-gnu/4.8/include
 /usr/local/include
 /usr/lib/gcc/x86_64-linux-gnu/4.8/include-fixed
 /usr/include/x86_64-linux-gnu
 /usr/include
End of search list.
GNU C (Ubuntu 4.8.2-19ubuntu1) version 4.8.2 (x86_64-linux-gnu)
	compiled by GNU C version 4.8.2, GMP version 5.1.3, MPFR version 3.1.2-p3, MPC version 1.0.1
GGC heuristics: --param ggc-min-expand=97 --param ggc-min-heapsize=127216
Compiler executable checksum: dc75e0628c9356affcec059d0c81cc01
COLLECT_GCC_OPTIONS='-v' '-Os' '-c' '-mtune=generic' '-march=x86-64'
 as -v --64 -o parse.o /tmp/ccZIGWnY.s
GNU assembler version 2.24 (x86_64-linux-gnu) using BFD version (GNU Binutils for Ubuntu) 2.24
COMPILER_PATH=/usr/lib/gcc/x86_64-linux-gnu/4.8/:/usr/lib/gcc/x86_64-linux-gnu/4.8/:/usr/lib/gcc/x86_64-linux-gnu/:/usr/lib/gcc/x86_64-linux-gnu/4.8/:/usr/lib/gcc/x86_64-linux-gnu/
LIBRARY_PATH=/usr/lib/gcc/x86_64-linux-gnu/4.8/:/usr/lib/gcc/x86_64-linux-gnu/4.8/../../../x86_64-linux-gnu/:/usr/lib/gcc/x86_64-linux-gnu/4.8/../../../../lib/:/lib/x86_64-linux-gnu/:/lib/../lib/:/usr/lib/x86_64-linux-gnu/:/usr/lib/../lib/:/usr/lib/gcc/x86_64-linux-gnu/4.8/../../../:/lib/:/usr/lib/
COLLECT_GCC_OPTIONS='-v' '-Os' '-c' '-mtune=generic' '-march=x86-64'


---


### compiler : `gcc`
### title : `Can GCC produce local mergeable symbols for *.__FUNCTION__ and *.__PRETTY_FUNCTION__ functions?`
### open_at : `2014-12-11T12:29:05Z`
### last_modified_date : `2022-12-29T02:40:03Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=64266
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `c++`
### version : `5.0`
### severity : `normal`
### contents :
Created attachment 34250
test case

For the following testcase:

extern "C" {
 extern int printf (char *, ...);
 }
 
 class a {
  public:
   void sub (int i)
     {
       printf ("__FUNCTION__ = %s\n", __FUNCTION__);
       printf ("__PRETTY_FUNCTION__ = %s\n", __PRETTY_FUNCTION__);
     }

   void sub()
   {
       printf ("__FUNCTION__ = %s\n", __FUNCTION__);
   }
 };

int
main (void)
{
  a ax;
  ax.sub (0);
  ax.sub ();
  return 0;
}

Unlink clang, GCC produces a local symbol residing in .symtab and string values are not in mergeable section:

$ g++ ~/Programming/testcases/pretty-function.c -o a.o
$ readelf -s a.o --wide |  grep PRE
    15: 0000000000400710    17 OBJECT  LOCAL  DEFAULT   14 _ZZN1a3subEiE19__PRETTY_FUNCTION__

$ readelf -p '.rodata' a.out

String dump of section '.rodata':
  [    10]  __FUNCTION__ = %s

  [    23]  __PRETTY_FUNCTION__ = %s

  [    3d]  sub
  [    50]  void a::sub(int)
  [    61]  sub

and clang produces:

$ clang++ ~/Programming/testcases/pretty-function.c -o a.o
$ readelf -s a.out --wide |  grep PRE
(nothing)

$ readelf -p '.rodata' a.o

String dump of section '.rodata':
  [     4]  __FUNCTION__ = %s

  [    17]  sub
  [    1b]  __PRETTY_FUNCTION__ = %s

  [    35]  void a::sub(int)

I'm wondering if we can also process such kind of optimization.
For Inkscape (compiled with -O2), there are following differences:

section                  portion        size        size    compared  comparison
.rodata                  15.69 %     2.41 MB     2523277     2291412     90.81 %
.strtab                  13.06 %     2.00 MB     2099988     1933845     92.09 %

Where column 'size' is related to GCC and 'compared' is size generated by clang.

Thanks,
Martin


---


### compiler : `gcc`
### title : `Missed optimization: 64-bit divide used when 32-bit divide would work`
### open_at : `2014-12-14T18:39:05Z`
### last_modified_date : `2022-01-28T00:52:29Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=64308
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.2`
### severity : `enhancement`
### contents :
Created attachment 34280
Test case

The following is a fairly typical implementation of exponentiation modulo m:

$ cat ipowm.c
// Computes (b**e) % m
unsigned int
ipowm(unsigned int b, unsigned int e, unsigned int m)
{
  unsigned int ret;
  b %= m;
  for (ret = m > 1; e; e >>= 1) {
    if ((e & 1) == 1) {
      ret = (unsigned long long)ret * b % m;
    }
    b = (unsigned long long)b * b % m;
  }
  return ret;
}

Unfortunately, GCC emits a 64-bit multiply and divide for both "... * b % m" expressions on x86 and x86-64, where a 32-bit multiply and divide would be equivalent and faster.

$ gcc -std=c11 -O3 -Wall -S -save-temps ipowm.c
$ cat ipowm.s
...
	imulq	%rdi, %rax
	divq	%rcx
...
	imulq	%rdi, %rax
	divq	%rcx
...

The pattern

	mull	%edi
	divl	%ecx

would be much faster.  They're equivalent because b is always reduced mod m, so b < m and therefore (for any unsigned int x), x * b / m <= x * m / m == x, thus the quotient will always fit in 32 bits.


---


### compiler : `gcc`
### title : `add alias runtime check to remove load after load redundancy`
### open_at : `2014-12-15T19:19:14Z`
### last_modified_date : `2021-12-15T21:39:22Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=64319
### status : `NEW`
### tags : `alias, missed-optimization`
### component : `tree-optimization`
### version : `unknown`
### severity : `enhancement`
### contents :
Looking at the code generated at -O3 for the following function, we have to load "*a" twice because "a" may alias "b":

$ cat foo.c
int foo(int *a, int *b)
{
  *a = 1;
  (*b)++;
  return *a;
}

Here is the code generated for aarch64 (for illustration only, ie., this is not an aarch64 bug):

$ gcc foo.c -O3 -S -o -
[...]
foo:
 mov w2, 1
 str w2, [x0]
 ldr w2, [x1]
 add w2, w2, 1
 str w2, [x1]
 ldr w0, [x0]
 ret

GCC could insert a runtime check to disambiguate the two pointers: in principle, we should obtain better code on both branches, because the compiler knows something more about the program in each case.

$ cat bar.c
int bar(int *a, int *b)
{
  if (a == b)
    {
      *a = 1;
      (*b)++;
      return *a;
    }

  *a = 1;
  (*b)++;
  return *a;
}

GCC does optimize correctly the case "a==b" and still has an optimization problem in the case "a!=b". Here is the code generated for aarch64:

bar:
 cmp	x0, x1
 beq	.L6
 mov	w2, 1
 str	w2, [x0]
 ldr	w2, [x1]
 add	w2, w2, 1
 str	w2, [x1]
 ldr	w0, [x0]  <-- this load should be replaced by a "mov w0, 1" 
                      because we know "x1 != x0" on this branch.
 ret
.L6:
 mov	w1, 2
 str	w1, [x0]
 mov	w0, w1
 ret


---


### compiler : `gcc`
### title : `More optimize opportunity for constant folding`
### open_at : `2014-12-15T23:01:17Z`
### last_modified_date : `2021-08-19T19:26:26Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=64322
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `5.0`
### severity : `enhancement`
### contents :
The two programs (A.c) and (B.c) only differ by one line
(marked by "// <---HERE"), where (B.c) change 0x100000000L to 0L.

Resulting codes by "x86_64-unknown-linux-gnu-gcc-5.0.0 -Os -S"
are different;
the code (A.s) for (A.c) is less optimized than (B.s) for (B.c).
Note that variable c is not referenced at all in this program.

(A.c)
int main (void)
{
          long a = -1L;
 volatile long b =  0L;
 volatile long c = 0x100000000L;      // <---HERE
 a = (1+b >> 63 << 1) / 0x100000000L;

 if (a == 0L);
 else __builtin_abort();
 
 return 0;
}

(B.c)
int main (void)
{
          long a = -1L;
 volatile long b =  0L;
 volatile long c =  0L;               // <---HERE
 a = (1+b >> 63 << 1) / 0x100000000L;

 if (a == 0L);
 else __builtin_abort();
 
 return 0;
}

+-----------------------------+-----------------------------+
|(A.s)                        |(B.s)                        |
+-----------------------------+-----------------------------+
|main:                        |main:                        |
|.LFB0:                       |.LFB0:                       |
|  .cfi_startproc             |  .cfi_startproc             |
|  subq  $24, %rsp            |  movq  $0, -24(%rsp)        |
|  .cfi_def_cfa_offset 32     |  movq  $0, -16(%rsp)        |
|  movabsq  $4294967296, %rcx |  movq  -24(%rsp), %rax      |
|  movq  $0, (%rsp)           |                             |
|  movq  %rcx, 8(%rsp)        |                             |
|  movq  (%rsp), %rax         |                             |
|  incq  %rax                 |                             |
|  sarq  $63, %rax            |                             |
|  addq  %rax, %rax           |                             |
|  cqto                       |                             |
|  idivq  %rcx                |                             |
|  testq  %rax, %rax          |                             |
|  je  .L2                    |                             |
|  call  abort                |                             |
|.L2:                         |                             |
|  xorl  %eax, %eax           |  xorl  %eax, %eax           |
|  addq  $24, %rsp            |                             |
|  .cfi_def_cfa_offset 8      |                             |
|  ret                        |  ret                        |
|  .cfi_endproc               |  .cfi_endproc               |
|.LHOTE0:                     |.LHOTE0:                     |
+-----------------------------+-----------------------------+

$ x86_64-unknown-linux-gnu-gcc-5.0.0 -v
Using built-in specs.
COLLECT_GCC=x86_64-unknown-linux-gnu-gcc-5.0.0
COLLECT_LTO_WRAPPER=/usr/local/x86_64-tools/gcc-5.0.0/libexec/gcc/x86_64-unknown-linux-gnu/5.0.0/lto-wrapper
Target: x86_64-unknown-linux-gnu
Configured with: /home/hassy/gcc/configure --prefix=/usr/local/x86_64-tools/gcc-5.0.0/
--with-gmp=/usr/local/gmp-5.1.1/ --with-mpfr=/usr/local/mpfr-3.1.2/
--with-mpc=/usr/local/mpc-1.0.1/ --disable-multilib --disable-nls --enable-languages=c
Thread model: posix
gcc version 5.0.0 20141215 (experimental) (GCC)


---


### compiler : `gcc`
### title : `[SH] Improve bswap support`
### open_at : `2014-12-22T15:21:46Z`
### last_modified_date : `2021-08-28T19:43:33Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=64376
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `target`
### version : `5.0`
### severity : `enhancement`
### contents :
There have been some improvements made w.r.t. bswap pattern detection at the tree level.  Some of them expect a bswaphi2 expander, which is absent on SH (see PR 63259).  It seems that adding the bswaphi2 pattern is not enough and we still need support from combine to get better pattern matching.


---


### compiler : `gcc`
### title : `Missed optimization: smarter dead store elimination in dtors`
### open_at : `2014-12-22T23:30:32Z`
### last_modified_date : `2021-12-27T03:55:35Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=64380
### status : `NEW`
### tags : `missed-optimization`
### component : `c++`
### version : `5.0`
### severity : `enhancement`
### contents :
Some of the stores are eliminated in dtors already, if the values are not used later. But if there are function calls after the stores, then they are not eliminated. I see the reason for this, but some functions are special, eg free(), operator delete and others with the same semantics: they won't crawl back and access these variables, so if the vars are not used locally, and no other functions are called, the stores could be eliminated. 

This would be useful eg for classes where there is a user callable function that releases some/all resources, while keeping the instance alive, and the dtor calls the same function to release all resources. In this latter case, stores that are otherwise needed to have a proper state can be omitted since the instance is being destroyed, anyway.

This is a minor issue probably, since the program shouldn't spend most of its time running dtors. However, some function attribute symmetric in spirit to 'malloc' would be nice: eg 'free': this would mean that if called, it won't reach back to the variables of the calling scope, either through its arguments or through global variables, so those stores could be safely eliminated that are otherwise dead.

g++-5.0.0 -v
Using built-in specs.
COLLECT_GCC=g++-5.0.0
COLLECT_LTO_WRAPPER=/usr/local/libexec/gcc/x86_64-unknown-linux-gnu/5.0.0/lto-wrapper
Target: x86_64-unknown-linux-gnu
Configured with: ../configure --enable-languages=c,c++ --disable-multilib --program-suffix=-5.0.0
Thread model: posix
gcc version 5.0.0 20141222 (experimental) (GCC) 

Compliled with
g++-5.0.0 -g -O3 -Wall 20141222-dtor-deadstore.cpp

Dump of assembler code for function test_ra(Foo*):
   0x00000000004005f0 <+0>:     push   %rbp
   0x00000000004005f1 <+1>:     push   %rbx
   0x00000000004005f2 <+2>:     mov    %rdi,%rbp
   0x00000000004005f5 <+5>:     sub    $0x8,%rsp
# two stores before the loop
   0x00000000004005f9 <+9>:     movl   $0x1,0x10(%rdi)
   0x0000000000400600 <+16>:    movl   $0x2,0x14(%rdi)
   0x0000000000400607 <+23>:    mov    0x8(%rdi),%rdi
   0x000000000040060b <+27>:    test   %rdi,%rdi
   0x000000000040060e <+30>:    je     0x400620 <test_ra(Foo*)+48>
   0x0000000000400610 <+32>:    mov    (%rdi),%rbx
   0x0000000000400613 <+35>:    callq  0x4004d0 <_ZdlPv@plt>
   0x0000000000400618 <+40>:    test   %rbx,%rbx
   0x000000000040061b <+43>:    mov    %rbx,%rdi
   0x000000000040061e <+46>:    jne    0x400610 <test_ra(Foo*)+32>
# two stores after the loop, so far so good
   0x0000000000400620 <+48>:    movq   $0x0,0x8(%rbp)
   0x0000000000400628 <+56>:    movl   $0x3,0x18(%rbp)
   0x000000000040062f <+63>:    add    $0x8,%rsp
   0x0000000000400633 <+67>:    pop    %rbx
   0x0000000000400634 <+68>:    pop    %rbp
   0x0000000000400635 <+69>:    retq   

Dump of assembler code for function test_dtor(Foo*):
# two stores before the lop in the dtor. these won't ever be read again
# could be eliminated
   0x0000000000400640 <+0>:     movl   $0x1,0x10(%rdi)
   0x0000000000400647 <+7>:     movl   $0x2,0x14(%rdi)
   0x000000000040064e <+14>:    mov    0x8(%rdi),%rdi
   0x0000000000400652 <+18>:    test   %rdi,%rdi
   0x0000000000400655 <+21>:    je     0x400671 <test_dtor(Foo*)+49>
   0x0000000000400657 <+23>:    push   %rbx
   0x0000000000400658 <+24>:    nopl   0x0(%rax,%rax,1)
   0x0000000000400660 <+32>:    mov    (%rdi),%rbx
   0x0000000000400663 <+35>:    callq  0x4004d0 <_ZdlPv@plt>
   0x0000000000400668 <+40>:    test   %rbx,%rbx
   0x000000000040066b <+43>:    mov    %rbx,%rdi
   0x000000000040066e <+46>:    jne    0x400660 <test_dtor(Foo*)+32>
# no stores here, the ones after 'delete' were eliminated successfully
   0x0000000000400670 <+48>:    pop    %rbx
   0x0000000000400671 <+49>:    repz retq 

Dump of assembler code for function test_dtor2(Foo*):
   0x0000000000400680 <+0>:     push   %rbp
   0x0000000000400681 <+1>:     push   %rbx
   0x0000000000400682 <+2>:     mov    %rdi,%rbp
   0x0000000000400685 <+5>:     sub    $0x8,%rsp
# 4 dead stores in the src, the one to the same addr is eliminated
   0x0000000000400689 <+9>:     movl   $0xc0,(%rdi)
   0x000000000040068f <+15>:    movl   $0x1,0x10(%rdi)
   0x0000000000400696 <+22>:    movl   $0x2,0x14(%rdi)
   0x000000000040069d <+29>:    mov    0x8(%rdi),%rdi
   0x00000000004006a1 <+33>:    test   %rdi,%rdi
   0x00000000004006a4 <+36>:    je     0x4006c0 <test_dtor2(Foo*)+64>
   0x00000000004006a6 <+38>:    nopw   %cs:0x0(%rax,%rax,1)
   0x00000000004006b0 <+48>:    mov    (%rdi),%rbx
   0x00000000004006b3 <+51>:    callq  0x4004d0 <_ZdlPv@plt>
   0x00000000004006b8 <+56>:    test   %rbx,%rbx
   0x00000000004006bb <+59>:    mov    %rbx,%rdi
   0x00000000004006be <+62>:    jne    0x4006b0 <test_dtor2(Foo*)+48>
# stores after 'delete' are eliminated
   0x00000000004006c0 <+64>:    add    $0x8,%rsp
   0x00000000004006c4 <+68>:    mov    %rbp,%rdi
   0x00000000004006c7 <+71>:    pop    %rbx
   0x00000000004006c8 <+72>:    pop    %rbp
   0x00000000004006c9 <+73>:    jmpq   0x4004d0 <_ZdlPv@plt>
End of assembler dump.

----8<----8<----8<---
struct Node
{
        Node*   next;
        char*   cur;
        char    beg[0];
};

struct Base
{
        int     b0;
        int     b1;

        ~Base() { Clear(); }

        void Clear()
        {
                b0 = 0xb0; // OK, these are dead store eliminated (DSE)
                b1 = 0xb1;
        }
};

struct Foo : Base
{
        Node*   nodes;
        int     m1;
        int     m2;
        int     m3;

        ~Foo() { ReleaseAll(false); }

        void ReleaseAll(bool k)
        {
                m1 = 1; // should be DSE'd if called from the dtor, but it's not
                m2 = 2; // ditto
                Node* n = nodes;
                while (n) {
                        Node* t = n->next;
                        if (!t  &&  k) {
                                n->cur = n->beg;
                                break;
                        }
                        delete n;
                        n = t;
                }
                nodes = n; // OK, DSE'd if called from the dtor
                m3 = 3;    // ditto
        }
};

void test_ra(Foo* f)
{
        f->ReleaseAll(false);
}

void test_dtor(Foo* f)
{
        f->~Foo();
}

void test_dtor2(Foo* f)
{
        f->b0 = 0xc0;   // should be DSE'd, but it's not
        f->m1 = 42;     // OK, DSE'd via the ReleaseAll(): m1=1 store
        delete f;
}

int main()
{
}


---


### compiler : `gcc`
### title : `Missed optimization in post-loop register handling`
### open_at : `2014-12-23T20:35:43Z`
### last_modified_date : `2021-09-19T08:46:13Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=64396
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.9.0`
### severity : `enhancement`
### contents :
I noticed a missed opportunity in GCC that Clang and ICC seem to take advantage of. All versions of GCC I tested (up to 4.9.0) seem to have the same trouble. The following source (for x86_64) shows up the problem:

-----
#include <stdint.h>

#define add_carry32(sum, v)  __asm__("addl %1, %0 ;"  \
"adcl $0, %0 ;"  \
: "=r" (sum)  \
: "g" ((uint32_t) v), "0" (sum))

unsigned sorta_checksum(const void* src, int n, unsigned sum)
{
  const uint32_t *s4 = (const uint32_t*) src;
  const uint32_t *es4 = s4 + (n >> 2);

  while( s4 != es4 ) {
    add_carry32(sum, *s4++);
  }

  add_carry32(sum, *(const uint16_t*) s4);
  return sum;
}
-----

$ g++ -O3 path-to-file -c
$ objdump file.o
...
  10:	74 24                	je     36 <_Z14sorta_checksumPKvij+0x36>
  12:	66 0f 1f 44 00 00    	nopw   0x0(%rax,%rax,1)
  18:	03 11                	add    (%rcx),%edx
  1a:	83 d2 00             	adc    $0x0,%edx
  1d:	48 83 c1 04          	add    $0x4,%rcx
  21:	48 39 c8             	cmp    %rcx,%rax
  24:	75 f2                	jne    18 <_Z14sorta_checksumPKvij+0x18>
  26:	48 8d 4f 04          	lea    0x4(%rdi),%rcx
  2a:	48 29 c8             	sub    %rcx,%rax
  2d:	48 c1 e8 02          	shr    $0x2,%rax
  31:	48 8d 4c 87 04       	lea    0x4(%rdi,%rax,4),%rcx
...

(the example is a contrived version of the original code, which comes
from Solarflare's OpenOnload project).

GCC optimizes the loop but then re-calculates the "s4" variable outside of the loop (offsets 26 through 31 in the above code) before the last add_carry32.  ICC and Clang both realise that the 's4' value in the loop is fine to re-use. GCC has an extra four instructions to calculate the same value known to be in a
register upon loop exit.

Compiler explorer links:
GCC 4.9.0: http://goo.gl/fi3p2J
ICC 13.0.1: http://goo.gl/PRTTc6
Clang 3.4.1: http://goo.gl/95JEQc


---


### compiler : `gcc`
### title : `gcc 25% slower than clang 3.5 for adding complex numbers`
### open_at : `2014-12-26T05:17:48Z`
### last_modified_date : `2023-07-06T02:14:21Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=64410
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.2`
### severity : `normal`
### contents :
Created attachment 34336
cxaddspeed.cpp

gcc 4.9.2 has worse performance than clang 3.5 when dealing with complex numbers.

Attached is a simple program which adds two vectors with complex numbers.  Compiled with -O3 on x86-64 (i7), Fedora 21, gcc 4.9.2 and clang 3.5.0.

$ time ./cxaddspeed_gcc 5000 1000000
5.364u 0.002s 0:05.36 100.0%

$ time ./cxaddspeed_clang 5000 1000000
4.417u 0.001s 0:04.41 100.0%

ie. gcc is about 25% slower.


inner loop produced by gcc:
.L52:
	movsd	(%r15,%rax), %xmm1
	movsd	8(%r15,%rax), %xmm0
	addsd	0(%rbp,%rax), %xmm1
	addsd	8(%rbp,%rax), %xmm0
	movsd	%xmm1, (%rbx,%rax)
	movsd	%xmm0, 8(%rbx,%rax)
	addq	$16, %rax
	cmpq	%rsi, %rax
	jne	.L52

inner loop produced by clang:
.LBB0_145:
	movupd	-16(%rbx), %xmm0
	movupd	-16(%rax), %xmm1
	addpd	%xmm0, %xmm1
	movupd	%xmm1, -16(%rdi)
	movupd	(%rbx), %xmm0
	movupd	(%rax), %xmm1
	addpd	%xmm0, %xmm1
	movupd	%xmm1, (%rdi)
	addq	$2, %rbp
	addq	$32, %rbx
	addq	$32, %rax
	addq	$32, %rdi
	addl	$-2, %ecx
	jne	.LBB0_145


---


### compiler : `gcc`
### title : `[5 Regression] New middle-end pattern breaks vector BIF folding on AArch64.`
### open_at : `2014-12-30T18:12:48Z`
### last_modified_date : `2023-09-04T18:02:11Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=64448
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `5.0`
### severity : `normal`
### contents :
This new pattern

Author: mpolacek <mpolacek@138bc75d-0d04-0410-961f-82ee72b054a4>
Date: Wed Dec 17 11:48:33 2014 +0000

PR middle-end/63568

    match.pd: Add (x & ~m) | (y & m) -> ((x ^ y) & m) ^ x pattern.

    gcc.dg/pr63568.c: New test.

breaks BSL folding to a BIF on AArch64.

Causes this regression:

FAIL: gcc.target/aarch64/vbslq_u64_1.c scan-assembler-times bif\\tv 1


The code now generated is:

vbslq_dummy_u32:
	eor	v0.16b, v1.16b, v0.16b
	and	v0.16b, v0.16b, v2.16b
	eor	v0.16b, v1.16b, v0.16b
	ret
	.size	vbslq_dummy_u32, .-vbslq_dummy_

instead of:

vbslq_dummy_u32:
	bif	v0.16b, v1.16b, v2.16b
	ret
	.size	vbslq_dummy_u32, .-vbslq_dummy_u32

Optimized tree when folding happens:

vbslq_dummy_u32 (uint32x4_t a, uint32x4_t b, uint32x4_t mask)
{
  __Uint32x4_t _3;
  __Uint32x4_t _4;
  __Uint32x4_t _6;
  uint32x4_t _7;

  <bb 2>:
  _3 = mask_1(D) & a_2(D);
  _4 = ~mask_1(D);
  _6 = _4 & b_5(D);
  _7 = _3 | _6;
  return _7;

}

Optimized tree where folding does not happen:

vbslq_dummy_u32 (uint32x4_t a, uint32x4_t b, uint32x4_t mask)
{
  __Uint32x4_t _3;
  __Uint32x4_t _5;
  uint32x4_t _6;

  <bb 2>:
  _3 = b_1(D) ^ a_2(D);
  _5 = _3 & mask_4(D);
  _6 = b_1(D) ^ _5;
  return _6;

}

This will probably need another idiom to be caught by the BSL -> BIF folder.


---


### compiler : `gcc`
### title : `Optimize   0>=p-q   to   q>=p   for char*p,*q;`
### open_at : `2014-12-30T20:58:10Z`
### last_modified_date : `2023-10-23T15:20:29Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=64450
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `5.0`
### severity : `enhancement`
### contents :
Created attachment 34365
Testcase

It was noticed that Boost's iterator_facade incurred a performance penalty (while it should ideally be zero-overhead), which results from the fact that GCC does not optimize   0>=p-q  to  q>=p  for char*p,*q;. See attachment.

This probably applies to > and < and <= as well.


---


### compiler : `gcc`
### title : `optimize (x%5)%5`
### open_at : `2014-12-31T12:24:56Z`
### last_modified_date : `2023-09-12T17:26:18Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=64454
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `5.0`
### severity : `normal`
### contents :
unsigned f(unsigned x){
  return (x%5)%5;
}

gives:

  _2 = x_1(D) % 5;
  _3 = _2 % 5;
  return _3;

It seems we could easily do better in 2 ways:

1) (x%y)%y could be simplified to x%y in match.pd. This would work even when y is not a constant.

2) with VRP, depending on the interval for x, we may be able to simplify x%CST to just x (or sometimes x+CST).


---


### compiler : `gcc`
### title : `Optimization for reusing values in loops`
### open_at : `2015-01-01T15:10:46Z`
### last_modified_date : `2021-12-26T23:10:51Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=64464
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `5.0`
### severity : `enhancement`
### contents :
This is against gcc version 5.0.0 20141222 (experimental) (GCC), on x86_64-unknown-linux-gnu.

Consider the following two program snippets:

ig25@linux-fd1f:~/Krempel/Mandelbrot/Bug> cat m1.f90
module foo
  implicit none
  integer, parameter :: prec = selected_real_kind(15)
  integer, parameter :: n_iter = 10000

contains
  integer function iter_p(cx, cy)
    real(kind=prec), value :: cx, cy
    real(kind=prec) :: x, y, xn, yn
    integer :: k
    x = cx
    y = cy
    do k=1, n_iter
       xn = x*x - y*y + cx
       yn = 2*x*y + cy
       if (xn*xn + yn*yn > 4._prec) exit
       x = xn
       y = yn
    end do
    iter_p = k
  end function iter_p
end module foo
ig25@linux-fd1f:~/Krempel/Mandelbrot/Bug> cat m2.f90
module foo
  implicit none
  integer, parameter :: prec = selected_real_kind(15)
  integer, parameter :: n_iter = 10000

contains
  integer function iter_p(cx, cy)
    real(kind=prec), value :: cx, cy
    real(kind=prec) :: x, y, xn, yn, x2, y2
    integer :: k
    x = cx
    y = cy
    x2 = x*x
    y2 = y*y
    do k=1, n_iter
       xn = x2 - y2 + cx
       yn = 2*x*y + cy
       x2 = xn * xn
       y2 = yn * yn
       if (x2 + y2> 4._prec) exit
       x = xn
       y = yn
    end do
    iter_p = k
  end function iter_p
end module foo

With -O3, the tight loop for m1.f90 is translated into

.L6:
        addl    $1, %eax
        movapd  %xmm2, %xmm3
        cmpl    $10001, %eax
        je      .L2
.L3:
        movapd  %xmm3, %xmm2
        mulsd   %xmm3, %xmm2
        addsd   %xmm3, %xmm3
        mulsd   %xmm4, %xmm3
        subsd   %xmm5, %xmm2
        movapd  %xmm3, %xmm4
        addsd   %xmm0, %xmm2
        addsd   %xmm1, %xmm4
        movapd  %xmm2, %xmm3
        movapd  %xmm4, %xmm5
        mulsd   %xmm2, %xmm3
        mulsd   %xmm4, %xmm5
        addsd   %xmm5, %xmm3
        ucomisd %xmm6, %xmm3
        jbe     .L6

and for m2.f90 into

.L6:
        addl    $1, %eax
        movapd  %xmm5, %xmm4
        cmpl    $10001, %eax
        je      .L2
.L3:
        subsd   %xmm6, %xmm3
        addsd   %xmm4, %xmm4
        movapd  %xmm3, %xmm5
        mulsd   %xmm4, %xmm2
        addsd   %xmm0, %xmm5
        addsd   %xmm1, %xmm2
        movapd  %xmm5, %xmm3
        mulsd   %xmm5, %xmm3
        movapd  %xmm2, %xmm6
        mulsd   %xmm2, %xmm6
        movapd  %xmm3, %xmm4
        addsd   %xmm6, %xmm4
        ucomisd %xmm7, %xmm4
        jbe     .L6

For m1.f90, this is 5 moves, 5 adds, 1 sub and 4 muls.

For m2.f80, this is 5 moves, 5 adds, 1 sub and 3 muls.

I would expect the same number of operations for m2.f90 as for m1.f90.

Same result for 4.8, so this is (very probably) not a regression.


---


### compiler : `gcc`
### title : `Unreachable catch BB for try blocks that cannot create an exception of specific type`
### open_at : `2015-01-05T16:18:22Z`
### last_modified_date : `2019-08-09T13:32:00Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=64501
### status : `NEW`
### tags : `EH, missed-optimization`
### component : `middle-end`
### version : `5.0`
### severity : `enhancement`
### contents :
Hello.

I've been wondering if following catch branch in main can be optimized out as unreachable:

void linker_error (void);

void t()
{
  try
    {
      throw (char)(1);
    }
  catch (char t) {}
}

int
main()
{
  try
    {
      t();
    }
  catch (void *v)
    {
      linker_error ();
    }
}

As there's no possible emission of an exception of void*, can by call of linker_error removed?

Thanks,
Martin


---


### compiler : `gcc`
### title : `Duplicate instructions in both paths in conditional code`
### open_at : `2015-01-07T17:44:11Z`
### last_modified_date : `2021-08-27T07:45:44Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=64525
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `5.0`
### severity : `normal`
### contents :
Created attachment 34395
testcase

gcc is generating the same instructions down both paths of conditional execution. For exmaple, in the attached test case.

...
        cmp     r0, #0
        movt    r2, #:upper16:tree_code_length_0
        ldr     r0, [r2]
        movweq  r2, #:lower16:permanent_obstack
        movteq  r2, #:upper16:permanent_obstack
        movwne  r2, #:lower16:permanent_obstack
        moveq   r3, r2
        movtne  r2, #:upper16:permanent_obstack
...


---


### compiler : `gcc`
### title : `Aarch64 redundant sxth instruction gets generated`
### open_at : `2015-01-08T10:51:27Z`
### last_modified_date : `2022-02-04T18:14:05Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=64537
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `5.0`
### severity : `enhancement`
### contents :
For the below test case redundant sxth instruction gets generate.

int
adds_shift_ext ( long long a, short b, int c)
{
 long long  d = (a - ((long long)b << 3));

  if (d == 0)
    return a + c;
  else
    return b + d + c;
}


adds_shift_ext:
        sxth    w1, w1  // 3    *extendhisi2_aarch64/1  [length = 4] <==1
        subs    x3, x0, x1, sxth 3      // 11   *subs_extvdi_multp2     [length = 4] <==2
        beq     .L5     // 12   *condjump       [length = 4]
        add     w0, w1, w2      // 19   *addsi3_aarch64/2       [length = 4]
        add     w0, w0, w3      // 20   *addsi3_aarch64/2       [length = 4]
        ret     // 57   simple_return   [length = 4]
        .p2align 2
.L5:
        add     w0, w2, w0      // 14   *addsi3_aarch64/2       [length = 4]
        ret     // 55   simple_return   [length = 4]

<== 1 is not needed.


---


### compiler : `gcc`
### title : `FRE pass optimization failure`
### open_at : `2015-01-08T16:06:02Z`
### last_modified_date : `2021-12-15T21:43:39Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=64541
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `5.0`
### severity : `enhancement`
### contents :
Created attachment 34403
1.c 2.c 1.c.028t.esra 2.c.028t.esra 1.c.030t.fre1 2.c.030t.fre1 1.s 2.s compile_gcc.sh

Files 1.c and 2.c in attach are equivalent from C/C++ standpoint:

$ diff 1.c 2.c
3c3,5
<       return *(*q = ++*p);
---
>       ++*p;
>       *q = *p;
>       return **p;

Compiled with gcc-5.0.0, disassembled with objdump (GNU Binutils) 2.24
(see full script compile_gcc.sh in attach).

For 1.c gcc generates better code than for 2.c
(compare 1.s vs 2.s in attach).

I looked at GIMPLE optimization dumps (-fdump-tree-all) and found that
up to *.029t.ealias pass dumps differ insignificantly (attached 
*.028t.esra dumps as they are shorter), but .030t.fre1 pass fails to
reduce intermediate variable '_9' in the second case (attached *.030t.fre
dumps).

Looks like a bug in full redundancy elimination.


---


### compiler : `gcc`
### title : `missed optimization: redundant test before clearing bit(s)`
### open_at : `2015-01-12T13:15:14Z`
### last_modified_date : `2021-08-15T22:58:23Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=64567
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `unknown`
### severity : `enhancement`
### contents :
(Not sure the "Component" is correct). gcc fails to optimize

  if (foo & FLAG)
    foo &= ~FLAG;

into simply unconditionally doing foo &= ~FLAG. Currently, the above code sequence generates four instructions (mov, and, test, cmov) whereas a single and would be sufficient. Note that this is a valid transformation regardless of how many bits are set in FLAG; it doesn't even have to be a compile-time constant (but must of course be side-effect free).

gcc also doesn't optimize the dual

  if (!(foo & FLAG))
    foo |= FLAG;

into foo |= FLAG;. That transformation is however only valid when FLAG is known to consist of only a single bit (so would probably require either a compile-time constant where this can be checked or an expression of the form "1 << something").

Trivial test case below. I'd expect foo and foo2 to compile to the same code, and similarly for baz and baz2.

$ cat test.c
#define F1 0x04
#define F2 0x08
int bar(unsigned flags);
int foo(unsigned flags)
{
        if (flags & (F1 | F2))
                flags &= ~(F1 | F2);
        return bar(flags);
}

int foo2(unsigned flags)
{
        flags &= ~(F1 | F2);
        return bar(flags);
}

int baz(unsigned flags)
{
        if (!(flags & F1))
                flags |= F1;
        return bar(flags);
}

int baz2(unsigned flags)
{
        flags |= F1;
        return bar(flags);
}

$ ./gcc-5.0 -Wall -Wextra -O3 -c test.c
$ objdump -d test.o

test.o:     file format elf64-x86-64


Disassembly of section .text:

0000000000000000 <foo>:
   0:   89 f8                   mov    %edi,%eax
   2:   83 e0 f3                and    $0xfffffff3,%eax
   5:   40 f6 c7 0c             test   $0xc,%dil
   9:   0f 45 f8                cmovne %eax,%edi
   c:   e9 00 00 00 00          jmpq   11 <foo+0x11>
  11:   66 66 66 66 66 66 2e    data32 data32 data32 data32 data32 nopw %cs:0x0(%rax,%rax,1)
  18:   0f 1f 84 00 00 00 00 
  1f:   00 

0000000000000020 <foo2>:
  20:   83 e7 f3                and    $0xfffffff3,%edi
  23:   e9 00 00 00 00          jmpq   28 <foo2+0x8>
  28:   0f 1f 84 00 00 00 00    nopl   0x0(%rax,%rax,1)
  2f:   00 

0000000000000030 <baz>:
  30:   89 f8                   mov    %edi,%eax
  32:   83 c8 04                or     $0x4,%eax
  35:   40 f6 c7 04             test   $0x4,%dil
  39:   0f 44 f8                cmove  %eax,%edi
  3c:   e9 00 00 00 00          jmpq   41 <baz+0x11>
  41:   66 66 66 66 66 66 2e    data32 data32 data32 data32 data32 nopw %cs:0x0(%rax,%rax,1)
  48:   0f 1f 84 00 00 00 00 
  4f:   00 

0000000000000050 <baz2>:
  50:   83 cf 04                or     $0x4,%edi
  53:   e9 00 00 00 00          jmpq   58 <baz2+0x8>


---


### compiler : `gcc`
### title : `Redundant ldr when accessing var inside and outside a loop`
### open_at : `2015-01-15T18:16:21Z`
### last_modified_date : `2018-11-19T13:28:40Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=64616
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `5.0`
### severity : `normal`
### contents :
When compiling the below example with -O2, 2 ldr are generated to access the variable "some": one for the loop and one for the store.

int g (int);

unsigned int glob;

void
f (void)
{
  while (g (glob));
  glob = 1;
}
{code}

The following code is then generated:

f:
push    {r3, r4, r5, lr}
ldr     r5, .L6
.L2:
ldr     r0, [r5]
ldr     r4, .L6
bl      g
cmp     r0, #0
bne     .L2
movs    r3, #1
str     r3, [r4]
pop     {r3, r4, r5, pc}

Note the redundant load of the address at offset 2c in instructions at offsets 4 and 14.


---


### compiler : `gcc`
### title : `convoluted loop codegen for __strcspn_c1`
### open_at : `2015-01-16T01:57:02Z`
### last_modified_date : `2022-12-12T20:22:24Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=64622
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `5.0`
### severity : `enhancement`
### contents :
Compiling
extern __inline long                                                          
__strcspn_c1 (__const char *__s, int __reject)                                  
{                                                                               
  register long __result = 0;                                                 
  while (__s[__result] != '\0' && __s[__result] != __reject)                    
    ++__result;                                                                 
  return __result;                                                              
}                                                                               

With -O2 gives:
__strcspn_c1:
.LFB0:
        .cfi_startproc
        movsbl  (%rdi), %eax
        testb   %al, %al
        je      .L4
        cmpl    %eax, %esi
        movl    $0, %eax
        jne     .L3
        jmp     .L2
        .p2align 4,,10
        .p2align 3
.L12:
        cmpl    %esi, %edx
        je      .L11
.L3:
        addq    $1, %rax
        movsbl  (%rdi,%rax), %edx
        testb   %dl, %dl
        jne     .L12
.L2:
        rep ret
        .p2align 4,,10
        .p2align 3
.L11:
        rep ret
.L4:
        xorl    %eax, %eax
        ret


Whilie clang produces:
__strcspn_c1:                           # @__strcspn_c1
        .cfi_startproc
# BB#0:
        movq    $-1, %rax
        .align  16, 0x90
.LBB0_1:                                # =>This Inner Loop Header: Depth=1
        movsbl  1(%rdi,%rax), %ecx
        incq    %rax
        testl   %ecx, %ecx
        je      .LBB0_3
# BB#2:                                 #   in Loop: Header=BB0_1 Depth=1
        cmpl    %esi, %ecx
        jne     .LBB0_1
.LBB0_3:                                # %.critedge
        retq


---


### compiler : `gcc`
### title : `Suboptimal register allocation for bytes comparison on i386`
### open_at : `2015-01-20T15:25:59Z`
### last_modified_date : `2021-12-25T12:43:51Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=64691
### status : `NEW`
### tags : `missed-optimization, ra`
### component : `target`
### version : `5.0`
### severity : `enhancement`
### contents :
This problem was actually found in 256.bzip2 benchmark codes compiled by GCC 5.0 on -O2.  There is a small loop with bytes comparison which appeared to be ineffective because compared values were not allocated on registers allowing byte access.  That caused additional copies and as a result significant loop slow down.

Situation may be simulated on a small test if we restrict registers usage.

>cat test.c
void test (unsigned char *p, unsigned char val)
{
  unsigned char tmp1, tmp2;
  int i;

  i = 0;
  tmp1 = p[0];
  while (val != tmp1)
    {
      i++;
      tmp2 = tmp1;
      tmp1  = p[i];
      p[i] = tmp2;
    }
  p[0]= tmp1;
}
>gcc -O2 -m32 -ffixed-ebx test.c -S

Here is a loop:

.L3:
        movzbl  (%eax), %ebp
        movl    %esi, %ecx
        movb    %dl, (%eax)
        addl    $1, %eax
        movl    %ebp, %edx
        cmpb    %dl, %cl
        jne     .L3

We have an extra register copy esi->ecx to perform comparison.

Suppose the easiest way to get better register allocation here would be to transform QI comparison into SI one to relax register constraints.


---


### compiler : `gcc`
### title : `Sink common code through PHI`
### open_at : `2015-01-20T22:01:02Z`
### last_modified_date : `2023-06-02T06:04:41Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=64700
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `5.0`
### severity : `enhancement`
### contents :
Created attachment 34507
Testcode

Originally from BZ 64081....


We do miss some interesting kind of optimization opportunities like
transforming

  if (prephitmp_87 == 1)
    goto <bb 9>;
  else
    goto <bb 10>;

  <bb 9>:
  _24 = arr1.5_23 + _62;
  pos.6_25 = *_24;
  goto <bb 11>;

  <bb 10>:
  _28 = arr2.7_27 + _62;
  pos.8_29 = *_28;

  <bb 11>:
  # prephitmp_89 = PHI <pos.6_25(9), pos.8_29(10)>

to

  if (prephitmp_87 == 1)
    goto <bb 9>;
  else
    goto <bb 11>;

  <bb 9>:
  goto <bb 11>;

  <bb 11>:
  # _24 = PHI <arr1.5_23, arr2.7_27>
  _28 = _24 + _62;
  prephitmp_89 = *_28;

sinking common computations through a PHI.

With the followup optimization in out-of-SSA to coalesce arr1.5_23 and
arr2.7_27 which means we can drop the conditional entirely.


---


### compiler : `gcc`
### title : `Missed ccmp optimization`
### open_at : `2015-01-21T16:00:11Z`
### last_modified_date : `2021-08-16T07:44:36Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=64713
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `unknown`
### severity : `enhancement`
### contents :
In a small percentage of ccmp uses within the stage3 cc1plus I see

  56b638:       f100045f        cmp     x2, #0x1
  56b63c:       fa421320        ccmp    x25, x2, #0x0, ne
  56b640:       1a9f17e3        cset    w3, eq
  56b644:       350001c3        cbnz    w3, ...

This is a reminder to dig those out as test cases and see if we can
eliminate the cset.


---


### compiler : `gcc`
### title : `Missed vectorization in a hot code of SPEC2000 ammp`
### open_at : `2015-01-21T16:58:08Z`
### last_modified_date : `2021-07-21T03:28:34Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=64716
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `5.0`
### severity : `enhancement`
### contents :
Created attachment 34521
Preprocessed rectmm.c from SPEC2000 amp

GCC does not vectorize one of the hotest code in SPECFP2000 ammp
(function mm_fv_update_nonbon in file rectmm.c) on x86-64 when -Ofast
-march=core-avx2 -ffast-math -fno-schedule-insns2 is used.  The
preprocessed rectmm.i is in the attachment.

The source code in the consideration is

 r0 = 1./(*vector)[j+3];
 r = r0*r0;
 r = r*r*r;
 xt = a1->q*a2->q*dielectric*r0;
 yt = a1->a*a2->a*r;
 zt = a1->b*a2->b*r*r;
 k = xt - yt + zt;
 xt = xt*r0; yt = yt*r0; zt = zt*r0;
 k1 = xt - yt*6. + zt*12.;
 xt = xt*r0; yt = yt*r0; zt = zt*r0;
 k2 = xt*3.; ka2 = - yt*6.*8.; kb2 = zt*12.*14;




 k1 = -k1;
 xt = (*vector)[j]*r0 ;
 yt = (*vector)[j+1]*r0 ;
 zt = (*vector)[j+2] *r0;





 a1->VP += k;
 a2->dpx -= k1*xt;
 a1->dpx += k1*xt;
 a2->dpy -= k1*yt;
 a1->dpy += k1*yt;
 a2->dpz -= k1*zt;
 a1->dpz += k1*zt;
 xt2 = xt*xt; yt2 = yt*yt; zt2 = zt*zt;
 a2->qxx -= k2*(xt2 - 1./3) + ka2*(xt2 - 1./8)+kb2*(xt2-1./14) ;
 a1->qxx -= k2*(xt2 - 1./3) + ka2*(xt2 - 1./8)+kb2*(xt2-1./14) ;
 a2->qxy -= (k2+ka2+kb2)*yt*xt;
 a1->qxy -= (k2+ka2+kb2)*yt*xt;
 a2->qxz -= (k2+ka2+kb2)*zt*xt;
 a1->qxz -= (k2+ka2+kb2)*zt*xt;
 a2->qyy -= k2*(yt2 - 1./3) + ka2*(yt2 - 1./8)+kb2*(yt2-1./14) ;
 a1->qyy -= k2*(yt2 - 1./3) + ka2*(yt2 - 1./8)+kb2*(yt2-1./14) ;
 a2->qyz -= (k2+ka2+kb2)*yt*zt;
 a1->qyz -= (k2+ka2+kb2)*yt*zt;
 a2->qzz -= k2*(zt2 - 1./3) + ka2*(zt2 - 1./8)+kb2*(zt2-1./14) ;
 a1->qzz -= k2*(zt2 - 1./3) + ka2*(zt2 - 1./8)+kb2*(zt2-1./14) ;

GCC on the trunk generates 118 insns

.L85:
        .cfi_restore_state
        vmovsd  .LC12(%rip), %xmm7
        vdivsd  %xmm0, %xmm7, %xmm6
        vmulsd  %xmm6, %xmm6, %xmm0
        vmulsd  %xmm0, %xmm0, %xmm10
        vmulsd  %xmm10, %xmm0, %xmm0
        vmovsd  56(%rbx), %xmm12
        vmulsd  56(%rdi), %xmm12, %xmm12
        vmulsd  %xmm4, %xmm12, %xmm12
        vmulsd  %xmm12, %xmm6, %xmm12
        vmovsd  64(%rbx), %xmm10
        vmulsd  64(%rdi), %xmm10, %xmm10
        vmulsd  %xmm10, %xmm0, %xmm11
        vmovsd  72(%rbx), %xmm10
        vmulsd  72(%rdi), %xmm10, %xmm10
        vmulsd  %xmm10, %xmm0, %xmm10
        vmulsd  %xmm0, %xmm10, %xmm10
        vmulsd  %xmm12, %xmm6, %xmm0
        vmulsd  %xmm11, %xmm6, %xmm1
        vmulsd  %xmm10, %xmm6, %xmm2
        vmulsd  .LC22(%rip), %xmm2, %xmm8
        vfnmadd231sd    %xmm9, %xmm1, %xmm8
        vaddsd  %xmm8, %xmm0, %xmm8
        vmulsd  .LC21(%rip), %xmm6, %xmm5
        vmulsd  %xmm0, %xmm5, %xmm5
        vmulsd  %xmm1, %xmm6, %xmm0
        vxorpd  %xmm15, %xmm0, %xmm0
        vmulsd  .LC24(%rip), %xmm0, %xmm3
        vmulsd  .LC25(%rip), %xmm6, %xmm7
        vmulsd  %xmm2, %xmm7, %xmm7
        vxorpd  %xmm15, %xmm8, %xmm8
        movslq  %esi, %rax
        vmulsd  (%r12,%rax,8), %xmm6, %xmm2
        leal    1(%rsi), %eax
        cltq
        vmulsd  (%r12,%rax,8), %xmm6, %xmm1
        leal    2(%rsi), %eax
        cltq
        vmulsd  (%r12,%rax,8), %xmm6, %xmm0
        vaddsd  208(%rbx), %xmm12, %xmm12
        vaddsd  %xmm12, %xmm10, %xmm10
        vsubsd  %xmm11, %xmm10, %xmm10
        vmovsd  %xmm10, 208(%rbx)
        vmovapd %xmm8, %xmm6
        vfnmadd213sd    240(%rdi), %xmm2, %xmm6
        vmovsd  %xmm6, 240(%rdi)
        vmovapd %xmm8, %xmm6
        vfmadd213sd     240(%rbx), %xmm2, %xmm6
        vmovsd  %xmm6, 240(%rbx)
        vmovapd %xmm8, %xmm6
        vfnmadd213sd    248(%rdi), %xmm1, %xmm6
        vmovsd  %xmm6, 248(%rdi)
        vmovapd %xmm8, %xmm6
        vfmadd213sd     248(%rbx), %xmm1, %xmm6
        vmovsd  %xmm6, 248(%rbx)
        vmovapd %xmm8, %xmm6
        vfnmadd213sd    256(%rdi), %xmm0, %xmm6
        vmovsd  %xmm6, 256(%rdi)
        vfmadd213sd     256(%rbx), %xmm0, %xmm8
        vmovsd  %xmm8, 256(%rbx)
        vmovsd  .LC26(%rip), %xmm8
        vmovapd %xmm2, %xmm11
        vfnmadd132sd    %xmm2, %xmm8, %xmm11
        vmulsd  %xmm11, %xmm5, %xmm11
        vmovsd  .LC27(%rip), %xmm6
        vmovapd %xmm2, %xmm10
        vfnmadd132sd    %xmm2, %xmm6, %xmm10
        vmovapd %xmm10, %xmm12
        vfmadd132sd     %xmm7, %xmm11, %xmm12
        vmovsd  .LC28(%rip), %xmm10
        vmovapd %xmm2, %xmm11
        vfnmadd132sd    %xmm2, %xmm10, %xmm11
        vfmadd132sd     %xmm3, %xmm12, %xmm11
        vaddsd  264(%rdi), %xmm11, %xmm12
        vmovsd  %xmm12, 264(%rdi)
        vaddsd  264(%rbx), %xmm11, %xmm11
        vmovsd  %xmm11, 264(%rbx)
        vaddsd  %xmm7, %xmm5, %xmm12
        vaddsd  %xmm12, %xmm3, %xmm12
        vmulsd  %xmm12, %xmm1, %xmm11
        vmovapd %xmm2, %xmm13
        vfnmadd213sd    272(%rdi), %xmm11, %xmm13
        vmovsd  %xmm13, 272(%rdi)
        vmovapd %xmm2, %xmm13
        vfnmadd213sd    272(%rbx), %xmm11, %xmm13
        vmovsd  %xmm13, 272(%rbx)
        vmulsd  %xmm0, %xmm2, %xmm2
        vmovapd %xmm12, %xmm13
        vfnmadd213sd    280(%rdi), %xmm2, %xmm13
        vmovsd  %xmm13, 280(%rdi)
        vfnmadd213sd    280(%rbx), %xmm12, %xmm2
        vmovsd  %xmm2, 280(%rbx)
        vmovapd %xmm1, %xmm2
        vfnmadd132sd    %xmm1, %xmm8, %xmm2
        vmulsd  %xmm2, %xmm5, %xmm12
        vmovapd %xmm1, %xmm2
        vfnmadd132sd    %xmm1, %xmm6, %xmm2
        vfmadd132sd     %xmm7, %xmm12, %xmm2
        vfnmadd132sd    %xmm1, %xmm10, %xmm1
        vfmadd132sd     %xmm3, %xmm2, %xmm1
        vaddsd  288(%rdi), %xmm1, %xmm2
        vmovsd  %xmm2, 288(%rdi)
        vaddsd  288(%rbx), %xmm1, %xmm1
        vmovsd  %xmm1, 288(%rbx)
        vmovapd %xmm0, %xmm1
        vfnmadd213sd    296(%rdi), %xmm11, %xmm1
        vmovsd  %xmm1, 296(%rdi)
        vfnmadd213sd    296(%rbx), %xmm0, %xmm11
        vmovsd  %xmm11, 296(%rbx)
        vfnmadd231sd    %xmm0, %xmm0, %xmm8
        vmulsd  %xmm8, %xmm5, %xmm5
        vfnmadd231sd    %xmm0, %xmm0, %xmm6
        vfmadd132sd     %xmm6, %xmm5, %xmm7
        vfnmadd132sd    %xmm0, %xmm10, %xmm0
        vfmadd132sd     %xmm3, %xmm7, %xmm0
        vaddsd  304(%rdi), %xmm0, %xmm1
        vmovsd  %xmm1, 304(%rdi)
        vaddsd  304(%rbx), %xmm0, %xmm0
        vmovsd  %xmm0, 304(%rbx)

LLVM-3.5 with -Ofast -ffast-math -march=core-avx2 generates
107 insns (10% less than GCC!):

.LBB0_135:                              # %if.then1703
                                        #   in Loop: Header=BB0_132 Depth=3
         leal    (,%r15,4), %eax
        vmovsd  .LCPI0_4(%rip), %xmm1
        vdivsd  %xmm0, %xmm1, %xmm1
        vmulsd  %xmm1, %xmm1, %xmm0
        vmulsd  %xmm0, %xmm0, %xmm2
        vmulsd  %xmm2, %xmm0, %xmm0
        vmovsd  56(%r13), %xmm2
        vmovsd  64(%r13), %xmm3
        vmulsd  56(%rcx), %xmm2, %xmm2
        vmovsd  368(%rsp), %xmm4        # 8-byte Reload
        vmulsd  %xmm2, %xmm4, %xmm2
        vmulsd  %xmm2, %xmm1, %xmm2
        vmulsd  64(%rcx), %xmm3, %xmm3
        vmulsd  %xmm3, %xmm0, %xmm3
        vmovsd  72(%r13), %xmm4
        vmulsd  72(%rcx), %xmm4, %xmm4
        vmulsd  %xmm0, %xmm0, %xmm0
        vmulsd  %xmm4, %xmm0, %xmm0
        vsubsd  %xmm3, %xmm2, %xmm4
        vaddsd  %xmm0, %xmm4, %xmm5
        vmulsd  %xmm2, %xmm1, %xmm2
        vmulsd  %xmm3, %xmm1, %xmm3
        vmulsd  %xmm0, %xmm1, %xmm0
        vmovsd  .LCPI0_9(%rip), %xmm4
        vfmsub213sd     %xmm2, %xmm3, %xmm4
        vmovsd  .LCPI0_10(%rip), %xmm6
        vfmadd213sd     %xmm4, %xmm0, %xmm6
        vmulsd  %xmm2, %xmm1, %xmm2
        vmulsd  %xmm3, %xmm1, %xmm4
        vmulsd  %xmm0, %xmm1, %xmm0
        vmulsd  .LCPI0_11(%rip), %xmm2, %xmm11
        vmulsd  .LCPI0_12(%rip), %xmm4, %xmm14
        vmulsd  .LCPI0_13(%rip), %xmm0, %xmm10
        cltq
        vpermilpd       $0, %xmm1, %xmm0 # xmm0 = xmm1[0,0]
        vmulpd  (%r11,%rax,8), %xmm0, %xmm0
        orl     $2, %eax
        cltq
        vmulsd  (%r11,%rax,8), %xmm1, %xmm9
        vaddsd  208(%r13), %xmm5, %xmm5
        vmovsd  %xmm5, 208(%r13)
        vpermilpd       $0, %xmm6, %xmm5 # xmm5 = xmm6[0,0]
        vmulpd  %xmm0, %xmm5, %xmm5
        vmovupd 240(%rcx), %xmm7
        vsubpd  %xmm5, %xmm7, %xmm7
        vmovupd %xmm7, 240(%rcx)
        vaddpd  240(%r13), %xmm5, %xmm5
        vmovupd %xmm5, 240(%r13)
        vmulsd  %xmm6, %xmm9, %xmm5
        vmovsd  256(%rcx), %xmm6
        vsubsd  %xmm5, %xmm6, %xmm6
        vmovsd  %xmm6, 256(%rcx)
        vaddsd  256(%r13), %xmm5, %xmm5
        vmovsd  %xmm5, 256(%r13)
        vmulsd  %xmm0, %xmm0, %xmm5
        vunpckhpd       %xmm0, %xmm0, %xmm8 # xmm8 = xmm0[1,1]
        vmulsd  %xmm8, %xmm8, %xmm15
        vmulsd  %xmm9, %xmm9, %xmm7
        vmovsd  .LCPI0_14(%rip), %xmm3
        vaddsd  %xmm3, %xmm5, %xmm1
        vmovsd  .LCPI0_15(%rip), %xmm4
        vaddsd  %xmm4, %xmm5, %xmm2
        vmulsd  %xmm2, %xmm14, %xmm2
        vfmadd213sd     %xmm2, %xmm11, %xmm1
        vmovsd  .LCPI0_16(%rip), %xmm6
        vaddsd  %xmm6, %xmm5, %xmm5
        vfmadd213sd     %xmm1, %xmm10, %xmm5
        vaddsd  %xmm3, %xmm15, %xmm1
        vaddsd  %xmm4, %xmm15, %xmm2
        vmulsd  %xmm2, %xmm14, %xmm2
        vfmadd213sd     %xmm2, %xmm11, %xmm1
        vaddsd  %xmm3, %xmm7, %xmm2
        vaddsd  %xmm4, %xmm7, %xmm3
        vmulsd  %xmm3, %xmm14, %xmm3
        vfmadd213sd     %xmm3, %xmm11, %xmm2
        vaddsd  %xmm14, %xmm11, %xmm3
        vaddsd  %xmm6, %xmm15, %xmm4
        vfmadd213sd     %xmm1, %xmm10, %xmm4
        vaddsd  %xmm6, %xmm7, %xmm1
        vfmadd213sd     %xmm2, %xmm10, %xmm1
        vaddsd  %xmm10, %xmm3, %xmm2
        vmulsd  %xmm2, %xmm8, %xmm3
        vmulsd  %xmm3, %xmm0, %xmm6
        vunpcklpd       %xmm6, %xmm5, %xmm5 # xmm5 = xmm5[0],xmm6[0]
        vmovupd 264(%rcx), %xmm6
        vsubpd  %xmm5, %xmm6, %xmm6
        vmovupd %xmm6, 264(%rcx)
        vmovupd 264(%r13), %xmm6
        vsubpd  %xmm5, %xmm6, %xmm5
        vmovupd %xmm5, 264(%r13)
        vmulsd  %xmm2, %xmm9, %xmm2
        vmulsd  %xmm2, %xmm0, %xmm0
        vunpcklpd       %xmm4, %xmm0, %xmm0 # xmm0 = xmm0[0],xmm4[0]
        vmovupd 280(%rcx), %xmm2
        vsubpd  %xmm0, %xmm2, %xmm2
        vmovupd %xmm2, 280(%rcx)
        vmovupd 280(%r13), %xmm2
        vsubpd  %xmm0, %xmm2, %xmm0
        vmovupd %xmm0, 280(%r13)
        vmulsd  %xmm3, %xmm9, %xmm0
        vunpcklpd       %xmm1, %xmm0, %xmm0 # xmm0 = xmm0[0],xmm1[0]
        vmovupd 296(%rcx), %xmm1
        vsubpd  %xmm0, %xmm1, %xmm1
        vmovupd %xmm1, 296(%rcx)
        vmovupd 296(%r13), %xmm1
        vsubpd  %xmm0, %xmm1, %xmm0
        vmovupd %xmm0, 296(%r13)

It is achieved by vectorization, please see vsubpd and vmulpd in LLVM
generated code.


---


### compiler : `gcc`
### title : `vector lowering should split loads and stores`
### open_at : `2015-01-22T15:15:13Z`
### last_modified_date : `2023-05-12T13:05:08Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=64731
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `5.0`
### severity : `enhancement`
### contents :
It would be nice if for some simple cases too large vector_size for the selected instruction set would still produce efficient code.
E.g. using vector_size of 32 for SSE2 code results in essentially once unrolled vector_size 16 code and it still simply uses AVX if it one compiles with the appropriate option.

But with current gcc 5.0 with this code:

typedef double double4 __attribute__((vector_size(32)));

void fun(double * a, double * b)
{
    for (int i = 0; i < 1024; i+=4) {
        *(double4*)&a[i] += *(double4*)&b[i];
    }
}

with AVX this turns into the expected code, but with only SSE2 enabled one gets this:
gcc -O3 test2.c -c -std=c99

0000000000000000 <fun>:
   0:	4c 8d 54 24 08       	lea    0x8(%rsp),%r10
   5:	48 83 e4 e0          	and    $0xffffffffffffffe0,%rsp
   9:	31 c0                	xor    %eax,%eax
   b:	41 ff 72 f8          	pushq  -0x8(%r10)
   f:	55                   	push   %rbp
  10:	48 89 e5             	mov    %rsp,%rbp
  13:	41 52                	push   %r10
  15:	48 83 ec 10          	sub    $0x10,%rsp
  19:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)
  20:	48 8b 14 07          	mov    (%rdi,%rax,1),%rdx
  24:	48 89 55 90          	mov    %rdx,-0x70(%rbp)
  28:	48 8b 54 07 08       	mov    0x8(%rdi,%rax,1),%rdx
  2d:	48 89 55 98          	mov    %rdx,-0x68(%rbp)
  31:	48 8b 54 07 10       	mov    0x10(%rdi,%rax,1),%rdx
  36:	48 89 55 a0          	mov    %rdx,-0x60(%rbp)
  3a:	48 8b 54 07 18       	mov    0x18(%rdi,%rax,1),%rdx
  3f:	48 89 55 a8          	mov    %rdx,-0x58(%rbp)
  43:	48 8b 14 06          	mov    (%rsi,%rax,1),%rdx
  47:	48 89 55 b0          	mov    %rdx,-0x50(%rbp)
  4b:	48 8b 54 06 08       	mov    0x8(%rsi,%rax,1),%rdx
  50:	48 89 55 b8          	mov    %rdx,-0x48(%rbp)
  54:	48 8b 54 06 10       	mov    0x10(%rsi,%rax,1),%rdx
  59:	66 0f 28 45 b0       	movapd -0x50(%rbp),%xmm0
  5e:	66 0f 58 45 90       	addpd  -0x70(%rbp),%xmm0
  63:	48 89 55 c0          	mov    %rdx,-0x40(%rbp)
  67:	48 8b 54 06 18       	mov    0x18(%rsi,%rax,1),%rdx
  6c:	48 89 55 c8          	mov    %rdx,-0x38(%rbp)
  70:	0f 29 85 70 ff ff ff 	movaps %xmm0,-0x90(%rbp)
  77:	66 48 0f 7e c2       	movq   %xmm0,%rdx
  7c:	66 0f 28 45 c0       	movapd -0x40(%rbp),%xmm0
  81:	48 89 14 07          	mov    %rdx,(%rdi,%rax,1)
  85:	48 8b 95 78 ff ff ff 	mov    -0x88(%rbp),%rdx
  8c:	66 0f 58 45 a0       	addpd  -0x60(%rbp),%xmm0
  91:	0f 29 45 80          	movaps %xmm0,-0x80(%rbp)
  95:	48 89 54 07 08       	mov    %rdx,0x8(%rdi,%rax,1)
  9a:	48 8b 55 80          	mov    -0x80(%rbp),%rdx
  9e:	48 89 54 07 10       	mov    %rdx,0x10(%rdi,%rax,1)
  a3:	48 8b 55 88          	mov    -0x78(%rbp),%rdx
  a7:	48 89 54 07 18       	mov    %rdx,0x18(%rdi,%rax,1)
  ac:	48 83 c0 20          	add    $0x20,%rax
  b0:	48 3d 00 20 00 00    	cmp    $0x2000,%rax
  b6:	0f 85 64 ff ff ff    	jne    20 <fun+0x20>
  bc:	48 83 c4 10          	add    $0x10,%rsp
  c0:	41 5a                	pop    %r10
  c2:	5d                   	pop    %rbp
  c3:	49 8d 62 f8          	lea    -0x8(%r10),%rsp
  c7:	c3                   	retq   
  c8:	0f 1f 84 00 00 00 00 	nopl   0x0(%rax,%rax,1)
  cf:	00 


while I would have hoped for something along the lines of this:

  10:	66 0f 28 44 c6 10    	movapd 0x10(%rsi,%rax,8),%xmm0
  16:	66 0f 28 0c c6       	movapd (%rsi,%rax,8),%xmm1
  1b:	66 0f 58 0c c7       	addpd  (%rdi,%rax,8),%xmm1
  20:	66 0f 58 44 c7 10    	addpd  0x10(%rdi,%rax,8),%xmm0
  26:	66 0f 29 44 c7 10    	movapd %xmm0,0x10(%rdi,%rax,8)
  2c:	66 0f 29 0c c7       	movapd %xmm1,(%rdi,%rax,8)
  31:	48 83 c0 04          	add    $0x4,%rax
  35:	3d 00 04 00 00       	cmp    $0x400,%eax
  3a:	7c d4                	jl     10 <fun+0x10>


---


### compiler : `gcc`
### title : `Generic vectorization missed opportunities`
### open_at : `2015-01-23T12:09:50Z`
### last_modified_date : `2021-12-26T22:49:02Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=64745
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `5.0`
### severity : `enhancement`
### contents :
unsigned short a[2], b[2];
void foo (void)
{
  int i;
  for (i = 0; i < 2; ++i)
    a[i] = b[i];
}

unsigned char x[4], y[4];
void bar (void)
{
  int i;
  for (i = 0; i < 4; ++i)
    x[i] = y[i];
}

vectorizing this on i?86 (without SSE) fails for the first testcase at -O3
because we unroll the loop and SLP refuses to handle the "unaligned" load.
For the 2nd case we loop-vectorize it but apply versioning for alignment.

The alignment checks in the vectorizer do not account for non-vector modes.

If we fix that the first loop fails to SLP vectorize because of bogus
cost calculation:

t.c:6:13: note: Cost model analysis:
  Vector inside of basic block cost: 4
  Vector prologue cost: 0
  Vector epilogue cost: 0
  Scalar cost of basic block: 4
t.c:6:13: note: not vectorized: vectorization is not profitable.

because of the unaligned load/store cost:

t.c:6:13: note: vect_model_load_cost: unaligned supported by hardware.
t.c:6:13: note: vect_model_load_cost: inside_cost = 2, prologue_cost = 0 .
...
t.c:6:13: note: vect_model_store_cost: unaligned supported by hardware.
t.c:6:13: note: vect_model_store_cost: inside_cost = 2, prologue_cost = 0 .

that's a backend bug which doesn't consider !VECTOR_MODE_P vector types
in ix86_builtin_vectorization_cost.  OTOH for SLP vectorization if
the cost is equal we can assume less stmts will be used so eventually
just vectorize anyway if the costs are equal.


The real issue of course is that generic vectorization is not attempted
if a vector ISA is available - but that fails to vectorize the above cases
where SLP vectorization would take care of combining small loads and stores.

So we'd need to support HImode, SImode (and DImode on x86_64) vectorization
sizes which probably comes at a too big cost to consider that though
basic-block vectorization (knowing the size of the loads) could try anyway.
But that needs some re-org of the analysis.


---


### compiler : `gcc`
### title : `Loop with nested load/stores is not vectorized using aggressive if-conversion.`
### open_at : `2015-01-23T13:09:05Z`
### last_modified_date : `2021-10-01T03:21:14Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=64746
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `5.0`
### severity : `normal`
### contents :
Attached simple test-case extracted from important suite is not vectorized even if 'pragma omp simd' is used since ifcvt_repair_bool_pattern does not remove all multiple uses and we get the following message:

test.c:11:14: note: bit-precision arithmetic not supported.
test.c:11:14: note: not vectorized: relevant stmt not supported: _ifc__90 = x1_7 >= 0;

The problem is that statement splitting may introduce other multiple predicate uses and iterative algorithm should be used.

I attached simple fix which cures the problem.


---


### compiler : `gcc`
### title : `[SH] Avoid multiple #imm,r0 insns with the same #imm value`
### open_at : `2015-01-24T00:57:52Z`
### last_modified_date : `2021-09-12T22:33:53Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=64760
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `5.0`
### severity : `normal`
### contents :
In libstdc++ there is code such as:
        mov     r9,r0
        cmp/eq  #-1,r0
        mov     r1,r0
        movt    r2
        cmp/eq  #-1,r0
        movt    r1
        cmp/eq  r1,r2
        bt      ...

It seems that it's better to avoid #imm,r0 insns such as cmp/eq, and, or, xor, tst, if the #imm value can be shared among several insns.  The insns don't have to be same, only the constant value.

The above code could be something like:
        mov     #-1,r0
        cmp/eq  r9,r0
        movt    r2
        cmp/eq  r1,r0
        movt    r1
        cmp/eq  r1,r2

Preferably, this should be done before RA to reduce r0 pressure.  It can be accomplished by simply loading the constant into a pseudo and replacing the operands in the insns.

On the other hand, if the other operand (other than #imm) is likely to end up in r0, the #imm,r0 insn is probably going to be better.

A possible metric for 'likely to be in r0' could be:
- the operand is loaded using a mov.{b|w} @(disp,Rn),R0
- the operand is needed in r0 by some other surrounding insns


---


### compiler : `gcc`
### title : `[ARM/thumb] missed optimization: pc relative ldr used when constant can be derived from register`
### open_at : `2015-01-24T16:00:22Z`
### last_modified_date : `2020-06-05T05:39:25Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=64774
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `9.2.1`
### severity : `enhancement`
### contents :
In the example the second write address of each function can either be generated using 'str' with an immediate offset or using an adds with an immediate addend.

The compiler does this for test1-3. For test4-6 it emits a pc-relative ldr instruction and a 32bit constant. This increases size and likely impacts execution speed.

cat test.c
void test1()
{
    *(unsigned *)4 = 0x666;
    *(unsigned *)(4 + 4) = 0x666;
}


void test2()
{
    *(unsigned *)4 = 0x666;
    *(unsigned *)(4 + 128) = 0x666;
}

void test3()
{
    *(unsigned *)0x444 = 0x666;
    *(unsigned *)(0x444 + 4) = 0x666;
}


void test4()
{
    *(unsigned *)0x444 = 0x666;
    *(unsigned *)(0x444 + 128) = 0x666;
}

void test5()
{
    *(unsigned *)0x44444444 = 0x666;
    *(unsigned *)(0x44444444 + 4) = 0x666;
}


void test6()
{
    *(unsigned *)0x44444444 = 0x666;
    *(unsigned *)(0x44444444 + 128) = 0x666;
}

arm-none-eabi-gcc -c test.c -mthumb -mcpu=cortex-m0 -mtune=cortex-m0 -Ofast -o test.o

00000000 <test1>:
   0:	2204      	movs	r2, #4
   2:	4b02      	ldr	r3, [pc, #8]	; (c <test1+0xc>)
   4:	6013      	str	r3, [r2, #0]
   6:	6053      	str	r3, [r2, #4]
   8:	4770      	bx	lr
   a:	46c0      	nop			; (mov r8, r8)
   c:	00000666 	.word	0x00000666

00000010 <test2>:
  10:	2204      	movs	r2, #4
  12:	4b02      	ldr	r3, [pc, #8]	; (1c <test2+0xc>)
  14:	6013      	str	r3, [r2, #0]
  16:	3280      	adds	r2, #128	; 0x80
  18:	6013      	str	r3, [r2, #0]
  1a:	4770      	bx	lr
  1c:	00000666 	.word	0x00000666

00000020 <test3>:
  20:	4b02      	ldr	r3, [pc, #8]	; (2c <test3+0xc>)
  22:	4a03      	ldr	r2, [pc, #12]	; (30 <test3+0x10>)
  24:	6013      	str	r3, [r2, #0]
  26:	6053      	str	r3, [r2, #4]
  28:	4770      	bx	lr
  2a:	46c0      	nop			; (mov r8, r8)
  2c:	00000666 	.word	0x00000666
  30:	00000444 	.word	0x00000444

00000034 <test4>:
  34:	4b02      	ldr	r3, [pc, #8]	; (40 <test4+0xc>)
  36:	4a03      	ldr	r2, [pc, #12]	; (44 <test4+0x10>)
  38:	6013      	str	r3, [r2, #0]
  3a:	4a03      	ldr	r2, [pc, #12]	; (48 <test4+0x14>)
  3c:	6013      	str	r3, [r2, #0]
  3e:	4770      	bx	lr
  40:	00000666 	.word	0x00000666
  44:	00000444 	.word	0x00000444
  48:	000004c4 	.word	0x000004c4

0000004c <test5>:
  4c:	4b02      	ldr	r3, [pc, #8]	; (58 <test5+0xc>)
  4e:	4a03      	ldr	r2, [pc, #12]	; (5c <test5+0x10>)
  50:	6013      	str	r3, [r2, #0]
  52:	4a03      	ldr	r2, [pc, #12]	; (60 <test5+0x14>)
  54:	6013      	str	r3, [r2, #0]
  56:	4770      	bx	lr
  58:	00000666 	.word	0x00000666
  5c:	44444444 	.word	0x44444444
  60:	44444448 	.word	0x44444448

00000064 <test6>:
  64:	4b02      	ldr	r3, [pc, #8]	; (70 <test6+0xc>)
  66:	4a03      	ldr	r2, [pc, #12]	; (74 <test6+0x10>)
  68:	6013      	str	r3, [r2, #0]
  6a:	4a03      	ldr	r2, [pc, #12]	; (78 <test6+0x14>)
  6c:	6013      	str	r3, [r2, #0]
  6e:	4770      	bx	lr
  70:	00000666 	.word	0x00000666
  74:	44444444 	.word	0x44444444
  78:	444444c4 	.word	0x444444c4


Compiled using:
https://launchpad.net/gcc-arm-embedded/4.9/4.9-2014-q4-major/+download/gcc-arm-none-eabi-4_9-2014q4-20141203-win32.exe


---


### compiler : `gcc`
### title : `[9/10/11/12 Regression][SH] and|or|xor #imm not used`
### open_at : `2015-01-25T13:11:18Z`
### last_modified_date : `2022-02-26T15:47:47Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=64785
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `5.0`
### severity : `normal`
### contents :
It seems that for some reason loading a constant is now favored instead of using the #imm,R0 alternative.

void test000 (int* x, int xb)
{
  x[0] = xb & 128;
}

void test001 (int* x, int xb)
{
  x[0] = xb | 128;
}

void test002 (int* x, int xb)
{
  x[0] = xb ^ 128;
}

trunk:
_test000:
	mov.w	.L7,r1	! 15	*movhi/1	[length = 2]
	and	r1,r5	! 7	*andsi_compact/4	[length = 2]
	rts		! 18	*return_i	[length = 2]
	mov.l	r5,@r4	! 8	movsi_ie/9	[length = 2]

4.9:
	mov	r5,r0	! 15	movsi_ie/2	[length = 2]
	and	#128,r0	! 7	*andsi_compact/3	[length = 2]
	rts		! 18	*return_i	[length = 2]
	mov.l	r0,@r4	! 8	movsi_ie/9	[length = 2]


The RTL before RA is the same in both cases:

(insn 7 4 8 2 (set (reg:SI 163 [ D.1431 ])
        (and:SI (reg:SI 5 r5 [ xb ])
            (const_int 128 [0x80]))) sh_tmp.cpp:257 124 {*andsi_compact}
     (expr_list:REG_DEAD (reg:SI 5 r5 [ xb ])
        (nil)))
(insn 8 7 0 2 (set (mem:SI (reg:SI 4 r4 [ x ]) [1 *x_4(D)+0 S4 A32])
        (reg:SI 163 [ D.1431 ])) sh_tmp.cpp:257 257 {movsi_ie}
     (expr_list:REG_DEAD (reg:SI 4 r4 [ x ])
        (expr_list:REG_DEAD (reg:SI 163 [ D.1431 ])
            (nil))))

Reload on trunk says:

Reloads for insn # 7
Reload 0: reload_in (SI) = (const_int 128 [0x80])
	GENERAL_REGS, RELOAD_FOR_INPUT (opnum = 2)
	reload_in_reg: (const_int 128 [0x80])
	reload_reg_rtx: (reg:SI 1 r1)


While reload on 4.9 says:

Reloads for insn # 7
Reload 0: reload_in (SI) = (reg:SI 5 r5 [ xb ])
	reload_out (SI) = (reg:SI 0 r0 [orig:163 D.1377 ] [163])
	R0_REGS, RELOAD_OTHER (opnum = 0)
	reload_in_reg: (reg:SI 5 r5 [ xb ])
	reload_out_reg: (reg:SI 0 r0 [orig:163 D.1377 ] [163])
	reload_reg_rtx: (reg:SI 0 r0 [orig:163 D.1377 ] [163])

Maybe this is because the function argument from hardreg r5 is propagated into the insn.  This propagation is also causing unnecessary sign/zero extensions, see https://gcc.gnu.org/bugzilla/show_bug.cgi?id=53987#c9


---


### compiler : `gcc`
### title : `Eliminate exceptions thrown/caught inside a function`
### open_at : `2015-01-25T14:01:31Z`
### last_modified_date : `2021-12-25T11:07:24Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=64786
### status : `NEW`
### tags : `EH, missed-optimization`
### component : `c++`
### version : `5.0`
### severity : `enhancement`
### contents :
If I'm not mistaken, in the following example:

int test (int a, int b, int* c)
{
  enum err_a_t { ERR_A };
  enum err_b_t { ERR_B };

  try
  {
    if ((a + b) == 123)
      throw ERR_A;

    if ((a - b) == 5)
      throw ERR_B;

    for (int i = 0; i < b; ++i)
      c[i] = 4;

    return 0;
  }
  catch (err_a_t)
  {
    c[0] = 0;
    return -1;
  }
  catch (err_b_t)
  {
    c[0] = 1;
    return -1;
  }
  catch (...)
  {
    __builtin_abort ();
  }
}

... the exceptions can be eliminated and converted into something like this unless -fnon-call-exceptions is used (the mem accesses could throw).

int test (int a, int b, int* c)
{
  if ((a + b) == 123)
  {
    c[0] = 0;
    return -1;
  }

  if ((a - b) == 5)
  {
    c[0] = 0;
    return -1;
  }

  for (int i = 0; i < b; ++i)
    c[i] = 4;

  return 0;
}

.. because all possible exceptions are known and are also known to be caught in the function itself and there's nothing to stack-unwind.


---


### compiler : `gcc`
### title : `[11/12/13/14 Regression][SH] movu.b movu.w not working`
### open_at : `2015-01-25T22:57:07Z`
### last_modified_date : `2023-07-07T10:30:34Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=64792
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `target`
### version : `5.0`
### severity : `normal`
### contents :
The treg_set_expr patch from r220081 disabled early matching of the SH2A movu.b and movu.w patterns during RTL expansion and combine.  This was done because it's otherwise difficult to convert zero-extending loads back to sign-extending loads in cases where using sign-extended values is fine.  Sign-extending loads are shorter (2 bytes vs. 4 bytes insns) and the zero-extending loads should be formed as a last resort option, after combine and split1, but before RA.  The idea is to do that in a simple peephole-like RTL pass.


---


### compiler : `gcc`
### title : `[AArch64] Improve target folding for vsqrt_f64 intrinsic`
### open_at : `2015-01-27T09:43:21Z`
### last_modified_date : `2022-01-23T22:19:14Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=64821
### status : `RESOLVED`
### tags : `missed-optimization, patch`
### component : `target`
### version : `5.0`
### severity : `enhancement`
### contents :
Following the implementation of vsqrt_f64 with a target builtin:
https://gcc.gnu.org/ml/gcc-patches/2015-01/msg00699.html

it was suggested to add some target folding code into a sqrt when -fno-math-errno is given:
https://gcc.gnu.org/ml/gcc-patches/2015-01/msg00710.html

This issue tracks that work that should be done for GCC 6


---


### compiler : `gcc`
### title : `RA picks the wrong register for -fipa-ra`
### open_at : `2015-02-01T13:47:38Z`
### last_modified_date : `2019-09-08T19:41:52Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=64895
### status : `REOPENED`
### tags : `missed-optimization, ra`
### component : `rtl-optimization`
### version : `5.0`
### severity : `normal`
### contents :
'-fipa-ra'
     Use caller save registers for allocation if those registers are not
     used by any called function.  In that case it is not necessary to
     save and restore them around calls.  This is only possible if
     called functions are part of same compilation unit as current
     function and they are compiled before it.

But in this case testcase 
[hjl@gnu-tools-1 gcc]$ cat /tmp/x.c 
static int __attribute__((noinline))
bar (int x)
{
  if (x > 4)
    return bar (x - 3);
  return 0;
}

int __attribute__((noinline))
foo (int y)
{
  return y + bar (y);
}
[hjl@gnu-tools-1 gcc]$ ./xgcc -B./ -m32 -fpic -O2 -fipa-ra -fomit-frame-pointer -fno-optimize-sibling-calls -mregparm=1 /tmp/x.c -S -fno-asynchronous-unwind-tables        
[hjl@gnu-tools-1 gcc]$ cat x.s 
	.file	"x.c"
	.section	.text.unlikely,"ax",@progbits
.LCOLDB0:
	.text
.LHOTB0:
	.p2align 4,,15
	.type	bar, @function
bar:
	cmpl	$4, %eax
	jg	.L7
	xorl	%eax, %eax
	ret
	.p2align 4,,10
	.p2align 3
.L7:
	subl	$12, %esp
	subl	$3, %eax
	call	bar
	addl	$12, %esp
	ret
	.size	bar, .-bar
	.section	.text.unlikely
.LCOLDE0:
	.text
.LHOTE0:
	.section	.text.unlikely
.LCOLDB1:
	.text
.LHOTB1:
	.p2align 4,,15
	.globl	foo
	.type	foo, @function
foo:
	pushl	%ebx
	movl	%eax, %ebx
	subl	$8, %esp
	call	bar
	addl	$8, %esp
	addl	%ebx, %eax
	popl	%ebx
	ret
	.size	foo, .-foo
	.section	.text.unlikely
.LCOLDE1:
	.text
.LHOTE1:
	.ident	"GCC: (GNU) 5.0.0 20150201 (experimental)"
	.section	.note.GNU-stack,"",@progbits
[hjl@gnu-tools-1 gcc]$ 

Pick EBX instead of EDX to save EAX in foo.


---


### compiler : `gcc`
### title : `Floating-point "and" not optimized on x86-64`
### open_at : `2015-02-01T19:45:59Z`
### last_modified_date : `2021-11-28T08:07:16Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=64897
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.9.2`
### severity : `enhancement`
### contents :
I notice that gcc does not generate "vandpd" for floating-point "and" operations. Here is an example code that demonstrates this:
{{{
#include <math.h>
#include <string.h>
double fand1(double x)
{
  unsigned long ix;
  memcpy(&ix, &x, 8);
  ix &= 0x7fffffffffffffffUL;
  memcpy(&x, &ix, 8);
  return x;
}
double fand2(double x)
{
  return fabs(x);
}
}}}

When I compile this via:
{{{
gcc-mp-4.9 -O3 -march=native -S fand.c -o fand-gcc-4.9.s
}}}
(OS X, x86-64 CPU, Intel Core i7), this results in:
{{{
_fand1:
	movabsq	$9223372036854775807, %rax
	vmovd	%xmm0, %rdx
	andq	%rdx, %rax
	vmovd	%rax, %xmm0
	ret
_fand2:
	vmovsd	LC1(%rip), %xmm1
	vandpd	%xmm1, %xmm0, %xmm0
	ret
}}}

This shows that (a) gcc performs the bitwise and operation in an integer register, which is probably slower, and (b) the implementors of "fabs" assume that using the "vandpd" instruction is faster.


---


### compiler : `gcc`
### title : `[5 Regression] Inefficient address pre-computation in PIC mode`
### open_at : `2015-02-06T13:56:19Z`
### last_modified_date : `2021-09-27T01:55:26Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=64960
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `5.0`
### severity : `enhancement`
### contents :
After EBX was unfixed in i386 PIC target, we may see addresses of static objects are loaded from GOT and placed to the stack for later usage.  It allows to reuse PIC register for other purposes.  But in cases when PIC register is still used (e.g. for calls) it may cause inefficiency in produced code. Here is an example:

>cat test.c
void f (int);
int val1, *val2, val3;
int test (int max)
{
  int i;
  for (i = 0; i < max; i++)
    {
      val1 += val2[i];
      f (val3);
    }
}
>gcc test.c -O2 -fPIE -S -m32 -ffixed-esi -ffixed-edi -ffixed-edx
>cat test.s
...
        movl    val1@GOT(%ebx), %eax  <-- may be removed
        xorl    %ebp, %ebp
        movl    %eax, 4(%esp)         <-- may be removed
        movl    val2@GOT(%ebx), %eax  <-- may be removed
        movl    %eax, 8(%esp)         <-- may be removed
        movl    val3@GOT(%ebx), %eax  <-- may be removed
        movl    %eax, 12(%esp)        <-- may be removed
.L3:
        movl    8(%esp), %eax         <-- equal to    movl  val2@GOT(%ebx), %eax
        subl    $12, %esp
        movl    (%eax), %ecx
        movl    16(%esp), %eax        <-- equal to    movl  val1@GOT(%ebx), %eax
        movl    (%ecx,%ebp,4), %ecx
        addl    %ecx, (%eax)
        addl    $1, %ebp
        movl    24(%esp), %eax        <-- equal to    movl  val3@GOT(%ebx), %eax
        pushl   (%eax)
        call    f@PLT
        addl    $16, %esp
        cmpl    %ebp, 32(%esp)
        jne     .L3
...

Also storing value on the stack doesn't benefit on static objects optimization performed by linker which transforms movl <symbol>@GOT<PIC> into lea instruction.  It would be useful to avoid early address computation in case PIC register is available at address usage.

Here is a code generated by GCC 4.9:

        xorl    %ebp, %ebp
.L2:
        movl    val2@GOT(%ebx), %eax
        subl    $12, %esp
        movl    (%eax), %ecx
        movl    val1@GOT(%ebx), %eax
        movl    (%ecx,%ebp,4), %ecx
        addl    %ecx, (%eax)
        addl    $1, %ebp
        movl    val3@GOT(%ebx), %eax
        pushl   (%eax)
        call    f@PLT
        addl    $16, %esp
        cmpl    16(%esp), %ebp
        jne     .L2

Used gcc (GCC) 5.0.0 20150205 (experimental).


---


### compiler : `gcc`
### title : `More optimize opportunity`
### open_at : `2015-02-10T03:01:11Z`
### last_modified_date : `2023-09-21T11:40:16Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=64992
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `5.0`
### severity : `enhancement`
### contents :
The two programs (A.c) and (B.c) only differ by one line (marked by "// <---HERE"),
where (B.c) simply replace local variable b by its initial value 2U.
The code (A.s) for (A.c) is less optimized than (B.s) for (B.c).

(org.c)
int main (void)
{
  volatile int a = -1;
  unsigned int b = 2U;

  int          c = a + 0;
  unsigned     d = b * (1 == c);     //<---HERE
  
  if (c == -1) ;
  else __builtin_abort();
  if (d == 0U) ;
  else __builtin_abort();
  
  return 0;
}

(opt.c)
int main (void)
{
  volatile int a = -1;
  unsigned int b = 2U;

  int          c = a + 0;
  unsigned     d = 2U * (1 == c);    //<---HERE
  
  if (c == -1) ;
  else __builtin_abort();
  if (d == 0U) ;
  else __builtin_abort();
  
  return 0;
}

(org.s)
main:
.LFB0:
  .cfi_startproc
  subq   $24, %rsp
  .cfi_def_cfa_offset 32
  xorl   %eax, %eax
  movl   $-1, 12(%rsp)
  movl   12(%rsp), %edx
  cmpl   $1, %edx
  sete   %al
  addl   %eax, %eax
  cmpl   $-1, %edx
  jne    .L3
  testl  %eax, %eax
  jne    .L3
  addq   $24, %rsp
  .cfi_remember_state
  .cfi_def_cfa_offset 8
  ret
.L3:
  .cfi_restore_state
  call  abort
  .cfi_endproc
.LFE0:
  .size  main, .-main
  .section  .text.unlikely
.LCOLDE0:
  .section  .text.startup
.LHOTE0:
  .ident  "GCC: (GNU) 5.0.0 20150205 (experimental)"
  .section  .note.GNU-stack,"",@progbits

(opt.s)
main:
.LFB0:
  .cfi_startproc
  subq   $24, %rsp
  .cfi_def_cfa_offset 32
  movl   $-1, 12(%rsp)
  movl   12(%rsp), %eax
  cmpl   $-1, %eax
  jne    .L5
  xorl   %eax, %eax
  addq   $24, %rsp
  .cfi_remember_state
  .cfi_def_cfa_offset 8
  ret
.L5:
  .cfi_restore_state
  call  abort
  .cfi_endproc
.LFE0:
  .size  main, .-main
  .section  .text.unlikely
.LCOLDE0:
  .section  .text.startup
.LHOTE0:
  .ident  "GCC: (GNU) 5.0.0 20150205 (experimental)"
  .section  .note.GNU-stack,"",@progbits
  
  
$ x86_64-unknown-linux-gnu-gcc-5.0.0 -v
Using built-in specs.
COLLECT_GCC=x86_64-unknown-linux-gnu-gcc-5.0.0
COLLECT_LTO_WRAPPER=/usr/local/x86_64-tools/gcc-5.0.0/libexec/gcc/x86_64-unknown-linux-gnu/5.0.0/lto-wrapper
Target: x86_64-unknown-linux-gnu
Configured with: /home/iwatsuji/gcc/configure --prefix=/usr/local/x86_64-tools/gcc-5.0.0/
--with-gmp=/usr/local/gmp-5.1.1/ --with-mpfr=/usr/local/mpfr-3.1.2/ --with-mpc=/usr/local/mpc-1.0.1/ --disable-multilib --disable-nls --enable-languages=c
Thread model: posix
gcc version 5.0.0 20150205 (experimental) (GCC)


---


### compiler : `gcc`
### title : `ppc backend generates unnecessary signed extension`
### open_at : `2015-02-11T01:20:58Z`
### last_modified_date : `2023-04-11T17:10:00Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=65010
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `target`
### version : `5.0`
### severity : `normal`
### contents :
I use ppc gcc to compile following code with option -O2

unsigned long c2l(unsigned char* p)
{
  unsigned long res = *p + *(p+1);
  return res;
}

long c2sl(signed char* p)
{
  long res = *p + *(p+1);
  return res;
}


Trunk gcc generates:

c2l:
	lbz 10,0(3)
	lbz 9,1(3)
	add 3,10,9
	extsw 3,3
	blr


c2sl:
	lbz 9,1(3)
	lbz 10,0(3)
	extsb 9,9
	extsb 3,10
	add 3,3,9
	extsw 3,3
	blr


The extsw instructions in both functions are unnecessary since it can't change the value in return register.


---


### compiler : `gcc`
### title : `Missed optimization (x86): Redundant test/compare after arithmetic operations`
### open_at : `2015-02-13T18:22:53Z`
### last_modified_date : `2021-08-27T05:48:04Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=65056
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `5.0`
### severity : `normal`
### contents :
The following code seems to miss some really obvious optimizations on
x86, both in -m32 and -m64.  Gcc is generating separate test & compare
instruction for conditions which are available in the condition codes set by
preceding arithmetic operations.

Bugs #30455 and #31799 are similar, but the problems there are caused by a memory destination, which isn't the case here.

This happens with -O2, -O3 and -Os and with various models specified, so it
doesn't appear to be some obscure model-specific optimization.

Versions tested:
* gcc (Debian 4.9.2-10) 4.9.2
* gcc-5 (Debian 5-20150205-1) 5.0.0 20150205 (experimental) [trunk revision 220455]
* gcc (Debian 20150211-1) 5.0.0 20150211 (experimental) [trunk revision 220605]

#include <stddef.h>

#define BITS_PER_LONG (8 * sizeof(long))
#define DIV_ROUND_UP(x,n) (((x) + (n) - 1) / (n))
#define LAST_WORD_MASK(x) (~0ull >> (-(x) & BITS_PER_LONG - 1))

/*
 * __fls: find last set bit in word
 * @word: The word to search
 *
 * Undefined if no set bit exists, so code should check against 0 first.
 */
static inline unsigned long __fls(unsigned long word)
{
	asm("bsr %1,%0"
	    : "=r" (word)
	    : "rm" (word));
	return word;
}

size_t find_last_bit(const unsigned long *addr, size_t size)
{
	size_t idx = DIV_ROUND_UP(size, BITS_PER_LONG);
	unsigned long mask = LAST_WORD_MASK(size);

	while (idx--) {
		unsigned long val = addr[idx] & mask;
		if (val)
			return idx * BITS_PER_LONG + __fls(val);
		mask = ~0ul;
	}
	return size;
}

The code generated is (-m32 is equivalent):

	.file	"flb.c"
	.section	.text.unlikely,"ax",@progbits
.LCOLDB0:
	.text
.LHOTB0:
	.p2align 4,,15
	.globl	find_last_bit
	.type	find_last_bit, @function
find_last_bit:
.LFB1:
	.cfi_startproc
	movl	%esi, %ecx
	leaq	63(%rsi), %rdx
	movq	$-1, %r8
	negl	%ecx
	shrq	%cl, %r8
	shrq	$6, %rdx
	movq	%r8, %rcx
	jmp	.L2
	.p2align 4,,10
	.p2align 3
.L4:
	andq	(%rdi,%rdx,8), %rcx
	movq	%rcx, %r8
	movq	$-1, %rcx
	testq	%r8, %r8
	jne	.L8
.L2:
	subq	$1, %rdx
	cmpq	$-1, %rdx
	jne	.L4
	movq	%rsi, %rax
	ret
	.p2align 4,,10
	.p2align 3
.L8:
	salq	$6, %rdx
#APP
# 15 "flb.c" 1
	bsr %r8,%r8
# 0 "" 2
#NO_APP
	leaq	(%rdx,%r8), %rax
	ret
	.cfi_endproc
.LFE1:
	.size	find_last_bit, .-find_last_bit
	.section	.text.unlikely
.LCOLDE0:
	.text
.LHOTE0:
	.ident	"GCC: (Debian 20150211-1) 5.0.0 20150211 (experimental) [trunk revision 220605]"
	.section	.note.GNU-stack,"",@progbits

In the loop at .L4, there's a completely unnecessary "movq %rcx, %r8;
testq %r8, %r8", when the jne could go right after the andq (and the
code at .L8 changed to expect the masked value in %rcx rather than %r8).

At .L2, it's even more ridiculous.  The subq generates a borrow if the value
wraps to -1.  Why is that not just "subq $1, %rdx; jnc .L4"?

A smarter compiler would notice that %rdx must have its top 6 bits clear
and thus "decq %rdx; jpl .L4" would also be legal.  (For non-x86 weenies,
the "dec" instructions do not modify the carry flag, originally so they
could be used for loop control in multi-word arithmetic.  This partial flags
update makes them slower than "subq $1" on many processors, so which is used
depends on the model flags.)

I tried reorganizing the source to encourage the first optimization:

size_t find_last_bit2(const unsigned long *addr, size_t size)
{
	unsigned long val = LAST_WORD_MASK(size);
	size_t idx = DIV_ROUND_UP(size, BITS_PER_LONG);

	while (idx--) {
		val &= addr[idx];
		if (val)
			return idx * BITS_PER_LONG + __fls(val);
		val = ~0ul;
	}
	return size;
}

... but the generated code is identical.


This version:

size_t find_last_bit3(const unsigned long *addr, size_t size)
{
	if (size) {
		unsigned long val = LAST_WORD_MASK(size);
		size_t idx = (size-1) / BITS_PER_LONG;

		do {
			val &= addr[idx];
			if (val)
				return idx * BITS_PER_LONG + __fls(val);
			val = ~0ul;
		} while (idx--);
	}
	return size;
}

Makes the first optimziation, and is at least clever with the second, but it's still three instructions rather than two for an absolutely bog-standard decrement loop:

find_last_bit3:
.LFB3:
	.cfi_startproc
	xorl	%eax, %eax
	testq	%rsi, %rsi
	je	.L17
	movl	%esi, %ecx
	leaq	-1(%rsi), %rax
	movq	$-1, %rdx
	negl	%ecx
	shrq	%cl, %rdx
	shrq	$6, %rax
	jmp	.L19
	.p2align 4,,10
	.p2align 3
.L18:
	subq	$1, %rax
	movq	$-1, %rdx
	cmpq	%rdx, %rax
	je	.L23
.L19:
	andq	(%rdi,%rax,8), %rdx
	je	.L18
	salq	$6, %rax
#APP
# 15 "flb.c" 1
	bsr %rdx,%rdx
# 0 "" 2
#NO_APP
	addq	%rdx, %rax
	ret
	.p2align 4,,10
	.p2align 3
.L23:
	movq	%rsi, %rax
.L17:
	rep ret


---


### compiler : `gcc`
### title : `Wasted cycles when using a register based varible`
### open_at : `2015-02-16T21:40:50Z`
### last_modified_date : `2023-05-26T02:30:29Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=65082
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.8.0`
### severity : `enhancement`
### contents :
gcc version 4.8.0 20130306 (experimental) (GCC) 

Was just playing around and found this.  When using a register based variable, the compiler misses an obvious optimisation.  

Notice in code below the addition does not take place 'in place' and is instead performed in scratch/temporary registers and then shifted back to "phaseAccPh".  Why not just add directly to "phaseAccPh" since in this case it IS register based already.  It seems that GCC "thinks" that the variable is still in SRAM or something else.....
Nick.




c code:
---------------------------------------------------------
register uint16_t phaseAccPh  asm ("r4");
uint16_t phaseAccFr;

phaseAccPh += phaseAccFr;



asm code:
---------------------------------------------------------
  40:pll.c         **** void pllExec(void)
  41:pll.c         **** {
  15               		.loc 1 41 0
  16               		.cfi_startproc
  17               	/* prologue: function */
  18               	/* frame size = 0 */
  19               	/* stack size = 0 */
  20               	.L__stack_usage = 0
  42:pll.c         ****   int16_t mix_output_s2;
  43:pll.c         ****   phaseAccPh += phaseAccFr;
  21               		.loc 1 43 0
  22 0000 E091 0000 		lds r30,phaseAccFr
  23 0004 F091 0000 		lds r31,phaseAccFr+1
  24 0008 E40D      		add r30,r4
  25 000a F51D      		adc r31,r5
  26 000c 2F01      		movw r4,r30


---


### compiler : `gcc`
### title : `Lack of type narrowing/widening inhibits good vectorization`
### open_at : `2015-02-17T05:21:53Z`
### last_modified_date : `2023-08-22T04:35:25Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=65084
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `unknown`
### severity : `enhancement`
### contents :
These are testcases extracted from 47477.  

short a[1024], b[1024];

void
foo (void)
{
  int i;
  for (i = 0; i < 1024; i++)
    {
      short c = (char) a[i] + 5;
      long long d = (long long) b[i] + 12;
      a[i] = c + d;
    }
}

Compiled with -O3 -mavx2 we ought to get something similar to:

short a[1024], b[1024];

void
foo (void)
{
  int i;
  for (i = 0; i < 1024; i++)
    {
      unsigned short c = ((short)(a[i] << 8) >> 8) + 5U;
      unsigned short d = b[i] + 12U;
      a[i] = c + d;
    }
}


though even in this case I still couldn't achieve the sign extension to be actually performed as 16-bit left + right (signed) shift, while I guess that would lead to even better code.
Or look at how we vectorize:
short a[1024], b[1024];

void
foo (void)
{
  int i;
  for (i = 0; i < 1024; i++)
    {
      unsigned char e = a[i];
      short c = e + 5;
      long long d = (long long) b[i] + 12;
      a[i] = c + d;
    }
}
(note, here forwprop pass already performs type promotion, instead of converting a[i] to unsigned char and back to short, it computes a[i] & 255 in short mode) and how we could instead with type demotions:
short a[1024], b[1024];

void
foo (void)
{
  int i;
  for (i = 0; i < 1024; i++)
    {
      unsigned short c = (a[i] & 0xff) + 5U;
      unsigned short d = b[i] + 12U;
      a[i] = c + d;
    }
}

These are all admittedly artificial testcases, but I've seen tons of loops where multiple types were vectorized and I think in some portion of those loops we could either use just a single type size, or at least decrease the number of conversions and different type sizes in the vectorized loops.


---


### compiler : `gcc`
### title : `[i386] GOTOFF relocation is not propagated into address expression`
### open_at : `2015-02-18T11:41:25Z`
### last_modified_date : `2021-08-16T08:34:06Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=65103
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `target`
### version : `5.0`
### severity : `enhancement`
### contents :
In PIC code there are multiple cases when GOTOFF relocation is put into register and then used in address expression instead of using relocation directly in address expression.  Here is an example:

>cat test.c
typedef struct S
{
  int a;
  int sum;
  int delta;
} S;

S gs;
int global_opt (int max)
{
  while (gs.sum < max)
    gs.sum += gs.delta;
  return gs.a;
}
>gcc test.c -m32 -O2 -fPIE -S
>cat test.s
...
        pushl   %esi
        leal    gs@GOTOFF, %esi
        pushl   %ebx
        call    __x86.get_pc_thunk.bx
        addl    $_GLOBAL_OFFSET_TABLE_, %ebx
        movl    12(%esp), %edx
        movl    4(%esi,%ebx), %eax
        cmpl    %eax, %edx
        jle     .L4
        movl    8(%esi,%ebx), %ecx
.L3:
        addl    %ecx, %eax
        cmpl    %eax, %edx
        jg      .L3
        movl    %eax, 4(%esi,%ebx)
.L4:
        movl    gs@GOTOFF(%ebx), %eax
        popl    %ebx
        popl    %esi
        ret

A separate instruction to get gs@GOTOFF is generated in expand.  Later fwprop propagates this constant only into memory references with zero offset and leave register usage in all others.

Used compiler:

Target: x86_64-unknown-linux-gnu
Configured with: ../gcc/configure --enable-languages=c,c++,fortran --disable-bootstrap --prefix=/export/users/ienkovic/ --disable-libsanitizer
Thread model: posix
gcc version 5.0.0 20150217 (experimental) (GCC)


---


### compiler : `gcc`
### title : `Improve register allocation for aarch64_*_sisd_or_int<mode>3 patterns`
### open_at : `2015-02-20T14:02:51Z`
### last_modified_date : `2023-05-16T17:57:01Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=65139
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `unknown`
### severity : `enhancement`
### contents :
Following discussion in http://thread.gmane.org/gmane.comp.gcc.patches/336162 , review usage of early clobber in aarch64_lshr_sisd_or_int_≤mode>3, aarch64_ashr_sisd_or_int_≤mode>3, and, maybe, other patterns.  Convert them to use (match_scratch) and compare quality of generated code between the two approaches.

In theory, (match_scratch) should give more freedom to RA, but this requires double-checking.


---


### compiler : `gcc`
### title : `[C++11] missing devirtualization for virtual base in  "final" classes`
### open_at : `2015-02-20T17:36:54Z`
### last_modified_date : `2019-07-08T09:52:26Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=65143
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `c++`
### version : `4.9.2`
### severity : `enhancement`
### contents :
When a class is marked final, it can devirtualize access to all base classes as its layout is known. This is missing in gcc. 

struct A
{
  int i();
};

struct B : public virtual A
{
  int get()
  {
    return A::i() + 1;
  }
};

struct C final : public B
{
  int get()
  {
    return A::i() + 2;
  }
};

int foo(C& c)
{  
  return c.get(); // Need not go via vtable pointer as class C is final
}

int foo(B& b2)
{
  return b2.get(); // This has to go via vtable as most derived class can change the location of A
}
  
Assembly: Both do virtual dispatch

foo(C&):
	subq	$8, %rsp
	movq	(%rdi), %rax
	addq	-24(%rax), %rdi
	call	one::A::i()
	addq	$8, %rsp
	addl	$2, %eax
	ret
foo(B&):
	subq	$8, %rsp
	movq	(%rdi), %rax
	addq	-24(%rax), %rdi
	call	one::A::i()
	addq	$8, %rsp
	addl	$1, %eax
	ret

Complete example:
gcc: http://goo.gl/U4KEvj
clang: http://goo.gl/PpQCkd  -- Clang does this optimization


---


### compiler : `gcc`
### title : `static initialization via intel intrinsics`
### open_at : `2015-02-24T22:02:41Z`
### last_modified_date : `2021-08-15T06:30:15Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=65197
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `target`
### version : `5.0`
### severity : `normal`
### contents :
I am compiling the following with: g++ -std=gnu++11 -Ofast

#include <x86intrin.h>
extern const __m128i x = { -1, 0 };
extern const __m128i y = _mm_set_epi64x (0, -1);

While x becomes a nice constant in .rodata, y is initialized by _GLOBAL__sub_I_x (copying a constant that is in .rodata). For this specific case, marking _mm_set_epi64x as constexpr gives y the same treatment as x, and I believe we should do that, i.e. mark all intrinsics that can be constexpr in C++11/C++14. However, I believe we are missing an optimization in the general case that would notice (late, after many optimizations) when the initialization function has become unnecessary.

Some possibly related bugs: PR4131, PR18399, PR24928, PR37949.


---


### compiler : `gcc`
### title : `vectorized version of loop is removed, dependence analysis fails for *&a[i] vs a[j]`
### open_at : `2015-02-25T14:01:31Z`
### last_modified_date : `2022-03-29T12:57:59Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=65206
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `5.0`
### severity : `normal`
### contents :
I noticed that vectorized version of loop is deleted although compiler reports that it was successfully vectorized:
t1.c:7:3: note: LOOP VECTORIZED

but after we can see in vect-dump:

Removing basic block 4
basic block 4, loop depth 1
 pred:       45
# i_16 = PHI <i_73(45)>
# ivtmp_15 = PHI <ivtmp_76(45)>
# vectp_a1.11_116 = PHI <vectp_a1.12_114(45)>
# vectp_a2.19_125 = PHI <vectp_a2.20_123(45)>
# vectp_a3.22_130 = PHI <vectp_a3.23_128(45)>
# vectp_a1.25_136 = PHI <vectp_a1.26_134(45)>
# vectp_a3.34_147 = PHI <vectp_a3.35_145(45)>
# ivtmp_38 = PHI <0(45)>
vect__5.13_118 = MEM[(float *)vectp_a1.11_116];
_5 = a1[i_16];
_31 = &a2[i_16];
vect__ifc__32.14_122 = VEC_COND_EXPR <vect__5.13_118 >= vect_cst_.15_119, vect_cst_.16_120, vect_cst_.17_121>;
_ifc__32 = _5 >= x_6(D) ? 4294967295 : 0;
vect__7.18_127 = MASK_LOAD (vectp_a2.19_125, 0B, vect__ifc__32.14_122);
_7 = 0.0;
_33 = &a3[i_16];
vect__8.21_132 = MASK_LOAD (vectp_a3.22_130, 0B, vect__ifc__32.14_122);
_8 = 0.0;
vect__9.24_133 = vect__7.18_127 + vect__8.21_132;
_9 = _7 + _8;
_34 = &a1[i_16];
MASK_STORE (vectp_a1.25_136, 0B, vect__ifc__32.14_122, vect__9.24_133);
vect__11.27_140 = vect_cst_.28_37 + vect_cst_.29_139;
_11 = x_6(D) + 1.0e+0;
_35 = &a3[i_16];
vect__ifc__36.30_144 = VEC_COND_EXPR <vect__5.13_118 >= vect_cst_.31_141, vect_cst_.32_142, vect_cst_.33_143>;
_ifc__36 = _5 >= x_6(D) ? 0 : 4294967295;
...

Test and compile options will be attached.


---


### compiler : `gcc`
### title : `[SH] Improve comparisons followed by a negated cstore`
### open_at : `2015-02-28T09:23:57Z`
### last_modified_date : `2023-10-22T02:52:59Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=65250
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `5.0`
### severity : `normal`
### contents :
The following example

bool test (int value)
{
  switch(value)
  {
    case 0:
    case 1:
    case 2:
      return true;
    default:
      return false;
  }
}

with -O2 -m4 compiles to:
        mov     #2,r1
        cmp/hi  r1,r4
        mov     #-1,r0
        rts
	negc    r0,r0

On SH4 there is no movrt, so it's better to do that as:
        mov     #2,r1
        cmp/hs  r4,r2
        rts
        movt    r0

..which is just inverting the comparison.


Combine tries the following pattern:

Failed to match this instruction:
(parallel [
        (set (reg:SI 168)
            (leu:SI (reg:SI 4 r4 [ value ])
                (const_int 2 [0x2])))
        (set (reg:SI 147 t)
            (const_int 1 [0x1]))
        (use (reg:SI 169))
    ])

..which is a combination of the inverted comparison and the expanded movrt (via negc), which always sets T = 1.

A treg_set_expr pattern like the following could be added:

(define_insn_and_split "*"
  [(set (match_operand:SI 0 "arith_reg_dest")
        (match_operand 1 "treg_set_expr_not_const01"))
   (set (reg:SI T_REG) (const_int 1))
   (use (match_operand:SI 2 "arith_reg_operand"))]
 ...)

which would then split out the comparison insn and a trailing sett.  If the sett is a dead store it will (should) get eliminated afterwards.

However, before that, the initial comparison and cstore expansion should be investigated.


---


### compiler : `gcc`
### title : `[SH] Use rotcl for bit reversals`
### open_at : `2015-03-01T20:45:53Z`
### last_modified_date : `2021-08-28T03:51:49Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=65266
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `target`
### version : `5.0`
### severity : `enhancement`
### contents :
The following examples are small bit reversals:

unsigned int test1 (unsigned int a)
{
  return ((a & 1) << 1) | ((a >> 1) & 1);
}

unsigned int test2 (unsigned int a)
{
  return ((a & 1) << 2) | (((a >> 1) & 1) << 1) | ((a >> 2) & 1);
}

unsigned int test3 (unsigned int a)
{
  return ((a & 1) << 3) | (((a >> 1) & 1) << 2) | (((a >> 2) & 1) << 1)
         | (((a >> 3) & 1) << 0);
}

where test3 currently compiles to:
        mov     r4,r0
        mov     #1,r2
        tst     #8,r0
        and     r4,r2
        movt    r1
        mov     r2,r0
        shll2   r0
        tst     r1,r1
        mov     r0,r1
        mov     r4,r0
        and     #2,r0
        rotcl   r1
        add     r0,r0
        mov     r0,r2
        mov     r4,r0
        or      r1,r2
        tst     #4,r0
        mov     #-1,r1
        mov     r2,r0
        negc    r1,r1
        add     r1,r1
        rts
        or      r1,r0

where a minimal sequence would be:
        shlr    r4
        movt    r0
        shlr    r4
        rotcl   r0
        shlr    r4
        rotcl   r0
        shlr    r4
        rotcl   r0


For example, combine tries the following pattern:

Failed to match this instruction:
(set (reg:SI 186 [ D.2006 ])
    (ior:SI (ior:SI (and:SI (ashift:SI (reg/v:SI 176 [ a ])
                                       (const_int 1 [0x1]))
                            (const_int 4 [0x4]))
                    (zero_extract:SI (reg/v:SI 176 [ a ])
                                     (const_int 1 [0x1])
                                     (const_int 3 [0x3])))
             (and:SI (ashift:SI (reg/v:SI 176 [ a ])
                                (const_int 3 [0x3]))
                     (const_int 8 [0x8]))))

A predicate that accepts IOR chains of single bit selections (via zero_extract or shift-and) could be used to capture the sequence during combine and then smash it in split1.

Possibly related: PR 65265, PR 63321.


---


### compiler : `gcc`
### title : `Potential optimization issue with 'tree-loop-vectorize'`
### open_at : `2015-03-06T16:16:31Z`
### last_modified_date : `2021-08-23T06:44:35Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=65335
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.2`
### severity : `enhancement`
### contents :
When I enable the tree-loop-vectorize optimization I'm seeing some behavior that I don't understand...

Here is a minimized test case that highlights the scenario:


typedef long unsigned int size_t;
extern void *malloc (size_t __size);

int main(){

    unsigned int a = 2;
    unsigned int *buffer = malloc(10000 * sizeof(*buffer));

    for (int i = 0; i < 10000; i++){
        if ((i % 1000) == 0){
            a = a * a * a * a * a;
        }
        buffer[i] = a;
    }

    return buffer[999];
}


When compiled with the option disabled (xgcc -save-temps -m32 -Wall -Wextra -std=c99 -O3 -fno-tree-loop-vectorize -S -masm=intel test.c) the following code is produced:

	mov	ebx, 2           ; a = 2
	mov	edi, 274877907
	sub	esp, 20
	push	40000
	call	malloc
	add	esp, 16
	mov	esi, eax         ; buffer = malloc(...)
	xor	ecx, ecx         ; i = 0
	.p2align 4,,10
	.p2align 3
.L3:
	mov	eax, ecx
	imul	edi
	mov	eax, ecx
	sar	eax, 31
	sar	edx, 6
	sub	edx, eax
	imul	edx, edx, 1000 
	cmp	ecx, edx
	jne	.L2              ; if ((i % 1000) == 0) {
	mov	eax, ebx
	imul	eax, ebx
	imul	eax, eax
	imul	ebx, eax         ; a = a * a * a * a * a; }
.L2:
	mov	DWORD PTR [esi+ecx*4], ebx ; buffer[i] = a
	add	ecx, 1           ; i++
	cmp	ecx, 10000
	jne	.L3              ; continue if i < 10000
        ...

When the tree-loop-vectorize option is enabled (xgcc -save-temps -m32 -Wall -Wextra -std=c99 -O3 -ftree-loop-vectorize test.c -S -masm=intel), though, the following code is generated:

	mov	esi, 2           ; a = 2
	sub	esp, 20
	push	40000
	call	malloc
	add	esp, 16
	mov	edi, eax         ; buffer = malloc(...)
	xor	ecx, ecx         ; i = 0
	.p2align 4,,10
	.p2align 3
.L2:
	mov	ebx, esi
	mov	eax, 274877907
	imul	ecx
	mov	eax, ecx
	imul	ebx, esi
	sar	eax, 31
	sar	edx, 6
	imul	ebx, ebx
	sub	edx, eax
	imul	edx, edx, 1000
	imul	ebx, esi          ; a = a * a * a * a * a;
	cmp	ecx, edx
	cmove	esi, ebx          ; move new value if ((i % 1000) == 0)
	mov	DWORD PTR [edi+ecx*4], esi ; buffer[i] = a
	add	ecx, 1           ; i++
	cmp	ecx, 10000
	jne	.L2              ; continue if i < 10000


The main difference here is that the 'a * a * a * a * a' calculation is done every loop iteration instead of every 1000th, but a is only assigned the new value every 1000th time via the conditional move instruction.  It seems inefficient to do this, and from basic testing the code compiled without the tree-loop-vectorize optimization seems to run faster on my machine.

The "real" code that I derived this from has it worse - it uses 64-bit data types in a 32-bit binary, so there are several multiply instructions for each logical multiplication in the code, the stack gets used for storing some of the intermediate values, and after computing everything into some registers it just replaces those values with ones stored on the stack from previous iterations in the case where the modulus condition is not met.  :(

GCC version:

Using built-in specs.
COLLECT_GCC=xgcc
Target: x86_64-unknown-linux-gnu
Configured with: ./configure
Thread model: posix
gcc version 4.9.2 (GCC)

I've also reproduced the issue on gcc 4.9.2 20141224 (prerelease) from an Arch Linux distro and gcc 4.5.2-8ubuntu4 from a Ubuntu distro.

I'm happy to provide any other information needed.  Thanks!


---


### compiler : `gcc`
### title : `[SH] Implement bit counting built-in functions`
### open_at : `2015-03-10T07:57:13Z`
### last_modified_date : `2021-08-28T03:53:15Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=65373
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `5.0`
### severity : `enhancement`
### contents :
In linux/arch/sh/include/asm there's following code:

static inline unsigned long ffz(unsigned long word)
{
	unsigned long result;

	__asm__("1:\n\t"
		"shlr	%1\n\t"
		"bt/s	1b\n\t"
		" add	#1, %0"
		: "=r" (result), "=r" (word)
		: "0" (~0L), "1" (word)
		: "t");
	return result;
}

static inline unsigned long __ffs(unsigned long word)
{
	unsigned long result;

	__asm__("1:\n\t"
		"shlr	%1\n\t"
		"bf/s	1b\n\t"
		" add	#1, %0"
		: "=r" (result), "=r" (word)
		: "0" (~0L), "1" (word)
		: "t");
	return result;
}

The respective GCC built-in functions such as __builtin_ffs should be implemented.  The code snippets above result in quite compact code, which could be used for -Os.

Otherwise, it could be interesting to see whether it makes sense to expand some inline code as found in include/longlong.h.


---


### compiler : `gcc`
### title : `[SH] Tail call optimization not done for libcalls`
### open_at : `2015-03-10T08:03:20Z`
### last_modified_date : `2021-08-16T06:40:03Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=65374
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `5.0`
### severity : `normal`
### contents :
This example function:

unsigned int test (unsigned int x)
{
  return __builtin_clz (x);
}

Compiled with -m4 -O2:

_test:
        mov.l   .L3,r0
        sts.l   pr,@-r15
        jsr     @r0
        nop
        lds.l   @r15+,pr
        rts	
        nop
.L4:
        .align 2
.L3:
        .long   ___clzsi2


For some reason, tail call optimization is not performed in this case.


---


### compiler : `gcc`
### title : `missed store motion for conditionally updated pointer in loop`
### open_at : `2015-03-11T16:12:14Z`
### last_modified_date : `2021-07-07T11:58:58Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=65391
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `5.0`
### severity : `normal`
### contents :
When compiling for powerpc64 or powerpc64le with -O3, a load and store of *o_ptr is done inside the loop. 

If you remove the if statement and make the update unconditional, then the load goes away and the store is deferred until after the loop.

If you remove the __restrict__ keywords, then the store remains in the loop in either case as expected. However the load is still done in the loop if the update is conditional.

void compute_object_gain(long * __restrict__ p_ptr, long * __restrict__ o_ptr, long g_order)
{
    long a_binding;
    *o_ptr = 0;
    while(*p_ptr!=0) {
       a_binding = *p_ptr;
       if(a_binding <= g_order)
          *o_ptr += a_binding;
        p_ptr++;
    }
}

This behavior is consistent on 4.1, 4.5, 4.6, 4.7, 4.8, and 5.0 (trunk 220806).


---


### compiler : `gcc`
### title : `"Short local string array" optimization doesn't happen if string has NULs`
### open_at : `2015-03-12T19:08:25Z`
### last_modified_date : `2021-10-02T18:53:58Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=65410
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.7.2`
### severity : `enhancement`
### contents :
void f(char *);
void g() {
        char buf[12] = "1234567890";
        f(buf);
}

In the above example, "gcc -O2" creates buf[12] with immediate stores:

        subq    $24, %rsp
        movabsq $4050765991979987505, %rax
        movq    %rsp, %rdi
        movq    %rax, (%rsp)
        movl    $12345, 8(%rsp)
        call    f
        addq    $24, %rsp
        ret

But if buf[] definition has \0 anywhere (for example, at the end where it does not even change the semantics of the code), optimization is not happening, gcc allocates a constant string and copies it into buf[]:

void f(char *);
void g() {
        char buf[12] = "1234567890\0";
        f(buf);
}

        .section        .rodata
.LC0:
        .string "1234567890"
        .string ""

        .text
g:
        subq    $24, %rsp
        movq    .LC0(%rip), %rax
        movq    %rsp, %rdi
        movq    %rax, (%rsp)
        movl    .LC0+8(%rip), %eax
        movl    %eax, 8(%rsp)
        call    f
        addq    $24, %rsp
        ret


---


### compiler : `gcc`
### title : `sequence of ifs not turned into a switch statement`
### open_at : `2015-03-12T21:33:06Z`
### last_modified_date : `2021-06-04T21:41:15Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=65412
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.2`
### severity : `enhancement`
### contents :
Created attachment 35023
files 1.c (source), 1.s (gcc assembly), 2.s (clang assembly)

Consider the following code:

void f(int x)
{
   if (x == 0) f0();
   else if (x == 1) f1();
   else if (x == 2) f2();
   else if (x == 3) f3();
   else if (x == 4) f4();
   else if (x == 5) f5();
}

gcc-4.9.2 doesn't optimize ifs to decision tree, jump table or something (see 1.s in attach). clang does (2.s in attach, jump table).

Maybe you could improve that?


---


### compiler : `gcc`
### title : `inefficient code returning float aggregates on powepc64le`
### open_at : `2015-03-13T23:24:20Z`
### last_modified_date : `2023-05-09T03:23:51Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=65421
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `5.0`
### severity : `normal`
### contents :
When returning homogeneous floating-point aggregates, gcc first loads the aggregate into GPRs, then saves it to the save area, and then copies the aggregate from the GPRs to the floating registers used to return it to the caller.  Clang emits much more efficient code (see below).

$ cat x.c && ./gcc/xgcc -B./gcc -O3 -o/dev/tty -S x.c
typedef struct { double a[4]; } A;

A foo (const A *a) { return *a; }

	.file	"x.c"
	.machine power8
	.abiversion 2
	.section	".toc","aw"
	.section	".text"
	.align 2
	.p2align 4,,15
	.globl foo
	.type	foo, @function
foo:
	ld 7,0(3)
	ld 8,8(3)
	ld 10,16(3)
	ld 9,24(3)
	std 7,-64(1)
	std 8,-56(1)
	std 10,-48(1)
	std 9,-40(1)
	lfd 2,-56(1)
	lfd 1,-64(1)
	ori 2,2,0
	lfd 3,-48(1)
	lfd 4,-40(1)
	blr
	.long 0
	.byte 0,0,0,0,0,0,0,0
	.size	foo,.-foo
	.ident	"GCC: (GNU) 5.0.0 20150310 (experimental)"
	.section	.note.GNU-stack,"",@progbits


Clang emits:
	.text
	.abiversion 2
	.file	"-"
	.globl	foo
	.align	2
	.type	foo,@function
foo:
	lfd 1, 0(3)
	lfd 2, 8(3)
	lfd 3, 16(3)
	lfd 4, 24(3)
	blr
	.long	0
	.quad	0
.Ltmp0:
	.size	foo, .Ltmp0-foo


	.ident	"clang version 3.6.0 (trunk 215935)"


---


### compiler : `gcc`
### title : `gcc does not recognize byte swaps implemented as loop.`
### open_at : `2015-03-14T14:31:29Z`
### last_modified_date : `2019-12-08T20:12:43Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=65424
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `5.0`
### severity : `enhancement`
### contents :
Created attachment 35034
endianess-aware reading / writing macros

gcc (r221432) is able to recognize the following code and implements it with either a bswap or a straight load on x86.

    #include <stdint.h>

    extern uint32_t
    rbe32(const uint8_t a[4])
    {
        uint32_t x = 0;

        x |= a[0] << 24;
        x |= a[1] << 16;
        x |= a[2] <<  8;
        x |= a[3] <<  0;

        return x;
    }

    extern uint32_t
    rle32(const uint8_t a[4])
    {
        uint32_t x = 0;

        x |= a[0] <<  0;
        x |= a[1] <<  8;
        x |= a[2] << 16;
        x |= a[3] << 24;

        return x;
    }

it isn't able to recognize the following two functions which yield identical results:

    extern uint32_t
    rle32(const uint8_t a[4])
    {
        int i;
        uint32_t x = 0;

        for (i = 0; i < 4; i++)
                x |= a[i] << 8 * i;

        return x;
    }

    extern uint32_t
    rbe32(const uint8_t a[4])
    {
        int i;
        uint32_t x = 0;

        for (i = 0; i < 4; i++)
                x |= a[i] << 8 * (3 - i);

        return x;
    }

It would be great if gcc was able to recognize these implementations of endianess-aware reads; this kind of code is produced by macros I use to generate a bunch of read / write functions for differently sized types. Attached is a file containing the macros I want to use.


---


### compiler : `gcc`
### title : `Recognize byte-swaps when writing to buffers`
### open_at : `2015-03-14T18:16:52Z`
### last_modified_date : `2021-12-28T06:41:10Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=65426
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `5.0`
### severity : `enhancement`
### contents :
Created attachment 35036
Various instances of the aforementioned pattern

It would be great if gcc could recognize code like this:

    static inline void
    wm32(uint8_t a[4], uint32_t x)
    {
        a[0] = x >> 24;
        a[1] = x >> 16;
        a[2] = x >>  8;
        a[3] = x >>  0;
    }

and turn it into a single unaligned write (and perhaps a byte swap on platforms where this is supported). This kind of code appears when one tries to write marshalling code in a portable fashion.

Attached is a file containing various instances of this pattern.


---


### compiler : `gcc`
### title : `pass_lim misses support for predicated code motion`
### open_at : `2015-03-16T14:27:54Z`
### last_modified_date : `2022-01-06T00:02:35Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=65440
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `5.0`
### severity : `enhancement`
### contents :
tree-ssa-loop-im.c ( https://gcc.gnu.org/git/?p=gcc.git;a=blob;f=gcc/tree-ssa-loop-im.c;h=9aba79ba776944ec6fba8459354deabe8c126b75;hb=HEAD#l74 ):
...
/* TODO:  Support for predicated code motion.  I.e.

   while (1)
     {
       if (cond)
	 {
	   a = inv;
	   something;
	 }
     }

   Where COND and INV are invariants, but evaluating INV may trap or be
   invalid from some other reason if !COND.  This may be transformed to

   if (cond)
     a = inv;
   while (1)
     {
       if (cond)
	 something;
     }  */
...


---


### compiler : `gcc`
### title : `pass_lim misses support for exit-first loops`
### open_at : `2015-03-16T14:57:59Z`
### last_modified_date : `2021-08-29T00:50:43Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=65442
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `5.0`
### severity : `enhancement`
### contents :
Consider test.c:
...
#include <string.h>

const char *something (void);

size_t
f (unsigned int n)
{
  const char *s = something ();
  size_t sum = 0;
  size_t t;
  unsigned int i;

  if (!s)
    return 0;

  for (i = 0; i < n; ++i)
    {
      t = strlen (s);
      sum += t;
    }

  return sum;
}
...

The resulting code with -O2 -fno-tree-ch from the optimized dump is: 
...
f (unsigned int n)
{
  unsigned int i;
  size_t t;
  size_t sum;
  const char * s;
  size_t _3;

  <bb 2>:
  s_6 = something ();
  if (s_6 == 0B)
    goto <bb 6>;
  else
    goto <bb 3>;

  <bb 3>:
  # sum_14 = PHI <0(2)>
  # i_12 = PHI <0(2)>
  goto <bb 5>;

  <bb 4>:
  t_9 = strlen (s_6);
  sum_10 = sum_1 + t_9;
  i_11 = i_2 + 1;

  <bb 5>:
  # sum_1 = PHI <sum_14(3), sum_10(4)>
  # i_2 = PHI <i_12(3), i_11(4)>
  if (i_2 != n_8(D))
    goto <bb 4>;
  else
    goto <bb 6>;

  <bb 6>:
  # _3 = PHI <0(2), sum_1(5)>
  return _3;

}
...

The strlen is not taken out of the loop. It could be taken out of the loop, provided it's guarded with the loop condition.

This PR is similar to PR65440. There the strlen is conditional in the loop body, which is entered unconditionally. Here the strlen is unconditional in the loop body, which is entered conditionally.


---


### compiler : `gcc`
### title : `Bad optimization in -O3 due to if-conversion and/or unrolling`
### open_at : `2015-03-20T12:01:00Z`
### last_modified_date : `2021-08-14T23:12:29Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=65492
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `5.0`
### severity : `normal`
### contents :
After investigating a loop using SSE intrinsics that was significantly faster in clang than in gcc, I discovered gcc had the same performance as clang in -O2, and only performed signficantly worse in -O3.

Disabling all the switches mentioned in the documentation as activates by -O3 (or enabling them for -O2), doesn't fully account for the difference, but the switch -f(no-)tree-loop-vectorize accounts for roughly half of it.

I have attached the files I used to test it. Using gcc -O2 or clang -O2 or -O3, it times in at 1.8s on my machine. Using g++ (4.9 or 5.0) -O3 it times in at 2.5s. Using -O3 -fno-tree-loop-vectorize it runs in 2.3s, and -O2 -ftree-vectorize at 2.25s.

Using callgrind, it seems the performance difference is mainly spend on the accessing integers in the vector union.


---


### compiler : `gcc`
### title : `g++ string array in struct crash`
### open_at : `2015-03-21T09:51:54Z`
### last_modified_date : `2022-01-07T00:48:26Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=65503
### status : `RESOLVED`
### tags : `compile-time-hog, missed-optimization`
### component : `c++`
### version : `4.8.1`
### severity : `normal`
### contents :
Created attachment 35082
file produced by >gcc -v -save-temps -Wall -Wextra c.cc

This crashes mingw g++ (GCC) 4.8.1 XP home SP3
Ubuntu 4.8.1-2ubuntu1~12.04 with s[99999] it hangs.

>gcc c.cc  -Wall -Wextra
>gcc c.cc  -Wall -Wextra -fno-strict-aliasing -fwrapv

#include <string>
struct T {
   std::string s[4065]; // 4064 is OK
};
int main() {
   T m = {"x", "y"};
} 


>gcc -v -save-temps -Wall -Wextra c.cc
Using built-in specs.
COLLECT_GCC=gcc
COLLECT_LTO_WRAPPER=c:/mingw/bin/../libexec/gcc/mingw32/4.8.1/lto-wrapper.exe
Target: mingw32
Configured with: ../gcc-4.8.1/configure --prefix=/mingw --host=mingw32 --build=mingw32 --without-pic --enable-shared --e
nable-static --with-gnu-ld --enable-lto --enable-libssp --disable-multilib --enable-languages=c,c++,fortran,objc,obj-c++
,ada --disable-sjlj-exceptions --with-dwarf2 --disable-win32-registry --enable-libstdcxx-debug --enable-version-specific
-runtime-libs --with-gmp=/usr/src/pkg/gmp-5.1.2-1-mingw32-src/bld --with-mpc=/usr/src/pkg/mpc-1.0.1-1-mingw32-src/bld --
with-mpfr= --with-system-zlib --with-gnu-as --enable-decimal-float=yes --enable-libgomp --enable-threads --with-libiconv
-prefix=/mingw32 --with-libintl-prefix=/mingw --disable-bootstrap LDFLAGS=-s CFLAGS=-D_USE_32BIT_TIME_T
Thread model: win32
gcc version 4.8.1 (GCC)
COLLECT_GCC_OPTIONS='-v' '-save-temps' '-Wall' '-Wextra' '-mtune=generic' '-march=pentiumpro'
 c:/mingw/bin/../libexec/gcc/mingw32/4.8.1/cc1plus.exe -E -quiet -v -iprefix c:\mingw\bin\../lib/gcc/mingw32/4.8.1/ c.cc
 -mtune=generic -march=pentiumpro -Wall -Wextra -fpch-preprocess -o c.ii
ignoring duplicate directory "c:/mingw/lib/gcc/../../lib/gcc/mingw32/4.8.1/include/c++"
ignoring duplicate directory "c:/mingw/lib/gcc/../../lib/gcc/mingw32/4.8.1/include/c++/mingw32"
ignoring duplicate directory "c:/mingw/lib/gcc/../../lib/gcc/mingw32/4.8.1/include/c++/backward"
ignoring duplicate directory "c:/mingw/lib/gcc/../../lib/gcc/mingw32/4.8.1/include"
ignoring duplicate directory "c:/mingw/lib/gcc/../../lib/gcc/mingw32/4.8.1/../../../../include"
ignoring duplicate directory "/mingw/include"
ignoring duplicate directory "c:/mingw/lib/gcc/../../lib/gcc/mingw32/4.8.1/include-fixed"
ignoring duplicate directory "c:/mingw/lib/gcc/../../lib/gcc/mingw32/4.8.1/../../../../mingw32/include"
ignoring duplicate directory "/mingw/include"
#include "..." search starts here:
#include <...> search starts here:
 c:\mingw\bin\../lib/gcc/mingw32/4.8.1/include/c++
 c:\mingw\bin\../lib/gcc/mingw32/4.8.1/include/c++/mingw32
 c:\mingw\bin\../lib/gcc/mingw32/4.8.1/include/c++/backward
 c:\mingw\bin\../lib/gcc/mingw32/4.8.1/include
 c:\mingw\bin\../lib/gcc/mingw32/4.8.1/../../../../include
 c:\mingw\bin\../lib/gcc/mingw32/4.8.1/include-fixed
 c:\mingw\bin\../lib/gcc/mingw32/4.8.1/../../../../mingw32/include
End of search list.
COLLECT_GCC_OPTIONS='-v' '-save-temps' '-Wall' '-Wextra' '-mtune=generic' '-march=pentiumpro'
 c:/mingw/bin/../libexec/gcc/mingw32/4.8.1/cc1plus.exe -fpreprocessed c.ii -quiet -dumpbase c.cc -mtune=generic -march=p
entiumpro -auxbase c -Wall -Wextra -version -o c.s
GNU C++ (GCC) version 4.8.1 (mingw32)
        compiled by GNU C version 4.8.1, GMP version 5.1.2, MPFR version 3.1.2, MPC version 1.0.1
GGC heuristics: --param ggc-min-expand=99 --param ggc-min-heapsize=130944
GNU C++ (GCC) version 4.8.1 (mingw32)
        compiled by GNU C version 4.8.1, GMP version 5.1.2, MPFR version 3.1.2, MPC version 1.0.1
GGC heuristics: --param ggc-min-expand=99 --param ggc-min-heapsize=130944
Compiler executable checksum: 1ebc2a6f92fbd3aadc367a20a63fdf9f


---


### compiler : `gcc`
### title : `tailcall not optimized away`
### open_at : `2015-03-23T23:56:37Z`
### last_modified_date : `2023-03-31T11:56:50Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=65534
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `5.0`
### severity : `normal`
### contents :
Maybe this could be optimized by a thunk or by creating the alias automatically or the like? Or is tailcall supposed to do this already?

trunk@221345
$ gcc -Os -c missed-opt.c -o missed-opt.plain.o
$ gcc -Os -c missed-opt.c -o missed-opt.manual.o -DOPTIMIZE_MANUALLY
$ size missed-opt.*.o
   text	   data	    bss	    dec	    hex	filename
     86	      0	      0	     86	     56	missed-opt.manual.o
    104	      0	      0	    104	     68	missed-opt.plain.o

$ cat missed-opt.c ; echo EOF
static int fd = -1;
extern void dummy0(void);
extern void dummy1(int);
extern void setutent(void) __attribute__ ((__nothrow__ ));
extern __typeof (setutent) setutent __asm__ ("" "__GI_setutent")
	__attribute__ ((visibility ("hidden")));
extern void getutent(void) __attribute__ ((__nothrow__ ));
extern __typeof (getutent) getutent __asm__ ("" "__GI_getutent")
	__attribute__ ((visibility ("hidden")));
static void __setutent_unlocked(void) {
	if (fd < 0) {
		dummy0();
		if (fd < 0) {
			dummy0();
			if (fd < 0)
				return;
		}
		return;
	}
	dummy1(fd);
}
#ifndef OPTIMIZE_MANUALLY
void setutent(void) {
	((void)0);
	__setutent_unlocked();
	((void)0);
}
#else
extern __typeof (__setutent_unlocked) setutent
	__attribute__ ((alias ("__setutent_unlocked")));
#endif
extern __typeof (setutent) __EI_setutent __asm__("" "setutent");
extern __typeof (setutent) __EI_setutent
	__attribute__((alias ("" "__GI_setutent")));

static void __getutent_unlocked(void) {
	if (fd < 0)
		__setutent_unlocked();
}

#ifndef OPTIMIZE_MANUALLY
void getutent(void) {
	((void)0);
	__getutent_unlocked();
	((void)0);
}
#else
extern __typeof (__getutent_unlocked) getutent
	__attribute__ ((alias ("__getutent_unlocked")));
#endif
extern __typeof (getutent) __EI_getutent __asm__("" "getutent");
extern __typeof (getutent) __EI_getutent
	__attribute__((alias ("" "__GI_getutent")));

EOF


---


### compiler : `gcc`
### title : `G++ should use default constructor for {}-init when possible`
### open_at : `2015-03-26T20:19:16Z`
### last_modified_date : `2022-01-07T05:23:03Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=65591
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `c++`
### version : `5.0`
### severity : `normal`
### contents :
From Mikhail Maltsev's comment 5 on Bug #65154:

But it reveals some latent bug (PR65503). In the following case (after applying the patch):

struct ss {
    ss() {};
};
struct C {
      ss s[1000];
};
int main() {
      C cs[5]{};
}

We'll get 1000 calls to ss() in main instead of calling default c-tor of struct C. (which is probably not what we want).

-----

I agree that we want to call the default constructor in this case, and let the inliner decide from there.  This is not the same issue as bug 65503.


---


### compiler : `gcc`
### title : `Redundant cmp with zero instruction in loop for x86 target.`
### open_at : `2015-04-01T12:33:54Z`
### last_modified_date : `2022-01-10T00:08:13Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=65651
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `5.0`
### severity : `normal`
### contents :
Compile attached bad.c with "-O2" option only we can see that redundant cmp with zero instruction is generated:
	subl	%r9d, %eax
	cmpl	$0, %eax
	je	.L10
 but for slightly changed good.c there is no such redundancy:
	subl	%r9d, %eax
	je	.L10

The problem phase is combine.
For good case it does combining:
Trying 37 -> 38:
Successfully matched this instruction:
(parallel [
        (set (reg:CCZ 17 flags)
            (compare:CCZ (minus:SI (reg:SI 121 [ D.2002 ])
                    (reg/v:SI 115 [ med ]))
                (const_int 0 [0])))
        (set (reg/v:SI 101 [ n ])
            (minus:SI (reg:SI 121 [ D.2002 ])
                (reg/v:SI 115 [ med ])))
    ])
allowing combination of insns 37 and 38
original costs 4 + 4 = 8
replacement cost 0
but for bad case it is not performed:
Trying 37 -> 38:
Failed to match this instruction:
(set (reg:CC 17 flags)
    (compare:CC (minus:SI (reg:SI 120 [ D.2006 ])
            (reg/v:SI 114 [ med ]))
        (const_int 0 [0])))

Note that this test-case extracted from one of hot loop in bzip2 (mainQSort3).


---


### compiler : `gcc`
### title : `Missed loop optimization with asm`
### open_at : `2015-04-11T06:00:52Z`
### last_modified_date : `2021-09-13T21:33:39Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=65741
### status : `NEW`
### tags : `inline-asm, missed-optimization`
### component : `tree-optimization`
### version : `5.0`
### severity : `enhancement`
### contents :
Trimming the code down to minimal:

int main()
{
   int lo;

   for(int x=0; x < 10; x++)
   {
      asm ( "# asm here" : "=r" (lo));
   }

   return lo;
}

Compile with: c++.exe -O2 -m64 -S loop.cpp
x86_64-w64-mingw32 5.0.0

The -O2 optimization correctly detects that the asm statement can be moved outside the loop (and moves it).  However, it then leaves an empty loop:

        movl    $10, %edx
/APP
 # 7 "loop.cpp" 1
        #
 # 0 "" 2
        .p2align 4,,10
/NO_APP
.L2:
        subl    $1, %edx
        jne     .L2

With the asm moved, the .L2 loop serves no purpose.  I expected it to get optimized out.

Even more perplexing is that if the asm has 2 outputs, it *doesn't* get moved outside the loop:

int main()
{
   int hi, lo;

   for(int x=0; x < 10; x++)
   {
      asm  ( "# asm here" : "=r" (lo), "=r" (hi));
   }

   return hi * lo;
}

        movl    $10, %edx
        .p2align 4,,10
.L2:
/APP
 # 7 "loop.cpp" 1
        # asm here
 # 0 "" 2
/NO_APP
        subl    $1, %edx
        jne     .L2

I expected this asm to get moved just like the other one did.


---


### compiler : `gcc`
### title : `[i386] Incorrect tail call inhibition logic on i386 (32-bit)`
### open_at : `2015-04-13T16:26:38Z`
### last_modified_date : `2019-06-15T00:59:20Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=65753
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `unknown`
### severity : `normal`
### contents :
i386.c contains the following comment (line 5448 as of this writing):

   /* If we are generating position-independent code, we cannot sibcall
      optimize any indirect call, or a direct call to a global function,
      as the PLT requires %ebx be live. (Darwin does not have a PLT.)  */

And the subsequent code disables tail calls via function pointers. The claim in the comment that %ebx must be live for PLT use by indirect calls, and the corresponding code that inhibits sibcall, is wrong.

For PLT slots in the non-PIE main executable, %ebx is not required at all. PLT slots in PIE or shared libraries need %ebx, but a function pointer can never evaluate to such a PLT slot; it always evaluates to the nominal address of the function which is the same in all DSOs and therefore fundamentally cannot depend on the address of the GOT in the calling DSO.

Removing this incorrect check will significantly improve code generation in certain circumstances.


---


### compiler : `gcc`
### title : `after reload, the memrefs_conflict_p is unreliable?`
### open_at : `2015-04-16T05:59:57Z`
### last_modified_date : `2021-09-19T09:07:23Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=65783
### status : `UNCONFIRMED`
### tags : `internal-improvement, missed-optimization`
### component : `rtl-optimization`
### version : `unknown`
### severity : `normal`
### contents :
int f = -1;
int foo(int * pa)
{
  int a = 1;
  *(pa) = a;
  pa = pa + f;
  a = *(pa + 1);
  return a;
}

With -O2, the ARM's assembler is as follows:
foo:
        @ args = 0, pretend = 0, frame = 0
        @ frame_needed = 0, uses_anonymous_args = 0
        @ link register save eliminated.
        movw    r3, #:lower16:.LANCHOR0 @ 20    *arm_movsi_insn/4       [length = 4]
        mov     r2, #1  @ 6     *arm_movsi_insn/2       [length = 4]
        movt    r3, #:upper16:.LANCHOR0 @ 21    *arm_movt       [length = 4]
        str     r2, [r0]        @ 7     *arm_movsi_insn/6       [length = 4]
        ldr     r3, [r3]        @ 9     *arm_movsi_insn/5       [length = 4]
        add     r0, r0, r3, asl #2      @ 11    *arith_shiftsi/1        [length = 4]
        ldr     r0, [r0, #4]    @ 17    *arm_movsi_insn/5       [length = 4]
        bx      lr      @ 26    *arm_return     [length = 12]
        .size   foo, .-foo
        .global f
        .data
        .align  2

In sched1, insn 7 and insn 17 has true dependence, but in sched2, the true dependence between insn 7 and insn 17 is omitted.
It seems after reload, in function true_dependence_1, the memrefs_conflict_p is unreliable?


---


### compiler : `gcc`
### title : `unnecessary stack spills during complex numbers function calls`
### open_at : `2015-04-17T17:06:13Z`
### last_modified_date : `2023-05-15T07:03:20Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=65796
### status : `NEW`
### tags : `missed-optimization, ra`
### component : `rtl-optimization`
### version : `5.0`
### severity : `normal`
### contents :
following function calling cabsf exhibits poor performance when compiled with gcc:

#include <complex>
using namespace std;
void __attribute__((noinline)) v(int nCor, complex<float> * inp, complex<float> * out)
{
    for (int icorr = 0; icorr < nCor; icorr++) {
        float amp = abs(inp[icorr]);
        if (amp > 0.f) {
            out[icorr] = amp * inp[icorr];
        }   
        else {
            out[icorr] = 0.; 
        }   
    }

with gcc 4.9 and 5 (20150208) on x86_64 produces:
g++- test.cc -O2  -c -S

.L15:
	movss	4(%rsp), %xmm2
	addq	$8, %rbx
	addq	$8, %rbp
	movss	(%rsp), %xmm1
	mulss	%xmm0, %xmm2
	mulss	%xmm0, %xmm1
	movss	%xmm2, -8(%rbx)
	movss	%xmm1, -4(%rbx)
	cmpq	%r12, %rbx
	je	.L14
.L7:
	movss	0(%rbp), %xmm2
	movss	4(%rbp), %xmm1
	movss	%xmm2, 8(%rsp)
	movss	%xmm1, 12(%rsp)
	movq	8(%rsp), %xmm0
	movss	%xmm2, 4(%rsp)
	movss	%xmm1, (%rsp)
	call	cabsf
	pxor	%xmm3, %xmm3
	ucomiss	%xmm3, %xmm0
	ja	.L15


note the spills of xmm[12] onto the stack and reloading it into xmm0
instead of spilling to the stack one could use unpcklps to prepare xmm0

with a simple benchmark on 5000 floats this would speed up the function by about 30% on an intel core2 and an i5 which is quite significant given the expensive cabs call that is also done in it.


---


### compiler : `gcc`
### title : `Inefficient vector construction`
### open_at : `2015-04-21T13:56:01Z`
### last_modified_date : `2021-08-10T23:06:28Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=65832
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `6.0`
### severity : `normal`
### contents :
typedef int v4si __attribute__((vector_size(16)));

v4si foo (int i, int j, int k, int l)
{
  return (v4si) { i, j, k, l };
}

produces

        movl    %edx, -12(%rsp)
        movd    -12(%rsp), %xmm1
        movl    %ecx, -12(%rsp)
        movd    -12(%rsp), %xmm2
        movl    %edi, -12(%rsp)
        movd    -12(%rsp), %xmm0
        movl    %esi, -12(%rsp)
        movd    -12(%rsp), %xmm3
        punpckldq       %xmm2, %xmm1
        punpckldq       %xmm3, %xmm0
        punpcklqdq      %xmm1, %xmm0
        ret

as we spill everything to the stack we could as well use a vector load, thus
something like

        movl    %edx, -12(%rsp)
        movl    %ecx, -16(%rsp)
        movl    %edi, -20(%rsp)
        movl    %esi, -24(%rsp)
        movdqu  -12(%rsp), %xmm0
        ret


---


### compiler : `gcc`
### title : `SSE2 code for adding two structs is much worse at -O3 than at -O2`
### open_at : `2015-04-22T13:50:34Z`
### last_modified_date : `2023-08-26T23:37:10Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=65847
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `6.0`
### severity : `normal`
### contents :
On x86_64 I get decent code at -O2:

$ cat zplus.c
typedef struct { double a, b; } Z;
Z zplus(Z x, Z y) { return (Z){ x.a + y.a, x.b + y.b }; }
$ gcc -O2 -S -o - zplus.c
...
zplus:
.LFB0:
        .cfi_startproc
        addsd   %xmm3, %xmm1
        addsd   %xmm2, %xmm0
        ret
        .cfi_endproc
.LFE0:
...

but awful code at -O3:

$ gcc -O3 -S -o - zplus.c
...
zplus:
.LFB0:
        .cfi_startproc
        movq    %xmm0, -40(%rsp)
        movq    %xmm1, -32(%rsp)
        movq    %xmm2, -56(%rsp)
        movq    %xmm3, -48(%rsp)
        movupd  -40(%rsp), %xmm1
        movupd  -56(%rsp), %xmm0
        addpd   %xmm0, %xmm1
        movaps  %xmm1, -72(%rsp)
        movq    -72(%rsp), %rdx
        movq    -64(%rsp), %rax
        movq    %rdx, -72(%rsp)
        movsd   -72(%rsp), %xmm0
        movq    %rax, -72(%rsp)
        movsd   -72(%rsp), %xmm1
        ret
...

I see similar bad code generated by various versions of GCC, starting around version 4.8:
gcc-4.8 (Ubuntu 4.8.3-12ubuntu3) 4.8.3
gcc (Ubuntu 4.9.1-16ubuntu6) 4.9.1
gcc (GCC) 6.0.0 20150422 (experimental)


---


### compiler : `gcc`
### title : `SCEV / SCCP missing optimization: triangular numbers`
### open_at : `2015-04-23T04:52:16Z`
### last_modified_date : `2023-06-10T16:02:48Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=65855
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `5.1.0`
### severity : `enhancement`
### contents :
Created attachment 35388
triangle.c

If a register mode is available to avoid multiplication overflow, a loop that is calculating triangular numbers could be optimized to a multiplication:

uint64_t triangle(uint32_t n) {
uint64_t t = 0;
for (uint64_t i=1;i<=n;i++) t += i;
return t;
}

=>

uint64_t triangle_fast(uint32_t _n) {
uint64_t t, n = _n;
t = (n * (n + 1)) / 2;
return t;
}


---


### compiler : `gcc`
### title : `[MIPS] IRA/LRA issue: integers spilled to floating-point registers`
### open_at : `2015-04-23T16:04:26Z`
### last_modified_date : `2019-09-24T04:19:29Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=65862
### status : `UNCONFIRMED`
### tags : `missed-optimization, ra`
### component : `rtl-optimization`
### version : `5.1.1`
### severity : `normal`
### contents :
Following up the following thread:
https://gcc.gnu.org/ml/gcc/2015-04/msg00239.html

Here is a reduced testcase from the Linux kernel:

$ cat sort.c
int a, c;
int *b;
void
fn1(int p1, int *p2(void *, void *), void *p3(void *, void *, int)) {
  int n = c;
  for (;;) {
    a = 1;
    for (; a < n;) {
      p1 && p2(0, (int *) (p1 + 1));
      p3(0, b + p1, 0);
    }
  }
}

Spill/reload to/from FP reg should be triggerable with (tested on SVN rev. 222257):
$ mips-img-linux-gnu -mips32r6 -O2 sort.c 

Because of ALL_REGS assigned to most of allocnos, LRA uses FP regs freely. The class is preferred because of the equal cost between registers and memory. This likely happened because of the following fix:

2011-12-20  Vladimir Makarov  <vmakarov@redhat.com>                  
                                                                     
	PR target/49865
	* ira-costs.c (find_costs_and_classes): Prefer registers even 
	  if the memory cost is the same.                            
                                                                     
As Matthew already pointed out, one way to prevent this is through increasing the cost of moving between GP and FP registers for integral modes.

I briefly tested out Wilco's patch but it did not appear to have the same effect as changing the cost and I've seen a few ICEs when building the kernel.


---


### compiler : `gcc`
### title : `x_rtl.x_frame_offset not updated after frame related insn deleted`
### open_at : `2015-04-28T09:40:07Z`
### last_modified_date : `2021-12-19T00:26:51Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=65912
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `6.0`
### severity : `normal`
### contents :
given the following simple test.c

typedef unsigned long int uint64_t;
typedef __Uint8x8_t uint8x8_t;

typedef struct uint8x8x4_t
{
  uint8x8_t val[4];
} uint8x8x4_t;

__inline uint8x8_t
bar (uint64_t __a)
{
  return (uint8x8_t) __a;
}

uint8x8x4_t foo(uint8x8x4_t v1, uint8x8x4_t v2)
{
  return (uint8x8x4_t){{bar(0), bar(0), bar(0), bar(0)}};
}

on aarch64, compile it with "./cc1-aarch64 -std=c99 -Wall -O3 -ftree-vectorizer-verbose=3"

foo:
        movi    v0.2s, 0
        sub     sp, sp, #128  <== useless stack adjustment
        add     sp, sp, 128   <== useless stack adjustment
        ...

There are useless stack adjustment. A quick investigation shows it's caued by we first decide to put the return value on stack, then later optimized them into registers, and all those store to stack are deleted by dse1, but stack space required kept in x_rtl->x_frame_offset is not updated accordingly.

Although I run into this issue on AArch64, I highly suspect it's a generic issue when the type of return value is very complex.

Has anyone run into this issue on other architecture like MIPS, PPC?


---


### compiler : `gcc`
### title : `Reduction with sign-change not handled`
### open_at : `2015-04-29T12:17:38Z`
### last_modified_date : `2019-10-30T11:29:54Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=65930
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `6.0`
### severity : `normal`
### contents :
Neither

int foo (unsigned int *x)
{
  int sum = 0;
  for (int i = 0; i < 4; ++i)
    sum += x[i*4+0]+ x[i*4 + 1] + x[i*4 + 2] + x[i*4 + 3];
  return sum;
}

nor

int bar (unsigned int *x)
{
  int sum = 0;
  for (int i = 0; i < 16; ++i)
    sum += x[i];
  return sum;
}

are currently vectorized because

t.c:4:3: note: reduction: not commutative/associative: sum_27 = (int) _26;

though the sign of 'sum' vs the sign of 'x' doesn't really matter here.

It works for

unsigned baz (int *x)
{
  unsigned int sum = 0;
  for (int i = 0; i < 16; ++i)
    sum += x[i];
  return sum;
}

because C promotes x[i] instead of sum in this case.

For vectorization we might want to change the add(s) to int - of course
not strictly valid because of undefined overflow issues.

This kind of loop appears in a hot area of x264.


---


### compiler : `gcc`
### title : `[AArch64] Will not vectorize 64bit integer multiplication`
### open_at : `2015-04-30T17:26:28Z`
### last_modified_date : `2021-12-10T10:24:32Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=65951
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `5.1.0`
### severity : `normal`
### contents :
This loop:
void
foo (long *arr)
{
  for (int i = 0; i < 256; i++)
    arr[i] *= 19594L;
}

will not vectorize on AArch64, but does on x86. On AArch64, -fdump-tree-vect-details reveals:
test.c:4:3: note: ==> examining statement: _9 = _8 * 19594;
test.c:4:3: note: vect_is_simple_use: operand _8
test.c:4:3: note: def_stmt: _8 = *_7;
test.c:4:3: note: type of def: 3.
test.c:4:3: note: vect_is_simple_use: operand 19594
test.c:4:3: note: op not supported by target.
test.c:4:3: note: not vectorized: relevant stmt not supported: _9 = _8 * 19594;

on x86, vectorization fails with vectorization_factor = 4 (V4DI), but succeeds at V2DI.

We could vectorize this on AArch64 even if we have to perform a multiple-instruction load of that constant (invariant!) before the loop...right?


---


### compiler : `gcc`
### title : `[meta-bug] Operand Shortening`
### open_at : `2015-05-01T13:55:31Z`
### last_modified_date : `2021-09-06T10:54:35Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=65964
### status : `UNCONFIRMED`
### tags : `meta-bug, missed-optimization`
### component : `tree-optimization`
### version : `unknown`
### severity : `enhancement`
### contents :
Meta bug for tracking operand shortening issues


---


### compiler : `gcc`
### title : `Failure to remove casts, cause poor code generation`
### open_at : `2015-05-01T18:37:57Z`
### last_modified_date : `2021-07-25T03:20:01Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=65968
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `unknown`
### severity : `enhancement`
### contents :
Failure to shorten the multiplies from int mode down to their more native short modes causes poor code generation for this loop:


void f(short*a) {
  a = __builtin_assume_aligned(a,128);
  for (int i = 0; i < (1<<22); ++i) {
#ifdef EASY
    a[i] *= a[i];
#else
    int x = a[i];
    x *= x;
    a[i] = x;
#endif
  }
}

With -DEASY, a nice little loop:
.L2:
    movdqa    (%rdi), %xmm0
    addq    $16, %rdi
    pmullw    %xmm0, %xmm0
    movaps    %xmm0, -16(%rdi)
    cmpq    %rdi, %rax
    jne    .L2

while without EASY, we get the uglier:
.L2:
    movdqa    (%rdi), %xmm0
    addq    $16, %rdi
    movdqa    %xmm0, %xmm2
    movdqa    %xmm0, %xmm1
    pmullw    %xmm0, %xmm2
    pmulhw    %xmm0, %xmm1
    movdqa    %xmm2, %xmm0
    punpckhwd    %xmm1, %xmm2
    punpcklwd    %xmm1, %xmm0
    movdqa    %xmm2, %xmm1
    movdqa    %xmm0, %xmm2
    punpcklwd    %xmm1, %xmm0
    punpckhwd    %xmm1, %xmm2
    movdqa    %xmm0, %xmm1
    punpcklwd    %xmm2, %xmm0
    punpckhwd    %xmm2, %xmm1
    punpcklwd    %xmm1, %xmm0
    movaps    %xmm0, -16(%rdi)
    cmpq    %rdi, %rax
    jne    .L2

The narrowing patterns currently in match.pd and proposed for match.pd at the time of submitting this BZ handle plus/minus, but not multiply.  When writing the current patterns I saw regressions when mult handling was included.  Finding a way to avoid the regressions (should have filed BZs for them) while still shortening for this case would be good.

Marc indicates that pattern along these lines:

(simplify
 (vec_pack_trunc (widen_mult_lo @0 @1) (widen_mult_hi:c @0 @1))
 (mult @0 @1))

Would help this specific case, but we may do better if we can do the type narrowing before vectorization.


---


### compiler : `gcc`
### title : `paq8p benchmark 50% slower than clang on sandybridge`
### open_at : `2015-05-04T07:20:51Z`
### last_modified_date : `2021-08-14T23:12:29Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=66002
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `6.0`
### severity : `normal`
### contents :
Created attachment 35451
testcase

On sandybridge I get:

trippels@gcc75 ~ % g++ -O3 -march=native paq8p.ii -o paq8p
trippels@gcc75 ~ % time ./paq8p -4 file1.in
Creating archive with 1 file(s)...
file1.in 262144 -> 262371      
262144 -> 262400
Extracting 1 file(s) from archive -4
Comparing file1.in 262144 -> identical   
./paq8p -4 file1.in  61.82s user 0.08s system 100% cpu 1:01.90 total

trippels@gcc75 ~ % clang++ -w -O3 -march=native paq8p.ii -o paq8p
trippels@gcc75 ~ % time ./paq8p -4 file1.in
...
./paq8p -4 file1.in  29.60s user 0.12s system 100% cpu 29.715 total

Intel compiler:
./paq8p -4 file1.in  22.00s user 0.09s system 99% cpu 22.092 total


---


### compiler : `gcc`
### title : `Missed optimization after inlining va_list parameter, -m32 case`
### open_at : `2015-05-05T07:24:30Z`
### last_modified_date : `2021-03-26T00:08:49Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=66013
### status : `UNCONFIRMED`
### tags : `missed-optimization, patch`
### component : `tree-optimization`
### version : `6.0`
### severity : `trivial`
### contents :
[ -m32 twin PR of PR66010 ]

Consider this test-case (based on gcc.dg/tree-ssa/stdarg-2.c, f15):
...
#include <stdarg.h>

int
f1 (int i, ...)
{
  int res;
  va_list ap;

  va_start (ap, i);
  res = va_arg (ap, int);
  va_end (ap);

  return res;
}

inline int __attribute__((always_inline))
f2_1 (va_list ap)
{
  return va_arg (ap, int);
}

int
f2 (int i, ...)
{
  int res;
  va_list ap;

  va_start (ap, i);
  res = f2_1 (ap);
  va_end (ap);

  return res;
}
...

When compiling at -O2 with -m32, the optimized dump for f1 and f2 are very similar:
...
   # .MEM_9 = VDEF <.MEM_1(D)>
   # USE = anything 
   # CLB = anything 
-  ap_8 = __builtin_next_argD.993 (0);
-  ap_6 = ap_8;
+  ap_11 = __builtin_next_argD.993 (0);
+  ap_6 = ap_11;
   # PT = nonlocal 
-  ap_7 = ap_6;
+  ap_3 = ap_6;
   # VUSE <.MEM_9>
-  res_4 = MEM[(intD.1 *)ap_7];
+  _7 = MEM[(intD.1 *)ap_3];
   GIMPLE_NOP
   # VUSE <.MEM_9>
-  return res_4;
+  return _7;
 ;;    succ:       EXIT [100.0%] 
...

However, at pass_stdarg, we see on one hand:
...
f1: va_list escapes 0, needs to save 4 GPR units and all FPR units.
...

but OTOH:
...
f2: va_list escapes 1, needs to save all GPR units and all FPR units.
...

Still the .s code is identical for f1 and f2:
...
	.cfi_startproc
	movl	8(%esp), %eax
	ret
	.cfi_endproc
...

This is because ix86_setup_incoming_varargs doesn't do anything for -m32:
...
static void
ix86_setup_incoming_varargs (cumulative_args_t cum_v, machine_mode mode,
                             tree type, int *, int no_rtl)
{
  CUMULATIVE_ARGS *cum = get_cumulative_args (cum_v);
  CUMULATIVE_ARGS next_cum;
  tree fntype;

  /* This argument doesn't appear to be used anymore.  Which is good,
     because the old code here didn't suppress rtl generation.  */
  gcc_assert (!no_rtl);

  if (!TARGET_64BIT)
    return;
...


---
