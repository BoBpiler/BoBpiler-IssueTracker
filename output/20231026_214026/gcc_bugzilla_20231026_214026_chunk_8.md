### Total Bugs Detected: 4649
### Current Chunk: 8 of 30
### Bugs in this Chunk: 160 (From bug 1121 to 1280)
---


### compiler : `gcc`
### title : `uint8_t memory access not optimized`
### open_at : `2015-05-11T17:02:54Z`
### last_modified_date : `2019-06-15T00:10:59Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=66110
### status : `RESOLVED`
### tags : `alias, missed-optimization`
### component : `middle-end`
### version : `5.1.0`
### severity : `normal`
### contents :
It appears that gcc does not do a good job of optimizing memory accesses to 'uint8_t' variables.  In particular, it appears as if "strict aliasing" is not done on uint8_t variables, and it appears it is not done even if the uint8_t is in a struct.

============ GCC version:

$ ~/src/install-5.1.0/bin/gcc -v
Using built-in specs.
COLLECT_GCC=/home/kevin/src/install-5.1.0/bin/gcc
COLLECT_LTO_WRAPPER=/home/kevin/src/install-5.1.0/libexec/gcc/x86_64-unknown-linux-gnu/5.1.0/lto-wrapper
Target: x86_64-unknown-linux-gnu
Configured with: ../gcc-5.1.0/configure --prefix=/home/kevin/src/install-5.1.0 --enable-languages=c
Thread model: posix
gcc version 5.1.0 (GCC) 

=========== Compile command line:

~/src/install-5.1.0/bin/gcc -v -save-temps -O2 -Wall u8alias.c -c

=========== Contents of u8alias.c:

typedef __UINT8_TYPE__ uint8_t;
typedef __UINT16_TYPE__ uint16_t;

struct s1 {
    uint16_t f1;
    uint8_t f2;
};

struct s2 {
    struct s1 *p1;
};

void f1(struct s2 *p)
{
    p->p1->f2 = 9;
    p->p1->f2 = 10;
}

=========== Contents of u8alias.i:

# 1 "u8alias.c"
# 1 "<built-in>"
# 1 "<command-line>"
# 1 "/usr/include/stdc-predef.h" 1 3 4
# 1 "<command-line>" 2
# 1 "u8alias.c"
typedef unsigned char uint8_t;
typedef short unsigned int uint16_t;

struct s1 {
    uint16_t f1;
    uint8_t f2;
};

struct s2 {
    struct s1 *p1;
};

void f1(struct s2 *p)
{
    p->p1->f2 = 9;
    p->p1->f2 = 10;
}

=========== Results of compilation:

$ objdump -ldr u8alias.o

0000000000000000 <f1>:
f1():
   0:   48 8b 07                mov    (%rdi),%rax
   3:   c6 40 02 09             movb   $0x9,0x2(%rax)
   7:   48 8b 07                mov    (%rdi),%rax
   a:   c6 40 02 0a             movb   $0xa,0x2(%rax)
   e:   c3                      retq   

=========== Expected results:

I expected the second redundant load to be eliminated - for example, clang produces this assembler (after replacing the gcc specific uint8_t typedefs with an include of <stdint.h>):

$ clang -Wall -O2 u8alias.c -c
$ objdump -ldr u8alias.o

0000000000000000 <f1>:
f1():
   0:   48 8b 07                mov    (%rdi),%rax
   3:   c6 40 02 0a             movb   $0xa,0x2(%rax)
   7:   c3                      retq   

=========== Other notes:

If the code is changed so that there are two redundant writes to ->f1 then gcc does properly optimize away the first store.  Also, if the above definition of f2 is changed to an 8-bit bitfield (ie, "uint8_t f2 : 8;") then gcc does properly optimize away the first store.

This occurs on other platforms besides x86_64.  (In particular, it happens on avr-gcc where 8-bit integers are very common.)  I reproduced the above on gcc 5.1.0, but I've also seen it on variants of gcc 4.8 and gcc 4.9.

My guess is that the above is the result of an interpretation of the C99 specification - in particular section 6.5:

  An object shall have its stored value accessed only by an lvalue expression that has one of the following types:
[...]
      -- a character type.

However, I do not think that should apply to the above test case for either of the two following reasons:

1 - the memory access was not to a character type, it was to an integer type that happened to be 1 byte in size (ie, a uint8_t type)
2 - the memory access was not to a character type, it was to a member of 'struct s1'.

As noted above, clang (eg, 3.4.2) does perform the expected optimization.


---


### compiler : `gcc`
### title : `Loop is not vectorized because not sufficient support for GOMP_SIMD_LANE`
### open_at : `2015-05-14T14:18:04Z`
### last_modified_date : `2021-10-01T02:56:42Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=66142
### status : `REOPENED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `6.0`
### severity : `normal`
### contents :
The attached test-case compiled with "-Ofast -fopenmp -march=core-avx2" options contains loop marked with pragma omp simd which is not vectorized:
t1.cpp:66:20: note: not vectorized: data ref analysis failed MEM[(struct vec_ *)_9] = 1.0e+0;
where index is defined as
  _12 = GOMP_SIMD_LANE (simduid.0_11(D));
  _9 = &D.4231[_12].org;

Note that this test was extracted from important benchmark and loop in question is vectorized if we revert fix for 59984.


---


### compiler : `gcc`
### title : `[9 Regression] suboptimal load bytes to stack`
### open_at : `2015-05-14T21:37:41Z`
### last_modified_date : `2019-02-16T18:52:59Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=66152
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `9.0`
### severity : `normal`
### contents :
for code

void foo(char *);

void bar(void)
{
  char a[] = {0,1,2,3,4,5,6,7};
  foo(a);
}

gcc generates many movb instructions:
	subq	$24, %rsp
	movq	%rsp, %rdi
	movb	$0, (%rsp)
	movb	$1, 1(%rsp)
	movb	$2, 2(%rsp)
	movb	$3, 3(%rsp)
	movb	$4, 4(%rsp)
	movb	$5, 5(%rsp)
	movb	$6, 6(%rsp)
	movb	$7, 7(%rsp)

clang produces:
	pushq	%rax
	movabsq	$506097522914230528, %rax # imm = 0x706050403020100
	movq	%rax, (%rsp)
	leaq	(%rsp), %rdi

for 16-byte array, gcc 5.1.0 builds the array separately and copies it using movqda and movaps instruction i.e. :
  char a[] = {0,1,2,3,4,5,6,7,0,1,2,3,4,5,6,7};
produces:
	subq	$24, %rsp
	movdqa	.LC0(%rip), %xmm0
	movq	%rsp, %rdi
	movaps	%xmm0, (%rsp)
but if I make a 17-byte array, it again create movb instruction for each byte


---


### compiler : `gcc`
### title : `failure to vectorize parallelized loop`
### open_at : `2015-05-26T07:55:19Z`
### last_modified_date : `2021-08-16T04:46:31Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=66285
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `6.0`
### severity : `minor`
### contents :
Another pr46032-inspired example.

Consider par-2.c:
...
#define nEvents 1000

int __attribute__((noinline,noclone))
f (int argc, double *__restrict results, double *__restrict data)
{
  double coeff = 12.2;

  for (INDEX_TYPE idx = 0; idx < nEvents; idx++)
    results[idx] = coeff * data[idx];

  return !(results[argc] == 0.0);
}

#if defined (MAIN)
int
main (int argc)
{
  double results[nEvents] = {0};
  double data[nEvents] = {0};

  return f (argc, results, data);
}
#endif
...

And investigate.sh:
...
#!/bin/bash

src=par-2.c

for parloops_factor in 0 2; do
    for index_type in "int" "unsigned int" "long" "unsigned long"; do
	rm -f *.c.*;

	./lean-c/install/bin/gcc -O2 $src -S \
	    -ftree-parallelize-loops=$parloops_factor \
	    -ftree-vectorize \
	    -fdump-tree-all-all \
	    "-DINDEX_TYPE=$index_type"

	vectdump=$src.132t.vect
	pardump=$src.129t.parloops

	vectorized=$(grep -c "LOOP VECTORIZED" $vectdump)

	if [ ! -f $pardump ]; then 
	    parallelized=0
	else
	    parallelized=$(grep -c "parallelizing inner loop" $pardump)
	fi

	echo "parloops_factor: $parloops_factor, index_type: $index_type:"
	echo "  vectorized: $vectorized, parallelized: $parallelized"
    done
done
...

If we're not parallelizing, vectorization succeeds:
...
parloops_factor: 0, index_type: int:
  vectorized: 1, parallelized: 0
parloops_factor: 0, index_type: unsigned int:
  vectorized: 1, parallelized: 0
parloops_factor: 0, index_type: long:
  vectorized: 1, parallelized: 0
parloops_factor: 0, index_type: unsigned long:
  vectorized: 1, parallelized: 0
...

If we're parallelizing, vectorization succeeds for (unsigned) long:
...
parloops_factor: 2, index_type: long:
  vectorized: 1, parallelized: 1
parloops_factor: 2, index_type: unsigned long:
  vectorized: 1, parallelized: 1
...

but not for (unsigned) int:
...
parloops_factor: 2, index_type: int:
  vectorized: 0, parallelized: 1
parloops_factor: 2, index_type: unsigned int:
  vectorized: 0, parallelized: 1
...


---


### compiler : `gcc`
### title : `poor optimization of packed structs containing bitfields`
### open_at : `2015-06-01T15:34:57Z`
### last_modified_date : `2023-07-19T04:11:45Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=66364
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `5.1.0`
### severity : `enhancement`
### contents :
Created attachment 35667
Simple program demonstrating the issue

Code accessing bitfields in packed structures seem to load the value a byte at a time and build the value up using shifts and ors even with -O3.

On x64 it could load the value using a single mov instruction as it does when the struct is not packed or when the field is not a bitfield.


---


### compiler : `gcc`
### title : `gcc 4.8.3/5.1.0 miss optimisation with vpmovmskb`
### open_at : `2015-06-01T21:53:44Z`
### last_modified_date : `2021-07-26T09:25:58Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=66369
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.8.3`
### severity : `minor`
### contents :
Created attachment 35672
example C code to demonstrate the missed optimisation in gcc 4.8.3 and 5.1.0

When using _mm256_movemask_epi8() I cannot find a way for gcc to produce
   vpmovmskb YMM,R64
instead of 
   vpmovmskb YMM,R32

When the result of the vpmovmskb is not stored in R64, unnecessary sign-extension instructions cltq, movl or movslq are generated later.  With a result in R32 and indexing an array of structs, gcc generates for 
   node = node->children[ __builtin_ctzl(result-of-vpmovmskb) ]
the following:
   vpmovmskb YMM,R32
   movslq    R32, R64
   tzcntq    R64, R64
   movq      offset(%rdi,R64,8), %rdi
instead of the more efficient:
   vpmovmskb YMM,R64
   tzcntq    R64,R64
   movq      offset(%rdi,R64,8), %rdi

Attached is avx2.c which has the C source code that demonstrates the above.
aavx2.c is compiled with gcc (GCC) 4.8.3 20140911 (Red Hat 4.8.3-9) and flags
   -std=c99 -march=core-avx2  -mtune=core-avx2 -O3
gcc 5.1.0 has the same behaviour.


---


### compiler : `gcc`
### title : `suboptimal code for assignment of SImode struct with bitfields`
### open_at : `2015-06-03T06:56:43Z`
### last_modified_date : `2023-07-19T04:07:29Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=66391
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `5.0`
### severity : `enhancement`
### contents :
This is caused by early SRA splitting elem's assignment into separate per-field assignments.

struct x {
        unsigned a : 6;
        unsigned b : 26;
};      

int f(struct x *x, unsigned a, unsigned b)
{       
        struct x elem = { .a = a, .b = b };
        int i;
        
        for (i = 0; i < 512; i++)
                x[i] = elem;
}       

Generated code:

.LFB0:
	.cfi_startproc
	leaq	2048(%rdi), %rcx
	andl	$63, %esi
	sall	$6, %edx
	.p2align 4,,10
	.p2align 3
.L2:
	movzbl	(%rdi), %eax
	addq	$4, %rdi
	andl	$-64, %eax
	orl	%esi, %eax
	movb	%al, -4(%rdi)
	movl	-4(%rdi), %eax
	andl	$63, %eax
	orl	%edx, %eax
	movl	%eax, -4(%rdi)
	cmpq	%rcx, %rdi
	jne	.L2
	rep ret
	.cfi_endproc


---


### compiler : `gcc`
### title : `combine fails to merge insns if some are reused later on`
### open_at : `2015-06-10T14:30:31Z`
### last_modified_date : `2023-06-02T04:53:08Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=66489
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `6.0`
### severity : `enhancement`
### contents :
Consider code:
int f2(int a, int b, int c, int d)
{
  a = -a;
  b += a * c;
  c += a * d;
  return b ^ c;
}

On aarch64 this could be written with to msub instructions, RTL code:

(set (reg/i:SI 0 x0)
     (minus:SI
       (reg:SI 1 x1 [ b ])
       (mult:SI (reg:SI 0 x0 [ a ])
                (reg:SI 2 x2 [ c ])))) 

However, combine doesn't merge the neg and the multiply-adds and generates:
f2:
        neg     w4, w0
        madd    w0, w4, w2, w1
        madd    w3, w4, w3, w2
        eor     w0, w0, w3
        ret


If we modify the code to only do a single multiply-accumulate:
int f2(int a, int b, int c, int d)
{
  a = -a;
  b += a * c;
  return b;
}

Then they the expected single msub instruction is generated.
I think this is due to combine being scared of the negated 'a' being used in two places.


---


### compiler : `gcc`
### title : `SCCVN can't handle PHIs optimistically optimally`
### open_at : `2015-06-11T09:16:36Z`
### last_modified_date : `2022-01-07T06:38:53Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=66502
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `6.0`
### severity : `normal`
### contents :
Currently FRE doesn't eliminate redundant IVs like in

int x[1024];
int foo (int a, int s, unsigned int k)
{
  int i = a, j = a;
  int sum = 0;
  do
    {
      sum += x[i];
      sum += x[j];
      i += s;
      j += s;
    }
  while (k--);
  return sum;
}

but it handles the following instead

int foo (int a, int s, unsigned int k)
{
  int i = a, j = a;
  do
    {
      i += s;
      j += j;
      j -= a;
    }
  while (k--);
  return j+i;
}

the difference is whether a PHI node with all but one non-VN_TOP argument
is optimistically value-numbered to that argument or to another PHI node
in the same BB with the same argument in its position (if existing).

If it were not SCCVN then if both PHIs are value-numbered together
value-numbering optimistically to the non-VN_TOP argument could catch
both cases, but only if we allow a questionable lattice-transition
from a final value (the non-VN_TOP argument) to a still optimistic
one (the other PHI nodes result).  That's of course exactly a transition
that we want to avoid because of lattice oscillations (well, if we
allow it in this one direction only and not back it might be fine).

To "fix" SCCVN we'd need to put any such PHI node candidates into the
same SCC and allow that lattice transition.


---


### compiler : `gcc`
### title : `[avr] whole-byte shifts not optimized away for uint64_t`
### open_at : `2015-06-11T14:49:47Z`
### last_modified_date : `2023-04-16T17:27:33Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=66511
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `target`
### version : `4.9.2`
### severity : `enhancement`
### contents :
When doing whole-byte shifts, gcc usually optimizes away the shifts and
ends up moving data between registers instead. However, it seems this
doesn't happen when uint64_t is used.

Here's an example (assembler output slightly trimmed of unrelated
comments and annotations etc.):

matthijs@grubby:~$ cat test.cpp
#include <stdint.h>

uint8_t foo64_8(uint64_t a) {
        return a >> 8;
}

uint16_t foo64_16(uint64_t a) {
        return a >> 8;
}

uint8_t foo32_8(uint32_t a) {
        return a >> 8;
}

uint16_t foo32_16(uint32_t a) {
        return (a >> 8);
}

matthijs@grubby:~$ avr-gcc -Os test.cpp -S -o -
_Z7foo64_8y:
        push r16
        ldi r16,lo8(8)
        rcall __lshrdi3
        mov r24,r18
        pop r16
        ret

_Z8foo64_16y:
        push r16
        ldi r16,lo8(8)
        rcall __lshrdi3
        mov r24,r18
        mov r25,r19
        pop r16
        ret


_Z7foo32_8m:
        mov r24,r23
        ret

_Z8foo32_16m:
        clr r27
        mov r26,r25
        mov r25,r24
        mov r24,r23
        ret

        .ident  "GCC: (GNU) 4.9.2 20141224 (prerelease)"

The output is identical for 4.8.1 on Debian, and the above 4.9.2 on
Arch. I haven't found a readily available 5.x package yet to test.

As you can see, the versions operating on 64 bit values preserve the
8-bit shift (which is very inefficient on AVR), while the versions
running on 32 bit values simply copy the right registers.

The foo32_16 function still has some useless instructions (r27 and r26
are not part of the return value, not sure why these are set) but that
is probably an unrelated problem.

I've marked this with component "target", since I think these
optimizations are avr-specific (or at least not applicable to bigger
architectures).


---


### compiler : `gcc`
### title : `Missed optimization when shift amount is result of signed modulus`
### open_at : `2015-06-16T08:24:11Z`
### last_modified_date : `2020-10-21T03:15:52Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=66552
### status : `RESOLVED`
### tags : `easyhack, missed-optimization`
### component : `rtl-optimization`
### version : `5.0`
### severity : `enhancement`
### contents :
In code such as

unsigned f(unsigned x, int n)
{
  return x >> (n % 32);
}

I think gcc should be allowed to assume that n is either positive or divisible by 32 (i.e., that the result of the % is non-negative). So it should actually compile this the same as it does x >> (n & 31). However, it seems to generate code to compute the actual value of n%32 and then uses that.

Even if one doesn't want to optimize based on UB, this is silly on a platform like x86: There, gcc already knows that the shift instruction only depends on the lower 5 bits, and those 5 bits do not depend on the full result of the modulus (whether following C99 or not).


---


### compiler : `gcc`
### title : `Unexpected change in static, branch-prediction cost from O1 to O2 in if-then-else.`
### open_at : `2015-06-17T15:07:53Z`
### last_modified_date : `2020-04-13T11:27:31Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=66573
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `unknown`
### severity : `normal`
### contents :
For the following versions of gcc: 4.8.2, 4.9.0 and 5.10 with the following code sequence:

extern void bar1();
extern void bar2();

void foo(bool i) {
  if (i)
	bar1();
  else
    bar2();
}

I have examined the assembler output for -O0, -O1, -O2 and -O3.

For all versions with -O0 & -O1 I get this:

foo(bool):
	subq	$8, %rsp
	testb	%dil, %dil
	je	.L2
	call	bar1()
	jmp	.L1
.L2:
	call	bar2()
.L1:
	addq	$8, %rsp
	ret

For all version with -O2 and -O3 I get this:

foo(bool):
	testb	%dil, %dil
	jne	.L4
	jmp	bar2()
.L4:
	jmp	bar1()

Note how the calls to bar1() and bar2() have been swapped. (I realise that the condition has been swapped too, so that the generated code is correct.)

According to:

https://software.intel.com/en-us/articles/branch-and-loop-reorganization-to-prevent-mispredicts/

Forward jumps are not taken. So what has happened is that for -O0 and -O1 the static branch-prediction has given no mis-prediction if bar1() is called, i.e. the condition is usually true. But this flips for -O2 and -O3 so that now bar2() suffers no mis-prediction if the condition is usually false.

The result is that if one codes so that one minimises the mis-predition cost for -O0 and -O1 this becomes a pessimisation for -O2 and -O3. A rather unexpected result.

Note that icc v13.0.1 generates the following assembly sequence:

foo(bool):
        testb     %dil, %dil                                    #5.7
        je        ..B1.3        # Prob 50%                      #5.7
        jmp       bar1()                                      #6.2
..B1.3:                         # Preds ..B1.1
        jmp       bar2()                                      #8.5

Which is stable for all optimisation levels, and works as one might expect: the if-branch is the predicted branch, the else not.

(Yes I am aware of __builtin_expected(), but that is beside the point. One would expect that the cost should reduce with increasing levels of optimisation not increase!)


---


### compiler : `gcc`
### title : `combine should try transforming if_then_else of zero_extends into zero_extend of if_then_else`
### open_at : `2015-06-18T13:39:43Z`
### last_modified_date : `2023-04-19T15:45:00Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=66588
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `6.0`
### severity : `normal`
### contents :
Consider the code:

unsigned long
foo (unsigned int a, unsigned int b, unsigned int c)
{
  return a ? b : c;
}

On aarch64 this generates:
foo:
        uxtw    x1, w1
        cmp     w0, wzr
        uxtw    x2, w2
        csel    x0, x2, x1, eq
        ret

where in fact it could generate:
        cmp      w0, #0
        csel    w0, w1, w2, ne
        ret

A write to the 32-bit w-register implicitly zero-extends the value up to the full
64 bits of an x-register.

This is reflected in aarch64.md by the cmovsi_insn_uxtw pattern that matches:
(set (dest:DI)
     (zero_extend:DI
        (if_then_else:SI (cond) (src1:SI) (src2:SI))
     )
)

However, this doesn't get matched because combine instead tries to match
(set (dest:DI)
     (if_then_else:DI (cond)
                      (zero_extend:DI (src1:SI))
                      (zero_extend:DI (src2:SI))
     )
)

If I change the pattern to the second form then I get the desired codegen.
However, it seems that combine should really be trying that transformation by itself.


---


### compiler : `gcc`
### title : `Aggregate assignment prevents store-motion`
### open_at : `2015-06-20T00:53:41Z`
### last_modified_date : `2021-07-07T12:09:02Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=66610
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `6.0`
### severity : `normal`
### contents :
Created attachment 35818
Minimal testcase demonstrating the issue

libgccjit showed poor performance relative to a LLVM backend within an experimental JIT-compiler for Lua (https://github.com/dibyendumajumdar/ravi).

On investigation it appears to be due to unions and structs stopping value-numbering from working.

I'm attaching a minimal reproducer for the issue.

If the code copies the struct and the union within it field-wise, pass_fre (tree-ssa-pre.c) uses value numbering to eliminate the copy of the loop index through *arr, and turns loop_using_union_field_assignment into:

  loop_using_union_field_assignment (int num_iters, struct s * arr)
  {
    int i;
  
    <bb 2>:
    goto <bb 4>;
  
    <bb 3>:
    arr_6(D)->union_field.int_field = i_1;
    MEM[(struct s *)arr_6(D) + 4B].union_field.int_field = i_1;
    i_11 = i_1 + 1;
  
    <bb 4>:
    # i_1 = PHI <0(2), i_11(3)>
    if (i_1 < num_iters_5(D))
      goto <bb 3>;
    else
      goto <bb 5>;
  
    <bb 5>:
    return;
  }

and the loop is eliminated altogether by cddce2.
  
However, if the code does a compound copy, pass_fre doesn't eliminate the copy of the loop index and the loop can't be eliminated (with a big performance loss); in the example, functions "loop_using_struct_assignment" and "loop_using_union_assignment" fail to have their loops optimized away at -O3.

Hence the libgccjit user has patched things at their end to direct copying the fields (fwiw their workaround was this commit
https://github.com/dibyendumajumdar/ravi/commit/a5b192cd4f4213cd544e31b08b02eb9082142b20 )

Should compound assignments be optimizable via value-numbering?  Would it make sense to split out the compound assignments field-wise internally before doing value-numbering?

This is all with gcc trunk (r224625 aka e3a904dbdc78cb45b98e8b109e0e49e759315b7c) on x86_64 at -O3.


---


### compiler : `gcc`
### title : `small loop turned into memmove because of tree ldist`
### open_at : `2015-06-24T02:31:42Z`
### last_modified_date : `2021-09-05T01:01:33Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=66646
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `6.0`
### severity : `enhancement`
### contents :
Considering below small case
int foo (int flag, char *a)                                                    
{                                                                              
  short i, j;                                                                  
  short l = 0;                                                                 
  if (flag == 1)                                                               
    l = 3;                                                                     

  for (i = 0; i < 4; i++)                                                      
    {                                                                          
      for (j = l - 1; j > 0; j--)                                              
        a[j] = a[j - 1];                                                       
      a[0] = i;                                                                
    }                                                                          
}
After revision 224020, SCEV can recognize &a[j], &a[j-1].  pass ldist decides to replace the inner loop with memmove.  Since it's a small loop, most likely this results in peformance regression.  We need:
A) compute more accurate loop niter bound in such case so that optimizers know it's small loop.
B) don't turn loop into mem* call if it's small loop.


---


### compiler : `gcc`
### title : `gcc misses optimization emits useless test of (a & 31) with 32`
### open_at : `2015-06-25T12:02:31Z`
### last_modified_date : `2021-07-27T00:05:06Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=66663
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `5.0`
### severity : `enhancement`
### contents :
The following code:

    unsigned long long foo(unsigned long long x, int a) {
        return x << (a & 31);
    }

compiled with a recent build of gcc for i386 Linux (with -O3) yields the following assembly:

    foo:
        movl    12(%esp), %ecx
        movl    4(%esp), %eax
        movl    8(%esp), %edx
	andl    $31, %ecx
	shldl   %eax, %edx
	sall    %cl, %eax
	testb   $32, %cl
	je      .L2
	movl    %eax, %edx
	xorl    %eax, %eax
.L2:
	rep ret

        .ident	"GCC: (GNU) 5.0.0 20150314 (experimental)"

The testb instruction seems redundant as %cl has been masked with $31 a few instructions before: The jump will never be taken.


---


### compiler : `gcc`
### title : `gcc misses optimization emits subtraction where relocation arithmetic would suffice`
### open_at : `2015-06-25T12:25:07Z`
### last_modified_date : `2021-12-25T08:39:38Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=66664
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `5.0`
### severity : `enhancement`
### contents :
For the following C code:

    int foo(int x)  {
        extern int bar[];
        return bar[x - 1];
    }

gcc emits the following code (with -O3) on amd64 Linux:

    foo:
        subl    $1, %edi
        movslq  %edi, %rdi
        movl    bar(,%rdi,4), %eax
        ret

        .ident	"GCC: (GNU) 5.0.0 20150314 (experimental)"

I expected gcc to emit the following (as signed underflow is undefined):

    foo:
        movslq  %edi, %rdi
        movl    bar-4(,%rdi,4), %eax
        ret

or even this (as the memory model places global variables in the first 2^32 byte of RAM):

    foo:
        movl    bar-4(,%edi,4), %eax
        ret


---


### compiler : `gcc`
### title : `Could improve vector lane folding style operations.`
### open_at : `2015-06-25T21:03:04Z`
### last_modified_date : `2021-08-20T06:01:52Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=66675
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `5.1.0`
### severity : `enhancement`
### contents :
This example 


#include <arm_neon.h>
 
int main(int argc, char *argv[])
{
    int8x8_t a = {argc, 1, 2, 3, 4, 5, 6, 7};
    int8x8_t b = {0, 1, 2, 3, 4, 5, 6, 7};
    int8x8_t c = vadd_s8(a, b);
    return c[0];
}


or it's variant written in gcc vector speak generate pretty terrible code for AArch64 

main:
        adr     x1, .LC0
        ld1     {v0.8b}, [x1]
        ins     v0.b[0], w0
        adr     x0, .LC2
        ld1     {v1.8b}, [x0]
        add     v0.8b, v0.8b, v1.8b
        umov    w0, v0.b[0]
        sxtb    w0, w0
        ret
        .size   main, .-main


This could well be folded down to a simple function that returns just argc. While this is a bit silly to expect in real life, it does show an interesting example....


regards
Ramana


---


### compiler : `gcc`
### title : `loop counter not accurately described by vrp`
### open_at : `2015-06-26T11:15:10Z`
### last_modified_date : `2023-08-10T06:57:15Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=66678
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `6.0`
### severity : `enhancement`
### contents :
consider testcase:
...
void
f (unsigned int n, unsigned int *__restrict__ a, unsigned int *__restrict__ b,
   unsigned int *__restrict__ c)
{
  unsigned int i;

  for (i = 0; i < n; ++i)
    c[i] = a[i] + b[i];
}
...

After vrp1 we have:
...
f (unsigned intD.9 nD.2874, unsigned intD.9 * restrict aD.2875, unsigned intD.9 * restrict bD.2876, unsigned intD.9 * restrict cD.2877)
{
  unsigned intD.9 iD.2880;
  long unsigned intD.10 _5;
  long unsigned intD.10 _6;
  unsigned intD.9 * _8;
  unsigned intD.9 * _10;
  unsigned intD.9 _11;
  unsigned intD.9 * _13;
  unsigned intD.9 _14;
  unsigned intD.9 _15;

;;   basic block 2, loop depth 0, count 0, freq 900, maybe hot
;;    prev block 0, next block 3, flags: (NEW, REACHABLE)
;;    pred:       ENTRY [100.0%]  (FALLTHRU,EXECUTABLE)
  goto <bb 4>;
;;    succ:       4 [100.0%]  (FALLTHRU,EXECUTABLE)

;;   basic block 3, loop depth 1, count 0, freq 9100, maybe hot
;;    prev block 2, next block 4, flags: (NEW, REACHABLE)
;;    pred:       4 [91.0%]  (TRUE_VALUE,EXECUTABLE)
  # RANGE [0, 18446744073709551615] NONZERO 4294967295
  _5 = (long unsigned intD.10) i_1;
  # RANGE [0, 18446744073709551615] NONZERO 18446744073709551612
  _6 = _5 * 4;
  # PT = { D.2900 } (nonlocal)
  _8 = c_7(D) + _6;
  # PT = { D.2898 } (nonlocal)
  _10 = a_9(D) + _6;
  # VUSE <.MEM_2>
  _11 = MEM[(unsigned intD.9 *)_10 clique 1 base 2];
  # PT = { D.2899 } (nonlocal)
  _13 = b_12(D) + _6;
  # VUSE <.MEM_2>
  _14 = MEM[(unsigned intD.9 *)_13 clique 1 base 3];
  # RANGE [0, 4294967295]
  _15 = _11 + _14;
  # .MEM_16 = VDEF <.MEM_2>
  MEM[(unsigned intD.9 *)_8 clique 1 base 1] = _15;
  # RANGE [0, 4294967295]
  i_17 = i_1 + 1;
;;    succ:       4 [100.0%]  (FALLTHRU,DFS_BACK,EXECUTABLE)

;;   basic block 4, loop depth 1, count 0, freq 10000, maybe hot
;;    prev block 3, next block 5, flags: (NEW, REACHABLE)
;;    pred:       2 [100.0%]  (FALLTHRU,EXECUTABLE)
;;                3 [100.0%]  (FALLTHRU,DFS_BACK,EXECUTABLE)
  # i_1 = PHI <0(2), i_17(3)>
  # .MEM_2 = PHI <.MEM_3(D)(2), .MEM_16(3)>
  if (i_1 < n_4(D))
    goto <bb 3>;
  else
    goto <bb 5>;
;;    succ:       3 [91.0%]  (TRUE_VALUE,EXECUTABLE)
;;                5 [9.0%]  (FALSE_VALUE,EXECUTABLE)

;;   basic block 5, loop depth 0, count 0, freq 900, maybe hot
;;    prev block 4, next block 1, flags: (NEW, REACHABLE)
;;    pred:       4 [9.0%]  (FALSE_VALUE,EXECUTABLE)
  # VUSE <.MEM_2>
  return;
;;    succ:       EXIT [100.0%] 

}
...

AFAIU:
- the loop iv i_1 has range [0, 4294967294], and 
- the loop iv increment i_17 has range [1, 4294967295]

But in the dump resulting from vrp1, i_1 has no range assigned, and i_17 has RANGE [0, 4294967295] (which is equivalent to no range assigned).


During vrp the pass inserts an assert at the start of bb 3:
...
;;   basic block 3, loop depth 1, count 0, freq 9100, maybe hot
;;    prev block 2, next block 4, flags: (NEW, REACHABLE)
;;    pred:       4 [91.0%]  (TRUE_VALUE,EXECUTABLE)
  i_18 = ASSERT_EXPR <i_1, i_1 < n_4(D)>;
  # RANGE [0, 18446744073709551615] NONZERO 4294967295
  _5 = (long unsigned intD.10) i_18;
  # RANGE [0, 18446744073709551615] NONZERO 18446744073709551612
  _6 = _5 * 4;
  # PT = { D.2900 } (nonlocal)
  _8 = c_7(D) + _6;
  # PT = { D.2898 } (nonlocal)
  _10 = a_9(D) + _6;
  # VUSE <.MEM_2>
  _11 = MEM[(unsigned intD.9 *)_10 clique 1 base 2];
  # PT = { D.2899 } (nonlocal)
  _13 = b_12(D) + _6;
  # VUSE <.MEM_2>
  _14 = MEM[(unsigned intD.9 *)_13 clique 1 base 3];
  _15 = _11 + _14;
  # .MEM_16 = VDEF <.MEM_2>
  MEM[(unsigned intD.9 *)_8 clique 1 base 1] = _15;
  i_17 = i_18 + 1;
;;    succ:       4 [100.0%]  (FALLTHRU,DFS_BACK,EXECUTABLE)

;;   basic block 4, loop depth 1, count 0, freq 10000, maybe hot
;;    prev block 3, next block 5, flags: (NEW, REACHABLE)
;;    pred:       2 [100.0%]  (FALLTHRU,EXECUTABLE)
;;                3 [100.0%]  (FALLTHRU,DFS_BACK,EXECUTABLE)
  # i_1 = PHI <0(2), i_17(3)>
  # .MEM_2 = PHI <.MEM_3(D)(2), .MEM_16(3)>
  if (i_1 < n_4(D))
    goto <bb 3>;
  else
    goto <bb 5>;
...

When visiting the assert we get:
...
Visiting statement:
i_18 = ASSERT_EXPR <i_1, i_1 < n_4(D)>;
Intersecting
  [0, n_4(D) + 4294967295]  EQUIVALENCES: { i_1 } (1 elements)
and
  [0, 0]
to
  [0, n_4(D) + 4294967295]  EQUIVALENCES: { i_1 } (1 elements)
Found new range for i_18: [0, n_4(D) + 4294967295]
...

AFAIU, if we have no information on n_4, then range
  [0, n_4(D) + 4294967295]
is equal to 
  [0, 4294967295]

From the assert however we can also derive a range of
  [0, 4294967294 ]
given that i_1 < n_4 and n_4 is at most 4294967295.

So, a more accurate range is
  [0, MIN (n_4(D) + 4294967295, 4294967294) ].


---


### compiler : `gcc`
### title : `Non-invariant ADDR_EXPR not vectorized`
### open_at : `2015-07-01T09:41:12Z`
### last_modified_date : `2021-12-23T23:44:44Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=66718
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `6.0`
### severity : `normal`
### contents :
E.g. on:
int *a[1024], b[1024];
struct S { int u, v, w, x; };
struct S c[1024];

void
f0 (void)
{
  for (int i = 0; i < 1024; i++)
    a[i] = &b[0];
}

void
f1 (void)
{
  for (int i = 0; i < 1024; i++)
    {
      int *p = &b[0];
      a[i] = p + i;
    }
}

void
f2 (int *p)
{
  for (int i = 0; i < 1024; i++)
    a[i] = &p[i];
}

void
f3 (void)
{
  for (int i = 0; i < 1024; i++)
    a[i] = &b[i];
}

void
f4 (void)
{
  int *p = &c[0].v;
  for (int i = 0; i < 1024; i++)
    a[i] = &p[4 * i];
}

void
f5 (void)
{
  for (int i = 0; i < 1024; i++)
    a[i] = &c[i].v;
}

with -O3 -mavx2 we vectorize only the loops where the address computation has been lowered (f1, f2, f4) or is address of invariant (f0), but the vectorizer is not able to vectorize ADDR_EXPR of non-invariant.

Richard thinks this would be best solved by lowering such ADDR_EXPR assignments,
somewhere in between the last objsz pass and pre, maybe even before reassoc so that it can optimize even that.


---


### compiler : `gcc`
### title : `missed optimization, factor conversion out of COND_EXPR`
### open_at : `2015-07-01T17:23:06Z`
### last_modified_date : `2019-07-01T21:49:26Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=66726
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `unknown`
### severity : `normal`
### contents :
Given something like this:

   n = (short unsigned int) mode_size[(unsigned int) mode] * 8 <= 64 ? (int) ((short unsigned int) mode_size[(unsigned int) mode] * 8) : 64; 

Note the (int) cast on the true arm of the COND_EXPR.  As a result of that cast, the transformations to turn a COND_EXPR into a MIN/MAX expression in fold-const.c will not trigger.

This could be fixed by a patch to match.pd, but the pattern would only really be applicable to GENERIC and thus isn't considered a good design match for match.pd.

We could extend fold-const.c to catch this case, but that would really only help GENERIC as well.

The best option it seems would be to catch this in phi-opt which would also take us a step closer to handling pr45397.

Testcase:

/* { dg-do compile } */
/* { dg-options "-O2 -fdump-tree-original" } */


extern unsigned short mode_size[];
int
oof (int mode)
{
  return (64 < mode_size[mode] ? 64 : mode_size[mode]);
}

/* { dg-final { scan-tree-dump-times "MIN_EXPR" 1 "original" } } */


---


### compiler : `gcc`
### title : `loops not fused nor vectorized`
### open_at : `2015-07-02T12:42:38Z`
### last_modified_date : `2021-07-20T23:12:57Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=66741
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `6.0`
### severity : `enhancement`
### contents :
I would have hoped that the strcpy loop and &~0x20 loop would be fused, perusing some masked store for the tolower.

$ cat > strcpy.c <<EOF
typedef __SIZE_TYPE__ size_t;
char *tolower_strcpy(char *dest, const char *src) {
	char *ret = __builtin_strcpy(dest, src);
#if 1
	size_t sz = __builtin_strlen(dest);
	while (sz--)
#else
	while (*ret)
#endif
	{
		int ch = *ret;
		*ret = __builtin_tolower(ch);
		++ret;
	}
	return dest;
}
#ifdef MAIN
#include <unistd.h>
#include <string.h>
int main(void) {
	char src[128], dest[128];
	int n = read(0, &src, sizeof(src));
	if (n < 1)
		return 1;
	src[n] = 0;
	tolower_strcpy(dest, src);
	write(2, dest, strlen(dest));
	return 0;
}
#endif
EOF

gcc-5 -S strcpy.c -o strcpy.s -Ofast -fomit-frame-pointer -minline-all-stringops -mstringop-strategy=unrolled_loop -mtune=ivybridge


---


### compiler : `gcc`
### title : `gcc fails tail call elimination`
### open_at : `2015-07-07T11:15:31Z`
### last_modified_date : `2021-06-20T10:20:06Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=66787
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.2`
### severity : `normal`
### contents :
Created attachment 35921
source file

In the attached `test.cpp`, BlendingTable::create and BlendingTable::print are two tail-recursive functions with the same form. gcc will optimize BlendingTable::print as a loop but it fails to do so for BlendingTable::create, resulting in stack overflow.


---


### compiler : `gcc`
### title : `[ARM] Replace builtins with gcc vector extensions code`
### open_at : `2015-07-07T16:11:57Z`
### last_modified_date : `2021-08-11T10:02:24Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=66791
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `target`
### version : `6.0`
### severity : `normal`
### contents :
Lots of ARM neon intrinsics are implemented using builtins backing onto patterns in neon.md. These are opaque to the midend, but we could rewrite them using equivalent gcc vector operations, that would be transparent to the midend but would still eventually be turned into the same instructions. This would enable more optimization in the midend.

Many of the AArch64 intrinsics have been implemented in this way so AArch64 arm_neon.h may provide some useful templates.


---


### compiler : `gcc`
### title : `fold a & ((1 << b) - 1) to a & ~(-1 << b)`
### open_at : `2015-07-14T17:20:17Z`
### last_modified_date : `2021-12-25T09:05:53Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=66872
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `5.0`
### severity : `enhancement`
### contents :
This can save one or two instructions on some architectures.  For example, when compiling

int f(int x, int t)
{
	return x & ((1 << t) - 1);
}

vs.

int f(int x, int t)
{
	return x & ~(-1 << t);
}

with -march=haswell you get before:

	movl	$1, %edx
	shlx	%esi, %edx, %esi
	subl	$1, %esi               # not sure why no lea here?
	movl	%esi, %eax
	andl	%edi, %eax
	ret

and after:

	movl	$-1, %edx
	shlx	%esi, %edx, %esi
	andn	%edi, %esi, %eax
	ret

Even if you account for the strange register allocation in the first assembly listing, using andn can save one instruction.  Also, with -mtune=generic the size is the same.  Before:

	movl	%esi, %ecx
	movl	$1, %edx
	sall	%cl, %edx
	subl	$1, %edx
	movl	%edx, %eax
	andl	%edi, %eax
	ret

After:

	movl	%esi, %ecx
	movl	$-1, %edx
	sall	%cl, %edx
	notl	%edx
	movl	%edx, %eax
	andl	%edi, %eax
	ret


---


### compiler : `gcc`
### title : `function splitting only works with profile feedback`
### open_at : `2015-07-15T22:17:05Z`
### last_modified_date : `2023-05-16T22:26:36Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=66890
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `5.0`
### severity : `enhancement`
### contents :
Consider this simple example:

volatile int count;

int main()
{
        int i;
        for (i = 0; i < 100000; i++) {
                if (i == 999)
                        count *= 2;
                count++;
        }
}

The default EQ is unlikely heuristic in predict.* predicts that the if (i == 999) is unlikely. So the tracer moves the count *= 2 basic block out of line to preserve instruction cache.

gcc50 -O2 -S thotcold.c

        movl    $1, %edx
        jmp     .L2
        .p2align 4,,10
        .p2align 3
.L4:
        addl    $1, %edx
.L2:
        cmpl    $1000, %edx
        movl    count(%rip), %eax
        je      .L6
        addl    $1, %eax
        cmpl    $100000, %edx
        movl    %eax, count(%rip)
        jne     .L4
        xorl    %eax, %eax
        ret
# out of line code
.L6:
        addl    %eax, %eax
        movl    %eax, count(%rip)
        movl    count(%rip), %eax
        addl    $1, %eax
        movl    %eax, count(%rip)
        jmp     .L4


Now if we enable -freorder-blocks-and-partition I would expect it to be also put into .text.unlikely to given even better cache layout. But that's what is not happening. It generates the same code.

Only when I use actual profile feedback and -freorder-blocks-and-partition the code actually ends up being in a separate section

(it also unrolled the loop, so the code looks a bit different)

gcc -O2 -fprofile-generate -freorder-blocks-and-partition thotcold.c
./a.out 
gcc -O2 -fprofile-use -freorder-blocks-and-partition thotcold.c 
...
       .cfi_endproc
        .section        .text.unlikely
        .cfi_startproc
.L55:
        movl    count(%rip), %ecx
        addl    $1, %eax
        addl    $1, %ecx
        cmpl    $100000, %eax
        movl    %ecx, count(%rip)
        je      .L6
        cmpl    $1, %edx
        je      .L5
        cmpl    $2, %edx
        je      .L28
        cmpl    $3, %edx


-freorder-blocks-and-partition should already use the extra section even without profile feedback. 

I tested some larger programs and without profile feedback the unlikely section is always empty.

The heuristics in predict.* often work quite well and a lot of code would benefit from moving cold code out of the way of the caches.

This would allow to use the option to improve frontend bound codes without needing to do full profile feedback.


---


### compiler : `gcc`
### title : `[AVR] Shifted multiplication produces suboptimal asm`
### open_at : `2015-07-19T00:01:23Z`
### last_modified_date : `2023-04-11T19:24:03Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=66933
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `target`
### version : `5.2.0`
### severity : `enhancement`
### contents :
The function

    uint8_t test(uint8_t a, uint8_t b) { return (a*b) >> 7; }

compiles into the following assembly, with e.g.
    
    avr-gcc -mmcu=atmega328 -S -O3 test.c

(or any other optimization flag)

    test:
        mul r24,r22
        movw r24,r0
        clr __zero_reg__
        lsl r24
        mov r24,r25
        rol r24
        sbc r25,r25
        ret

This has two obvious possible enhancements:
- It uses mul instead of fmul: fmul calculates (a*b)<<1,
  so the high byte is already the correct return value of
  the function
- After calculating the return value (wih "rol r24"),
  there's an instruction "sbc r25, r25" that puts a
  completely unneeded value in r25, if I'm not mistaken
  it's 255 if (a*b) & 0x8000, else 0.

A better version that uses 8 instead of 12 cycles would be

    test:
        fmul r24, r22
        mov r24, r1
        clr __zero_reg__
        ret


---


### compiler : `gcc`
### title : `[graphite] delinearization of arrays`
### open_at : `2015-07-23T21:16:17Z`
### last_modified_date : `2021-10-01T02:58:41Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=66981
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `6.0`
### severity : `normal`
### contents :
Graphite needs to delinearize the memory accesses in this loop to do vectorization and parallelization:

$ cat s.c
void foo(unsigned char *in, unsigned char *out, int w, int h)
{
  unsigned int i, j;
  for (i = 0; i < 3*w*h; i++)
    for (j = 0; j < 3*w*h; j++)
      out[i*w+j] = in[(i*w+j)*3] + in[(i*w+j)*3+1] + in[(i*w+j)*3+2];
}

$ gcc -O3 -floop-parallelize-all s.c

Polly vectorizes this loop with vector factor 16.


---


### compiler : `gcc`
### title : `tree_single_nonnegative_warnv_p and fold_relational_const are inconsistent with NaNs`
### open_at : `2015-07-29T09:03:05Z`
### last_modified_date : `2022-10-27T15:27:08Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=67052
### status : `UNCONFIRMED`
### tags : `missed-optimization, wrong-code`
### component : `middle-end`
### version : `6.0`
### severity : `normal`
### contents :
int main ()
{
  double x = __builtin_nan ("");
  if (x < 0.0)
    return 1;
  return 0;
}

this simplifies via

      /* Convert ABS_EXPR<x> < 0 to false.  */
      strict_overflow_p = false;
      if (code == LT_EXPR
          && (integer_zerop (arg1) || real_zerop (arg1))
          && tree_expr_nonnegative_warnv_p (arg0, &strict_overflow_p))
        {
          if (strict_overflow_p)
            fold_overflow_warning (("assuming signed overflow does not occur "
                                    "when simplifying comparison of "
                                    "absolute value and zero"),
                                   WARN_STRICT_OVERFLOW_CONDITIONAL);
          return omit_one_operand_loc (loc, type,
                                       constant_boolean_node (false, type),
                                       arg0);
        }

(the ABS_EXPR<x> >= 0 case is guarded with ! HONOR_NANS)

but not via constant folding in fold_relational_const.

bool
tree_single_nonnegative_warnv_p (tree t, bool *strict_overflow_p)
{
...
    case REAL_CST:
      return ! REAL_VALUE_NEGATIVE (TREE_REAL_CST (t));

but

static tree
fold_relational_const (enum tree_code code, tree type, tree op0, tree op1)
{
...
      /* Handle the cases where either operand is a NaN.  */
      if (real_isnan (c0) || real_isnan (c1))
        {
...
            case LT_EXPR:
            case LE_EXPR:
            case GT_EXPR:
            case GE_EXPR:
            case LTGT_EXPR:
              if (flag_trapping_math)
                return NULL_TREE;

is this a missed optimization or wrong-code?


---


### compiler : `gcc`
### title : `[11/12/13/14 Regression] integer optimizations 53% slower than std::bitset<>`
### open_at : `2015-08-07T23:54:19Z`
### last_modified_date : `2023-07-07T10:30:53Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=67153
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `8.1.0`
### severity : `normal`
### contents :
Created attachment 36146
The std::bitset<> version

I have attached two small, semantically equivalent C++14 programs.

One uses std::bitset<26> for its operations; the other uses raw unsigned int.
The one that uses unsigned int runs 53% slower than the bitset<> version, as
compiled with g++-5.1 and running on a 2013-era Haswell i7-4770.  While this
represents, perhaps, a stunning triumph in the optimization of inline member
and lambda functions operating on structs, it may represent an equally
intensely embarrassing, even mystifying, failure for optimization of the
underlying raw integer operations.

For both, build and test was with

  $ g++-5 -O3 -march=native -mtune=native -g3 -Wall $PROG.cc
  $ time ./a.out | wc -l
  2818

Times on a 3.2GHz Haswell are consistently 0.25s for the unsigned int
version, 0.16s for the std::bitset<26> version.

These programs are archived at <https://github.com/ncm/nytm-spelling-bee/>.

The runtimes of the two versions are identical as built and run on my
2009 Westmere 2.4GHz i5-M520, and about the same as the integer version
on Haswell.


---


### compiler : `gcc`
### title : `[11/12/13/14 Regression] Missed jump thread and false positive from -Wuninitialized`
### open_at : `2015-08-12T17:19:53Z`
### last_modified_date : `2023-07-07T10:30:55Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=67194
### status : `NEW`
### tags : `diagnostic, missed-optimization`
### component : `tree-optimization`
### version : `4.8.0`
### severity : `normal`
### contents :
Extracted from bz55035:

Reconfirmed.

Nowadays (trunk@221914) also breaks all-gcc for nios2-linux-gnu.
Reminds me of bug #36550

Smallish testcase:

$ cat reload1.i ; echo EOF
/* PR target/55035 */
/* { dg-do compile } */
/* { dg-options "-O2 -W -Wall -Werror" } */
struct rtx_def;
typedef struct rtx_def *rtx;
enum rtx_code {
  UNKNOWN,
  INSN, 
  ASM_INPUT,
  CLOBBER
};
struct rtx_def {
  enum rtx_code code: 4;
};
class rtx_def;
class rtx_insn : public rtx_def {};
struct recog_data_d
{
  rtx operand[30];
  rtx *operand_loc[30];
  rtx *dup_loc[1];
  char dup_num[1];
  char n_operands;
  char n_dups;
};
extern struct recog_data_d recog_data;
extern int get_int(void);
void
elimination_costs_in_insn (rtx_insn *insn)
{
  int icode = get_int ();
  int i;
  rtx orig_operand[30];
  rtx orig_dup[30];
  if (icode < 0)
    {
      if (((enum rtx_code) insn->code) == INSN)
        __builtin_abort();
      return;
    }
  for (i = 0; i < recog_data.n_dups; i++)
    orig_dup[i] = *recog_data.dup_loc[i];
  for (i = 0; i < recog_data.n_operands; i++)
    {
      orig_operand[i] = recog_data.operand[i];
      if (orig_operand[i]->code == CLOBBER)
        *recog_data.operand_loc[i] = 0;
    }
  for (i = 0; i < recog_data.n_dups; i++)
    *recog_data.dup_loc[i]
      = *recog_data.operand_loc[(int) recog_data.dup_num[i]];
  for (i = 0; i < recog_data.n_dups; i++)
    *recog_data.dup_loc[i] = orig_dup[i];
}
EOF

$ g++ -O2 -W -Wall -Werror -c reload1.i -o reload1.o
reload1.i: In function ‘void elimination_costs_in_insn(rtx_insn*)’:
reload1.i:53:41: error: ‘orig_dup[0]’ may be used uninitialized in this function [-Werror=maybe-uninitialized]
     *recog_data.dup_loc[i] = orig_dup[i];
                                         ^
cc1plus: all warnings being treated as errors

And a second, related testcase:

typedef struct rtx_def *rtx;
struct recog_data_d
{
  rtx operand;
  char n_dups;
};

rtx *operand_loc;
rtx dup_loc;

struct recog_data_d recog_data;

void elimination_costs_in_insn ()
{
  rtx orig_dup;
  if (recog_data.n_dups)
      orig_dup = dup_loc;
  *operand_loc = 0;
  if (recog_data.n_dups)
      dup_loc = orig_dup;
}

A warning is issued even at -O1. If I remove "rtx operand" field from struct recog_data_d (or if I change the type of n_dups to int), then it disappears at -O2 (but still present at -O1).

In both cases the -Wuninitialized warning is bogus and points to a miss jump threading opportunity.


---


### compiler : `gcc`
### title : `Redundant spills in simple copy loop for 32-bit x86 target`
### open_at : `2015-08-13T14:46:48Z`
### last_modified_date : `2021-07-25T00:48:27Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=67206
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `6.0`
### severity : `normal`
### contents :
For attached simple test-case we can see strange spills to stack, namely
    for (i=0; i<n; i++)
      out[j * n + i] = in[j * n + i];

.L9:
	movdqa	(%eax), %xmm0
	addl	$1, %edx
	movdqu	%xmm0, (%ecx)
	addl	$16, %eax
	movdqa	%xmm0, 32(%esp)  ?? Redundant
	addl	$16, %ecx
	movl	%eax, 32(%esp)   ?? Redundant
	cmpl	52(%esp), %edx
	movl	%ecx, 48(%esp)   ?? Redundant
	jb	.L9

Another issue is that loop distribution is not recognized such loop and memmove loop. Note that this is reproduced with 4-9 compiler.


---


### compiler : `gcc`
### title : `Missing optimization with float IV in SCEV-CCP`
### open_at : `2015-08-16T20:12:52Z`
### last_modified_date : `2021-12-15T21:56:45Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=67242
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.3`
### severity : `enhancement`
### contents :
testcase:

int n, dummy;
float dummyfloat;

void bug(void) 
{
 for(n=0; n<1000; n++)
    dummy = n;
 for(n=0; n<1000; n++)
    dummyfloat = n;
}

the first loop (dummy=) is optimized away with -O2 and -O3
the second (dummyfloat=) NOT.

Tested with 4.9.2 & 4.9.3, targets x86-64, arm-thumb and arm.

commandline: gcc -O2 bug.c -S


---


### compiler : `gcc`
### title : `FRE should CSE sqrt() calls even with -ferrno-math`
### open_at : `2015-08-20T08:26:36Z`
### last_modified_date : `2021-12-04T21:28:07Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=67287
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `6.0`
### severity : `normal`
### contents :
double sqrt(double x);
double t (double x)
{
  double a = sqrt (x);
  double b = sqrt (x);
  return a * b;
}

should be optimized to

double t (double x)
{
  double a = sqrt (x);
  return a * a;
}

with -fmath-errno.  FRE currently gives up too early and the alias oracle
can handle errno-style references (but it can't use a call as a "ref", so
the "errno"-only side-effect has to be modeled by creating a special ref
for performing the walking for math builtins setting errno as their only
side-effect).

We may not miscompile

  sqrt (x);
  errno = 0;
  sqrt (x);
  if (errno != 0)
   ...

to CSE the second sqrt.


---


### compiler : `gcc`
### title : `[9/10/11/12 regression] non optimal simple function (useless additional shift/remove/shift/add)`
### open_at : `2015-08-20T08:29:41Z`
### last_modified_date : `2021-07-14T16:14:19Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=67288
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.9.3`
### severity : `normal`
### contents :
The following function (Linux Kernel, compiled with -O2) was resulting in a good assembly with GCC 4.8.3. With GCC 4.9.3 there are a lot of unneccessary instructions

/* L1_CACHE_BYTES = 16 */
/* L1_CACHE_SHIFT = 4 */

#define mb()   __asm__ __volatile__ ("sync" : : : "memory")

static inline void dcbf(void *addr)
{
	__asm__ __volatile__ ("dcbf 0, %0" : : "r"(addr) : "memory");
}

void flush_dcache_range(unsigned long start, unsigned long stop)
{
	void *addr = (void *)(start & ~(L1_CACHE_BYTES - 1));
	unsigned int size = stop - (unsigned long)addr + (L1_CACHE_BYTES - 1);
	unsigned int i;

	for (i = 0; i < size >> L1_CACHE_SHIFT; i++, addr += L1_CACHE_BYTES)
		dcbf(addr);
	if (i)
		mb();
}

Result with GCC 4.9.3: (15 insns)

c000d970 <flush_dcache_range>:
c000d970:       54 63 00 36     rlwinm  r3,r3,0,0,27
c000d974:       38 84 00 0f     addi    r4,r4,15
c000d978:       7c 83 20 50     subf    r4,r3,r4
c000d97c:       54 89 e1 3f     rlwinm. r9,r4,28,4,31
c000d980:       4d 82 00 20     beqlr   
c000d984:       55 24 20 36     rlwinm  r4,r9,4,0,27
c000d988:       39 24 ff f0     addi    r9,r4,-16
c000d98c:       55 29 e1 3e     rlwinm  r9,r9,28,4,31
c000d990:       39 29 00 01     addi    r9,r9,1
c000d994:       7d 29 03 a6     mtctr   r9
c000d998:       7c 00 18 ac     dcbf    0,r3
c000d99c:       38 63 00 10     addi    r3,r3,16
c000d9a0:       42 00 ff f8     bdnz    c000d998 <flush_dcache_range+0x28>
c000d9a4:       7c 00 04 ac     sync    
c000d9a8:       4e 80 00 20     blr

The following section is just useless: (shift left 4 bits, remove 16, shift right 4 bits, add 1)
c000d984:       55 24 20 36     rlwinm  r4,r9,4,0,27
c000d988:       39 24 ff f0     addi    r9,r4,-16
c000d98c:       55 29 e1 3e     rlwinm  r9,r9,28,4,31
c000d990:       39 29 00 01     addi    r9,r9,1



Result with GCC 4.8.3 was correct: (11 insns)

c000d894 <flush_dcache_range>:
c000d894:       54 63 00 36     rlwinm  r3,r3,0,0,27
c000d898:       38 84 00 0f     addi    r4,r4,15
c000d89c:       7d 23 20 50     subf    r9,r3,r4
c000d8a0:       55 29 e1 3f     rlwinm. r9,r9,28,4,31
c000d8a4:       4d 82 00 20     beqlr   
c000d8a8:       7d 29 03 a6     mtctr   r9
c000d8ac:       7c 00 18 ac     dcbf    0,r3
c000d8b0:       38 63 00 10     addi    r3,r3,16
c000d8b4:       42 00 ff f8     bdnz    c000d8ac <flush_dcache_range+0x18>
c000d8b8:       7c 00 04 ac     sync    
c000d8bc:       4e 80 00 20     blr


---


### compiler : `gcc`
### title : `[ARM][6 Regression] FAIL: gcc.target/arm/builtin-bswap-1.c scan-assembler-times revshne\\t 1`
### open_at : `2015-08-20T13:59:55Z`
### last_modified_date : `2020-09-01T09:57:26Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=67295
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `6.0`
### severity : `normal`
### contents :
After the big copyrename patch r226901 I'm seeing these two fails on arm:
FAIL: gcc.target/arm/builtin-bswap-1.c scan-assembler-times revshne\\t 1
FAIL: gcc.target/arm/builtin-bswap-1.c scan-assembler-times rev16ne\\t 1

The reduced part from these tests is:

extern short foos16 (short);

/* revshne */
short swaps16_cond (short x, int y)
{
  short z = x;
  if (y)
    z = __builtin_bswap16 (x);
  return foos16 (z);
}


Compile with -O2.
With the new revision we generate:
        cmp     r1, #0
        rev16ne r0, r0
        uxthne  r0, r0
.L2:
        sxth    r0, r0
        b       foos16

whereas before that we generated:
        cmp     r1, #0
        revshne r0, r0
.L2:
        b       foos16


Never mind the extra label, I think that's a practically harmless artifact of if-conversion.
My arm-none-eabi cross compiler was configured with:
--with-arch=armv7-a --with-float=hard --with-fpu=neon-vfpv4

Note, the subsequent commit:
Author: aoliva <aoliva@138bc75d-0d04-0410-961f-82ee72b054a4>
Date:   Wed Aug 19 17:00:32 2015 +0000

    [PR64164] fix regressions reported on m68k and armeb
    
    Defer stack slot address assignment for all parms that can't live in
    pseudos, and accept pseudos assignments in assign_param_setup_block.
    
    for  gcc/ChangeLog
    
        PR rtl-optimization/64164
        * cfgexpand.c (parm_maybe_byref_p): Renamed to...
        (parm_in_stack_slot_p): ... this.  Disregard mode, what
        matters is whether the parm will live in a pseudo or a stack
        slot.
        (expand_one_ssa_partition): Deal with params without a default
        def.  Disregard mode.
        * cfgexpand.h: Renamed function declaration.
        * tree-ssa-coalesce.c: Adjust.
        * function.c (split_complex_args): Allocate stack slot for
        unassigned parms before splitting.
        (parm_in_unassigned_mem_p): New.  Use it instead of
        parm_maybe_byref_p throughout this file.
        (assign_parm_setup_block): Use it.  Accept pseudos in the
        expand-assigned rtl.
        (assign_parm_setup_reg): Drop BLKmode requirement.
        (assign_parm_setup_stack): Allocate and fill in the address of
        unassigned MEM parms.
    
    git-svn-id: svn+ssh://gcc.gnu.org/svn/gcc/trunk@227015 138bc75d-0d04-0410-961f-82ee72b054a4

didn't fix this.

Let me know if any more information is needed


---


### compiler : `gcc`
### title : `Use non-unit stride loads by preference when applicable`
### open_at : `2015-08-23T03:14:05Z`
### last_modified_date : `2021-05-04T12:32:17Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=67323
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `6.0`
### severity : `normal`
### contents :
On arm targets the following code fails to generate a vld3:

struct pixel {
  char r,g,b;
};

void 
t2(int len, struct pixel * __restrict p, struct pixel * __restrict x)
{
  len = len & ~31;
  for (int i = 0; i < len; i++){
      p[i].r = x[i].r * 2;
      p[i].g = x[i].g * 3;
      p[i].b = x[i].b * 4;
  }
}

Yes the same code with line 11 changed to:

p[i].g = x[i].g;

does generate a vld3.


---


### compiler : `gcc`
### title : `RTL combiner is too eager to combine (plus (reg 92) (reg 92)) to (ashift (reg 92) (const_int 1))`
### open_at : `2015-08-28T12:27:21Z`
### last_modified_date : `2021-07-25T21:07:32Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=67382
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `6.0`
### severity : `normal`
### contents :
Following testcase:

--cut here--
extern void abort (void);

void test (void)
{
  unsigned char c = 0;
  unsigned int x = 0xFFFFFFFF;
  unsigned int y = 0xFFFFFFFF;
  unsigned int sum_ref = 0xFFFFFFFE;

  /* X = 0xFFFFFFFF, Y = 0xFFFFFFFF, C = 0.  */
  c = __builtin_ia32_addcarryx_u32 (c, x, y, &x);

  /* X = 0xFFFFFFFE, Y = 0xFFFFFFFF, C = 1.  */
  c = __builtin_ia32_addcarryx_u32 (c, x, y, &x);
  /* X = 0xFFFFFFFE, Y = 0xFFFFFFFF, C = 1.  */

  if (x != sum_ref)
    abort ();
}
--cut here--

compiles to unoptimized code on x86_64-linux-gnu with -O2:

        movl    $-1, %edx
        movl    $-4, %eax
        subq    $24, %rsp
        addl    %edx, %eax
        adcl    %edx, %eax
        cmpl    $-2, %eax
        movl    %eax, 12(%rsp)
        jne     .L5
        addq    $24, %rsp
        ret
.L5:
        call    abort

The problem is with combine pass, which tries to combine:

(insn 10 7 11 2 (parallel [
            (set (reg:CCC 17 flags)
                (compare:CCC (plus:QI (reg:QI 91)
                        (const_int -1 [0xffffffffffffffff]))
                    (reg:QI 91)))
            (clobber (scratch:QI))
        ]) carry.c:11 292 {*addqi3_cconly_overflow}
     (expr_list:REG_DEAD (reg:QI 91)
        (expr_list:REG_EQUAL (compare:CCC (const_int -1 [0xffffffffffffffff])
                (const_int 0 [0]))
            (nil))))
(insn 11 10 12 2 (parallel [
            (set (reg:CCC 17 flags)
                (compare:CCC (plus:SI (plus:SI (ltu:SI (reg:CCC 17 flags)
                                (const_int 0 [0]))
                            (reg:SI 92))
                        (reg:SI 92))
                    (reg:SI 92)))
            (set (reg:SI 95)
                (plus:SI (plus:SI (ltu:SI (reg:CCC 17 flags)
                            (const_int 0 [0]))
                        (reg:SI 92))
                    (reg:SI 92)))
        ]) carry.c:11 283 {addcarrysi}
     (nil))

to:

Trying 10 -> 11:
Failed to match this instruction:
(parallel [
        (set (reg:CC 17 flags)
            (compare:CC (ashift:SI (reg:SI 92)
                    (const_int 1 [0x1]))
                (reg:SI 92)))
        (set (reg:SI 95)
            (ashift:SI (reg:SI 92)
                (const_int 1 [0x1])))
    ])
Failed to match this instruction:
(parallel [
        (set (reg:CC 17 flags)
            (compare:CC (ashift:SI (reg:SI 92)
                    (const_int 1 [0x1]))
                (reg:SI 92)))
        (set (reg:SI 95)
            (ashift:SI (reg:SI 92)
                (const_int 1 [0x1])))
    ])

Please note that combine pass converts

(plus (reg 92) (reg 92))

to

(ashift (reg 92) (const_int 1)

and combined pattern fails.

BTW: The duplicate pattern is copied verbatim from the dump. It looks like combine is trying to do something with unrecognized pattern to re-recognize it.

When we change e.g.:

  unsigned int x = 0xFFFFFFFF;

to

  unsigned int x = 0xFFFFFFFC;

we get the expected pattern:

Trying 10 -> 11:
Successfully matched this instruction:
(parallel [
        (set (reg:CCC 17 flags)
            (compare:CCC (plus:SI (reg:SI 92)
                    (reg:SI 93))
                (reg:SI 92)))
        (set (reg:SI 95)
            (plus:SI (reg:SI 92)
                (reg:SI 93)))
    ])


---


### compiler : `gcc`
### title : `Complex NOP expanded to several operations`
### open_at : `2015-08-31T14:43:38Z`
### last_modified_date : `2023-06-25T22:14:47Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=67413
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `6.0`
### severity : `enhancement`
### contents :
_Complex unsigned f(_Complex int i){return i;}

yields

	movl	%edi, %eax
	shrq	$32, %rdi
	salq	$32, %rdi
	orq	%rdi, %rax
	ret

I read somewhere that complex integers are a deprecated gcc extension, but gcc only warns in pedantic mode, and it should not be too hard to improve the generated code.

Note that tree optimizers currently also fail to optimize the corresponding code:

long f(long x){
  long y = x >> 32;
  y <<= 32;
  int z = x;
  return z | y;
}

(using & CST instead of >> and << does not help)


---


### compiler : `gcc`
### title : `resolution to constant fails between pointer on stack and pointer within argument structure`
### open_at : `2015-09-01T09:14:18Z`
### last_modified_date : `2021-12-25T08:10:46Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=67418
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `5.2.0`
### severity : `enhancement`
### contents :
Hi,

In the code below, gcc version 4.8.4, 4.9.3, and 5.2.0 fail to resolve the expression temp != a->x as being a constant, while all succeed in resolving temp != b.

It seems to me however that no valid code can reach either temp==b or temp==a->x. Shouldn't gcc decide then that temp != a->x is constant and equal to true in this case ? Please correct me if I am wrong.

[I've run into this as being the cause of an unexpected uninitialized warning, whose root cause is this constant problem]

E.

struct container {
    unsigned long * x;
};

int bang() __attribute__((error("should never be called")));
#define MUST_BE_CONSTANT(c) do {   \
    int n __attribute__((unused)) = __builtin_constant_p((c)) ? 0 : bang(); \
} while (0)

void test(struct container * a, unsigned long * b)
{
    unsigned long temp[1];
    MUST_BE_CONSTANT(temp != b);           // passes ok.
    MUST_BE_CONSTANT(temp != a->x);        // fails to decide it holds
}


/*

$ ./gcc-5.2.0/bin/gcc -O2 -Wextra /tmp/a.c -c
/tmp/a.c: In function ‘test’:
/tmp/a.c:7:67: error: call to ‘bang’ declared with attribute error: should never be called
     int n __attribute__((unused)) = __builtin_constant_p((c)) ? 0 : bang(); \
                                                                   ^
/tmp/a.c:14:5: note: in expansion of macro ‘MUST_BE_CONSTANT’
     MUST_BE_CONSTANT(temp != a->x);        // fails to decide it holds

                   ^
$ uname -a
Linux localhost 4.1.0-1-amd64 #1 SMP Debian 4.1.3-1 (2015-08-03) x86_64 GNU/Linux

$ lsb_release -a
No LSB modules are available.
Distributor ID: Debian
Description:    Debian GNU/Linux testing (stretch)
Release:        testing
Codename:       stretch

$ ./gcc-5.2.0/bin/gcc -v
Using built-in specs.
COLLECT_GCC=/opt/gcc-5.2.0/bin/gcc
COLLECT_LTO_WRAPPER=/opt/gcc-5.2.0/libexec/gcc/x86_64-unknown-linux-gnu/5.2.0/lto-wrapper
Target: x86_64-unknown-linux-gnu
Configured with: ../gcc-5.2.0/configure --prefix=/opt/gcc-5.2.0 --enable-languages=c,c++
Thread model: posix
gcc version 5.2.0 (GCC) 

 */


---


### compiler : `gcc`
### title : `Feature request: Implement align-loops attribute`
### open_at : `2015-09-02T13:24:37Z`
### last_modified_date : `2021-08-16T06:40:45Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=67435
### status : `NEW`
### tags : `missed-optimization`
### component : `c`
### version : `4.8.4`
### severity : `normal`
### contents :
Some weird effect with gcc (tested version : 4.8.4).

I've got a performance oriented code, which runs pretty fast. Its speed depends for a large part on inlining many small functions.
There is no inline statement. All functions are either normal or static. Automatic inlining decision is solely within compiler's realm, which has worked fine so far (functions to inline are very small, typically from 1 to 5 lines).

Since inlining across multiple .c files is difficult (-flto is not yet widely available), I've kept a lot of small functions into a single `.c` file, into which I'm also developing a codec, and its associated decoder. It's "relatively" large by my standard (about ~2000 lines, although a lot of them are mere comments and blank lines), but breaking it into smaller parts opens new problems, so I would prefer to avoid that, if that is possible.

Encoder and Decoder are related, since they are inverse operations. But from a programming perspective, they are completely separated, sharing nothing in common, except a few typedef and very low-level functions (such as reading from unaligned memory position).

The strange effect is this one :

I recently added a new function fnew to the encoder side. It's a new "entry point". It's not used nor called from anywhere within the .c file.

The simple fact that it exists makes the performance of the decoder function fdec drops substantially, by more than 20%, which is way too much to be ignored.

Now, keep in mind that encoding and decoding operations are completely separated, they share almost nothing, save some minor typedef (u32, u16 and such) and associated operations (read/write).

When defining the new encoding function fnew as static, performance of the decoder fdec increases back to normal. Since fnew isn't called from the .c, I guess it's the same as if it was not there (dead code elimination).

If static fnew is now called from the encoder side, performance of fdec remains good.
But as soon as fnew is modified, fdec performance just drops substantially.

Presuming fnew modifications crossed a threshold, I increased the following gcc parameter : --param max-inline-insns-auto=60 (by default, its value is supposed to be 40.) And it worked : performance of fdec is now back to normal.

But I guess this game will continue forever with each little modification of fnew or anything else similar, requiring further tweak on some customized advance parameter. So I want to avoid that.

I tried another variant : I'm adding another completely useless function, just to play with. Its content is strictly exactly a copy-paste of fnew, but the name of the function is obviously different, so let's call it wtf.

When wtf exists (on top of fnew), it doesn't matter if fnew is static or not, nor what is the value of max-inline-insns-auto : performance of fdec is just back to normal. Even though wtf is not used nor called from anywhere... :'(


All these effects look plain weird. There is no logical reason for some little modification in function fnew to have knock-on effect on completely unrelated function fdec, which only relation is to be in the same file.

I'm trying to understand what could be going on, in order to develop the codec more reliably. 
For the time being, any modification in function A can have large ripple effects (positive or negative) on completely unrelated function B, making each step a tedious process with random outcome. A developer's nightmare.


---


### compiler : `gcc`
### title : `[6 Regression] ~X op ~Y pattern relocation causes loop performance degradation on 32bit x86`
### open_at : `2015-09-02T17:29:35Z`
### last_modified_date : `2023-10-15T23:12:04Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=67438
### status : `RESOLVED`
### tags : `missed-optimization, ra`
### component : `middle-end`
### version : `6.0`
### severity : `normal`
### contents :
For the loop in the attached test compiled with -O3 -m32 -march=slm -ftree-loop-if-convert (in fact, -march=slm can be omitted resulting in a greater number of insns) after r225249 we generate 28 insns instead of 23 insns for r225248. That revision moves some simplification patterns from fold-const.c to match.pd, and I've noticed that relocating back ~X op ~Y -> Y op X from match.pd to fold-const.c fixes the problem.

r225248:
movzbl (%ebx),%ecx
add    $0x3,%ebx
movzbl -0x2(%ebx),%edx
not    %ecx
movzbl -0x1(%ebx),%eax
not    %edx
mov    %cl,(%esi)
mov    %dl,0x1(%esi)
not    %eax
cmp    %al,%cl
mov    %eax,%edi
mov    %al,0x2(%esi)
mov    %eax,%ebp
cmovle %ecx,%edi
cmp    %al,%dl
cmovle %edx,%ebp
add    $0x4,%esi
cmp    %dl,%cl
mov    %ebp,%eax
cmovl  %edi,%eax
cmp    (%esp),%ebx
mov    %al,-0x1(%esi)
jne    30 <foo+0x30>

r225249:
movzbl (%edi),%eax
add    $0x3,%edi
movzbl -0x2(%edi),%edx
mov    %al,0x2(%esp)
mov    %eax,%ebx
movzbl -0x1(%edi),%eax
not    %ebx
mov    %dl,0x3(%esp)
mov    %edx,%ecx
mov    %bl,0x0(%ebp)
not    %ecx
mov    %cl,0x1(%ebp)
not    %eax
cmp    %al,%bl
mov    %eax,%esi
mov    %al,0x2(%ebp)
cmovle %ebx,%esi
cmp    %al,%cl
mov    %esi,%edx
mov    %eax,%esi
cmovle %ecx,%esi
add    $0x4,%ebp
movzbl 0x3(%esp),%ecx
cmp    %cl,0x2(%esp)
cmovle %esi,%edx
cmp    0x4(%esp),%edi
mov    %dl,-0x1(%ebp)
jne    30 <foo+0x30>


---


### compiler : `gcc`
### title : `Scheduler unable to disambiguate memory references in unrolled loop`
### open_at : `2015-09-03T02:39:04Z`
### last_modified_date : `2022-03-08T16:20:59Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=67441
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `6.0`
### severity : `enhancement`
### contents :
The following shows an example where the scheduler is unable to disambiguate memory references inside the unrolled loop, which prevents any motion of the loads above the (non-overlapping) preceding stores.

pthaugen@genoa:~/temp/unroll-alias$ cat junk.c
#define SIZE 1024

double x[SIZE] __attribute__ ((aligned (16)));

void do_one(void)
{
  unsigned long i;

  for (i = 0; i < SIZE; i++)
    x[i] = x[i] + 1.0;
}
pthaugen@genoa:~/temp/unroll-alias$ ~/install/gcc/trunk/bin/gcc -O3 -funroll-loops -S junk.c -mcpu=power8

Following is generated, which shows the loop unrolled, but no movement of the loads/adds, so we basically have back to back copies of the loop body.

.L2:
        lxvd2x 12,0,9
        addi 4,9,16
        addi 11,9,32
        addi 5,9,48
        addi 6,9,64
        addi 7,9,80
        addi 8,9,96
        addi 12,9,112
        xvadddp 1,12,0
        stxvd2x 1,0,9
        addi 9,9,128
        lxvd2x 2,0,4
        xvadddp 3,2,0
        stxvd2x 3,0,4
        lxvd2x 4,0,11
        xvadddp 5,4,0
        stxvd2x 5,0,11
        lxvd2x 6,0,5
        xvadddp 7,6,0
        stxvd2x 7,0,5
        lxvd2x 8,0,6
        xvadddp 9,8,0
        stxvd2x 9,0,6
        lxvd2x 10,0,7
        xvadddp 11,10,0
        stxvd2x 11,0,7
        lxvd2x 13,0,8
        xvadddp 12,13,0
        stxvd2x 12,0,8
        lxvd2x 1,0,12
        xvadddp 2,1,0
        stxvd2x 2,0,12
        bdnz .L2


An example store/load sequence looks like the following at sched1 timeframe, where r193 coming in was set to r170+64.

(insn 81 80 82 3 (set (mem:V2DF (reg:DI 193 [ ivtmp.14 ]) [1 MEM[base: _7, offset: 0B]+0 S16 A128])
        (reg:V2DF 196 [ vect__5.6 ])) junk.c:12 886 {*vsx_movv2df}
     (expr_list:REG_DEAD (reg:V2DF 196 [ vect__5.6 ])
        (expr_list:REG_DEAD (reg:DI 193 [ ivtmp.14 ])
            (nil))))
(insn 82 81 90 3 (set (reg:DI 197 [ ivtmp.14 ])
        (plus:DI (reg:DI 170 [ ivtmp.14 ])
            (const_int 80 [0x50]))) 81 {*adddi3}
     (nil))
(insn 90 82 91 3 (set (reg:V2DF 199 [ MEM[base: _7, offset: 0B] ])
        (mem:V2DF (reg:DI 197 [ ivtmp.14 ]) [1 MEM[base: _7, offset: 0B]+0 S16 A128])) junk.c:12 886 {*vsx_movv2df}
     (nil))

The str/ld use different base regs, and the fact that they're both based off r170+displ is lost when we're just looking at the two mem refs during the sched-deps code. So it falls back to the tree aliasing oracle where they both have the same MEM expr with offset 0 so are not disambiguated.

Not sure if unroller should be creating new tree MEM expr with appropriate offsets so the mem's can be seen as not overlapping or if sched-deps code needs to be enhanced to try and incorporate the base reg increment so that the rtl base/displ is clearly seen and can be disambiguated that way.


---


### compiler : `gcc`
### title : `Branch elimination problem on x86`
### open_at : `2015-09-04T10:26:49Z`
### last_modified_date : `2021-08-14T07:56:32Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=67449
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.9.3`
### severity : `enhancement`
### contents :
The following `do ... while` statement creates a loop with two branches:

C code:
<code>
    int a[10];
    
    void next(int **pp){
        (++*pp == a + 10) && (*pp = 0);
    }
    
    int main(){
        for(int i = 0; i < 10; ++i){
            a[i] = i;
        }
    
        int *p = a;
        do {
            __builtin_printf("element = %d\n", *p);
            next(&p);
    //      __asm__("");
        } while(p);
    }
</code>

Assembly output:
<code>
    L13:
        testl   %ebx, %ebx
        je  L6                      ; one here.
    L4:
        movl    (%ebx), %eax
        movl    $LC1, (%esp)
        addl    $4, %ebx
        movl    %eax, 4(%esp)
        call    _printf
        cmpl    $_a+40, %ebx
        jne L13                     ; another one here.
    L6:
</code>

But if we uncomment that empty __asm__ statement, the first branch vanishes:

Assembly output:
<code>
    L5:
        movl    (%ebx), %eax
        movl    $LC1, (%esp)
        addl    $4, %ebx
        movl    %eax, 4(%esp)
        call    _printf
        cmpl    $_a+40, %ebx
        cmove   %esi, %ebx
        testl   %ebx, %ebx          ; the only one branch in this loop.
        jne L5
</code>


---


### compiler : `gcc`
### title : `Multiple atomic stores generate a StoreLoad barrier between each one, not just at the end`
### open_at : `2015-09-05T12:44:24Z`
### last_modified_date : `2021-10-02T18:43:25Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=67461
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `5.2.0`
### severity : `enhancement`
### contents :
Multiple atomic stores in a row generate multiple barriers.

I noticed this while playing around with the same code that led to https://gcc.gnu.org/bugzilla/show_bug.cgi?id=67458.  This is a separate issue, but if I left out any context, look at that bug.

I suspect this is a case of correctness trumps performance, since atomics are still new.  These cases are probably just missing optimizations for weird use-cases, and fixing them is not very likely to benefit real code (unless it over-uses atomics).



#include <atomic>
std::atomic<int> a, c;
void simple_set(void){ a=1; a=1; a=3; c=2; a=3; }

compiles to (x86, g++ 5.2.0 -O3, on godbolt.org)

	movl	$1, %eax
	movl	%eax, a(%rip)  # a=1
	mfence
	movl	%eax, a(%rip)  # a=1
	movl	$3, %eax
	mfence
	movl	%eax, a(%rip)  # a=3
	mfence
	movl	$2, c(%rip)    # c=2
	mfence
	movl	%eax, a(%rip)  # a=3
	mfence
	ret

First, does the C++ standard actually require multiple stores to the same variable in a row, if there are no intervening loads or stores in the source?  I would have thought that at least a=1; a=1; would collapse to a single store.  

Consider
  initially: a=0
  thread1: a=1; a=1;
  thread2: tmp=a.exchange(2); tmp2=a;

These operations have to happen in some order, but isn't the compiler allowed to make decisions at compile-time that eliminate some possible orders?  e.g. collapsing both a=1 operations into a single store would make this impossible:

  a=1; tmp=a.exchange(2); a=1; tmp2=a; 

But the remaining two orderings are valid, and I think it would be an error for software to depend on that interleaved ordering being possible.  Does the standard require generation of machine code that can end up with tmp=1, tmp2=1?  If it does, then this isn't a bug.  >.<

More generally, collapsing a=1; a=3;  into a single store should be ok for the same reason.

 A producer thread doing stores separated by StoreStore barriers to feed a consumer thread doing loads separated by LoadLoad barriers gives no guarantee that the consumer doesn't miss some events.

-----------

There are no loads between the stores, so I don't understand having multiple StoreLoad barriers (mfence), unless that's just a missing optimization, too.

Are the mfence instructions between each store supposed to protect a signal handler from something?  An interrupt could come in after the first store, but before the first mfence.  (clang uses (lock) xchg for each atomic store with sequential consistency, which would prevent the possibility of an interrupt between the store and the mfence).

 I guess if the signal handler sees a=3, it knows that the mfence between a=1 and a=3 has already happened, but not necessarily the mfence after a=3.

 If these extra mfences in a sequence of stores are just for the potential benefit of a signal handler, doesn't that already as part of the context switch to/from the kernel?  It seems very inefficient that stores to multiple atomic variables produces multiple mfences.

 It's worse for ARM, where there's a full memory barrier before/after every atomic store, so two stores in a row produces two memory barriers in a row.

	dmb	sy
	movs	r2, #1
	str	r2, [r3]   # a=1
	dmb	sy
	dmb	sy
	str	r2, [r3]   # a=1
	dmb	sy


---


### compiler : `gcc`
### title : `x86: Faster code is possible for integer absolute value`
### open_at : `2015-09-09T07:55:25Z`
### last_modified_date : `2021-07-26T23:44:46Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=67510
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `5.2.0`
### severity : `minor`
### contents :
Consider integer absolute value in its own function:

int absval(int x) { return x >= 0 ? x : -x; }  // https://goo.gl/PBduHM

I think the ideal sequence would be this, which only has two instructions on the critical path:
        xorl      %eax, %eax    # not on the critical path.  
                                # 1 uop, no execution unit on Intel SnB and later.
        subl      %edi, %eax    # 1 uop, port 0/1/5/6
        cmovl     %edi, %eax    # 2 uops, p0156, latency=2
        # ret  # not included in calculations

Intel Sandybridge microarchitecture: latency = 3, throughput = 1.  4 uops (3 for p0156, 1 eliminated at register rename).

Intel P6 (Core2/Nehalem): Same, but the xor takes an execution port.

Silvermont: 3 uops, latency=3, throughput=2 per 3c.


AMD Bulldozer-family: 3 m-ops, 2c latency.  throughput=2 per 3c.  The xor is recognized as independent, but still uses one of the two execution ports.

AMD K10: 3 m-ops, 2c latency.  throughput = 1 per c.


clang already uses a variant of this:

absval(int): clang 3.7
	movl	%edi, %eax  # on the critical path
	negl	%eax
	cmovll	%edi, %eax
	retq

 On Sandybridge, xor self,self is eliminated at register-rename time (and doesn't take an execution unit), but mov is only eliminated on IvyBridge.  On all CPUs other than Intel IvyBridge and later, my version is better than clang's.  (On IvB+, they're equivalent.)

 On AMD Piledriver / Steamroller, mov r,r has higher throughput than other integer instructions, but it still has latency=1c, unlike IvyBridge's zero-latency move elimination.  So clang's version may be better on recent AMD, if throughput trumps latency.


gcc and icc both use the xor/sub bithack formula:
  sign = x>>31; // (register filled with sign bit of x).
  Abs(x) = (x ^ sign) - sign;

absval(int): gcc various versions, including 5.2.0 (godbolt)
        movl    %edi, %edx   # Why do this at all?
        movl    %edi, %eax   # no latency on IvyBridge and later
        sarl    $31, %edx
        xorl    %edx, %eax
        subl    %edx, %eax
        ret

Why does gcc copy edi to edx before shifting?  It could movl %edi, %eax  / sarl $31, %edi / etc.  I guess that's a separate bug, and wouldn't come up most of the time when inlining.  Let's pretend gcc is smart, and only uses one mov.

Intel IvyBridge and later: 3(+1) uops (1 p0/5, 2 p015(6), 1 eliminated mov).
  Lat=3 (+1 on SnB and earlier, no move elimination)
  Throughput ~= 1 per cycle.  (3 per 4 cycles on Sandybridge and earlier, because the move still needs one of the 3 execution ports (.)

Intel Silvermont: uops=4, Lat=4, Tput = 1 per 2c.

Intel P6 (pre SnB): this avoids any multi-uop instructions which can bottleneck the decoders.  Performance is the same as Sandybridge: lat=4, tput=3 per 4c.

AMD Bulldozer family: mov reg,reg has higher throughput than other instructions, but still 1 cycle latency.  4 m-ops, one of them being a reg-reg move.
  Lat=4, Tput=2 per 3c (Piledriver & Steamroller, where mov r,r can run on an AG port).  Or 1 per 2c (Bulldozer where mov r,r is on ports EX01)

AMD K10: 4 m-ops.  Lat=4, Tput=3 per 4c.



absval(int): icc13
        movl      %edi, %eax  # not needed if we can generate input in eax
        cltd               # replaces mov + sar 31.  CDQ in NASM syntax
        xorl      %edx, %edi
        subl      %edx, %edi
        movl      %edi, %eax  # not needed if output in the input reg is ok
        # ret

This is an interesting optimization which saves a mov if we can generate the input in eax, and clobber it with the output, bringing this down to 3 instructions with lat=3.  None of the instructions are mov, and cltd/xor/sub are all 1 cycle latency instructions that can run on any port, on all Intel/AMD CPUs.


========================================================

If we look at something that uses the absolute value without caring what register it's in (e.g. as a LUT index), that takes out the extra move in gcc's abs() idiom:


int abslookup(int x, int *LUT) { return LUT[x >= 0 ? x : -x]; }
        # gcc 5.2
	movl	%edi, %eax
	sarl	$31, %eax
	xorl	%eax, %edi
	subl	%eax, %edi
	movslq	%edi, %rdi         # abs(INT_MIN) is still negative :/
	movl	(%rsi,%rdi,4), %eax
	ret

This would have more parallelism if we shifted edi and produced the result in eax.  That would shorten the critical path for CPUs without zero-latency mov.  (The mov and sar could happen in parallel.)  Any chance the extra mov in plain abs, and the badly chosen dependency chain here, are related?

  It would also let us save another couple instruction bytes by using cltq (aka NASM cdqe) to sign-extend eax to rax, instead of movslq.  (Clang does this after generating abs(x) in eax with cmov.)


---


### compiler : `gcc`
### title : `Failure to perform constant folding through type conversion`
### open_at : `2015-09-17T07:46:03Z`
### last_modified_date : `2021-08-18T23:57:19Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=67607
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `6.0`
### severity : `enhancement`
### contents :
This code is taken from PR67606:

$ cat pr67606.c
int f(int a[], int length)
{
  int count=0;
  for (int i = 0 ; i < length ; i++)
    if (a[i] > 5)
      count++;

  return count;
}

$ g++ -S -O3 -fno-tree-vectorize pr67606.c -fverbose-asm -fdump-tree-optimized

We get:

  <bb 3>:
  ivtmp.6_1 = (unsigned long) a_7(D);
  _19 = (unsigned int) length_4(D);
  _18 = _19 + 4294967295;
  _21 = (sizetype) _18;
  _22 = _21 + 1;
  _23 = _22 * 4;
  _24 = a_7(D) + _23;
  _25 = (unsigned long) _24;

And this leads to generating some redundant code:

  leal    -1(%rsi), %eax  #, tmp114
  leaq    4(%rdi,%rax,4), %rcx    #, tmp111


---


### compiler : `gcc`
### title : `[tree-optimization] (a && b) && c shows better codegen than a && (b && c)`
### open_at : `2015-09-18T14:32:23Z`
### last_modified_date : `2023-09-04T08:09:39Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=67628
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `6.0`
### severity : `enhancement`
### contents :
Consider the two functions:
int
foo1 (int a, int b, int c, int d)
{
  return a > b && b <= c && c > d;
}

int
foo2 (int a, int b, int c, int d)
{
  return a > b && (b <= c && c > d);
}

On aarch64 foo1 generates:
foo1:
        cmp     w1, w2
        ccmp    w2, w3, 4, le
        ccmp    w0, w1, 4, gt
        cset    w0, gt
        ret

but for foo2 generates:
foo2:
        cmp     w0, w1
        ble     .L4
        cmp     w1, w2
        cset    w1, le
        cmp     w2, w3
        cset    w0, gt
        and     w0, w1, w0
        ret


Something similar is observed on x86_64 where foo2 contains a conditional branch instruction where foo1 is a single basic block

In foo2 we end up generating multiple basic blocks whereas for foo1 we manage to merge them all into 1 basic block which ends up going through the conditional-compare pass nicely.

Looking at the final .optimized tree dump the foo1 tree is:
  _BoolD.2673 _1;
  _BoolD.2673 _4;
  _BoolD.2673 _6;
  _BoolD.2673 _10;
  _BoolD.2673 _11;
  intD.7 _12;

;;   basic block 2, loop depth 0, count 0, freq 10000, maybe hot
;;    prev block 0, next block 1, flags: (NEW, REACHABLE)
;;    pred:       ENTRY [100.0%]  (FALLTHRU,EXECUTABLE)
  # RANGE [0, 1]
  _4 = a_2(D) > b_3(D);
  # RANGE [0, 1]
  _6 = b_3(D) <= c_5(D);
  # RANGE [0, 1]
  _10 = c_5(D) > d_8(D);
  # RANGE [0, 1]
  _1 = _6 & _10;
  # RANGE [0, 1]
  _11 = _1 & _4;
  # RANGE [0, 1] NONZERO 1
  _12 = (intD.7) _11;
  # VUSE <.MEM_9(D)>
  return _12;
;;    succ:       EXIT [100.0%] 




whereas for foo2 it's more complex:
  intD.7 iftmp.0_1;
  _BoolD.2673 _5;
  _BoolD.2673 _7;
  _BoolD.2673 _8;
  intD.7 _10;
  _BoolD.2673 _11;

;;   basic block 2, loop depth 0, count 0, freq 10000, maybe hot
;;    prev block 0, next block 3, flags: (NEW, REACHABLE)
;;    pred:       ENTRY [100.0%]  (FALLTHRU,EXECUTABLE)
  if (a_2(D) > b_3(D))
    goto <bb 3>;
  else
    goto <bb 4>;
;;    succ:       3 [50.0%]  (TRUE_VALUE,EXECUTABLE)
;;                4 [50.0%]  (FALSE_VALUE,EXECUTABLE)

;;   basic block 3, loop depth 0, count 0, freq 5000, maybe hot
;;    prev block 2, next block 4, flags: (NEW, REACHABLE)
;;    pred:       2 [50.0%]  (TRUE_VALUE,EXECUTABLE)
  # RANGE [0, 1]
  _5 = b_3(D) <= c_4(D);
  # RANGE [0, 1]
  _7 = c_4(D) > d_6(D);
  # RANGE [0, 1]
  _8 = _5 & _7;
;;    succ:       4 [100.0%]  (FALLTHRU,EXECUTABLE)

;;   basic block 4, loop depth 0, count 0, freq 10000, maybe hot
;;    prev block 3, next block 1, flags: (NEW, REACHABLE)
;;    pred:       3 [100.0%]  (FALLTHRU,EXECUTABLE)
;;                2 [50.0%]  (FALSE_VALUE,EXECUTABLE)
  # _11 = PHI <_8(3), 0(2)>
  # RANGE [0, 1] NONZERO 1
  iftmp.0_1 = (intD.7) _11;
  # VUSE <.MEM_9(D)>
  return iftmp.0_1;
;;    succ:       EXIT [100.0%] 



If we were to pick some kind of canonicalization for these equivalent expressions it would make life easier for later passes to generate consistent code.


---


### compiler : `gcc`
### title : `[SH] ifcvt missed optimization`
### open_at : `2015-09-19T04:09:40Z`
### last_modified_date : `2023-08-08T07:02:14Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=67635
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `unknown`
### severity : `normal`
### contents :
At least on SH, the following:

bool test (int a, int b, int* r)
{
  return __builtin_mul_overflow (a, b, r);
}

compiled with -m4 -ml -O2 results in:

        dmuls.l r5,r4
        mov     #0,r0
        sts     macl,r1
        sts     mach,r2
        cmp/gt  r1,r0
        subc    r3,r3
        cmp/eq  r2,r3    <<
        bf      .L6      <<
.L2:
        rts
        mov.l   r1,@r6
        .align 1
.L6:
        bra     .L2
        mov     #1,r0


The expected code would be:
        dmuls.l r5,r4
        mov     #0,r0
        sts     macl,r1
        sts     mach,r2
        cmp/gt  r1,r0
        subc    r3,r3
        cmp/eq  r2,r3    // T = r2 == r3
        mov     #-1,r0
        negc    r0,r0    // T = r2 != r3
        rts
        mov.l   r1,@r6


Alternatively, in cases zero-displacement branches are fast (e.g. SH4):
        dmuls.l r5,r4
        mov     #0,r0
        sts     macl,r1
        sts     mach,r2
        cmp/gt  r1,r0
        subc    r3,r3
        cmp/eq  r2,r3
        bt      0f
        mov     #1,r0
0:
        rts
        mov.l   r1,@r6


I think I have seen similar cases before, where something tries to preserve the zero constant in a reg.  Instead of overwriting it with a cstore value {0,1}, conditional branches are created for the non-zero paths.

If conditional move patterns are enabled on SH with -mpretend-cmove the conditional branches go away:

        dmuls.l r5,r4
        mov     #-1,r0
        sts     macl,r2
        sts     mach,r3
        sts     macl,r1
        shll    r2
        subc    r2,r2
        cmp/eq  r3,r2
        mov.l   r1,@r6
        rts
        negc    r0,r0

But enabling -mpretend-cmove on SH has some other side effects and currently is not safe (PR 58517).


---


### compiler : `gcc`
### title : `Missed vectorization: shifts of an induction variable`
### open_at : `2015-09-22T17:21:52Z`
### last_modified_date : `2021-08-25T05:32:15Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=67683
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `6.0`
### severity : `enhancement`
### contents :
This testcase:

void test (unsigned char *data, int max)
{
  unsigned short val = 0xcdef;
  for(int i = 0; i < max; i++) { 
          data[i] = (unsigned char)(val & 0xff);
          val >>= 1; 
  }
}

does not vectorize on AArch64 or x86_64 at -O3. (I haven't yet looked at whether it's a mid-end deficiency or both back-ends are missing patterns.)


---


### compiler : `gcc`
### title : `builtin cmpstrn not used if not one of the inputs is not a string literal`
### open_at : `2015-09-24T15:05:21Z`
### last_modified_date : `2021-10-01T02:53:57Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=67713
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `unknown`
### severity : `normal`
### contents :
It seems that the following

int test_06 (const char* s1)
{
  return __builtin_strncmp (s1, "abcdabcd", 8);
}

will emit the builtin strncmp code, while

int test_07 (const char* s1, const char* s2)
{
  return __builtin_strncmp (s1, s2, 8);
}

will always invoke the strncmp function.

This happens on trunk for SH and on GCC 4.9 (Ubuntu 4.9.2-10ubuntu13) for x86_64.  Not sure whether this is a tree or RTL issue, though.


---


### compiler : `gcc`
### title : `Combine of OR'ed bitfields should use bit-test`
### open_at : `2015-09-27T11:19:54Z`
### last_modified_date : `2023-07-19T04:08:47Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=67731
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `unknown`
### severity : `enhancement`
### contents :
This is what happens on SH, but it's probably not entirely SH specific.  All examples below have been compiled with -x c -std=gnu11 -O2 -m4 -ml.

typedef struct
{
  _Bool a : 1;
  _Bool b : 1;
  _Bool c : 1;
  _Bool d : 1;
  unsigned int e : 4;
} S;


_Bool test_00 (S* s)
{
  return s->b | s->c;
}

compiles to:
	mov.l	@r4,r2
	mov	r2,r0
	tst	#2,r0     // bit test 'b'
	mov	#-1,r0
	negc	r0,r1
	mov	r2,r0
	tst	#4,r0     // bit test 'c'
	mov	#-1,r0
	negc	r0,r0
	rts	
	or	r1,r0

while the equivalent


_Bool test_01 (unsigned char* s)
{
  return *s & ((1 << 1) | (1 << 2));
}

compiles to:
	mov.b	@r4,r0
	mov	#-1,r1
	tst	#6,r0    // bit test 'b' | 'c'
	rts	
	negc	r1,r0

For the bitfield case, combine is looking for a pattern:

Failed to match this instruction:
(set (reg:SI 180)
    (ior:SI (zero_extract:SI (reg:SI 170 [ *s_2(D) ])
            (const_int 1 [0x1])
            (const_int 2 [0x2]))
        (zero_extract:SI (reg:SI 170 [ *s_2(D) ])
            (const_int 1 [0x1])
            (const_int 1 [0x1]))))

Adding it to sh.md as:

(define_insn_and_split "*"
  [(set (match_operand:SI 0 "arith_reg_dest")
	(ior:SI (zero_extract:SI (match_operand:SI 1 "arith_reg_operand")
				 (const_int 1)
				 (match_operand 2 "const_int_operand"))
		(zero_extract:SI (match_dup 1)
				 (const_int 1)
				 (match_operand 3 "const_int_operand"))))
   (clobber (reg:SI T_REG))]
  "TARGET_SH1 && can_create_pseudo_p ()"
  "#"
  "&& 1"
  [(parallel [(set (match_dup 0)
		   (ne:SI (and:SI (match_dup 1) (match_dup 2)) (const_int 0)))
	      (clobber (reg:SI T_REG))])]
{
  operands[2] = GEN_INT ((1LL << INTVAL (operands[2]))
			 | (1LL << INTVAL (operands[3])));
})

results in the expected code:

        mov.l   @r4,r0
        tst     #6,r0
        mov     #-1,r0
        rts
        negc    r0,r0


Then...

_Bool test_03 (S* s)
{
  return s->b | s->c | s->d;
}

results in combine looking for something like
Failed to match this instruction:
(set (reg:SI 195)
    (and:SI (ior:SI (ior:SI (lshiftrt:SI (reg:SI 173 [ *s_2(D) ])
                    (const_int 2 [0x2]))
                (lshiftrt:SI (reg:SI 173 [ *s_2(D) ])
                    (const_int 1 [0x1])))
            (lshiftrt:SI (reg:SI 173 [ *s_2(D) ])
                (const_int 3 [0x3])))
        (const_int 1 [0x1])))

and for 4 bits it's

(set (reg:SI 204)
    (and:SI (ior:SI (ior:SI (ior:SI (lshiftrt:SI (reg:SI 173 [ *s_2(D) ])
                        (const_int 2 [0x2]))
                    (lshiftrt:SI (reg:SI 173 [ *s_2(D) ])
                        (const_int 1 [0x1])))
                (lshiftrt:SI (reg:SI 173 [ *s_2(D) ])
                    (const_int 3 [0x3])))
            (lshiftrt:SI (reg:SI 173 [ *s_2(D) ])
                (const_int 4 [0x4])))
        (const_int 1 [0x1])))

and so on.

Although it's of course possible to add these with a recursive predicate the the backend, maybe it could be a good idea to either do this at the tree-level or in combine/simplify rtx.  I think this is a problem on every target, not just SH.


---


### compiler : `gcc`
### title : `builtin functions should be able to know when their first argument is returned for tail calls`
### open_at : `2015-10-01T14:19:52Z`
### last_modified_date : `2021-12-27T04:28:15Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=67797
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `5.2.0`
### severity : `enhancement`
### contents :
Compiled with -Os and with -O2 (result is the same):
#include <string.h>

void *my_func(void *s, size_t n)
{
    memset(s, 0, n);
    return s;
}

The generated code is following:

00000000 <my_func>:
   0:	e92d4010 	push	{r4, lr}
   4:	e1a02001 	mov	r2, r1
   8:	e1a04000 	mov	r4, r0
   c:	e3a01000 	mov	r1, #0
  10:	ebfffffe 	bl	0 <memset>
  14:	e1a00004 	mov	r0, r4
  18:	e8bd8010 	pop	{r4, pc}

First, copying r0 into r4 is redundant as memset doesn't clobber r0. So the code could be reduced to:

push	{r4, lr}
mov	r2, r1
mov	r1, #0
bl	0 <memset>
pop	{r4, pc}

That in turn can be simplified more to:

mov	r2, r1
mov	r1, #0
b	0 <memset>


---


### compiler : `gcc`
### title : `Empty pointer-chasing loops aren't optimized out`
### open_at : `2015-10-01T20:47:13Z`
### last_modified_date : `2021-08-28T23:52:24Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=67809
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `5.2.0`
### severity : `enhancement`
### contents :
The following code:

```
struct Foo {
  Foo *next; 
  
  void release() {
    Foo *tmp = 0;
    for (Foo *it = next; it; it = tmp) {
      tmp = it->next;
    }
  }
};

void test(Foo &f) { f.release(); }
```

Results in pointer-chasing code when compiled at -O3:

```
test(Foo&):
	mov	rax, QWORD PTR [rdi]
	test	rax, rax
	je	.L1
.L3:
	mov	rax, QWORD PTR [rax]
	test	rax, rax
	jne	.L3
.L1:
	rep ret
```

clang and icc both optimize this to a single ret. e.g. https://goo.gl/saN4XC vs https://goo.gl/LeUGn0

Would be nice for this loop to go away completely. For context, this was in code I added to use ASAN_POISON_MEMORY_REGION() around a pooled allocator upon free of a list (each node was poisoned individually). Without -fsanitize=address I was expecting the loop to entirely vanish, but the pointer-chase was still done.


---


### compiler : `gcc`
### title : `callee-saved register saves should be shrink-wrapped`
### open_at : `2015-10-05T18:20:39Z`
### last_modified_date : `2021-05-04T12:31:58Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=67856
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `5.1.1`
### severity : `enhancement`
### contents :
This code:

typedef _Bool bool;

extern int a(void);

/* used as a proxy for real code. */
volatile int x;

bool func(void *regs)
{
	int t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11;

	while (1) {
		int cached_flags = a();

		if (!__builtin_expect(cached_flags & 31, 0))
			break;

		t1 = x;
		t2 = x;
		t3 = x;
		t4 = x;
		t5 = x;
		t6 = x;
		t7 = x;
		t8 = x;
		t9 = x;
		t10 = x;
		t11 = x;

		x = t1;
		x = t2;
		x = t3;
		x = t4;
		x = t5;
		x = t6;
		x = t7;
		x = t8;
		x = t9;
		x = t10;
		x = t11;
	}

	return 0;
}

generates (gcc -O2 -S):

	.file	"ra.c"
	.section	.text.unlikely,"ax",@progbits
.LCOLDB0:
	.text
.LHOTB0:
	.p2align 4,,15
	.globl	func
	.type	func, @function
func:
.LFB0:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	pushq	%rbx
	.cfi_def_cfa_offset 24
	.cfi_offset 3, -24
	subq	$8, %rsp
	.cfi_def_cfa_offset 32
.L3:
	call	a
	testb	$31, %al
	jne	.L6
	addq	$8, %rsp
	.cfi_remember_state
	.cfi_def_cfa_offset 24
	xorl	%eax, %eax
	popq	%rbx
	.cfi_def_cfa_offset 16
	popq	%rbp
	.cfi_def_cfa_offset 8
	ret
	.p2align 4,,10
	.p2align 3
.L6:
	.cfi_restore_state
	movl	x(%rip), %ebp
	movl	x(%rip), %ebx
	movl	x(%rip), %r11d
	movl	x(%rip), %r10d
	movl	x(%rip), %r9d
	movl	x(%rip), %r8d
	movl	x(%rip), %edi
	movl	x(%rip), %esi
	movl	x(%rip), %ecx
	movl	x(%rip), %edx
	movl	x(%rip), %eax
	movl	%ebp, x(%rip)
	movl	%ebx, x(%rip)
	movl	%r11d, x(%rip)
	movl	%r10d, x(%rip)
	movl	%r9d, x(%rip)
	movl	%r8d, x(%rip)
	movl	%edi, x(%rip)
	movl	%esi, x(%rip)
	movl	%ecx, x(%rip)
	movl	%edx, x(%rip)
	movl	%eax, x(%rip)
	jmp	.L3
	.cfi_endproc
.LFE0:
	.size	func, .-func
	.section	.text.unlikely
.LCOLDE0:
	.text
.LHOTE0:
	.comm	x,4,4
	.ident	"GCC: (GNU) 5.1.1 20150618 (Red Hat 5.1.1-4)"
	.section	.note.GNU-stack,"",@progbits

The unconditional pushes of rbp and rbx are missed optimizations: they should be sunk into the cold code that needs them pushed.


---


### compiler : `gcc`
### title : `Incomplete optimization for virtual function call into freshly constructed object`
### open_at : `2015-10-07T20:05:55Z`
### last_modified_date : `2023-05-05T06:51:57Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=67886
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.2`
### severity : `enhancement`
### contents :
This is a bit of a corner/academic case, but came up in a Stack Overflow discussion:

    struct Base {
        virtual void func() = 0;
    };

    struct Derived : Base {
        virtual void func() { };
    };

    void test()
    {
        Base* base = new Derived;

        for (int i = 0; i < 1000; ++i)
        {
            base->func();
        }
    }

The generated assembler code on x86_64 with -O3 is

Disassembly of section .text:

0000000000000000 <test()>:
   0:   55                      push   %rbp
   1:   53                      push   %rbx
   2:   bf 08 00 00 00          mov    $0x8,%edi
   7:   bb e8 03 00 00          mov    $0x3e8,%ebx
   c:   48 83 ec 08             sub    $0x8,%rsp
  10:   e8 00 00 00 00          callq  15 <test()+0x15>
                        11: R_X86_64_PC32       operator new(unsigned long)-0x4
  15:   ba 00 00 00 00          mov    $0x0,%edx
                        16: R_X86_64_32 vtable for Derived+0x10
  1a:   48 89 c5                mov    %rax,%rbp
  1d:   48 c7 00 00 00 00 00    movq   $0x0,(%rax)
                        20: R_X86_64_32S        vtable for Derived+0x10
  24:   eb 13                   jmp    39 <test()+0x39>
  26:   66 2e 0f 1f 84 00 00    nopw   %cs:0x0(%rax,%rax,1)
  2d:   00 00 00 
  30:   83 eb 01                sub    $0x1,%ebx
  33:   74 1a                   je     4f <test()+0x4f>
  35:   48 8b 55 00             mov    0x0(%rbp),%rdx
  39:   48 8b 12                mov    (%rdx),%rdx
  3c:   48 81 fa 00 00 00 00    cmp    $0x0,%rdx
                        3f: R_X86_64_32S        Derived::func()
  43:   74 eb                   je     30 <test()+0x30>
  45:   48 89 ef                mov    %rbp,%rdi
  48:   ff d2                   callq  *%rdx
  4a:   83 eb 01                sub    $0x1,%ebx
  4d:   75 e6                   jne    35 <test()+0x35>
  4f:   48 83 c4 08             add    $0x8,%rsp
  53:   5b                      pop    %rbx
  54:   5d                      pop    %rbp
  55:   c3                      retq   

Disassembly of section .text._ZN7Derived4funcEv:

0000000000000000 <Derived::func()>:
   0:   f3 c3                   repz retq 

This looks like an optimization half-done. The optimizer correctly inlines the function call to Derived::func() into the loop, and also correctly verifies that the function pointer found in the vtable is indeed the same function that was inlined -- otherwise, the inlined function is skipped and the regular function called.

I presume that the pointer is rechecked on every loop iteration because it is possible that the function call can destroy the object and create a new one in its place that still derives from Base, so that is correct.

If you set -fPIC, the actual values for the vtable pointer and the pointer to Derived::func() are fetched outside of the loop, and rechecked on each loop iteration, again, correctly.

However: without -fPIC, there is no way to get a different definition of Derived::func() without invoking UB, so the function pointer check is tautological and can be optimized out, unraveling the entire fuzzy ball, as the inlined function does not destroy the object, and inlining it into the loop should give an empty loop that can be removed.

Also, wouldn't setting -fvisibility=hidden also take Derived's symbols out of the dynamic symbol table, in which case I wouldn't be able to override them at runtime with a preload library?

The optimal solution from an assembler programmer's perspective would be to take the knowledge that the inlined function does not touch the object's vtable, and create a path that handles the remaining loop iterations after the object was shown to be a Derived object once -- this would probably be optimized to a conditional jump to the ret instruction in the RTL pass -- but I don't have enough knowledge to tell whether that would be easily doable in this case.


---


### compiler : `gcc`
### title : `Optimization opportunity with conditional swap to two MIN/MAX in phiopt`
### open_at : `2015-10-14T11:06:21Z`
### last_modified_date : `2023-07-21T08:26:11Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=67962
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `5.2.0`
### severity : `enhancement`
### contents :
If have some algorithms that use an extensive number of conditional swaps like this (a few hundreds I guess):

    if (y < x)
    {
        std::swap(x, y);
    }

I thought that such a construct could be optimized by the compiler, but it appears that the following function is more performant with integers most of the time:

    void swap_if(int& x, int& y)
    {
        int dx = x;
        int dy = y;
        int tmp = x = std::min(dx, dy);
        y ^= dx ^ tmp;
    }

Would it be possible for g++ to recognize this kind of construct and optimize it, at least for integer types? Reordering two values seems like something common enough so that optimizing it could also benefit existing code.

As a side note, I hope that Bugzilla is he right place for this kind of request. Sorry if it isn't.


---


### compiler : `gcc`
### title : `redundant test for 0 when also checking inequality`
### open_at : `2015-10-16T21:31:24Z`
### last_modified_date : `2021-06-03T04:14:44Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=67998
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `5.1.0`
### severity : `enhancement`
### contents :
int f(unsigned a, unsigned b)
{
	if (!a || b >= a)
		return 5;
	return 2;
}

compiles to

f(unsigned int, unsigned int):
	testl	%edi, %edi
	je	.L3
	cmpl	%esi, %edi
	jbe	.L3
	movl	$2, %eax
	ret
.L3:
	movl	$5, %eax
	ret

The first test is redundant, since if a is zero, the inequality is guaranteed to hold.


---


### compiler : `gcc`
### title : `Suboptimal ternary operator codegen`
### open_at : `2015-10-17T06:47:39Z`
### last_modified_date : `2021-06-03T04:11:31Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=68000
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `5.1.0`
### severity : `enhancement`
### contents :
Created attachment 36534
Preprocessed C code for "Suboptimal ternary operator codegen"

I think this problem is likely related to bug 23286, bug 56096, bug 64524, and possibly bug 67879.

struct pair8 { uint8_t x,y; };
uint8_t foo_manual_hoist(struct pair8 *p) {
	const uint8_t a = p->x + 1;
	return a == p->y ? 0 : a;
}
uint8_t foo(struct pair8 *p) {
	return p->x + 1 == p->y ? 0 : p->x + 1;
}
uint8_t foo_if(struct pair8 *p) {
	uint8_t a = p->x + 1;
	if (a == p->y)
		a = 0;
	return a;
}
int main() {}

Under gcc-5.1, gcc -m64 -march=native -O3 -g -S -masm=intel -o test.asm test.c produces

foo_manual_hoist:
    movzx eax, BYTE PTR [rdi+1]
    mov   edx, 0
    add   eax, 1
    cmp   al, BYTE PTR [rdi+2]
    cmove eax, edx
    ret
foo:
    movzx edx, BYTE PTR [rdi+1]
    movzx ecx, BYTE PTR [rdi+2]
    mov   eax, edx   // weird!
    add   edx, 1
    add   eax, 1
    cmp   edx, ecx
    mov   edx, 0
    cmove eax, edx
    ret
foo_if:
    movzx eax, BYTE PTR [rdi+1]
    mov   edx, 0
    add   eax, 1
    cmp   al, BYTE PTR [rdi+2]
    cmove eax, edx
    ret

As expect, the ternary version with the manual hoist of the common subexpression produces identical codegen as the if version with the same hoist. What is unexpected, is the duplication of the common subexpression for the "bare" ternary version (line 3 of the disassembly of foo). It is clear that the compiler sees the expressions to be the same, but treats them separately anyway. As an aside, clang-3.6 produces identical code for all three versions.


---


### compiler : `gcc`
### title : `Pessimization of simple non-tail-recursive functions`
### open_at : `2015-10-18T09:25:17Z`
### last_modified_date : `2019-05-21T23:19:45Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=68008
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `5.1.1`
### severity : `enhancement`
### contents :
Created attachment 36537
preprocessed source code

As discussed on Stack Overflow in http://stackoverflow.com/questions/32974625 (Misleading title: "Is gcc's asm volatile equivalent to the gfortran default setting for recursions?"), gcc pessimizes the example fibonacci function, which can be avoided by "-fno-optimize-sibling-calls" (which is the reason I assigned the bug to tree-optimization)

The non-optimal code is generated at least by
  gcc 4.5.3 (Debian 4.5.3-12)
  gcc version 4.9.2 (Debian 4.9.2-10)
  gcc version 5.1.1 20150507 (Debian 5.1.1-5)

I will focus on gcc 5.1.1 in the remaining report.

Configured with: ../src/configure -v --with-pkgversion='Debian 5.1.1-5' --with-bugurl=file:///usr/share/doc/gcc-5/README.Bugs --enable-languages=c,ada,c++,java,go,d,fortran,objc,obj-c++ --prefix=/usr --program-suffix=-5 --enable-shared --enable-linker-build-id --libexecdir=/usr/lib --without-included-gettext --enable-threads=posix --libdir=/usr/lib --enable-nls --with-sysroot=/ --enable-clocale=gnu --enable-libstdcxx-debug --enable-libstdcxx-time=yes --with-default-libstdcxx-abi=c++98 --disable-libstdcxx-dual-abi --enable-gnu-unique-object --disable-vtable-verify --enable-libmpx --enable-plugin --with-system-zlib --disable-browser-plugin --enable-java-awt=gtk --enable-gtk-cairo --with-java-home=/usr/lib/jvm/java-1.5.0-gcj-5-amd64/jre --enable-java-home --with-jvm-root-dir=/usr/lib/jvm/java-1.5.0-gcj-5-amd64 --with-jvm-jar-dir=/usr/lib/jvm-exports/java-1.5.0-gcj-5-amd64 --with-arch-directory=amd64 --with-ecj-jar=/usr/share/java/eclipse-ecj.jar --enable-objc-gc --enable-multiarch --with-arch-32=i586 --with-abi=m64 --with-multilib-list=m32,m64,mx32 --enable-multilib --with-tune=generic --enable-checking=release --build=x86_64-linux-gnu --host=x86_64-linux-gnu --target=x86_64-linux-gnu

gcc is invoked as: g++-5 -O3 -march=core2 -std=c++0x stack-overflow-32974625.cc; ./a.out
compared to g++-5 -O3 -march=core2 -std=c++0x -fno-optimize-sibling-calls stack-overflow-32974625.cc; ./a.out


There are no error or warning messages printed by the compiler or linker (even if warning would be enabled by -Wall -Wextra)

The file stack-overflow-32974625.ii is attached.

Timing with g++ 5.1.1 on a Core2Duo T7200 under 64-bit linux (cpu frequency scaling set to "performance"):
With -fno-optimize-sibling-calls: 34.5us/iteration
Without -fno-optimize-sibling-calls: 68us/iteration


---


### compiler : `gcc`
### title : `uncprop should work on more than PHI nodes`
### open_at : `2015-10-20T05:24:54Z`
### last_modified_date : `2021-08-10T18:22:23Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=68027
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `5.2.0`
### severity : `enhancement`
### contents :
C source code:

int a1(int);
int a2(int);
int a3(int);

int test1(int a)
{
  if (a > 100) return a1(a);
  else if (a < 100) return a2(a);
  return a3(a);
}

-----------------------------------

Assembly output:


test1:
.LFB0:
        .cfi_startproc
        cmpl    $100, %edi
        jg      .L5
        jne     .L6
        movl    $100, %edi   # no need to do this, eax is equal $100 at this point
        jmp     a3
        .p2align 4,,10
        .p2align 3
.L6:
        jmp     a2
        .p2align 4,,10
        .p2align 3
.L5:
        jmp     a1
        .cfi_endproc

-----------------------------------

Tested on http://gcc.godbolt.org/ : gcc versions 4.4.7 - 5.2.0 have this problem.


---


### compiler : `gcc`
### title : `Redundant address calculations in vectorized loop`
### open_at : `2015-10-20T13:37:20Z`
### last_modified_date : `2021-10-01T02:57:20Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=68030
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `6.0`
### severity : `normal`
### contents :
Created attachment 36548
Reproducer

Attached testcase.
Compiled w/: -S -Ofast -march=haswell 1.c

Code in main loop is:
.L7:
        movq    -176(%rbp), %rdx
        vmovaps -272(%rbp), %ymm1
        addl    $1, %r9d
        vmulps  (%rdx,%rax), %ymm11, %ymm0
        movq    -184(%rbp), %rdx ; <- Fill
        vfmadd231ps     (%rdx,%rax), %ymm12, %ymm0
        movq    -192(%rbp), %rdx ; <- Fill
        vmovaps %ymm0, %ymm15
        vmulps  (%rdx,%rax), %ymm13, %ymm0
        movq    -112(%rbp), %rdx; <- Fill
        vfmadd231ps     (%rdx,%rax), %ymm14, %ymm0
        movq    -160(%rbp), %rdx; <- Fill
        vaddps  %ymm0, %ymm15, %ymm0
        vmulps  (%rdx,%rax), %ymm9, %ymm15
        movq    -168(%rbp), %rdx
        ...

Those loads are related to the same array  (global_Input in the source)
with fixed offsets from the base.
Unfortunately, this is not recognized by Gimple (optimized):
  # ratio_mult_vf.11_1609 = PHI <504(8), 512(5)>
  # bnd.10_1618 = PHI <63(8), 64(5)>
  # niters.9_1610 = PHI <niters.9_339(8), 512(5)>
  # prolog_loop_adjusted_niters.8_1611 = PHI <prolog_loop_adjusted_niters.8_340(8), 0(5)>
  # ivtmp_1615 = PHI <_401(8), 512(5)>
  # ix_1592 = PHI <_456(8), 2(5)>
  _999 = ivtmp.345_510 + prolog_loop_adjusted_niters.8_1611;
  _998 = _999 * 4;
  _995 = _998 + 18446744073709547488;
  vectp.15_1 = pretmp_889 + _995; <-- addr is (base + _999*4 + OFFSET1)
  _986 = *local_Filter_12;
  vect_cst__984 = {_986, _986, _986, _986, _986, _986, _986, _986};
  _975 = _998 + 18446744073709547492;
  vectp.22_982 = pretmp_889 + _975; <-- addr is (base + _999*4 + OFFSET11)
  _965 = MEM[(float *)local_Filter_12 + 4B];
  vect_cst__964 = {_965, _965, _965, _965, _965, _965, _965, _965};
  _956 = _998 + 18446744073709547496;
  vectp.30_961 = pretmp_889 + _956; <-- addr is (base + _999*4 + OFFSET2)
  _948 = MEM[(float *)local_Filter_12 + 8B];
  vect_cst__947 = {_948, _948, _948, _948, _948, _948, _948, _948};
  _940 = _998 + 18446744073709547500;
  vectp.37_945 = pretmp_889 + _940; <-- addr is (base + _999*4 + OFFSET3)
  _932 = MEM[(float *)local_Filter_12 + 12B];
  vect_cst__931 = {_932, _932, _932, _932, _932, _932, _932, _932};
  _924 = _998 + 18446744073709547504;
  vectp.44_929 = pretmp_889 + _924; <-- addr is (base + _999*4 + OFFSET4)
  _916 = MEM[(float *)local_Filter_12 + 16B];`
  vect_cst__915 = {_916, _916, _916, _916, _916, _916, _916, _916};
  _903 = _998 + 18446744073709549552;
  vectp.53_911 = pretmp_889 + _903; <-- addr is (base + _999*4 + OFFSET5)
  _895 = MEM[(float *)local_Filter_12 + 20B];
  vect_cst__894 = {_895, _895, _895, _895, _895, _895, _895, _895};
  _155 = _998 + 18446744073709549556;
  vectp.60_892 = pretmp_889 + _155;<-- addr is (base + _999*4 + OFFSET6)
  _500 = MEM[(float *)local_Filter_12 + 24B];
  vect_cst__37 = {_500, _500, _500, _500, _500, _500, _500, _500};
  _1070 = _998 + 18446744073709549560;
  vectp.68_907 = pretmp_889 + _1070; <-- addr is (base + _999*4 + OFFSET7)
  _1078 = MEM[(float *)local_Filter_12 + 28B];
  vect_cst__1079 = {_1078, _1078, _1078, _1078, _1078, _1078, _1078, _1078};
  _1087 = _998 + 18446744073709549564;
  vectp.76_1082 = pretmp_889 + _1087; <-- addr is (base + _999*4 + OFFSET8)
  _1095 = MEM[(float *)local_Filter_12 + 32B];
  vect_cst__1096 = {_1095, _1095, _1095, _1095, _1095, _1095, _1095, _1095};
  _1103 = _998 + 18446744073709549568; <-- addr is (base + _999*4 + OFFSET9)
  vectp.83_1098 = pretmp_889 + _1103;
  _1111 = MEM[(float *)local_Filter_12 + 36B];
...
  <bb 10>:
  # ivtmp.250_79 = PHI <ivtmp.250_56(10), 0(9)>
  # ivtmp.253_329 = PHI <ivtmp.253_330(10), 0(9)>
  vect__161.16_992 = MEM[base: vectp.15_1, index: ivtmp.253_329, offset: 0B]; // load @ (base + _999*4 + OFFSET1 + IV + 0)
  vect__177.23_972 = MEM[base: vectp.22_982, index: ivtmp.253_329, offset: 0B]; // load @ (base + _999*4 + OFFSET11 + IV + 0)
  vect__182.27_963 = vect_cst__964 * vect__177.23_972;
  _1256 = vect_cst__984 * vect__161.16_992 + vect__182.27_963;
  vect__193.31_953 = MEM[base: vectp.30_961, index: ivtmp.253_329, offset: 0B]; // load @ (base + _999*4 + OFFSET2 + IV + 0)
  vect__209.38_937 = MEM[base: vectp.37_945, index: ivtmp.253_329, offset: 0B]; // load @ (base + _999*4 + OFFSET3 + IV + 0)
  vect__214.42_930 = vect_cst__931 * vect__209.38_937;
  _1235 = vect_cst__947 * vect__193.31_953 + vect__214.42_930;
  _1307 = _1235 + _1256;
  vect__225.45_921 = MEM[base: vectp.44_929, index: ivtmp.253_329, offset: 0B]; // load @ (base + _999*4 + OFFSET4 + IV + 0)
  vect__247.54_900 = MEM[base: vectp.53_911, index: ivtmp.253_329, offset: 0B]; // load @ (base + _999*4 + OFFSET5 + IV + 0)
  vect__252.58_893 = vect_cst__894 * vect__247.54_900;
  _1291 = vect_cst__915 * vect__225.45_921 + vect__252.58_893;
  _341 = _1291 + _1307;
  vect__263.61_242 = MEM[base: vectp.60_892, index: ivtmp.253_329, offset: 0B]; // load @ (base + _999*4 + OFFSET6 + IV + 0)
  vect__279.69_1073 = MEM[base: vectp.68_907, index: ivtmp.253_329, offset: 0B]; // load @ (base + _999*4 + OFFSET7 + IV + 0)
...

You can see all loads are differ in a constant.
All vector loads mentions may use common base for addres + constant offset.

Which pass is responsible for such optimization?

I'd like to see something like this:
  _999 = ivtmp.345_510 + prolog_loop_adjusted_niters.8_1611;
  _998 = _999 * 4;
  vectp.15_1 = pretmp_889 + _998; <-- addr is (base + _999*4)
...
  <bb 10>:
  # ivtmp.250_79 = PHI <ivtmp.250_56(10), 0(9)>
  # ivtmp.253_329 = PHI <ivtmp.253_330(10), 0(9)>
  vect__161.16_992 = MEM[base: vectp.15_1, index: ivtmp.253_329, offset: OFFSET1]; // load @ (base + _999*4 + IV + OFFSET1)
  vect__177.23_972 = MEM[base: vectp.15_1, index: ivtmp.253_329, offset: OFFSET11]; // load @ (base + _999*4 + IV + OFFSET11)
  vect__182.27_963 = vect_cst__964 * vect__177.23_972;
  _1256 = vect_cst__984 * vect__161.16_992 + vect__182.27_963;
  vect__193.31_953 = MEM[base: vectp.15_1, index: ivtmp.253_329, offset: OFFSET2]; // load @ (base + _999*4 + IV + OFFSET2)
  vect__209.38_937 = MEM[base: vectp.15_1, index: ivtmp.253_329, offset: OFFSET3]; // load @ (base + _999*4 + IV + OFFSET3)
  vect__214.42_930 = vect_cst__931 * vect__209.38_937;
  _1235 = vect_cst__947 * vect__193.31_953 + vect__214.42_930;
  _1307 = _1235 + _1256;
  vect__225.45_921 = MEM[base: vectp.15_1, index: ivtmp.253_329, offset: OFFSET4]; // load @ (base + _999*4 + IV + OFFSET4)
  vect__247.54_900 = MEM[base: vectp.15_1, index: ivtmp.253_329, offset: OFFSET5]; // load @ (base + _999*4 + IV + OFFSET5)
  vect__252.58_893 = vect_cst__894 * vect__247.54_900;
  _1291 = vect_cst__915 * vect__225.45_921 + vect__252.58_893;
  _341 = _1291 + _1307;
  vect__263.61_242 = MEM[base: vectp.15_1, index: ivtmp.253_329, offset: OFFSET6]; // load @ (base + _999*4 + IV + OFFSET6 )
  vect__279.69_1073 = MEM[base: vectp.15_1, index: ivtmp.253_329, offset: OFFSET7]; // load @ (base + _999*4 + IV + OFFSET7)


ICC exploit this successfully, it puts difference to offset:
  402636:       c4 01 64 59 a4 8a 20    vmulps 0x820(%r10,%r9,4),%ymm3,%ymm12
  40263d:       08 00 00
  402640:       c4 01 14 59 b4 8a 30    vmulps 0x1030(%r10,%r9,4),%ymm13,%ymm14
  402647:       10 00 00
  40264a:       c4 02 5d b8 a4 8a 18    vfmadd231ps 0x818(%r10,%r9,4),%ymm4,%ymm12
  402651:       08 00 00
  402654:       c4 02 2d b8 b4 8a 28    vfmadd231ps 0x1028(%r10,%r9,4),%ymm10,%ymm14
  40265b:       10 00 00
  40265e:       c4 41 24 57 db          vxorps %ymm11,%ymm11,%ymm11
  402663:       c4 02 7d b8 9c 8a 2c    vfmadd231ps 0x102c(%r10,%r9,4),%ymm0,%ymm11
  40266a:       10 00 00
  40266d:       c4 02 75 b8 9c 8a 24    vfmadd231ps 0x1024(%r10,%r9,4),%ymm1,%ymm11
  402674:       10 00 00
  402677:       c4 41 24 58 de          vaddps %ymm14,%ymm11,%ymm11
  40267c:       c4 01 6c 59 b4 8a 20    vmulps 0x1020(%r10,%r9,4),%ymm2,%ymm14

This causes GCC to be ~50% slower than ICC on this kernel.


---


### compiler : `gcc`
### title : `SLP vectorization should negate constants to match up + vs -`
### open_at : `2015-10-22T10:03:13Z`
### last_modified_date : `2021-08-30T07:44:05Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=68050
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `6.0`
### severity : `enhancement`
### contents :
double x[1024], y[1024], z[1024];
void foo (double w)
{
  int i;
  for (i = 0; i < 1023; i+=2)
    {
      z[i] = x[i] + 3.;
      z[i+1] = x[i+1] + -3.;
    }
}


---


### compiler : `gcc`
### title : `Expression explicitly defined outside the loop is moved inside the loop by the optimizer`
### open_at : `2015-10-25T03:46:09Z`
### last_modified_date : `2023-05-16T23:22:14Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=68086
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `5.2.0`
### severity : `enhancement`
### contents :
Created attachment 36578
Single function to reproduce the results

Compileable C source in "ex324_core.c" does not include any header files. It consists of a single function whose performance is spoiled by the optimizer. Please read explanatory comments in that file.

"ex324.c" is a compileable test program build around the same core function. It merely measures the amount of CPU clock ticks taken by that core function. It includes system headers for printf and mmap, and is provided just for convenience of testing.

The problem was first discovered in x86_64 gcc 5.2.0 compiler. Brief regression research showed that 4.8.3 has this problem too. 4.7.4 seems to be good.

Problem in a nutshell. Let's start with this loop:

// Case 1
for (i = 0; i < size; ++i)
  accumulator += data[i];

and rewrite it in this equivalent form:

// Case 2
int*  rebased = data + size;
for (i = -size; i; ++i)
  accumulator += rebased[i];

It looks like the forward propagation pass decides not to allocate a register for variable 'rebased', but rather compute its value every time it is used in the loop. This results in assembly output which, if written in terms of C, would look like this:

for (i = -size; i; ++i)
  accumulator += *(data + (size + i));

Extra operation inside the loop only slows the program down.
This happens at any optimization level above -O0.

Command line:
x86_64-unknown-freebsd9.0_5.2.0-gcc -O2 -S ex324_core.c

Compiler:
x86_64-unknown-freebsd9.0_5.2.0-gcc -v
Using built-in specs.
COLLECT_GCC=x86_64-unknown-freebsd9.0_5.2.0-gcc
COLLECT_LTO_WRAPPER=/usr/toolchain/x86_64-unknown-freebsd9.0_5.2.0/libexec/gcc/x86_64-unknown-freebsd9.0/5.2.0/lto-wrapper
Target: x86_64-unknown-freebsd9.0
Configured with: /mnt/hdd/usr/home/toolbuilder/build_scripts/x86_64-unknown-freebsd9.0_5.2.0/build_scripts/../tools_build/x86_64-unknown-freebsd9.0_5.2.0/gcc-5.2.0/configure --target=x86_64-unknown-freebsd9.0 --prefix=/usr/toolchain/x86_64-unknown-freebsd9.0_5.2.0 --with-local-prefix=/usr/local --with-sysroot=/usr/toolchain/x86_64-unknown-freebsd9.0_5.2.0/sysroot --program-prefix=x86_64-unknown-freebsd9.0_5.2.0- --with-gnu-as --with-gnu-ld --with-as=/usr/toolchain/x86_64-unknown-freebsd9.0_5.2.0/bin/x86_64-unknown-freebsd9.0_5.2.0-as --with-ld=/usr/toolchain/x86_64-unknown-freebsd9.0_5.2.0/bin/x86_64-unknown-freebsd9.0_5.2.0-ld --with-nm=/usr/toolchain/x86_64-unknown-freebsd9.0_5.2.0/bin/x86_64-unknown-freebsd9.0_5.2.0-nm --with-objdump=/usr/toolchain/x86_64-unknown-freebsd9.0_5.2.0/bin/x86_64-unknown-freebsd9.0_5.2.0-objdump --with-gmp=/mnt/hdd/usr/home/toolbuilder/build_scripts/x86_64-unknown-freebsd9.0_5.2.0/build_scripts/../tools_build/x86_64-unknown-freebsd9.0_5.2.0/gmp-root --with-mpfr=/mnt/hdd/usr/home/toolbuilder/build_scripts/x86_64-unknown-freebsd9.0_5.2.0/build_scripts/../tools_build/x86_64-unknown-freebsd9.0_5.2.0/mpfr-root --with-mpc=/mnt/hdd/usr/home/toolbuilder/build_scripts/x86_64-unknown-freebsd9.0_5.2.0/build_scripts/../tools_build/x86_64-unknown-freebsd9.0_5.2.0/mpc-root --disable-__cxa_atexit --enable-languages=c,c++ --disable-multilib --disable-nls --enable-shared=libstdc++ --enable-static --enable-threads
Thread model: posix
gcc version 5.2.0 (GCC)

Operating system:
amd64 FreeBSD 9.0-RELEASE

CPU:
Intel(R) Core(TM) i7-2700K CPU @ 3.50GHz (3500.10-MHz K8-class CPU)
  Origin = "GenuineIntel"  Id = 0x206a7  Family = 6  Model = 2a Stepping = 7
Features=0xbfebfbff<FPU,VME,DE,PSE,TSC,MSR,PAE,MCE,CX8,APIC,SEP,MTRR,PGE,MCA,CMOV,PAT,PSE36,CLFLUSH,DTS,ACPI,MMX,FXSR,SSE,SSE2,SS,HTT,TM,PBE>
Features2=0x179ae3bf<SSE3,PCLMULQDQ,DTES64,MON,DS_CPL,VMX,EST,TM2,SSSE3,CX16,xTPR,PDCM,PCID,SSE4.1,SSE4.2,POPCNT,TSCDLT,AESNI,XSAVE,AVX>
  AMD Features=0x28100800<SYSCALL,NX,RDTSCP,LM>
  AMD Features2=0x1<LAHF>


---


### compiler : `gcc`
### title : `We should track ranges for floating-point values too`
### open_at : `2015-10-26T08:48:49Z`
### last_modified_date : `2022-11-28T22:24:32Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=68097
### status : `RESOLVED`
### tags : `compile-time-hog, missed-optimization`
### component : `tree-optimization`
### version : `6.0`
### severity : `enhancement`
### contents :
We have functions to query things like whether a real is nonnegative and whether it is integer-valued.  At the moment we recurse through SSA name definitions, limited by --param max-ssa-name-query-depth, but it would be better to record this information alongside the SSA name, as range_info_def does for integers.


---


### compiler : `gcc`
### title : `GCC fails to vectorize popcount on x86_64`
### open_at : `2015-10-27T03:07:42Z`
### last_modified_date : `2021-08-16T04:50:32Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=68109
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `5.2.0`
### severity : `enhancement`
### contents :
Created attachment 36595
Clang Vectorized Assembly Output

The following code is an SSCCE that GCC doesn't vectorize on x86_64:

#include <stdlib.h>
#include <stdint.h>

size_t hd (const uint8_t *restrict a, const uint8_t *restrict b, size_t l) {
  size_t r = 0, x;
  for (x = 0; x < l; x++)
    r += __builtin_popcount (a[x] ^ b[x]);

  return r;
}

On other architectures, such as power8, GCC successfully vectorizes the loop. However, on x86_64, there doesn't actually exist a vector version of the `popcnt` instruction. Despite this, as shown by [http://wm.ite.pl/articles/sse-popcount.html] it is actually possible to vectorize popcount by using SSE2 or SSSE3 instructions. Further research on [https://software.intel.com/sites/landingpage/IntrinsicsGuide/] shows that it may be possible to achieve further performance on the latest architectures gains by using AVX2 instructions along the same lines as in the article, albeit with 256-bit YMM registers in place of the 128-bit XMM registers used in the article. Since GCC often has support for insofar unreleased architectures, I did a bit more research on the Intel Intrisics Guide mentioned above for future architectures and found that the same could likely also be done using AVX-512 with the 512-bit ZMM registers if you guys are interested.

Anyways, I did find that clang has been doing these optimizations since ~clang3.5. I've attached an output of the resulting [vectorized] assembly emitted by clang3.7 for the above function, since it appears to be done relatively thoroughly and cleanly.

In both GCC and Clang, I used the following flags:

-xc -O2 -ftree-vectorize -D_GNU_SOURCE  -std=gnu11 -fverbose-asm


---


### compiler : `gcc`
### title : `__builtin_sub_overflow unsigned performance issue`
### open_at : `2015-10-27T05:07:04Z`
### last_modified_date : `2021-08-21T22:34:34Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=68110
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `5.2.1`
### severity : `minor`
### contents :
I ran into this minor performance issue when changing Gnulib's lib/intprops.h to use the new __builtin_sub_overflow function. I found that __builtin_sub_overflow is less efficient than the portable C code that it replaced, when the operands and result are unsigned, or unsigned long, or unsigned long long. To reproduce the problem, compile and run the following program with 'gcc -O2 -S' on x86-64:

  _Bool f1 (unsigned long long a, unsigned long long b)
  {
    return a < b;
  }

  _Bool f2 (unsigned long long a, unsigned long long b)
  {
    unsigned long long r;
    return __builtin_sub_overflow (a, b, &r);
  }

Although the functions are semantically equivalent, f1 uses only 3 instructions:

	f1:
		cmpq	%rsi, %rdi
		setb	%al
		ret

whereas f2 uses 5 instructions:

	f2:
		movq	%rdi, %rax
		subq	%rsi, %rax
		cmpq	%rdi, %rax
		seta	%al
		ret

There is a similar problem for x86.


---


### compiler : `gcc`
### title : `GCC vector extension behaves funny with large vector size`
### open_at : `2015-10-27T22:00:25Z`
### last_modified_date : `2021-08-10T23:03:26Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=68123
### status : `NEW`
### tags : `compile-time-hog, missed-optimization`
### component : `tree-optimization`
### version : `4.8.3`
### severity : `enhancement`
### contents :
Created attachment 36599
test source file

It would complete unroll the loop and produces a huge assembly.
With -O3 the produced assembly is smaller, but compilation takes a lot longer than no -O3. 

I attached test source file.
With
CFLAGS=-std=gnu11 -O3 -mcpu=cortex-a9 -mfloat-abi=hard -mfpu=neon -fPIE -Wall -S -fverbose-asm
it compiles to a 57K line assembly and takes about 2min to compile, on a XEON 1245v3 machine.

Tested on "GCC: (crosstool-NG linaro-1.13.1-4.8-2013.11 - Linaro GCC 2013.10) 4.8.3 20131111 (prerelease)"


---


### compiler : `gcc`
### title : `missed optimization and warning for broken overflow check`
### open_at : `2015-10-28T11:39:42Z`
### last_modified_date : `2023-10-24T20:45:50Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=68131
### status : `RESOLVED`
### tags : `diagnostic, missed-optimization`
### component : `tree-optimization`
### version : `5.1.0`
### severity : `normal`
### contents :
Using "a + b < a" is the standard (and well-defined) way of checking for overflow when adding unsigned variables a,b. However, due to promotion rules, this breaks down when a and b have type narrower than int. Consider

struct s {
	unsigned short x;
};

int f(struct s *a, const struct s *b)
{
	if (a->x + b->x < a->x)
		return -1;
	a->x += b->x;
	return 0;
}

The conditional is never true, but neither clang or gcc warns (with -Wall -Wextra) about what was obviously intended to be an overflow check. clang does compile this to

   0:   66 8b 06                mov    (%rsi),%ax
   3:   66 01 07                add    %ax,(%rdi)
   6:   31 c0                   xor    %eax,%eax
   8:   c3                      retq   

whereas gcc generates

   0:   0f b7 0f                movzwl (%rdi),%ecx
   3:   0f b7 16                movzwl (%rsi),%edx
   6:   89 d0                   mov    %edx,%eax
   8:   01 ca                   add    %ecx,%edx
   a:   39 d1                   cmp    %edx,%ecx
   c:   7f 12                   jg     20 <f+0x20>
   e:   01 c8                   add    %ecx,%eax
  10:   66 89 07                mov    %ax,(%rdi)
  13:   31 c0                   xor    %eax,%eax
  15:   c3                      retq   
  16:   66 2e 0f 1f 84 00 00    nopw   %cs:0x0(%rax,%rax,1)
  1d:   00 00 00 
  20:   b8 ff ff ff ff          mov    $0xffffffff,%eax
  25:   c3                      retq


---


### compiler : `gcc`
### title : `missed tree-level optimization with redundant computations`
### open_at : `2015-10-28T14:39:16Z`
### last_modified_date : `2023-10-24T03:57:34Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=68136
### status : `NEW`
### tags : `missed-optimization, TREE`
### component : `tree-optimization`
### version : `6.0`
### severity : `enhancement`
### contents :
Take the testcase gcc.dg/ifcvt-3.c:
typedef long long s64;

int
foo (s64 a, s64 b, s64 c)
{
 s64 d = a - b;

  if (d == 0)
    return a + c;
  else
    return b + d + c;
}


on aarch64 this produces the simplest possible:
foo:
        add     w0, w2, w0
        ret


However, this is due to RTL-level ifconversion.
The final tree dump is the more complex:
foo (s64D.2694 aD.2695, s64D.2694 bD.2696, s64D.2694 cD.2697)
{
  s64D.2694 dD.2700;
  intD.7 _1;
  unsigned int _5;
  unsigned int _7;
  unsigned int _8;
  intD.7 _9;
  unsigned int _10;
  unsigned int _11;
  unsigned int _13;
  unsigned int _14;
  intD.7 _15;
  unsigned int _17;

;;   basic block 2, loop depth 0, count 0, freq 10000, maybe hot
;;    prev block 0, next block 3, flags: (NEW, REACHABLE)
;;    pred:       ENTRY [100.0%]  (FALLTHRU,EXECUTABLE)
  d_4 = a_2(D) - b_3(D);
  if (d_4 == 0)
    goto <bb 3>;
  else
    goto <bb 4>;
;;    succ:       3 [39.0%]  (TRUE_VALUE,EXECUTABLE)
;;                4 [61.0%]  (FALSE_VALUE,EXECUTABLE)

;;   basic block 3, loop depth 0, count 0, freq 3900, maybe hot
;;    prev block 2, next block 4, flags: (NEW, REACHABLE)
;;    pred:       2 [39.0%]  (TRUE_VALUE,EXECUTABLE)
  # RANGE [0, 4294967295]
  _5 = (unsigned int) a_2(D);
  # RANGE [0, 4294967295]
  _7 = (unsigned int) c_6(D);
  # RANGE [0, 4294967295]
  _8 = _5 + _7;
  _9 = (intD.7) _8;
  goto <bb 5>;
;;    succ:       5 [100.0%]  (FALLTHRU,EXECUTABLE)

;;   basic block 4, loop depth 0, count 0, freq 6100, maybe hot
;;    prev block 3, next block 5, flags: (NEW, REACHABLE)
;;    pred:       2 [61.0%]  (FALSE_VALUE,EXECUTABLE)
  # RANGE [0, 4294967295]
  _10 = (unsigned int) b_3(D);
  # RANGE [0, 4294967295]
  _11 = (unsigned int) d_4;
  # RANGE [0, 4294967295]
  _13 = (unsigned int) c_6(D);
  # RANGE [0, 4294967295]
  _17 = _10 + _13;
  # RANGE [0, 4294967295]
  _14 = _11 + _17;
  _15 = (intD.7) _14;
;;    succ:       5 [100.0%]  (FALLTHRU,EXECUTABLE)

;;   basic block 5, loop depth 0, count 0, freq 10000, maybe hot
;;    prev block 4, next block 1, flags: (NEW, REACHABLE)
;;    pred:       3 [100.0%]  (FALLTHRU,EXECUTABLE)
;;                4 [100.0%]  (FALLTHRU,EXECUTABLE)
  # _1 = PHI <_9(3), _15(4)>
  # VUSE <.MEM_16(D)>
  return _1;
;;    succ:       EXIT [100.0%] 

}

It's probably a good idea to detect this earlier and produce a " return a + c;"
at the tree level


---


### compiler : `gcc`
### title : `Free __m128d subreg of double`
### open_at : `2015-11-04T16:40:58Z`
### last_modified_date : `2021-09-05T08:13:18Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=68211
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `6.0`
### severity : `enhancement`
### contents :
Hello,

we still seem to be missing some way of passing a double to intrinsics that take a __m128d argument (see below for an example) without any overhead when we do not care about the high part.

__m128d to __m256d has an intrinsic, although its implementation is not optimal (see PR 50829). But Intel apparently "forgot" to add a similar one for double to __m128d.

Say I want to use the new AVX512 _mm_sqrt_round_sd to compute the square root of a double rounded towards +infinity. Using -mavx512f, I can try:

#include <x86intrin.h>

double sqrt_up(double x){
  __m128d y = { x, 0 };
  return _mm_cvtsd_f64(_mm_sqrt_round_sd(y, y, _MM_FROUND_TO_POS_INF|_MM_FROUND_NO_EXC));
}

which generates

	vmovsd	%xmm0, -16(%rsp)
	vmovsd	-16(%rsp), %xmm0
	vsqrtsd	{ru-sae}, %xmm0, %xmm0, %xmm0

I get the exact same code with

  double d = d;
  __m128d y = { x, d };

or

  __m128d y = y;
  y[0] = x;

I can shorten it to

	vmovddup	%xmm0, %xmm0
	vsqrtsd	{ru-sae}, %xmm0, %xmm0, %xmm0

using

  __m128d y = { x, x };

I am forced to use inline asm

  __m128d y;
  asm("":"=x"(y):"0"(x));

to get what I wanted, i.e. only vsqrtsd without any extra instruction. But that makes the code non-portable, and I might as well write the vsqrtsd instruction myself in the asm. It probably also has similar drawbacks to the unspec in PR 50829.


---


### compiler : `gcc`
### title : `__builtin_unreachable pessimizes code`
### open_at : `2015-11-10T14:47:38Z`
### last_modified_date : `2023-06-07T13:21:44Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=68274
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `5.2.0`
### severity : `enhancement`
### contents :
While experimenting with __builtin_unreachable I found that in some cases adding it pessimizes the code. Consider the following code (also at https://goo.gl/WmR8PX):

--
enum Side { Bid, Ask };
struct Foo {  int a;  int b; };

int test(Side side, const Foo &foo) {
  if (side == Bid) return foo.a;
  return foo.b;
}

int test_with_unreach(Side side, const Foo &foo) {
  if (side == Bid) return foo.a;
  if (side != Ask) __builtin_unreachable();
  return foo.b;
}
--

In the non-unreachable case `test`, the code generates the cmove I'd expect:

--
test(Side, Foo const&):
	mov	eax, DWORD PTR [rsi+4]
	test	edi, edi
	cmove	eax, DWORD PTR [rsi]
	ret
--

In the unreachable case, GCC resorts back to branching:

--
test_with_unreach(Side, Foo const&):
	test	edi, edi
	je	.L9
	mov	eax, DWORD PTR [rsi+4]
	ret
.L9:
	mov	eax, DWORD PTR [rsi]
	ret
--

It's not really clear to me how much of a pessimization this is; but it was surprising that the unreachability had such an effect.

I was hoping to prove to the compiler that the only valid inputs were "Bid" and "Ask" and as such it could actually generate something like:

--
mov eax, DWORD PTR[rsi+eax*4]
ret
--


---


### compiler : `gcc`
### title : `bb-slp-38 FAILs on armeb`
### open_at : `2015-11-10T15:18:19Z`
### last_modified_date : `2021-12-27T22:35:01Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=68275
### status : `NEW`
### tags : `FIXME, missed-optimization, testsuite-fail`
### component : `target`
### version : `6.0`
### severity : `normal`
### contents :
Created attachment 36677
slp1 log, big-endian

The vect/bb-slp-38.c test recently introduced fails on armeb and passes on arm.

GCC configured as:
--target=armeb-none-linux-gnueabihf --with-float=hard --with-mode=arm --with-cpu=cortex-a9 --with-fpu=neon

I attach the vectorizer logs in LE and BE modes.


---


### compiler : `gcc`
### title : `Optimization fails to remove unnecessary sign extension instruction`
### open_at : `2015-11-11T00:06:30Z`
### last_modified_date : `2021-08-19T13:57:44Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=68282
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `6.0`
### severity : `enhancement`
### contents :
For the code

int table[256];

int func(unsigned char c)
{
  return table[(c >> 2) + 1];
}

x86-64 gcc -m64 -O2 generates

        movzbl  %dil, %eax
        sarl    $2, %eax
        addl    $1, %eax
        cltq
        movl    table(,%rax,4), %eax
        ret

where the cltq is not really needed.

Current Clang produces

        shrl    $2, %edi
        incl    %edi
        movl    table(,%rdi,4), %eax
        retq

which is more like what we would want.


---


### compiler : `gcc`
### title : `gcc cannot deduce (a | b) != 0 from (a != 0 && b != 0)`
### open_at : `2015-11-11T11:57:54Z`
### last_modified_date : `2021-08-03T02:09:47Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=68294
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `5.1.0`
### severity : `normal`
### contents :
I implemented Stein's binary gcd algorithm, which contains code like this:

        int u, v, k;

        /* ... */

    	if (u == 0 || v == 0)
		return (u | v);

	k = ffs(u | v) - 1;

Sadly, for the ffs() call, gcc emits (on x86 where behaviour of bsf is unclear if the operand is zero) code for the case when u | v is zero, even though this possibility has been ruled out in the if-statement before. Adding a redundant clause

        if ((u | v) == 0 || u == 0 || v == 0)

to the if-statement makes the compiler omit the extra code it emits above, but then it emits an extra unneeded test for (u | v) == 0.

It would be great if gcc would catch this.


---


### compiler : `gcc`
### title : `[4.8 4.9]gcc using array index to accelerate loop running , why turn off at gcc 5.X`
### open_at : `2015-11-13T09:14:27Z`
### last_modified_date : `2021-08-11T04:09:34Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=68329
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.5`
### severity : `normal`
### contents :



---


### compiler : `gcc`
### title : `std::uninitialized_copy overly restrictive for trivially_copyable types`
### open_at : `2015-11-14T17:26:40Z`
### last_modified_date : `2023-07-27T09:21:56Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=68350
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `libstdc++`
### version : `5.2.0`
### severity : `enhancement`
### contents :
I think the following decision is too restrictive:

return std::__uninitialized_copy<__is_trivial(_ValueType1)
			      && __is_trivial(_ValueType2)
		              && __assignable>::
	__uninit_copy(__first, __last, __result);

(cf. stl_uninitialized.h:123ff). The following should be sufficient:

return std::__uninitialized_copy<is_trivially_copyable(_ValueType1)
			      && is_trivially_copyable(_ValueType2)
		              && __assignable>::
	__uninit_copy(__first, __last, __result);

Found this in 5.2.0 and 6.0. Probably it's in versions prior to 5.2.0 as well.


---


### compiler : `gcc`
### title : `GCC bitfield processing code is very inefficient`
### open_at : `2015-11-15T14:43:13Z`
### last_modified_date : `2023-07-19T04:06:12Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=68360
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `5.2.0`
### severity : `enhancement`
### contents :
It looks like GCC couldn't generate efficient code where clang could. I'm not talking about something extremely complicated - just the code where few bits must be copied without modifications.

E.g.

$ cat test.c
#include <string.h>

struct test {
  unsigned :32;
  unsigned :2;
  unsigned a:2;
  unsigned :2;
  unsigned b:1;
  unsigned :1;
};

void bar(struct test*);

void foo(unsigned int i) {
  struct test a;
  a.a = (i >> 2) & 0x3;
  a.b = (i >> 6) & 0x1;
  bar(&a);
}

$ clang -O3 -S test2.c -o-
        .text
        .file   "test2.c"
        .globl  foo
        .align  16, 0x90
        .type   foo,@function
foo:                                    # @foo
# BB#0:
        subl    $28, %esp
        movl    32(%esp), %eax
        andl    $76, %eax
        movl    %eax, 20(%esp)
        movl    $0, 16(%esp)
        leal    16(%esp), %eax
        movl    %eax, (%esp)
        calll   bar
        addl    $28, %esp
        retl
.Lfunc_end0:
        .size   foo, .Lfunc_end0-foo


        .ident  "clang version 3.6 "
        .section        ".note.GNU-stack","",@progbits
$ g++ -O3 -S test2.c -o-
        .file   "test2.c"
        .section        .text.unlikely,"ax",@progbits
.LCOLDB0:
        .text
.LHOTB0:
        .p2align 4,,15
        .globl  _Z3fooj
        .type   _Z3fooj, @function
_Z3fooj:
.LFB14:
        .cfi_startproc
        subq    $24, %rsp
        .cfi_def_cfa_offset 32
        movl    %edi, %edx
        shrl    $6, %edi
        movzbl  4(%rsp), %ecx
        shrl    $2, %edx
        andl    $1, %edi
        andl    $3, %edx
        movl    %edi, %eax
        sall    $2, %edx
        sall    $6, %eax
        andl    $-77, %ecx
        orl     %edx, %ecx
        movl    %ecx, %edi
        orl     %eax, %edi
        movb    %dil, 4(%rsp)
        movq    %rsp, %rdi
        call    _Z3barP4test
        addq    $24, %rsp
        .cfi_def_cfa_offset 8
        ret
        .cfi_endproc
.LFE14:
        .size   _Z3fooj, .-_Z3fooj
        .section        .text.unlikely
.LCOLDE0:
        .text
.LHOTE0:
        .ident  "GCC: (GNU) 5.2.0"
        .section        .note.GNU-stack,"",@progbits


---


### compiler : `gcc`
### title : `Return value optimization does not fire iff in C mode`
### open_at : `2015-11-17T07:15:05Z`
### last_modified_date : `2022-02-24T06:45:31Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=68378
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.8.4`
### severity : `enhancement`
### contents :
struct Foo { int x[1000]; };
struct Foo f(void);
struct Foo g(void) {
    struct Foo x = f();
    return x;
}

When built with -O3 -xc this generates superfluous inefficient copying.
When built with -O3 -xc++ this generates an efficient call without copying.

Copying should not be generated here.


---


### compiler : `gcc`
### title : `unused copy of global register variable into another gpr`
### open_at : `2015-11-18T21:06:17Z`
### last_modified_date : `2023-05-26T02:33:00Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=68421
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `6.0`
### severity : `normal`
### contents :
Created attachment 36767
test case for unused registers

There are unneeded moves from the global register variables to other registers generated.

register zend_execute_data *execute_data __asm__("r28");
register const zend_op *opline __asm__("r29");
int ZEND_IS_SMALLER_SPEC_CV_CV_HANDLER(void)
{
 zval *op1, *op2, *result;
 op1 = _get_zval_ptr_cv_undef(execute_data, opline->op1.var);
 if (__builtin_expect(!!(zval_get_type(&(*(op1))) == 4), 1)) {
  if (__builtin_expect(!!(zval_get_type(&(*(op2))) == 4), 1)) {
   do { (*(((zval*)(((char*)(execute_data)) + ((int)(opline->result.var)))))).u1.type_info = ((*(op1)).value.lval < (*(op2)).value.lval) ? 3 : 2; } while (0);
  }
 }
 ((execute_data)->opline) = opline;
}

generates:

ZEND_IS_SMALLER_SPEC_CV_CV_HANDLER:
        lwa 6,0(29)
        mr 8,29
        mr 10,28
        add 9,28,6
        lbz 9,8(9)
        cmpwi 7,9,4
        bne 7,.L3
        li 7,0
        lbz 9,8(7)
        cmpwi 7,9,4
        bne 7,.L3
        ldx 9,28,6
        ld 6,0(7)
        lwa 7,4(29)
        cmpd 7,9,6
        add 7,28,7
        mfcr 9,1
        rlwinm 9,9,29,1
        addi 9,9,2
        stw 9,8(7)
.L3:
        std 8,0(10)

Registers 8 and 10 are never used, 28 and 29 are used directly.

Generated by trunk 230468 on ppc64le with:

gcc -O3 -S min_unused_regs10.c


---


### compiler : `gcc`
### title : `[ARM] Use vector multiply by lane`
### open_at : `2015-11-23T05:03:37Z`
### last_modified_date : `2018-12-20T14:17:01Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=68494
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `6.0`
### severity : `enhancement`
### contents :
The following test case should utilize vector multiply by a single lane.

short taps[4];

void fir_t5(int len, short * __restrict p, short *__restrict x, short *__restrict taps)
{
  len = len & ~31;
  for (int i = 0; i < len; i++)
    {
      int tmp = 0;
      for (int j = 0; j < NTAPS; j++)
	{
	  tmp += x[i - j] * taps[j];
	}

      p[i] = tmp;
    }
}


---


### compiler : `gcc`
### title : `[AArch64] Implement overflow arithmetic standard names {u,}{add,sub,mul}v4<mode> and/or negv3<mode>`
### open_at : `2015-11-25T17:26:00Z`
### last_modified_date : `2019-11-14T09:12:05Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=68543
### status : `RESOLVED`
### tags : `missed-optimization, patch`
### component : `target`
### version : `6.0`
### severity : `enhancement`
### contents :
As mentioned in https://gcc.gnu.org/bugzilla/show_bug.cgi?id=66112#c13
we should consider implementing the various overflow arithmetic standard name expanders that take a label argument and emit a jump to it if the operation overflows.

A motivational example is the code quality regression from PR 68381:
int
foo(unsigned short x, unsigned short y)
{
  int r;
  if (__builtin_mul_overflow (x, y, &r))
    __builtin_abort ();
  return r;
}

which for aarch64 at -O3 generates:
foo:
        uxth    w0, w0
        uxth    w1, w1
        umull   x0, w0, w1
        tbnz    w0, #31, .L6
        mov     w2, 0
        cbnz    w2, .L6
        ret
.L6:
        stp     x29, x30, [sp, -16]!
        add     x29, sp, 0
        bl      abort

which could be improved


---


### compiler : `gcc`
### title : `Missed x86 peephole optimization for multiplying by a bool`
### open_at : `2015-11-26T14:00:39Z`
### last_modified_date : `2022-11-26T07:02:18Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=68557
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `5.1.0`
### severity : `enhancement`
### contents :
On x86 the following code

void bar (int x);

void
baz (int x, bool b)
{
  bar (x * b);
}


is compiled to


bar:
        movzbl  %sil, %esi
        imull   %esi, %edi
        jmp     baz


when it could instead be compiled to

bar:
        movzbl  %sil, %esi
        negl    %esi
        andl    %esi, %edi
        jmp     baz


On modern processors the "neg" and "and" instructions takes a minimum of one cycle each, whereas the "imul" instruction takes a minimum three cycles.  So transforming "x * (int)b" to "x & -(int)b" would save one cycle in the best case.


---


### compiler : `gcc`
### title : `get_integer_range () that handles symbolical ranges`
### open_at : `2015-11-26T16:18:28Z`
### last_modified_date : `2022-01-11T21:06:29Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=68561
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `6.0`
### severity : `enhancement`
### contents :
As mentioned here <https://gcc.gnu.org/ml/gcc-patches/2015-11/msg02758.html>, it would be nice to implement get_integer_range () function that handles symbolical ranges better.


---


### compiler : `gcc`
### title : `SSE2 cannot vec_perm of low and high part`
### open_at : `2015-12-02T13:55:48Z`
### last_modified_date : `2021-08-03T07:03:08Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=68655
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `6.0`
### severity : `enhancement`
### contents :
typedef unsigned short v8hi __attribute__((vector_size(16)));

v8hi foo (v8hi a, v8hi b)
{
  return __builtin_shuffle (a, b, (v8hi) { 0, 1, 2, 3, 8, 9, 10, 11 });
}

should be able to use

  movlhps %xmm0, %xmm1
  ret

but ends up being lowered by vector lowering because the target says
it cannot can_vec_perm_p (V8HI, false, { 0, 1, 2, 3, 8, 9, 10, 11 })

There are also two-instruction permutes possible with movhl/lhps
like { 0, 1, 2, 3, 12, 13, 14, 15 } can use

  movhlps %xmm1, %xmm1
  movlhps %xmm0, %xmm1

ah, that uses shufpd.  Not sure why the above doesn't use shufpd if that
is available in SSE2.


---


### compiler : `gcc`
### title : `SLP loads should be permuted until supported if possible`
### open_at : `2015-12-04T09:53:07Z`
### last_modified_date : `2022-02-01T07:35:50Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=68694
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `6.0`
### severity : `enhancement`
### contents :
gcc.dg/vect/pr45752.c FAILs with --param=tree-reassoc-width=2 because the
association lets us arrive with a load permutation we don't support.  With
this testcase it's possible to shuffle the SLP tree (without making it invalid)
making the load permutation supported.


---


### compiler : `gcc`
### title : `suboptimal handling of constant compound literals`
### open_at : `2015-12-05T18:46:26Z`
### last_modified_date : `2021-09-30T01:53:40Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=68725
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `c`
### version : `5.1.0`
### severity : `normal`
### contents :
The motivation for this comes from the linux kernel's
include/trace/trace_events.h file (hence the cc Steven Rostedt), in
particular the __print_flags and __print_symbolic macros. They are
invoked multiple times with the same list of flag_array initializers,
which causes identical copies of the defined static array to be stored
in .rodata. The obvious solution, to define the array once in some .c
file and declare it extern, is rather inconvenient to try to retrofit
to the way the tracing subsystem works.

So I decided to try and see if using anonymous objects (compound
literals) would work. It turns out it did, and then it didn't. gcc is
smart enough to only emit a single copy to .rodata (at least within a
single translation unit, but that's good enough in this
case). However, at each use site, gcc decides to make a stack copy and
pass a pointer to that copy on to trace_print_flags_seq function. This
is very inefficient, completely redundant, and since some of the
arrays are over 1k in size, unacceptable in kernel code.

The problem can be seen in the example below. For smaller arrays, gcc
doesn't seem to put a copy in .rodata; it constructs the array on the
stack with a sequence of movq instructions, which is even more
inefficient (the .text to build the array takes more space than a copy
of the array in .rodata + a memcpy would) and equally wasteful. And it
gets even worse when one looks at the g functions, where the stack use
is doubled, and the copy/construction is done twice.

For const-qualified compound literals with compile-time constant
initializers, which are not explicitly used to initialize another
object, I don't see any reason to actually construct such an
object. [Maybe as an optimization if the object only takes up a few
words, but even that is questionable.] As soon as the size is greater
than, say, 32 bytes, I think it would much better to just refer to a
single copy in .rodata.

I've tried gcc 4.9, 5.1 and both -O2, -O3, and they all show the same
behaviour.

// gcc -std=gnu89 -O2 -o complit.o -c complit.c

#include <stddef.h>

struct flag_name { unsigned long mask; const char *name; };

#define FLAG_0 (1UL << 0)
#define FLAG_1 (1UL << 1)
#define FLAG_2 (1UL << 2)
#define FLAG_3 (1UL << 3)
#define FLAG_4 (1UL << 4)
#define FLAG_5 (1UL << 5)
#define FLAG_6 (1UL << 6)
#define FLAG_7 (1UL << 7)
#define FLAG_8 (1UL << 8)
#define FLAG_9 (1UL << 9)
#define FLAG_10 (1UL << 10)
#define FLAG_11 (1UL << 11)
#define FLAG_12 (1UL << 12)
#define FLAG_13 (1UL << 13)
#define FLAG_14 (1UL << 14)
#define FLAG_15 (1UL << 15)
#define FLAG_16 (1UL << 16)
#define FLAG_17 (1UL << 17)
#define FLAG_18 (1UL << 18)
#define FLAG_19 (1UL << 19)
#define FLAG_20 (1UL << 20)
#define FLAG_21 (1UL << 21)
#define FLAG_22 (1UL << 22)
#define FLAG_23 (1UL << 23)
#define FLAG_24 (1UL << 24)
#define FLAG_25 (1UL << 25)
#define FLAG_26 (1UL << 26)
#define FLAG_27 (1UL << 27)
#define FLAG_28 (1UL << 28)
#define FLAG_29 (1UL << 29)
#define FLAG_30 (1UL << 30)
#define FLAG_31 (1UL << 31)
#define FLAG_32 (1UL << 32)

#define flag_pair(f) {f, #f}
#define FLAG_NAMES	   \
        flag_pair(FLAG_0), \
        flag_pair(FLAG_1), \
        flag_pair(FLAG_2), \
        flag_pair(FLAG_3), \
        flag_pair(FLAG_4), \
        flag_pair(FLAG_5), \
        flag_pair(FLAG_6), \
        flag_pair(FLAG_7), \
        flag_pair(FLAG_8), \
        flag_pair(FLAG_9), \
        flag_pair(FLAG_10), \
        flag_pair(FLAG_11), \
        flag_pair(FLAG_12), \
        flag_pair(FLAG_13), \
        flag_pair(FLAG_14), \
        flag_pair(FLAG_15), \
        flag_pair(FLAG_16), \
        flag_pair(FLAG_17), \
        flag_pair(FLAG_18), \
        flag_pair(FLAG_19), \
        flag_pair(FLAG_20), \
        flag_pair(FLAG_21), \
        flag_pair(FLAG_22), \
        flag_pair(FLAG_23), \
        flag_pair(FLAG_24), \
        flag_pair(FLAG_25), \
        flag_pair(FLAG_26), \
        flag_pair(FLAG_27), \
        flag_pair(FLAG_28), \
        flag_pair(FLAG_29), \
        flag_pair(FLAG_30), \
        flag_pair(FLAG_31), \
        flag_pair(FLAG_32)

#define FLAG_NAMES2	   \
        flag_pair(FLAG_0), \
        flag_pair(FLAG_1), \
        flag_pair(FLAG_2), \
        flag_pair(FLAG_3), \
	flag_pair(FLAG_4)

void print_flags(const char *s, unsigned long flags, const struct flag_name *names);

void f(unsigned long flags)
{
	print_flags("foo", flags, (const struct flag_name[]){ FLAG_NAMES, {-1UL, NULL}});
}

void g(unsigned long flags)
{
	print_flags("bar", flags, (const struct flag_name[]){ FLAG_NAMES, {-1UL, NULL}});
	flags &= 0x07;
	print_flags("baz", flags, (const struct flag_name[]){ FLAG_NAMES, {-1UL, NULL}});
}

void f2(unsigned long flags)
{
	print_flags("foo", flags, (const struct flag_name[]){ FLAG_NAMES2, {-1UL, NULL}});
}

void g2(unsigned long flags)
{
	print_flags("bar", flags, (const struct flag_name[]){ FLAG_NAMES2, {-1UL, NULL}});
	flags &= 0x07;
	print_flags("baz", flags, (const struct flag_name[]){ FLAG_NAMES2, {-1UL, NULL}});
}

objdump output:

complit.o:     file format elf64-x86-64


Disassembly of section .text:

0000000000000000 <f>:
   0:	48 81 ec 28 02 00 00                	sub    $0x228,%rsp
   7:	49 89 f8                            	mov    %rdi,%r8
   a:	be 00 00 00 00                      	mov    $0x0,%esi
			b: R_X86_64_32	.rodata
   f:	48 89 e7                            	mov    %rsp,%rdi
  12:	48 89 e2                            	mov    %rsp,%rdx
  15:	b9 44 00 00 00                      	mov    $0x44,%ecx
  1a:	f3 48 a5                            	rep movsq %ds:(%rsi),%es:(%rdi)
  1d:	4c 89 c6                            	mov    %r8,%rsi
  20:	bf 00 00 00 00                      	mov    $0x0,%edi
			21: R_X86_64_32	.rodata.str1.1
  25:	e8 00 00 00 00                      	callq  2a <f+0x2a>
			26: R_X86_64_PC32	print_flags-0x4
  2a:	48 81 c4 28 02 00 00                	add    $0x228,%rsp
  31:	c3                                  	retq   
  32:	66 66 66 66 66 2e 0f 1f 84 00 00 00 	data16 data16 data16 data16 nopw %cs:0x0(%rax,%rax,1)
  3e:	00 00 

0000000000000040 <g>:
  40:	53                                  	push   %rbx
  41:	48 89 fb                            	mov    %rdi,%rbx
  44:	be 00 00 00 00                      	mov    $0x0,%esi
			45: R_X86_64_32	.rodata
  49:	b9 44 00 00 00                      	mov    $0x44,%ecx
  4e:	48 81 ec 40 04 00 00                	sub    $0x440,%rsp
  55:	48 89 e2                            	mov    %rsp,%rdx
  58:	48 89 e7                            	mov    %rsp,%rdi
  5b:	f3 48 a5                            	rep movsq %ds:(%rsi),%es:(%rdi)
  5e:	48 89 de                            	mov    %rbx,%rsi
  61:	bf 00 00 00 00                      	mov    $0x0,%edi
			62: R_X86_64_32	.rodata.str1.1+0x102
  66:	83 e3 07                            	and    $0x7,%ebx
  69:	e8 00 00 00 00                      	callq  6e <g+0x2e>
			6a: R_X86_64_PC32	print_flags-0x4
  6e:	48 8d 94 24 20 02 00 00             	lea    0x220(%rsp),%rdx
  76:	48 8d bc 24 20 02 00 00             	lea    0x220(%rsp),%rdi
  7e:	be 00 00 00 00                      	mov    $0x0,%esi
			7f: R_X86_64_32	.rodata
  83:	b9 44 00 00 00                      	mov    $0x44,%ecx
  88:	f3 48 a5                            	rep movsq %ds:(%rsi),%es:(%rdi)
  8b:	48 89 de                            	mov    %rbx,%rsi
  8e:	bf 00 00 00 00                      	mov    $0x0,%edi
			8f: R_X86_64_32	.rodata.str1.1+0x106
  93:	e8 00 00 00 00                      	callq  98 <g+0x58>
			94: R_X86_64_PC32	print_flags-0x4
  98:	48 81 c4 40 04 00 00                	add    $0x440,%rsp
  9f:	5b                                  	pop    %rbx
  a0:	c3                                  	retq   
  a1:	66 66 66 66 66 66 2e 0f 1f 84 00 00 	data16 data16 data16 data16 data16 nopw %cs:0x0(%rax,%rax,1)
  ad:	00 00 00 

00000000000000b0 <f2>:
  b0:	48 83 ec 68                         	sub    $0x68,%rsp
  b4:	48 89 fe                            	mov    %rdi,%rsi
  b7:	bf 00 00 00 00                      	mov    $0x0,%edi
			b8: R_X86_64_32	.rodata.str1.1
  bc:	48 89 e2                            	mov    %rsp,%rdx
  bf:	48 c7 04 24 01 00 00 00             	movq   $0x1,(%rsp)
  c7:	48 c7 44 24 08 00 00 00 00          	movq   $0x0,0x8(%rsp)
			cc: R_X86_64_32S	.rodata.str1.1+0x4
  d0:	48 c7 44 24 10 02 00 00 00          	movq   $0x2,0x10(%rsp)
  d9:	48 c7 44 24 18 00 00 00 00          	movq   $0x0,0x18(%rsp)
			de: R_X86_64_32S	.rodata.str1.1+0xb
  e2:	48 c7 44 24 20 04 00 00 00          	movq   $0x4,0x20(%rsp)
  eb:	48 c7 44 24 28 00 00 00 00          	movq   $0x0,0x28(%rsp)
			f0: R_X86_64_32S	.rodata.str1.1+0x12
  f4:	48 c7 44 24 30 08 00 00 00          	movq   $0x8,0x30(%rsp)
  fd:	48 c7 44 24 38 00 00 00 00          	movq   $0x0,0x38(%rsp)
			102: R_X86_64_32S	.rodata.str1.1+0x19
 106:	48 c7 44 24 40 10 00 00 00          	movq   $0x10,0x40(%rsp)
 10f:	48 c7 44 24 48 00 00 00 00          	movq   $0x0,0x48(%rsp)
			114: R_X86_64_32S	.rodata.str1.1+0x20
 118:	48 c7 44 24 50 ff ff ff ff          	movq   $0xffffffffffffffff,0x50(%rsp)
 121:	48 c7 44 24 58 00 00 00 00          	movq   $0x0,0x58(%rsp)
 12a:	e8 00 00 00 00                      	callq  12f <f2+0x7f>
			12b: R_X86_64_PC32	print_flags-0x4
 12f:	48 83 c4 68                         	add    $0x68,%rsp
 133:	c3                                  	retq   
 134:	66 66 66 2e 0f 1f 84 00 00 00 00 00 	data16 data16 nopw %cs:0x0(%rax,%rax,1)

0000000000000140 <g2>:
 140:	55                                  	push   %rbp
 141:	53                                  	push   %rbx
 142:	48 c7 c5 ff ff ff ff                	mov    $0xffffffffffffffff,%rbp
 149:	48 89 fe                            	mov    %rdi,%rsi
 14c:	48 89 fb                            	mov    %rdi,%rbx
 14f:	bf 00 00 00 00                      	mov    $0x0,%edi
			150: R_X86_64_32	.rodata.str1.1+0x102
 154:	48 81 ec c8 00 00 00                	sub    $0xc8,%rsp
 15b:	83 e3 07                            	and    $0x7,%ebx
 15e:	48 89 e2                            	mov    %rsp,%rdx
 161:	48 89 6c 24 50                      	mov    %rbp,0x50(%rsp)
 166:	48 c7 04 24 01 00 00 00             	movq   $0x1,(%rsp)
 16e:	48 c7 44 24 08 00 00 00 00          	movq   $0x0,0x8(%rsp)
			173: R_X86_64_32S	.rodata.str1.1+0x4
 177:	48 c7 44 24 10 02 00 00 00          	movq   $0x2,0x10(%rsp)
 180:	48 c7 44 24 18 00 00 00 00          	movq   $0x0,0x18(%rsp)
			185: R_X86_64_32S	.rodata.str1.1+0xb
 189:	48 c7 44 24 20 04 00 00 00          	movq   $0x4,0x20(%rsp)
 192:	48 c7 44 24 28 00 00 00 00          	movq   $0x0,0x28(%rsp)
			197: R_X86_64_32S	.rodata.str1.1+0x12
 19b:	48 c7 44 24 30 08 00 00 00          	movq   $0x8,0x30(%rsp)
 1a4:	48 c7 44 24 38 00 00 00 00          	movq   $0x0,0x38(%rsp)
			1a9: R_X86_64_32S	.rodata.str1.1+0x19
 1ad:	48 c7 44 24 40 10 00 00 00          	movq   $0x10,0x40(%rsp)
 1b6:	48 c7 44 24 48 00 00 00 00          	movq   $0x0,0x48(%rsp)
			1bb: R_X86_64_32S	.rodata.str1.1+0x20
 1bf:	48 c7 44 24 58 00 00 00 00          	movq   $0x0,0x58(%rsp)
 1c8:	e8 00 00 00 00                      	callq  1cd <g2+0x8d>
			1c9: R_X86_64_PC32	print_flags-0x4
 1cd:	48 8d 54 24 60                      	lea    0x60(%rsp),%rdx
 1d2:	48 89 de                            	mov    %rbx,%rsi
 1d5:	bf 00 00 00 00                      	mov    $0x0,%edi
			1d6: R_X86_64_32	.rodata.str1.1+0x106
 1da:	48 89 ac 24 b0 00 00 00             	mov    %rbp,0xb0(%rsp)
 1e2:	48 c7 44 24 60 01 00 00 00          	movq   $0x1,0x60(%rsp)
 1eb:	48 c7 44 24 68 00 00 00 00          	movq   $0x0,0x68(%rsp)
			1f0: R_X86_64_32S	.rodata.str1.1+0x4
 1f4:	48 c7 44 24 70 02 00 00 00          	movq   $0x2,0x70(%rsp)
 1fd:	48 c7 44 24 78 00 00 00 00          	movq   $0x0,0x78(%rsp)
			202: R_X86_64_32S	.rodata.str1.1+0xb
 206:	48 c7 84 24 80 00 00 00 04 00 00 00 	movq   $0x4,0x80(%rsp)
 212:	48 c7 84 24 88 00 00 00 00 00 00 00 	movq   $0x0,0x88(%rsp)
			21a: R_X86_64_32S	.rodata.str1.1+0x12
 21e:	48 c7 84 24 90 00 00 00 08 00 00 00 	movq   $0x8,0x90(%rsp)
 22a:	48 c7 84 24 98 00 00 00 00 00 00 00 	movq   $0x0,0x98(%rsp)
			232: R_X86_64_32S	.rodata.str1.1+0x19
 236:	48 c7 84 24 a0 00 00 00 10 00 00 00 	movq   $0x10,0xa0(%rsp)
 242:	48 c7 84 24 a8 00 00 00 00 00 00 00 	movq   $0x0,0xa8(%rsp)
			24a: R_X86_64_32S	.rodata.str1.1+0x20
 24e:	48 c7 84 24 b8 00 00 00 00 00 00 00 	movq   $0x0,0xb8(%rsp)
 25a:	e8 00 00 00 00                      	callq  25f <g2+0x11f>
			25b: R_X86_64_PC32	print_flags-0x4
 25f:	48 81 c4 c8 00 00 00                	add    $0xc8,%rsp
 266:	5b                                  	pop    %rbx
 267:	5d                                  	pop    %rbp
 268:	c3                                  	retq


---


### compiler : `gcc`
### title : `C frontend does not fold away trivial expressions that refer to const variables`
### open_at : `2015-12-07T12:40:32Z`
### last_modified_date : `2021-09-27T20:42:58Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=68764
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `c`
### version : `5.2.0`
### severity : `normal`
### contents :
In the following snippet, one would expect foo and bar to get folded to the same code, but that is not the case.

void dummy (const void *);

int
foo (void)
{
  const int x = 7;
  dummy (&x);
  return x + 0;
}

int
bar (void)
{
  const int x = 7;
  dummy (&x);
  return x;
}


While the C FE does fold "return x + 0;" to "return 7;", it does not fold "return x;" to "return 7;". And the load of x is the function bar() eventually survives all optimization passes and is present in the final optimized code:

bar ()
{
  const int x;
  int _4;

  <bb 2>:
  x = 7;
  dummy (&x);
  _4 = x;
  x ={v} {CLOBBER};
  return _4;

}

The C++ frontend is able to fully fold both return statements.


---


### compiler : `gcc`
### title : `PAREN_EXPR not "ignored" where possible`
### open_at : `2015-12-11T13:57:16Z`
### last_modified_date : `2023-05-15T06:39:08Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=68855
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `6.0`
### severity : `enhancement`
### contents :
In 465.tonto we end up with

  [shell2.fppized.f90:975:0] _967 = COMPLEX_EXPR <_178, _201>;
  [shell2.fppized.f90:975:0] _968 = ((_967));
  _3980 = REALPART_EXPR <_968>;

and _201/_967 otherwise unused.  REALPART_EXPR should look through
PAREN_EXPR here and wrap its simplification result in PAREN_EXPR
instead (or PAREN_EXPRs should be pushed into operands of non-associatable
stmts).

Not sure if one can devise other interesting examples.


---


### compiler : `gcc`
### title : `Recognition min/max pattern with multiple arguments.`
### open_at : `2015-12-14T12:34:18Z`
### last_modified_date : `2023-04-28T14:55:33Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=68894
### status : `RESOLVED`
### tags : `missed-optimization, TREE`
### component : `tree-optimization`
### version : `6.0`
### severity : `enhancement`
### contents :
Analyzing one important benchmark (rgb to cmyk conversion) we found out that MIN pattern is not recognized for more than 2 arguments. I attached simple reproducer which exhibit the issue - explicit use of multiple <IM macros leads to more effective binary for x86. I attached simple test-case for two sequential MIN but such recognition must be implemented for arbitrary number of comparisons.


---


### compiler : `gcc`
### title : `Null-pointer store not removed`
### open_at : `2015-12-15T14:40:14Z`
### last_modified_date : `2021-10-01T02:54:18Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=68919
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `6.0`
### severity : `normal`
### contents :
Consider test-case test.c (based on src/gcc/testsuite/c-c++-common/asan/null-deref-1.c):
...
__attribute__((noinline, noclone))
static void
NullDeref(int *ptr)
{
  ptr[10]++;
}

__attribute__((noinline, noclone))
static void
NullDeref2 (void)
{
  int *ptr = (int*)0;
  ptr[10]++;
}

int
main (void)
{
  NullDeref ((int*)0);
  NullDeref2 ();
  return 0;
}
...

Compile with:
...
$ gcc test.c -o test.exe -O2 -flto -flto-partition=none -fipa-pta
...

At test.exe.optimized, we see:
...
__attribute__((noclone, noinline))
NullDeref (int * ptr)
{
  <bb 2>:
  return;

}

__attribute__((noclone, noinline))
NullDeref2 ()
{
  int _2;
  int _3;

  <bb 2>:
  _2 = MEM[(int *)40B];
  _3 = _2 + 1;
  MEM[(int *)40B] = _3;
  return;

}

main ()
{
  <bb 2>:
  NullDeref2 ();
  return 0;

}
...

In the ipa-case, we removed the store to the NULL pointer. In the local case, we don't.

This seems to be a missing optimization in the local case.

When compiling with "-fno-tree-ccp -fno-tree-fre -fno-tree-forwprop" in addition, we see at ealias:
...
NullDeref2 ()
{
  intD.6 * ptrD.1761;
  intD.6 * _2;
  intD.6 _4;
  intD.6 _5;

  # PT = null
  ptr_1 = 0B;
  # PT = null
  _2 = ptr_1 + 40;
  # VUSE <.MEM_3(D)>
  _4 = *_2;
  _5 = _4 + 1;
  # .MEM_6 = VDEF <.MEM_3(D)>
  *_2 = _5;
  # VUSE <.MEM_6>
  return;
}
...

And subsequently at cddce1:
...
__attribute__((noclone, noinline))
NullDeref2 ()
{
  intD.6 * ptrD.1761;

  # VUSE <.MEM_3(D)>
  return;
}
...


---


### compiler : `gcc`
### title : `SSE/AVX movq load (_mm_cvtsi64_si128) not being folded into pmovzx`
### open_at : `2015-12-15T20:15:20Z`
### last_modified_date : `2019-01-18T19:05:36Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=68923
### status : `RESOLVED`
### tags : `missed-optimization, ssemmx`
### component : `target`
### version : `5.3.0`
### severity : `normal`
### contents :
context and background:
http://stackoverflow.com/questions/34279513/loading-8-chars-from-memory-into-an-m256-variable-as-packed-single-precision-f

Using intrinsics, I can't find a way to get gcc to emit

    VPMOVZXBD   (%rsi), %ymm0   ; 64b load
    VCVTDQ2PS   %ymm0,  %ymm0

without using _mm_loadu_si128, which will compile to an actual 128b load with -O0.  (not counting evil use of #ifndef __OPTIMIZE__ to do it two different ways, of course).


Since there is no intrinsic for PMOVSX / PMOVZX as a load from a narrower memory location, the only way I can see to correctly write this with intrinsics involves _mm_cvtsi64_si128 (MOVQ), which I don't even want the compiler to emit.  clang3.6 and ICC13 compile this to the optimal sequence, still folding the load into VPMOVZXBD, but gcc doesn't.


#include <immintrin.h>
#include <stdint.h>
#define USE_MOVQ
__m256 load_bytes_to_m256(uint8_t *p)
{
#ifdef  USE_MOVQ  // compiles to an actual movq then pmovzx xmm,xmm with gcc -O3
    __m128i small_load = _mm_cvtsi64_si128( *(uint64_t*)p );
#else  // loadu compiles to a 128b load with gcc -O0, potentially segfaulting
    __m128i small_load = _mm_loadu_si128( (__m128i*)p );
#endif

    __m256i intvec = _mm256_cvtepu8_epi32( small_load );
    return _mm256_cvtepi32_ps(intvec);
}



Problem 1: g++ -O3 -march=haswell emits (gcc 5.3.0 on godbolt)

load_bytes_to_m256(unsigned char*):
        vmovq   (%rdi), %xmm0
        vpmovzxbd       %xmm0, %ymm0
        vcvtdq2ps       %ymm0, %ymm0
        ret


Problem 2:
 gcc and clang don't even provide that movq intrinsic in 32bit mode.

(Split into a separate bug, since it's totally separate from the missing optimization issue).


---


### compiler : `gcc`
### title : `No intrinsic for x86  `MOVQ m64, %xmm`  in 32bit mode.`
### open_at : `2015-12-15T20:21:29Z`
### last_modified_date : `2019-03-10T23:05:40Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=68924
### status : `RESOLVED`
### tags : `missed-optimization, ssemmx`
### component : `target`
### version : `5.3.0`
### severity : `normal`
### contents :
context and background:
http://stackoverflow.com/questions/34279513/loading-8-chars-from-memory-into-an-m256-variable-as-packed-single-precision-f

https://gcc.gnu.org/bugzilla/show_bug.cgi?id=68923


gcc and clang don't even provide the _mm_cvtsi64_si128 intrinsic for movq in 32bit mode (ICC does, see below).  They still provide  m128i _mm_mov_epi64(__m128i a), but at -O0 the load of the source __m128i won't fold into the movq, so you'd get an undesired 128b load that could cross a page boundary and segfault.


The lack of this, and lack of an intrinsic for PMOVZX as a load from a narrower source, is a design flaw in the intrinsics, IMO.  I think it's super dumb to be forced to use an intrinsic for an instruction I don't want (movq), even if it didn't cause a portability issue for x86-32bit.


Consider trying to get gcc to emit `VPMOVZXBD  (%src), %ymm0` for 32bit mode:

#include <immintrin.h>
#include <stdint.h>
__m256 load_bytes_to_m256(uint8_t *p)
{
    __m128i small_load = _mm_cvtsi64_si128( *(uint64_t*)p );
    __m256i intvec = _mm256_cvtepu8_epi32( small_load );
    return _mm256_cvtepi32_ps(intvec);
}

That's the same code as in the other bug report (about the failure to fold the load into a memory source operand for vpmovzx: https://gcc.gnu.org/bugzilla/show_bug.cgi?id=68923 ), but with the #ifdefs taken out


--------


_mm_cvtsi64_si128 is the intrinsic for the MOVQ %r/m64, %xmm form of MOVQ.  (This is the MOVD/MOVQ entry in Intel's manual).  Its non-VEX encoding includes a REX prefix, and even the VEX encoding of it is illegal in 32bit mode (prob. because it couldn't decide if the insn was legal or not until it checked the mod/rm byte to see if it encoded a 64b register source, instead of a 64b memory location).  Since the other MOVQ gives identical results, and has a shorter non-VEX encoding, there's no reason to bother with that complexity.

The other MOVQ (the one Intel's insn ref lists under just MOVQ), which can be used for %mm,%mm reg moves, or the low half of %xmm,%xmm regs, only has a m128i to m128i intrinsic:  m128i _mm_mov_epi64(__m128i a), not a load form (same problem as the pmovz/sx intrinsics).



------------

Other than this design-flaw in the intrinsics, you could see it as only a bug in gcc/clang's implementation, since Intel's own implementation does still make it possible to get MOVQ m64, %xmm emitted in 32bit mode.


ICC13 still provides _mm_cvtsi64_si128 in 32bit mode, and will use the MOVQ xmm, m64 form as a load.  If it has a uint64_t in two 32bit registers, it emulates it with 2xMOVD %r32, %xmm and a PUNPCKLDQ.  http://goo.gl/LQkVJL.  Two 32b stores then a movq load would cause a store-forwarding failure stall.    vmovd/vpinsrd would be fewer instructions, but pinsrd is a 2-uop instruction on Intel SnB-family CPUs, so as far as uops they're equal: 3 uops for the shuffle port (port5).

At -O0, ICC emulates it that way even if the value is in memory, with 2x MOVD m32, %xmm and a PUNPCK, so even Intel's compiler "thinks of" the intrinsic as normally being the MOVQ %r/m64, %xmm form, not the MOVQ %xmm/m64, %xmm form.


---


### compiler : `gcc`
### title : `gcc emits unneeded memory access when passing trivial structs by value (ARM)`
### open_at : `2015-12-21T23:08:50Z`
### last_modified_date : `2021-08-16T00:57:33Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=69008
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `5.2.1`
### severity : `enhancement`
### contents :
gcc is emitting unneeded memory accesses in this code snippet.
Trivial structs up to 16 bytes are passed in r0-r3, no need for stack.

struct Trivial {
    int i1;
    int i2;
};

int foo(Trivial t)
{
    return t.i1 + t.i2;
}

gcc on armv7:
$ g++ arm.cpp -O2 -mabi=aapcs -c -S && cat arm.s
  sub     sp, sp, #8
  add     r3, sp, #8
  stmdb   r3, {r0, r1}
  ldmia   sp, {r0, r3}
  add     r0, r0, r3
  add     sp, sp, #8
  bx      lr

clang:
$ clang++ arm.cpp -O2 -mabi=aapcs -c -S && cat arm.s

add r0, r0, r1
bx  lr


---


### compiler : `gcc`
### title : `memcpy is not as optimized as union is`
### open_at : `2015-12-24T21:21:11Z`
### last_modified_date : `2020-01-06T04:09:59Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=69047
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `5.3.0`
### severity : `enhancement`
### contents :
Created attachment 37131
d.c

When a function does memcpy to a local integer and returns it, pointless stack operations are done (subtraction, and addition just after that).

Command line
============

arm-none-eabi-gcc -O3 -S -o- d.c

Output
======

Assembly code containing following function.

f:
        @ Function supports interworking.
        @ args = 0, pretend = 0, frame = 8
        @ frame_needed = 0, uses_anonymous_args = 0
        @ link register save eliminated.
        sub     sp, sp, #8
        add     sp, sp, #8
        @ sp needed
        bx      lr
        .size   f, .-f

Version information
===================

Using built-in specs.
COLLECT_GCC=arm-none-eabi-gcc
COLLECT_LTO_WRAPPER=/usr/lib/gcc/arm-none-eabi/5.3.0/lto-wrapper
Target: arm-none-eabi
Configured with: /build/arm-none-eabi-gcc/src/gcc-5.3.0/configure --target=arm-none-eabi --prefix=/usr --with-sysroot=/usr/arm-none-eabi --with-native-system-header-dir=/include --libexecdir=/usr/lib --enable-languages=c,c++ --enable-plugins --disable-decimal-float --disable-libffi --disable-libgomp --disable-libmudflap --disable-libquadmath --disable-libssp --disable-libstdcxx-pch --disable-nls --disable-shared --disable-threads --disable-tls --with-gnu-as --with-gnu-ld --with-system-zlib --with-newlib --with-headers=/usr/arm-none-eabi/include --with-python-dir=share/gcc-arm-none-eabi --with-gmp --with-mpfr --with-mpc --with-isl --with-libelf --enable-gnu-indirect-function --with-host-libstdcxx='-static-libgcc -Wl,-Bstatic,-lstdc++,-Bdynamic -lm' --with-pkgversion='Arch Repository' --with-bugurl=https://bugs.archlinux.org/ --with-multilib-list=armv6-m,armv7-m,armv7e-m,armv7-r
Thread model: single
gcc version 5.3.0 (Arch Repository)


---


### compiler : `gcc`
### title : `explicit atomic ops treating non-constant memory orders as memory_order_seq_cst`
### open_at : `2016-01-03T22:18:34Z`
### last_modified_date : `2021-09-19T23:49:45Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=69130
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `6.0`
### severity : `enhancement`
### contents :
I hesitated before raising this issue since what GCC does isn't strictly speaking incorrect. But after thinking about it for a bit I convinced myself it is a bug (or at least an opportunity for an improvement).

GCC seems to treat invocations of the atomic_xxx_explicit() intrinsics with a memory order argument that's not a constant expression as if they were to the sequentially consistent atomic_xxx() built-ins.  This shouldn't be a problem for the correctness of the code, but it does mean that the code will be less efficient than it could be.  The test case below illustrates a couple of basic instances of the problem.

In contrast, while its code could stand to be improved, Clang checks the memory order and emits a fence only in the branch that requires it.

$ cat z.c && /build/gcc-trunk/gcc/xgcc -B /build/gcc-trunk/gcc -O2 -S -Wall -Wextra -Wpedantic -o/dev/stdout z.c
#include <stdatomic.h>

void store_explicit (_Atomic int *i, memory_order mo)
{
    atomic_store_explicit (i, 0, mo);
}

void store (_Atomic int *i, _Bool relax)
{
    memory_order mo = relax ? memory_order_relaxed : memory_order_seq_cst;

    atomic_store_explicit (i, 0, mo);
}
	.file	"z.c"
	.machine power8
	.abiversion 2
	.section	".toc","aw"
	.section	".text"
	.align 2
	.p2align 4,,15
	.globl store_explicit
	.type	store_explicit, @function
store_explicit:
	sync
	li 9,0
	stw 9,0(3)
	blr
	.long 0
	.byte 0,0,0,0,0,0,0,0
	.size	store_explicit,.-store_explicit
	.align 2
	.p2align 4,,15
	.globl store
	.type	store, @function
store:
	sync
	li 9,0
	stw 9,0(3)
	blr
	.long 0
	.byte 0,0,0,0,0,0,0,0
	.size	store,.-store
	.ident	"GCC: (GNU) 6.0.0 20151217 (experimental)"
	.section	.note.GNU-stack,"",@progbits


---


### compiler : `gcc`
### title : `PowerPC64: aggregate results are badly handled`
### open_at : `2016-01-05T05:21:59Z`
### last_modified_date : `2022-03-08T16:20:54Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=69143
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `6.0`
### severity : `enhancement`
### contents :
This testcase:

struct foo1 {
        float x;
        float y;
};

struct foo1 blah1(struct foo1 y)
{
        struct foo1 x;

        x.x = y.y;
        x.y = y.x;

        return x;
}

Compiled with:

gcc -fno-stack-protector -mcpu=power8 -O2

Results in the following code:

blah1:
	xscvdpspn 12,2
	stfs 1,-16(1)
	ori 2,2,0
	lwz 8,-16(1)
	mfvsrd 10,12
	mr 9,8
	rldicl 9,9,0,32
	srdi 10,10,32
	sldi 10,10,32
	or 9,9,10
	rotldi 9,9,32
	mr 10,9
	srdi 9,9,32
	sldi 8,10,32
	sldi 10,9,32
	mtvsrd 1,8
	mtvsrd 2,10
	xscvspdpn 1,1
	xscvspdpn 2,2
	blr


I was expecting a couple of FPR moves. Clang does what I expected:

blah1:
	fmr 0, 1
	fmr 1, 2
	fmr 2, 0
	blr


---


### compiler : `gcc`
### title : `code size regression with jump threading at -O2`
### open_at : `2016-01-08T12:34:03Z`
### last_modified_date : `2022-01-09T00:58:48Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=69196
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `6.0`
### severity : `normal`
### contents :
Created attachment 37274
Test case.

This is quite an increase of the code size for the attached test case.

sparc-rtems4.11-gcc (GCC) 4.9.4 20150723 (prerelease)
sparc-rtems4.12-gcc (GCC) 6.0.0 20160108 (experimental)
sparc-rtems4.11-gcc -c -O2 -o vprintk.4.11.o vprintk.i
sparc-rtems4.12-gcc -c -O2 -o vprintk.4.12.o vprintk.i
size vprintk.4.11.o
   text    data     bss     dec     hex filename
    688       0       0     688     2b0 vprintk.4.11.o
size vprintk.4.12.o
   text    data     bss     dec     hex filename
   1272       0       0    1272     4f8 vprintk.4.12.o

I noticed a size increase for various files, but this one was quite drastic.


---


### compiler : `gcc`
### title : `Compiling without --profile-generate causes longer execution time (-O3)`
### open_at : `2016-01-15T01:19:42Z`
### last_modified_date : `2021-12-11T06:06:33Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=69289
### status : `NEW`
### tags : `missed-optimization, needs-bisection`
### component : `tree-optimization`
### version : `5.3.0`
### severity : `normal`
### contents :
Created attachment 37349
Source

Running without --profile-generate (NOT --profile-use) causes a slowdown.

The speed script that I run simply runs the program with time output.

Effect is still present when using/not using -march=native and when using/not using -funroll-loops

speed.sh
  1 #!/bin/zsh
  2 
  3 sudo cpupower frequency-set -g performance
  4 
  5 time ./a.out 1
  6 time ./a.out 2
  7 time ./a.out 3
  8 time ./a.out 4
  9 time ./a.out 5
 10 time ./a.out 1
 11 time ./a.out 2
 12 time ./a.out 3
 13 time ./a.out 4
 14 time ./a.out 5
 15 
 16 sudo cpupower frequency-set -g powersave

% g++ --version    
g++ (GCC) 5.3.0
Copyright (C) 2015 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

% cat /proc/version 
Linux version 4.3.3-2-ARCH (builduser@tobias) (gcc version 5.3.0 (GCC) ) #1 SMP PREEMPT Wed Dec 23 20:09:18 CET 2015

%g++ test.cpp -std=c++11 -O3 -funroll-loops -march=native --profile-generate -Wall -Wextra
test.cpp:37:14: warning: unused parameter ‘argc’ [-Wunused-parameter]
 int main(int argc, char** argv)

% ./speed.sh 
[sudo] password for XXXXXXX: 
Setting cpu: 0
Setting cpu: 1
Setting cpu: 2
Setting cpu: 3
Setting cpu: 4
Setting cpu: 5
Setting cpu: 6
Setting cpu: 7
166
./a.out 1  0.32s user 0.55s system 99% cpu 0.875 total
166
./a.out 2  0.33s user 0.54s system 100% cpu 0.870 total
166
./a.out 3  0.33s user 0.54s system 100% cpu 0.870 total
166
./a.out 4  0.33s user 0.55s system 99% cpu 0.874 total
166
./a.out 5  0.35s user 0.52s system 99% cpu 0.870 total
166
./a.out 1  0.32s user 0.55s system 99% cpu 0.867 total
166
./a.out 2  0.35s user 0.52s system 99% cpu 0.872 total
166
./a.out 3  0.32s user 0.56s system 99% cpu 0.889 total
166
./a.out 4  0.33s user 0.53s system 99% cpu 0.868 total
166
./a.out 5  0.32s user 0.55s system 100% cpu 0.873 total
Setting cpu: 0
Setting cpu: 1
Setting cpu: 2
Setting cpu: 3
Setting cpu: 4
Setting cpu: 5
Setting cpu: 6
Setting cpu: 7
./speed.sh  3.34s user 5.42s system 79% cpu 10.947 total

% g++ test.cpp -std=c++11 -O3 -funroll-loops -march=native -Wall -Wextra    
test.cpp:37:14: warning: unused parameter ‘argc’ [-Wunused-parameter]
 int main(int argc, char** argv)

% ./speed.sh
Setting cpu: 0
Setting cpu: 1
Setting cpu: 2
Setting cpu: 3
Setting cpu: 4
Setting cpu: 5
Setting cpu: 6
Setting cpu: 7
166
./a.out 1  0.43s user 0.56s system 100% cpu 0.990 total
166
./a.out 2  0.42s user 0.57s system 99% cpu 0.983 total
166
./a.out 3  0.41s user 0.58s system 99% cpu 0.997 total
166
./a.out 4  0.47s user 0.54s system 99% cpu 1.005 total
166
./a.out 5  0.43s user 0.56s system 99% cpu 0.988 total
166
./a.out 1  0.45s user 0.54s system 99% cpu 0.991 total
166
./a.out 2  0.42s user 0.55s system 99% cpu 0.971 total
166
./a.out 3  0.39s user 0.59s system 99% cpu 0.982 total
166
./a.out 4  0.46s user 0.52s system 99% cpu 0.985 total
166
./a.out 5  0.48s user 0.51s system 99% cpu 0.985 total
Setting cpu: 0
Setting cpu: 1
Setting cpu: 2
Setting cpu: 3
Setting cpu: 4
Setting cpu: 5
Setting cpu: 6
Setting cpu: 7
./speed.sh  4.36s user 5.53s system 99% cpu 9.909 total


---


### compiler : `gcc`
### title : `missing -Wreturn-local-addr assigning address of a local to a static`
### open_at : `2016-01-22T18:19:43Z`
### last_modified_date : `2020-05-20T22:07:42Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=69433
### status : `NEW`
### tags : `diagnostic, missed-optimization`
### component : `c++`
### version : `6.0`
### severity : `enhancement`
### contents :
Gcc issues the helpful -Wreturn-local-addr warning for the first two functions in the test case below but not for for the second two.  It would be useful if the same or similar warning (say something like -Wleak-local-addr) were issued there as well.  (Note that Clang only diagnoses f0.)

$ cat z.cpp && ~/bin/gcc-5.1.0/bin/g++ -O2 -S -Wall -Wextra -Wpedantic -o/dev/null z.cpp
const char* f0 () {
    const char a[] = "abc";
    return a;
}

const char* f1 (int i) {
    const char a[] = "abc";
    const char *q = i ? a : "def";
    return q;
}

const char* f2 () {
    const char a[] = "abc";
    static const char *s = a;
    return s;
}

static const char *s;

void f3 () {
    const char a[] = "abc";
    s = a;
}
z.cpp: In function ‘const char* f0()’:
z.cpp:2:16: warning: address of local variable ‘a’ returned [-Wreturn-local-addr]
     const char a[] = "abc";
                ^
z.cpp: In function ‘const char* f1(int)’:
z.cpp:9:12: warning: function may return address of local variable [-Wreturn-local-addr]
     return q;
            ^
z.cpp:7:16: note: declared here
     const char a[] = "abc";
                ^


---


### compiler : `gcc`
### title : `Fail to devirtualize call to base class function even though derived class type is 'final'`
### open_at : `2016-01-23T17:03:11Z`
### last_modified_date : `2022-05-13T17:40:47Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=69445
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `6.0`
### severity : `enhancement`
### contents :
G++ should devirtualize both calls in func(const C&):

struct Base {
  virtual void foo() const = 0;
  virtual void bar() const {}
};

struct C final : Base {
  void foo() const { }
};

void func(const C & c) {
  c.bar();
  c.foo();
}

We take advantage of the fact that C is final and so C::foo() can't be overriden, but don't apply the same logic to Base::bar().

With -O3 Clang optimises func to an empty function but with G++ the x86_64 code is:

Base::bar() const:
        rep ret
func(C const&):
        movq    (%rdi), %rax
        movq    8(%rax), %rax
        cmpq    Base::bar() const, %rax
        jne     .L5
        rep ret
.L5:
        jmp     *%rax


---


### compiler : `gcc`
### title : `missed vectorization for boolean loop, missed if-conversion`
### open_at : `2016-01-26T14:24:28Z`
### last_modified_date : `2023-08-24T07:13:55Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=69489
### status : `NEW`
### tags : `missed-optimization, needs-bisection`
### component : `tree-optimization`
### version : `5.2.1`
### severity : `enhancement`
### contents :
following (abbreviated) code does not vectorize with gcc 5.2.1:

gcc file.c -O2 -ftree-vectorize -c

double
yule_bool_distance_char2(const char *u, const char *v, long n)
{
    long i;
    long ntt = 0, nff = 0, nft = 0, ntf = 0;

    for (i = 0; i < n; i++) {
        ntf += (u[i] && !v[i]);
        nft += (!u[i] && v[i]);
    }   
    return (2.0 * ntf * nft);
} 

but if one replaces the loop body with this:

        char x = u[i], y = v[i];
        ntf += x && (!y);
        nft += (!x) && y;

gcc will vectorize it.
As I understand it both code is equivalent, so it would be great if gcc could vectorize both variants.


---


### compiler : `gcc`
### title : `Poor code generation for return of struct containing vectors on PPC64LE`
### open_at : `2016-01-26T16:32:43Z`
### last_modified_date : `2022-03-08T16:21:03Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=69493
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `6.0`
### severity : `normal`
### contents :
For this simple test using the ELFv2 ABI, we generate code that correctly returns the structures in v2 and v3 (vs34 and vs35).  However, there is an unnecessary store and reload of the vectors prior to the return, which will perform extremely poorly on POWER processors.

 typedef struct
 {
   __vector double vx0;
   __vector double vx1;
 } vdoublex4_t;

  vdoublex4_t
  test_big_double (long double a, long double b)
  {
    vdoublex4_t result;
    /* return a 0.0 */
    result.vx0[0] = __builtin_unpack_longdouble (a, 0);
    result.vx0[1] = __builtin_unpack_longdouble (a, 1);
    result.vx1[0] = __builtin_unpack_longdouble (b, 0);
    result.vx1[1] = __builtin_unpack_longdouble (b, 1);

    return (result);
  }

$ gcc -S -O2 poor.c

poor.s:
        .file   "poor.c"
        .abiversion 2
        .section        ".toc","aw"
        .section        ".text"
        .align 2
        .p2align 4,,15
        .globl test_big_double
        .type   test_big_double, @function
test_big_double:
        fmr 10,1
        fmr 11,3
        addi 8,1,-96
        li 10,32
        xxlxor 12,12,12
        li 9,48
        xxlor 0,12,12
        xxpermdi 12,12,10,0
        xxpermdi 0,0,11,0
        xxpermdi 12,2,12,1
        xxpermdi 0,4,0,1
        xxpermdi 12,12,12,2
        xxpermdi 0,0,0,2
        stxvd2x 12,8,10
        stxvd2x 0,8,9
        lxvd2x 34,8,10
        lxvd2x 35,8,9
        xxpermdi 34,34,34,2
        xxpermdi 35,35,35,2
        blr
        .long 0
        .byte 0,0,0,0,0,0,0,0
        .size   test_big_double,.-test_big_double
        .ident  "GCC: (GNU) 6.0.0 20160125 (experimental) [trunk revision 232783]"
        .section        .note.GNU-stack,"",@progbits


---


### compiler : `gcc`
### title : `STV doesn't use xmm register for DImove move`
### open_at : `2016-01-27T20:46:12Z`
### last_modified_date : `2021-08-07T01:58:43Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=69519
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `6.0`
### severity : `enhancement`
### contents :
[hjl@gnu-6 gcc]$ cat x.i
long long a, b;
extern void fn2 (void);
void
fn1 (void)
{
  long long c = a;
  a = b ^ a;
  fn2 ();
  a = c;
}
[hjl@gnu-6 gcc]$ ./xgcc -B./ -S -O2 x.i -m32  -msse2
[hjl@gnu-6 gcc]$ cat x.s
	.file	"x.i"
	.text
	.p2align 4,,15
	.globl	fn1
	.type	fn1, @function
fn1:
.LFB0:
	.cfi_startproc
	subl	$28, %esp
	.cfi_def_cfa_offset 32
	movl	a, %eax
	movl	a+4, %edx
	movq	b, %xmm0
	movl	%eax, (%esp)
	movl	%edx, 4(%esp)
	movdqa	(%esp), %xmm2

I am expecting xmm register is used to move `a' onto stack.

	pxor	%xmm2, %xmm0
	movq	%xmm0, a
	call	fn2
	movq	(%esp), %xmm1
	movq	%xmm1, a
	addl	$28, %esp
	.cfi_def_cfa_offset 4
	ret
	.cfi_endproc
.LFE0:
	.size	fn1, .-fn1
	.comm	b,8,8
	.comm	a,8,8
	.ident	"GCC: (GNU) 6.0.0 20160126 (experimental)"
	.section	.note.GNU-stack,"",@progbits
[hjl@gnu-6 gcc]$


---


### compiler : `gcc`
### title : `ivopts candidate strangeness`
### open_at : `2016-01-28T08:52:51Z`
### last_modified_date : `2021-12-22T08:44:43Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=69526
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `6.0`
### severity : `minor`
### contents :
While inspecting loop generation code on s390, I saw ivopts choose an IV candidate which does something peculiar. On x86 the same candidate is never chosen because of different cost estimations, yet the behavior can be evoked on x86, through "forcing" GCC to use the same candidate as on s390. I did this to confirm my suspicions and I'll show the x86 version here:

This source

void v(unsigned long *in, unsigned long *out, unsigned int n)
{
  int i;

  for (i = 0; i < n; i++)
  {
    out[i] = in[i];
  }
}

results in the following assembly, when ivopts candidate 7 is used:

v:
  testl %edx, %edx
  je .L1
  leal -1(%rdx), %eax
  leaq 8(,%rax,8), %rcx
  xorl %eax, %eax
.L3:
  movq (%rdi,%rax), %rdx
  movq %rdx, (%rsi,%rax)
  addq $8, %rax
  cmpq %rcx, %rax
  jne .L3
.L1:
  rep ret

Should the following be happening?

  leal -1(%rdx), %eax
  leaq 8(,%rax,8), %rcx

i.e. %eax = n - 1
     %rcx = 8 * (n + 1)

The pattern can already be observed in ivopts' GIMPLE:

<bb 4>:
_15 = n_5(D) + 4294967295;
_2 = (sizetype) _15;
_1 = _2 + 1;
_24 = _1 * 8;

Why do we need the - 1 and subsequent + 1 when the %eax is zeroed afterwards anyway? Granted, this exact situation won't ever be observed on x86 as another ivopts candidate is chosen but on s390 this situation will amount to three instructions.

If I see it correctly, the n - 1 comes from estimating the number of loop iterations, while the +1 is then correctly added by cand_value_at() because the loop counter is incremented before the exit test. Perhaps this is intended behavior and there is nothing wrong with it?

Regards
 Robin


---


### compiler : `gcc`
### title : `[ARM] revsh instruction not being conditionalised for Thumb2`
### open_at : `2016-01-29T15:29:00Z`
### last_modified_date : `2021-12-19T00:56:08Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=69557
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `6.0`
### severity : `enhancement`
### contents :
While doing some of the testcase splitting work for PR 65578
I saw that we don't use conditional execution as much as we should for Thumb2.

The testcase:

extern short foos16 (short);
/* revshne */
short swaps16_cond (short x, int y)
{
  short z = x;
  if (y)
    z = __builtin_bswap16 (x);
  return foos16 (z);
}

for -march=armv6t2 -mthumb -O2 I get:
swaps16_cond:
        @ args = 0, pretend = 0, frame = 0
        @ frame_needed = 0, uses_anonymous_args = 0
        @ link register save eliminated.
        cbz     r1, .L2
        revsh   r0, r0
.L2:
        b

whereas for -march=armv6t2 -mthumb -O2 we get conditional execution:
swaps16_cond:
        @ args = 0, pretend = 0, frame = 0
        @ frame_needed = 0, uses_anonymous_args = 0
        @ link register save eliminated.
        cmp     r1, #0
        revshne r0, r0
.L2:
        b

Note that the -marm version gets conditionalised at the very end in arm_final_prescan_insn which we don't perform for Thumb2.

The ce3 pass doesn't create the COND_EXEC forms like I'd expect.
For the testcase above it refuses to perform any transformations in cond_exec_find_if_block (from ifcvt.c) where it fails the check:

  /* The edges of the THEN and ELSE blocks cannot have complex edges.  */
  FOR_EACH_EDGE (cur_edge, ei, then_bb->preds)
    {
      if (cur_edge->flags & EDGE_COMPLEX)
	return FALSE;
    }

Seems the edge is deemed complex so ifconversion bails out.


---


### compiler : `gcc`
### title : `[11/12/13/14 Regression] lto and/or C++ make scimark2 LU slower`
### open_at : `2016-01-30T10:50:39Z`
### last_modified_date : `2023-07-07T10:31:03Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=69564
### status : `NEW`
### tags : `lto, missed-optimization`
### component : `c++`
### version : `6.0`
### severity : `normal`
### contents :
mkdir scimark2; cd scimark2
wget http://math.nist.gov/scimark2/scimark2_1c.zip
unzip scimark2_1c.zip
c++ -Ofast *.c; ./a.out
c++ -Ofast *.c -flto; ./a.out


with gcc 4.9.3
gcc version 4.9.3 (GCC) 

c++ -Ofast *.c; ./a.out
**                                                              **
** SciMark2 Numeric Benchmark, see http://math.nist.gov/scimark **
** for details. (Results can be submitted to pozo@nist.gov)     **
**                                                              **
Using       2.00 seconds min time per kenel.
Composite Score:         2462.90
FFT             Mflops:  2070.32    (N=1024)
SOR             Mflops:  1661.17    (100 x 100)
MonteCarlo:     Mflops:   813.44
Sparse matmult  Mflops:  2978.91    (N=1000, nz=5000)
LU              Mflops:  4790.64    (M=100, N=100)
[innocent@vinavx3 scimark2]$ c++ -Ofast *.c -flto; ./a.out
**                                                              **
** SciMark2 Numeric Benchmark, see http://math.nist.gov/scimark **
** for details. (Results can be submitted to pozo@nist.gov)     **
**                                                              **
Using       2.00 seconds min time per kenel.
Composite Score:         2582.94
FFT             Mflops:  2064.19    (N=1024)
SOR             Mflops:  1654.04    (100 x 100)
MonteCarlo:     Mflops:  1426.90
Sparse matmult  Mflops:  2978.91    (N=1000, nz=5000)
LU              Mflops:  4790.64    (M=100, N=100)


with latest build
gcc version 6.0.0 20160129 (experimental) (GCC) 

[innocent@vinavx3 scimark2]$ c++ -Ofast *.c; ./a.out
**                                                              **
** SciMark2 Numeric Benchmark, see http://math.nist.gov/scimark **
** for details. (Results can be submitted to pozo@nist.gov)     **
**                                                              **
Using       2.00 seconds min time per kenel.
Composite Score:         2377.18
FFT             Mflops:  1970.89    (N=1024)
SOR             Mflops:  1654.04    (100 x 100)
MonteCarlo:     Mflops:   810.37
Sparse matmult  Mflops:  3328.81    (N=1000, nz=5000)
LU              Mflops:  4121.76    (M=100, N=100)
[innocent@vinavx3 scimark2]$ c++ -Ofast *.c -flto; ./a.out
**                                                              **
** SciMark2 Numeric Benchmark, see http://math.nist.gov/scimark **
** for details. (Results can be submitted to pozo@nist.gov)     **
**                                                              **
Using       2.00 seconds min time per kenel.
Composite Score:         2136.23
FFT             Mflops:  2076.48    (N=1024)
SOR             Mflops:  1654.04    (100 x 100)
MonteCarlo:     Mflops:  1533.92
Sparse matmult  Mflops:  3266.59    (N=1000, nz=5000)
LU              Mflops:  2150.13    (M=100, N=100)


---


### compiler : `gcc`
### title : `0 to limit signed range checks don't always use unsigned compare`
### open_at : `2016-02-02T07:30:41Z`
### last_modified_date : `2018-11-19T14:14:12Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=69615
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `5.3.0`
### severity : `normal`
### contents :
gcc sometimes misses the unsigned-compare trick for checking if a signed value is between 0 and limit (where limit is known to be <= INT_MAX).

It seems that gcc fails when the upper limit is a variable, even if I shift or mask it down to a small range.  clang handles this case, so I'm sure I constructed my test case in a way that could be optimized.



All the code in this bug report is on godbolt, for ease of trying with older versions of gcc (including for ARM64/ARM/PPC), and with clang / icc13.  http://goo.gl/V7PFmv.   (I used -x c to compile as C, even though it only provides c++ compilers).

This appears to be arch-independent (unless my quick skim of asm for ISAs I barely know misled me...)

--------

The simplest case is when the upper limit is a compile-time constant.  There's one case where gcc and clang fail to optimize:  x<=(INT_MAX-1), or equivalently, x<INT_MAX.


#include <limits.h>
#include <stdint.h>
extern void ext(void);

// clang and gcc both optimize range checks up to INT_MAX-2 to a single unsigned compare
void r0_to_imax_2(int x){ if (x>=0 && x<=(INT_MAX-2)) ext(); }  // good code
void r0_to_imax_1(int x){ if (x>=0 && x<=(INT_MAX-1)) ext(); }  // bad code
void r0_to_imax  (int x){ if (x>=0 && x<=(INT_MAX-0)) ext(); }  // good code (test/js.  not shown)

gcc 5.3.0 -Ofast -mtune=haswell  compiles this to:

r0_to_imax_2:
        cmpl    $2147483645, %edi   # that's 0x7ffffffd
        jbe     .L4
        ret
.L4:    jmp     ext

r0_to_imax_1:
        movl    %edi, %eax
        subl    $0, %eax       ## Without any -mtune, uses test edi,edi
        js      .L5
        cmpl    $2147483647, %edi   # that's 0x7fffffff
        je      .L5
        jmp     ext
.L5:    ret

ICC13 compiles this last one to cmp  edi, 0x7ffffffe / ja, so unless my mental logic is wrong *and* icc13 is buggy, gcc and clang should still be able to  use the same optimization as for smaller upper-limits.  They don't: both clang and gcc use two compare-and-branches for r0_to_imax_1.

BTW, the movl %edi, %eax / subl $0, %eax sequence is used instead of the test instruction with -mtune=haswell, and even worse with -march=bdver2 where it even prevents fusion into a compare-and-branch m-op.  I'll file a separate bug report for that if anyone wants me to.  Agner Fog's microarch guide doesn't mention anything that would give that sequence an advantage over test, unless I'm missing something.  It slows AMD down more than (recent) Intel, but that's not what tuning for Haswell means. :P



Now, on to the case where the limit is variable, but can easily be proven to itself be in the range [0 .. INT_MAX-1) or much smaller.  (If the limit can be negative (or unsigned greater than INT_MAX) the optimization is impossible:  INT_MIN and other negative numbers could be "below" the limit.)


// gcc always fails to optimize this to an unsigned compare, but clang succeeds
void rangecheck_var(int64_t x, int64_t lim2) {
  //lim2 >>= 60;
  lim2 &= 0xf;  // let the compiler figure out the limited range of limit
  if (x>=0 && x<lim2) ext();
}

compiles to (with -O3, and -mtune=core2 to avoid the sub $0 sillyness):

rangecheck_var:
        andl    $15, %esi
        cmpq    %rdi, %rsi
        jle     .L16
        testq   %rdi, %rdi
        js      .L16
        jmp     ext
.L16:   ret


---


### compiler : `gcc`
### title : `[11/12/13/14 Regression] Redundant move is generated after r228097`
### open_at : `2016-02-02T16:44:51Z`
### last_modified_date : `2023-07-07T10:31:08Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=69633
### status : `ASSIGNED`
### tags : `missed-optimization, ra`
### component : `rtl-optimization`
### version : `6.0`
### severity : `normal`
### contents :
Sorry, that we noticed this regression just now but not in September.
After Makarov's fix for 61578 ( and s390 regression) we noticed that for attached simple test-case extracted from real benchmark one more redundant move instruction is generated (till 20160202 compiler build):

before fix (postreload dump)
   86: NOTE_INSN_BASIC_BLOCK 4
   40: dx:QI=[si:SI]
   41: ax:QI=[si:SI+0x1]
   42: {si:SI=si:SI+0x3;clobber flags:CC;}
   43: dx:SI=zero_extend(dx:QI)
   44: ax:SI=zero_extend(ax:QI)
   45: cx:SI=zero_extend([si:SI-0x1])
   46: {di:SI=dx:SI*0x4c8b;clobber flags:CC;}
   47: {bx:SI=ax:SI*0x9646;clobber flags:CC;}
   48: {bx:SI=bx:SI+di:SI;clobber flags:CC;}
   49: {di:SI=cx:SI*0x1d2f;clobber flags:CC;}
   50: NOTE_INSN_DELETED
   51: bx:SI=bx:SI+di:SI+0x8000
   52: {bx:SI=bx:SI>>0x10;clobber flags:CC;}
   53: [bp:SI]=bx:QI
   96: bx:SI=dx:SI
   55: {bx:SI=bx:SI<<0xf;clobber flags:CC;}
   57: {bx:SI=bx:SI-dx:SI;clobber flags:CC;}

after fix
   86: NOTE_INSN_BASIC_BLOCK 4
   40: dx:QI=[si:SI]
   41: ax:QI=[si:SI+0x1]
   42: {si:SI=si:SI+0x3;clobber flags:CC;}
   43: dx:SI=zero_extend(dx:QI)
   44: ax:SI=zero_extend(ax:QI)
   45: cx:SI=zero_extend([si:SI-0x1])
   46: {di:SI=dx:SI*0x4c8b;clobber flags:CC;}
   47: {bx:SI=ax:SI*0x9646;clobber flags:CC;}
   48: {bx:SI=bx:SI+di:SI;clobber flags:CC;}
   49: {di:SI=cx:SI*0x1d2f;clobber flags:CC;}
   50: NOTE_INSN_DELETED
   51: bx:SI=bx:SI+di:SI+0x8000
   52: {bx:SI=bx:SI>>0x10;clobber flags:CC;}
   53: [bp:SI]=bx:QI
   96: bx:SI=dx:SI
   55: {bx:SI=bx:SI<<0xf;clobber flags:CC;}
   98: di:SI=bx:SI                           !! redundnat move
   57: {di:SI=di:SI-dx:SI;clobber flags:CC;}

In result, we got >3% slowdown on Silvermont in pie & 32-bit mode.


---


### compiler : `gcc`
### title : `gcc.target/i386/addr-sel-1.c FAILs with PR69274 fix`
### open_at : `2016-02-05T12:09:51Z`
### last_modified_date : `2021-09-14T05:39:13Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=69689
### status : `RESOLVED`
### tags : `missed-optimization, ra, xfail`
### component : `rtl-optimization`
### version : `6.0`
### severity : `normal`
### contents :
With

Index: gcc/ira.c
===================================================================
--- gcc/ira.c   (revision 231814)
+++ gcc/ira.c   (working copy)
@@ -1888,10 +1888,11 @@ ira_setup_alts (rtx_insn *insn, HARD_REG
        }
       if (commutative < 0)
        break;
-      if (curr_swapped)
-       break;
+      /* Swap forth and back to avoid changing recog_data.  */
       std::swap (recog_data.operand[commutative],
                 recog_data.operand[commutative + 1]);
+      if (curr_swapped)
+       break;
     }
 }

I see

FAIL: gcc.target/i386/addr-sel-1.c scan-assembler b\\\\+1

where we fail to reload_combine

(insn 6 21 8 2 (parallel [
            (set (reg:SI 1 dx [orig:87 _2 ] [87])
                (plus:SI (reg:SI 0 ax [99])
                    (const_int 1 [0x1])))
            (clobber (reg:CC 17 flags))
        ]) /space/rguenther/src/svn/trunk3/gcc/testsuite/gcc.target/i386/addr-sel-1.c:13 218 {*addsi_1}
     (nil))
...
(insn 10 8 11 2 (set (reg:SI 1 dx [98])
        (sign_extend:SI (mem/j:QI (plus:SI (reg:SI 1 dx [orig:87 _2 ] [87])
                    (symbol_ref:SI ("b") [flags 0x2]  <var_decl 0x7faa46f94d80 b>)) [0 b S1 A8]))) /space/rguenther/src/svn/trunk3/gcc/testsuite/gcc.target/i386/addr-sel-1.c:13 151 {extendqisi2}
     (nil))

probably because dx dies in the same instruction it is used in.


---


### compiler : `gcc`
### title : `[11/12/13/14 Regression] excessive stack usage with -fprofile-arcs, LIM store motion lacks a register pressure aware cost model`
### open_at : `2016-02-05T22:45:07Z`
### last_modified_date : `2023-07-07T10:31:12Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=69702
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `5.3.1`
### severity : `normal`
### contents :
Created attachment 37604
standalone test case extracted from Linux kernel

With gcc versions 4.9 or higher, the stack usage of some functions in the Linux kernel has grown to the point where we risk a stack overflow, with 8kb or 16kb of stack being available per thread.

When building an ARM kernel, I get at least these warnings in some configurations when using "gcc -fprofile-arcs -Wframe-larger-than=1024", and don't get them without -fprofile-arcs:

drivers/isdn/isdnhdlc.c:629:1: error: the frame size of 1152 bytes is larger than 1024 bytes 
drivers/media/common/saa7146/saa7146_hlp.c:464:1: error: the frame size of 1040 bytes is larger than 1024 bytes 
drivers/mtd/chips/cfi_cmdset_0020.c:651:1: error: the frame size of 1040 bytes is larger than 1024 bytes 
drivers/net/wireless/ath/ath6kl/main.c:495:1: error: the frame size of 1200 bytes is larger than 1024 bytes 
drivers/net/wireless/ath/ath9k/ar9003_aic.c:434:1: error: the frame size of 1208 bytes is larger than 1024 bytes 
drivers/video/fbdev/riva/riva_hw.c:426:1: error: the frame size of 1248 bytes is larger than 1024 bytes 
lib/lz4/lz4hc_compress.c:514:1: error: the frame size of 2464 bytes is larger than 1024 bytes 

The lz4hc_compress.c file is a good example, as it has the worst stack usage and is usable as a working test case outside of the kernel. I have reduced this file to a standalone .c file that can optionally compile into an executable program (lz4 compression from stdin to stdout). The code is orginally from www.lz4.org, but has been adapted for use in Linux.

Compile with:
gcc -O2 -Wall -Wno-pointer-sign -Wframe-larger-than=200 -fprofile-arcs  -c lz4hc_compress.c 

The same problem happens on all architectures, e.g. gcc-4.9.3:

Target                  -fprofile-arcs  normal
aarch64-linux-gcc         1136          112 
alpha-linux-gcc           1008          304 
am33_2.0-linux-gcc        1280           84 
arm-linux-gnueabi-gcc     1080          112 
cris-linux-gcc            828           100 
frv-linux-gcc             904           104 
hppa64-linux-gcc          944           248 
hppa-linux-gcc            824            92 
i386-linux-gcc            824           108 
m32r-linux-gcc            908           136 
microblaze-linux-gcc      832            88 
mips64-linux-gcc          864           192 
mips-linux-gcc            792           120 
powerpc64-linux-gcc       800            96 
powerpc-linux-gcc         808            56 
s390-linux-gcc            832           112 
sh3-linux-gcc             824           128 
sparc64-linux-gcc         896           192 
sparc-linux-gcc           824           104 
x86_64-linux-gcc          912           192 
xtensa-linux-gcc          816           128 

With gcc-4.8.1, the numbers are much lower:

arm-linux-gnueabi-gcc     184           104
x86_64-linux-gcc          224           192

The size of the binary object has also grown noticeably, from around 3000 bytes  without -fprofile-arcs (on any version) to 10300 bytes with gcc-5.3.1 but only 6941 bytes with gcc-4.8. Runtime speed does not appear to be affected much (less than 20% overhead for -fprofile-arcs, which seems reasonable).

I have tested ARM cross-compilers version 4.9.3 through 5.3.1, which all show similar problematic behavior, while version 4.6 through 4.8.3 are ok.


---


### compiler : `gcc`
### title : `performance issue with SP Linpack with Autovectorization`
### open_at : `2016-02-06T21:22:53Z`
### last_modified_date : `2021-05-04T12:31:59Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=69710
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `6.0`
### severity : `normal`
### contents :
Created attachment 37614
extracted daxpy example

We've noticed a performance problem in single precision
Linpack with the MSA patch applied:

https://gcc.gnu.org/ml/gcc-patches/2016-01/msg00177.html

which I have been able to reproduce with ARM Neon.

The problem that the autovectorization is generating more induction
variables for memory references in daxpy (this is an issue on all
architectures).  That is, when the statement:

  dy[i] = dy[i] + da*dx[i];

is vectorized the vector load associated with load of dy[i] uses
a different Induction Variable (IV) for the subsequent vector store
for dy[i].  For example, for ARM neon after vect we see:

  <bb 12>:
  # i_26 = PHI <i_44(11), i_19(20)>
  # vectp_dy.12_83 = PHI <vectp_dy.13_81(11), vectp_dy.12_84(20)>
  # vectp_dx.15_88 = PHI <vectp_dx.16_86(11), vectp_dx.15_89(20)>
  # vectp_dy.20_96 = PHI <vectp_dy.21_94(11), vectp_dy.20_97(20)>
  # ivtmp_99 = PHI <0(11), ivtmp_100(20)>
  i.0_7 = (unsigned int) i_26;
  _8 = i.0_7 * 4;
  _10 = dy_9(D) + _8;
  vect__12.14_85 = MEM[(float *)vectp_dy.12_83];
  _12 = *_10;
  _14 = dx_13(D) + _8;
  vect__15.17_90 = MEM[(float *)vectp_dx.15_88];
  _15 = *_14;
  vect__16.18_92 = vect_cst__91 * vect__15.17_90;
  _16 = da_6(D) * _15;
  vect__17.19_93 = vect__12.14_85 + vect__16.18_92;
  _17 = _12 + _16;
  MEM[(float *)vectp_dy.20_96] = vect__17.19_93;
  i_19 = i_26 + 1;
  vectp_dy.12_84 = vectp_dy.12_83 + 16;
  vectp_dx.15_89 = vectp_dx.15_88 + 16;
  vectp_dy.20_97 = vectp_dy.20_96 + 16;
  ivtmp_100 = ivtmp_99 + 1;
  if (ivtmp_100 < bnd.9_53)
    goto <bb 20>;
  else
    goto <bb 15>;
...
  <bb 20>:
  goto <bb 12>;

Note that the use of a separate IV for the load and store off of dy
can introduces a false memory dependency which causes poor scheduling
after unrolling.  From what I have seen so far, for double precision
the ivopts phase is able to clean up the induction variables so the
false memory dependency is removed.  However the cleanup does not
happen for single precision.

Attached simple example for single precision, more to follow.


---


### compiler : `gcc`
### title : `Unnecessary temporary object during std::thread construction`
### open_at : `2016-02-09T00:31:58Z`
### last_modified_date : `2020-08-18T13:30:19Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=69724
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `libstdc++`
### version : `6.0`
### severity : `enhancement`
### contents :
#include <thread>
#include <cstdio>

class F {
public:
    F() { std::puts("create"); }
    ~F() { std::puts("destroy"); }
    F(const F&) { std::puts("copy"); }
    F(F&&) noexcept { std::puts("move"); }
    void run() { }
};

int main()
{
  std::thread{&F::run, F{}}.join();
}

prints:

create
move
move
destroy
destroy
destroy

The standard requires a copy to be made, so one of the move constructions is required, but a more efficient result would be:

create
move
destroy
destroy

This could be done by removing the call to __bind_simple() and constructing the _Bind_simple member of the thread::_State_impl directly, rather than returning by value from __bind_simple() and then moving that value into the member.

However, the benefit for most types is probably small so the additional complexity might not be worth it.


---


### compiler : `gcc`
### title : `Vectorization runtime alias check due to failed dependence analysis`
### open_at : `2016-02-09T10:11:41Z`
### last_modified_date : `2022-03-29T12:57:59Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=69732
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `6.0`
### severity : `normal`
### contents :
We now fail to vectorize the testcase in PR69726 which exhibits the pattern

 p = &a[i];
 *(p + 0) = ...
 *(p + 1) = ...
 *(p + 2) = ...
...

where p is forward-propagated into *(p + 0) only, leading to

 a[i] = ...
 *(p + 1) = ...
...

which then results in

        base_address: &temp
        offset from base address: 0
        constant offset from base address: 0
        step: 32
        aligned to: 128
        base_object: temp
        Access function 0: {0, +, 8}_2

vs.

        base_address: &temp
        offset from base address: 0
        constant offset from base address: 16
        step: 32
        aligned to: 128
        base_object: MEM[(int *)&temp]
        Access function 0: {16B, +, 32}_2

which have different base objects and thus are not handled by dependence
analysis.  This results in bogus runtime alias checks.


---


### compiler : `gcc`
### title : `gcc/config/arm/arm.c:15949: return in strange place ?`
### open_at : `2016-02-17T15:26:37Z`
### last_modified_date : `2019-10-01T04:08:38Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=69857
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `6.0`
### severity : `normal`
### contents :
[trunk/gcc/config/arm/arm.c:15949]: (style) Statements following return, break, continue, goto or throw will never be executed.

Source code is

    else if (TARGET_ARM)
      {
        return false;
        int regno = REGNO (operands[0]);
        if (!peep2_reg_dead_p (4, operands[0]))
          {

svn blame says

197530     gretay     else if (TARGET_ARM)
197530     gretay       {
197530     gretay         return false;
197530     gretay         int regno = REGNO (operands[0]);
197530     gretay         if (!peep2_reg_dead_p (4, operands[0]))
197530     gretay           {


---


### compiler : `gcc`
### title : `vec_perm built-in is not handled by swap optimization on powerpc64le`
### open_at : `2016-02-18T20:53:19Z`
### last_modified_date : `2019-04-29T19:31:26Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=69868
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `6.0`
### severity : `normal`
### contents :
The following test case, compiled with --std=c++11 -maltivec -O3 on powerpc64le-unknown-linux-gnu, produces assembly code from which the endian swaps have not been removed.  The problem is that swap optimization is not smart enough to recognize the patterns produced by the vec_perm built-in.  Although we do recognize a vperm instruction whose permute control vector is loaded from the constant pool, the vec_perm built-in produces a sequence in which the PCV is loaded and then complemented, which requires more work to get right.

This provides an opportunity for further performance improvement, since swap optimization should be able to perform the complement at compile time, swap the results, and create this as a new constant to be loaded in the generated code.  This is something we've wanted to do anyway, and doing it in the context of swap optimization will catch these opportunities immediately after expand.

Opening this against myself as a reminder to fix this during next stage 1.

Test case:

#include <cstdlib>
#include <altivec.h>

using VecUC = vector unsigned char;
using VecUI = vector unsigned int;

void bar(VecUC *vpInput, VecUI *vpOut)
{
  VecUI v1 = {0,};
  VecUI vMask = { 0xffffff, 0xffffff,0xffffff,0xffffff};
  VecUI vShift = { 0xfffff, 0xffffff,0xffffff,0xffffff};
  VecUC vPermControl = { 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15 };

#define FOO(a,b,c)  v1 = (VecUI)vec_perm(vpInput[a], vpInput[b], vPermControl); \
  v1 = vec_sr(v1, vShift);                     \
  v1 = vec_and(v1, vMask);                          \
  vpOut[c] = v1;

  FOO(0,0,0);
  FOO(0,0,1);
  FOO(0,1,2);
  FOO(0,1,3);
  FOO(1,0,4);
  FOO(1,0,5);
}


---


### compiler : `gcc`
### title : `Type punned structs returned by value optimized poorly due to SRA`
### open_at : `2016-02-19T10:30:58Z`
### last_modified_date : `2023-04-27T23:16:36Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=69871
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `5.3.0`
### severity : `enhancement`
### contents :
The following code, which unpacks a 32-bit integer into a struct of four bytes, does not optimize as well as it should.  While "unpack" seems to optimize just fine, trivial wrappers of the function do not seem to get optimized nearly as well:

- Two of the wrappers ("wrapper", "wrapper2") are completely identical yet they do not result in the same assembly code.  One is optimized well, the other is not.
- Adding another layer of indirection ("wrapperwrapper") also prevents the optimization from occurring.

The problem occurs not only for union-based type-punning, but also for similar tricks that involve:

  - memcpy, where all three wrappers would optimize poorly, or
  - bitshift operators, where even "unpack" would optimize poorly.

See also: https://gcc.gnu.org/ml/gcc/2016-02/msg00244.html

The code was compiled with "gcc -fverbose-asm -Wall -S -O3 foo.c" on Linux 4.4.1 x86-64.  The GCC binaries are part of the Arch Linux's gcc-multilib 5.3.0-4 binary package.

---

struct alpha {
    char a, b, c, d;
};

struct alpha unpack(unsigned x)
{
    union {
        struct alpha r;
        unsigned i;
    } u;
    u.i = x;
    return u.r;
}

struct alpha wrapper(unsigned y)
{
    return unpack(y);
}

struct alpha wrapper2(unsigned y)
{
    return unpack(y);
}

struct alpha wrapperwrapper(unsigned y)
{
    return wrapper(y);
}

---

	.file	"foo.c"
# GNU C11 (GCC) version 5.3.0 (x86_64-unknown-linux-gnu)
#	compiled by GNU C version 5.3.0, GMP version 6.1.0, MPFR version 3.1.3-p5, MPC version 1.0.3
# GGC heuristics: --param ggc-min-expand=100 --param ggc-min-heapsize=131072
# options passed:  foo.c -mtune=generic -march=x86-64 -O3 -Wall
# -fverbose-asm
# options enabled:  -faggressive-loop-optimizations -falign-labels
# -fasynchronous-unwind-tables -fauto-inc-dec -fbranch-count-reg
# -fcaller-saves -fchkp-check-incomplete-type -fchkp-check-read
# -fchkp-check-write -fchkp-instrument-calls -fchkp-narrow-bounds
# -fchkp-optimize -fchkp-store-bounds -fchkp-use-static-bounds
# -fchkp-use-static-const-bounds -fchkp-use-wrappers
# -fcombine-stack-adjustments -fcommon -fcompare-elim -fcprop-registers
# -fcrossjumping -fcse-follow-jumps -fdefer-pop
# -fdelete-null-pointer-checks -fdevirtualize -fdevirtualize-speculatively
# -fdwarf2-cfi-asm -fearly-inlining -feliminate-unused-debug-types
# -fexpensive-optimizations -fforward-propagate -ffunction-cse -fgcse
# -fgcse-after-reload -fgcse-lm -fgnu-runtime -fgnu-unique
# -fguess-branch-probability -fhoist-adjacent-loads -fident -fif-conversion
# -fif-conversion2 -findirect-inlining -finline -finline-atomics
# -finline-functions -finline-functions-called-once
# -finline-small-functions -fipa-cp -fipa-cp-alignment -fipa-cp-clone
# -fipa-icf -fipa-icf-functions -fipa-icf-variables -fipa-profile
# -fipa-pure-const -fipa-ra -fipa-reference -fipa-sra -fira-hoist-pressure
# -fira-share-save-slots -fira-share-spill-slots
# -fisolate-erroneous-paths-dereference -fivopts -fkeep-static-consts
# -fleading-underscore -flifetime-dse -flra-remat -flto-odr-type-merging
# -fmath-errno -fmerge-constants -fmerge-debug-strings
# -fmove-loop-invariants -fomit-frame-pointer -foptimize-sibling-calls
# -foptimize-strlen -fpartial-inlining -fpeephole -fpeephole2
# -fpredictive-commoning -fprefetch-loop-arrays -free -freg-struct-return
# -freorder-blocks -freorder-blocks-and-partition -freorder-functions
# -frerun-cse-after-loop -fsched-critical-path-heuristic
# -fsched-dep-count-heuristic -fsched-group-heuristic -fsched-interblock
# -fsched-last-insn-heuristic -fsched-rank-heuristic -fsched-spec
# -fsched-spec-insn-heuristic -fsched-stalled-insns-dep -fschedule-fusion
# -fschedule-insns2 -fsemantic-interposition -fshow-column -fshrink-wrap
# -fsigned-zeros -fsplit-ivs-in-unroller -fsplit-wide-types -fssa-phiopt
# -fstdarg-opt -fstrict-aliasing -fstrict-overflow
# -fstrict-volatile-bitfields -fsync-libcalls -fthread-jumps
# -ftoplevel-reorder -ftrapping-math -ftree-bit-ccp -ftree-builtin-call-dce
# -ftree-ccp -ftree-ch -ftree-coalesce-vars -ftree-copy-prop
# -ftree-copyrename -ftree-cselim -ftree-dce -ftree-dominator-opts
# -ftree-dse -ftree-forwprop -ftree-fre -ftree-loop-distribute-patterns
# -ftree-loop-if-convert -ftree-loop-im -ftree-loop-ivcanon
# -ftree-loop-optimize -ftree-loop-vectorize -ftree-parallelize-loops=
# -ftree-partial-pre -ftree-phiprop -ftree-pre -ftree-pta -ftree-reassoc
# -ftree-scev-cprop -ftree-sink -ftree-slp-vectorize -ftree-slsr -ftree-sra
# -ftree-switch-conversion -ftree-tail-merge -ftree-ter -ftree-vrp
# -funit-at-a-time -funswitch-loops -funwind-tables -fverbose-asm
# -fzero-initialized-in-bss -m128bit-long-double -m64 -m80387
# -malign-stringops -mavx256-split-unaligned-load
# -mavx256-split-unaligned-store -mfancy-math-387 -mfp-ret-in-387 -mfxsr
# -mglibc -mieee-fp -mlong-double-80 -mmmx -mno-sse4 -mpush-args -mred-zone
# -msse -msse2 -mtls-direct-seg-refs -mvzeroupper

	.section	.text.unlikely,"ax",@progbits
.LCOLDB0:
	.text
.LHOTB0:
	.p2align 4,,15
	.globl	unpack
	.type	unpack, @function
unpack:
.LFB0:
	.cfi_startproc
	movl	%edi, %eax	# x, x
	ret
	.cfi_endproc
.LFE0:
	.size	unpack, .-unpack
	.section	.text.unlikely
.LCOLDE0:
	.text
.LHOTE0:
	.section	.text.unlikely
.LCOLDB1:
	.text
.LHOTB1:
	.p2align 4,,15
	.globl	wrapper
	.type	wrapper, @function
wrapper:
.LFB5:
	.cfi_startproc
	movl	%edi, %eax	# y, y
	xorl	%edx, %edx	# retval.9
	movsbl	%ah, %eax	# y, SR.14
	movb	%dil, %dl	# y, retval.9
	movb	%al, %dh	# SR.14, retval.9
	movl	%edi, %eax	# y, tmp101
	andl	$-16777216, %edi	#, tmp105
	andl	$16711680, %eax	#, tmp101
	movzwl	%dx, %edx	# retval.9, tmp103
	orl	%eax, %edx	# tmp101, tmp106
	movl	%edx, %eax	# tmp106, tmp107
	orl	%edi, %eax	# tmp105, tmp107
	ret
	.cfi_endproc
.LFE5:
	.size	wrapper, .-wrapper
	.section	.text.unlikely
.LCOLDE1:
	.text
.LHOTE1:
	.section	.text.unlikely
.LCOLDB2:
	.text
.LHOTB2:
	.p2align 4,,15
	.globl	wrapper2
	.type	wrapper2, @function
wrapper2:
.LFB2:
	.cfi_startproc
	movl	%edi, %eax	# y, y
	ret
	.cfi_endproc
.LFE2:
	.size	wrapper2, .-wrapper2
	.section	.text.unlikely
.LCOLDE2:
	.text
.LHOTE2:
	.section	.text.unlikely
.LCOLDB3:
	.text
.LHOTB3:
	.p2align 4,,15
	.globl	wrapperwrapper
	.type	wrapperwrapper, @function
wrapperwrapper:
.LFB3:
	.cfi_startproc
	movl	%edi, %eax	# y, y
	xorl	%edx, %edx	# D.1859
	movsbl	%ah, %eax	# y, SR.5
	movb	%dil, %dl	# y, D.1859
	movb	%al, %dh	# SR.5, D.1859
	movl	%edi, %eax	# y, tmp101
	andl	$-16777216, %edi	#, tmp105
	andl	$16711680, %eax	#, tmp101
	movzwl	%dx, %edx	# D.1859, tmp103
	orl	%eax, %edx	# tmp101, tmp106
	movl	%edx, %eax	# tmp106, tmp107
	orl	%edi, %eax	# tmp105, tmp107
	ret
	.cfi_endproc
.LFE3:
	.size	wrapperwrapper, .-wrapperwrapper
	.section	.text.unlikely
.LCOLDE3:
	.text
.LHOTE3:
	.ident	"GCC: (GNU) 5.3.0"
	.section	.note.GNU-stack,"",@progbits


---


### compiler : `gcc`
### title : `Vectorizer fails to emit runtime profitability check if no peeling/versioning is done`
### open_at : `2016-02-19T12:19:44Z`
### last_modified_date : `2022-03-29T13:10:51Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=69873
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `6.0`
### severity : `normal`
### contents :
double a[1024];
void foo (unsigned n)
{
  for (unsigned i = 0; i < n * 2; ++i)
    a[i] = 1.;
}

currently says the threshold is > 3 iterations but no such guard is added
(whether that's a reasonable threshold is another question of course).


---


### compiler : `gcc`
### title : `recognizing idioms that check for a buffer of all-zeros could make *much* better code`
### open_at : `2016-02-22T22:48:06Z`
### last_modified_date : `2018-12-23T12:04:15Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=69908
### status : `UNCONFIRMED`
### tags : `missed-optimization, ssemmx`
### component : `tree-optimization`
### version : `5.3.0`
### severity : `normal`
### contents :
Checking a block of memory to see if it's all-zero, or to find the first non-zero, seems to be a not-uncommon problem.  It's really hard to get gcc to emit code that's even half-way efficient.

The most recent stackoverflow question about this (with links to previous ones) is http://stackoverflow.com/questions/35450237/fastest-way-to-check-mass-data-if-null-in-c

Summary:

* gcc would benefit a lot from recognizing zero-checking idioms (with a suggested asm loop for x86).
* one zero-checking function compiles to bad x86 code in multiple ways
* even a simple byte-at-a-time loop on a fixed-size buffer compiles to byte-at-a-time asm.
* gcc is bad at horizontal reductions, esp with AVX2

I'm using x86 asm for examples of whether gcc auto-vectorizes or not, but this is architecture-independent.

---------


Ideally we'd like the main loop in these functions to test 64B at a time (a whole cache-line on all modern x86 microarchitectures), something like:

    ... some intro stuff ...
    pxor     %xmm5, %xmm5
.Lvec_loop:
    movdqa   (%rsi), %xmm0
    por    16(%rsi), %xmm0
    por    32(%rsi), %xmm0
    por    48(%rsi), %xmm0
#    ptest     %xmm0, %xmm0  # SSE4.1
#    jnz  .Lnonzero_found
    pcmpeqb   %xmm5, %xmm0
    pmovmskb  %xmm0, %eax
    cmp       $0xffff, %eax  # check that all the bytes compared equal to zero
    jne   .Lnonzero_found

    add    $64, %rsi
    cmp    pointer, end
    jb  $Lvec_loop 
    # Intel: 9 fused-domain uops in the loop: 
    # one too many to issue in 2 cycles and saturate 2 loads per cycle.

    # epilogue for the final partial cache-line
    # We can test some bytes again,
    # e.g. using 16B unaligned loads that end at the correct place
    movdqu  -16(end), %xmm0
    movdqu  -32(end), %xmm1
    por     %xmm1, %xmm0
    movdqu  -48(end), %xmm1
    por     %xmm1, %xmm0
    movdqu  -64(end), %xmm3
    por     %xmm1, %xmm0
    # ptest or pcmpeq / pmovmskb / cmp

We'd have the intro code handle inputs smaller than 64B, so the epilogue couldn't access memory from before the start of the buffer.

pcmpeq / pmovmsk / cmp is better than pshufd / por / movq / test, esp for 32bit where another round of horizontal reduction would be needed.

It might be better to use two accumulators to make better use of two load ports from a single cache-line, but hopefully the loads will dispatch mostly in program order, so there hopefully won't be many cache-bank conflicts on SnB/IvB when multiple iterations are in flight at once.  The POR dep chain is not loop-carried, and out-of-order execution should hide it nicely.


I have no idea how to write C (without intrinsics) that would auto-vectorize to anything like that, or even to something acceptable.  It would be nice if there was some kind of idiom that compilers could recognize and make good code for, without needing custom code for every platform where we want non-terrible output.


----------

The most solid attempt on that SO question ORs together eight size_t elements in the main loop, then uses a byte cleanup loop.  gcc makes a mess of it:

Summary of problems with gcc 5.3.0 -O3 -march=haswell for this function:

(I can report separate bugs for the separate problems; Other than recognizing zero-checking idioms, most of these problems could probably be fixed separately.)

* gcc doesn't realize that we're ultimately testing for all-zero, and just treats OR as any other associative operation.

* even a simple byte-loop over a fixed-size buffer doesn't get optimized at all (different function, see below)

* main loop not auto-vectorized
* word-at-a-time and byte-at-a-time cleanup loops generate full loops:
  gcc doesn't realize they're just cleanup that will only do less than one vector of data.
* word-at-a-time cleanup loop gets a bloated fully-unrolled scalar intro (which is all that will ever run)
* byte cleanup loop auto-vectorization unpacks vectors of bytes to longs before ORing, with a big chain of vextracti128 / vmovzx.
* Without AVX2, gcc does a full-unroll of the unaligned-epilogue for the byte cleanup autovectorization.


The bad auto-vectorized cleanup-loop code will never run, only their scalar intros, because of the logic of the function.  Presumably gcc would generate the nasty pmovzx byte-unpacking code in situations where it would actually run.

The byte cleanup loop has a byte-at-a-time scalar intro loop (not unrolled), which is ok I guess.


//  See on godbolt: http://goo.gl/DHKUIE
int dataisnull_orig_evenworse(const void *data, size_t length) {
    /* assuming data was returned by malloc, thus is properly aligned */
    size_t i = 0, n = length / sizeof(size_t);
    const size_t *pw = data;
    const unsigned char *pb = data;
#define UNROLL_FACTOR  8
    size_t n1 = n - n % UNROLL_FACTOR;
    for (; i < n1; i += UNROLL_FACTOR) {
        size_t val = pw[i + 0] | pw[i + 1] | pw[i + 2] | pw[i + 3] |
                     pw[i + 4] | pw[i + 5] | pw[i + 6] | pw[i + 7];
        if (val)
            return 0;
    }

    size_t val = 0;
    // gcc fully unrolls this cleanup loop
    for (; i < n; i++) {
        val |= pw[i];
    }

    i = n * sizeof(size_t)
    // Without AVX2, gcc does a full-unroll of the unaligned-epilogue for the byte cleanup autovectorization

    for (; i < length; i++) {
        val |= pb[i];
    }
    return val == 0;
}

The main loop doesn't get autovectorized at all, so it's just a sequence of straightforward scalar ORs and then a conditional branch.  The cleanup code is massively bloated, though, at -O3.  The byte-cleanup loop gets auto-vectorized, and gcc doesn't figure out that it can run at most 7B.  Worst of all, it unpacks bytes to longs before ORing, with a chain of many vextracti128, 2x vpmovzxbw, 4x vpmovzxwd, and 8x vpmovzxdq.

-----

Even the sequence to horizontally OR a single vector down to a long is clunky:

        vpxor   %xmm1, %xmm1, %xmm1
        vperm2i128      $33, %ymm1, %ymm0, %ymm2
        vpor    %ymm2, %ymm0, %ymm0
        vperm2i128      $33, %ymm1, %ymm0, %ymm1
        vpalignr        $8, %ymm0, %ymm1, %ymm1
        vpor    %ymm1, %ymm0, %ymm0
        vmovq   %xmm0, %rdx

With only -mavx, it only uses 16B vectors, and does the horizontal OR with

        vpsrldq $8, %xmm2, %xmm0
        vpor    %xmm0, %xmm2, %xmm2
        addq    %r12, %rcx
        vmovq   %xmm2, %rdx


The optimal AVX2 sequence would use vextracti128, not vperm2i128.  Shuffling with a zeroed vector is perverse, and using 256b lane-crossing shuffles is slow.  Reducing to a 128b vector ASAP is better for energy/power reasons, and latency.  Esp for a hypothetical CPU that implements AVX2 the way Bulldozer-family does AVX (with 128b execution units).

        # suggested optimal horizontal-OR sequence
        vextracti128    $1, %ymm0, %xmm1
        vpor            %xmm1, %xmm0, %xmm0
        vpshufd         $0b1001110, %xmm0, %xmm1  # swap upper/lower halves
        vpor            %xmm1, %xmm0, %xmm0
        vmovq           %xmm0, %rdx

Using pshufd works great in the non-AVX case, saving a movdqa because it's not an in-place shuffle like psrldq, unpckhqdq.  pshufd is also slightly cheaper than psrldq on Pentium M, but apparently not on first-gen Core2 (according to Agner Fog's tables).  It's a tiny difference: avoiding the movdqa with pshufd is the way to go for the benefit of all other CPUs in builds without -mavx.  With -mtune=core2. movdqa / unpckhqdq would be optimal, because shuffles with 64b elements are very cheap on Merom.

movhlps %xmm0, %xmm1 would be good, except for a potential bypass-delay (int->float and back) on some CPUs (probably Nehalem).  We have a scratch register (xmm1) that's part of the same dep chain, and that has to be ready already.

palignr $24, %xmm0, %xmm1  has possibilities (since we have a scratch reg we don't mind a data dependency on): slightly faster than pshufd on first-gen core2 (merom/conroe), but same everywhere else.  Longer instruction encoding than pshufd, though, so it's actually worse than pshufd for everything else (and much harder to use; because we need to identify a scratch reg that we already have a data dependency on).

What gcc actually does with -march=core2 is movdqa / psrldq / por down to one byte, then a movaps store, then a movzbl load into an integer register.  Obviously a movd / movzbl %dl, %edx would be better, or recognize the zero-checking and don't worry about zeroing the upper bytes.  If the low byte is zero, the upper bytes will be, too.  And if we're optimizing for first-gen (not 45nm Penryn which has a full 128b shuffle unit), then palignr or movdqa / unpckhqd would be optimal.  Then movq to integer, and mov/shr/or in integer registers.  Those instructions are shorter, so you'll get less of a decode bottleneck (definitely an issue for CPUs without a uop cache, with long SSE instructions).


------------------

Even the most straightforward function with a fixed size doesn't get optimized at all:

char data [static 4096] prevents decay into a simple pointer, guaranteeing that it's safe to read the full object, instead of having to avoid reading data that the C source wouldn't.

int allzero_fixedsize(const char data [static 4096]) {
  size_t len=4096;
  while(len--)
    if (*(data++)) return 0;
  return 1;
}
   gcc 5.3 -O3 -march=haswell

        lea     rax, [rdi+4096]
        jmp     .L10
.L15:
        cmp     rdi, rax
        je      .L14
.L10:
        add     rdi, 1
        cmp     BYTE PTR [rdi-1], 0
        je      .L15
        xor     eax, eax
        ret
.L14:
        mov     eax, 1

clang doesn't do any better (it's actually worse, including mov eax, 1 in the hot loop.)


---


### compiler : `gcc`
### title : `non-ideal branch layout for an early-out return`
### open_at : `2016-02-24T03:50:41Z`
### last_modified_date : `2021-12-09T16:53:57Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=69933
### status : `RESOLVED`
### tags : `missed-optimization, needs-bisection`
### component : `target`
### version : `5.3.0`
### severity : `normal`
### contents :
(just guessing about this being an RTL bug, please reassign if it's target-specific or something else).

This simple linked-list traversal compiles to slightly bulkier code than it needs to:

int traverse(struct foo_head *ph)
{
  int a = -1;
  struct foo *p, *pprev;
  pprev = p = ph->h;
  while (p != NULL) {
    pprev = p;
    p = p->n;
  }
  if (pprev)
    a = pprev->a;
  return a;
}

 (gcc 5.3.0 -O3 on godbolt: http://goo.gl/r8vb5L)

        movq    (%rdi), %rdx
        movl    $-1, %eax       ; only needs to happen in the early-out case
        testq   %rdx, %rdx
        jne     .L3             ; jne/ret or je / fall through would be better
        jmp     .L9
.L5:
        movq    %rax, %rdx
.L3:
        movq    (%rdx), %rax
        testq   %rax, %rax
        jne     .L5
        movl    8(%rdx), %eax
        ret
.L9:
               ; ARM / PPC gcc 4.8.2 put the a=-1 down here
        ret                     ; this is a rep ret without -mtune=intel


Clang 3.7 chooses a better layout with a je .early_out instead the jne / jmp.  It arranges the loop so it can enter at the top.  It actually look pretty optimal:

        movq    (%rdi), %rcx
        movl    $-1, %eax
        testq   %rcx, %rcx
        je      .LBB0_3
.LBB0_1:                                # %.lr.ph
        movq    %rcx, %rax
        movq    (%rax), %rcx
        testq   %rcx, %rcx
        jne     .LBB0_1
        movl    8(%rax), %eax
.LBB0_3:                                # %._crit_edge.thread
        retq

Getting the mov $-1 out of the common case would require a separate mov/ret block after the normal ret, so it's a code-size tradeoff which isn't worth it, because a mov-immediate is dirt cheap.

Anyway, there are a couple different ways to lay out the branches and the mov $-1, %eax, but gcc's choice is in no way optimal. :(


---


### compiler : `gcc`
### title : `load not hoisted out of linked-list traversal loop`
### open_at : `2016-02-24T04:15:01Z`
### last_modified_date : `2021-12-06T05:46:09Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=69935
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `5.3.0`
### severity : `normal`
### contents :
(please check the component.  I guessed tree-optimization since it's cross-architecture.)

gcc doesn't hoist the p->a load out of the loop in this linked-list function

int traverse_loadloop(struct foo_head *ph)
{
  int a = -1;
  struct foo *p = ph->h;
  while (p) {
    a = p->a;
    p = p->n;
  }
  return a;
}

I checked on godbolt with gcc 4.8 on ARM/PPC/ARM64, and gcc 4.5.3 for AVR.
For x86, gcc 5.3.0 -O3 on godbolt (http://goo.gl/r8vb5L) does this:

        movq    (%rdi), %rdx
        movl    $-1, %eax
        testq   %rdx, %rdx
        je      .L10
.L11:
        movl    8(%rdx), %eax     ; load p->a inside the loop, not hoisted
        movq    (%rdx), %rdx
        testq   %rdx, %rdx
        jne     .L11
.L10:
        rep ret

This is nice and compact, but less hyperthreading-friendly than it could be.  (The mov reg,reg alternative doesn't even take an execution unit on recent CPUs).

The load of p->a every time through the loop might also delay the p->n load by a cycle on CPUs with only one load port, or when there's a cache-bank conflict.  This might take the loop from one iteration per 4c to one per 5c (if L1 load-use latency is 4c).

Clang hoists the load out of the loop, producing identical asm output for this function and one with the load hoisted in the C source.  (The godbolt link has both versions.  Also see bug 69933 which I just reported, since gcc showed a separate branch-layout issue for the source-level hoisting version.)


---


### compiler : `gcc`
### title : `expressions with multiple associative operators don't always create instruction-level parallelism`
### open_at : `2016-02-24T15:16:34Z`
### last_modified_date : `2023-09-24T03:41:56Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=69943
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `5.3.0`
### severity : `normal`
### contents :
separate problems (which maybe should be separate bugs, let me know):

* associativity not exploited for ILP in integer operations
* using a mov from memory instead of an add
* FP ILP from associativity generates two extra mov instructions


gcc 5.3.0 -O3 (http://goo.gl/IRdw05) has two problems compiling this:

int sumi(int a, int b,int c,int d,int e,int f,int g,int h) {
  return a+b+c+d+e+f+g+h;
}
        addl    %edi, %esi
        movl    8(%rsp), %eax     # when an arg comes from memory, it forgets to use lea as a 3-arg add
        addl    %esi, %edx
        addl    %edx, %ecx
        addl    %ecx, %r8d
        addl    %r8d, %r9d
        addl    %r9d, %eax
        addl    16(%rsp), %eax

The expression is evaluated most in order from left to right, not as
((a+b) + (c+d)) + ((e+f) + (g+h)).  This gives is a latency of 8 clocks.  If the inputs became ready at one-per-clock, this would be ideal (only one add depends on the last input), but we shouldn't assume that when we can't see the code that generated them.

The same lack of parallelism happens on ARM, ARM64, and PPC.

---------

The FP version of the same *does* take advantage of associativity for parallelism with -ffast-math, but uses two redundant mov instructions:

float sumf(float a, float b,float c,float d,float e,float f,float g,float h) {
  return a+b+c+d+e+f+g+h;
}
        addss   %xmm4, %xmm5  # e, D.1876
        addss   %xmm6, %xmm7  # g, D.1876
        addss   %xmm2, %xmm3  # c, D.1876
        addss   %xmm0, %xmm1  # a, D.1876
        addss   %xmm7, %xmm5  # D.1876, D.1876
        movaps  %xmm5, %xmm2        # D.1876, D.1876
        addss   %xmm3, %xmm2  # D.1876, D.1876
        movaps  %xmm2, %xmm0        # D.1876, D.1876
        addss   %xmm1, %xmm0  # D.1876, D.1876

clang avoids any unnecessary instructions, but has less FP ILP, and the same lack of integer ILP.

Interestingly, clang lightly auto-vectorizes sumf when the expression is parenthesised for ILP, but only *without* -ffast-math.  http://goo.gl/Pqjtu1.

As usual, IDK whether to mark this as RTL, tree-ssa, or middle-end.  The integer ILP problem is not target specific.


---


### compiler : `gcc`
### title : `missed tail merge optimization`
### open_at : `2016-02-27T16:17:09Z`
### last_modified_date : `2023-06-09T14:50:37Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=69991
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `6.0`
### severity : `enhancement`
### contents :
Consider testcase test.c:
...
void
foo (int c, int d, int *z, int *y)
{
  int res = 0;
  if (c)
    {
      *y = 0;
      if (d)
        {
          *z = 1;
          res = *y;
        }
    }
  else
    {
      *z = 1;
      res = *y;
    }
}
...

When compiled with -O2 -fno-tree-dce, tail-merge fails, due to this check in find_duplicate:
...
  /* If the incoming vuses are not the same, and the vuse escaped into an
     SSA_OP_DEF, then merging the 2 blocks will change the value of the def,
     which potentially means the semantics of one of the blocks will be changed.
     TODO: make this check more precise.  */
  if (vuse_escaped && vuse1 != vuse2)
    return;
...

Removing the check allows the testcase to be tail-merged, and the testcase belonging the check (pr52734.c) still passes.  This is due to the fix for PR62167. With a less conservative fix for PR62167, we'd still need this check for pr52734.c. So it's not necessarily a good idea to remove the check now.

A quick fix would be to ignore defs with no uses in gsi_advance_bw_nondebug_nonlocal, in the same way we ignore stmts with zero operands. But the usability of such a fix would be limited.

Another option is to consider the TODO mentioned in the comment. The test-case pr52734.c can actually safely be tail-merged, as long as the right bb is chosen. If we can model the incoming vuse as a dependency for one bb, we should be able to choose the right bb (the empty one with no depencencies).


---


### compiler : `gcc`
### title : `tree-ssa-tail-merge engine replacement`
### open_at : `2016-03-01T18:41:26Z`
### last_modified_date : `2023-06-09T14:50:37Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70032
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `6.0`
### severity : `enhancement`
### contents :
https://gcc.gnu.org/ml/gcc-patches/2015-07/msg00755.html :
...
Hello.

It's going to be almost a year Richard advised me to utilize IPA ICF
infrastructure in tree-ssa-tail-merge, currently using value numbering which
is quite hard to maintain.
Following small patch set is kick-off and I am opened for advices. Meanwhile,
I'm going to send statistics about merged basic blocks before/after the patch set.

Patch set can bootstrap on x86_64-linux-pc and survives regression tests.

Thanks,
Martin
...


---


### compiler : `gcc`
### title : `empty (not detected) sub-loop not removed`
### open_at : `2016-03-02T10:56:58Z`
### last_modified_date : `2021-08-29T01:02:32Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70041
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.3`
### severity : `enhancement`
### contents :
I have written two simple program to test the gcc optimization. I compiled them with -O2, but there is some difference of the assembly code. In my programs, I want to output "hello" in the loop, and add some delay between each output. These two programs are only for illustrating the bug (I think it maybe), and I know I can using volatile or asm in prgram 1 to achive my purpose. 

Program 1

#include <stdio.h>

int main(int argc, char **argv)
{
  	unsigned long i = 0;
 	while (1) {
 		if (++i > 0x1fffffffUL) {
			printf("hello\n");
		    i = 0;
		}
	}
}

Compile with -O2, the assembly code is:

Disassembly of section .text.startup:

00000000 <_main>:
#include <stdio.h>

int main(int argc, char **argv)
{
   0:	55                   	push   %ebp
   1:	89 e5                	mov    %esp,%ebp
   3:	83 e4 f0             	and    $0xfffffff0,%esp
   6:	83 ec 10             	sub    $0x10,%esp
   9:	e8 00 00 00 00       	call   e <_main+0xe>
   e:	66 90                	xchg   %ax,%ax
  10:	c7 04 24 00 00 00 00 	movl   $0x0,(%esp)
  17:	e8 00 00 00 00       	call   1c <_main+0x1c>
  1c:	eb f2                	jmp    10 <_main+0x10>
  1e:	90                   	nop
  1f:	90                   	nop


Program 2

int main(int argc, char **argv)
{
	unsigned long i = 0;
	while (1) {
		if (i > 0x1fffffffUL) {
			printf("hello\n");
			i = 0;
		}
		i++;
	}
}

Compile with -O2, the assembly code is:

Disassembly of section .text.startup:

00000000 <_main>:
#include <stdio.h>

int main(int argc, char **argv)
{
   0:	55                   	push   %ebp
   1:	89 e5                	mov    %esp,%ebp
   3:	83 e4 f0             	and    $0xfffffff0,%esp
   6:	83 ec 10             	sub    $0x10,%esp
   9:	e8 00 00 00 00       	call   e <_main+0xe>
   e:	31 c0                	xor    %eax,%eax
  10:	83 c0 01             	add    $0x1,%eax
  13:	3d ff ff ff 1f       	cmp    $0x1fffffff,%eax
  18:	76 f6                	jbe    10 <_main+0x10>
  1a:	c7 04 24 00 00 00 00 	movl   $0x0,(%esp)
	while (1) {
		if (i > 0x1fffffffUL) {
			printf("hello\n");
			i = 0;
		}
		i++;
  21:	e8 00 00 00 00       	call   26 <_main+0x26>

int main(int argc, char **argv)
{
	unsigned long i = 0;
	while (1) {
		if (i > 0x1fffffffUL) {
  26:	31 c0                	xor    %eax,%eax
  28:	eb e6                	jmp    10 <_main+0x10>
			printf("hello\n");
  2a:	90                   	nop
  2b:	90                   	nop
  2c:	90                   	nop
  2d:	90                   	nop
  2e:	90                   	nop
  2f:	90                   	nop


In program 1, the increasement of i is optimized out, but it's not in program 2. Why this happens? Is it a bug of gcc -O2?


---


### compiler : `gcc`
### title : `Returning a struct of _Decimal128 values generates extraneous stores and loads`
### open_at : `2016-03-02T22:03:59Z`
### last_modified_date : `2022-10-28T06:56:37Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70053
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `6.0`
### severity : `normal`
### contents :
If we compile the following testcase, we see uneeded stores to the stack followed by immediate loads from the same stack slots just before the return.  One set of stores/loads is completely unneeded and the others can be replaced by simple fmrs.

bergner@genoa:~/gcc/BUGS/DFP/arith128-P8AT9/src$ cat t.i 
typedef struct
{
  _Decimal128 td0;
  _Decimal128 td1;
} TDx2_t;


TDx2_t
D256_add_finite (_Decimal128 a, _Decimal128 b, _Decimal128 c)
{
  TDx2_t result;

  result.td0 = a;
  result.td1 = b;

  if (b == c)
  {
    result.td0 = c;
    result.td1 = c;
    return result;
  }

  return result;
}

bergner@genoa:~/gcc/BUGS/DFP/$ /home/bergner/gcc/build/gcc-fsf-mainline-base-debug/gcc/xgcc -B/home/bergner/gcc/build/gcc-fsf-mainline-base-debug/gcc -O2 -mcpu=power8 -S t.i 
bergner@genoa:~/gcc/BUGS/DFP/$ cat t.s 
	.file	"t.i"
	.abiversion 2
	.section	".text"
	.align 2
	.p2align 4,,15
	.globl D256_add_finite
	.type	D256_add_finite, @function
D256_add_finite:
	dcmpuq 7,4,6
	beq 7,.L5
	stfd 3,-64(1)
	stfd 2,-56(1)
	stfd 5,-48(1)
	stfd 4,-40(1)
	ori 2,2,0
	lfd 3,-64(1)
	lfd 2,-56(1)
	lfd 5,-48(1)
	lfd 4,-40(1)
	blr
	.p2align 4,,15
.L5:
	stfd 7,-64(1)
	stfd 6,-56(1)
	stfd 7,-48(1)
	stfd 6,-40(1)
	ori 2,2,0
	lfd 3,-64(1)
	lfd 2,-56(1)
	lfd 5,-48(1)
	lfd 4,-40(1)
	blr


---


### compiler : `gcc`
### title : `missed constant propagation in memcpy expansion`
### open_at : `2016-03-04T11:10:31Z`
### last_modified_date : `2021-08-07T02:14:41Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70079
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `5.3.1`
### severity : `normal`
### contents :
int f(char *restrict a, const char *restrict b)
{
	__builtin_memcpy(a, b, 512);
}

$ gcc f.c -O2 - -o f.s

includes the following code:

        movq    %rdi, %rcx
        leaq    8(%rdi), %rdi
        andq    $-8, %rdi                 ;; 1
        subq    %rdi, %rcx                ;; 2
        subq    %rcx, %rsi                ;; 3
        addl    $512, %ecx                ;; 4
        shrl    $3, %ecx                  ;; 5

At 1, rdi = (a + 8) & ~7 = a & ~7 + 8 = a + 8 - (a & 7)
At 2, rcx = a - rdi = a - a - 8 + (a & 7) = (a & 7) - 8
At 3, rsi = b - (a & 7) + 8
At 4, rcx = (a & 7) + 504, which is between 504 and 511
At 5, rcx is always 31.

Not sure how to fix it in RTL optimizers, so I'm leaving this in the target component for a backend-specific fix.


---


### compiler : `gcc`
### title : `missed optimization when passing a constant struct argument by value`
### open_at : `2016-03-05T13:47:28Z`
### last_modified_date : `2021-08-16T00:53:54Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70094
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `5.3.0`
### severity : `enhancement`
### contents :
Function baz in the code listing below gets compiled into something that writes to the stack. This is unnecessary: one can just load the argument into rdi with movabs and get rid of stack adjustments and memory accesses:

---snip---
[robryk@sharya-rana gccbug]$ cat > bug.cc
struct foo {
  int a;
  int b;
  int c;
};

void bar(foo);

void baz() {
  foo f;
  f.a = 1;
  f.b = 2;
  f.c = 3;
  bar(f);
}
[robryk@sharya-rana gccbug]$ g++ -v
Using built-in specs.
COLLECT_GCC=g++
COLLECT_LTO_WRAPPER=/usr/lib/gcc/x86_64-unknown-linux-gnu/5.3.0/lto-wrapper
Target: x86_64-unknown-linux-gnu
Configured with: /build/gcc-multilib/src/gcc-5.3.0/configure --prefix=/usr --libdir=/usr/lib --libexecdir=/usr/lib --mandir=/usr/share/man --infodir=/usr/share/info --with-bugurl=https://bugs.archlinux.org/ --enable-languages=c,c++,ada,fortran,go,lto,objc,obj-c++ --enable-shared --enable-threads=posix --enable-libmpx --with-system-zlib --with-isl --enable-__cxa_atexit --disable-libunwind-exceptions --enable-clocale=gnu --disable-libstdcxx-pch --disable-libssp --enable-gnu-unique-object --enable-linker-build-id --enable-lto --enable-plugin --enable-install-libiberty --with-linker-hash-style=gnu --enable-gnu-indirect-function --enable-multilib --disable-werror --enable-checking=release
Thread model: posix
gcc version 5.3.0 (GCC) 
[robryk@sharya-rana gccbug]$ g++ bug.cc -O2 -c -o bug.o
[robryk@sharya-rana gccbug]$ objdump -d bug.o

bug.o:     file format elf64-x86-64


Disassembly of section .text:

0000000000000000 <_Z3bazv>:
   0:	48 83 ec 18          	sub    $0x18,%rsp
   4:	be 03 00 00 00       	mov    $0x3,%esi
   9:	c7 04 24 01 00 00 00 	movl   $0x1,(%rsp)
  10:	c7 44 24 04 02 00 00 	movl   $0x2,0x4(%rsp)
  17:	00 
  18:	48 8b 3c 24          	mov    (%rsp),%rdi
  1c:	e8 00 00 00 00       	callq  21 <_Z3bazv+0x21>
  21:	48 83 c4 18          	add    $0x18,%rsp
  25:	c3                   	retq   
---snip---

I've verified that Clang performs the optimization I was talking about and that, according to gcc.godbolt.org, a snapshot of gcc 6 misses this optimization too.

For comparison, the code Clang produces (according to godbolt):

        movabsq $8589934593, %rdi       # imm = 0x200000001
        movl    $3, %esi
        jmp     bar(foo)              # TAILCALL


---


### compiler : `gcc`
### title : `gcc reports bad dependence and bails out of vectorization for one of the bwaves loops.`
### open_at : `2016-03-06T07:18:33Z`
### last_modified_date : `2021-05-04T13:33:35Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70103
### status : `RESOLVED`
### tags : `alias, missed-optimization`
### component : `tree-optimization`
### version : `6.0`
### severity : `enhancement`
### contents :
flux_lam.f:68:0: note: dependence distance  = 0.
flux_lam.f:68:0: note: dependence distance == 0 between MEM[(real(kind=8)D.18[0:D.3627] *)ev_197(D) clique 1 base 12][_244] and MEM[(real(kind=8)D.18[0:D.3627] *)ev_197(D) clique 1 base 12][_244]
flux_lam.f:68:0: note: READ_WRITE dependence in interleaving.
flux_lam.f:68:0: note: bad data dependence.

Looking at vector dumps, if we have CSEd the load, then there is no dependency issue here. 

MEM[(real(kind=8)D.18[0:D.3627] *)ev_197(D) clique 1 base 12][_244] = _272

_323 = MEM[(real(kind=8)D.18[0:D.3627] *)ev_197(D) clique 1 base 12][_244];


---snip---
  MEM[(real(kind=8)D.18[0:D.3627] *)ev_197(D) clique 1 base 12][_244] = _272;
  # VUSE <.MEM_273>
  _274 = MEM[(real(kind=8)D.18[0:D.3605] *)u.105_58][_219];
  # VUSE <.MEM_273>
  _275 = MEM[(real(kind=8)D.18[0:D.3605] *)u.105_58][_224];
  _276 = _274 - _275;
  _277 = ((_276));
  t1_278 = _277 / dy2_68;
  _279 = _195 + 3;
  # VUSE <.MEM_273>
  _280 = MEM[(real(kind=8)D.18[0:D.3605] *)u.105_58][_252];
  # VUSE <.MEM_273>
  _281 = MEM[(real(kind=8)D.18[0:D.3605] *)u.105_58][_254];
  _282 = _280 - _281;
  _283 = ((_282));
  _284 = _283 / dy2_68;
  _285 = t1_278 + _284;
  _286 = ((_285));
  _287 = _286 * 5.0e-1;
  # VUSE <.MEM_273>
  _288 = MEM[(real(kind=8)D.18[0:D.3601] *)v.107_60][_206];
  # VUSE <.MEM_273>
  _289 = MEM[(real(kind=8)D.18[0:D.3601] *)v.107_60][_203];
  _290 = _288 - _289;
  _291 = ((_290));
  _292 = _291 / _64;
  _293 = _287 + _292;
  _294 = ((_293));
  _295 = t0_210 * _294;
  # .MEM_296 = VDEF <.MEM_273>
  MEM[(real(kind=8)D.18[0:D.3627] *)ev_197(D) clique 1 base 12][_279] = _295;
  # VUSE <.MEM_296>
  _297 = MEM[(real(kind=8)D.18[0:D.3605] *)u.105_58][_233];
  # VUSE <.MEM_296>
  _298 = MEM[(real(kind=8)D.18[0:D.3605] *)u.105_58][_239];
  _299 = _297 - _298;
  _300 = ((_299));
 t2_301 = _300 / dz2_71;
  _302 = _195 + 4;
  # VUSE <.MEM_296>
  _303 = MEM[(real(kind=8)D.18[0:D.3605] *)u.105_58][_261];
  # VUSE <.MEM_296>
  _304 = MEM[(real(kind=8)D.18[0:D.3605] *)u.105_58][_263];
  _305 = _303 - _304;
  _306 = ((_305));
  _307 = _306 / dz2_71;
  _308 = t2_301 + _307;
  _309 = ((_308));
  _310 = _309 * 5.0e-1;
  # VUSE <.MEM_296>
  _311 = MEM[(real(kind=8)D.18[0:D.3597] *)w.109_62][_206];
  # VUSE <.MEM_296>
  _312 = MEM[(real(kind=8)D.18[0:D.3597] *)w.109_62][_203];
  _313 = _311 - _312;
  _314 = ((_313));
  _315 = _314 / _64;
  _316 = _310 + _315;
  _317 = ((_316));
  _318 = t0_210 * _317;
  # .MEM_319 = VDEF <.MEM_296>
  MEM[(real(kind=8)D.18[0:D.3627] *)ev_197(D) clique 1 base 12][_302] = _318;
  _320 = _195 + 5;
  _321 = _246 + _247;
  _322 = ((_321));
  # VUSE <.MEM_319>
   _323 = MEM[(real(kind=8)D.18[0:D.3627] *)ev_197(D) clique 1 base 12][_244];
---snip---


---


### compiler : `gcc`
### title : `[11/12/13/14 Regression] Code/performance regression due to poor register allocation on Cortex-M0`
### open_at : `2016-03-10T10:58:53Z`
### last_modified_date : `2023-07-07T10:31:13Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70164
### status : `NEW`
### tags : `missed-optimization, ra`
### component : `rtl-optimization`
### version : `6.0`
### severity : `normal`
### contents :
Created attachment 37920
current ira dump

After a quick investigation of the testcase in gcc/testsuite/gcc.target/arm/pr45701-1.c for cortex-m0 on trunk I found out that the test case was failing due to a change in the register allocation after revision r226901.

Before this register allocation would choose to load the global 'hist_verify' onto r6 representing 'old_verify' prior to the function call to pre_process_line. This old_verify is used after the function call. With the patch it decides to load it onto r3, a caller-saved register, which means it has to be spilled before the function call and reloaded after.

Before patch:
history_expand_line_internal:
        push    {r3, r4, r5, r6, r7, lr}
        ldr     r3, .L5
        ldr     r5, .L5+4
        ldr     r4, [r3]
        movs    r3, #0
        ldr     r6, [r5]       ; <--- load of 'hist_verify' onto r6
        movs    r7, r0
        str     r3, [r5]
        bl      pre_process_line
        adds    r6, r4, r6
        str     r6, [r5]
        movs    r4, r0
        cmp     r7, r0
        bne     .L2
        bl      str_len
        adds    r0, r0, #1
        bl      x_malloc
        movs    r1, r4
        bl      str_cpy
        movs    r4, r0
.L2:
        movs    r0, r4
        @ sp needed
        pop     {r3, r4, r5, r6, r7, pc}

Current:
history_expand_line_internal:
        push    {r0, r1, r2, r4, r5, r6, r7, lr}
        ldr     r3, .L3
        ldr     r5, .L3+4
        ldr     r6, [r3]
        ldr     r3, [r5]        ; <--- load of 'hist_verify' onto r3
        movs    r7, r0
        str     r3, [sp, #4]    ; <--- Spill
        movs    r3, #0
        str     r3, [r5]
        bl      pre_process_line
        ldr     r3, [sp, #4]    ; <--- Reload
        movs    r4, r0
        adds    r6, r6, r3
        str     r6, [r5]
        cmp     r7, r0
        bne     .L1
        bl      str_len
        adds    r0, r0, #1
        bl      x_malloc
        movs    r1, r4
        bl      str_cpy
        movs    r4, r0
.L1:
        movs    r0, r4
        @ sp needed
        pop     {r1, r2, r3, r4, r5, r6, r7, pc}


I have also attached the dumps for ira and reload for both pre-patch and current. In the current reload dump insn 9 represents the load onto r3 and insn 62 the spill. In pre-patch ira/reload the load is in insn 10.

I am not familiar with RA in GCC, so I'm not entirely sure what code to blame for this sub-optimal allocation, any comments or pointers would be most welcome.


---


### compiler : `gcc`
### title : `Loop-invariant memory loads from std::string innards are not hoisted`
### open_at : `2016-03-10T22:48:19Z`
### last_modified_date : `2023-01-19T06:17:59Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70178
### status : `UNCONFIRMED`
### tags : `alias, missed-optimization`
### component : `c++`
### version : `6.0`
### severity : `enhancement`
### contents :
Consider

#include <string>
#include <algorithm>
#include <iterator>
using std::string;

inline unsigned char hexval(unsigned char c)
{
    if (c >= '0' && c <= '9')
        return c - '0';
    else if (c >= 'A' && c <= 'F')
        return c - 'A' + 10;
    else if (c >= 'a' && c <= 'f')
        return c - 'a' + 10;
    else
        throw "input character not a hexadecimal digit";
}

void hex2ascii_1(const string& in, string& out)
{
    size_t inlen = in.length();
    if (inlen % 2 != 0)
        throw "input length not a multiple of 2";
    out.clear();
    out.reserve(inlen / 2);
    for (string::const_iterator p = in.begin(); p != in.end(); p++)
    {
       unsigned char c = hexval(*p);
       p++;
       c = (c << 4) + hexval(*p);
       out.push_back(c);
    }
}

void hex2ascii_2(const string& in, string& out)
{
    size_t inlen = in.length();
    if (inlen % 2 != 0)
        throw "input length not a multiple of 2";
    out.clear();
    out.reserve(inlen / 2);
    std::transform(in.begin(), in.end() - 1, in.begin() + 1,
                   std::back_inserter(out),
                   [](unsigned char a, unsigned char b)
                   { return (hexval(a) << 4) + hexval(b); });
}

It seems to me that both of these should be optimizable to the equivalent thing you would write in C, with all the pointers in registers ...

void hex2ascii_hypothetical(const string& in, string& out)
{
    size_t inlen = in.length();
    if (inlen % 2 != 0)
        throw "input length not a multiple of 2";
    out.clear();
    out.reserve(inlen / 2);

    const unsigned char *p = in._M_data();
    const unsigned char *limit = p + in._M_length();
    unsigned char *q = out._M_data();
    // (check for pointer wrap-around here?)

    while (p < limit)
    {
        *q++ = (hexval(p[0]) << 4) + hexval(p[1]);
        p += 2;
    }
}

Maybe it wouldn't be able to deduce that capacity overflow is impossible by construction, but that's a detail.  The important thing is that g++ 5 and 6 cannot hoist the pointer initializations out of the loop as shown.  They reload p, limit, and q from memory (that is, from the relevant string objects) on every iteration.


---


### compiler : `gcc`
### title : `optimization goes astray and adds completely redundant code`
### open_at : `2016-03-17T12:30:01Z`
### last_modified_date : `2021-11-29T07:13:51Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70274
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `5.2.0`
### severity : `normal`
### contents :
here is c code that demonstrates the problem:

double x;
unsigned n;
void foo() {
	while (n > 8) {
		n -= 8;
		x *= 3.0;
	}
}

compiled with options: -O2 -fomit-frame-pointer -quiet -ffast-math -march=core2

then observe the result assembly (i will paste part of it here for convenience):
....
_foo:
	movl	_n, %edx
	cmpl	$8, %edx
	jbe	L1
	movsd	_x, %xmm0
	movl	%edx, %eax
	movsd	LC0, %xmm1
	.p2align 4,,10
L3:
	mulsd	%xmm1, %xmm0
	subl	$8, %eax
	cmpl	$8, %eax
	ja	L3
	leal	-9(%edx), %eax  // redundant code
	subl	$8, %edx        // redundant code
	movsd	%xmm0, _x
	andl	$-8, %eax       // redundant code
	subl	%eax, %edx      // redundant code
	movl	%edx, _n
L1:
	ret
...

Apparently GCC notices opportunity for strength-reduction (or something else, i'm not sure what) about the variable n and produces code that directly calculates n without the need of the loop (the instructions i marked with "redundant code").

But GCC fails to consider that the loop is run anyway (because it has other effects besides calculating n, which can't be strength-reduced).
So after the end of the loop, the final value of n is already available, but GCC decides to discard it and re-calculates it again by means of the witty "strength-reduced" code. That is completely redundant.


---


### compiler : `gcc`
### title : `Improve code generation for large initializer lists`
### open_at : `2016-03-17T14:53:34Z`
### last_modified_date : `2023-01-19T06:21:48Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70277
### status : `NEW`
### tags : `compile-time-hog, missed-optimization`
### component : `c++`
### version : `6.0`
### severity : `enhancement`
### contents :
#include <string>
#include <vector>

#define T10 "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
#define T100 T10, T10, T10, T10, T10, T10, T10, T10, T10, T10
#define T1000 T100, T100, T100, T100, T100, T100, T100, T100, T100, T100
#define T10000 T1000, T1000, T1000, T1000, T1000, T1000, T1000, T1000, T1000, T1000
#define T100000 T10000, T10000, T10000, T10000, T10000, T10000, T10000, T10000, T10000, T10000

int
main ()
{
  std::vector<std::string> v {
    T100000, T100000
  };
}

ICEs during GC, 200000 nested try {} finally {} gimple stmts is just too much for typical stack size limits.

Perhaps the compiler should find out that all initializers (over certain threshold, perhaps --param?) are the same type and need to be constructed the same (or at least significant range of them, e.g. if there are 1000 constant string literals, then one other initializer that needs another kind of constructor, then 10000 other initializers that need yet another kind), and expand it as a loop over some const POD array instead of emitting huge spaghetti code?


---


### compiler : `gcc`
### title : `memset generates rep stosl instead of rep stosq`
### open_at : `2016-03-19T08:36:24Z`
### last_modified_date : `2021-07-24T05:46:54Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70308
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `5.2.1`
### severity : `minor`
### contents :
Consider this program:

=============================
#include <string.h>
#include <stdio.h>
#include <unistd.h>

int main() {
    char buf[128];
    if (scanf("%s", buf) != 1)   return 42;
    memset(buf,0, 128);
    asm volatile("": : :"memory");
    return 0;
}
==============================
compile with -O3

and you will see, that memset is translated to "rep stosl". good.

Next, comment line with scanf() and compile again

and you will see, that memset is translated to "rep stosq", which is much faster.

So, I consider that gcc should emit "rep stosq" in both cases.


---


### compiler : `gcc`
### title : `AVX512 not using kandw to combine comparison results`
### open_at : `2016-03-19T16:28:02Z`
### last_modified_date : `2020-08-06T06:16:39Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70314
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `6.0`
### severity : `enhancement`
### contents :
This comes from PR 68714 (comment 7), there are more details and suggestions there.

typedef int T __attribute__((vector_size(64)));
T f(T a,T b,T c,T d){
  return (a<b)&(c<d);
}

we generate (-march=skylake-avx512):

  _3 = VEC_COND_EXPR <a_1(D) < b_2(D), { -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 }, { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }>;
  _6 = VEC_COND_EXPR <c_4(D) < d_5(D), { -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 }, { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }>;
  _7 = _3 & _6;
  return _7;

yielding this code:

        vpcmpgtd        %zmm0, %zmm1, %k1
        vpternlogd      $0xFF, %zmm4, %zmm4, %zmm4
        vmovdqa32       %zmm4, %zmm0{%k1}{z}
        vpcmpgtd        %zmm2, %zmm3, %k1
        vmovdqa32       %zmm4, %zmm2{%k1}{z}
        vpandd  %zmm2, %zmm0, %zmm0

We perform the bit_and on the mask type, whereas it would be better to do it on the vector boolean type and use 'kandw'.


---


### compiler : `gcc`
### title : `FAIL: gcc.dg/tree-ssa/sra-17.c scan-tree-dump-times esra`
### open_at : `2016-03-19T18:57:27Z`
### last_modified_date : `2022-05-27T08:03:46Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70315
### status : `UNCONFIRMED`
### tags : `missed-optimization, testsuite-fail`
### component : `tree-optimization`
### version : `6.0`
### severity : `normal`
### contents :
Created attachment 38030
Tree dump

Executing on host: /test/gnu/gcc/objdir/gcc/xgcc -B/test/gnu/gcc/objdir/gcc/ /te
st/gnu/gcc/gcc/gcc/testsuite/gcc.dg/tree-ssa/sra-17.c   -fno-diagnostics-show-ca
ret -fdiagnostics-color=never   -O2 -fdump-tree-esra --param sra-max-scalarizati
on-size-Ospeed=32  -lm    -o ./sra-17.exe    (timeout = 300)
spawn /test/gnu/gcc/objdir/gcc/xgcc -B/test/gnu/gcc/objdir/gcc/ /test/gnu/gcc/gc
c/gcc/testsuite/gcc.dg/tree-ssa/sra-17.c -fno-diagnostics-show-caret -fdiagnosti
cs-color=never -O2 -fdump-tree-esra --param sra-max-scalarization-size-Ospeed=32
 -lm -o ./sra-17.exe
PASS: gcc.dg/tree-ssa/sra-17.c (test for excess errors)
Setting LD_LIBRARY_PATH to :/test/gnu/gcc/objdir/gcc:/test/gnu/gcc/objdir/hppa64
-hp-hpux11.11/./libatomic/.libs::/test/gnu/gcc/objdir/gcc:/test/gnu/gcc/objdir/h
ppa64-hp-hpux11.11/./libatomic/.libs
spawn [open ...]
PASS: gcc.dg/tree-ssa/sra-17.c execution test
FAIL: gcc.dg/tree-ssa/sra-17.c scan-tree-dump-times esra "Removing load: a = \\*
.?L.?C.?.?.?0;" 1
FAIL: gcc.dg/tree-ssa/sra-17.c scan-tree-dump-times esra "SR\\.[0-9_]+ = \\*.?L.
?C.?.?.?0\\[" 4

Load is not removed on hppa64.

Similar fails:

FAIL: gcc.dg/tree-ssa/sra-18.c scan-tree-dump-times esra "Removing load: a = \\*
.?L.?C.?.?.?0;" 1
FAIL: gcc.dg/tree-ssa/sra-18.c scan-tree-dump-times esra "SR\\.[0-9_]+ = \\*.?L.
?C.?.?.?0\\.b\\[0\\]\\.f\\[0\\]\\.x" 1
FAIL: gcc.dg/tree-ssa/sra-18.c scan-tree-dump-times esra "SR\\.[0-9_]+ = \\*.?L.
?C.?.?.?0\\.b\\[0\\]\\.f\\[1\\]\\.x" 1
FAIL: gcc.dg/tree-ssa/sra-18.c scan-tree-dump-times esra "SR\\.[0-9_]+ = \\*.?L.
?C.?.?.?0\\.b\\[1\\]\\.f\\[0\\]\\.x" 1
FAIL: gcc.dg/tree-ssa/sra-18.c scan-tree-dump-times esra "SR\\.[0-9_]+ = \\*.?L.
?C.?.?.?0\\.b\\[1\\]\\.f\\[1\\]\\.x" 1

Again no load is removed, etc.

Tests work on 32-bit hppa.


---


### compiler : `gcc`
### title : `[10/11/12/13 Regression] STV generates less optimized code`
### open_at : `2016-03-20T14:40:52Z`
### last_modified_date : `2022-06-04T09:12:26Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70321
### status : `RESOLVED`
### tags : `deferred, missed-optimization, patch`
### component : `target`
### version : `6.0`
### severity : `normal`
### contents :
[hjl@gnu-tools-1 bitwise-1]$ cat z.i
void
foo (long long ixi)
{
  if (ixi != 14348907)
    __builtin_abort ();
}
[hjl@gnu-tools-1 bitwise-1]$ make z.s z1.s
/export/build/gnu/gcc/build-x86_64-linux/gcc/xgcc -B/export/build/gnu/gcc/build-x86_64-linux/gcc/ -O2 -m32 -S -o z.s z.i
/export/build/gnu/gcc/build-x86_64-linux/gcc/xgcc -B/export/build/gnu/gcc/build-x86_64-linux/gcc/ -O2 -m32 -mno-stv -S -o z1.s z.i
[hjl@gnu-tools-1 bitwise-1]$ cat z.s
	.file	"z.i"
	.text
	.p2align 4,,15
	.globl	foo
	.type	foo, @function
foo:
.LFB0:
	.cfi_startproc
	subl	$12, %esp
	.cfi_def_cfa_offset 16
	movl	20(%esp), %edx
	movl	16(%esp), %eax
	xorb	$0, %dh
	xorl	$14348907, %eax
	movl	%edx, %ecx
	orl	%eax, %ecx
	jne	.L5
	addl	$12, %esp
	.cfi_remember_state
	.cfi_def_cfa_offset 4
	ret
.L5:
	.cfi_restore_state
	call	abort
	.cfi_endproc
.LFE0:
	.size	foo, .-foo
	.ident	"GCC: (GNU) 6.0.0 20160318 (experimental)"
	.section	.note.GNU-stack,"",@progbits
[hjl@gnu-tools-1 bitwise-1]$ cat z1.s
	.file	"z.i"
	.text
	.p2align 4,,15
	.globl	foo
	.type	foo, @function
foo:
.LFB0:
	.cfi_startproc
	subl	$12, %esp
	.cfi_def_cfa_offset 16
	movl	16(%esp), %eax
	xorl	$14348907, %eax
	orl	20(%esp), %eax
	jne	.L5
	addl	$12, %esp
	.cfi_remember_state
	.cfi_def_cfa_offset 4
	ret
.L5:
	.cfi_restore_state
	call	abort
	.cfi_endproc
.LFE0:
	.size	foo, .-foo
	.ident	"GCC: (GNU) 6.0.0 20160318 (experimental)"
	.section	.note.GNU-stack,"",@progbits
[hjl@gnu-tools-1 bitwise-1]$ 

STV generates:

	movl	20(%esp), %edx
	movl	16(%esp), %eax
	xorb	$0, %dh
	xorl	$14348907, %eax
	movl	%edx, %ecx
	orl	%eax, %ecx

vs

	movl	16(%esp), %eax
	xorl	$14348907, %eax
	orl	20(%esp), %eax


---


### compiler : `gcc`
### title : `STV doesn't optimize andn`
### open_at : `2016-03-20T15:25:11Z`
### last_modified_date : `2022-03-05T08:52:17Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70322
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `6.0`
### severity : `normal`
### contents :
i386.md has

(define_insn_and_split "*andndi3_doubleword"
  [(set (match_operand:DI 0 "register_operand" "=r,r")
        (and:DI
          (not:DI (match_operand:DI 1 "register_operand" "r,r"))
          (match_operand:DI 2 "nonimmediate_operand" "r,m")))
   (clobber (reg:CC FLAGS_REG))]
  "TARGET_BMI && !TARGET_64BIT && TARGET_STV && TARGET_SSE"
  "#"

But it is never used:

[hjl@gnu-tools-1 bitwise-1]$ cat andn.i
extern long long z;

void
foo (long long x, long long y)
{
  z = ~x & y;
}
[hjl@gnu-tools-1 bitwise-1]$ /export/build/gnu/gcc/build-x86_64-linux/gcc/xgcc -B/export/build/gnu/gcc/build-x86_64-linux/gcc/ -O2 -m32 -S  andn.i -fno-asynchronous-unwind-tables
[hjl@gnu-tools-1 bitwise-1]$ cat andn.s
	.file	"andn.i"
	.text
	.p2align 4,,15
	.globl	foo
	.type	foo, @function
foo:
	movl	4(%esp), %ecx
	notl	%ecx
	movl	%ecx, %eax
	movl	8(%esp), %ecx
	andl	12(%esp), %eax
	notl	%ecx
	movl	%ecx, %edx
	andl	16(%esp), %edx
	movl	%eax, z
	movl	%edx, z+4
	ret
	.size	foo, .-foo
	.ident	"GCC: (GNU) 6.0.0 20160318 (experimental)"
	.section	.note.GNU-stack,"",@progbits
[hjl@gnu-tools-1 bitwise-1]$


---


### compiler : `gcc`
### title : `[11/12/13/14 Regression] cost model for addresses is incorrect, slsr is using reg + reg + CST for arm`
### open_at : `2016-03-21T16:57:41Z`
### last_modified_date : `2023-07-07T10:31:15Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70341
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `5.3.0`
### severity : `normal`
### contents :
Created attachment 38049
test_switch.c

Starting with GCC-4.9.x suboptimal code is generated for this switch-statement.
Toolchain arm-none-eabi.

extern void handle_case_1(int name);
extern void handle_case_2(int name);
extern void handle_case_3(int name);
extern void handle_case_4(int name);

struct item_s
{
  int index;
  int type;
  int name;
  int data;
};

struct table_s
{
  struct item_s items[1];
};

void test(struct table_s *table, int xi)
{
  struct item_s *item = &(table->items[xi]);
  switch (item->type)
    {
    case 1:
      handle_case_1(item->name);
      break;
    case 2:
      handle_case_2(item->name);
      break;
    case 3:
      handle_case_3(item->name);
      break;
    case 4:
      handle_case_4(item->name);
      break;
    }
}

Compiled with gcc-4.6.x, gcc-4.7.x, gcc-4.8.x:

00000000 <test>:
   0:   eb00 1101       add.w   r1, r0, r1, lsl #4
   4:   684b            ldr     r3, [r1, #4]
   6:   3b01            subs    r3, #1
   8:   2b03            cmp     r3, #3
   a:   d80f            bhi.n   2c <test+0x2c>
   c:   e8df f003       tbb     [pc, r3]
  10:   0b080502        bleq    201420 <test+0x201420>
  14:   6888            ldr     r0, [r1, #8]
  16:   f7ff bffe       b.w     0 <handle_case_1>
  1a:   6888            ldr     r0, [r1, #8]
  1c:   f7ff bffe       b.w     0 <handle_case_2>
  20:   6888            ldr     r0, [r1, #8]
  22:   f7ff bffe       b.w     0 <handle_case_3>
  26:   6888            ldr     r0, [r1, #8]
  28:   f7ff bffe       b.w     0 <handle_case_4>
  2c:   4770            bx      lr

Compiled with 4.9.x, 5.3.0, and with current master:

00000000 <test>:
   0:   0109            lsls    r1, r1, #4
   2:   1843            adds    r3, r0, r1
   4:   685b            ldr     r3, [r3, #4]
   6:   3b01            subs    r3, #1
   8:   2b03            cmp     r3, #3
   a:   d813            bhi.n   34 <test+0x34>
   c:   e8df f003       tbb     [pc, r3]
  10:   0e0a0602        cfmadd32eq      mvax0, mvfx0, mvfx10, mvfx2
  14:   4408            add     r0, r1
  16:   6880            ldr     r0, [r0, #8]
  18:   f7ff bffe       b.w     0 <handle_case_1>
  1c:   4408            add     r0, r1
  1e:   6880            ldr     r0, [r0, #8]
  20:   f7ff bffe       b.w     0 <handle_case_2>
  24:   4408            add     r0, r1
  26:   6880            ldr     r0, [r0, #8]
  28:   f7ff bffe       b.w     0 <handle_case_3>
  2c:   4408            add     r0, r1
  2e:   6880            ldr     r0, [r0, #8]
  30:   f7ff bffe       b.w     0 <handle_case_4>
  34:   4770            bx      lr

Flags: -mcpu=cortex-m3
Both -Os and -O2 gives increased code size.


---


### compiler : `gcc`
### title : `[7/8/9 Regression] Code size increase for x86/ARM/others compared to gcc-5.3.0`
### open_at : `2016-03-22T13:49:11Z`
### last_modified_date : `2022-08-19T20:43:14Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70359
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `6.0`
### severity : `normal`
### contents :
Created attachment 38058
inttostr.c

Code size increase on master for ARM target compared to gcc-5.3.0
Target: arm-none-eabi
Flags: -Os -mcpu=arm966e-s -marm

gcc 5.3.0:

00000000 <inttostr>:
   0:   e3a03000        mov     r3, #0
   4:   e92d4070        push    {r4, r5, r6, lr}
   8:   e1a06000        mov     r6, r0
   c:   e2422001        sub     r2, r2, #1
  10:   e0205fc0        eor     r5, r0, r0, asr #31
  14:   e0455fc0        sub     r5, r5, r0, asr #31
  18:   e0814002        add     r4, r1, r2
  1c:   e7c13002        strb    r3, [r1, r2]
  20:   e1a00005        mov     r0, r5
  24:   e3a0100a        mov     r1, #10
  28:   ebfffffe        bl      0 <__aeabi_uidivmod>
  2c:   e2811030        add     r1, r1, #48     ; 0x30
  30:   e5641001        strb    r1, [r4, #-1]!
  34:   e1a00005        mov     r0, r5
  38:   e3a0100a        mov     r1, #10
  3c:   ebfffffe        bl      0 <__aeabi_uidiv>
  40:   e2505000        subs    r5, r0, #0
  44:   1afffff5        bne     20 <inttostr+0x20>
  48:   e3560000        cmp     r6, #0
  4c:   b3a0302d        movlt   r3, #45 ; 0x2d
  50:   b5443001        strblt  r3, [r4, #-1]
  54:   b2444001        sublt   r4, r4, #1
  58:   e1a00004        mov     r0, r4
  5c:   e8bd8070        pop     {r4, r5, r6, pc}


gcc-6-20160313 snapshot from master:

00000000 <inttostr>:
   0:   e3a03000        mov     r3, #0
   4:   e92d41f0        push    {r4, r5, r6, r7, r8, lr}
   8:   e1a07000        mov     r7, r0
   c:   e3a0800a        mov     r8, #10
  10:   e2422001        sub     r2, r2, #1
  14:   e0206fc0        eor     r6, r0, r0, asr #31
  18:   e0466fc0        sub     r6, r6, r0, asr #31
  1c:   e0815002        add     r5, r1, r2
  20:   e7c13002        strb    r3, [r1, r2]
  24:   e1a00006        mov     r0, r6
  28:   e1a01008        mov     r1, r8
  2c:   ebfffffe        bl      0 <__aeabi_uidivmod>
  30:   e2811030        add     r1, r1, #48     ; 0x30
  34:   e5451001        strb    r1, [r5, #-1]
  38:   e1a00006        mov     r0, r6
  3c:   e1a01008        mov     r1, r8
  40:   ebfffffe        bl      0 <__aeabi_uidiv>
  44:   e2506000        subs    r6, r0, #0
  48:   e2454001        sub     r4, r5, #1
  4c:   1a000005        bne     68 <inttostr+0x68>
  50:   e3570000        cmp     r7, #0
  54:   b3a0302d        movlt   r3, #45 ; 0x2d
  58:   b5443001        strblt  r3, [r4, #-1]
  5c:   b2454002        sublt   r4, r5, #2
  60:   e1a00004        mov     r0, r4
  64:   e8bd81f0        pop     {r4, r5, r6, r7, r8, pc}
  68:   e1a05004        mov     r5, r4
  6c:   eaffffec        b       24 <inttostr+0x24>


---


### compiler : `gcc`
### title : `reusing the same call-preserved register would give smaller code in some cases`
### open_at : `2016-03-25T07:35:11Z`
### last_modified_date : `2022-01-10T08:10:04Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70408
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `target`
### version : `6.0`
### severity : `enhancement`
### contents :
int foo(int);  // not inlineable
int bar(int a) {
  return foo(a+2) + 5 * foo (a);
}

gcc (and clang and icc) all make bigger code than necessary for x86.  gcc uses two call-preserved registers to save `a` and `foo(a+2)`.  Besides the extra push/pop, stack alignment requires a sub/add esp,8 pair.

Combining data-movement with arithmetic wherever possible is also a win (using lea), but gcc also misses out on that.

    # gcc6 snapshot 20160221 on godbolt (with -O3): http://goo.gl/dN5OXD
    pushq   %rbp
    pushq   %rbx
    movl    %edi, %ebx
    leal    2(%rdi), %edi      # why lea instead of add rdi,2?
    subq    $8, %rsp
    call    foo                # foo(a+2)
    movl    %ebx, %edi
    movl    %eax, %ebp
    call    foo                # foo(a)
    addq    $8, %rsp
    leal    (%rax,%rax,4), %eax
    popq    %rbx
    addl    %ebp, %eax
    popq    %rbp
    ret

clang 3.8 makes essentially the same code (but wastes an extra mov because it doesn't produce the result in %eax).

By hand, the best I can come up with is:

    push    %rbx
    lea     2(%rdi), %ebx          # stash ebx=a+2
    call    foo                    # foo(a)
    mov     %ebx, %edi
    lea     (%rax,%rax,4), %ebx    # reuse ebx to stash 5*foo(a)
    call    foo                    # foo(a+2)
    add     %ebx, %eax
    pop     %rbx
    ret

Note that I do the calls to foo() in the other order, which allows more folding of MOV into LEA.  The savings from that are somewhat orthogonal to the savings from reusing the same call-preserved register.

Should I open a separate bug report for the failure to optimize by reordering the calls?

I haven't tried to look closely at ARM or PPC code to see if they succeed at combining data movement with math (prob. worth testing with `foo(a) * 4` since x86's shift+add LEA is not widely available).  I didn't mark this as an i386/x86-64 but, because the reuse of call-preserved registers affects all architectures.


IDK if teaching gcc about either of these tricks would help with real code in many cases, or how hard it would be.


---


### compiler : `gcc`
### title : `Unnecessary "base object constructor" for final classes`
### open_at : `2016-03-30T15:29:27Z`
### last_modified_date : `2020-08-24T21:46:52Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70462
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `c++`
### version : `5.3.0`
### severity : `enhancement`
### contents :
g++ -std=c++11 -c -o t.o -x c++ - << EOF
struct Bar final
{
    Bar();
};
Bar::Bar()
{}
EOF
nm t.o

gives:

0000000000000000 T _ZN3BarC1Ev
0000000000000000 T _ZN3BarC2Ev

'_ZN3BarC2Ev' is the "base object constructor" and can never be called for 'final' classes, AFAICS.


---


### compiler : `gcc`
### title : `Useless "and [esp],-1" emitted on AND with uint64_t variable`
### open_at : `2016-03-30T18:59:28Z`
### last_modified_date : `2018-11-19T14:17:18Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70467
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `6.0`
### severity : `normal`
### contents :
Consider the following C code:

#include <string.h>
long double __attribute__((noinline)) test() { return 0; }

long double doStuff()
{
    long double value=test();
    unsigned long long v;
    memcpy(&v,&value,sizeof v);
    v&=~(1ull<<63);
    memcpy(&value,&v,sizeof v);
    return value;
}
int main(){}

I get the following output for duStuff() function when I compile this code with
`gcc -O3 -fomit-frame-pointer -m32`:


doStuff:
        sub     esp, 28
        call    test       ; OK, I asked to avoid inlining it
        fstp    TBYTE PTR [esp]
        and     DWORD PTR [esp], -1           ; DO NOTHING!!!
        and     DWORD PTR [esp+4], 2147483647 ; Clear highest bit
        fld     TBYTE PTR [esp]
        add     esp, 28
        ret


The instruction marked with `DO NOTHING!!!` is a no-op here (flags are not tested) and should have been eliminated.

This useless instruction is generated across generations of GCC starting at least with 4.4.7 and ending at 6.0.0 20160221 (the snapshot testable at gcc.godbolt.org).


---


### compiler : `gcc`
### title : `FMA is not reassociated causing x2 slowdown vs. ICC`
### open_at : `2016-03-31T13:23:20Z`
### last_modified_date : `2023-05-19T07:24:39Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70479
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `6.0`
### severity : `normal`
### contents :
Created attachment 38146
Reproducer

Attached example demonstrates the issue.
GCC is recent trunk. ICC is v16.

Compile:
  GCC: g++ -march=haswell -Ofast -flto -fopenmp-simd -fpermissive m.cpp -o m.gcc
  ICC: icpc -O3 -ipo -fpermissive -xAVX2 -qopenmp m.cpp -o m.icc

Run
  GCC: time ./m.icc 20000 20000
  ICC: time ./m.gcc 20000 20000

Hot spot generated by GCC (annotated w/ perf hit counts):
157 │8d0:┌─→vbroad 0x4(%r13),%zmm0
193 │    │  lea    0x1(%rdx),%edx
173 │    │  vmulps (%r14,%rax,1),%zmm0,%zmm0
2943│    │  vbroad 0x60(%r13),%zmm1
166 │    │  vbroad 0x5c(%r13),%zmm2
151 │    │  vbroad 0x58(%r13),%zmm3
144 │    │  vbroad 0x54(%r13),%zmm4
164 │    │  vbroad 0x50(%r13),%zmm5
170 │    │  vbroad 0x4c(%r13),%zmm6
162 │    │  vbroad 0x48(%r13),%zmm7
162 │    │  vbroad 0x44(%r13),%zmm8
154 │    │  vbroad 0x40(%r13),%zmm9
172 │    │  vbroad 0x3c(%r13),%zmm10
167 │    │  vbroad 0x38(%r13),%zmm11
172 │    │  vbroad 0x34(%r13),%zmm12
171 │    │  vbroad 0x30(%r13),%zmm13
161 │    │  vbroad 0x2c(%r13),%zmm14
176 │    │  vbroad 0x28(%r13),%zmm15
139 │    │  vbroad 0x24(%r13),%zmm16
180 │    │  vbroad 0x20(%r13),%zmm17
158 │    │  vbroad 0x1c(%r13),%zmm18
165 │    │  vbroad 0x18(%r13),%zmm19
140 │    │  vbroad 0x10(%r13),%zmm21
179 │    │  vbroad 0xc(%r13),%zmm22
146 │    │  vbroad 0x8(%r13),%zmm23
170 │    │  vbroad 0x0(%r13),%zmm24
170 │    │  vbroad 0x14(%r13),%zmm20
168 │    │  vfmadd (%r15,%rax,1),%zmm24,%zmm0
2732│    │  mov    0xb8(%rsp),%rcx
172 │    │  vfmadd (%r11,%rax,1),%zmm23,%zmm0
1649│    │  vfmadd (%rsi,%rax,1),%zmm22,%zmm0                                                                         3413│    │  vfmadd (%rcx,%rax,1),%zmm21,%zmm0                                                                         3653│    │  mov    0xc0(%rsp),%rcx                                                                                    182 │    │  vfmadd (%rcx,%rax,1),%zmm20,%zmm0
2806│    │  mov    0xc8(%rsp),%rcx
176 │    │  vfmadd (%rcx,%rax,1),%zmm19,%zmm0
2439│    │  mov    0xd0(%rsp),%rcx
179 │    │  vfmadd (%rcx,%rax,1),%zmm18,%zmm0
2562│    │  mov    0xd8(%rsp),%rcx
197 │    │  vfmadd (%rcx,%rax,1),%zmm17,%zmm0
2867│    │  mov    0xe0(%rsp),%rcx
141 │    │  vfmadd (%rcx,%rax,1),%zmm16,%zmm0
3200│    │  mov    0xe8(%rsp),%rcx
156 │    │  vfmadd (%rcx,%rax,1),%zmm15,%zmm0
3557│    │  mov    0xf0(%rsp),%rcx
158 │    │  vfmadd (%rcx,%rax,1),%zmm14,%zmm0
3333│    │  mov    0xf8(%rsp),%rcx
143 │    │  vfmadd (%rcx,%rax,1),%zmm13,%zmm0
3004│    │  mov    0x100(%rsp),%rcx
177 │    │  vfmadd (%rcx,%rax,1),%zmm12,%zmm0
2876│    │  mov    0x108(%rsp),%rcx
144 │    │  vfmadd (%rcx,%rax,1),%zmm11,%zmm0
2838│    │  mov    0x110(%rsp),%rcx
168 │    │  vfmadd (%rcx,%rax,1),%zmm10,%zmm0
2503│    │  mov    0x118(%rsp),%rcx
203 │    │  vfmadd (%rcx,%rax,1),%zmm9,%zmm0
2471│    │  mov    0x120(%rsp),%rcx
185 │    │  vfmadd (%rcx,%rax,1),%zmm8,%zmm0
2153│    │  mov    0x128(%rsp),%rcx
152 │    │  vfmadd (%r12,%rax,1),%zmm7,%zmm0
2091│    │  vfmadd (%rbx,%rax,1),%zmm6,%zmm0
3049│    │  vfmadd (%r10,%rax,1),%zmm5,%zmm0
3737│    │  vfmadd (%r9,%rax,1),%zmm4,%zmm0
3665│    │  vfmadd (%r8,%rax,1),%zmm3,%zmm0
3627│    │  vfmadd (%rdi,%rax,1),%zmm2,%zmm0
3804│    │  vfmadd (%rcx,%rax,1),%zmm1,%zmm0
4052│    │  mov    0x130(%rsp),%rcx
160 │    │  cmp    0x138(%rsp),%edx
534 │    │  vmovup %zmm0,(%rcx,%rax,1)
3235│    │  lea    0x40(%rax),%rax
161 │    └──jb     8d0

Hot spot generated by ICC (annotated w/ perf hit counts):
   344 │47a:┌─→vmulps 0x204c(%r11,%r14,4),%zmm27,%zmm2
   821 │    │  vmulps 0x2050(%r11,%r14,4),%zmm4,%zmm1
   318 │    │  vmulps 0x2040(%r11,%r14,4),%zmm6,%zmm29
   818 │    │  vmulps 0x1840(%r11,%r14,4),%zmm7,%zmm31
   275 │    │  vfmadd 0x1838(%r11,%r14,4),%zmm9,%zmm31
  1234 │    │  vfmadd 0x183c(%r11,%r14,4),%zmm8,%zmm29
   442 │    │  vfmadd 0x2044(%r11,%r14,4),%zmm5,%zmm2
  1110 │    │  vfmadd 0x2048(%r11,%r14,4),%zmm28,%zmm1
   337 │    │  vaddps %zmm29,%zmm31,%zmm0
  1047 │    │  vaddps %zmm1,%zmm2,%zmm3
   655 │    │  vmulps 0x1830(%r11,%r14,4),%zmm11,%zmm30
   956 │    │  vmulps 0x1834(%r11,%r14,4),%zmm10,%zmm2
   296 │    │  vmulps 0x1024(%r11,%r14,4),%zmm15,%zmm1
  1050 │    │  vmulps 0x1028(%r11,%r14,4),%zmm14,%zmm31
   294 │    │  vaddps %zmm0,%zmm3,%zmm3
  1057 │    │  vfmadd 0x102c(%r11,%r14,4),%zmm13,%zmm30
   344 │    │  vfmadd 0x1030(%r11,%r14,4),%zmm12,%zmm2
   911 │    │  vfmadd 0x1020(%r11,%r14,4),%zmm16,%zmm31
   332 │    │  vfmadd 0x820(%r11,%r14,4),%zmm17,%zmm1
   885 │    │  vaddps %zmm2,%zmm30,%zmm29
   486 │    │  vmulps 0x818(%r11,%r14,4),%zmm19,%zmm2
   837 │    │  vaddps %zmm31,%zmm1,%zmm30
   487 │    │  vmulps 0x81c(%r11,%r14,4),%zmm18,%zmm1
   851 │    │  vfmadd 0x810(%r11,%r14,4),%zmm21,%zmm2
   424 │    │  vfmadd 0x814(%r11,%r14,4),%zmm20,%zmm1
  1123 │    │  vaddps %zmm30,%zmm29,%zmm29
   389 │    │  vaddps %zmm1,%zmm2,%zmm31
  1372 │    │  vmulps 0xc(%r11,%r14,4),%zmm23,%zmm2
   311 │    │  vmulps 0x10(%r11,%r14,4),%zmm22,%zmm1
   916 │    │  vaddps %zmm29,%zmm3,%zmm3
   297 │    │  vfmadd (%r11,%r14,4),%zmm26,%zmm2
   795 │    │  vfmadd 0x8(%r11,%r14,4),%zmm24,%zmm1
   426 │    │  vaddps %zmm1,%zmm2,%zmm0
  1275 │    │  vmulps 0x208c(%r11,%r14,4),%zmm27,%zmm1
   364 │    │  vmulps 0x2080(%r11,%r14,4),%zmm6,%zmm30
  1061 │    │  vfmadd 0x4(%r11,%r14,4),%zmm25,%zmm0
   473 │    │  vfmadd 0x2084(%r11,%r14,4),%zmm5,%zmm1
  1106 │    │  vaddps %zmm31,%zmm0,%zmm2
   327 │    │  vmulps 0x2090(%r11,%r14,4),%zmm4,%zmm0
  1410 │    │  vmulps 0x1880(%r11,%r14,4),%zmm7,%zmm29
   274 │    │  vfmadd 0x2088(%r11,%r14,4),%zmm28,%zmm0
  1317 │    │  vaddps %zmm2,%zmm3,%zmm2
   364 │    │  vmulps 0x1874(%r11,%r14,4),%zmm10,%zmm3
  1196 │    │  vaddps %zmm0,%zmm1,%zmm31
   408 │    │  nop
     9 │    │  vmulps 0x1870(%r11,%r14,4),%zmm11,%zmm0
   374 │    │  vfmadd 0x1878(%r11,%r14,4),%zmm9,%zmm29
  1515 │    │  vfmadd 0x187c(%r11,%r14,4),%zmm8,%zmm30
   333 │    │  vfmadd 0x106c(%r11,%r14,4),%zmm13,%zmm0
  1728 │    │  vfmadd 0x1070(%r11,%r14,4),%zmm12,%zmm3
   306 │    │  vaddps %zmm30,%zmm29,%zmm1
  1778 │    │  vmulps 0x1064(%r11,%r14,4),%zmm15,%zmm29
   321 │    │  vaddps %zmm3,%zmm0,%zmm0
  1826 │    │  vmulps 0x1068(%r11,%r14,4),%zmm14,%zmm3
   347 │    │  vfmadd 0x860(%r11,%r14,4),%zmm17,%zmm29
  1562 │    │  vaddps %zmm1,%zmm31,%zmm1
   239 │    │  vfmadd 0x1060(%r11,%r14,4),%zmm16,%zmm3
  1600 │    │  vmulps 0x85c(%r11,%r14,4),%zmm18,%zmm30
   311 │    │  vaddps %zmm3,%zmm29,%zmm3
  1776 │    │  vmulps 0x858(%r11,%r14,4),%zmm19,%zmm29
   338 │    │  vfmadd 0x854(%r11,%r14,4),%zmm20,%zmm30
  1588 │    │  vfmadd 0x850(%r11,%r14,4),%zmm21,%zmm29
   292 │    │  vaddps %zmm3,%zmm0,%zmm0
  1331 │    │  vaddps %zmm30,%zmm29,%zmm31
   460 │    │  vmulps 0x4c(%r11,%r14,4),%zmm23,%zmm29
  1365 │    │  vmulps 0x50(%r11,%r14,4),%zmm22,%zmm30
   347 │    │  vaddps %zmm0,%zmm1,%zmm1
  1461 │    │  vfmadd 0x40(%r11,%r14,4),%zmm26,%zmm29
   489 │    │  vfmadd 0x48(%r11,%r14,4),%zmm24,%zmm30
  1583 │    │  vaddps %zmm30,%zmm29,%zmm30
   875 │    │  vfmadd 0x44(%r11,%r14,4),%zmm25,%zmm30
  1912 │    │  vmovup %zmm2,0x1028(%r13,%r14,4)
  1536 │    │  vaddps %zmm31,%zmm30,%zmm31
  1472 │    │  vaddps %zmm31,%zmm1,%zmm0
  1088 │    │  vmovup %zmm0,0x1068(%r13,%r14,4)
  1644 │    │  add    $0x20,%r14
   182 │    │  cmp    $0x200,%r14
    10 │    └──jb     47a


The issue is that we not doing rebalancing of FMA calculations.
This issue might be reproduced on Haswell as well, although because
of shorter vector perf difference is about 30%


---


### compiler : `gcc`
### title : `Missed fold for "(long int) x * 12 - (long int)(x + 1) * 12"`
### open_at : `2016-04-04T11:50:47Z`
### last_modified_date : `2021-12-25T08:51:09Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70527
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `6.0`
### severity : `enhancement`
### contents :
Given below test:
long unsigned int foo (int x)
{
  return (long unsigned int) x * 12 - (long unsigned int)(x + 1) * 12;
}

long int bar (int x)
{
  return (long int) x * 12 - (long int)(x + 1) * 12;
}
The 004t.gimple dump is like:
foo (int x)
{
  long unsigned int D.1762;

  D.1762 = 18446744073709551604;
  return D.1762;
}


bar (int x)
{
  long int D.1764;
  long int D.1765;
  long int D.1766;
  int D.1767;
  long int D.1768;
  long int D.1769;

  D.1765 = (long int) x;
  D.1766 = D.1765 * 12;
  D.1767 = x + 1;
  D.1768 = (long int) D.1767;
  D.1769 = D.1768 * -12;
  D.1764 = D.1766 + D.1769;
  return D.1764;
}


Seems "(long int) x * 12 - (long int)(x + 1) * 12" is missed in generic-simplify.


---


### compiler : `gcc`
### title : `ifconvert if(cond) ++count; to count += cond; fails because of mergephi and failed loop header copying`
### open_at : `2016-04-05T09:35:09Z`
### last_modified_date : `2023-05-05T06:59:24Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70546
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `6.0`
### severity : `enhancement`
### contents :
In the example from http://stackoverflow.com/q/36414959/1918193 we fail to vectorize f0 (using g++ -O3) because of the condition in the loop. However, if I manually change the condition as in the #else case, the vectorizer is happy and we get a very nice performance boost. Could ifconvert (or some other phi optimization pass) handle this transformation? n is a local variable, so we shouldn't even need -ftree-loop-if-convert-stores. At -O1, it is also a clear win with the random distribution, but it becomes a slight loss if the vector v is sorted in increasing order and a big loss for the decreasing order, so I don't know for sure under which condition this should be done.

#include <algorithm>
#include <chrono>
#include <random>
#include <iomanip>
#include <iostream>
#include <vector>

using namespace std;
using namespace std::chrono;

vector<int> v(1'000'000);

int f0()
{
  int n = 0;

  for (int i = 1; i < v.size()-1; ++i) {
    int a = v[i-1];
    int b = v[i];
    int c = v[i+1];

#ifndef IMPROVED
    if (a < b  &&  b < c) ++n;
#else
    n += (a < b  &&  b < c);
#endif
  }

  return n;
}


int f1()
{
  int n = 0;

  for (int i = 1; i < v.size()-1; ++i)
    if (v[i-1] < v[i]  &&  v[i] < v[i+1])
      ++n;

  return n;
}


int main()
{
  auto benchmark = [](int (*f)()) {
    const int N = 100;

    volatile long long result = 0;
    vector<long long>  timings(N);

    for (int i = 0; i < N; ++i) {
      auto t0 = high_resolution_clock::now();
      result += f();
      auto t1 = high_resolution_clock::now();

      timings[i] = duration_cast<nanoseconds>(t1-t0).count();
    }

    sort(timings.begin(), timings.end());
    cout << fixed << setprecision(6) << timings.front()/1'000'000.0 << "ms min\n";
    cout << timings[timings.size()/2]/1'000'000.0 << "ms median\n" << "Result: " << result/N << "\n\n";
  };

  mt19937                    generator   (31415);   // deterministic seed
  uniform_int_distribution<> distribution(0, 1023);

  for (auto& e: v)
    e = distribution(generator);

  benchmark(f0);
  benchmark(f1);

  cout << "\ndone\n";

  return 0;
}


---


### compiler : `gcc`
### title : `Optimize multiplication of booleans to bit_and`
### open_at : `2016-04-05T10:08:43Z`
### last_modified_date : `2022-11-26T06:51:46Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70547
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `6.0`
### severity : `enhancement`
### contents :
int f(int a,int b,int c,int d){
  return (a<b)*(c<d);
}

produces

  _3 = a_1(D) < b_2(D);
  _4 = (int) _3;
  _7 = c_5(D) < d_6(D);
  _8 = (int) _7;
  _9 = _4 * _8;
  return _9;

Since we know that _4 and _8 are in the range [0, 1], we could replace the multiplication with a cheaper AND.


---


### compiler : `gcc`
### title : `uint64_t zeroing on 32-bit hardware`
### open_at : `2016-04-05T23:40:05Z`
### last_modified_date : `2020-04-18T19:53:11Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70557
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `5.3.0`
### severity : `normal`
### contents :
Created attachment 38196
C source, gcc 5.3.0 assembly output, IDA Pro disassembly

This is C with gcc 5.3.0 targeting the MCF5272 coldfire (m68k w/o alignment constraint).

To clear 8 bytes of memory, gcc should always issue a pair of clr.L instructions. 

This applies both when the address is known to the linker (the address should be contained in an instruction that loads an address register) and when the address is supplied as a function argument (the address should be loaded into a register which the clr.L will then use).

Because the hardware is 32-bit, a 64-bit value should be handled the same as a pair of 32-bit values. Because there is no alignment requirement, 8 adjacent 8-bit values (total of 64 bits) should likewise be handled the same.

All 6 cases (3 access sizes times 2 ways to address the data) are shown in the provided attachment. Only one of the 6 cases seems optimal, the one named "clear32p" which takes a pointer to a pair of 32-bit values as a function argument. The case named "clear32", referring to global data, isn't bad... but really the address should be loaded into an address register to save 2 bytes.

Though not the worst for performance (that honor going to the 8-bit functions), the 64-bit functions are particularly painful to look at. With these, gcc clears out two different registers and then moves both of them into memory. An obvious optimization would be to clear only a single register and use it twice. Another obvious optimization would be to directly clear the memory via a clr.L that uses memory addressing, either absolute or register-based as appropriate, though loading an address register is even better.

In any case, the 6 functions in this example should compile to 2 distinct kinds of result. The access size should not change the resulting assembly.


---


### compiler : `gcc`
### title : `Missed tree optimization with multiple additions in different types.`
### open_at : `2016-04-08T14:21:03Z`
### last_modified_date : `2020-05-15T03:53:36Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70600
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `6.0`
### severity : `enhancement`
### contents :
The following is a testcase reduced from a Linux kernel file. Compile with -O2 on x86_64-linux.

There are two additions, the first in type unsigned long, the second one after casting the first result to unsigned int. Together, they end up as a no-op, but this is not caught during tree optimization. The combiner finally manages to eliminate them, with the help of a note added by fwprop.

(I was looking at whether we could eliminate the creation of REG_EQUAL notes from fwprop, and found only three cases out of a set of 4492 source files where they changed code generation; this was one of them.)

int p (long mem_map, long page, unsigned int *p, unsigned int *frag)
{
  
  unsigned int _83 = *p;
  long _142 = page - mem_map;
  long _143 = _142 / 56;
  unsigned long _144 = _143;
  unsigned long _145 = _144 << 12;
  unsigned long _146 = _145 + 0xc0000000;
  unsigned int _147 = _146;
  unsigned int _190 = _83 + 0x40000000;
  unsigned int _149 = _147 + _190;
  return _149;
}


---


### compiler : `gcc`
### title : `SLP vectorization opportunity to use load element + splat`
### open_at : `2016-04-14T14:23:34Z`
### last_modified_date : `2019-08-30T12:24:39Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70666
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `6.0`
### severity : `normal`
### contents :
As discussed in PR70130, there is an opportunity to produce better code during SLP vectorization for a vector load with a permutation vector where all elements of the permutation are identical.  A load of the desired element and a splat would be better than current generated code, which makes use of unaligned loads.  See https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70130#c23 for details, and see https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70130#c11 for a test case that can be used to reproduce the pattern.


---


### compiler : `gcc`
### title : `suboptimal code generation on AVR`
### open_at : `2016-04-15T08:50:31Z`
### last_modified_date : `2022-02-24T18:06:07Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70676
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `5.3.1`
### severity : `normal`
### contents :
gcc -Os -fno-optimize-sibling-calls

don't optimizes out tail recursion:

return SPI::transfer(0xff);
     f54:8f ef       ldi r24, 0xFF; 255
     f56:0e 94 d9 2e call 0x5db2 ; 0x5db2 <_ZN3SPI8transferEh>
}
     f5a:08 95       ret

where it should be 
     ldi r24, 0xFF; 255
     jmp  0x5db2 ; 0x5db2 <_ZN3SPI8transferEh>

Yes I can remove -fno-optimize-sibling-calls but then size of compiled project will be much more:

with:    30566 bytes (93.3% Full)
without: 30772 bytes and binary don't fit to flash (30720 is maximum)

Reason is that even with -Os optimize-sibling-calls tries to make epilogue for each tail recursion:


    2080:<----->92 e0       <-->ldi<--->r25, 0x02<----->; 2
    2082:<----->df 91       <-->pop<--->r29
    2084:<----->cf 91       <-->pop<--->r28
    2086:<----->1f 91       <-->pop<--->r17
    2088:<----->0f 91       <-->pop<--->r16
    208a:<----->ff 90       <-->pop<--->r15
    208c:<----->ef 90       <-->pop<--->r14
    208e:<----->bf 90       <-->pop<--->r11
    2090:<----->af 90       <-->pop<--->r10
    2092:<----->9f 90       <-->pop<--->r9
    2094:<----->8f 90       <-->pop<--->r8
    2096:<----->0c 94 2a 0f <-->jmp<--->0x1e54<>; 0x1e54 <_ZL12osd_printf_1PKcf>
(rjmp here)
    209a:<----->df 91       <-->pop<--->r29
    209c:<----->cf 91       <-->pop<--->r28
    209e:<----->1f 91       <-->pop<--->r17
    20a0:<----->0f 91       <-->pop<--->r16
    20a2:<----->ff 90       <-->pop<--->r15
    20a4:<----->ef 90       <-->pop<--->r14
    20a6:<----->bf 90       <-->pop<--->r11
    20a8:<----->af 90       <-->pop<--->r10
    20aa:<----->9f 90       <-->pop<--->r9
    20ac:<----->8f 90       <-->pop<--->r8
    20ae:<----->08 95       <-->ret

Can GCC in -Os really optimize only size and rollback optimizations if size of "optimized" code is more than size of non-optimized ?


---


### compiler : `gcc`
### title : `[7/8/9 Regression] FAIL: gcc.dg/ira-shrinkwrap-prep-2.c  gcc.dg/pr10474.c on arm and powerpc`
### open_at : `2016-04-15T11:37:34Z`
### last_modified_date : `2018-11-20T14:36:27Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70681
### status : `RESOLVED`
### tags : `missed-optimization, patch`
### component : `rtl-optimization`
### version : `6.0`
### severity : `normal`
### contents :
As reported at:
https://gcc.gnu.org/ml/gcc-patches/2016-03/msg01640.html
and
https://gcc.gnu.org/ml/gcc-patches/2016-04/msg00094.html

The tests:
  gcc.dg/ira-shrinkwrap-prep-2.c scan-rtl-dump pro_and_epilogue
"Performing shrink-wrapping"
  gcc.dg/pr10474.c scan-rtl-dump pro_and_epilogue "Performing shrink-wrapping"

Have started failing on arm and powerpc after a regalloc change.
On arm at least the resulting codegen doesn't look worse
(https://gcc.gnu.org/ml/gcc-patches/2016-04/msg00223.html)

but arguably shrink-wrapping could be improved (https://gcc.gnu.org/ml/gcc-patches/2016-04/msg00265.html)

This is a report to track work on shrinkwrapping or adjustment of the testscases


---


### compiler : `gcc`
### title : `Suboptimal code generated when using _mm_min_sd`
### open_at : `2016-04-19T00:34:36Z`
### last_modified_date : `2021-08-02T23:17:46Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70721
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `7.0`
### severity : `enhancement`
### contents :
_mm_min_sd is implemented as

(define_insn "<sse>_vm<code><mode>3<round_saeonly_name>"
  [(set (match_operand:VF_128 0 "register_operand" "=x,v")
        (vec_merge:VF_128
          (smaxmin:VF_128
            (match_operand:VF_128 1 "register_operand" "0,v")
            (match_operand:VF_128 2 "vector_operand" "xBm,<round_saeonly_constraint>"))
         (match_dup 1)
         (const_int 1)))] 

The problem is smaxmin is applied to the full 128-bit operand.
Can we change it to apply only to the first 64-bit of operand
so that we can remove 2 xmm moves in

---
#include <emmintrin.h>

double
__attribute ((noinline, noclone))
foo (double a, double b)
{
   __m128d x = _mm_set_sd(a);
   __m128d y = _mm_set_sd(b);
   return _mm_cvtsd_f64(_mm_min_sd(x, y));
}
---


---


### compiler : `gcc`
### title : `Missed optimization opportunity for lambda converted to fun-ptr`
### open_at : `2016-04-19T08:15:43Z`
### last_modified_date : `2021-12-25T12:20:12Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70723
### status : `NEW`
### tags : `missed-optimization`
### component : `c++`
### version : `6.0`
### severity : `enhancement`
### contents :
Hi,

the following code gets properly optimized-out if erasedTypeVTable is initialized with &dtor<T> (case [2]), but it is not optimized if initialized with lambda (case [1]).

#include <type_traits>
#include <new>

namespace
{
struct ErasedTypeVTable
{
   using destructor_t = void (*)(void *obj);

   destructor_t dtor;
};

template <typename T>
void dtor(void *obj)
{
   return static_cast<T *>(obj)->~T();
}

template <typename T>
static const ErasedTypeVTable erasedTypeVTable = {
  /* 1 */  [] (void *obj) { return static_cast<T *>(obj)->~T(); }
  /* 2 */ // &dtor<T>
};
struct myType
{
   int a;
};

void meow()
{
   std::aligned_storage<sizeof(myType)>::type storage;
   auto *ptr = new ((char *)(&storage)) myType{5};

   ptr->a = 10;

   erasedTypeVTable<myType>.dtor(ptr);
}

}

int main()
{
   meow();
}

Compiled with -O3 -std=c++14 flags.

g++ --version:
g++ (Ubuntu 6-20160405-0ubuntu1) 6.0.0 20160405 (experimental) [trunk revision 234749]

FWIW, clang 3.8 optimizes both versions.


---


### compiler : `gcc`
### title : `Support div as a builtin`
### open_at : `2016-04-20T21:29:46Z`
### last_modified_date : `2021-06-03T10:20:57Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70742
### status : `NEW`
### tags : `missed-optimization`
### component : `c`
### version : `6.0`
### severity : `enhancement`
### contents :
Created attachment 38318
example with disassembly listing

This idea has been originated here
https://sourceware.org/ml/libc-alpha/2016-04/msg00503.html
and later from here
https://sourceware.org/bugzilla/show_bug.cgi?id=19974

Due to suggestions in both the libc-alpha mailing list and in the glibc issue tracker, I created this issue here as a compiler enhencement.

Basically the idea is to create the __builtin_div builtins family, so they finally get translated to a single asm insn (if available) that calculates both the quotient and the remainder. I attach the same file that is attached in the glibc's bug tracker.

The goal is that std::div and cstdlib's div can be reimplemented as calling this builtin.


---


### compiler : `gcc`
### title : `[ARM] excessive struct alignment for globals`
### open_at : `2016-04-21T16:34:42Z`
### last_modified_date : `2021-11-29T01:06:52Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70755
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `5.3.1`
### severity : `enhancement`
### contents :
Discussion at the end

$ arm-none-eabi-g++.exe -std=c++11 -Ofast -c align_foo.cpp -S -fdata-sections

$ cat align_foo.cpp

struct S
{
    bool val;
};

S s1;			// 32 bit align
alignas(S) S s2;	// 8 bit align

struct alignas(bool) SA
{
    bool val;
};

struct alignas(long long) SB
{
    bool val;
};

SA sa;			// 32 bit align
SB sb;			// 64 bit align


$ cat align_foo.s
	.cpu arm7tdmi
	.fpu softvfp
	.eabi_attribute 23, 1
	.eabi_attribute 24, 1
	.eabi_attribute 25, 1
	.eabi_attribute 26, 1
	.eabi_attribute 30, 2
	.eabi_attribute 34, 0
	.eabi_attribute 18, 4
	.arm
	.syntax divided
	.file	"align_foo.cpp"
	.global	sb
	.global	sa
	.global	s2
	.global	s1
	.section	.bss.s1,"aw",%nobits
	.align	2
	.type	s1, %object
	.size	s1, 1
s1:
	.space	1
	.section	.bss.s2,"aw",%nobits
	.type	s2, %object
	.size	s2, 1
s2:
	.space	1
	.section	.bss.sa,"aw",%nobits
	.align	2
	.type	sa, %object
	.size	sa, 1
sa:
	.space	1
	.section	.bss.sb,"aw",%nobits
	.align	3
	.type	sb, %object
	.size	sb, 8
sb:
	.space	8
	.ident	"GCC: (GNU Tools for ARM Embedded Processors) 5.3.1 20160307 (release) [ARM/embedded-5-branch revision 234589]"

---

The code comments show how the respective variable was aligned in the assembly output.

a) s1 should be byte aligned.

b) alignas works around the problem but only for s2 but not SA. Even though the compiler clearly accepts the alignment increase for SB.

c) sb blocks 8 bytes, rather then just being 8 byte aligned


"-fdata-sections" is for clarity, without it we get basically the same, although for sa the alignment could be unintentional:

	...

	.bss
	.align	3
	.type	sb, %object
	.size	sb, 8
sb:
	.space	8
	.type	sa, %object
	.size	sa, 1
sa:
	.space	1
	.type	s2, %object
	.size	s2, 1
s2:
	.space	1
	.space	2
	.type	s1, %object
	.size	s1, 1
s1:
	.space	1


---


### compiler : `gcc`
### title : `Use SSE for DImode load/store`
### open_at : `2016-04-22T14:30:27Z`
### last_modified_date : `2022-01-11T10:29:03Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70763
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `7.0`
### severity : `enhancement`
### contents :
On i386, we should use SSE for DImode load/store:

[hjl@gnu-6 pr70155d]$ cat x1.i
extern long long a, b;

void
foo (void)
{
  a = b;
}
[hjl@gnu-6 pr70155d]$ cat x2.i
struct foo
{
  long long i;
}__attribute__ ((packed));

extern struct foo x, y;

void
foo (void)
{
  x = y;
}
[hjl@gnu-6 pr70155d]$ cat x5.i
extern long long a;

void
foo (void)
{
  a = 0;
}
[hjl@gnu-6 pr70155d]$ cat x6.i
extern long long a;

void
foo (void)
{
  a = -1;
}
[hjl@gnu-6 pr70155d]$ make x1.s x2.s x5.s x6.s
/export/build/gnu/gcc/build-x86_64-linux/gcc/xgcc -B/export/build/gnu/gcc/build-x86_64-linux/gcc/ -O2 -msse2 -m32 -fno-asynchronous-unwind-tables -S -o x1.s x1.i
/export/build/gnu/gcc/build-x86_64-linux/gcc/xgcc -B/export/build/gnu/gcc/build-x86_64-linux/gcc/ -O2 -msse2 -m32 -fno-asynchronous-unwind-tables -S -o x2.s x2.i
/export/build/gnu/gcc/build-x86_64-linux/gcc/xgcc -B/export/build/gnu/gcc/build-x86_64-linux/gcc/ -O2 -msse2 -m32 -fno-asynchronous-unwind-tables -S -o x5.s x5.i
/export/build/gnu/gcc/build-x86_64-linux/gcc/xgcc -B/export/build/gnu/gcc/build-x86_64-linux/gcc/ -O2 -msse2 -m32 -fno-asynchronous-unwind-tables -S -o x6.s x6.i
[hjl@gnu-6 pr70155d]$ cat  x1.s x2.s x5.s x6.s
	.file	"x1.i"
	.text
	.p2align 4,,15
	.globl	foo
	.type	foo, @function
foo:
	movl	b, %eax
	movl	b+4, %edx
	movl	%eax, a
	movl	%edx, a+4
	ret
	.size	foo, .-foo
	.ident	"GCC: (GNU) 7.0.0 20160422 (experimental)"
	.section	.note.GNU-stack,"",@progbits
	.file	"x2.i"
	.text
	.p2align 4,,15
	.globl	foo
	.type	foo, @function
foo:
	movl	y, %eax
	movl	y+4, %edx
	movl	%eax, x
	movl	%edx, x+4
	ret
	.size	foo, .-foo
	.ident	"GCC: (GNU) 7.0.0 20160422 (experimental)"
	.section	.note.GNU-stack,"",@progbits
	.file	"x5.i"
	.text
	.p2align 4,,15
	.globl	foo
	.type	foo, @function
foo:
	movl	$0, a
	movl	$0, a+4
	ret
	.size	foo, .-foo
	.ident	"GCC: (GNU) 7.0.0 20160422 (experimental)"
	.section	.note.GNU-stack,"",@progbits
	.file	"x6.i"
	.text
	.p2align 4,,15
	.globl	foo
	.type	foo, @function
foo:
	movl	$-1, a
	movl	$-1, a+4
	ret
	.size	foo, .-foo
	.ident	"GCC: (GNU) 7.0.0 20160422 (experimental)"
	.section	.note.GNU-stack,"",@progbits
[hjl@gnu-6 pr70155d]$ 

They all can use SSE loa/store.


---


### compiler : `gcc`
### title : `zero-initialized long returned by value generates useless stores/loads to the stack`
### open_at : `2016-04-25T04:18:30Z`
### last_modified_date : `2021-12-07T00:14:44Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70782
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `5.2.1`
### severity : `enhancement`
### contents :
Test case:

--
#include <string.h>

typedef union {
  char ch;
  float fl;
  double dbl;
} u;

u f(const void *p, int type) {
  u v;
  memset(&v, 0, 8);
  if (type == 1) {
    memcpy(&v, p, 1);
  } else if (type <= 5) {
    memcpy(&v, p, 4);
  } else if (type <= 8) {
    memcpy(&v, p, 8);
  }
  return v;
}

--

With gcc 5.2.1 on Ubuntu, compiled with -O3 -fno-stack-protect I get:

--

0000000000000000 <f>:
   0:	83 fe 01             	cmp    esi,0x1
   3:	48 c7 44 24 e8 00 00 	mov    QWORD PTR [rsp-0x18],0x0
   a:	00 00 
   c:	74 32                	je     40 <f+0x40>
   e:	83 fe 05             	cmp    esi,0x5
  11:	7e 1d                	jle    30 <f+0x30>
  13:	83 fe 08             	cmp    esi,0x8
  16:	7f 08                	jg     20 <f+0x20>
  18:	48 8b 07             	mov    rax,QWORD PTR [rdi]
  1b:	48 89 44 24 e8       	mov    QWORD PTR [rsp-0x18],rax
  20:	48 8b 44 24 e8       	mov    rax,QWORD PTR [rsp-0x18]
  25:	c3                   	ret    
  26:	66 2e 0f 1f 84 00 00 	nop    WORD PTR cs:[rax+rax*1+0x0]
  2d:	00 00 00 
  30:	8b 07                	mov    eax,DWORD PTR [rdi]
  32:	89 44 24 e8          	mov    DWORD PTR [rsp-0x18],eax
  36:	48 8b 44 24 e8       	mov    rax,QWORD PTR [rsp-0x18]
  3b:	c3                   	ret    
  3c:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
  40:	0f b6 07             	movzx  eax,BYTE PTR [rdi]
  43:	88 44 24 e8          	mov    BYTE PTR [rsp-0x18],al
  47:	48 8b 44 24 e8       	mov    rax,QWORD PTR [rsp-0x18]
  4c:	c3                   	ret

--

In every code path it saves the read value to the stack, only to read it back.  None of these operations are actually necessary, since the code is already zeroing the other parts of rax.  This function shouldn't need to use any stack space at all.


---


### compiler : `gcc`
### title : `IRA memory cost calculation incorrect for immediates`
### open_at : `2016-04-26T12:13:31Z`
### last_modified_date : `2023-05-31T06:02:36Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70802
### status : `RESOLVED`
### tags : `missed-optimization, ra`
### component : `middle-end`
### version : `7.0`
### severity : `normal`
### contents :
The following code in ira-costs.c tries to improve the memory cost for rematerializeable loads. There are several issues with this though:

1. The memory cost can become negative, forcing a spill, which is known to cause incorrect code (https://gcc.gnu.org/bugzilla/show_bug.cgi?id=64242)
2. The code only handles a subset of immediate loads, not all rematerializeable values
3. The cost adjustment is not sufficient to make better decisions between allocating an immediate to a callee-save register and spill a variable, or allocate the variable and rematerialize the immediate

As an example of (3), if there is only one callee-save register free, IRA will use it to allocate the immediate rather than the variable:

float bad_alloc(float x)
{
  x += 3.0f;
  g();
  x *= 3.0f;
  return x;
}

With -O2 -fomit-frame-pointer -ffixed-d8 -ffixed-d9 -ffixed-d10 -ffixed-d11 -ffixed-d12 -ffixed-d13 -ffixed-d14:

        str     x30, [sp, -32]!
        str     d15, [sp, 8]
        fmov    s15, 3.0e+0
        fadd    s0, s0, s15
        str     s0, [sp, 28]
        bl      g
        ldr     s0, [sp, 28]
        fmul    s0, s0, s15
        ldr     d15, [sp, 8]
        ldr     x30, [sp], 32
        ret

  a0(r76,l0) costs: CALLER_SAVE_REGS:15000,15000 GENERAL_REGS:15000,15000 FP_REGS:0,0 ALL_REGS:15000,15000 MEM:12000,12000
  a1(r73,l0) costs: CALLER_SAVE_REGS:10000,10000 GENERAL_REGS:10000,10000 FP_REGS:0,0 ALL_REGS:10000,10000 MEM:8000,8000

The immediate value r76 is counted as 1 def and 2 uses, so memory cost of 12000, while r73 has 1 def and 1 use, so memory cost of 8000. However the worst-case rematerialization cost of r76 would be 2 moves, one which already exists of course, so the memory cost should have been 4000...

ira-costs.c, ~line 1458:

  if (set != 0 && REG_P (SET_DEST (set)) && MEM_P (SET_SRC (set))
      && (note = find_reg_note (insn, REG_EQUIV, NULL_RTX)) != NULL_RTX
      && ((MEM_P (XEXP (note, 0))
           && !side_effects_p (SET_SRC (set)))
          || (CONSTANT_P (XEXP (note, 0))
              && targetm.legitimate_constant_p (GET_MODE (SET_DEST (set)),
                                                XEXP (note, 0))
              && REG_N_SETS (REGNO (SET_DEST (set))) == 1))
      && general_operand (SET_SRC (set), GET_MODE (SET_SRC (set))))
    {
      enum reg_class cl = GENERAL_REGS;
      rtx reg = SET_DEST (set);
      int num = COST_INDEX (REGNO (reg));

      COSTS (costs, num)->mem_cost
        -= ira_memory_move_cost[GET_MODE (reg)][cl][1] * frequency;
      record_address_regs (GET_MODE (SET_SRC (set)),
                           MEM_ADDR_SPACE (SET_SRC (set)),
                           XEXP (SET_SRC (set), 0), 0, MEM, SCRATCH,
                           frequency * 2);
      counted_mem = true;
    }


---


### compiler : `gcc`
### title : `atomic store of __int128 is not lock free on aarch64`
### open_at : `2016-04-26T21:40:22Z`
### last_modified_date : `2023-05-31T14:04:00Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70814
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `5.3.0`
### severity : `enhancement`
### contents :
`std::atomic<__int128>::store` on aarch64 is not lock free and generates a function call `__atomic_store_16`. However, required atomic instructions (`stlxp`) exists in armv8 and is used by clang. Should gcc use the same instruction as well?

Ref https://llvm.org/bugs/show_bug.cgi?id=27081, which fixes the clang codegen for this case.


---
