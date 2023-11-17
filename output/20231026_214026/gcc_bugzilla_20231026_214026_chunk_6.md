### Total Bugs Detected: 4649
### Current Chunk: 6 of 30
### Bugs in this Chunk: 160 (From bug 801 to 960)
---


### compiler : `gcc`
### title : `SLP vectorization of sqrt fails if in a loop`
### open_at : `2012-12-12T13:29:08Z`
### last_modified_date : `2021-10-01T02:50:53Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=55662
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.0`
### severity : `normal`
### contents :
given the code below
computeOne vectorizes, computeS does not
c++ -std=c++11 -Ofast -mavx2 -S sqrtV.cc; less sqrtV.s
gcc version 4.8.0 20121212 (experimental) [trunk revision 194442] (GCC) 

funny enough it works with arbitrary (inlined) functions of mine (instead of sqrtf) see computeA 

computeL does "vectorize", not in the way I expected!
I really do not understand the code generated for computeAL

cat >> sqrtV.cc
#include<cmath>
#include<type_traits>

typedef float __attribute__( ( vector_size( 16 ) ) ) float32x4_t;
typedef float __attribute__( ( vector_size( 32 ) ) ) float32x8_t;
typedef int __attribute__( ( vector_size( 32 ) ) ) int32x8_t;

float32x8_t va[1024];
float32x8_t vb[1024];
float32x8_t vc[1024];

template<typename Vec, typename F> 
inline
Vec apply(Vec v, F f) {
  typedef typename std::remove_reference<decltype(v[0])>::type T;
  constexpr int N = sizeof(Vec)/sizeof(T);
  Vec ret;
  for (int i=0;i!=N;++i) ret[i] = f(v[i]);
  return ret;
}

void computeOne() {
    vb[0]=apply(va[0],sqrtf);
}

void computeS() {
  for (int i=0;i!=1024;++i)
    vb[i]=apply(va[i],sqrtf);
}

void computeL() {
  for (int i=0;i!=1024;++i)
    for (int j=0;j!=8;++j)
    vb[i][j]=sqrtf(va[i][j]);
}

template<typename Float>
inline
Float atanF(Float t) {
  constexpr float PIO4F = 0.7853981633974483096f;
  Float z= (t > 0.4142135623730950f) ? (t-1.0f)/(t+1.0f) : t;
  // if( t > 0.4142135623730950f ) // * tan pi/8 
  
  Float z2 = z * z;
  Float ret =
    ((( 8.05374449538e-2f * z2
	- 1.38776856032E-1f) * z2
      + 1.99777106478E-1f) * z2
     - 3.33329491539E-1f) * z2 * z
    + z;
  
  // move back in place
  return ( t > 0.4142135623730950f ) ? ret : ret + PIO4F;
  return ret;
}

void computeA() {
  for (int i=0;i!=1024;++i)
    vb[i]=apply(va[i],atanF<float>);
}

void computeAL() {
  for (int i=0;i!=1024;++i)
    for (int j=0;j!=8;++j)
      vb[i][j]=atanF(va[i][j]);
}


---


### compiler : `gcc`
### title : `loop vectorization inefficient in presence of multiple identical conditions`
### open_at : `2012-12-17T18:57:54Z`
### last_modified_date : `2021-10-01T02:51:23Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=55723
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.0`
### severity : `normal`
### contents :
in the following code, basic block vectorization seems to be more efficient that standard loop vectorization (I measure 20% better)
Is the loop vectorization computing the polynomial twice?


gcc version 4.8.0 20121215 (experimental) [trunk revision 194522] (GCC) 



cat AtanT.cc;
typedef float __attribute__( ( vector_size( 16 ) ) ) float32x4_t;

template<typename Float>
inline
Float atan(Float t) {
  constexpr float PIO4F = 0.7853981633974483096f;

  Float z= (t > 0.4142135623730950f) ? (t-1.0f)/(t+1.0f) : t;
  
  Float z2 = z * z;
  Float ret =
    ((( 8.05374449538e-2f * z2
	- 1.38776856032E-1f) * z2
      + 1.99777106478E-1f) * z2
     - 3.33329491539E-1f) * z2 * z
    + z;
  
  // move back in place
  return ( t > 0.4142135623730950f ) ? ret+PIO4F : ret;
  return ret;
}

float32x4_t va[1024];
float32x4_t vb[1024];

float a[4*1024];
float b[4*1024];

void computeV() {
  for (int i=0;i!=1024;++i)
    vb[i]=atan(va[i]);
}

//inline
void computeL() {
  for (int i=0;i!=4*1024;++i)
    b[i]=atan(a[i]);
}
Vincenzos-MacBook-Pro:floatPrec innocent$ c++ -std=c++11 -Ofast -march=corei7 -S AtanT.cc; cat AtanT.s
	.text
	.align 4,0x90
	.globl __Z8computeVv
__Z8computeVv:
LFB1:
	movaps	LC1(%rip), %xmm4
	leaq	_va(%rip), %rcx
	xorl	%eax, %eax
	movaps	LC0(%rip), %xmm10
	leaq	_vb(%rip), %rdx
	movaps	LC2(%rip), %xmm9
	movaps	LC3(%rip), %xmm8
	movaps	LC4(%rip), %xmm7
	movaps	LC5(%rip), %xmm6
	movaps	LC6(%rip), %xmm5
	.align 4,0x90
L3:
	movaps	(%rcx,%rax), %xmm1
	movaps	%xmm1, %xmm3
	movaps	%xmm1, %xmm2
	addps	%xmm4, %xmm3
	subps	%xmm4, %xmm2
	rcpps	%xmm3, %xmm0
	mulps	%xmm0, %xmm3
	mulps	%xmm0, %xmm3
	addps	%xmm0, %xmm0
	subps	%xmm3, %xmm0
	movaps	%xmm1, %xmm3
	mulps	%xmm0, %xmm2
	movaps	%xmm10, %xmm0
	cmpltps	%xmm1, %xmm0
	blendvps	%xmm0, %xmm2, %xmm3
	movaps	%xmm3, %xmm2
	mulps	%xmm3, %xmm2
	movaps	%xmm2, %xmm1
	mulps	%xmm9, %xmm1
	subps	%xmm8, %xmm1
	mulps	%xmm2, %xmm1
	addps	%xmm7, %xmm1
	mulps	%xmm2, %xmm1
	subps	%xmm6, %xmm1
	mulps	%xmm2, %xmm1
	addps	%xmm4, %xmm1
	mulps	%xmm3, %xmm1
	movaps	%xmm1, %xmm2
	addps	%xmm5, %xmm2
	blendvps	%xmm0, %xmm2, %xmm1
	movaps	%xmm1, (%rdx,%rax)
	addq	$16, %rax
	cmpq	$16384, %rax
	jne	L3
	rep; ret
LFE1:
	.align 4,0x90
	.globl __Z8computeLv
__Z8computeLv:
LFB2:
	movaps	LC1(%rip), %xmm5
	leaq	_a(%rip), %rcx
	xorl	%eax, %eax
	movaps	LC0(%rip), %xmm11
	leaq	_b(%rip), %rdx
	movaps	LC2(%rip), %xmm9
	movaps	LC7(%rip), %xmm8
	movaps	LC4(%rip), %xmm7
	movaps	LC8(%rip), %xmm6
	movaps	LC6(%rip), %xmm10
	.align 4,0x90
L7:
	movaps	(%rcx,%rax), %xmm0
	movaps	%xmm0, %xmm3
	movaps	%xmm0, %xmm1
	addps	%xmm5, %xmm3
	subps	%xmm5, %xmm1
	rcpps	%xmm3, %xmm2
	mulps	%xmm2, %xmm3
	mulps	%xmm2, %xmm3
	addps	%xmm2, %xmm2
	subps	%xmm3, %xmm2
	movaps	%xmm0, %xmm3
	mulps	%xmm0, %xmm3
	mulps	%xmm2, %xmm1
	movaps	%xmm1, %xmm4
	mulps	%xmm1, %xmm4
	movaps	%xmm4, %xmm2
	mulps	%xmm9, %xmm2
	addps	%xmm8, %xmm2
	mulps	%xmm4, %xmm2
	addps	%xmm7, %xmm2
	mulps	%xmm4, %xmm2
	addps	%xmm6, %xmm2
	mulps	%xmm4, %xmm2
	movaps	%xmm11, %xmm4
	cmpltps	%xmm0, %xmm4
	addps	%xmm5, %xmm2
	mulps	%xmm1, %xmm2
	movaps	%xmm3, %xmm1
	mulps	%xmm9, %xmm1
	addps	%xmm10, %xmm2
	addps	%xmm8, %xmm1
	mulps	%xmm3, %xmm1
	addps	%xmm7, %xmm1
	mulps	%xmm3, %xmm1
	addps	%xmm6, %xmm1
	mulps	%xmm3, %xmm1
	addps	%xmm5, %xmm1
	mulps	%xmm0, %xmm1
	movaps	%xmm4, %xmm0
	blendvps	%xmm0, %xmm2, %xmm1
	movaps	%xmm1, (%rdx,%rax)
	addq	$16, %rax
	cmpq	$16384, %rax
	jne	L7
	rep; ret


---


### compiler : `gcc`
### title : `Issue with complete innermost loop unrolling (cunrolli)`
### open_at : `2012-12-18T14:12:53Z`
### last_modified_date : `2021-12-12T09:45:25Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=55731
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.0`
### severity : `normal`
### contents :
I attached 2 test-cases extracted from important benchmark at which clang and icc outperform gcc for x86 target (atom). For 1st test-case (t.c) cunrolli phase does not perform complete loop unrolling with the following message (test was compiled with -O3 -funroll-loops options):

  Loop size: 23
  Estimated size after unrolling: 33
Not unrolling loop 1: size would grow.

but it is unrolled by cunroll phase:

  Loop size: 24
  Estimated size after unrolling: 32
Unrolled loop 1 completely (duplicated 2 times).

I wonder why this loop was not unrolled by cunrolli? We lost a lot of optimizations for unrolled loop such as Constant (address) Propagation, Dead code elimination etc. and got non-optimal binaries.

For comparsion I added another test (t2.c) with successfull complete unrolling by cunrolli, at which we can see that all assignments to local array 'b' were properly propagated and deleted but we don't have such transformations for 1st test-case.


---


### compiler : `gcc`
### title : `Suboptimal interrupt prologue/epilogue for ARMv7-M (Cortex-M3)`
### open_at : `2012-12-20T15:03:25Z`
### last_modified_date : `2020-04-09T19:23:21Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=55757
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.6.2`
### severity : `enhancement`
### contents :
With a Cortex-M3 microcontroller (ARMv7-M) and an empty interrupt handler function:

void DMA_IRQHandler(void) __attribute((interrupt));
void DMA_IRQHandler(void)
{

}

Results in suboptimal prologue/epilogue:

000023b4 <DMA_IRQHandler>:
void DMA_IRQHandler(void) __attribute((interrupt));
void DMA_IRQHandler(void)
{
    23b4:	4668      	mov	r0, sp
    23b6:	f020 0107 	bic.w	r1, r0, #7
    23ba:	468d      	mov	sp, r1
    23bc:	b501      	push	{r0, lr}
}
    23be:	e8bd 4001 	ldmia.w	sp!, {r0, lr}
    23c2:	4685      	mov	sp, r0
    23c4:	4770      	bx	lr
	...

Without the __attribute__ the function is fine, just a single "bx lr".

This behavior is incorrect not only because r0 and lr are unused, but also because on ARMv7-M these registers (r0-r3, lr, ip, sp, pc, psr) are saved by hardware, so there's no point in saving them again.


---


### compiler : `gcc`
### title : `unnecessary spill/reload to compose register pair`
### open_at : `2012-12-21T00:38:33Z`
### last_modified_date : `2021-08-30T02:48:28Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=55769
### status : `UNCONFIRMED`
### tags : `missed-optimization, ra`
### component : `target`
### version : `4.8.0`
### severity : `enhancement`
### contents :
Created attachment 29018
testcase

Compile the attached source code with options: -march=armv7-a -mthumb -O2

Trunk gcc generates:

sum_ror_mem:
	@ args = 0, pretend = 0, frame = 40
	@ frame_needed = 0, uses_anonymous_args = 0
	push	{r4, r5, r6, r7, r8, r9, r10, fp, lr}
	add	r8, r1, r2
	cmp	r1, r8
	sub	sp, sp, #44
	mov	r4, r0
	mov	r5, #0
	bcs	.L2
	mov	r9, r1
.L3:
	add	r0, r9, #1024
	add	r9, r9, #64
	bl	prefetch
	ldrd	r2, [r9, #-64]
	adds	r2, r2, r4
	adc	r3, r3, r5
	lsrs	r1, r2, #8
	orr	r1, r1, r3, lsl #24
	lsrs	r3, r3, #8
	str	r1, [sp]                    // A
	orr	r3, r3, r2, lsl #24
	str	r3, [sp, #4]                // B
	ldrd	r0, [r9, #-56]
	ldrd	r2, [sp]                    // C
	adds	r2, r2, r0
	adc	r3, r3, r1
	lsrs	r1, r2, #8
	orr	r1, r1, r3, lsl #24
	lsrs	r3, r3, #8
	str	r1, [sp, #8]
	orr	r3, r3, r2, lsl #24
	str	r3, [sp, #12]
	ldrd	r0, [r9, #-48]
	ldrd	r2, [sp, #8]
	adds	r2, r2, r0
	adc	r3, r3, r1
	lsrs	r1, r2, #8
	orr	r1, r1, r3, lsl #24
	lsrs	r3, r3, #8
	str	r1, [sp, #16]
	orr	r3, r3, r2, lsl #24
	str	r3, [sp, #20]
	ldrd	r0, [r9, #-40]
	ldrd	r2, [sp, #16]
	adds	r2, r2, r0
	adc	r3, r3, r1
	lsrs	r1, r2, #8
	orr	r1, r1, r3, lsl #24
	lsrs	r3, r3, #8
	str	r1, [sp, #24]
	orr	r3, r3, r2, lsl #24
	str	r3, [sp, #28]
	ldrd	r0, [r9, #-32]
	ldrd	r2, [sp, #24]
	adds	r2, r2, r0
	adc	r3, r3, r1
	lsrs	r1, r2, #8
	orr	r10, r1, r3, lsl #24
	lsrs	r3, r3, #8
	orr	fp, r3, r2, lsl #24
	ldrd	r2, [r9, #-24]
	adds	r2, r2, r10
	adc	r3, r3, fp
	lsrs	r1, r2, #8
	orr	r1, r1, r3, lsl #24
	lsrs	r3, r3, #8
	str	r1, [sp, #32]
	orr	r3, r3, r2, lsl #24
	str	r3, [sp, #36]
	ldrd	r0, [r9, #-16]
	ldrd	r2, [sp, #32]
	adds	r2, r2, r0
	adc	r3, r3, r1
	lsr	ip, r2, #8
	ldrd	r0, [r9, #-8]
	orr	r6, ip, r3, lsl #24
	lsrs	r3, r3, #8
	adds	r0, r0, r6
	orr	r7, r3, r2, lsl #24
	adc	r1, r1, r7
	cmp	r8, r9
	lsr	r2, r0, #8
	lsr	r3, r1, #8
	orr	r4, r2, r1, lsl #24
	orr	r5, r3, r0, lsl #24
	bhi	.L3
.L2:
	adds	r0, r5, r4
	add	sp, sp, #44
	@ sp needed
	pop	{r4, r5, r6, r7, r8, r9, r10, fp, pc}

Note that instructions AB spill two value onto stack, and instruction C read them back to form a 64bit register pair. If we swap the register usage of r1 and r2, then we can avoid these 3 instructions. There are also many similar patterns in the following instructions that can be avoided.


---


### compiler : `gcc`
### title : `Comparison with a negated number vs sum for FP`
### open_at : `2012-12-23T09:51:21Z`
### last_modified_date : `2021-12-28T05:39:11Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=55796
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.0`
### severity : `enhancement`
### contents :
Hello,

gcc doesn't seem to notice that for double variables a and b, comparing a==-b or a+b==0 is the same thing for finite math.

void g();
void f(double a,double b){
  if(a==-b)  g();
  if(-a==b)  g();
  if(a+b==0) g();
}

compiled with -Ofast on x86_64-linux still has three comparisons and jumps. Merging the first two shouldn't even require any unsafe flag.


---


### compiler : `gcc`
### title : `Various missed optimizations for a simple function in GCC itself`
### open_at : `2012-12-24T00:00:28Z`
### last_modified_date : `2021-07-20T06:01:09Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=55802
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.0`
### severity : `enhancement`
### contents :
Consider this test case:

-------------- 8< -------------- 
typedef struct bitmap_head_def {
  unsigned int indx;
} bitmap_head;
typedef bitmap_head *bitmap;
extern int bitmap_ior_into (bitmap, bitmap);

struct basic_block_def;
typedef struct basic_block_def *basic_block;
struct edge_def;
typedef struct edge_def *edge;

struct basic_block_def {
  int index;
};

struct edge_def {
  basic_block src;
  basic_block dest;
  int flags;
};

struct dataflow
{
  void *block_info;
  unsigned int block_info_size;
};

struct df_d
{
  struct dataflow *problems_by_index[(7 + 1)];
};

extern struct df_d *df;

struct df_live_bb_info
{
  bitmap_head in, out;
};

static __inline__ struct df_live_bb_info *
df_live_get_bb_info (unsigned int index)
{
  if (index < (df->problems_by_index[2])->block_info_size)
    return &((struct df_live_bb_info *) (df->problems_by_index[2])->block_info)[index];
  else
    return ((void *)0);
}

unsigned char df_live_confluence_n (edge e);
unsigned char
df_live_confluence_n (edge e)
{
  bitmap op1 = &df_live_get_bb_info (e->dest->index)->in;
  bitmap op2 = &df_live_get_bb_info (e->src->index)->out;

  if (e->flags & 0x0010)
    return 0;

  return bitmap_ior_into (op1, op2);
}
-------------- 8< -------------- 

Compiled at -O2 on powerpc64, the ".optimized" dump at trunk r194705
looks like this:

;; Function df_live_confluence_n (df_live_confluence_n, funcdef_no=1, decl_uid=2030, cgraph_uid=1)

df_live_confluence_n (struct edge_def * e)
{
  struct df_d * df.0;
  struct bitmap_head * op2;
  struct bitmap_head * op1;
  unsigned char _1;
  struct basic_block_def * _5;
  int _6;
  unsigned int _7;
  struct basic_block_def * _9;
  int _10;
  unsigned int _11;
  int _13;
  int _14;
  int _16;
  unsigned char _17;
  struct dataflow * _19;
  unsigned int _20;
  void * _21;
  long unsigned int _22;
  long unsigned int _23;
  struct df_live_bb_info * _24;
  struct df_live_bb_info * _25;
  void * _26;
  long unsigned int _27;
  long unsigned int _28;
  struct df_live_bb_info * _29;
  struct df_live_bb_info * _30;

  <bb 2>:
  _5 = e_4(D)->dest;
  _6 = _5->index;
  _7 = (unsigned int) _6;
  df.0_18 = df;
  _19 = df.0_18->problems_by_index[2];
  _20 = _19->block_info_size;
  if (_7 < _20)
    goto <bb 3>;
  else
    goto <bb 4>;

  <bb 3>:
  _21 = _19->block_info;
  _22 = (long unsigned int) _7;
  _23 = _22 * 8;
  _24 = _21 + _23;

  <bb 4>:
  # _25 = PHI <0B(2), _24(3)>
  _9 = e_4(D)->src;
  _10 = _9->index;
  _11 = (unsigned int) _10;
  if (_11 < _20)
    goto <bb 5>;
  else
    goto <bb 6>;

  <bb 5>:
  _26 = _19->block_info;
  _27 = (long unsigned int) _11;
  _28 = _27 * 8;
  _29 = _26 + _28;

  <bb 6>:
  # _30 = PHI <0B(4), _29(5)>
  _13 = e_4(D)->flags;
  _14 = _13 & 16;
  if (_14 != 0)
    goto <bb 8>;
  else
    goto <bb 7>;

  <bb 7>:
  op2_12 = &_30->out;
  op1_8 = &_25->in;
  _16 = bitmap_ior_into (op1_8, op2_12);
  _17 = (unsigned char) _16;

  <bb 8>:
  # _1 = PHI <0(6), _17(7)>
  return _1;

}


There are several issues here.

First, the initializations of op1 and op2 are partially dead if the
"e->flags" test is true. But this optimization is not performed.
Even if the test is modified to assert that the basic block index is
always smaller than the block_info_size (linearizing the code to load
the bitmap addresses) the partially dead code is still not moved down
below the condition.

Second, the load from block_info is performed twice, even with profile
information available. The load should be speculated.

This all leads to very branchy code...


---


### compiler : `gcc`
### title : `SSE2 double negation less efficient than explicit xor`
### open_at : `2012-12-24T10:42:05Z`
### last_modified_date : `2021-08-15T05:31:49Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=55803
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.8.0`
### severity : `enhancement`
### contents :
Compiling the following code with -Os (-O3 or -O2 have the same with xorpd) on x86_64-linux

#include <x86intrin.h>
double f(double d){
  return -d;
}
__m128d g(__m128d d){
  __m128d m={-0.,0.};
  return _mm_xor_pd(d,m);
}

gives for f:
	movsd	.LC0(%rip), %xmm1
	xorps	%xmm1, %xmm0

and for g:
	xorps	.LC0(%rip), %xmm0

-mavx doesn't help.


---


### compiler : `gcc`
### title : `thread_local with either a ctor or dtor causes a function call every time through a loop`
### open_at : `2012-12-26T12:53:22Z`
### last_modified_date : `2021-12-28T05:35:02Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=55812
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.0`
### severity : `enhancement`
### contents :
Hello,

TLS accesses are expensive, so as much as possible gcc should copy the address to a local variable and use that instead. The following example may not be very good, I am just trying to illustrate the issue.

#include <vector>
thread_local std::vector<int> v;
int main(){
  for(long i=0;i<400000000;++i){
    v.push_back(i);
  }
  return v.size();
}

compiled with g++ -std=c++11 -O2 -Wall -DNDEBUG. If I remove "thread_local", the speed-up is about 20%. It seems to me that the compiler should get the address of v once at the beginning of main and use that for the rest of the function, and thus the performance difference should be negligible.

If I add "static" in front of "thread_local", the program fails to link, but my gcc snapshot is a bit old (Nov 20) and I think I've already seen that reported.

I was surprised not to find any compiler option that would disable threads, so I could write thread_local but not pay the price when compiling a single-threaded program. Without -pthread, glibc uses cheap thread-unsafe functions, but I still pay for TLS.


---


### compiler : `gcc`
### title : `Cannot sink conditional code`
### open_at : `2013-01-02T11:01:23Z`
### last_modified_date : `2021-12-25T09:19:50Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=55846
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.0`
### severity : `enhancement`
### contents :
Code sinking (tree-ssa-sink.c) cannot sink conditional code:

int foo (int b, int c)
{
  int res = 0;
  if (b)
    res = b * 2 + 4;
  if (c)
    return res;
  return 0;
}

here we want to sink the whole if (b) res = b * 2 + 4; block into
the if (c) block.

Profitable if the original conditional becomes dead after sinking
the PHI node for 'res' and its dependencies.

Happens in GCC itself - usually exposed via inlining.


---


### compiler : `gcc`
### title : `Turn segmented iteration into nested loops`
### open_at : `2013-01-03T14:02:29Z`
### last_modified_date : `2021-11-03T20:15:03Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=55860
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.0`
### severity : `enhancement`
### contents :
Hello,

in the code below (compiled with g++ -O3), replacing L2 with L1 in the goto lets gcc generate much better code (the loop on iii never tests jkl), whereas with L2 it performs the redundant test every time. I have no idea how hard it would be to teach gcc to notice that. This kind of code appears in C++ when we define an iterator that iterates over the elements of several containers successively.

void f(int,int);
void g(int n,int m){
  int iii=0;
  int jkl=0;
  while(jkl<n)
  {
L1:
    if(iii<m)
    {
      f(jkl,iii);
      ++iii;
      goto L2;
    }
    else
    {
      ++jkl;
      iii=0;
    }
L2:;
  }
}


---


### compiler : `gcc`
### title : `different bit shift/or optimization.`
### open_at : `2013-01-03T20:13:29Z`
### last_modified_date : `2021-05-24T07:12:17Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=55869
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.0`
### severity : `normal`
### contents :
here're equvialent functions:

$ cat u.cpp
unsigned long long convert_1( bool flag )
{
        return (unsigned long long)(flag ? 1ull : 0ull) << 57;
}
unsigned long long convert_2( bool flag )
{
        return (unsigned long long)flag << 57;
}

current 4.7/4.8 gcc emits following different machine code:

_Z9convert_1b:

        testb   %dil, %dil      # 29    *cmpqi_ccno_1/1 [length = 3]
        movl    $0, %edx        # 32    *movdi_internal_rex64/1 [length = 5]
        movabsq $144115188075855872, %rax       # 28    *movdi_internal_rex64/3 [length = 10]
        cmove   %rdx, %rax      # 31    *movdicc_noc/1  [length = 4]
        ret     # 39    simple_return_internal  [length = 1]

_Z9convert_2b:
        movq    %rdi, %rax      # 19    *movdi_internal_rex64/2 [length = 3]
        salq    $57, %rax       # 8     *ashldi3_1/1    [length = 4]
        ret     # 27    simple_return_internal  [length = 1]


while clang/llvm emits equivalent machine code for both functions:

_Z9convert_1b:                          # @_Z9convert_1b
        movzbl  %dil, %eax
        shlq    $57, %rax
        ret

_Z9convert_2b:                          # @_Z9convert_2b
        movzbl  %dil, %eax
        shlq    $57, %rax
        ret


---


### compiler : `gcc`
### title : `No constant propagation in Intel intrinsics`
### open_at : `2013-01-07T13:14:34Z`
### last_modified_date : `2021-12-29T04:47:26Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=55894
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.8.0`
### severity : `enhancement`
### contents :
I was comparing ways to generate a constant (Intel 12.0 doesn't support the first one), and noticed that these functions result in different asm. In particular, there doesn't seem to be a lot of constant propagation going on :-(
-Ofast and various -march only managed to change 'g' to movddup	.LC1(%rip), %xmm0 (which in itself looks better than movapd, except that if I change g to take an argument __m128d a and return _mm_xor_pd(a,m), that prevents gcc from compacting it to a single insn, and I really don't see a reason for f and g to generate different code as they look so similar). By the way, if you have a suggestion on the simplest portable way to get this constant...

#include <x86intrin.h>
__m128d f(){
  const __m128d m = _mm_castsi128_pd (_mm_set1_epi64x (0x7fffffffffffffff));
  return m;
}
__m128d g(){
  const __m128d m = _mm_castsi128_pd (_mm_set1_epi64 (_mm_set_pi32(0x7fffffff,0xffffffff)));
  return m;
}
__m128d h(){
  const __m128d x = _mm_set1_pd (-0.);
  const __m128d m1 = _mm_cmpeq_pd (x, x);
  const __m128d m = _mm_xor_pd (x, m1);
  return m;
}

_Z1fv:
.LFB539:
	.cfi_startproc
	movapd	.LC0(%rip), %xmm0
	ret
	.cfi_endproc
[...]
_Z1gv:
.LFB540:
	.cfi_startproc
	movq	.LC1(%rip), %xmm0
	punpcklqdq	%xmm0, %xmm0
	ret
	.cfi_endproc
[...]
_Z1hv:
.LFB541:
	.cfi_startproc
	movapd	.LC3(%rip), %xmm0
	movapd	%xmm0, %xmm1
	cmpeqpd	%xmm0, %xmm1
	xorpd	%xmm1, %xmm0
	ret
	.cfi_endproc
[...]
.LC0:
	.long	4294967295
	.long	2147483647
	.long	4294967295
	.long	2147483647
	.section	.rodata.cst8,"aM",@progbits,8
	.align 8
.LC1:
	.long	-1
	.long	2147483647
	.section	.rodata.cst16
	.align 16
.LC3:
	.long	0
	.long	-2147483648
	.long	0
	.long	-2147483648


---


### compiler : `gcc`
### title : `suboptimal code generated for post-inc on Thumb1`
### open_at : `2013-01-08T05:55:51Z`
### last_modified_date : `2023-06-21T04:04:05Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=55906
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.0`
### severity : `normal`
### contents :
For below program:

int
ffs(int word)

{
  int i;

  if (!word)
    return 0;

  i = 0;
  for (;;)
    {
      if (((1 << i++) & word) != 0)
 return i;
    }
}

The dump of 164t.optimized is like:
ffs (int word)
{
  int i;
  int _6;
  int _7;

  <bb 2>:
  if (word_3(D) == 0)
    goto <bb 6>;
  else
    goto <bb 3>;

  <bb 3>:

  <bb 4>:
  # i_1 = PHI <0(3), i_5(5)>
  i_5 = i_1 + 1;
  _6 = word_3(D) >> i_1;
  _7 = _6 & 1;
  if (_7 != 0)
    goto <bb 6>;
  else
    goto <bb 5>;

  <bb 5>:
  goto <bb 4>;

  <bb 6>:
  # i_2 = PHI <0(2), i_5(4)>
  return i_2;

}
GCC increases i before i_1 is used, causing i_5 and i_1 to be partitioned into different partitions as in expanded rtl:
    2: r115:SI=r0:SI
    3: NOTE_INSN_FUNCTION_BEG
    9: pc={(r115:SI==0)?L33:pc}
      REG_BR_PROB 0xf3c
   10: NOTE_INSN_BASIC_BLOCK 4
    4: r110:SI=0
   18: L18:
   11: NOTE_INSN_BASIC_BLOCK 5
   12: r111:SI=r110:SI+0x1        <-----i_5/i_1 in different pseudos
   13: r116:SI=r115:SI>>r110:SI
   14: r118:SI=0x1
   15: r117:SI=r116:SI&r118:SI
      REG_EQUAL r116:SI&0x1
   16: pc={(r117:SI!=0)?L21:pc}
      REG_BR_PROB 0x384
   17: NOTE_INSN_BASIC_BLOCK 6
    5: r110:SI=r111:SI
   19: pc=L18
   20: barrier
   33: L33:
   32: NOTE_INSN_BASIC_BLOCK 7
    6: r111:SI=0
   21: L21:
   22: NOTE_INSN_BASIC_BLOCK 8
   23: r114:SI=r111:SI
   27: r0:SI=r114:SI
   30: use r0:SI

Finally, suboptimal codes are generated :
ffs:
	mov	r3, #0
	push	{r4, lr}
	cmp	r0, r3
	beq	.L2
	mov	r2, r3
	mov	r1, #1
.L3:
	mov	r4, r0
	asr	r4, r4, r2
	add	r3, r2, #1
	tst	r4, r1
	bne	.L2
	mov	r2, r3
	b	.L3
.L2:
	mov	r0, r3
	@ sp needed
	pop	{r4, pc}

While GCC 4.6 generates better codes:
ffs:
	push	{lr}
	sub	r3, r0, #0
	beq	.L2
	mov	r3, #0
	mov	r2, #1
.L3:
	mov	r1, r0
	asr	r1, r1, r3
	add	r3, r3, #1
	tst	r1, r2
	beq	.L3
.L2:
	mov	r0, r3
	@ sp needed for prologue
	pop	{pc}


The command line is:
arm-none-eabi-gcc -mthumb -mcpu=cortex-m0 -Os -S ffs.c -o ffs.S

Same problem exists when optimizing with "-O2"


---


### compiler : `gcc`
### title : `missing optimization of x/x and x/std::abs(x)`
### open_at : `2013-01-09T07:45:39Z`
### last_modified_date : `2023-05-12T05:53:45Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=55912
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.0`
### severity : `enhancement`
### contents :
in the following examples I'm quite surprised that only (x/x)is optimized to "!".
With Ofast (and even more with -mrecip) I would have expected that commutativity of multiplication to be used at least to optimized x*a/x

Optimizing x/x and x/std::abs(x) would be beneficial with -mrecip to amortize a trivial loss of precision.

cat one.cc;c++ -Ofast  -S one.cc -msse4.2; cat one.s
#include<cmath>
int one1(float a, float x) {
  return x*a/x;
}

#include<cmath>
int one2(float a, float x) {
  return a*(x/x);
}



int sign1(float a, float x) {
  return x*a/std::abs(x);
}

int sign2(float a, float x) {
  return a*(x/std::abs(x));
}

	.text
	.align 4,0x90
	.globl __Z4one1ff
__Z4one1ff:
LFB86:
	mulss	%xmm1, %xmm0
	divss	%xmm1, %xmm0
	cvttss2si	%xmm0, %eax
	ret
LFE86:
	.align 4,0x90
	.globl __Z4one2ff
__Z4one2ff:
LFB87:
	cvttss2si	%xmm0, %eax
	ret
LFE87:
	.align 4,0x90
	.globl __Z5sign1ff
__Z5sign1ff:
LFB88:
	mulss	%xmm1, %xmm0
	movss	LC0(%rip), %xmm2
	andps	%xmm2, %xmm1
	divss	%xmm1, %xmm0
	cvttss2si	%xmm0, %eax
	ret
LFE88:
	.align 4,0x90
	.globl __Z5sign2ff
__Z5sign2ff:
LFB89:
	movss	LC0(%rip), %xmm2
	andps	%xmm1, %xmm2
	divss	%xmm2, %xmm1
	mulss	%xmm0, %xmm1
	cvttss2si	%xmm1, %eax
	ret


---


### compiler : `gcc`
### title : `tree passes pessimize complex load/store operations`
### open_at : `2013-01-09T18:20:13Z`
### last_modified_date : `2023-10-01T18:45:18Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=55923
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.0`
### severity : `normal`
### contents :
Created attachment 29130
preprocessed test case

The Epiphany can do aligned 64 bit loads/stores just fine, and do that
with post-increment / modify too, so one ldrd and one strd instruction
(each 64 bit) with post-increment would be sufficient to do the loads / stores
in the inner loop of the testcase.
But because the tree optimizers think they know best how to handle complex
values, we end up with three address computation instructions, two loads, and
two stores (each 32 bit).


---


### compiler : `gcc`
### title : `Bytemark HUFFMAN 11% slower with -ftree-vectorize`
### open_at : `2013-01-14T13:34:20Z`
### last_modified_date : `2021-10-01T02:51:38Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=55968
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.0`
### severity : `normal`
### contents :
http://www.tux.org/~mayer/linux/nbench-byte-2.2.3.tar.gz

with -fno-tree-vectorize
HUFFMAN             :            5232  :     145.08  :      46.33
without -fno-tree-vectorize
HUFFMAN             :          4640.9  :     128.69  :      41.10

CFLAGS = -fomit-frame-pointer -Wall -O3 -funroll-loops -g0  -march=corei7 -ffast-math -fno-PIE -fno-exceptions -fno-stack-protector -static
CPU Sandy Bridge


---


### compiler : `gcc`
### title : `SCEV should thread flags ^= 0x80000000 as an addition to discover an IV var.`
### open_at : `2013-01-16T13:32:45Z`
### last_modified_date : `2023-09-04T00:41:44Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=56003
### status : `UNCONFIRMED`
### tags : `missed-optimization, needs-bisection`
### component : `tree-optimization`
### version : `4.8.0`
### severity : `enhancement`
### contents :
In the following testcase we fail to work out that the loop is not really iterating after unswitching otherwise.
void my_waitpid (int flags, int wnohang)
{
  while (1)
    {
      if (flags & 0x80000000)
        {
          if (wnohang)
            break;
          if (debug_threads)
            __builtin_puts ("blocking\n");
          sigsuspend ();
        }
      flags ^= 0x80000000;
    }
}


---


### compiler : `gcc`
### title : `[7/8 Regression] Simplification to constants not done`
### open_at : `2013-01-20T10:23:04Z`
### last_modified_date : `2019-04-16T07:57:04Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=56049
### status : `RESOLVED`
### tags : `deferred, missed-optimization`
### component : `tree-optimization`
### version : `4.8.0`
### severity : `enhancement`
### contents :
From http://gcc.gnu.org/ml/fortran/2013-01/msg00158.html :

program inline

    integer i
    integer a(8,8), b(8,8)

    a = 0
    do i = 1, 10000000
        call add(b, a, 1)
        a = b
    end do

    print *, a

contains

    subroutine add(b, a, o)
        integer, intent(inout) :: b(8,8)
        integer, intent(in) :: a(8,8), o
        b = a + o
    end subroutine add

end program inline

is simplified all the way to the final constant with 4.6 and
4.7 (example for 4.6.2):

;; Function inline (MAIN__) (executed once)

inline ()
{
  struct array2_integer(kind=4) parm.3;
  struct __st_parameter_dt dt_parm.2;
  integer(kind=4) a[64];

<bb 2>:
  a = {};
  MEM[(integer(kind=4)[64] *)&a] = 10000000;
  MEM[(integer(kind=4)[64] *)&a + 4B] = 10000000;
  MEM[(integer(kind=4)[64] *)&a + 8B] = 10000000;
  MEM[(integer(kind=4)[64] *)&a + 12B] = 10000000;
  MEM[(integer(kind=4)[64] *)&a + 16B] = 10000000;
  MEM[(integer(kind=4)[64] *)&a + 20B] = 10000000;
  MEM[(integer(kind=4)[64] *)&a + 24B] = 10000000;
  MEM[(integer(kind=4)[64] *)&a + 28B] = 10000000;
  MEM[(integer(kind=4)[64] *)&a + 32B] = 10000000;

... and so on.  Current trunk converts this to

;; Function inline (MAIN__, funcdef_no=0, decl_uid=1874, cgraph_uid=1) (executed once)

inline ()
{
  vector(4) integer(kind=4) vect_var_.16;
  vector(4) integer(kind=4) vect_var_.15;
  vector(4) integer(kind=4) vect_var_.14;
  struct array2_integer(kind=4) parm.3;
  struct __st_parameter_dt dt_parm.2;
  integer(kind=4) b[64];
  integer(kind=4) a[64];
  unsigned int ivtmp_153;
  unsigned int ivtmp_154;

  <bb 2>:
  a = {};

  <bb 3>:
  # ivtmp_154 = PHI <10000000(2), ivtmp_153(4)>
  vect_var_.14_1 = MEM[(integer(kind=4)[64] *)&a];
  vect_var_.15_42 = MEM[(integer(kind=4)[64] *)&a + 16B];
  vect_var_.16_43 = vect_var_.14_1 + { 1, 1, 1, 1 };
  vect_var_.16_44 = vect_var_.15_42 + { 1, 1, 1, 1 };
  MEM[(integer(kind=4)[64] *)&b] = vect_var_.16_43;
  MEM[(integer(kind=4)[64] *)&b + 16B] = vect_var_.16_44;
  vect_var_.14_71 = MEM[(integer(kind=4)[64] *)&a + 32B];
  vect_var_.15_77 = MEM[(integer(kind=4)[64] *)&a + 48B];
  vect_var_.16_78 = vect_var_.14_71 + { 1, 1, 1, 1 };
  vect_var_.16_79 = vect_var_.15_77 + { 1, 1, 1, 1 };


---


### compiler : `gcc`
### title : `[7 Regression] RA pessimization`
### open_at : `2013-01-21T17:37:09Z`
### last_modified_date : `2022-05-27T08:00:45Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=56069
### status : `RESOLVED`
### tags : `missed-optimization, ra`
### component : `rtl-optimization`
### version : `4.8.0`
### severity : `normal`
### contents :
Since http://gcc.gnu.org/viewcvs?root=gcc&view=rev&rev=139993
unsigned long foo (unsigned long mem)
{
  return (mem >> 3) | (1UL << 44);
}

unsigned long bar (unsigned long mem)
{
  return (mem >> 3) + (1UL << 44);
}

on x86_64-linux at -O2 (and -Os) the generated code for foo is one insn longer.
We used to emit:
        shrq    $3, %rdi
        movabsq $17592186044416, %rax
        orq     %rdi, %rax
        ret
but now emit:
        movq    %rdi, %rax
        movabsq $17592186044416, %rdx
        shrq    $3, %rax
        orq     %rdx, %rax
        ret


---


### compiler : `gcc`
### title : `Sub-optimal code generated for conditional shift`
### open_at : `2013-01-24T06:46:47Z`
### last_modified_date : `2023-08-05T03:54:28Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=56096
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.7.2`
### severity : `enhancement`
### contents :
Compiling this snippet

unsigned f1 (unsigned x, unsigned m)
{
    x >>= ((m & 0x008080) ? 8 : 0);
    return x;
}

with gcc 4.7.2 gives this code for ARMv5:

$ armv5tel-softfloat-linux-gnueabi-gcc -O2 -S -o- f.c
[...]
	ldr	r3, .L4
	and	r3, r1, r3
	cmp	r3, #0
	movne	r3, #8           @ XXX
	moveq	r3, #0           @ XXX
	mov	r0, r0, lsr r3   @ XXX
	bx	lr
[...]

Those three mov instructions are clearly sub-optimal.

Replacing the ternary operator with an if-statement gives the expected code sequence:

unsigned f1 (unsigned x, unsigned m)
{
	if (m & 0x008080)
		x >>= 8;

	return x;
}

-> 
	ldr	r3, .L6
	and	r3, r1, r3
	cmp	r3, #0
	movne	r0, r0, lsr #8
	bx	lr

ie we saved two mov instructions.


---


### compiler : `gcc`
### title : `unnecessary additions in loop [x86, x86_64]`
### open_at : `2013-01-31T10:43:17Z`
### last_modified_date : `2021-07-24T14:47:09Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=56160
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `target`
### version : `4.8.0`
### severity : `normal`
### contents :
the attached code which does complex float multiplication using sse3 produces 4 unnecessary integer additions if the NaN fallback function comp_mult is inlined

the assembly for the loop generated with -msse3 -O3 -std=c99 in gcc 4.4, 4.6, 4.7 and 4.8 svn 195604 looks like this:
  28:	0f 28 0e             	movaps (%esi),%xmm1
  2b:	f3 0f 12 c1          	movsldup %xmm1,%xmm0
  2f:	8b 55 08             	mov    0x8(%ebp),%edx
  32:	0f 28 13             	movaps (%ebx),%xmm2
  35:	f3 0f 16 c9          	movshdup %xmm1,%xmm1
  39:	0f 59 c2             	mulps  %xmm2,%xmm0
  3c:	0f c6 d2 b1          	shufps $0xb1,%xmm2,%xmm2
  40:	0f 59 ca             	mulps  %xmm2,%xmm1
  43:	f2 0f d0 c1          	addsubps %xmm1,%xmm0
  47:	0f 29 04 fa          	movaps %xmm0,(%edx,%edi,8)
  4b:	0f c2 c0 04          	cmpneqps %xmm0,%xmm0
  4f:	0f 50 c0             	movmskps %xmm0,%eax
  52:	85 c0                	test   %eax,%eax
  54:	75 1d                	jne    73 <sse3_mult+0x73> // inlined comp_mult
  56:	83 c7 02             	add    $0x2,%edi
  59:	83 c6 10             	add    $0x10,%esi
  5c:	83 c3 10             	add    $0x10,%ebx
  5f:	83 c1 10             	add    $0x10,%ecx
  62:	83 45 e4 10          	addl   $0x10,-0x1c(%ebp)
  66:	39 7d 14             	cmp    %edi,0x14(%ebp)
  69:	7f bd                	jg     28 <sse3_mult+0x28>
...

the 4 adds for esi ebx ecx and ebp are completely unnecessary and reduce performance by about 20% on my core2duo.
on amd64 it also creates to seemingly unnecessary additions but I did not test the performance.

a way to coax gcc to emit proper code is to not allow it to inline the fallback
it then generates following good assembly with only one integer add:

  a8:	0f 28 0c df          	movaps (%edi,%ebx,8),%xmm1
  ac:	f3 0f 12 c1          	movsldup %xmm1,%xmm0
  b0:	8b 45 08             	mov    0x8(%ebp),%eax
  b3:	0f 28 14 de          	movaps (%esi,%ebx,8),%xmm2
  b7:	f3 0f 16 c9          	movshdup %xmm1,%xmm1
  bb:	0f 59 c2             	mulps  %xmm2,%xmm0
  be:	0f c6 d2 b1          	shufps $0xb1,%xmm2,%xmm2
  c2:	0f 59 ca             	mulps  %xmm2,%xmm1
  c5:	f2 0f d0 c1          	addsubps %xmm1,%xmm0
  c9:	0f 29 04 d8          	movaps %xmm0,(%eax,%ebx,8)
  cd:	0f c2 c0 04          	cmpneqps %xmm0,%xmm0
  d1:	0f 50 c0             	movmskps %xmm0,%eax
  d4:	85 c0                	test   %eax,%eax
  d6:	75 10                	jne    e8 <sse3_mult+0x58> // non-inlined comp_mult
  d8:	83 c3 02             	add    $0x2,%ebx
  db:	39 5d 14             	cmp    %ebx,0x14(%ebp)
  de:	7f c8                	jg     a8 <sse3_mult+0x18>
...


---


### compiler : `gcc`
### title : `strcpy/strcat builtins for constant strings generates suboptimal code.`
### open_at : `2013-02-04T08:40:55Z`
### last_modified_date : `2021-08-16T05:28:03Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=56199
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `target`
### version : `unknown`
### severity : `normal`
### contents :
Current strcpy/strcat generates code in form 

movabsq $7954893459765158241, %r11
movq %r11,(%rax)
...

Which is slower than copying string from memory using

movq (%rdx),%r11
movq %r11,(%rax)
...

Attached benchmark is 50% faster on sandy bridge for 70 byte string.

Note that icc also translates strcpy into this form(but not strcat for some reason.)


---


### compiler : `gcc`
### title : `queens benchmark is faster with -O0 than with any other optimization level`
### open_at : `2013-02-04T10:40:52Z`
### last_modified_date : `2021-09-04T20:36:06Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=56200
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.8.0`
### severity : `normal`
### contents :
Created attachment 29346
queens benchmark

While preparing some teaching slides I have noticed that the queens benchmark from Aburto generates slower code with -O1/O2/O3 than with plain -O0.  I've removed all timing routines from the attached file, compile and run it with ./a.out 30.

For 4.7.1 of OpenSUSE 12.2, we have:

$ time ./o0 30 >/dev/null
user    0m10.017s

$ time ./o1 30 >/dev/null
user    0m11.824s

$ time ./o2 30 >/dev/null
user    0m10.388s

$ time ./o3 30 >/dev/null  //this one is with -march=native
user    0m11.065s

For today's 4.8, 

$ time ./o048 30 >/dev/null
user    0m9.780s

$ time ./o148 30 >/dev/null
user    0m12.590s

$ time ./o248 30 >/dev/null //this one is with -march=native
user    0m10.487s

$ time ./o348 30 >/dev/null //this one is with -march=native
user    0m10.850s

Perf shows that in the -O1 versions of above we have the new lea that has a lot of counter hits and lots more of branch mispredictions.


---


### compiler : `gcc`
### title : `invalid -Warray-bounds warning`
### open_at : `2013-02-05T00:25:27Z`
### last_modified_date : `2022-10-31T23:47:50Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=56210
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.0`
### severity : `normal`
### contents :
The following code evokes what looks like an invalid warning with -Warray-bounds.
It is independent of char signedness (same with -funsigned-char or with -fsigned-char), so should be different from bug#35903.

$ cat k.c
#include <string.h>
#include <stdio.h>

void
f (void)
{
    char *p = ";";
    while (*p) {
        static char key[] = "abc";
        if (strncmp(p, key, 3) == 0) {
            p += 3;
            printf("%s\n", p);
            return;
        }
        if ((p = strchr(p, ';')) == NULL)
            return;
        p++;
    }
}
$ gcc -save-temps -O2 -Wall -c k.c
k.c: In function 'f':
k.c:12:19: warning: array subscript is above array bounds [-Warray-bounds]
             printf("%s\n", p);
                   ^
$ gcc -v
Using built-in specs.
COLLECT_GCC=/p/bin/gcc
COLLECT_LTO_WRAPPER=/p/p/gcc-2013-01-16.09h15/libexec/gcc/x86_64-unknown-linux-gnu/4.8.0/lto-wrapper
Target: x86_64-unknown-linux-gnu
Configured with: /h/j/w/co/gcc/configure --prefix=/p/p/gcc-2013-01-16.09h15 --enable-languages='c++ go'
Thread model: posix
gcc version 4.8.0 20130116 (experimental) (GCC)


Attaching the .i file momentarily...


---


### compiler : `gcc`
### title : `Integer ABS is not recognized for more complicated pattern`
### open_at : `2013-02-06T11:39:43Z`
### last_modified_date : `2023-05-06T21:19:32Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=56223
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.0`
### severity : `enhancement`
### contents :
In one important benchmark the following ABS pattern which is not recognized by gcc was found:

   if (x >= 0)
      s += x;
   else
      s -= x;
that certainly should be converted to ABS as e.g. icc does.

In result the loop containing this pattern is not vectorized on x86 and arm.

I attached simple test-case to reproduce it.

If we complile it for atom with options " -O3 -m32 -march=atom2 -mtune=atom2 -ffast-math -msse2 -mfpmath=sse -ftree-vectorizer-verbose=2" we got:

...
t5.c:1: note: vectorized 0 loops in function.
...
t5.c:15: note: vectorized 1 loops in function.


---


### compiler : `gcc`
### title : `fp-contract does not work with SSE and AVX FMAs (neither FMA4 nor FMA3)`
### open_at : `2013-02-08T12:14:36Z`
### last_modified_date : `2019-05-22T08:15:48Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=56253
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.7.2`
### severity : `normal`
### contents :
Take the following testcase:

#include <immintrin.h>
__m256 foo(__m256 a, __m256 b, __m256 c)
{  
    return _mm256_add_ps(_mm256_mul_ps(a, b), c);
}
__m128 foo(__m128 a, __m128 b, __m128 c)
{  
    return _mm_add_ps(_mm_mul_ps(a, b), c);
}
float foo(float a, float b, float c)
{  
    return a * b + c;
}

compiled with 'g++ -O3 -mfma -ffp-contract=fast -fabi-version=0 -c' only the third function uses fmas (same for -mfma4). The SSE and AVX variant should make the same contraction as is implemented for scalar operations.


---


### compiler : `gcc`
### title : `missed VRP optimization on i for signed i << n from undefined left shift in ISO C`
### open_at : `2013-02-11T00:55:56Z`
### last_modified_date : `2023-09-28T14:29:39Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=56281
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.8.0`
### severity : `enhancement`
### contents :
It seems that GCC is unaware that a left shift is undefined in ISO C99 when it yields an integer overflow. See the following testcase with -O3 -std=c99:

int foo (int i)
{
  if (i < 0)
    i = -i;
  i *= 2;
  if (i < 0)
    i++;
  return i;
}

int bar (int i)
{
  if (i < 0)
    i = -i;
  i <<= 1;
  if (i < 0)
    i++;
  return i;
}

GCC optimizes foo() at the .065t.vrp1 step, but not bar().


---


### compiler : `gcc`
### title : `conditional moves instead of compare and branch result in almost 2x slower code`
### open_at : `2013-02-13T20:21:06Z`
### last_modified_date : `2021-09-04T20:33:09Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=56309
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.7.2`
### severity : `normal`
### contents :
Created attachment 29442
Self contained source file with parameter x passed by value (slow)

This bug report reflects the analysis of a question asked in stackoverflow

http://stackoverflow.com/questions/14805641/why-does-changing-const-ull-to-const-ull-in-function-parameter-result-in-pe/14819939#14819939

When an unsigned long long parameter to a function is passed by reference instead of by value the result is a dramatic almost 2x improvement in speed when compiled with -O3.  Given that the function is inlined this is unexpected.  Upon closer inspection it was found that the code generated is quite different, as if passing the parameter by value enables an optimization (use of x86 conditional moves) that backfires, possibly by suffering an unexpected stall in the processor.

Two files are attached

by-val-O3.ii
by-ref-O3.ii

They differ only in the way the unsigned long long parameter "x" is passed.

./by-ref-O3
Took 11.85 seconds total.

./by-ref-O3
Took 6.67 seconds total.


---


### compiler : `gcc`
### title : `Please allow per-function specification of register conventions`
### open_at : `2013-02-14T01:55:40Z`
### last_modified_date : `2022-10-03T16:20:30Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=56314
### status : `NEW`
### tags : `missed-optimization, ra`
### component : `middle-end`
### version : `4.8.0`
### severity : `enhancement`
### contents :
gcc allows register specifications (saved, clobbered, reserved) to be changed on a per-file basis.  However, for optimization uses it would be much more useful if they could be defined on a per-function basis using attributes, just as calling conventions can be specified with attributes.

In the Linux kernel world we currently have several uses of functions with ad hoc calling conventions.  We have to wrap them in assembly wrappers, and either write them in assembly or put them in separate files with the calling convention specified with compiler options.


---


### compiler : `gcc`
### title : `Simplify testing of related conditions in for loop`
### open_at : `2013-02-15T22:36:20Z`
### last_modified_date : `2021-08-07T23:30:13Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=56352
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.0`
### severity : `normal`
### contents :
If we have a loop like this:

for (i = 0; i < a && i < b; i++)
{
  /* Code which cannot affect i, a, or b */
}

gcc should be able to optimize this into:

tmp = MIN(a,b)
for (i = 0; i < tmp; i++)
{
  /* Body */
}

But it does not.  Similarly, code like:

for (i = 0; i < a; i++)
{
  if (i >= b)
    break;

  /* Code which cannot affect i, a, or b */
}

Should be similarly optimized.


---


### compiler : `gcc`
### title : `abs and multiplication`
### open_at : `2013-02-16T12:00:08Z`
### last_modified_date : `2023-05-03T06:12:45Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=56355
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.0`
### severity : `enhancement`
### contents :
#include <cmath>
#include <cstdlib>
typedef double T;
// typedef int T;
T f(T a, T b){
  return std::abs(a)*std::abs(b);
}
T g(T a){
  return std::abs(a)*std::abs(a);
}
T h(T a){
  return std::abs(a*a);
}

Compiled with g++ -O3 (-ffast-math doesn't help), g is properly optimized to a*a but only at the RTL level, and the other 2 are not optimized at all. If I make T a typedef for int, nothing is optimized.

For the first one, I would expect abs(a*b), and for the others just a*a.

Related to PR 31548.


---


### compiler : `gcc`
### title : `Missed opportunity to combine comparisons with zero`
### open_at : `2013-02-17T22:31:50Z`
### last_modified_date : `2021-07-26T21:42:30Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=56369
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.0`
### severity : `enhancement`
### contents :
I'm not sure whether this is really a tree-optimization or middle-end (e.g. combine) issue...

With rev 196091 the following example:

extern int func_10 (void*);

int
func_11 (void* x)
{
 int status = 0;

 do
 {
   status = func10 (x);
   status = status < 0 ? status : 0;
 } while (status >= 0);

 return status;
}

compiled for SH4 with -O2 -m4 results in:
_func_11:
        mov.l   r8,@-r15
        mov.l   r9,@-r15
        mov     r4,r9
        mov.l   .L8,r8
        sts.l   pr,@-r15
        .align 2
.L4:
        jsr     @r8
        mov     r9,r4

        cmp/pl  r0      // T = r0 > 0
        bt/s    .L4
        tst     r0,r0   // T = r0 == 0
        bt      .L4

        lds.l   @r15+,pr
        mov.l   @r15+,r9
        rts
        mov.l   @r15+,r8
.L9:
        .align 2
.L8:
        .long	_func10


As seen above, the two comparisons could be done with a single one:
  cmp/pz  r0   // T = r0 >= 0

I've tried out a few SH specific things to see if combine would do it, but it just won't combine the two.  I guess because the two comparisons end up in two different basic blocks.

On ARM, there's a smin insn defined, but the problem is the similar.  The example above compiled with -O2 results in:

func_11:
        stmfd	sp!, {r4, lr}
        mov	r4, r0
.L3:
        mov	r0, r4
        bl	func10

        and	r0, r0, r0, asr #31	// smin (r0, 0)
        cmp	r0, #0                  // r == 0
        beq	.L3
        ldmfd	sp!, {r4, lr}
        bx	lr

which could be done without the smin (r0, 0), and save the and insn:

func_11:
	stmfd	sp!, {r4, lr}
	mov	r4, r0
.L3:
	mov	r0, r4
	bl	func10

	cmp	r0, #0
	bge	.L3
	ldmfd	sp!, {r4, lr}
	bx	lr


---


### compiler : `gcc`
### title : `extra register moves for global register and local register variables`
### open_at : `2013-02-25T02:32:02Z`
### last_modified_date : `2023-05-26T02:33:00Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=56439
### status : `NEW`
### tags : `missed-optimization, ra`
### component : `middle-end`
### version : `4.7.2`
### severity : `normal`
### contents :
I am writing some interrupt code for an Atmel AVR microcontroller and I'm trying to shave cycles off, specifically at the beginning of the interrupt. I want to achieve this by minimizing the registers that need to be saved, so I decided to declare a few variables as global register variables.

What I found is that GCC will "optimize away" the register assignment and instead produce code that is almost what I want, except it copies the value in and out of another register (allocated the usual way) instead of operating on the assigned one.

For example the following C:

register unsigned char foo asm ("r4");

void baz();
void quux();

void bar() {
  foo = foo * 2;
  if (foo > 10)
    baz();
  else
    quux();
}

generates the following assembly:

        mov r24,r4
        lsl r24
        mov r4,r24
        cpi r24,lo8(11)
        brsh .L4
        rjmp quux
.L4:
        rjmp baz


It does the same thing (copy to r24, manipulate, copy back) on every optimization level.

Surely this can't be desired behavior? If you use local register variables it's often even worse, as gcc won't touch the assigned register at all but instead produce identical code that uses a different register.

I'm fairly certain this shouldn't work this way...


---


### compiler : `gcc`
### title : `-mveclibabi=... Support AMD's LibM 3.0 (sucessor of ACML)`
### open_at : `2013-03-01T21:58:40Z`
### last_modified_date : `2021-10-03T09:25:06Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=56504
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.8.0`
### severity : `enhancement`
### contents :
GCC currently supports:

       -mveclibabi=type
           Specifies the ABI type to use for vectorizing intrinsics
           [...] and acml for the AMD math core library. [...]

           [...]    and "__vrd2_sin",
           "__vrd2_cos", "__vrd2_exp", "__vrd2_log", "__vrd2_log2",
           "__vrd2_log10", "__vrs4_sinf", "__vrs4_cosf", "__vrs4_expf",
           "__vrs4_logf", "__vrs4_log2f", "__vrs4_log10f" and
           "__vrs4_powf" for the corresponding function type when
           -mveclibabi=acml is used.

The current AMD LibM version, however, supports much more:
http://developer.amd.com/tools/cpu-development/libm/


From the release notes:

Vector Functions 
----------------
         Exponential
         -----------
            * vrs4_expf, vrs4_exp2f, vrs4_exp10f, vrs4_expm1f
            * vrsa_expf, vrsa_exp2f, vrsa_exp10f, vrsa_expm1f
            * vrd2_exp, vrd2_exp2, vrd2_exp10, vrd2_expm1
            * vrda_exp, vrda_exp2, vrda_exp10, vrda_expm1

         Logarithmic
         -----------
            * vrs4_logf, vrs4_log2f, vrs4_log10f, vrs4_log1pf
            * vrsa_logf, vrsa_log2f, vrsa_log10f, vrsa_log1pf
            * vrd2_log, vrd2_log2, vrd2_log10, vrd2_log1p
            * vrda_log, vrda_log2, vrda_log10, vrda_log1p

         Trigonometric
         -------------
            * vrs4_cosf, vrs4_sinf
            * vrsa_cosf, vrsa_sinf
            * vrd2_cos, vrd2_sin
            * vrda_cos, vrda_sin
            * vrd2_sincos,vrda_sincos
            * vrs4_sincosf,vrsa_sincosf 
            * vrd2_tan, vrs4_tanf
            * vrd2_cosh
            

         Power
         -----
            * vrs4_cbrtf, vrd2_cbrt, vrs4_powf, vrs4_powxf
            * vrsa_cbrtf, vrda_cbrt, vrsa_powf, vrsa_powxf
            * vrd2_pow


The vector functions are the known (cf. include/amdlibm.h):
    __m128d amd_vrd2_exp    (__m128d x);
    __m128  amd_vrs4_expf   (__m128  x);
    etc.

While the array version use:
    void amd_vrsa_expf      (int len, float  *src, float  *dst);
    void amd_vrda_exp2      (int len, double *src, double *dst);

    void amd_vrda_exp       (int len, double *src, double *dst);
    void amd_vrsa_expf      (int len, float  *src, float  *dst);

Unfortunately, no further documentation is available, telling whether, e.g., src and dst may be the same or not.



Note that AMD LibM now uses "amd_" as prefix to the vector functions. It contains the old version as weak symbols but only those:

0000000000000340 W __vrd2_cos
00000000000000e0 W __vrd2_exp
00000000000001a0 W __vrd2_log
00000000000001c0 W __vrd2_log10
00000000000001b0 W __vrd2_log2
0000000000000330 W __vrd2_sin
0000000000000390 W __vrs4_cosf
00000000000000a0 W __vrs4_expf
0000000000000200 W __vrs4_log10f
00000000000001f0 W __vrs4_log2f
00000000000001e0 W __vrs4_logf
00000000000003a0 W __vrs4_sinf


---


### compiler : `gcc`
### title : `vectorizaton fails in conditional assignment of a constant`
### open_at : `2013-03-05T16:44:14Z`
### last_modified_date : `2021-12-12T10:52:23Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=56541
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.0`
### severity : `normal`
### contents :
this loop does not vectorize

#include<cmath>
float a,b,c,d;

float z[1024]; bool ok[1024];
constexpr float rBig = 150.;

void foo() {
  for (int i=0;i!=1024;++i) {
    float rR = a*z[i];
    float rL = b*z[i];
    float rMin = (rR<rL) ? rR : rL;  
    float rMax = (rR<rL) ? rL : rR;  
    //rMin = (rMax>0) ? rMin : rBig+std::abs(z[i]); // this vectorize (sic...)
    rMin = (rMax>0) ? rMin : rBig; // comment to vectorize
    rMin = (rMin>0) ? rMin : rMax; 
    ok[i] = rMin-c<rMax+d;
  }

}

c++ -std=c++11 -Ofast -march=corei7 -c range.cc -ftree-vectorizer-verbose=1

Analyzing loop at range.cc:8
range.cc:7: note: vectorized 0 loops in function.
range.cc:16: note: vect_recog_bool_pattern: detected: 
range.cc:16: note: pattern recognized: VIEW_CONVERT_EXPR<unsigned char>(ok[i_22]) = patt_15;
range.cc:16: note: additional pattern stmt: patt_13 = _14 < _16 ? 1 : 0;

adding to "rBig" std::abs(z[i]) it does
c++ -std=c++11 -Ofast -march=corei7 -c range.cc -ftree-vectorizer-verbose=1

Analyzing loop at range.cc:8

range.cc:8: note: vect_recog_bool_pattern: detected: 
range.cc:8: note: pattern recognized: VIEW_CONVERT_EXPR<unsigned char>(ok[i_24]) = patt_16;

range.cc:8: note: additional pattern stmt: patt_14 = _15 < _17 ? 1 : 0;


Vectorizing loop at range.cc:8

range.cc:8: note: LOOP VECTORIZED.
range.cc:7: note: vectorized 1 loops in function.


---


### compiler : `gcc`
### title : `missed opportunity for FMA with -ffast-math`
### open_at : `2013-03-06T01:02:36Z`
### last_modified_date : `2023-05-02T19:09:46Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=56547
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.0`
### severity : `enhancement`
### contents :
This one was mentioned in PR 55295:

float test (float a, float b)
{
  return a * b + a;
}

compiled with -m4-single -O2 -ffast-math results in:

        fldi1   fr0     ! 7     movsf_ie/4      [length = 2]
        fadd    fr5,fr0 ! 8     addsf3_i        [length = 2]
        rts             ! 27    *return_i       [length = 2]
        fmul    fr4,fr0 ! 9     mulsf3_i        [length = 2]

At least on SH using fmac in this case would be better than transforming
'a * b + a' into '(1 + b) * a'.  Not sure yet whether this is actually target specific.


---


### compiler : `gcc`
### title : `False "may be uninitialized variable" warning (&& converted to &)`
### open_at : `2013-03-08T19:09:36Z`
### last_modified_date : `2022-03-16T08:39:40Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=56574
### status : `ASSIGNED`
### tags : `diagnostic, missed-optimization`
### component : `tree-optimization`
### version : `4.7.0`
### severity : `normal`
### contents :
The following code produces the warning,'value' may be used uninitialized:

int get_value(void);

void show_problem(int flag)
{
	int value;

	if (!flag)
		value = get_value();

	for (;;) {
		if (!flag && value)
			continue;

		if (!flag)
			break;
	}
}

The warning occurs only with -O1 and -O2 optimization. -O0 and -O3 and higher do not. It also occurs with many versions. I have gotten the same result with the following versions of gcc:

i686-apple-darwin10-gcc-4.2.1 (GCC) 4.2.1 (Apple Inc. build 5664)
gcc (SUSE Linux) 4.3.4 [gcc-4_3-branch revision 152973]
gcc (GCC) 4.4.6 20110731 (Red Hat 4.4.6-3)
gcc (GCC) 4.7.0 20120507 (Red Hat 4.7.0-5)

Interestingly, the much larger function that originally displayed the problem does not generate a warning with the 4.7.0 compiler, but does on the others.


---


### compiler : `gcc`
### title : `Replace auto-inc-dec pass with generic address mode selection pass`
### open_at : `2013-03-10T17:05:28Z`
### last_modified_date : `2023-07-22T03:07:15Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=56590
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.8.0`
### severity : `enhancement`
### contents :
At least on SH there are several address mode selection issues which I'd like to group in this PR.

PR 54065
[SH] Prefer @(R0,Rn) addressing for floating-point load/store

PR 53911
[SH] Improve displacement addressing

PR 50749
Auto-inc-dec does not find subsequent contiguous mem accesses

PR 39423
[4.6/4.7/4.8 Regression] [SH] performance regression: lost mov @(disp,Rn)

PR 52049
SH Target: Inefficient constant address access

Based on my observations so far, I think the right thing to do is to replace the current auto-inc-dec pass with a pass that optimizes address mode selection in a more generic way, instead of just trying to find auto inc/dec opportunities.

The basic idea is to look at all memory accesses in a function (or basic block as a start) that share a base address and then try to select the cheapest addressing modes for each memory access.  The current address cost target hook can be used to determine the costs of a memory access with a particular address.

I have already started working on such a replacement pass a while ago and would like to first do a trial with the SH target.  Other targets might then also pick it up if it seems beneficial to do so.


---


### compiler : `gcc`
### title : `basic-block vectorization does not replace all scalar uses`
### open_at : `2013-03-13T10:50:05Z`
### last_modified_date : `2023-08-09T13:03:32Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=56612
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.0`
### severity : `normal`
### contents :
When vectorizing stmts in a basic-block we do not verify that the SLP
instance covers all uses of the definitions the stmts in the SLP tree.
This can easily result in both the scalar and vectorized set of stmts
being kept live and executed.

See PR56608 for an example (trivial re-use of the SLP roots stored values).


---


### compiler : `gcc`
### title : `duplicated sse code in switch`
### open_at : `2013-03-16T11:34:51Z`
### last_modified_date : `2021-12-05T10:37:12Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=56631
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `unknown`
### severity : `normal`
### contents :
Consider attached testcase. When compiled with -Os,-O2,-O3 it duplicates zeroing xmm1 register across all branches. Moving zeroing before braches will save space.

Relevant assembly at -Os is

  jmp *.L19(,%rax,8)
  .section  .rodata
  .align 8
  .align 4
.L19:
  .quad .L21
  .quad .L4
  .quad .L5
snip 

.L21:
  xorps %xmm1, %xmm1
.L38:
  movaps  %xmm0, %xmm2
  pcmpeqb %xmm1, %xmm2
  pmovmskb  %xmm2, %eax
  testl %eax, %eax
  jne .L1
.L2:
  movdqu  %xmm0, (%rdi)
  addq  $64, %rdi
  movups  64(%rsi), %xmm0
  addq  $64, %rsi
  jmp .L38
.L4:
  xorps %xmm1, %xmm1
  incq  %rdi
.L23:
snip
.L5:
  xorps %xmm1, %xmm1
  addq  $2, %rdi


---


### compiler : `gcc`
### title : `static/saved variables prevent loop vectorization.`
### open_at : `2013-03-22T10:48:29Z`
### last_modified_date : `2021-10-01T18:23:13Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=56688
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `normal`
### contents :
Analyzing gcc vectorization on 200.sixtrack from spec2000 suite we found out that only 6 loops are vectorized in the hottest routine (97% run time). The reason is that save statement is used. This issue can be illustrated by the following simple example:

	subroutine bar
	implicit real*8 (a-h,o-z)
	parameter (n=700)
	common/my_data/ x1(n), y1(n), z1(n), t1(n)
        save
	do i=1,n
	x = x1(i) - y1(i)
	z1(i) = t1(i) * x
	enddo
	end

and vectorizer issues the following message:

t1.f:6: note: ==> examining statement: _6 = my_data.x1[_5];

t1.f:6: note: num. args = 4 (not unary/binary/ternary op).
t1.f:6: note: vect_is_simple_use: operand my_data.x1[_5]
t1.f:6: note: not ssa-name.
t1.f:6: note: use not simple.
t1.f:6: note: vect_model_load_cost: aligned.
t1.f:6: note: vect_model_load_cost: inside_cost = 1, prologue_cost = 0 .
t1.f:6: note: vect_is_simple_use: operand my_data.x1
t1.f:6: note: not ssa-name.
t1.f:6: note: use not simple.
t1.f:6: note: not vectorized: live stmt not supported: _6 = my_data.x1[_5];

Note also if we comment down svae stmt loop will be vectorized.


---


### compiler : `gcc`
### title : `missed optimization for __uint128_t of (unsigned long long)x != x`
### open_at : `2013-03-24T15:30:11Z`
### last_modified_date : `2023-06-13T06:17:21Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=56711
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.7.2`
### severity : `enhancement`
### contents :
Consider this function:

size_t scan_ulong(const char* src,unsigned long int* dest) {
  register const char *tmp=src;
  register unsigned long int l=0;
  register unsigned char c;
  while ((c=*tmp-'0')<10) {
    __uint128_t x=(__uint128_t)l*10+c;
    if ((unsigned long)x != x) break;
    l=(unsigned long)x;
    ++tmp;
  }
  if (tmp-src) *dest=l;
  return tmp-src;
}

I'm compiling this with gcc -Os -c test.c on an amd64-linux box.
The code gcc generates is 92 bytes long, the one from clang only 65.  What is happening here?  What are all that code doing that gcc is generating there?


---


### compiler : `gcc`
### title : `Enhance Dot-product pattern recognition to avoid mult widening.`
### open_at : `2013-03-25T10:01:05Z`
### last_modified_date : `2021-07-21T03:19:01Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=56717
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `enhancement`
### contents :
Comparing performance of icc and gcc compilers we found out that for one important benchmark from eembc 1.1 suite gcc produces very poor code in comparison with icc. This deficiency can be illustrated by the following simple example:

typedef signed short s16;
typedef signed long  s32;
void bar (s16 *in1, s16 *in2, s16 *out, int n, s16 scale)
{
  int i;
  s32 acc = 0;
  for (i=0; i<n; i++)
    acc += ((s32) in1[i] * (s32) in2[i]) >> scale;
  *out = (s16) acc;
}
gcc performes mult widening conversion for it which does not look reasonable and leads to suboptiml code for x86 at least.

I assume that Dot-prodeuct pattern recognition can be simply enhanced to accept such case by allowing the following stmts:

     type x_t, y_t;
     TYPE1 prod;
     TYPE2 sum = init;
   loop:
     sum_0 = phi <init, sum_1>
     S1  x_t = ...
     S2  y_t = ...
     S3  x_T = (TYPE1) x_t;
     S4  y_T = (TYPE1) y_t;
     S5  prod = x_T * y_T;
     [S6  prod = (TYPE2) prod;  #optional]
     S6' prod1 = prod1 <bin-op> <opnd>
     S7  sum_1 = prod1 + sum_0;

where S6' is vectorizable.


---


### compiler : `gcc`
### title : `missed optimization: i > 0xffff || i*4 > 0xffff`
### open_at : `2013-03-25T11:27:43Z`
### last_modified_date : `2021-08-01T18:12:48Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=56719
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.7.2`
### severity : `enhancement`
### contents :
This is the test code:

int foo(unsigned int i) {
  if (i > 0xffff || i*4 > 0xffff)
    baz();
}

gcc -O2 generates a cmp, a shift, and another cmp.

Why does this not generate a single cmp with 0x3fff?


---


### compiler : `gcc`
### title : `i386: MALLOC_ABI_ALIGNMENT is too small (usually)`
### open_at : `2013-03-25T19:10:54Z`
### last_modified_date : `2021-10-15T20:44:27Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=56726
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.9.0`
### severity : `normal`
### contents :
Observed malloc alignment for the i386 ABI is double POINTER_SIZE.  BITS_PER_WORD, the current default, is usually too small.  (It's right only on X32.)

Proposed patch:

--- gcc/config/i386/i386.h      (revision 197055)
+++ gcc/config/i386/i386.h      (working copy)
@@ -815,6 +815,14 @@
    x86_field_alignment (FIELD, COMPUTED)
 #endif
 
+/* The maximum alignment 'malloc' honors.
+
+   This value is taken from glibc documentation for memalign().  It may
+   be up to double the very conservative GCC default.  This should be safe,
+   since even the GCC 4.8 default of BIGGEST_ALIGNMENT usually worked.  */
+
+#define MALLOC_ABI_ALIGNMENT (POINTER_SIZE * 2)
+
 /* If defined, a C expression to compute the alignment given to a
    constant that is being placed in memory.  EXP is the constant
    and ALIGN is the alignment that the object would ordinarily have


---


### compiler : `gcc`
### title : `Epilogue loop not partly vectorized`
### open_at : `2013-03-26T14:10:27Z`
### last_modified_date : `2021-10-01T02:51:51Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=56741
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `normal`
### contents :
Created attachment 29730
Reproducer

Hi guys,
Suppse we vectorize loop with AVX[2].
E.g.:
do i=0..N-1, ++i
  stmt [i];
enddo

If vectorization is allowed & possible we'll have something like

rem = N % VL /* VL is vector length.  */
/* Vectorized loop.  */
do i=0..N-rem-1, i+=VL
  v_stmt [i..i+VL];
enddo

/* Remainder.  */
do j=0..rem, ++j
  stmt [j+i];
enddo

Remainder maybe unrolled, if allowed.

For 128-bit vectors, we have remainder of 3 for floats and 1 for doubles maximum iterations.

For 256-bit vectors this number of iterations is 7 and 3 correspondingly.

Attached test shows 30% increase in instruction count because of loop remainder maximum iterations count.

Why for AVX[2] not to add one iteration on 128-bit registers, having 3 and 1 iteration is remainder?

Like this (necessary checks are omitted):

rem_1 = N % VL1 /* VL1 is widest vector length - 256-bit.  */
/* Vectorized loop.  */
do i=0..N-rem_1-1, i+=VL1
  v1_stmt[i..i+VL1]; /* Vectorized with 256-bit vector.  */
enddo

/* Additional iteration.  */
v2_stmt [i..(i+VL2)]; /* Vectorized with 128-bit vector.  */

rem_2 = rem_1-VL2; /* VL2 is narrow vector length - 128-bit.  */

/* Remainder.  */
do j=0..rem_2, ++j
  stmt[j+i];
enddo


Here is how to reproduce:
$ gcc -static -m64 -fstrict-aliasing -fno-prefetch-loop-arrays -Ofast -funroll-loops -fwhole-program -msse4 ./loop_vers.c -o loop_sse

$ gcc -static -m64 -fstrict-aliasing -fno-prefetch-loop-arrays -Ofast -funroll-loops -fwhole-program -mavx ./loop_vers.c -o loop_avx

$ sde -icount -- ./loop_sse 7
0.000000$$ TID: 0 ICOUNT: 16001317

$ sde -icount -- ./loop_avx 7
0.000000$$ TID: 0 ICOUNT: 20847322


---


### compiler : `gcc`
### title : `Partial sums loop optimization`
### open_at : `2013-03-28T19:45:27Z`
### last_modified_date : `2021-08-29T01:58:05Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=56770
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.9.0`
### severity : `enhancement`
### contents :
GCC loop optimization should unroll and transform loops using partial sums where beneficial for expensive, independent computations where the target has additional function units available.

Before

    double fValue = 0;
    int j;
    for (j = 0; j < NZ; j++)
        fValue += Q[j] / r[j];

After

    double fValue = 0;
    double fValue1 = 0;
    int j;
    for (j = 0; j < NZ; j=j+2){
        fValue += Q[j] / r[j];
        fValue1 += Q[j+1] / r[j+1];
    }

    for (j = (NZ/2)*2; j < NZ; j++){
        fValue += Q[j] / r[j];
    }

    fValue = fValue + fValue1;


---


### compiler : `gcc`
### title : `cmpnltpd recognition`
### open_at : `2013-04-07T14:15:54Z`
### last_modified_date : `2021-07-29T23:16:24Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=56863
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.9.0`
### severity : `enhancement`
### contents :
Hello,

I was looking at this program, trying to get it to generate cmpnltpd:

#include <x86intrin.h>
__m128d f(__m128d a, __m128d b){
  return (__m128d)(~(a<b));
}

but it doesn't:

	cmpltpd	%xmm1, %xmm0
	pcmpeqd	%xmm1, %xmm1
	pxor	%xmm0, %xmm1
	movapd	%xmm1, %xmm0

One reason seems to be that the instruction is modeled as (unge a b), whereas from a trapping point of view I think it should be (not (lt a b)). But even -ffast-math does not help.

As a side note, notice that:

  return (__m128d)((a<b)?0:(__m128i){-1,-1});

uses pandn instead of pxor to generate the negation. I don't think one is better than the other, I was just surprised to see the difference.


---


### compiler : `gcc`
### title : `vector shift lowered to scalars for -mxop`
### open_at : `2013-04-08T11:39:21Z`
### last_modified_date : `2021-08-25T03:02:10Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=56873
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.9.0`
### severity : `normal`
### contents :
#define SIZE 32
typedef long long veci __attribute__((vector_size(SIZE)));

veci f(veci a, veci b){
  return a>>b;
}

Compiling this with -O3 -mxop, the vector lowering pass gives scalar operations. However, if SIZE is either 16 or 64, I get vector shifts of size 16.


---


### compiler : `gcc`
### title : `Combine does not invent new moves`
### open_at : `2013-04-08T14:23:58Z`
### last_modified_date : `2021-12-27T05:47:26Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=56876
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.9.0`
### severity : `enhancement`
### contents :
Hello,

I am looking at this testcase:

typedef unsigned long long vec __attribute__((vector_size(16)));
vec g;
vec f1(vec a, vec b){
  return ~a&b;
}
vec f2(vec a, vec b){
  return ~g&b;
}

which compiles to:

f1:
	pandn	%xmm1, %xmm0

f2:
	pcmpeqd	%xmm0, %xmm0
	pxor	g(%rip), %xmm0
	pand	%xmm1, %xmm0

whereas I would like to get, like I do with the _mm_andnot_si128 builtin:

	movdqa	g(%rip), %xmm0
	pandn	%xmm1, %xmm0

It seems that combine cannot match the pandn pattern because the first argument is a memory load and not a register. In this case, it would be better if it emitted a move to put it in a register so it can match, instead of giving up. I don't know if there is a good way to characterize such situations where an extra move is worth it.


---


### compiler : `gcc`
### title : `Folding of checks into a range check should check upper boundary`
### open_at : `2013-04-11T18:29:21Z`
### last_modified_date : `2021-07-26T22:12:31Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=56924
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.9.0`
### severity : `normal`
### contents :
When we are performing folding of checks into a range check, if the values are at the top-end of the range we should just use a > test instead of normalizing them into the bottom of the range and using a < test.

For example, consider:

  struct stype {
    unsigned int pad:4;
    unsigned int val:4;
  };

  void bar (void);

  void foo (struct stype input)
  {
    if ((input.val == 0xe) || (input.val == 0xf))
      bar();
  }


When compiled at -O2, the original tree generated is:


  ;; Function foo (null)
  ;; enabled by -tree-original
  
  
  {
    if (input.val + 2 <= 1)
      {
        bar ();
      }
  }

This is likely to be more efficient if we instead generate:

    if (input.val >= 0xe)
      {
        bar ();
      }

This can be seen in the inefficient codegen for an ARM cortex-a15:

        ubfx    r0, r0, #4, #4
        add     r3, r0, #2
        and     r3, r3, #15
        cmp     r3, #1

(the add and the and are not necessary if we change the test condition).

I was able to improve this by adding detection of this case into build_range_check.


---


### compiler : `gcc`
### title : `SRA should take into account likelihood of statements being executed`
### open_at : `2013-04-11T18:58:50Z`
### last_modified_date : `2023-08-04T21:18:08Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=56925
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `enhancement`
### contents :
In the following code:

  struct stype {
    unsigned int pad:4;
    unsigned int val:4;
  };

  void bar (void);
  void baz (void);

  int x, y;

  unsigned int foo (struct stype input)
  {
    if (__builtin_expect (x, 0))
      return input.val;

    if (__builtin_expect (y, 0))
      return input.val + 1;

    return 0;
  }

When compiled with -O2, SRA moves the read of input.val to the top of the function:


  ;; Function foo (foo, funcdef_no=0, decl_uid=4988, cgraph_uid=0)
  
  Candidate (4987): input
  Rejected (4999): not aggregate: y.1
  Rejected (4993): not aggregate: x.0
  Created a replacement for input offset: 4, size: 4: input$val
  ...

  <bb 2>:
  input$val_14 = input.val;
  x.0_3 = x;
  _4 = __builtin_expect (x.0_3, 0);
  if (_4 != 0)
    goto <bb 3>;
  else
    goto <bb 4>;
  ...

Which means that the critical path for this function now executes an extra instruction.

It would be nice if SRA would take into account the likelihood of statement execution when deciding whether to apply the transformation.  We currently verify that there are at least two reads -- perhaps we should check that there are at least two reads that are likely to occur.

This can be seen in sub-optimal codegen for ARM, where a bitfield extract (ubfx) is moved out of unlikely code into the critical path:

  foo:
        movw    r3, #:lower16:x
        ubfx    r2, r0, #4, #4
        movt    r3, #:upper16:x
        ldr     r3, [r3]
        cmp     r3, #0
        bne     .L6
        ...


---


### compiler : `gcc`
### title : `Better isfinite in some cases?`
### open_at : `2013-04-13T09:23:51Z`
### last_modified_date : `2021-09-12T19:58:08Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=56944
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.9.0`
### severity : `enhancement`
### contents :
Hello,

for isfinite, gcc typically generates this sequence:

	movsd	.LC0(%rip), %xmm1
	andpd	%xmm1, %xmm0
	movsd	.LC1(%rip), %xmm1
	ucomisd	%xmm0, %xmm1
	setae	%al

With -fno-trapping-math, I tried this shorter sequence instead, which should be valid:

	subsd	%xmm0, %xmm0
	ucomisd	%xmm0, %xmm0
	setnp	%al

Depending on the tests, it seemed to be either the same speed or 15% faster, whether the argument is normal, infinite or nan. For a denormal argument, it is 15% slower (but then both codes take 100 times as long as the normal case). The results might also be different on a more recent processor.

I don't know if we want to try and generate this code when -fno-trapping-math is present.

(related to PR 30652)


---


### compiler : `gcc`
### title : `Select best typed instruction for scalar bitwise operations`
### open_at : `2013-04-19T19:46:38Z`
### last_modified_date : `2021-12-06T23:52:18Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=57009
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `target`
### version : `4.9.0`
### severity : `enhancement`
### contents :
Hello,

I purposedly took almost the same title as PR 54716, because this is the same issue, but for scalars. Consider this code:

union A { double d; unsigned long long i; };

bool f(double a, double b, double c){
  A x, y, z;
  x.d = a * a;
  y.d = b * b;
  z.i = x.i & y.i;
  return z.d < c;
}

which compiles to:

	mulsd	%xmm0, %xmm0
	mulsd	%xmm1, %xmm1
	movq	%xmm0, %rax
	movq	%xmm1, %rdx
	andq	%rdx, %rax
	movq	%rax, %xmm0
	ucomisd	%xmm0, %xmm2
	seta	%al

when using andpd would save 3 movq. Note that for vectors, we get nicer code thanks to Jakub's patch:

	mulpd	%xmm1, %xmm1
	mulpd	%xmm0, %xmm0
	andpd	%xmm1, %xmm0
	cmpltpd	%xmm2, %xmm0

It would be nice to extend that code to scalars (including the case where one of the arguments is a constant).

I hit this while experimenting for PR 56944.


---


### compiler : `gcc`
### title : `gcc too eager splitting cvtss2sd into unpcklps + cvtps2pd`
### open_at : `2013-04-21T12:32:09Z`
### last_modified_date : `2021-08-06T01:23:50Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=57024
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.9.0`
### severity : `normal`
### contents :
Hello,

I noticed a large performance regression compiling this micro-test:

int main(){
  long i;
  float d=1;
  for(i=0;i<100000000;++i){
    d+=.3;
  }
  return (long)d;
}

with gcc -O3 -march=native (-v shows that it passes -march=core2 -mtune=core2) on this processor: Intel(R) Core(TM)2 Duo CPU     T9600  @ 2.80GHz

with gcc-4.4, it takes .31s
with trunk, it takes .45s

This seems related to:
http://gcc.gnu.org/ml/gcc-patches/2007-09/msg00714.html

an amd vs intel tuning issue. Compiling with -Os restores the good performance.


---


### compiler : `gcc`
### title : `Missed optimization of finite finite builtin`
### open_at : `2013-04-24T16:36:54Z`
### last_modified_date : `2021-09-12T19:58:08Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=57056
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `target`
### version : `4.7.1`
### severity : `normal`
### contents :
Created attachment 29930
benchmark

Hi,

Current builtin finite is slower on attached benchmark than my version.
It also needs to load 64bit constants which is not friendly to code size. 
My version is:

int finite4(double x)
{
  uint64_t lx;
  EXTRACT_WORDS64(lx,x);
  lx=lx>>52;
  return ((lx&0x7ff)!=0x7ff);
}

Most of uses of isfinite()/finite() function are in condition so I benchmark finite in condition.

Benchmark is run by

for i in `seq 0 7`; do echo finite$i;  gcc finite_bench.c -O3 -Wall -W
-fno-builtin-finite -Dfinite=finite$i; for j in `seq 1 8`; do /usr/bin/time -f
"%U" ./a.out; done; done


---


### compiler : `gcc`
### title : `Ofast does not make use of avx while O3 does`
### open_at : `2013-05-03T13:57:35Z`
### last_modified_date : `2021-08-03T18:42:42Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=57162
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `enhancement`
### contents :
in a trivial 4x4 matmul Ofast code looks worse than O3 for avx


cat matmul.cc
alignas(32) float a[4][4];
alignas(32) float b[4][4];
alignas(32) float c[4][4];

void matmul() {
  for (int i=0;i!=4;++i)
    for (int j=0;j!=4;++j) {
      float sum=0;
      for (int k=0;k!=4;++k)
            sum += a[i][k]*b[k][j];
      c[i][j]=sum;
    }
}

c++ -O3 -march=corei7-avx -mavx2 -std=c++11 -S matmul.cc
	.text
	.align 4,0x90
	.globl __Z6matmulv
__Z6matmulv:
LFB0:
	vmovss	8+_b(%rip), %xmm4
	vmovss	_b(%rip), %xmm7
	vinsertps	$0x10, 12+_b(%rip), %xmm4, %xmm0
	vmovss	24+_b(%rip), %xmm1
	vmovss	16+_b(%rip), %xmm4
	vinsertps	$0x10, 4+_b(%rip), %xmm7, %xmm5
	vmovlhps	%xmm0, %xmm5, %xmm5
	vmovss	40+_b(%rip), %xmm7
	vinsertf128	$1, %xmm5, %ymm5, %ymm5
	vinsertps	$0x10, 28+_b(%rip), %xmm1, %xmm0
	vinsertps	$0x10, 20+_b(%rip), %xmm4, %xmm3
	vmovss	32+_b(%rip), %xmm1
	vmovlhps	%xmm0, %xmm3, %xmm3
	vmovss	56+_b(%rip), %xmm4
	vinsertf128	$1, %xmm3, %ymm3, %ymm3
	vinsertps	$0x10, 44+_b(%rip), %xmm7, %xmm0
	vmovss	48+_b(%rip), %xmm6
	vinsertps	$0x10, 36+_b(%rip), %xmm1, %xmm2
	vmovlhps	%xmm0, %xmm2, %xmm2
	vinsertps	$0x10, 60+_b(%rip), %xmm4, %xmm0
	vxorps	%xmm4, %xmm4, %xmm4
	vinsertf128	$1, %xmm2, %ymm2, %ymm2
	vinsertps	$0x10, 52+_b(%rip), %xmm6, %xmm1
	vmovlhps	%xmm0, %xmm1, %xmm1
	vmovaps	_a(%rip), %ymm0
	vinsertf128	$1, %xmm1, %ymm1, %ymm1
	vpermilps	$0, %ymm0, %ymm7
	vmulps	%ymm5, %ymm7, %ymm7
	vaddps	%ymm4, %ymm7, %ymm7
	vpermilps	$85, %ymm0, %ymm6
	vmulps	%ymm3, %ymm6, %ymm6
	vaddps	%ymm6, %ymm7, %ymm7
	vpermilps	$170, %ymm0, %ymm6
	vmulps	%ymm2, %ymm6, %ymm6
	vpermilps	$255, %ymm0, %ymm0
	vmulps	%ymm1, %ymm0, %ymm0
	vaddps	%ymm6, %ymm7, %ymm6
	vaddps	%ymm0, %ymm6, %ymm0
	vmovaps	%ymm0, _c(%rip)
	vmovaps	32+_a(%rip), %ymm0
	vpermilps	$0, %ymm0, %ymm6
	vmulps	%ymm5, %ymm6, %ymm5
	vaddps	%ymm4, %ymm5, %ymm4
	vpermilps	$85, %ymm0, %ymm5
	vmulps	%ymm3, %ymm5, %ymm3
	vaddps	%ymm3, %ymm4, %ymm3
	vpermilps	$170, %ymm0, %ymm4
	vmulps	%ymm2, %ymm4, %ymm2
	vpermilps	$255, %ymm0, %ymm0
	vmulps	%ymm1, %ymm0, %ymm1
	vaddps	%ymm2, %ymm3, %ymm2
	vaddps	%ymm1, %ymm2, %ymm0
	vmovaps	%ymm0, 32+_c(%rip)
	vzeroupper

and
c++ -Ofast -march=corei7-avx -mavx2 -std=c++11 -S matmul.cc
Vincenzos-MacBook-Pro:vectorize innocent$ cat matmul.s
	.text
	.align 4,0x90
	.globl __Z6matmulv
__Z6matmulv:
LFB0:
	vmovaps	16+_a(%rip), %xmm1
	vmovaps	48+_a(%rip), %xmm0
	vmovaps	_a(%rip), %xmm4
	vmovaps	32+_a(%rip), %xmm2
	vbroadcastss	32+_b(%rip), %xmm6
	vshufps	$136, %xmm1, %xmm4, %xmm3
	vshufps	$221, %xmm1, %xmm4, %xmm4
	vbroadcastss	36+_b(%rip), %xmm5
	vshufps	$136, %xmm0, %xmm2, %xmm1
	vshufps	$221, %xmm0, %xmm2, %xmm2
	vbroadcastss	40+_b(%rip), %xmm7
	vshufps	$136, %xmm1, %xmm3, %xmm0
	vshufps	$221, %xmm1, %xmm3, %xmm3
	vshufps	$136, %xmm2, %xmm4, %xmm1
	vshufps	$221, %xmm2, %xmm4, %xmm2
	vmulps	%xmm6, %xmm3, %xmm6
	vbroadcastss	48+_b(%rip), %xmm4
	vmulps	%xmm5, %xmm3, %xmm5
	vmulps	%xmm7, %xmm3, %xmm7
	vmulps	%xmm4, %xmm2, %xmm4
	vaddps	%xmm4, %xmm6, %xmm6
	vbroadcastss	16+_b(%rip), %xmm4
	vmulps	%xmm4, %xmm1, %xmm4
	vaddps	%xmm4, %xmm6, %xmm6
	vbroadcastss	_b(%rip), %xmm4
	vmulps	%xmm4, %xmm0, %xmm4
	vaddps	%xmm4, %xmm6, %xmm6
	vbroadcastss	52+_b(%rip), %xmm4
	vmulps	%xmm4, %xmm2, %xmm4
	vaddps	%xmm4, %xmm5, %xmm5
	vbroadcastss	20+_b(%rip), %xmm4
	vmulps	%xmm4, %xmm1, %xmm4
	vaddps	%xmm4, %xmm5, %xmm5
	vbroadcastss	4+_b(%rip), %xmm4
	vmulps	%xmm4, %xmm0, %xmm4
	vaddps	%xmm4, %xmm5, %xmm4
	vbroadcastss	56+_b(%rip), %xmm5
	vmulps	%xmm5, %xmm2, %xmm5
	vaddps	%xmm5, %xmm7, %xmm7
	vbroadcastss	24+_b(%rip), %xmm5
	vmulps	%xmm5, %xmm1, %xmm5
	vaddps	%xmm5, %xmm7, %xmm7
	vbroadcastss	8+_b(%rip), %xmm5
	vmulps	%xmm5, %xmm0, %xmm5
	vaddps	%xmm5, %xmm7, %xmm5
	vbroadcastss	44+_b(%rip), %xmm7
	vmulps	%xmm7, %xmm3, %xmm3
	vbroadcastss	60+_b(%rip), %xmm7
	vmulps	%xmm7, %xmm2, %xmm2
	vaddps	%xmm2, %xmm3, %xmm2
	vbroadcastss	28+_b(%rip), %xmm3
	vmulps	%xmm3, %xmm1, %xmm1
	vunpcklps	%xmm5, %xmm6, %xmm3
	vaddps	%xmm1, %xmm2, %xmm1
	vbroadcastss	12+_b(%rip), %xmm2
	vmulps	%xmm2, %xmm0, %xmm0
	vaddps	%xmm0, %xmm1, %xmm0
	vunpckhps	%xmm5, %xmm6, %xmm1
	vunpcklps	%xmm0, %xmm4, %xmm2
	vunpckhps	%xmm0, %xmm4, %xmm0
	vunpcklps	%xmm2, %xmm3, %xmm4
	vunpckhps	%xmm2, %xmm3, %xmm2
	vmovaps	%xmm4, _c(%rip)
	vmovaps	%xmm2, 16+_c(%rip)
	vunpcklps	%xmm0, %xmm1, %xmm2
	vunpckhps	%xmm0, %xmm1, %xmm0
	vmovaps	%xmm2, 32+_c(%rip)
	vmovaps	%xmm0, 48+_c(%rip)
	ret


---


### compiler : `gcc`
### title : `fully unrolled matrix multiplication not vectorized`
### open_at : `2013-05-04T08:55:02Z`
### last_modified_date : `2021-12-28T06:23:06Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=57169
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `normal`
### contents :
a lot of legacy code still fully unroll linear algebra for small dimensions

As shown below gcc fails to vectorized a unrolled 4x4 matrix multiplication
while vectorize well the corresponding loop expression 

sample code

alignas(32) float a[4][4];
alignas(32) float b[4][4];
alignas(32) float c[4][4];

void matmul() {
   for (int i=0;i!=4;++i)
     for (int j=0;j!=4;++j) {
       float sum=0;
       for (int k=0;k!=4;++k)
             sum += a[i][k]*b[k][j];
       c[i][j]=sum;
     }
}


alignas(32) float src1[4][4];
alignas(32) float src2[4][4];
alignas(32) float dest[4][4];

void matmulU(){
  dest[0][0] = src1[0][0] * src2[0][0] + src1[0][1] * src2[1][0] + src1[0][2] * src2[2][0] + src1[0][3] * src2[3][0]; 
  dest[0][1] = src1[0][0] * src2[0][1] + src1[0][1] * src2[1][1] + src1[0][2] * src2[2][1] + src1[0][3] * src2[3][1]; 
  dest[0][2] = src1[0][0] * src2[0][2] + src1[0][1] * src2[1][2] + src1[0][2] * src2[2][2] + src1[0][3] * src2[3][2]; 
  dest[0][3] = src1[0][0] * src2[0][3] + src1[0][1] * src2[1][3] + src1[0][2] * src2[2][3] + src1[0][3] * src2[3][3]; 
  dest[1][0] = src1[1][0] * src2[0][0] + src1[1][1] * src2[1][0] + src1[1][2] * src2[2][0] + src1[1][3] * src2[3][0]; 
  dest[1][1] = src1[1][0] * src2[0][1] + src1[1][1] * src2[1][1] + src1[1][2] * src2[2][1] + src1[1][3] * src2[3][1]; 
  dest[1][2] = src1[1][0] * src2[0][2] + src1[1][1] * src2[1][2] + src1[1][2] * src2[2][2] + src1[1][3] * src2[3][2]; 
  dest[1][3] = src1[1][0] * src2[0][3] + src1[1][1] * src2[1][3] + src1[1][2] * src2[2][3] + src1[1][3] * src2[3][3]; 
  dest[2][0] = src1[2][0] * src2[0][0] + src1[2][1] * src2[1][0] + src1[2][2] * src2[2][0] + src1[2][3] * src2[3][0]; 
  dest[2][1] = src1[2][0] * src2[0][1] + src1[2][1] * src2[1][1] + src1[2][2] * src2[2][1] + src1[2][3] * src2[3][1]; 
  dest[2][2] = src1[2][0] * src2[0][2] + src1[2][1] * src2[1][2] + src1[2][2] * src2[2][2] + src1[2][3] * src2[3][2]; 
  dest[2][3] = src1[2][0] * src2[0][3] + src1[2][1] * src2[1][3] + src1[2][2] * src2[2][3] + src1[2][3] * src2[3][3]; 
  dest[3][0] = src1[3][0] * src2[0][0] + src1[3][1] * src2[1][0] + src1[3][2] * src2[2][0] + src1[3][3] * src2[3][0]; 
  dest[3][1] = src1[3][0] * src2[0][1] + src1[3][1] * src2[1][1] + src1[3][2] * src2[2][1] + src1[3][3] * src2[3][1]; 
  dest[3][2] = src1[3][0] * src2[0][2] + src1[3][1] * src2[1][2] + src1[3][2] * src2[2][2] + src1[3][3] * src2[3][2]; 
  dest[3][3] = src1[3][0] * src2[0][3] + src1[3][1] * src2[1][3] + src1[3][2] * src2[2][3] + src1[3][3] * src2[3][3]; 
};

generated asm 

c++ -v
Using built-in specs.
COLLECT_GCC=c++
COLLECT_LTO_WRAPPER=/usr/local/libexec/gcc/x86_64-apple-darwin12.3.0/4.9.0/lto-wrapper
Target: x86_64-apple-darwin12.3.0
Configured with: ./configure --disable-multilib --disable-bootstrap --enable-lto -disable-libitm --enable-languages=c,c++,fortran,lto --no-create --no-recursion
Thread model: posix
gcc version 4.9.0 20130428 (experimental) [trunk revision 198366] (GCC) 
Vincenzos-MacBook-Pro:vectorize innocent$ c++ -O3 -march=corei7-avx  -std=c++11 -S matmul.cc -mavx2 -mfma
Vincenzos-MacBook-Pro:vectorize innocent$ cat matmul.s
	.text
	.align 4,0x90
	.globl __Z6matmulv
__Z6matmulv:
LFB0:
	vmovss	8+_b(%rip), %xmm7
	vmovss	24+_b(%rip), %xmm1
	vinsertps	$0x10, 12+_b(%rip), %xmm7, %xmm0
	vmovss	_b(%rip), %xmm7
	vmovss	16+_b(%rip), %xmm2
	vinsertps	$0x10, 4+_b(%rip), %xmm7, %xmm8
	vmovss	40+_b(%rip), %xmm3
	vmovlhps	%xmm0, %xmm8, %xmm8
	vmovss	32+_b(%rip), %xmm4
	vinsertf128	$1, %xmm8, %ymm8, %ymm8
	vinsertps	$0x10, 28+_b(%rip), %xmm1, %xmm0
	vmovss	56+_b(%rip), %xmm7
	vinsertps	$0x10, 20+_b(%rip), %xmm2, %xmm6
	vmovlhps	%xmm0, %xmm6, %xmm6
	vmovss	48+_b(%rip), %xmm1
	vinsertf128	$1, %xmm6, %ymm6, %ymm6
	vinsertps	$0x10, 44+_b(%rip), %xmm3, %xmm0
	vinsertps	$0x10, 36+_b(%rip), %xmm4, %xmm5
	vmovlhps	%xmm0, %xmm5, %xmm5
	vinsertps	$0x10, 60+_b(%rip), %xmm7, %xmm0
	vinsertps	$0x10, 52+_b(%rip), %xmm1, %xmm4
	vmovlhps	%xmm0, %xmm4, %xmm4
	vxorps	%xmm7, %xmm7, %xmm7
	vmovaps	_a(%rip), %ymm0
	vinsertf128	$1, %xmm5, %ymm5, %ymm5
	vinsertf128	$1, %xmm4, %ymm4, %ymm4
	vpermilps	$255, %ymm0, %ymm1
	vpermilps	$170, %ymm0, %ymm2
	vpermilps	$85, %ymm0, %ymm3
	vpermilps	$0, %ymm0, %ymm0
	vfmadd132ps	%ymm8, %ymm7, %ymm0
	vfmadd132ps	%ymm6, %ymm0, %ymm3
	vmovaps	32+_a(%rip), %ymm0
	vfmadd132ps	%ymm5, %ymm3, %ymm2
	vfmadd132ps	%ymm4, %ymm2, %ymm1
	vmovaps	%ymm1, _c(%rip)
	vpermilps	$170, %ymm0, %ymm2
	vpermilps	$255, %ymm0, %ymm1
	vpermilps	$85, %ymm0, %ymm3
	vpermilps	$0, %ymm0, %ymm0
	vfmadd132ps	%ymm8, %ymm7, %ymm0
	vfmadd132ps	%ymm6, %ymm0, %ymm3
	vfmadd132ps	%ymm5, %ymm3, %ymm2
	vfmadd132ps	%ymm4, %ymm2, %ymm1
	vmovaps	%ymm1, 32+_c(%rip)
	vzeroupper
	ret
LFE0:
	.align 4,0x90
	.globl __Z7matmulUv
__Z7matmulUv:
LFB1:
	vmovss	4+_src1(%rip), %xmm5
	vmovss	16+_src2(%rip), %xmm15
	vmovss	_src1(%rip), %xmm4
	vmulss	%xmm15, %xmm5, %xmm1
	vmovss	8+_src1(%rip), %xmm2
	vmovss	12+_src1(%rip), %xmm0
	vmovss	_src2(%rip), %xmm14
	vmovss	32+_src2(%rip), %xmm13
	vmovss	48+_src2(%rip), %xmm12
	vfmadd231ss	%xmm14, %xmm4, %xmm1
	vmovss	20+_src2(%rip), %xmm11
	vfmadd231ss	%xmm13, %xmm2, %xmm1
	vfmadd231ss	%xmm12, %xmm0, %xmm1
	vmovss	%xmm1, _dest(%rip)
	vmovss	4+_src2(%rip), %xmm10
	vmulss	%xmm11, %xmm5, %xmm1
	vmovss	36+_src2(%rip), %xmm9
	vmovss	52+_src2(%rip), %xmm8
	vmovss	24+_src2(%rip), %xmm7
	vmovss	28+_src2(%rip), %xmm6
	vfmadd231ss	%xmm10, %xmm4, %xmm1
	vfmadd231ss	%xmm9, %xmm2, %xmm1
	vfmadd231ss	%xmm8, %xmm0, %xmm1
	vmovss	%xmm1, 4+_dest(%rip)
	vmulss	%xmm7, %xmm5, %xmm1
	vmovss	44+_src2(%rip), %xmm3
	vmulss	%xmm6, %xmm5, %xmm5
	vfmadd231ss	8+_src2(%rip), %xmm4, %xmm1
	vfmadd231ss	40+_src2(%rip), %xmm2, %xmm1
	vfmadd231ss	56+_src2(%rip), %xmm0, %xmm1
	vfmadd231ss	12+_src2(%rip), %xmm4, %xmm5
	vfmadd231ss	%xmm3, %xmm2, %xmm5
	vfmadd231ss	60+_src2(%rip), %xmm0, %xmm5
	vmovss	%xmm5, 12+_dest(%rip)
	vmovss	20+_src1(%rip), %xmm5
	vmovss	%xmm1, 8+_dest(%rip)
	vmovss	16+_src1(%rip), %xmm4
	vmulss	%xmm5, %xmm15, %xmm1
	vmovss	24+_src1(%rip), %xmm2
	vmovss	28+_src1(%rip), %xmm0
	vfmadd231ss	%xmm4, %xmm14, %xmm1
	vfmadd231ss	%xmm2, %xmm13, %xmm1
	vfmadd231ss	%xmm0, %xmm12, %xmm1
	vmovss	%xmm1, 16+_dest(%rip)
	vmulss	%xmm5, %xmm11, %xmm1
	vfmadd231ss	%xmm4, %xmm10, %xmm1
	vfmadd231ss	%xmm2, %xmm9, %xmm1
	vfmadd231ss	%xmm0, %xmm8, %xmm1
	vmovss	%xmm1, 20+_dest(%rip)
	vmulss	%xmm5, %xmm7, %xmm1
	vmulss	%xmm5, %xmm6, %xmm5
	vfmadd231ss	8+_src2(%rip), %xmm4, %xmm1
	vfmadd231ss	40+_src2(%rip), %xmm2, %xmm1
	vfmadd231ss	56+_src2(%rip), %xmm0, %xmm1
	vmovss	%xmm1, 24+_dest(%rip)
	vfmadd231ss	12+_src2(%rip), %xmm4, %xmm5
	vfmadd231ss	%xmm2, %xmm3, %xmm5
	vfmadd231ss	60+_src2(%rip), %xmm0, %xmm5
	vmovss	%xmm5, 28+_dest(%rip)
	vmovss	36+_src1(%rip), %xmm5
	vmovss	32+_src1(%rip), %xmm4
	vmulss	%xmm5, %xmm15, %xmm1
	vmovss	40+_src1(%rip), %xmm2
	vmovss	44+_src1(%rip), %xmm0
	vfmadd231ss	%xmm4, %xmm14, %xmm1
	vfmadd231ss	%xmm2, %xmm13, %xmm1
	vfmadd231ss	%xmm0, %xmm12, %xmm1
	vmovss	%xmm1, 32+_dest(%rip)
	vmulss	%xmm5, %xmm11, %xmm1
	vfmadd231ss	%xmm4, %xmm10, %xmm1
	vfmadd231ss	%xmm2, %xmm9, %xmm1
	vfmadd231ss	%xmm0, %xmm8, %xmm1
	vmovss	%xmm1, 36+_dest(%rip)
	vmulss	%xmm5, %xmm7, %xmm1
	vmulss	%xmm5, %xmm6, %xmm5
	vfmadd231ss	8+_src2(%rip), %xmm4, %xmm1
	vfmadd231ss	40+_src2(%rip), %xmm2, %xmm1
	vfmadd231ss	56+_src2(%rip), %xmm0, %xmm1
	vfmadd231ss	12+_src2(%rip), %xmm4, %xmm5
	vfmadd231ss	%xmm2, %xmm3, %xmm5
	vfmadd231ss	60+_src2(%rip), %xmm0, %xmm5
	vmovss	%xmm5, 44+_dest(%rip)
	vmovss	52+_src1(%rip), %xmm5
	vmovss	48+_src1(%rip), %xmm4
	vmovss	%xmm1, 40+_dest(%rip)
	vmulss	%xmm5, %xmm15, %xmm15
	vmovss	56+_src1(%rip), %xmm2
	vmulss	%xmm5, %xmm11, %xmm11
	vmovss	60+_src1(%rip), %xmm0
	vmulss	%xmm5, %xmm7, %xmm7
	vmulss	%xmm5, %xmm6, %xmm5
	vfmadd231ss	%xmm4, %xmm14, %xmm15
	vfmadd231ss	%xmm2, %xmm13, %xmm15
	vfmadd231ss	%xmm0, %xmm12, %xmm15
	vfmadd132ss	%xmm4, %xmm11, %xmm10
	vmovss	%xmm15, 48+_dest(%rip)
	vfmadd132ss	%xmm2, %xmm10, %xmm9
	vfmadd231ss	8+_src2(%rip), %xmm4, %xmm7
	vfmadd231ss	%xmm0, %xmm8, %xmm9
	vfmadd231ss	40+_src2(%rip), %xmm2, %xmm7
	vfmadd132ss	12+_src2(%rip), %xmm5, %xmm4
	vfmadd132ss	%xmm3, %xmm4, %xmm2
	vfmadd231ss	56+_src2(%rip), %xmm0, %xmm7
	vfmadd231ss	60+_src2(%rip), %xmm0, %xmm2
	vmovss	%xmm9, 52+_dest(%rip)
	vmovss	%xmm7, 56+_dest(%rip)
	vmovss	%xmm2, 60+_dest(%rip)
	ret


---


### compiler : `gcc`
### title : `copy elision with function arguments passed by value`
### open_at : `2013-05-05T14:03:11Z`
### last_modified_date : `2022-03-08T13:55:40Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=57176
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `c++`
### version : `4.9.0`
### severity : `enhancement`
### contents :
Hello,

it is a well know issue that copy elision is allowed but never implemented in cases like:

A f(A x){
  return x;
}

and the reason is that the caller and the callee have to communicate for it to happen. In C, the function would be:
void f_impl(A* ret_p, A* x_p);
with the caller being responsible for allocating space for ret and x and making the copy into x.

It seems that to make it work, we would need to notice that f is eligible for this optimization, mark it somehow (indicating which argument can be used as return value) and clone it:
void f_impl_nrvo(A* ret_x_p);

Callers who would see this mark would instead call the clone with one less argument.

There are clearly many parts of the front-end I don't understand enough to do this, but does it look like a correct and workable approach?


---


### compiler : `gcc`
### title : `implement load sinking in loops`
### open_at : `2013-05-06T14:50:44Z`
### last_modified_date : `2021-07-26T22:09:33Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=57186
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `enhancement`
### contents :
Created attachment 30040
Original implementation

Even at -O3, the compiler doesn't figure out that the following loop is dumb:

#define SIZE 64

int foo (int v[])
{
  int r;

  for (i = 0; i < SIZE; i++)
    r = v[i];

  return r;
}

This isn't entirely unexpected, as it probably matters only for (slightly) pathological cases.  The attached patch nevertheless implements a form of load sinking in loops so as to optimize these cases.  It's combined with invariant motion to optimize:

int foo (int v[], int a)
{
  int r, i;

  for (i = 0; i < SIZE; i++)
    r = v[i] + a;

  return r;
}

and with store sinking to optimize:

int foo (int v1[], int v2[])
{
  int r[SIZE];
  int i, j;

  for (j = 0; j < SIZE; j++)
    for (i = 0; i < SIZE; i++)
      r[j] = v1[j] + v2[i];

  return r[SIZE - 1];
}

The optimization is enabled at -O2 in the patch for measurement purposes but, 
given how rarely it triggers (e.g. exactly 10 occurrences in a GCC bootstrap, 
compiler-only, all languages except Go), it's probably best suited to -O3.

It also comes with 3 testcases.


---


### compiler : `gcc`
### title : `[7 Regression] suboptimal register allocation for SSE registers`
### open_at : `2013-05-07T09:36:06Z`
### last_modified_date : `2019-11-14T09:09:20Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=57193
### status : `RESOLVED`
### tags : `missed-optimization, ra`
### component : `rtl-optimization`
### version : `4.9.0`
### severity : `normal`
### contents :
This bug _might_ be related to PR56339, although that report talks about a regression compared to 4.7, while this bug seems to be a regression compared to 4.4.

I was converting some hand-written asm code to SSE-intrinsics, but unfortunately the version using intrinsics generates worse code. It contains two unnecessary 'movdqa' instructions.

I managed to reduce my test to this routine:

//--------------------------------------------------------------
#include <emmintrin.h>

void test1(const __m128i* in1, const __m128i* in2, __m128i* out,
           __m128i f, __m128i zero)
{
	__m128i c = _mm_avg_epu8(*in1, *in2);
	__m128i l = _mm_unpacklo_epi8(c, zero);
	__m128i h = _mm_unpackhi_epi8(c, zero);
	__m128i m = _mm_mulhi_epu16(l, f);
	__m128i n = _mm_mulhi_epu16(h, f);
	*out = _mm_packus_epi16(m, n);
}
//--------------------------------------------------------------

A (few days old) gcc snapshot generates the following code. Versions 4.5, 4.6 and 4.7 generate similar code:

   0:   66 0f 6f 17             movdqa (%rdi),%xmm2
   4:   66 0f e0 16             pavgb  (%rsi),%xmm2
   8:   66 0f 6f da             movdqa %xmm2,%xmm3
   c:   66 0f 68 d1             punpckhbw %xmm1,%xmm2
  10:   66 0f 60 d9             punpcklbw %xmm1,%xmm3
  14:   66 0f e4 d0             pmulhuw %xmm0,%xmm2
  18:   66 0f 6f cb             movdqa %xmm3,%xmm1
  1c:   66 0f e4 c8             pmulhuw %xmm0,%xmm1
  20:   66 0f 6f c1             movdqa %xmm1,%xmm0
  24:   66 0f 67 c2             packuswb %xmm2,%xmm0
  28:   66 0f 7f 02             movdqa %xmm0,(%rdx)
  2c:   c3                      retq

Gcc version 4.3 and 4.4 (and clang) generate the following optimal(?) code:
   0:   66 0f 6f 17             movdqa (%rdi),%xmm2
   4:   66 0f e0 16             pavgb  (%rsi),%xmm2
   8:   66 0f 6f da             movdqa %xmm2,%xmm3
   c:   66 0f 68 d1             punpckhbw %xmm1,%xmm2
  10:   66 0f 60 d9             punpcklbw %xmm1,%xmm3
  14:   66 0f e4 d8             pmulhuw %xmm0,%xmm3
  18:   66 0f e4 c2             pmulhuw %xmm2,%xmm0
  1c:   66 0f 67 d8             packuswb %xmm0,%xmm3
  20:   66 0f 7f 1a             movdqa %xmm3,(%rdx)
  24:   c3                      retq


---


### compiler : `gcc`
### title : `Auto-vectorization in nested loops with non-varying indexed array access results in very poor performance (worse than no auto-vectorization)`
### open_at : `2013-05-08T09:09:10Z`
### last_modified_date : `2021-07-21T03:24:16Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=57204
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.7.3`
### severity : `enhancement`
### contents :
In the good case below, auto-vectorization improves performance by a factor of 3. In the bad case, it actually decreases performance compared to no auto-vectorization. 

Good:
void foo(float * d, int n)
{
  int i, j, k;
  for (k=0; k<n; ++k) {
    for (i=0; i<n; ++i) {
      float d_ik = d[i*n+k]; 
      for (j=0; j<n; ++j) {
        float t = d_ik + d[k*n+j];
        d[i*n+j] = (d[i*n+j] < t) ? d[i*n+j] : t;
      }
    }
  }
}

Bad:
void foo(float * d, int n)
{
  int i, j, k;
  for (k=0; k<n; ++k) {
    for (i=0; i<n; ++i) {
      for (j=0; j<n; ++j) {
        float t = d[i*n+k] + d[k*n+j];
        d[i*n+j] = (d[i*n+j] < t) ? d[i*n+j] : t;
      }
    }
  }
}

$ gcc -v
Using built-in specs.
COLLECT_GCC=gcc
COLLECT_LTO_WRAPPER=/usr/lib/gcc/x86_64-linux-gnu/4.7/lto-wrapper
Target: x86_64-linux-gnu
Configured with: ../src/configure -v --with-pkgversion='Ubuntu/Linaro 4.7.3-1ubuntu1' --with-bugurl=file:///usr/share/doc/gcc-4.7/README.Bugs --enable-languages=c,c++,go,fortran,objc,obj-c++ --prefix=/usr --program-suffix=-4.7 --enable-shared --enable-linker-build-id --libexecdir=/usr/lib --without-included-gettext --enable-threads=posix --with-gxx-include-dir=/usr/include/c++/4.7 --libdir=/usr/lib --enable-nls --with-sysroot=/ --enable-clocale=gnu --enable-libstdcxx-debug --enable-libstdcxx-time=yes --enable-gnu-unique-object --enable-plugin --with-system-zlib --enable-objc-gc --with-cloog --enable-cloog-backend=ppl --disable-cloog-version-check --disable-ppl-version-check --enable-multiarch --disable-werror --with-arch-32=i686 --with-abi=m64 --with-multilib-list=m32,m64,mx32 --with-tune=generic --enable-checking=release --build=x86_64-linux-gnu --host=x86_64-linux-gnu --target=x86_64-linux-gnu
Thread model: posix
gcc version 4.7.3 (Ubuntu/Linaro 4.7.3-1ubuntu1)

$ gcc -march=native -Q --help=target
The following options are target specific:
  -m128bit-long-double        		[disabled]
  -m32                        		[disabled]
  -m3dnow                     		[disabled]
  -m3dnowa                    		[disabled]
  -m64                        		[enabled]
  -m80387                     		[enabled]
  -m8bit-idiv                 		[disabled]
  -m96bit-long-double         		[enabled]
  -mabi=                      		sysv
  -mabm                       		[disabled]
  -maccumulate-outgoing-args  		[disabled]
  -maddress-mode=             		short
  -maes                       		[disabled]
  -malign-double              		[disabled]
  -malign-functions=          		0
  -malign-jumps=              		0
  -malign-loops=              		0
  -malign-stringops           		[enabled]
  -mandroid                   		[disabled]
  -march=                     		corei7
  -masm=                      		att
  -mavx                       		[disabled]
  -mavx2                      		[disabled]
  -mavx256-split-unaligned-load 	[disabled]
  -mavx256-split-unaligned-store 	[disabled]
  -mbionic                    		[disabled]
  -mbmi                       		[disabled]
  -mbmi2                      		[disabled]
  -mbranch-cost=              		0
  -mcld                       		[disabled]
  -mcmodel=                   		32
  -mcpu=                      		
  -mcrc32                     		[disabled]
  -mcx16                      		[enabled]
  -mdispatch-scheduler        		[disabled]
  -mf16c                      		[disabled]
  -mfancy-math-387            		[enabled]
  -mfentry                    		[enabled]
  -mfma                       		[disabled]
  -mfma4                      		[disabled]
  -mforce-drap                		[disabled]
  -mfp-ret-in-387             		[enabled]
  -mfpmath=                   		387
  -mfsgsbase                  		[disabled]
  -mfused-madd                		
  -mglibc                     		[enabled]
  -mhard-float                		[enabled]
  -mieee-fp                   		[enabled]
  -mincoming-stack-boundary=  		0
  -minline-all-stringops      		[disabled]
  -minline-stringops-dynamically 	[disabled]
  -mintel-syntax              		
  -mlarge-data-threshold=     		0x10000
  -mlwp                       		[disabled]
  -mlzcnt                     		[disabled]
  -mmmx                       		[disabled]
  -mmovbe                     		[disabled]
  -mms-bitfields              		[disabled]
  -mno-align-stringops        		[disabled]
  -mno-fancy-math-387         		[disabled]
  -mno-push-args              		[disabled]
  -mno-red-zone               		[disabled]
  -mno-sse4                   		[disabled]
  -momit-leaf-frame-pointer   		[disabled]
  -mpc32                      		[disabled]
  -mpc64                      		[disabled]
  -mpc80                      		[disabled]
  -mpclmul                    		[disabled]
  -mpopcnt                    		[enabled]
  -mprefer-avx128             		[disabled]
  -mpreferred-stack-boundary= 		0
  -mpush-args                 		[enabled]
  -mrdrnd                     		[disabled]
  -mrecip                     		[disabled]
  -mrecip=                    		
  -mred-zone                  		[enabled]
  -mregparm=                  		0
  -mrtd                       		[disabled]
  -msahf                      		[enabled]
  -msoft-float                		[disabled]
  -msse                       		[enabled]
  -msse2                      		[enabled]
  -msse2avx                   		[disabled]
  -msse3                      		[enabled]
  -msse4                      		[enabled]
  -msse4.1                    		[enabled]
  -msse4.2                    		[enabled]
  -msse4a                     		[disabled]
  -msse5                      		
  -msseregparm                		[disabled]
  -mssse3                     		[enabled]
  -mstack-arg-probe           		[disabled]
  -mstackrealign              		[enabled]
  -mstringop-strategy=        		[default]
  -mtbm                       		[disabled]
  -mtls-dialect=              		gnu
  -mtls-direct-seg-refs       		[enabled]
  -mtune=                     		corei7
  -muclibc                    		[disabled]
  -mveclibabi=                		[default]
  -mvect8-ret-in-mem          		[disabled]
  -mvzeroupper                		[disabled]
  -mx32                       		[disabled]
  -mxop                       		[disabled]

  Known assembler dialects (for use with the -masm-dialect= option):
    att intel

  Known ABIs (for use with the -mabi= option):
    ms sysv

  Known code models (for use with the -mcmodel= option):
    32 kernel large medium small

  Valid arguments to -mfpmath=:
    387 387+sse 387,sse both sse sse+387 sse,387

  Known vectorization library ABIs (for use with the -mveclibabi= option):
    acml svml

  Known address mode (for use with the -maddress-mode= option):
    long short

  Valid arguments to -mstringop-strategy=:
    byte_loop libcall loop rep_4byte rep_8byte rep_byte unrolled_loop

  Known TLS dialects (for use with the -mtls-dialect= option):
    gnu gnu2


---


### compiler : `gcc`
### title : `Hoist zero-extend operations when possible`
### open_at : `2013-05-09T23:36:04Z`
### last_modified_date : `2021-08-22T09:00:56Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=57231
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.8.0`
### severity : `enhancement`
### contents :
Compiling this code at -O2:

  unsigned char *value;
  
  unsigned short foobar (int iters)
  {
    unsigned short total;
    unsigned int i;
  
    for (i = 0; i < iters; i++)
      total += value[i];

    return total;
  }

On ARM generates a zero-extend of total for every iteration of the loop:

  .L3:
        ldrb    r1, [ip, r3]    @ zero_extendqisi2
        add     r3, r3, #1
        cmp     r3, r0
        add     r2, r2, r1
        uxth    r2, r2
        bne     .L3

I believe we should be able to hoist the zero-extend (uxth) after the loop.

Note that although I manifested this for ARM, I believe it's a general case that would have to be handled by the rtl optimizers.

This shows up in a hot loop of bzip2:

            for (i = gs; i <= ge; i++) {
               UInt16 icv = szptr[i];
               cost0 += len[0][icv];
               cost1 += len[1][icv];
               cost2 += len[2][icv];
               cost3 += len[3][icv];
               cost4 += len[4][icv];
               cost5 += len[5][icv];
            }


---


### compiler : `gcc`
### title : `Vector lowering of LROTATE_EXPR pessimizes code`
### open_at : `2013-05-10T08:01:55Z`
### last_modified_date : `2021-08-29T22:46:27Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=57233
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `normal`
### contents :
Hello,

the vector lowering pass, when it sees a rotate on a vector that is not a supported operation, lowers it to scalar rotates. However, from a quick look at the RTL expanders (untested), they know how to handle a vector rotate as long as shifts and ior are supported, and that would yield better code than the scalar ops. So I think the vector lowering pass should not just check if rotate is supported, but also if shift and ior are, before splitting the operation.

typedef unsigned vec __attribute__((vector_size(4*sizeof(int))));
vec f(vec a){
  return (a<<2)|(a>>30);
}

without rotate:
	vpsrld	$30, %xmm0, %xmm1
	vpslld	$2, %xmm0, %xmm0
	vpor	%xmm0, %xmm1, %xmm0

with a patch that recognizes rotate for vectors:
	vpextrd	$2, %xmm0, %edx
	vmovd	%xmm0, %eax
	rorx	$30, %eax, %eax
	movl	%eax, -16(%rsp)
	rorx	$30, %edx, %ecx
	vpextrd	$1, %xmm0, %eax
	movl	%ecx, -12(%rsp)
	vmovd	-16(%rsp), %xmm3
	vpextrd	$3, %xmm0, %edx
	vmovd	-12(%rsp), %xmm2
	rorx	$30, %eax, %eax
	rorx	$30, %edx, %edx
	vpinsrd	$1, %eax, %xmm3, %xmm1
	vpinsrd	$1, %edx, %xmm2, %xmm0
	vpunpcklqdq	%xmm0, %xmm1, %xmm0

(I am not sure all those ext/ins are optimal, I would have expected one mov from xmm0 to memory, then the scalar rotates are done and write to memory again, and one final mov back to the FPU, but my intuition may be wrong)


---


### compiler : `gcc`
### title : `Missed optimization: weird pointer update after the loop`
### open_at : `2013-05-10T13:01:43Z`
### last_modified_date : `2021-08-30T03:03:18Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=57236
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.1`
### severity : `minor`
### contents :
In short:
In a loop, I write to and increment a pointer in each iteration. Then, after the loop, I write to the pointer once more. I noticed that after the loop, instead of using the pointer and writing to it, the generated code calculates the resulting pointer from the loop count and the value of the pointer before the loop. This is clearly unneeded work.

In detail:
The attached code was reduced from a variable-length integer I/O lib, using binary streams. Bytes go into a buffer in the stream class, and get flushed when the buffer is full. Stream::WriteU8() writes a single byte: checks whether there is place in the buffer, flushes if needed and stores the byte. Calling this fn from loops is ineffective, as the flush check is performed on each call. To work around this, there is the Txn class which allows the flush check to be amortized: checks only once in the ctor, and the stream buffer ptr is updated in the dtor with the number of bytes written.

write1() uses Stream::WriteU8() directly, the buffer pointer gets loaded/stored on each iteration. I tried to Ensure() the needed number of bytes before the loop, but that didn't eliminate the loads/stores, I guess that this is too hard to track in the optimizer, though I'd be interested to read comments about this.

write2() is the same, except Stream::Txn is used. The pointer is loaded once, written to and incremented, so far so good. But when the loop exits, comes the weird part. The generated code looks like:

   0x000000000040078d <+141>:   mov    %rsi,%rdi
   0x0000000000400790 <+144>:   mov    %r12d,%ecx
   0x0000000000400793 <+147>:   mov    %ebp,%r8d
   0x0000000000400796 <+150>:   add    $0x1,%rdi
   0x000000000040079a <+154>:   shr    %cl,%r8d
   0x000000000040079d <+157>:   and    $0x7f,%r8d
   0x00000000004007a1 <+161>:   mov    %r8b,-0x1(%rdi)
   0x00000000004007a5 <+165>:   sub    $0x7,%cl
   0x00000000004007a8 <+168>:   jne    0x400793 <_Z6write2R6Streamj+147>
loop ends here, when cl is zero, then
   0x00000000004007aa <+170>:   mov    $0xffffffb7,%ecx
   0x00000000004007af <+175>:   mov    %r12d,%eax
   0x00000000004007b2 <+178>:   imul   %ecx,%eax
   0x00000000004007b5 <+181>:   sub    $0x1,%eax
   0x00000000004007b8 <+184>:   movzbl %al,%eax
   0x00000000004007bb <+187>:   lea    0x1(%rsi,%rax,1),%rsi
jump to the last WriteU8() after the loop
   0x00000000004007c0 <+192>:   jmpq   0x40072e <_Z6write2R6Streamj+46>

The source is:
        while (UNLIKELY(b)) {
                txn.WriteU8((v >> b) & 0x7f);
                b -= 7;
        }
        txn.WriteU8(v | 0x80);

If I undertand correctly, that imul calculates the pointer increment from the loop count, which is added to rsi (the pointer value before the loop). However, the pointer is readily available in rdi.

clang 3.4 generates the expected code: after the loop, just jumps and uses rax for the final write:
   0x0000000000400723 <+179>:   mov    %rdx,%rax
   0x0000000000400726 <+182>:   mov    %bl,%cl
   0x0000000000400728 <+184>:   mov    %ebp,%esi
   0x000000000040072a <+186>:   shr    %cl,%esi
   0x000000000040072c <+188>:   and    $0x7f,%sil
   0x0000000000400730 <+192>:   mov    %sil,(%rax)
   0x0000000000400733 <+195>:   inc    %rax
   0x0000000000400736 <+198>:   add    $0xf9,%bl
   0x0000000000400739 <+201>:   jne    0x400726 <write2(Stream&, unsigned int)+182>
   0x000000000040073b <+203>:   jmpq   0x40069f <write2(Stream&, unsigned int)+47>

For the full disasm dumps, see the attached files.

I'm just guessing that this is a tree-optimization issue, please change the component if needed.
 
On a side note: are there any benefits of pre-incrementing the pointer and then writing to offset -1? The insn is 4 bytes instead of 3, does the better scheduling (?) justify the code size increment?

Versions tested:
g++-4.8.1 -v
Using built-in specs.
COLLECT_GCC=g++-4.8.1
COLLECT_LTO_WRAPPER=/home/usr-local/bin/../libexec/gcc/x86_64-unknown-linux-gnu/4.8.1/lto-wrapper
Target: x86_64-unknown-linux-gnu
Configured with: ./configure --enable-languages=c,c++ --program-suffix=-4.8.1
Thread model: posix
gcc version 4.8.1 20130427 (prerelease) (GCC) 

g++ -v
Using built-in specs.
COLLECT_GCC=g++
COLLECT_LTO_WRAPPER=/usr/lib/gcc/x86_64-linux-gnu/4.7/lto-wrapper
Target: x86_64-linux-gnu
Configured with: ../src/configure -v --with-pkgversion='Debian 4.7.2-5' --with-bugurl=file:///usr/share/doc/gcc-4.7/README.Bugs --enable-languages=c,c++,go,fortran,objc,obj-c++ --prefix=/usr --program-suffix=-4.7 --enable-shared --enable-linker-build-id --with-system-zlib --libexecdir=/usr/lib --without-included-gettext --enable-threads=posix --with-gxx-include-dir=/usr/include/c++/4.7 --libdir=/usr/lib --enable-nls --with-sysroot=/ --enable-clocale=gnu --enable-libstdcxx-debug --enable-libstdcxx-time=yes --enable-gnu-unique-object --enable-plugin --enable-objc-gc --with-arch-32=i586 --with-tune=generic --enable-checking=release --build=x86_64-linux-gnu --host=x86_64-linux-gnu --target=x86_64-linux-gnu
Thread model: posix
gcc version 4.7.2 (Debian 4.7.2-5) 

 g++-4.9.0 -v
Using built-in specs.
COLLECT_GCC=g++-4.9.0
COLLECT_LTO_WRAPPER=/home/usr-local/bin/../libexec/gcc/x86_64-unknown-linux-gnu/4.9.0/lto-wrapper
Target: x86_64-unknown-linux-gnu
Configured with: ./configure --enable-languages=c,c++ --program-suffix=-4.9.0
Thread model: posix
gcc version 4.9.0 20130510 (experimental) (GCC) 

Regards, Peter


---


### compiler : `gcc`
### title : `Missed optimization: dead register move before noreturn fn call & unnecessary store/load of reg`
### open_at : `2013-05-10T19:21:46Z`
### last_modified_date : `2021-07-20T02:23:27Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=57244
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.1`
### severity : `minor`
### contents :
These are two separate issues, however, both occured in the same function, so I think it's simpler to report them together.

The reduced test case is the reader equivalent of the writer code I posted earlier today in #57236. The workings are very similar: using a helper class to amortize the number of buffer refills.

The compiler unrolled the loop, with five iterations. The read pointer is kept in a register (rbx), not incremented, but used with increasing offsets. The potential end pointer is kept in r12, updated in each iteration to the value value corresponding to the bytes read (ebx + N), and stored back to the memory at the end. However, I noticed a third issue now when looking through the code:

0) Just before the exit, the store of the end pointer looks like this:

   0x000000000040090a <+58>:	sub    %ebx,%r12d
   0x000000000040090d <+61>:	add    %r12,%rbx
   0x0000000000400910 <+64>:	mov    %rbx,0x10(%rbp)

ebx is the initial read pointer, r12 is the new pointer after N bytes were read. r12d-ebx = N, rbx + N = new end = r12d. The sub and the add is unnecessary, a single mov %r12d,0x10(%rbp) would do the very same.

+61 and +64 are not branch targets, so I think the code could be optimized more.

1) if there are no bytes at all in the buffer after the refill, we should throw an exception:

   0x00000000004008f1 <+33>:	cmp    %rcx,%rbx
   0x00000000004008f4 <+36>:	jae    0x4009a1 <_Z5read2R6Stream+209>
...
   0x00000000004009a1 <+209>:	mov    %rbx,%r12
   0x00000000004009a4 <+212>:	callq  0x400830 <_Z9throw_eofv>

The mov at +209 is unnecessary. r12 holds the new end pointer (which is the same as the start, ebx, since no bytes were read), but it is only useful if the code ever reaches +58 (see above), where it gets stored back to memory. But that won't happen, since throw_eof() throws an exception and doesn't ever return.

The other branches that throw jump to +212, so no dead move there.

2) the last iteration of the unrolled loop misses a check at the end, this changes the register assignments and introduces an unnecessary extra store/load to/from rsp.

4th iteration:
   0x000000000040096a <+154>:	movzbl 0x3(%rbx),%edx
   0x000000000040096e <+158>:	shl    $0x7,%eax
   0x0000000000400971 <+161>:	lea    0x4(%rbx),%r12
   0x0000000000400975 <+165>:	mov    %edx,%esi
   0x0000000000400977 <+167>:	and    $0x7f,%esi
   0x000000000040097a <+170>:	or     %esi,%eax
   0x000000000040097c <+172>:	test   %dl,%dl
   0x000000000040097e <+174>:	js     0x40090a <_Z5read2R6Stream+58>
5th iteration:
   0x0000000000400985 <+181>:	movzbl 0x4(%rbx),%esi
   0x0000000000400989 <+185>:	shl    $0x7,%eax
   0x000000000040098c <+188>:	lea    0x5(%rbx),%r12
   0x0000000000400990 <+192>:	mov    %sil,(%rsp)
   0x0000000000400994 <+196>:	mov    (%rsp),%edx
   0x0000000000400997 <+199>:	and    $0x7f,%edx
   0x000000000040099a <+202>:	or     %edx,%eax
   0x000000000040099c <+204>:	jmpq   0x40090a <_Z5read2R6Stream+58>

This is a regression probably, as 4.7 generates code w/o the store/load, and the byte is at the beginning loaded into %edx, not %esi, just like in the earlier iterations. 4.8.1, 4.9.0 generates the above suboptimal code.
 
The tested gcc versions and flags are the very same as in #57236.

Regards, Peter


---


### compiler : `gcc`
### title : `Unrolling too late for inlining`
### open_at : `2013-05-11T08:38:30Z`
### last_modified_date : `2022-01-06T00:06:51Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=57249
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `enhancement`
### contents :
Hello,

this code is a variant of the code at http://stackoverflow.com/questions/16493290/why-is-inlined-function-slower-than-function-pointer

typedef void (*Fn)();

long sum = 0;

inline void accu() {
  sum+=4;
}

static const Fn map[4] = {&accu, &accu, &accu, &accu};

void f(bool opt) {
  const long N = 10000000L;
  if (opt)
  {
    for (long i = 0; i < N; i++)
    {
      accu();
      accu();
      accu();
      accu();
    }
  }
  else
  {
    for (long i = 0; i < N; i++)
    {
      for (int j = 0; j < 4; j++)
        (*map[j])();
    }
  }
}


In the first loop, g++ -O3 inlines the 4 accu() calls in the einline pass. Later passes optimize the whole loop to a single +=. In the second loop, we need to wait until the inner loop is unrolled to see the accu() calls, and there is no inlining pass after that (and then it would still need the right passes to optimize the outer loop to sum+=160000000).

I am not sure what the right solution is, since too aggressive early unrolling can be bad for other optimizations. Note that LLVM manages to optimize the whole function to a single +=.


---


### compiler : `gcc`
### title : `Spill code degrades vectorized loop for 437.leslie3d on PPC64`
### open_at : `2013-05-17T03:05:54Z`
### last_modified_date : `2019-06-04T16:29:30Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=57309
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.9.0`
### severity : `normal`
### contents :
Note: This bug does NOT occur on current trunk.

To reproduce, it's necessary to patch config/rs6000/rs6000.h so that MALLOC_ABI_ALIGNMENT is defined as:

#define MALLOC_ABI_ALIGNMENT (TARGET_64BIT ? 128 : 64)

This allows more vectorization opportunities for loops that access malloc'd arrays that can be vectorized with 128-bit vectors.

I observed that making this change introduces a degradation of SPEC CPU2006 437.leslie3d, built for 64-bit PowerPC Linux.  There are a number of degraded loops in the code, which seem to all be pretty similar.  In all cases the loops are vectorized with and without the patch, but with the patch there is no need for prolog code to align the data.  Unfortunately, with the patch, the loops also contain a great deal of spill code (ld, addi, lxvd2x, stxvd2x) which reloads not only vector registers, but also GPRs used for address computation of vector loads and stores.  Without the spill code, the main loop body would be vectorized identically with and without the patch.

One of the worst degraded loops is in function fluxk.  I have oprofile data available to identify the loop as well as some dumps showing how the loop is transformed in various phases, available by request.


---


### compiler : `gcc`
### title : `Simplify (double)i != 0`
### open_at : `2013-05-22T14:36:14Z`
### last_modified_date : `2019-10-19T03:03:51Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=57371
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `enhancement`
### contents :
int f(int i){
  return (double)i != 0;
}

compiled with -Ofast (I don't think -ffast-math matters) keeps the conversion to double. I think returning i != 0 is always valid. I didn't think long about the exact set of circumstances where it is ok.


---


### compiler : `gcc`
### title : `Redundant move instruction is produced after function inlining`
### open_at : `2013-05-27T11:45:24Z`
### last_modified_date : `2021-07-25T00:33:22Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=57430
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `normal`
### contents :
This is based on performance analysis of eembc2.0 suite on Atom processor in comparison with clang compiler.

I prepared a simple reproducer that exhibits the issue.

Hottest loop (from function "remove") consists of 7 instructions if inlining was applied:
.L48:
	movl	%edx, %ebp   <<--  it is redundant!!
	movl	%ecx, %edx
.L39:
	cmpl	%edx, %eax
	je	.L24
	movl	16(%edx), %ecx
	testl	%ecx, %ecx
	jne	.L48

but without inlining it consists of 6 instructions:

.L5:
	cmpl	%eax, %ecx
	je	.L4
	movl	%eax, %edx
.L7:
	movl	16(%edx), %eax
	testl	%eax, %eax
	jne	.L5

In result we can see performance drop on 4% (Atom 32-bit mode).

The reproducer will be attached.


---


### compiler : `gcc`
### title : `memcpy in aggregate return not eliminated`
### open_at : `2013-05-31T17:54:54Z`
### last_modified_date : `2021-09-04T01:23:14Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=57485
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.8.0`
### severity : `enhancement`
### contents :
Returning a big aggregate sometimes yields an avoidable temporary and memcpy.
In this example, gcc manages to pass a pointer to the destination variable as the hidden struct return pointer only when that variable is being initialised, not when assigned separately.

Observed in 4.8.0 for x86-64 and i686.

struct S { int a[100]; };
struct S f(void);
void g(struct S *p);
void h(void) {
#if 0
        struct S s = f();  // no local temporary
#else
        struct S s;
        s = f();           // local temporary and memcpy
#endif
        g(&s);
}


---


### compiler : `gcc`
### title : `[4.8 Regression] Missing SCEV final value replacement`
### open_at : `2013-06-03T12:50:02Z`
### last_modified_date : `2021-12-17T07:58:46Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=57511
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.0`
### severity : `normal`
### contents :
The following simple loop is no longer optimized out with 4.8 and 4.9:


int main(int argc, char* argv[])
{
    int i, a = 0;
    for (i=0; i < 10000; i++)
            a += i + 0xff00ff;
    return a;
}


$ gcc-4.7.2 -O2 -S main.c -o-
main:
.LFB0:
	.cfi_startproc
	movl	$-334379544, %eax
	ret


$ gcc-4.8.0 -O2 -S main.c -o-
main:
.LFB0:
	.cfi_startproc
	movl	$16711935, %edx
	xorl	%eax, %eax
	.p2align 4,,10
	.p2align 3
.L3:
	addl	%edx, %eax
	addl	$1, %edx
	cmpl	$16721935, %edx
	jne	.L3
	rep ret


---


### compiler : `gcc`
### title : `Redundant masking of zero-extended values`
### open_at : `2013-06-04T18:36:36Z`
### last_modified_date : `2021-08-01T07:35:48Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=57529
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `target`
### version : `4.9.0`
### severity : `normal`
### contents :
Using version "gcc (GCC) 4.9.0 20130519 (experimental)" with target "x86_64-unknown-linux-gnu" and the flags "-Ofast -std=gnu99 -march=bdver1", the following code:

#include <stdint.h>

void foo(const uint16_t* restrict indexes, const uint64_t* restrict bits, unsigned int* restrict sum, int count) {
  for (int i = 0; i < count; ++i) {
    unsigned int val = indexes[i];
    if (bits[val / 64] & (1UL << (val % 64))) {sum[val] += 1;}
  }
}

produces two shifts to implement the "val / 64" operation instead of one, seemingly because the compiler is trying to mask val to 16 bits even though it was loaded with movzwl and thus was already masked and zero-extended.  Here is the assembly for the function body:

        testl   %ecx, %ecx      # count
        movl    %ecx, %r9d      # count, count
        jle     .L8     #,
        xorl    %eax, %eax      # ivtmp.5
        .p2align 4,,10
        .p2align 3
.L4:
        movzwl  (%rdi,%rax,2), %ecx     # MEM[base: indexes_8(D), index: ivtmp.5_52, step: 2, offset: 0B], D.2242
        movq    %rcx, %r8       # D.2242, D.2244
# **************** Redundant masking operation:
        salq    $48, %r8        #, D.2244
        shrq    $54, %r8        #, D.2244
# ****************
        movq    (%rsi,%r8,8), %r8       # *_16, D.2244
# ++++++++++++++++
        shrq    %cl, %r8        # D.2242, D.2244
        andl    $1, %r8d        #, D.2244
# ++++++++++++++++
        je      .L3     #,
# xxxxxxxxxxxxxxxx
        movzwl  %cx, %r8d       # D.2242, D.2244
# xxxxxxxxxxxxxxxx
        incl    (%rdx,%r8,4)    # *_25
.L3:
        incq    %rax    # ivtmp.5
        cmpl    %eax, %r9d      # ivtmp.5, count
        jg      .L4     #,
.L8:
        rep; ret

The seemingly-unnecessary operation is marked with stars; a single shrq by 6 should do the unsigned division operation correctly, while two instructions are used to both mask the value to 16 bits and shift it.  The zero-extension inside x's is also unnecessary (%rcx could have been used directly in the index expression).  On a somewhat unrelated issue, the code marked in +'s seems to be sub-optimal as well, and could probably be replaced by a bt instruction (GCC 4.4.7 uses "btq" there using -O3 and the same -march flag).


---


### compiler : `gcc`
### title : `[11/12/13/14 Regression]: Performance regression versus 4.7.3, 4.8.1 is ~15% slower`
### open_at : `2013-06-05T17:38:49Z`
### last_modified_date : `2023-07-07T10:29:57Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=57534
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.1`
### severity : `normal`
### contents :
Created attachment 30261
Reduced source code - timing functions

With x86 GCC 4.8.1, slower code is produced (than with 4.7.3) for a particular benchmark I ran, about 15% slower.

Whatever is wrong must be happening here:

 80486e5:       d9 ee                   fldz   
 80486e7:       d9 c0                   fld    %st(0)
 80486e9:       8d b4 26 00 00 00 00    lea    0x0(%esi,%eiz,1),%esi
 80486f0:       8d 04 f5 00 00 00 00    lea    0x0(,%esi,8),%eax
 80486f7:       dd 04 f3                fldl   (%ebx,%esi,8)
 80486fa:       dc 44 03 08             faddl  0x8(%ebx,%eax,1)
 80486fe:       dc 44 03 10             faddl  0x10(%ebx,%eax,1)
 8048702:       dc 44 03 18             faddl  0x18(%ebx,%eax,1)
 8048706:       de c2                   faddp  %st,%st(2)
 8048708:       dd 44 03 20             fldl   0x20(%ebx,%eax,1)
 804870c:       dc 44 03 28             faddl  0x28(%ebx,%eax,1)
 8048710:       dc 44 03 30             faddl  0x30(%ebx,%eax,1)
 8048714:       dc 44 03 38             faddl  0x38(%ebx,%eax,1)
 8048718:       8d 46 08                lea    0x8(%esi),%eax
 804871b:       39 c7                   cmp    %eax,%edi
 804871d:       de c1                   faddp  %st,%st(1)
 804871f:       7f 0e                   jg     804872f 
 8048721:       a1 34 91 04 08          mov    0x8049134,%eax
 8048726:       85 c0                   test   %eax,%eax
 8048728:       74 0e                   je     8048738 
 804872a:       83 c5 01                add    $0x1,%ebp
 804872d:       31 c0                   xor    %eax,%eax
 804872f:       89 c6                   mov    %eax,%esi
 8048731:       eb bd                   jmp    80486f0 
 8048733:       90                      nop
 8048734:       8d 74 26 00             lea    0x0(%esi,%eiz,1),%esi
 8048738:       dd 5c 24 10             fstpl  0x10(%esp)
 804873c:       83 c6 10                add    $0x10,%esi
 804873f:       dd 5c 24 08             fstpl  0x8(%esp)

This is the commandline: gcc -O2 reduceme.c timer.o -o cachebench

This is from a benchmark (llcbench, GPL software) and uses timers which may be a problem, if I preprocess them, they may not work.  I'll attach the main code (reduced) for now, and I'll work on getting the timing code included very soon.  I'll also test with 4.8.0 to see whether that version is also affected.

Attached is the reduced code minus the timing functions.  Uncommenting the commented line in the source code removes the bug.

Thanks.
Neil.


---


### compiler : `gcc`
### title : `Missed optimisation: compare + or`
### open_at : `2013-06-08T15:41:54Z`
### last_modified_date : `2021-07-20T02:34:11Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=57567
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `enhancement`
### contents :
Using 4.9.0 20130608 (experimental) [trunk revision 199851], target arm-unknown-eabi.

The following case produces suboptimal code:

unsigned
test (unsigned t)
{
  if (t != (unsigned)-1)
    t |= 3;
  return t;
}

Result:

	cmn	r0, #1
	orrne	r0, r0, #3

A simple:

	orr	r0, r0, #3

would be enough.


---


### compiler : `gcc`
### title : `Vector lowering could use larger modes`
### open_at : `2013-06-13T07:12:25Z`
### last_modified_date : `2021-08-19T21:58:55Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=57601
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.9.0`
### severity : `normal`
### contents :
typedef int vec __attribute__((vector_size(2*sizeof(int))));
vec f(vec a, vec b){
  return a-b;
}

	vmovq	%xmm0, %rcx
	vmovq	%xmm1, %rdx
	movl	%ecx, %eax
	shrq	$32, %rcx
	subl	%edx, %eax
	shrq	$32, %rdx
	subl	%edx, %ecx
	vmovd	%eax, %xmm2
	vpinsrd	$1, %ecx, %xmm2, %xmm0

(with -Ofast -mavx2) whereas if I change the size to 4, I get:

	vpsubd	%xmm1, %xmm0, %xmm0

which seems valid to me even for size 2. It is not clear to me how to model that at tree level, maybe it would be easier to just implement V2SI operations in the backend?


---


### compiler : `gcc`
### title : `Missed vectorization for a "fixed point multiplication" reduction`
### open_at : `2013-06-17T08:58:05Z`
### last_modified_date : `2021-08-16T06:07:01Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=57634
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `enhancement`
### contents :
I the following code the loop in "red" does not vectorize "because"of
note: reduction: not commutative/associative: s_12 = (unsigned int) _11;
if I use "unsigned long long" everywhere as in redl the reason becomes
reduction: not commutative/associative: s_10 = temp_9 >> 23;

the multiplication in itself vectorize…  (for unsigned!)

compiled as
c++ -std=c++11 -march=corei7-avx -mavx2 -Ofast -S FixedF.cc -ftree-vectorizer-verbose=2 -Wall
with gcc version 4.9.0 20130607 (experimental) [trunk revision 199812] (GCC) 


inline
unsigned int mult(unsigned int a, unsigned int b) {
  typedef unsigned long long ull; // (to support >>)
  // a and b are of the form 1.m with m of Q bits  as int is therefore max 2^(Q+2)-1. a*b is therefore < 2^(2*(Q+2)) 
  constexpr int Q = 23;
  constexpr unsigned long long K  = (1 << (Q-1));
  ull  temp = (ull)(a) * (ull)(b); // result type is operand's type
  // Rounding; mid values are rounded up
  temp += K;
  // Correct by dividing by base   
  return (temp >> Q);  
}

inline
unsigned long long multL(unsigned long long a, unsigned long long b) {
  typedef unsigned long long ull; // (to support >>)
  // a and b are of the form 1.m with m of Q bits. As int is therefore max 2^(Q+2)-1. a*b is therefore < 2^(2*(Q+2)) 
  constexpr int Q = 23;
  constexpr unsigned long long K  = (1 << (Q-1));
  ull  temp = (ull)(a) * (ull)(b); 
  // Rounding; mid values are rounded up
  temp += K;
  // Correct by dividing by base   
  return (temp >> Q);  
}



unsigned int   a[1024];
unsigned int   b[1024];
unsigned int   c[1024];

unsigned long long   al[1024];
unsigned long long   bl[1024];
unsigned long long   cl[1024];


void foo() {
 for (int i=0;i!=1204;++i)
   c[i] = mult(a[i],b[i]);
}


unsigned int red() {
  unsigned int s=1;
  for (int i=0;i!=1204;++i)
    s = mult(s,b[i]);
  return s;
}

unsigned long long redL() {
  unsigned long long s=1;
  for (int i=0;i!=1204;++i)
    s = multL(s,b[i]);
  return s;
}


unsigned int prod() {
  unsigned int s=1;
  for (int i=0;i!=1204;++i)
    s = s*b[i];
  return s;
}


---


### compiler : `gcc`
### title : `Suboptimal code after TRUTH_AND_EXPR is changed into BIT_AND_EXPR`
### open_at : `2013-06-19T11:49:15Z`
### last_modified_date : `2023-08-05T17:33:04Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=57650
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `enhancement`
### contents :
On:

int baz (int);

int
foo (char *x, int y, int z)
{
  if (y > z && x)
    return baz (1);
  if (x)
    baz (2);
  return 0;
}

int
bar (char *x, int y, int z)
{
  if (x && y > z)
    return baz (1);
  if (x)
    baz (2);
  return 0;
}

one of the functions (depending on reassoc decission to keep or swap the BIT_AND_EXPR arguments) ends up with really bad generated code, will do
testq %rdi, %rdi
setne %al
...
compare y with z, jump based on that, then test %al (separately in both branches).  Would be much better if tree optimizers could figure out that if one of the BIT_AND_EXPR operands is also used as condition for a conditional jump nearby, that it perhaps could jump thread this (essentially generate the same code as
if (x)
  {
    if (y > z)
      return bar (1);
    bar (2);
  }
would).


---


### compiler : `gcc`
### title : `Regression in vectorizing memcpy pattern.`
### open_at : `2013-06-21T10:36:37Z`
### last_modified_date : `2021-07-19T19:14:02Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=57668
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `normal`
### contents :
Hi,
When I ran atached benchmark that test how gcc can optimize byte by byte memcpy(attached memcpy_byte.c) I got a regression on nehalem and ivy_bridge architectures.
I ran it by commands ./run machine 2> machine_result

For ivy bridge results between 4.7 and 4.9 are:

memcpyO3-4.7.s
0.66
0.65
0.64
0.64
0.64
memcpyO3-4.9.s
0.74
0.74
0.73
0.74
0.74

Also when I look at assemblies and 4.9 version is excessively large compared to 4.7 one.


---


### compiler : `gcc`
### title : `bextr sometimes used instead of shr`
### open_at : `2013-06-23T19:26:40Z`
### last_modified_date : `2021-12-15T11:54:08Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=57690
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `unknown`
### severity : `normal`
### contents :
unsigned int bar (void);
unsigned long foo (unsigned int x) { return bar () >> 2; }

With -O2 -mtbm we get:
   0:	48 83 ec 08          	sub    $0x8,%rsp
   4:	e8 00 00 00 00       	callq  9 <foo+0x9>
			5: R_X86_64_PC32	bar-0x4
   9:	48 83 c4 08          	add    $0x8,%rsp
   d:	8f ea f8 10 c0 02 1e 	bextr  $0x1e02,%rax,%rax
  14:	00 00 
  16:	c3                   	retq   
while without it:
   0:	48 83 ec 08          	sub    $0x8,%rsp
   4:	e8 00 00 00 00       	callq  9 <foo+0x9>
			5: R_X86_64_PC32	bar-0x4
   9:	48 83 c4 08          	add    $0x8,%rsp
   d:	c1 e8 02             	shr    $0x2,%eax
  10:	c3                   	retq   
which is much shorter.  On the other side, bextr with immediate gives more freedom to the register allocator, because it is a non-destructive source instruction.  So, perhaps we want a peephole2 which will transform some forms of the immediate TARGET_TBM tbm_bextr* (those where upper bits of a SImode or DImode value are extracted and where destination is the same as source) into shrl.
For -Os maybe it would be even shorter to emit movl + shrl.


---


### compiler : `gcc`
### title : `Reassoc missed optimizations`
### open_at : `2013-06-24T18:18:30Z`
### last_modified_date : `2021-07-20T06:55:07Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=57702
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `enhancement`
### contents :
On:

int f1 (int x, int y) { x += y; return x + 3 * y; }
unsigned int f2 (unsigned int x, unsigned int y) { x += y; return x + 3 * y; }
int f3 (int x, int y) { x += 7 * y; return x + 12 * y; }
unsigned int f4 (unsigned int x, unsigned int y) { x += 7 * y; return x + 12 * y; }

reassoc optimizes only the f4 function into x += 19 * y; at the tree level, and at the RTL level combiner happens to optimize it except for f3, which has more insns than f4.  I don't see why not optimizing this even for signed types would be problematic, as long as the multiplication is performed in the same signed type and all terms have the same sign (with different sizes the optimization could remove undefined overflow, but I don't see how it could introduce it).

When things are vectorized the RTL optimizations will hardly help though.


---


### compiler : `gcc`
### title : `Non-constant step induction vars not vectorized`
### open_at : `2013-06-25T08:08:42Z`
### last_modified_date : `2021-02-28T15:52:31Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=57705
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `normal`
### contents :
int a[1024] __attribute__ ((aligned (32)));
void
bar (int k, int m)
{
  int i, k2 = k;
  for (i = 0; i < 1024; i++)
    {
      a[i] = k2;
      k2 += m + 1;
    }
}

isn't vectorized, although it seems fairly easy to handle these.


---


### compiler : `gcc`
### title : `Missed optimization: recursion around empty function`
### open_at : `2013-06-26T10:43:58Z`
### last_modified_date : `2021-08-16T23:47:32Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=57723
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `minor`
### contents :
Background: freeing nodes of a tree allocated with custom allocators. One of the allocators can't free individual pointers, so free() is NOP in that case (the whole pool will be freed at once when the allocator is destroyed). With this allocator, the whole recursive traversal can be eliminated in theory.

Examining the disasm of the generated code revealed that gcc unfolds the recursion many levels, just to do the unneeded node traversal; the actual call to the empty free() fn is eliminated.

In the test case, loop() does a simple linear traversal of the linked nodes. The pointers are not volatile, and are only read, so there should not be any side effects. Why can't the compiler optimize away the whole loop?

Clang does a somewhat better job, the recursion is optimized away, and one function is completely reduced to NOP (free_all2()), but the others still have the node traversal loop.

Tried with gcc 4.6, 4.7.3, 4.9.0 with the same results.

g++-4.9.0 -v:
Using built-in specs.
COLLECT_GCC=g++-4.9.0
COLLECT_LTO_WRAPPER=/home/usr-local/bin/../libexec/gcc/x86_64-unknown-linux-gnu/4.9.0/lto-wrapper
Target: x86_64-unknown-linux-gnu
Configured with: ./configure --enable-languages=c,c++ --program-suffix=-4.9.0
Thread model: posix
gcc version 4.9.0 20130626 (experimental) (GCC) 
commit 944f42fc29289812416f34d7b0c497ee79065396

command line:
g++-4.9.0 -std=c++11 -O3 -Wall 20130626-free_node.cpp

Regards, Peter


---


### compiler : `gcc`
### title : `Improve fold_binary_op_with_conditional_arg`
### open_at : `2013-06-28T18:02:15Z`
### last_modified_date : `2023-09-16T03:32:05Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=57755
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `enhancement`
### contents :
Hello,

fold_binary_op_with_conditional_arg performs the following:

   Transform `a + (b ? x : y)' into `b ? (a + x) : (a + y)'.
   Transform, `a + (x < y)' into `(x < y) ? (a + 1) : (a + 0)'.

It gives up in this first case (arg is 'a' above):

  if (!TREE_CONSTANT (arg)
      && (TREE_SIDE_EFFECTS (arg)
          || TREE_CODE (arg) == COND_EXPR || TREE_CODE (arg) == VEC_COND_EXPR
          || TREE_CONSTANT (true_value) || TREE_CONSTANT (false_value)))
    return NULL_TREE;

and after folding both branches:

  if (!TREE_CONSTANT (arg) && !TREE_CONSTANT (lhs) && !TREE_CONSTANT (rhs))
    return NULL_TREE;

This seems suboptimal. On the one hand, for ((a<b)?a:c)*3/2+1, it distributes the operations to a < b ? (a * 3) / 2 + 1 : (c * 3) / 2 + 1 (we can add as many operations with constants as we want) and this isn't completely undone later (partially with -Os, not at all with -O3). On the other hand, for ((a<2)?-1u:0)&b, it gives up instead of producing (a<2)?b:0.

We must be careful with recursions (PR55219) and with folders performing the reverse transformations, but I think we should be able to optimize:
(((a<2)?-1:0)&((b<1)?-1:0))!=0

(obviously, the title doesn't prevent from moving this functionality to gimple)


---


### compiler : `gcc`
### title : `large constants evaluated inline`
### open_at : `2013-07-06T11:58:47Z`
### last_modified_date : `2020-04-01T23:17:09Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=57836
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.9.0`
### severity : `enhancement`
### contents :
On powerpc64 with -mcmodel=small -O1, this

int x;

void f1 (long long hx)
{
  if (hx < 0x3ff0000000000000LL)
    x++;
}

results in

.L.f1:
	lis 9,0x3fef
	ori 9,9,65535
	sldi 9,9,32
	oris 9,9,0xffff
	ori 9,9,65535
	cmpd 7,3,9
	bgtlr 7
	ld 9,.LC1@toc(2)
	lwz 10,0(9)
	addi 10,10,1
	stw 10,0(9)
	blr

The -mcmodel isn't significant, just there to make comparison with older compilers easy.  Prior to gcc-4.5 we generated

.L.f1:
	ld 0,.LC0@toc(2)
	cmpd 7,3,0
	bgtlr 7
	ld 9,.LC1@toc(2)
	lwz 11,0(9)
	addi 0,11,1
	stw 0,0(9)
	blr

Both pre- and post-4.5 compilers initially expand rtl using the constant load from toc, but 4.5 and later substitute the constant in the first cse pass.
The problem stems from rtx cost for the load from toc being the same as the inline constant form.

The costs are the same both pre- and post-4.5.  The reason pre-4.5 does not substitute the constant is related to this comment is cse.c:
	  /* Find cheapest and skip it for the next time.   For items
	     of equal cost, use this order:
	     src_folded, src, src_eqv, src_related and hash table entry.  */
Pre-4.5 src_folded is NULL, src is a mem, src_eqv the constant.
Post-4.5 src_folded is the constant, src is a mem, src_eqv the constant again.

Pre-4.5, rs6000.c lacked delegitimize_address. src_folded is set by fold_rtx, which calls equiv_constant, which calls avoid_constant_pool_reference, which calls targetm.delegitimize_address.  When this is missing, we don't get to see the constant..


---


### compiler : `gcc`
### title : `AVX2: ymm used for div, not for sqrt`
### open_at : `2013-07-09T07:55:24Z`
### last_modified_date : `2021-09-11T06:37:51Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=57858
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `normal`
### contents :
in the following example div uses ymm registries while sqr only xmm ones
gcc version 4.9.0 20130630 (experimental) [trunk revision 200570] (GCC) 

cat avx2sqrt.cc
#include<math.h>
double div() {
   double s=0;
   for (int i=0; i!=1024; ++i) s+=1./(i+1);
   return s;
}


double sqr() {
   double s=0;
   for (int i=0; i!=1024; ++i) s+=sqrt(i+1);
   return s;
}

c++ -std=c++11 -Ofast -S avx2sqrt.cc -march=corei7-avx -mavx2 -ftree-vectorizer-verbose=1 -Wall ; cat avx2sqrt.s

_Z3divv:
.LFB3:
	.cfi_startproc
	vmovdqa	.LC1(%rip), %ymm6
	xorl	%eax, %eax
	vxorpd	%xmm1, %xmm1, %xmm1
	vmovdqa	.LC0(%rip), %ymm0
	vmovdqa	.LC2(%rip), %ymm5
	vmovapd	.LC3(%rip), %ymm2
	jmp	.L2
	.p2align 4,,10
	.p2align 3
.L3:
	vmovdqa	%ymm4, %ymm0
.L2:
	vpaddd	%ymm6, %ymm0, %ymm4
	vpaddd	%ymm5, %ymm0, %ymm0
	addl	$1, %eax
	vextracti128	$0x1, %ymm0, %xmm3
	vcvtdq2pd	%xmm0, %ymm0
	vcvtdq2pd	%xmm3, %ymm3
	vdivpd	%ymm0, %ymm2, %ymm0
	vdivpd	%ymm3, %ymm2, %ymm3
	vaddpd	%ymm0, %ymm3, %ymm0
	cmpl	$128, %eax
	vaddpd	%ymm0, %ymm1, %ymm1
	jne	.L3
	vhaddpd	%ymm1, %ymm1, %ymm1
	vperm2f128	$1, %ymm1, %ymm1, %ymm0
	vaddpd	%ymm0, %ymm1, %ymm0
	vzeroupper
	ret
	.cfi_endproc
.LFE3:
	.size	_Z3divv, .-_Z3divv
	.p2align 4,,15
	.globl	_Z3sqrv
	.type	_Z3sqrv, @function
_Z3sqrv:
.LFB4:
	.cfi_startproc
	movl	$1, %eax
	vmovsd	.LC4(%rip), %xmm1
	vxorpd	%xmm0, %xmm0, %xmm0
	jmp	.L6
	.p2align 4,,10
	.p2align 3
.L7:
	vcvtsi2sd	%eax, %xmm1, %xmm1
	vsqrtsd	%xmm1, %xmm1, %xmm1
.L6:
	addl	$1, %eax
	vaddsd	%xmm1, %xmm0, %xmm0
	cmpl	$1025, %eax
	jne	.L7
	rep; ret
	.cfi_endproc
.LFE4:
	.size	_Z3sqrv, .-_Z3sqrv


---


### compiler : `gcc`
### title : `gcc 4.8.1 regression: loops become slower`
### open_at : `2013-07-12T14:14:14Z`
### last_modified_date : `2021-06-08T21:37:34Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=57890
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.8.1`
### severity : `normal`
### contents :
$cat what_test.cpp
char c[100];

void f(void)
{
        for(int i=0; i < 100; ++i)
                c[i] = '0';
}

I run this test with:
cat test.cpp
#include <cstddef>

extern void f();

int main()
{
	for (size_t i = 0; i < 100000000; ++i)
		f();
}

compile with "-march=native -O3" on (i7 64bit mode).

Here is result:
for test_loop47 we get average 0.348000
for test_loop481 we get average 0.400000

If compare generated code then on 4.7 "f" function is transformed to:
push   %rbp
vmovdqa 0x107(%rip),%ymm0
movb   $0x30,0x200aa0(%rip)
movb   $0x30,0x200a9a(%rip)
mov    %rsp,%rbp
vmovdqa %ymm0,0x200a2e(%rip)
...

on gcc 4.8.1:

movabs $0x3030303030303030,%rax
movl   $0x30303030,0x200a9c(%rip)
mov    %rax,0x200a35(%rip)
mov    %rax,0x200a36(%rip)
...


PS

I just checked may be 
http://gcc.gnu.org/bugzilla/show_bug.cgi?id=55953
fixed in gcc 4.8.1,
and yes it indeed "fixed", instead of optimal for loops and
not optimal for builtin_memset it now produces not the same not optimal code for both cases.


---


### compiler : `gcc`
### title : `[11/12/13/14 Regression] Uniquization of constants reduces alignment of initializers`
### open_at : `2013-07-22T21:36:09Z`
### last_modified_date : `2023-07-07T10:29:59Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=57955
### status : `WAITING`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.6.0`
### severity : `normal`
### contents :
A patch to improve uniquization of constants at the tree level broke alignment of constants and vectorized copies.

gcc.target/powerpc/ppc-vector-memcpy.c


---


### compiler : `gcc`
### title : `Missed SLP opportunity`
### open_at : `2013-07-23T12:22:31Z`
### last_modified_date : `2021-12-26T23:12:54Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=57962
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.7.3`
### severity : `enhancement`
### contents :
Created attachment 30541
Sample code.

GCC 4.7.3 and 4.8.1 both miss an optimization when compiling the attached test case using:

  gcc -Ofast -march=corei7-avx test.c -S

By loading the components of ul and fl into the bottom half of an xmm register and ur and fr into the corresponding top half it is possible to compute disf_inv_impl(ul, fl) and disf_inv_impl(ur, fr) in a single hit.  Horizontal instructions can then be used to add the various fl and fr components together.


---


### compiler : `gcc`
### title : `Constant folding of infinity`
### open_at : `2013-07-26T15:13:47Z`
### last_modified_date : `2022-10-27T15:27:08Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=57994
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `normal`
### contents :
double f(){
  return __builtin_exp(-__builtin_huge_val());
}

As noticed in PR57974, we fail to fold this to a constant. Indeed, in do_mpfr_arg1, the relevant code is protected by if (real_isfinite (ra) ...

mpfr handles infinite values, so it should be doable, at least with -ffast-math (there might be some errno issues with default options).


---


### compiler : `gcc`
### title : `missed optimization printf constant string`
### open_at : `2013-07-27T19:44:30Z`
### last_modified_date : `2021-12-28T05:40:02Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=58005
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.1`
### severity : `enhancement`
### contents :
Simple code:

#include <cstdio>

int main()
{
	printf("%s: test1\n", __PRETTY_FUNCTION__);//1
	printf("test2\n");//2
	return 0;
}

compiled to:

callq  4005a0 <__printf_chk@plt> (1)
and to
callq  400590 <puts@plt> for (2)

I think that, because of __PRETTY_FUNCTION__ is known during compile time, it is also possible converting (1) to "puts" call.

This optimization can help speedup loging functionality.


---


### compiler : `gcc`
### title : `counterproductive bb-reorder`
### open_at : `2013-07-30T21:00:01Z`
### last_modified_date : `2021-12-19T00:27:58Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=58033
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.9.0`
### severity : `normal`
### contents :
On SH, compiling the following code with -O2

#include <bitset>

std::bitset<32> make_bits (void)
{
  std::bitset<32> r;
  for (auto&& i : { 4, 5, 6, 10 })
    if (i < r.size ())
      r.set (i);

  return r;
}

results in the following code:

        mov.l   .L8,r1
        mov     #0,r0
        mov     #31,r7
        mov     #1,r6
        mov     #4,r2
.L2:
        mov.l   @r1,r3
        cmp/hi  r7,r3
        bf/s    .L7
        mov     r6,r5
.L3:
        dt      r2
        bf/s    .L2     // branch if value not > 31, i.e. in each iteration
        add     #4,r1
        rts
        nop
        .align 1
.L7:
        shld    r3,r5
        bra     .L3
        or      r5,r0
.L9:
        .align 2
.L8:
        .long   _._45+0

_._45:
        .long   4
        .long   5
        .long   6
        .long   10

Disabling the bb-reorder pass or using -Os results in more compact and faster code:

        mov.l   .L7,r1
        mov     #0,r0
        mov     #31,r7
        mov     #1,r6
        mov     #4,r2
.L2:
        mov.l   @r1,r3
        cmp/hi  r7,r3
        bt/s    .L3    // branch if value > 31, i.e. never.
        mov     r6,r5
        shld    r3,r5
        or      r5,r0
.L3:
        dt      r2
        bf/s    .L2
        add     #4,r1
        rts	
        nop

Of course the bb-reorder pass doesn't know that the values in this case are always in range.  Still, maybe it could be improved by not splitting out a BB if it consists only of a few insns?  I've tried increasing the branch cost but it won't do anything.

Teresa, Steven,


---


### compiler : `gcc`
### title : `No return value optimization when calling static function through unnamed temporary`
### open_at : `2013-08-02T03:08:50Z`
### last_modified_date : `2023-06-07T01:33:21Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=58050
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `c++`
### version : `4.8.1`
### severity : `enhancement`
### contents :
Return value optimization is not applied when calling a static member function via an unnamed temporary (value or pointer, it doesn't matter). Calling the function directly, or through a named value/pointer, works as expected:

// <<<--- bug.cpp --->>>
extern "C" int puts(char const*);
struct B {
    ~B() { puts("\t~B"); }
};
struct A {
    static B make() { return B(); }
} a;
A *ap() { return &a; }
int main () {
    puts("b1");
    {B b = A::make();}
    puts("b2");
    {B B = a.make();}
    puts("b3");
    {B b = ap()->make();}
    puts("b4");
    {B b = A().make();}
}
// <<<--- end bug.cpp --->>>

Output is (same for both 4.8.1 and 4.6.3):
$ g++ bug.cpp && ./a.out
b1
        ~B
b2
        ~B
b3
        ~B
        ~B
b4
        ~B
        ~B

The workaround is simple enough to apply, if you happen to notice all the extra object copies being made; I isolated the test case from an app that used 5x more malloc bandwidth than necessary because a single static function called the wrong way returned a largish STL object by value.


---


### compiler : `gcc`
### title : `Suboptimal optimisation of ((x & 0x70) == 0x00 || (x & 0x70) == 0x10 || (x & 0x70) == 0x20)`
### open_at : `2013-08-03T17:01:42Z`
### last_modified_date : `2023-06-13T15:40:27Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=58073
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.1`
### severity : `enhancement`
### contents :
Created attachment 30605
Demonstration source code

When the attached demo code is compiled with gcc-4.8.1, two of the cases optimise fine and the third case is optimised suboptimally - probably because it initially matches the optimisation for the second case.

Going through the cases individually for 'shift' being 4:

 (1) return (mask(d) == (0x0 << shift));

This is rendered as a single TEST instruction in x86_64 asm:

   0:   f6 07 70                testb  $0x70,(%rdi)
   3:   0f 94 c0                sete   %al
   6:   c3                      retq   

which is good.

 (2) return (mask(d) == (0x0 << shift) ||
            	mask(d) == (0x1 << shift));

This is also rendered as a single TEST instruction:

  10:   f6 07 60                testb  $0x60,(%rdi)
  13:   0f 94 c0                sete   %al
  16:   c3                      retq   

which is again good.  The problem comes with the third case:

 (3) return (mask(d) == (0x0 << shift) ||
		           mask(d) == (0x1 << shift) ||
           		mask(d) == (0x2 << shift));

This is rendered as:

  20:   8b 17                   mov    (%rdi),%edx
  22:   b8 01 00 00 00          mov    $0x1,%eax
  27:   f6 c2 60                test   $0x60,%dl
  2a:   74 09                   je     35 <foo3+0x15>
  2c:   83 e2 70                and    $0x70,%edx
  2f:   83 fa 20                cmp    $0x20,%edx
  32:   0f 94 c0                sete   %al
  35:   f3 c3                   repz retq 

which is odd.  I would expect the thing to be turned into MOV, AND, CMP, SETE, RETQ since the numbers it is checking for lie adjacent to each other, starting from zero.

I think what has happened is that the first two comparisons matched the optimisation for case (2) - resulting in three extra instructions.

The compilation command line was:

gcc -O2 -c foo.c -Wall && objdump -d foo.o

The compiler version:

Using built-in specs.
COLLECT_GCC=/usr/bin/gcc
COLLECT_LTO_WRAPPER=/usr/libexec/gcc/x86_64-redhat-linux/4.8.1/lto-wrapper
Target: x86_64-redhat-linux
Configured with: ../configure --prefix=/usr --mandir=/usr/share/man --infodir=/usr/share/info --with-bugurl=http://bugzilla.redhat.com/bugzilla --enable-bootstrap --enable-shared --enable-threads=posix --enable-checking=release --with-system-zlib --enable-__cxa_atexit --disable-libunwind-exceptions --enable-gnu-unique-object --enable-linker-build-id --with-linker-hash-style=gnu --enable-languages=c,c++,objc,obj-c++,java,fortran,ada,go,lto --enable-plugin --enable-initfini-array --enable-java-awt=gtk --disable-dssi --with-java-home=/usr/lib/jvm/java-1.5.0-gcj-1.5.0.0/jre --enable-libgcj-multifile --enable-java-maintainer-mode --with-ecj-jar=/usr/share/java/eclipse-ecj.jar --disable-libjava-multilib --with-isl=/builddir/build/BUILD/gcc-4.8.1-20130603/obj-x86_64-redhat-linux/isl-install --with-cloog=/builddir/build/BUILD/gcc-4.8.1-20130603/obj-x86_64-redhat-linux/cloog-install --with-tune=generic --with-arch_32=i686 --build=x86_64-redhat-linux
Thread model: posix
gcc version 4.8.1 20130603 (Red Hat 4.8.1-1) (GCC) 

as supplied by Fedora: gcc-4.8.1-1.fc19.x86_64


---


### compiler : `gcc`
### title : `SIMD code requiring auxiliary array for best optimization`
### open_at : `2013-08-06T16:03:16Z`
### last_modified_date : `2021-08-28T18:48:33Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=58095
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `unknown`
### severity : `enhancement`
### contents :
Created attachment 30621
Source code and its generated asm code.

Hello. I have noticed a strange behavior when I'm trying to write SIMD code using provided SSE intrinsics. It looks like GCC is not able to generate/optimize same code like function (bar) for function (foo).


I was wondering how can I achieve same generated code for the function (foo) without going into trouble of defining and using an auxiliary array like function (bar).


I've tried using __restrict__ keyword for input data (foo2), but GCC still generates same code like function (foo). ICC and Clang also generate same code and fail to optimize.

Something strange I've noticed is that GCC 4.4.7 generates desired code for function (foo), but fails to do for function (foo2) and (bar). Newer versions generate exactly same code for function (foo) and (foo2), and desired code for function (bar).

Output attached is generated from GCC 4.8.1 using -O2 optimization level. I've used online GCC compiler from: http://gcc.godbolt.org/


---


### compiler : `gcc`
### title : `Useless GPR push and pop when only xmm registers are used.`
### open_at : `2013-08-09T12:38:28Z`
### last_modified_date : `2021-09-12T02:40:08Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=58110
### status : `RESOLVED`
### tags : `missed-optimization, ra`
### component : `target`
### version : `4.9.0`
### severity : `enhancement`
### contents :
Hi,attached code generates extra push/pop rbx pair while there is no gpr register assigned in segment between them.
This was generated by head xgcc -O3. A gcc-4.7 has similar issues with attached program.

  pushq   %rbx
        .cfi_def_cfa_offset 16
        .cfi_offset 3, -16
        movdqu  (%rsi), %xmm15
        movdqu  -16(%rsi,%rdx), %xmm14
        movdqu  16(%rsi), %xmm13
        movdqu  -32(%rsi,%rdx), %xmm12
        movdqu  32(%rsi), %xmm11
        movdqu  -48(%rsi,%rdx), %xmm10
        movdqu  48(%rsi), %xmm9
        movdqu  -64(%rsi,%rdx), %xmm8
        movdqu  64(%rsi), %xmm7
        movdqu  -80(%rsi,%rdx), %xmm6
        movdqu  80(%rsi), %xmm5
        movdqu  -96(%rsi,%rdx), %xmm4
        movdqu  96(%rsi), %xmm3
        movdqu  -112(%rsi,%rdx), %xmm2
        movdqu  112(%rsi), %xmm1
        movdqu  -128(%rsi,%rdx), %xmm0
        movdqu  %xmm15, (%rdi)
        movdqu  %xmm14, -16(%rdi,%rdx)
        movdqu  %xmm13, 16(%rdi)
        movdqu  %xmm12, -32(%rdi,%rdx)
        movdqu  %xmm11, 32(%rdi)
        movdqu  %xmm10, -48(%rdi,%rdx)
        movdqu  %xmm9, 48(%rdi)
        movdqu  %xmm8, -64(%rdi,%rdx)
        movdqu  %xmm7, 64(%rdi)
        movdqu  %xmm6, -80(%rdi,%rdx)
        movdqu  %xmm5, 80(%rdi)
        movdqu  %xmm4, -96(%rdi,%rdx)
        movdqu  %xmm3, 96(%rdi)
        movdqu  %xmm2, -112(%rdi,%rdx)
        movdqu  %xmm1, 112(%rdi)
        movdqu  %xmm0, -128(%rdi,%rdx)
        popq    %rbx


---


### compiler : `gcc`
### title : `Ineffective addressing mode used in loop.`
### open_at : `2013-08-09T12:57:49Z`
### last_modified_date : `2021-09-19T08:54:51Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=58112
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.9.0`
### severity : `enhancement`
### contents :
Hi, in following testcase gcc -O3 generates following loop:

        movq    %rsi, %r9
        subq    %rdx, %r9
        movq    %r9, %rdi
        movq    %r9, %rsi
        leaq    16(%r9), %r8
        addq    $32, %rdi
        addq    $48, %rsi
        .p2align 4,,10
        .p2align 3
.L14:
        movdqu  (%rdx,%r9), %xmm0
        addq    $64, %rdx
        movdqa  %xmm0, -64(%rdx)
        movdqu  -64(%rdx,%r8), %xmm0
        movdqa  %xmm0, -48(%rdx)
        movdqu  -64(%rdx,%rdi), %xmm0
        movdqa  %xmm0, -32(%rdx)
        movdqu  -64(%rdx,%rsi), %xmm0
        movdqa  %xmm0, -16(%rdx)
        cmpq    %rdx, %rcx
        jne     .L14
        rep; ret

It saves one addq $64, %rsi instruction. However it occupies four extra registers, and address calculations done at each iteration cost more and lead to bigger code than instruction saved.


---


### compiler : `gcc`
### title : `loops are not evaluated at compile time if loop count > 17`
### open_at : `2013-08-11T11:13:37Z`
### last_modified_date : `2021-12-17T07:58:46Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=58122
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `normal`
### contents :
This one was originally reported here:
http://gcc.gnu.org/ml/gcc-help/2013-08/msg00124.html

The original example was:
#include <stdio.h>
       
template <typename T>
inline T const& max (T const& a, T const& b)
{
  return a < b ? b : a;
}
       
int main()
{
  long long unsigned sum = 0;

  for (int x = 1; x <= 100000000; x++)
    sum += max (x, x + 1);

  printf("%llu\n", sum);
}

It seems that GCC 4.7 was able to evaluate the loop at compile time and reduce it to a constant value, but GCC 4.8 fails to do so.

I've also briefly checked with trunk rev 201282 and the problem seems to be still there.  Here is a reduced test case:

int test (void)
{
  int sum = 0;
  for (int x = 0; x < 100; x++)
    sum += x;

  return sum;
}

I've checked this with an SH cross compiler setup, but I don't think it matters.
The loops do get eliminated if the number of loop iterations is max. 17, for both the reduced example and the originally reported case.


---


### compiler : `gcc`
### title : `missed load PRE related to array index truncation`
### open_at : `2013-08-15T18:47:25Z`
### last_modified_date : `2021-08-02T17:35:27Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=58169
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `normal`
### contents :
Created attachment 30664
test case for 32 bit targets

gcc.dg/tree-ssa/ssa-pre-21.c fails for avr (which has 16 bit int
and sizetype).
The computation of k + 1L is done as unsigned int (16 bit),
but later ++k is performed as unsigned long (32 bit), and thus
array[k+1] is not re-used.

The problem can also be seen on i686-pc-linux-gnu (32 bit) native
by changing the testcase to do the index computations in 64 bit, as
per attachment.


---


### compiler : `gcc`
### title : `Missed optimization opportunity when returning a conditional`
### open_at : `2013-08-19T19:24:58Z`
### last_modified_date : `2022-11-19T23:24:58Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=58195
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.7.2`
### severity : `enhancement`
### contents :
When compiling the following function:

int a(int input)
{
    return input == 0 ? 0 : -input;
}

gcc is unable to see that the conditional and returning 0 can be optimized away, producing:

        movl    %edi, %edx
        xorl    %eax, %eax
        negl    %edx
        testl   %edi, %edi
        cmovne  %edx, %eax
        ret

For the record, I found out the above when I was testing what gcc would do with this function:

int a(int input)
{
    int value = 0;
    for(int n = input; n != 0; ++n)
        ++value;
    return value;
}

gcc is able to optimize that into the same asm code as above, but no further (not even if the conditional is written explicitly, as written in the first function above.)


---


### compiler : `gcc`
### title : `Suboptimal structure initialization with tree-sra`
### open_at : `2013-08-26T09:53:46Z`
### last_modified_date : `2021-01-08T18:54:50Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=58243
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `normal`
### contents :
Created attachment 30700
Example C code to be compiled at -O2 with/without -fno-tree-sra

See the attached code, which initializes a structure 4 byte long and copies it through the pointer parameter in various similar functions, except func0 which does the same bitwise setting using unsigned int to act as a reference for the generated code (assuming a specific structure layout).

All functions are functionally equivalent; all struct members are set to constants, either implicitly or explicitly, at initialization or afterwards, and should be compiled to the same code at -O2.  With tree-sra (default) that does not happen: there's byte-wise setting for at least x86_64-linux, armv5-linux-gnueabi and cris-* for some of the functions.  With -O2 -fno-tree-sra the same code is generated for all functions.  Observed for x86_64-unknown-linux-gnu, armv5-linux-gnueabi and cris-elf at r201882.

(I thought there already was a PR for this but couldn't find any.)


---


### compiler : `gcc`
### title : `unnecessary vtables emission for pure abstract classes`
### open_at : `2013-08-29T15:43:56Z`
### last_modified_date : `2021-08-11T21:34:37Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=58272
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `c++`
### version : `unknown`
### severity : `normal`
### contents :
Consider the following testcase:

class Interface {
public:
  virtual int f() = 0;
};

class Concrete : public Interface {
public:
  virtual int f();
};

int
Concrete::f()
{
  return 2;
}

Concrete*
do_stuff()
{
  Concrete* c = new Concrete();
  return c;
}

int
call_f()
{
  Interface* i = do_stuff();
  return i->f();
}

compiling this on x86-64 with:

g++ -fno-exceptions -S -o - -O2 vtables.cpp -fno-rtti

produces output with a vtable for Interface, which is completely unused in the compilation unit.  (Still does it when omitting -fno-rtti, so it's not a missing check for typeinfo emission or similar.)

Mozilla has a fair number of these and even though one can eliminate them via --gc-sections, they still take up time to assemble, write to disk, etc. etc.  Honza and I were talking about them and we did not know whether it was an ABI requirement that they be emitted or merely a bug in the compiler.  G++ appears to have some smarts about emitting the vtable for Concrete, so I am somewhat surprised that it doesn't have similar smarts for the vtable for Interface.


---


### compiler : `gcc`
### title : `Missed Opportunity for Aligned Vectorized Load`
### open_at : `2013-08-30T12:17:16Z`
### last_modified_date : `2021-07-21T03:23:21Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=58280
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.0`
### severity : `enhancement`
### contents :
Consider

void foo(int nr, int nc, int ldim,
         double *__restrict a, double *__restrict b)
{
    a = __builtin_assume_aligned(a, 32);
    b = __builtin_assume_aligned(b, 32);

    ldim = (ldim >> 5) << 5;
    
    for (int i = 0; i < nr; i++)
        for (int j = 0; j < nc; j++)
            a[i*ldim + j] += b[i*ldim + j];
}

Both GCC 4.7 and 4.8 on an AVX capable system with -march=native and -O3 vectorize the inner loop but utilise unaligned loads and stores.  It should be possible to reason that as "a" and "b" are aligned and ldim is a multiple of 32 bytes that "a + i*ldim" and "b + i*ldim" are also 32-byte aligned.  This would permit the inner loop to be vectorized with aligned loads.


---


### compiler : `gcc`
### title : `Add noexcept to functions with a narrow contract`
### open_at : `2013-09-06T17:33:19Z`
### last_modified_date : `2023-07-10T08:22:30Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=58338
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `libstdc++`
### version : `4.9.0`
### severity : `enhancement`
### contents :
Hello,

the standard only requires a noexcept specifier on functions with a wide contract, to allow some debug implementations of functions with a narrow contract. However, it also explicitly gives permission to strengthen the exception specification of non-virtual functions. I believe libstdc++ should add noexcept whereever it can, since this is supposed to help with performance.

Functions like vector::front seem like good candidates. I wouldn't mind if the debug version had a different exception specification, but that doesn't even seem necessary since libstdc++ aborts instead of throwing.

https://groups.google.com/a/isocpp.org/d/msg/std-discussion/lkRyImxouC0/kZpWqI0MjXsJ


---


### compiler : `gcc`
### title : `__builtin_unreachable prevents vectorization`
### open_at : `2013-09-08T08:20:22Z`
### last_modified_date : `2023-04-18T14:48:42Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=58359
### status : `NEW`
### tags : `missed-optimization, needs-bisection`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `enhancement`
### contents :
void f(int*q){
  int*p=(int*)__builtin_assume_aligned(q,32);
  for(int i=0;i<(1<<20);++i){
    if(p+i==0)__builtin_unreachable();
    p[i]=i;
  }
}

If I remove the line with __builtin_unreachable, this is vectorized at -O3. But as is, we have control flow in the loop and the vectorizer won't even try.


---


### compiler : `gcc`
### title : `[MIPS] Using LRA instead of reload increases code size for mips16`
### open_at : `2013-09-18T11:56:26Z`
### last_modified_date : `2021-12-19T00:00:11Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=58461
### status : `UNCONFIRMED`
### tags : `missed-optimization, ra`
### component : `rtl-optimization`
### version : `4.9.0`
### severity : `normal`
### contents :
Created attachment 30852
Test case to trigger LRA reload issue

While working on enabling LRA for MIPS (mips16 in particular) I have observed that LRA is not producing as optimal code as classic reload. The underlying cause of this is that the register allocation decisions made in IRA were sub-optimal but classic reload 'fixes' them whereas LRA does not. Regardless of fixing the IRA issues there is probably something to fix in LRA.

I have attached a patch that applies to top of tree to enable LRA for mips/mips16 and exposes two options to demonstrate how LRA differs from classic reload. I have also attached a test case (reload_test_mips16.i) which is a function from libjpeg.

The two options added by the patch are -mreload and -mfix-regalloc. LRA is default on with the patch applied:

* mips-sde-elf-gcc -Os -mips16 -march=m4kec reload_test_mips16.i

LRA introduces a number of reloads that involve $24 which is inaccessible to most mips16 instructions leading to an increase in code size. 

* mips-sde-elf-gcc -Os -mips16 -march=m4kec -mreload ...

Classic reload manages to avoid the reloads of $24 as its reloads converge to use the same reload register and eliminate $24 altogether.

* mips-sde-elf-gcc -Os -mips16 -march=m4kec -mfix-regalloc ...

LRA now outperforms classic reload as the initial register allocation by IRA is better so LRA does not hit the problem I am reporting.

The original register allocation from IRA is:
Disposition:
   26:r245 l0     2    2:r246 l0     4   28:r249 l0     2    3:r250 l0    16
    4:r251 l0    17    5:r252 l0     8    6:r253 l0     9   19:r260 l0    11
   15:r266 l0    24   12:r275 l0     3   11:r276 l0     2   10:r278 l0    10
   27:r281 l0     4    7:r282 l0     5    8:r283 l0     6    1:r284 l0     7
   29:r285 l0   mem   24:r286 l0    24   25:r287 l0     2   23:r288 l0    24
   22:r289 l0    24   21:r290 l0    24   20:r291 l0    24   18:r292 l0    24
   17:r293 l0    11   16:r294 l0    11   14:r295 l0    11   13:r296 l0    24
    9:r297 l0    24    0:r298 l0    24

The fixed register allocation from IRA is as follows, note the mems instead of hard registers 8-11,24:
Disposition:
   26:r245 l0     2    2:r246 l0     4   28:r249 l0     2    3:r250 l0   mem
    4:r251 l0   mem    5:r252 l0    16    6:r253 l0    17   19:r260 l0   mem
   15:r266 l0   mem   12:r275 l0     3   11:r276 l0     2   10:r278 l0   mem
   27:r281 l0     4    7:r282 l0     5    8:r283 l0     6    1:r284 l0     7
   29:r285 l0   mem   24:r286 l0   mem   25:r287 l0     2   23:r288 l0   mem
   22:r289 l0   mem   21:r290 l0   mem   20:r291 l0   mem   18:r292 l0   mem
   17:r293 l0   mem   16:r294 l0   mem   14:r295 l0   mem   13:r296 l0   mem
    9:r297 l0    24    0:r298 l0    24

So the issue (I believe) is that reloads from LRA do not converge as well as reloads introduced by classic reload. While this example can (and should) be fixed in the original register allocation it feels as though there is a problem to fix in LRA.

==============

[mfortune@mfortune-linux lra_bugreport]$ /althome/mips/tk/bin/mips-sde-elf-gcc -v
Using built-in specs.
COLLECT_GCC=/althome/mips/tk/bin/mips-sde-elf-gcc
COLLECT_LTO_WRAPPER=/althome/mips/tk/libexec/gcc/mips-sde-elf/4.9.0/lto-wrapper
Target: mips-sde-elf
Configured with: /althome/mips/git_br/gcc/configure --prefix=/althome/mips/tk --target=mips-sde-elf --with-gnu-as --with-gnu-ld --with-arch=mips32r2 --with-mips-plt --with-synci --with-llsc --with-newlib target_alias=mips-sde-elf --enable-languages=c,c++,lto
Thread model: single
gcc version 4.9.0 20130918 (experimental) (GCC)


---


### compiler : `gcc`
### title : `missing optimization opportunity for const std::vector compared to std::array`
### open_at : `2013-09-20T11:03:47Z`
### last_modified_date : `2023-07-26T16:42:22Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=58483
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.1`
### severity : `enhancement`
### contents :
this small testprogram shows a missing optimization opportunity for const std::vector when using initialization_list - in compared to std::array

#include <vector>
#include <numeric>
#include <array>

static int calc(const std::array<int,3> p_ints, const int& p_init)
//static int calc(const std::vector<int> p_ints, const int& p_init)
{
  return std::accumulate(p_ints.begin(), p_ints.end(), p_init);
}

int main()
{
  const int result = calc({10,20,30},100);
  return result;
}

optimizer-result using std::array

int main() ()
{
  <bb 2>:
  return 160;
}

the result using std::vector

int main() ()
{
  int __init;
  int _2;
  int _11;
  int _32;
  int * _33;

  <bb 2>:
  _33 = operator new (12);
  __builtin_memcpy (_33, &._79, 12);
  _32 = MEM[(const int &)_33];
  __init_28 = _32 + 100;
  _2 = MEM[(const int &)_33 + 4];
  __init_18 = _2 + __init_28;
  _11 = MEM[(const int &)_33 + 8];
  __init_13 = _11 + __init_18;
  if (_33 != 0B)
    goto <bb 3>;
  else
    goto <bb 4>;

  <bb 3>:
  operator delete (_33);

  <bb 4>:
  return __init_13;
}

according to Marc Gliss's answer in (http://gcc.gnu.org/ml/gcc/2013-09/msg00179.html)

"...
We don't perform such high-level optimizations. But if you expand, inline and simplify this program, the optimizers sees something like:

p=operator new(12);
memcpy(p,M,12); // M contains {10, 20, 30}
res=100+p[0]+p[1]+p[2];
if(p!=0) operator delete(p);

A few things that go wrong:
* because p is filled with memcpy and not with regular assignments,
the compiler doesn't realize that p[0] is known. 

* the test p != 0 is unnecessary (a patch that should help is pending review) * we would then be left with: 

p=new(12); delete p; return 160; 

gcc knows how to remove free(malloc(12)) but not the C++ variant (I don't even know if it is legal, or what conditions and flags are required to make it so).
..."

the pending patch is http://gcc.gnu.org/bugzilla/show_bug.cgi?id=19476

but the question is still can new(delete(12)) also removed like free(malloc(12)) in this scenario?


---


### compiler : `gcc`
### title : `Missed return value optimization`
### open_at : `2013-09-20T19:38:12Z`
### last_modified_date : `2023-07-06T01:58:50Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=58487
### status : `NEW`
### tags : `missed-optimization`
### component : `c++`
### version : `4.8.1`
### severity : `enhancement`
### contents :
$ cat rva.cpp
#include <iostream>

class rva
{
public:
    rva() { std::cout << "Default construction\n"; }
    rva(rva const&) { std::cout << "Copy construction\n"; }
    rva& operator=(rva const&) { std::cout << "Assignation\n"; }
    ~rva() { std::cout << "Destruction\n"; }
};

rva f(int i) {
    if (i == 0) {
        rva result;
        return result;
    } else {
        return rva();
    }
}

int main()
{
    { std::cout << "f(0)\n"; f(0); }
    { std::cout << "\nf(1)\n"; f(1); }
    { std::cout << "\ng(0)\n"; g(0); }
    { std::cout << "\ng(1)\n"; g(1); }
    return 0;
}
$ g++-4.8.1 --version
g++-4.8.1 (GCC) 4.8.1
Copyright (C) 2013 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

$ g++-4.8.1 rva.cpp  
$ ./a.out
f(0)
Default construction
Copy construction
Destruction
Destruction

f(1)
Default construction
Destruction


It seems to me that for f(0) the copy construction could be avoided.


---


### compiler : `gcc`
### title : `SLP vectorizes identical operations`
### open_at : `2013-09-22T07:04:09Z`
### last_modified_date : `2023-10-04T19:57:11Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=58497
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `normal`
### contents :
typedef float float4 __attribute__((vector_size(16)));

float4 g(int x)
{
  float4 W;
  W[0]=W[1]=W[2]=W[3]=x+1;
  return W;
}

is vectorized by SLP to:

  vect_cst_.4_11 = {x_1(D), x_1(D), x_1(D), x_1(D)};
  vect__2.3_13 = vect_cst_.4_11 + { 1, 1, 1, 1 };
  vect__3.6_14 = (vector(4) floatD.38) vect__2.3_13;

Maybe when a vector is really the same scalar copied into all slots it would be better not to turn the scalar ops into vector ops? (turning the 4 BIT_FIELD_REF writes into a constructor is still good though)


---


### compiler : `gcc`
### title : `Missed RTL optimization - same insns before unconditional jump as before the jump target`
### open_at : `2013-10-10T09:21:43Z`
### last_modified_date : `2023-06-09T17:10:58Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=58681
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.8.1`
### severity : `enhancement`
### contents :
While looking at PR58670 workaround, I've noticed we don't optimize very well:
int
foo (int a, int b)
{
  int c, d, e, f;
  if (a < 9)
    {
      c = -3;
      d = -1;
      e = -20;
      f = -5;
    }
  else
    {
      asm volatile goto ("bts $1, %0; jc %l[lab]" : : "m" (b) : "memory" : lab);
      asm ("");
      c = 0;
      d = 12;
      e = 26;
      f = 7;
      goto l;
    lab:
      c = 0;
      d = 12;
      e = 26;
      f = 7;
    l:;
    }
  return bar (bar (bar (c, d), e), f);
}

e.g. at -O0, the 4 assignments are the same right above a code label to which an unconditional jump jumps and above the unconditional jump.  If we detected that, we could remove the 4 assignments from the second bb and just adjust the unconditional jump to jump before the 4 assignments instead of after them.  Perhaps then even cfg cleanup would optimize away the jump (from asm goto) to just an unconditional jump elsewhere.    Note that if a < 9 in the testcase above is replaced with just a, then the insns are the same only before postreload, postreload then figures out that the %rdi already contains 0 and changes it, but apparently just in ebb and not in other bbs.

Could this optimization be perhaps performed before reload (or both before and after)?


---


### compiler : `gcc`
### title : `vect_get_loop_niters() fails for some loops`
### open_at : `2013-10-11T01:10:47Z`
### last_modified_date : `2021-12-12T10:21:32Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=58686
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `enhancement`
### contents :
Look at the following loop:


  unsigned int t = ...;
  do {
    ...
    t -= 4;
  } while (t >= 5);


When I tried to get the iteration number of this loop as an expression using vect_get_loop_niters(), it gave me the result "scev_not_known". If I changed the type of t into signed int, then I can get the result as below: 


t > 4 ? ((unsigned int) t + 4294967291) / 4 : 0


But even when t is unsigned, we should still get the result as:


t != 4 ? (t + 4294967291) / 4 : 0


I spent some time on tracking the reason why it failed to do so, and then reached the function assert_loop_rolls_lt(), in which the assumptions are built to make sure we can get the iteration number from the following formula:


(iv1->base - iv0->base + step - 1) / step


In the example above, iv1->base is t-4, iv0->base is 4 (t>=5 is t>4), and step is 4. This formula works only if


-step + 1 <= (iv1->base - iv0->base) <= MAX - step + 1

(MAX is the maximum value of the unsigned variant of type of t, and in this formula we don't have to take care of overflow.)


I think when (iv1->base - iv0->base) < -step + 1, then we can assume the number of times the back edge is taken is 0, and that is how niter->may_be_zero is built in this function. And niter->assumptions is built based on (iv1->base - iv0->base) <= MAX - step + 1. Note that we can only get the iteration number of the loop if niter->assumptions is always evaluated as true.

However, I found that the build of niter->assumptions does not involve both iv1->base and iv0->base, but only one of them. I think this is possibly a potential bug.

Further, the reason why we can get the iteration number if t is of unsigned int type is that niter->assumptions built here t-4 < MAX-3 is evaluated to true, by taking advantage of the fact that the overflow on signed int is undefined (so t-4 < MAX-3 can be converted to t < MAX+1, where MAX+1 is assumed to not overflow). But this is not working for unsigned int.

One more problem is the way how niter->may_be_zero is built. For the loop above, niter->may_be_zero I got is 4 > t - 4 - (-4 + 1), but we should make sure t-4 here does not overflow. Otherwise niter->may_be_zero is invalid. I think the function assert_loop_rolls_lt() should take care more of unsigned int types.

With this issue we cannot vectorize this loop as its iteration number is unknown.


Thank you!

Cong


---


### compiler : `gcc`
### title : `[meta-bug] __attribute__((returns_nonnull)) enhancements`
### open_at : `2013-10-11T12:19:15Z`
### last_modified_date : `2021-02-12T10:02:41Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=58689
### status : `NEW`
### tags : `diagnostic, meta-bug, missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `enhancement`
### contents :
For PR 20318, we added an attribute "returns_nonnull". For now, it is quite basic and only used by fold-const and VRP to assert in callers that the return value is != 0. However, there are many other things that could be done with it, see this conversation for details:

http://gcc.gnu.org/ml/gcc-patches/2013-10/msg00498.html
http://gcc.gnu.org/ml/gcc-patches/2013-10/msg00501.html
http://gcc.gnu.org/ml/gcc-patches/2013-10/msg00509.html

This includes in particular:
1) warn if a returns_nonnull function returns null (both using static analysis and runtime tests);
2) optimize the callee, back-propagating this non-null property and marking as unreachable the paths that would return 0;
3) preserve the nonnull property when inlining the function (assert_expr?);
4) mark a number of gcc functions with this attribute.

A number of these changes could be shared with the nonnull attribute and pointer dereferencing.


---


### compiler : `gcc`
### title : `Missed loop condition optimization opportunity`
### open_at : `2013-10-13T18:03:15Z`
### last_modified_date : `2021-08-18T22:57:39Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=58715
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.1`
### severity : `enhancement`
### contents :
Created attachment 30995
lzjb_decompress code from ZFS

Here is a snippet of the lzjb implementation from Open ZFS showing a change that tightens a loop condition in a frequently executed loop:

-			while (--mlen >= 0 && dst < d_end)
+			if (mlen > (d_end - dst))
+				mlen = d_end - dst;
+			while (--mlen >= 0)
 				*dst++ = *cpy++;

In the original version, dst increments toward d_end while mlen decrements toward 0 on each loop iteration. Eventually, one will reach its termination condition. Nothing else touches mlen, so it is safe to do mlen = MIN(mlen, d_end - dst) before the loop and drop the ` && dst < d_end` part of the condition. Even if it were used elsewhere, a temporary could be used to store the minimum of the two.

The assembly generated by GCC 4.8.1 on the original evaluates both conditions on each iteration while the assembly generated for the patched version does not. In addition, loop unrolling is done on the patched version on -O3 while the original sees no unrolling at any optimization level.


---


### compiler : `gcc`
### title : `Sub-optimal code for bit clear/set sequence`
### open_at : `2013-10-14T20:01:43Z`
### last_modified_date : `2021-07-26T21:47:33Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=58727
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `minor`
### contents :
GCC generates sub-optimal but functionally correct code when successively clearing a bit and setting another bit in an integral value, as shown in the "clear_set" and "set_clear" functions below. To be more specific, at all O-levels except "-O1", it emits code to clear the bit being set, prior to setting it. When splitting the clear and set operations with exactly the same bits, and calling them one after the other, the problem does not occur. It looks like this behaviour is caused by an optimization pass prior to inlining.

On ARM this may cause a superfluous instruction to be emitted. In most instructions, the 32-bit ARM ISA can only encode 8-bit immediate values. Most of those instructions provide 4 extra bits in their encoding to specify a rotation. This implies that when the bit being set ("SET" in the test case below) is close enough to the bit being cleared ("CLEAR"), the code generation phase merges the superflous clear for "SET" with the one for "CLEAR". When the bits are too far apart, however, an extra clear instruction is generated, even when optimizing with "-Os".

It looks like the root cause is a problem in the optimizer and not the code generator, since the same behaviour can be observed on x86_64. However, in the latter case this "bug" does not alter the number of instructions required. My knowledge of the x86 architecture is limited so I have no clue whether it causes any inefficiencies at all (instruction width, perhaps?).

The test case below contains six functions:
- "clear_set" and "set_clear" suffer from the problem described above: the compiler usually emits a superfluous clear for the bit being set;
- "clear" and "set" perform the individual operations;
- "clear_set_inline" and "set_clear_inline" are used to demonstrate that the problem does not occur when splitting and inlining the operations.

The tests were performed on a Gentoo x86_64 Linux system; GCC versions for both native and cross-compiler are given below.

## testcase.c #################################################################

enum masks { CLEAR = 0x400000, SET = 0x02 };
unsigned clear_set(unsigned a) { return (a & ~CLEAR) | SET; }
unsigned set_clear(unsigned a) { return (a | SET) & ~CLEAR; }
unsigned clear(unsigned a) { return a & ~CLEAR; }
unsigned set(unsigned a) { return a | SET; }
__attribute__((flatten)) unsigned clear_set_inline(unsigned a) { return set(clear(a)); }
__attribute__((flatten)) unsigned set_clear_inline(unsigned a) { return clear(set(a)); }

## GCC version (ARM) ##########################################################

$ arm-none-eabi-gcc -###
Using built-in specs.
COLLECT_GCC=/path/to/toolchain/bin/arm-none-eabi-gcc
COLLECT_LTO_WRAPPER=/path/to/toolchain/libexec/gcc/arm-none-eabi/4.8.1/lto-wrapper
Target: arm-none-eabi
Configured with: /path/to/builddir/src/gcc-4.8.1/configure --build=x86_64-build_unknown-linux-gnu --host=x86_64-build_unknown-linux-gnu --target=arm-none-eabi --prefix=/path/to/toolchain --with-local-prefix=/path/to/toolchain/arm-none-eabi/sysroot --disable-libmudflap --with-sysroot=/path/to/toolchain/arm-none-eabi/sysroot --with-newlib --enable-threads=no --disable-shared --with-pkgversion='crosstool-NG 1.19.0' --with-float=hard --disable-__cxa_atexit --with-gmp=/path/to/builddir/arm-none-eabi/buildtools --with-mpfr=/path/to/builddir/arm-none-eabi/buildtools --with-mpc=/path/to/builddir/arm-none-eabi/buildtools --with-ppl=no --with-isl=no --with-cloog=no --with-libelf=no --disable-lto --with-host-libstdcxx='-static-libgcc -Wl,-Bstatic,-lstdc++,-Bdynamic -lm' --enable-target-optspace --disable-libgomp --disable-libmudflap --disable-nls --disable-multilib --enable-languages=c
Thread model: single
gcc version 4.8.1 (crosstool-NG 1.19.0)

## GCC version (x86_64) #######################################################

$ gcc -###
Using built-in specs.
COLLECT_GCC=/usr/x86_64-pc-linux-gnu/gcc-bin/4.9.0-alpha20131013/gcc
COLLECT_LTO_WRAPPER=/usr/libexec/gcc/x86_64-pc-linux-gnu/4.9.0-alpha20131013/lto-wrapper
Target: x86_64-pc-linux-gnu
Configured with: /var/tmp/portage/sys-devel/gcc-4.9.0_alpha20131013/work/gcc-4.9-20131013/configure --prefix=/usr --bindir=/usr/x86_64-pc-linux-gnu/gcc-bin/4.9.0-alpha20131013 --includedir=/usr/lib/gcc/x86_64-pc-linux-gnu/4.9.0-alpha20131013/include --datadir=/usr/share/gcc-data/x86_64-pc-linux-gnu/4.9.0-alpha20131013 --mandir=/usr/share/gcc-data/x86_64-pc-linux-gnu/4.9.0-alpha20131013/man --infodir=/usr/share/gcc-data/x86_64-pc-linux-gnu/4.9.0-alpha20131013/info --with-gxx-include-dir=/usr/lib/gcc/x86_64-pc-linux-gnu/4.9.0-alpha20131013/include/g++-v4 --host=x86_64-pc-linux-gnu --build=x86_64-pc-linux-gnu --disable-altivec --disable-fixed-point --with-cloog --disable-isl-version-check --enable-lto --enable-nls --without-included-gettext --with-system-zlib --enable-obsolete --disable-werror --enable-secureplt --enable-multilib --with-multilib-list=m32,m64 --enable-libmudflap --disable-libssp --enable-libgomp --with-python-dir=/share/gcc-data/x86_64-pc-linux-gnu/4.9.0-alpha20131013/python --enable-checking=release --disable-libgcj --enable-libstdcxx-time --enable-languages=c,c++,fortran --enable-shared --enable-threads=posix --enable-__cxa_atexit --enable-clocale=gnu --enable-targets=all --with-bugurl=http://bugs.gentoo.org/ --with-pkgversion='Gentoo 4.9.0_alpha20131013'
Thread model: posix
gcc version 4.9.0-alpha20131013 20131013 (experimental) (Gentoo 4.9.0_alpha20131013)

## Compiler invocation / steps to reproduce ###################################

arm-none-eabi-gcc -O0 -S -fverbose-asm -o olevel0.s -c testcase.c
arm-none-eabi-gcc -O1 -fno-aggressive-loop-optimizations -fno-auto-inc-dec -fno-branch-count-reg -fno-combine-stack-adjustments -fno-common -fno-compare-elim -fno-cprop-registers -fno-defer-pop -fno-delete-null-pointer-checks -fno-dwarf2-cfi-asm -fno-early-inlining -fno-eliminate-unused-debug-types -fno-forward-propagate -fno-function-cse -fno-gcse-lm -fno-guess-branch-probability -fno-ident -fno-if-conversion -fno-if-conversion2 -fno-inline-atomics -fno-ipa-profile -fno-ipa-pure-const -fno-ipa-reference -fno-ira-hoist-pressure -fno-ira-share-save-slots -fno-ira-share-spill-slots -fno-ivopts -fno-keep-static-consts -fno-leading-underscore -fno-math-errno -fno-merge-constants -fno-merge-debug-strings -fno-move-loop-invariants -fno-peephole -fno-prefetch-loop-arrays -fno-reg-struct-return -fno-sched-critical-path-heuristic -fno-sched-dep-count-heuristic -fno-sched-group-heuristic -fno-sched-interblock -fno-sched-last-insn-heuristic -fno-sched-pressure -fno-sched-rank-heuristic -fno-sched-spec -fno-sched-spec-insn-heuristic -fno-sched-stalled-insns-dep -fno-section-anchors -fno-show-column -fno-shrink-wrap -fno-signed-zeros -fno-split-ivs-in-unroller -fno-split-wide-types -fno-strict-volatile-bitfields -fno-sync-libcalls -fno-toplevel-reorder -fno-trapping-math -fno-tree-bit-ccp -fno-tree-ccp -fno-tree-ch -fno-tree-coalesce-vars -fno-tree-copy-prop -fno-tree-copyrename -fno-tree-cselim -fno-tree-dce -fno-tree-dominator-opts -fno-tree-dse -fno-tree-forwprop -fno-tree-fre -fno-tree-loop-if-convert -fno-tree-loop-im -fno-tree-loop-ivcanon -fno-tree-loop-optimize -fno-tree-phiprop -fno-tree-pta -fno-tree-reassoc -fno-tree-scev-cprop -fno-tree-sink -fno-tree-slp-vectorize -fno-tree-slsr -fno-tree-sra -fno-tree-ter -fno-tree-vect-loop-version -fno-unit-at-a-time -fno-zero-initialized-in-bss -S -fverbose-asm -o olevel1-all-disabled.s -c testcase.c
arm-none-eabi-gcc -O1 -S -fverbose-asm -o olevel1.s -c testcase.c
arm-none-eabi-gcc -O1 -fexpensive-optimizations -S -fverbose-asm -o olevel2.s -c testcase.c
arm-none-eabi-gcc -Os -S -fverbose-asm -o olevels.s -c testcase.c

gcc -O0 -S -fverbose-asm -o olevel0-x86.s -c testcase.c
gcc -O1 -S -fverbose-asm -o olevel1-x86.s -c testcase.c
gcc -O1 -fexpensive-optimizations -S -fverbose-asm -o olevel2-x86.s -c testcase.c

## Observations & expected results ############################################

When adding "-Wall -Wextra" the compiler does not emit any warnings for any of the commands above.

The above commands generate 5 assembly files with different optimization levels:
1) olevel0.s at -O0
2) olevel1-all-disabled.s at -O1 with -fno-* for every -f* listed in olevel1.s
3) olevel1.s at -O1
4) olevel2.s at -O1 with -fexpensive-optimizations because it is the only -f* option additionally enabled with -O2 that causes the superflous clear to be emitted
5) olevels.s at -Os

The first interesting observation is that the superfluous clear is generated at -O0 ("olevel0.s"). The generated code for "clear_set" and "set_clear" is exactly the same, excluding comments/annotations (stripped for clarity):

 1:     str     fp, [sp, #-4]!
 2:     add     fp, sp, #0
 3:     sub     sp, sp, #12
 4:     str     r0, [fp, #-8]
 5:     ldr     r3, [fp, #-8]
 6:     bic     r3, r3, #4194304
 7:     bic     r3, r3, #2
 8:     orr     r3, r3, #2
 9:     mov     r0, r3
10:     sub     sp, fp, #0
11:     ldr     fp, [sp], #4
12:     bx      lr

Just for the record: bic = clear bits in the specified mask, 0x400000 = 4194304. If we take a look at lines 6-8, the following happens:
6: A &= ~CLEAR
7: A &= ~SET
8: A |= SET
The clear instruction at line 7 is superfluous.

Looking at the "*_inline" versions at "-O0" doesn't make sense since the compiler does not perform inlining at "-O0".

At "-O1", the code does not contain any superfluous instructions ("cat olevel1.s  | grep -vE '^\s*[@\.]' | sed -E 's/\s*@.*$//'"):

clear_set:
        bic     r0, r0, #4194304
        orr     r0, r0, #2
        bx      lr
set_clear:
        bic     r0, r0, #4194304
        orr     r0, r0, #2
        bx      lr
clear:
        bic     r0, r0, #4194304
        bx      lr
set:
        orr     r0, r0, #2
        bx      lr
clear_set_inline:
        bic     r0, r0, #4194304
        orr     r0, r0, #2
        bx      lr
set_clear_inline:
        bic     r0, r0, #4194304
        orr     r0, r0, #2
        bx      lr

Note that "clear_set", "set_clear", "clear_set_inline" and "set_clear_inline" are all identical. I have been unable to find out which particular optimization prevents the superfluous instruction from being emitted. I have tried to reverse all "-f*" optimization parameters enabled by "-O1" as found in "olevel1.s", but as should be visible from comparing "olevel1-all-disabled.s" and "olevel1.s" there is no difference in "clear_set" and "set_clear" other than in comments/annotations.

At "-O2" the superfluous clear is emitted once again. I have gone through the optimizations enabled by -O2 which are not enabled by -O1 by comparing the (verbose) assembly output. I have tracked down the cause to "-fexpensive-optimizations". Enabling this optimization flag in combination with -O1 results in the following output ("cat olevel2.s | grep -vE '^\s*[@\.]' | sed -E 's/\s*@.*$//'"):

clear_set:
        bic     r0, r0, #4194304
        bic     r0, r0, #2
        orr     r0, r0, #2
        bx      lr
set_clear:
        bic     r0, r0, #4194304
        bic     r0, r0, #2
        orr     r0, r0, #2
        bx      lr
clear:
        bic     r0, r0, #4194304
        bx      lr
set:
        orr     r0, r0, #2
        bx      lr
clear_set_inline:
        bic     r0, r0, #4194304
        orr     r0, r0, #2
        bx      lr
set_clear_inline:
        bic     r0, r0, #4194304
        orr     r0, r0, #2
        bx      lr

Note that the "*_inline" functions do not contain the superfluous clear instruction. The "-Os" case generates exactly the same instructions. Since "-Os" also enables "-fexpensive-optimizations" as can be seen from "olevels.s", the cause of the extra instruction at "-Os" is most likely the same as for "-O2".

The above examples all use the ARM 32-bit ISA. By providing the arguments "-march=armv7-m -mthumb" to the cross-compiler the exact same behaviour can be observed for Thumb.

On x86_64, the following happens with "-O0" ("cat olevel0-x86.s | grep -vE '^\s*[@\.]' | sed -E 's/\s*#.*$//'") in both "clear_set" and "set_clear":

1:      pushq   %rbp
2:      movq    %rsp, %rbp
3:      movl    %edi, -4(%rbp)
4:      movl    -4(%rbp), %eax
5:      andl    $-4194307, %eax
6:      orl     $2, %eax
7:      popq    %rbp
8:      ret

At line 5, the constant -4194307 is 0xFFBFFFFD in hex, so ~(CLEAR | SET). Once again, the bit that is set at line 6 with the "orl" instruction is first cleared in the "andl" instruction.

Surprisingly, at "-O1" on x86_64, the superfluous clear remains in place. In the inlined version the mask is correct, however ("cat olevel1-x86.s | grep -vE '^\s*[@\.]' | sed -E 's/\s*#.*$//'"):

clear_set:
        movl    %edi, %eax
        andl    $-4194307, %eax
        orl     $2, %eax
        ret
set_clear:
        movl    %edi, %eax
        andl    $-4194307, %eax
        orl     $2, %eax
        ret
clear:
        movl    %edi, %eax
        andl    $-4194305, %eax
        ret
set:
        movl    %edi, %eax
        orl     $2, %eax
        ret
clear_set_inline:
        movl    %edi, %eax
        andl    $-4194305, %eax
        orl     $2, %eax
        ret
set_clear_inline:
        movl    %edi, %eax
        andl    $-4194305, %eax
        orl     $2, %eax
        ret

The same behaviour is observed with "-Os", "-O2" and "-O3".

I guess something internal in GCC is causing the bit to be cleared before it is set even though there is absolutely no valid reason to do so from the perspective of the program. While on x86_64 it probably does not affect code performance, on ARM it adversely affects code size and perhaps performance (untested).


---


### compiler : `gcc`
### title : `x86: Better optimization for operations on global long long and long variables`
### open_at : `2013-10-15T21:34:51Z`
### last_modified_date : `2021-09-13T00:25:58Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=58741
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `target`
### version : `4.9.0`
### severity : `enhancement`
### contents :
Hello all,

I am using the experimental branch as well as version 4.6.3 to compile the following code using "gcc -S -O2 -Wall"

The code below produces inefficient assembly for x86 (i686-linux-gnu):
unsigned long long val;
unsigned long small;
unsigned long long example() {
	return val | small;
}

Which gives the following assembly:
example:
	movl	small, %ecx
	movl	val, %eax
	movl	val+4, %edx
	pushl	%ebx
	xorl	%ebx, %ebx
	orl	%ecx, %eax
	orl	%ebx, %edx
	popl	%ebx
	ret

A more efficient implementation could be (which is generated if "extern const" is added to the val and small definitions):
example:
	movl	small, %eax
	movl	val+4, %edx
	orl	val, %eax
	ret

This inefficiency also occurs if the bitwise-or is replaced with an bitwise-xor or subtraction.

Thanks


---


### compiler : `gcc`
### title : `[missed optimization] reduction of masks of builtin vectors not transformed to ptest or movemask instructions`
### open_at : `2013-10-18T16:05:24Z`
### last_modified_date : `2021-08-25T02:23:49Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=58790
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `10.0`
### severity : `normal`
### contents :
Testcase:
typedef int int32_4v __attribute__((__vector_size__(16)));
typedef long long int64_2v __attribute__((__vector_size__(16)));

bool all_equal1(int32_4v a, int32_4v b)
{
    const auto k = a == b;
    return k[0] && k[1] && k[2] && k[3];
}

bool all_equal2(int32_4v a, int32_4v b)
{
    const auto k = a == b;
    return __builtin_ia32_ptestc128((int64_2v)k, __extension__(int64_2v){-1, -1});
}

bool none_equal1(int32_4v a, int32_4v b)
{
    const auto k = a == b;
    return !k[0] && !k[1] && !k[2] && !k[3];
}

bool none_equal2(int32_4v a, int32_4v b)
{
    const auto k = a == b;
    return __builtin_ia32_ptestz128((int64_2v)k, (int64_2v)k);
}

bool some_equal1(int32_4v a, int32_4v b)
{
    return !all_equal1(a, b) && !none_equal1(a, b);
}

bool some_equal2(int32_4v a, int32_4v b)
{
    return !all_equal2(a, b) && !none_equal2(a, b);
}

bool some_equal3(int32_4v a, int32_4v b)
{
    const auto k = a == b;
    return __builtin_ia32_ptestnzc128((int64_2v)k, __extension__(int64_2v){-1, -1});
}

Compile with -O3 -msse4 -std=c++11.

The all_equal2, none_equal2, and some_equal3 functions use explicit calls to the ptest builtins to lead to the expected optimizations. All the other functions should get optimized accordingly.


---


### compiler : `gcc`
### title : `optimize alloca with constant size`
### open_at : `2013-10-21T04:12:01Z`
### last_modified_date : `2022-02-24T06:44:48Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=58817
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `enhancement`
### contents :
Hello,

I thought gcc already had this optimization but apparently not. We don't produce the same code with alloca and with arrays:

void f(int*);
void g(){
#if 1
  const int n=4;
  int a[n];
#elif 1
  int a[4];
#else
  int*a=__builtin_alloca(16);
#endif
  f(a);
}

possibly because arrays give alloca_with_align, not alloca.

There may be reasons why the transformation would be illegal though, I am not sure.


---


### compiler : `gcc`
### title : `conditional reduction does not vectorize`
### open_at : `2013-10-21T07:44:19Z`
### last_modified_date : `2021-06-08T14:01:34Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=58821
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `enhancement`
### contents :
in the following foo vectorize bar does not
(bar does not vectorize even for 
 if (x[i]>0) s+=x[i];
)
compiled as 
c++ -Ofast -fopt-info-loop -S condRed.cc -fopenmp -ftree-loop-if-convert-stores -march=core-avx2

gcc version 4.9.0 20131011 (experimental) [trunk revision 203426] (GCC) 

neither
#pragma omp simd reduction(+:s)
nor
#pragma ivdep
helps


const int N=1024;
float x[N], y[N];

float bar() {
  float s=0;
  for (int i=0; i<N; ++i)
   if (x[i]>0) s+=y[i];
  return s;
}


float foo() {
  float s=0;
  for (int i=0; i<N; ++i)
   s+= (x[i]>0) ?y[i] : 0;
  return s;
}



float barOMP() {
  float s=0;
#pragma omp simd reduction(+:s)
  for (int i=0; i<N; ++i)
   if (x[i]>0) s+=y[i];
  return s;
}


float fooOMP() {
  float s=0;
#pragma omp simd reduction(+:s)
  for (int i=0; i<N; ++i)
   s+= (x[i]>0) ?y[i] : 0;
  return s;
}


float barIVDEP() {
  float s=0;
#pragma ivdep
  for (int i=0; i<N; ++i)
   if (x[i]>0) s+=y[i];
  return s;
}


---


### compiler : `gcc`
### title : `tail-merge doesn't merge asm statements with vdef`
### open_at : `2013-10-24T09:08:42Z`
### last_modified_date : `2023-06-09T14:50:37Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=58860
### status : `NEW`
### tags : `inline-asm, missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `enhancement`
### contents :
Consider the test-case tail-merge-asm.c:
...
/* { dg-do compile } */
/* { dg-options "-O2 -ftree-tail-merge -fdump-tree-pre" } */

/* Type that matches the 'p' constraint.  */
#define TYPE void *

static inline
void bar (TYPE *r)
{
  TYPE t;
  __asm__ ("" : "=&p" (t), "=p" (*r));
}

void
foo (int n, TYPE *x)
{
  if (n == 0)
    bar (x);
  else
    bar (x);
}

/* { dg-final { scan-tree-dump-times "duplicate" 1 "pre"} } */
/* { dg-final { scan-tree-dump-times "__asm__" 1 "pre"} } */
/* { dg-final { cleanup-tree-dump "pre" } } */
...

The test fails:
...
PASS: gcc.dg/tail-merge-asm.c (test for excess errors)
FAIL: gcc.dg/tail-merge-asm.c scan-tree-dump-times pre "duplicate" 1
FAIL: gcc.dg/tail-merge-asm.c scan-tree-dump-times pre "__asm__" 1
...

It fails because:
- the asm statements are not stmt_local_def 
- tail-merge doesn't handle asm statements in gimple_equal_p.

The 2 stmts are merged in try_optimize_cfg during jump2 rtl pass.


---


### compiler : `gcc`
### title : `Improve 128/64 division`
### open_at : `2013-10-27T21:35:29Z`
### last_modified_date : `2022-05-08T04:39:48Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=58897
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `target`
### version : `4.9.0`
### severity : `enhancement`
### contents :
typedef unsigned __int128 ui;
ui f(ui a, unsigned long b){
  return a/b;
}

is compiled to a library call to __udivti3, which is implemented as a rather long loop. However, it seems to me that 2 calls to divq should do it (and sometimes only 1 if we have range information on the result).


Ideally the following would eventually compile to just mul+div, but that's probably too complicated for now.

unsigned long prod(unsigned long a, unsigned long b, unsigned long m){
  if (a >= m || b >= m) __builtin_unreachable ();
  return ((unsigned __int128) a * b) % m;
}


---


### compiler : `gcc`
### title : `small matrix multiplication non vectorized`
### open_at : `2013-10-28T10:39:55Z`
### last_modified_date : `2021-07-21T03:19:23Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=58902
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `enhancement`
### contents :
in the following example
matmul and matmul2 do not vectorize
the manual unroll does
c++ -std=c++11 -Ofast -S m3x10.cc -march=corei7-avx -fopt-info-vec-all
gcc version 4.9.0 20131011 (experimental) [trunk revision 203426] (GCC) 

cat m3x10.cc
const int nrow=3;
 alignas(32) double tmp[nrow][10];
 alignas(32) double param[nrow];
 alignas(32) double frame[10];

void matmul() {
    for (int j=0; j<nrow; ++j)
    for (int i=0; i<10; ++i)
        param[j] += tmp[j][i]*frame[i];
}

void matmul2() {
    for (int j=0; j<nrow; ++j) {
      double s=0;
      for (int i=0; i<10; ++i)
        s += tmp[j][i]*frame[i];
      param[j] =s;
    }
}


void matmul3() {
      for (int i=0; i<10; ++i) {
        param[0] += tmp[0][i]*frame[i];
        param[1] += tmp[1][i]*frame[i];
        param[2] += tmp[2][i]*frame[i];
    }
}



double vmul0() {
  double s=0;
    for (int i=0; i<10; ++i)
      s += tmp[0][i]*frame[i];
  return s;
}

double vmul1() {
  double s=0;
    for (int i=0; i<10; ++i)
      s += tmp[1][i]*frame[i];
  return s;
}


---


### compiler : `gcc`
### title : `[missed optimization] GCC fails to get the loop bound for some loops.`
### open_at : `2013-10-29T20:07:57Z`
### last_modified_date : `2021-12-12T10:16:01Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=58915
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `normal`
### contents :
Getting the correct loop upper bound is important for some optimizations. GCC tries to get this bound by calling bound_difference() in tree-ssa-loop-niters.c, where GCC finds all control-dependent predicates of the loop and attempt to extract bound information from each predicate. 

However, GCC fails to get the bound for some loops. Below shows such an example:

unsigned int i;
if (i > 0) {
   ...
   if (i < 4) {
      do {
         ...
         --i;
      } while (i > 0);
   }
}

Clearly the upper bound is 3. But GCC could not get it for this loop. The reason is that GCC check i<4 (i could be zero) and i>0 separately and from neither condition can the upper bound be calculated. Those two conditions may not be combined into one as there may exist other statements between them. 

One possible solution is letting GCC collect all conditions first then merge them before calculating the upper bound.


Any comments?


---


### compiler : `gcc`
### title : `Despite loop->safelen=INT_MAX / GCC ivdep: loop versioned for vectorization because of possible aliasing`
### open_at : `2013-10-30T18:58:10Z`
### last_modified_date : `2021-08-12T05:53:49Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=58927
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `normal`
### contents :
Compiling the testsuite's pr33426-ivdep-4.cc
  g++ -std=c++11 -O3 -fopt-info-vec-optimized g++.dg/vect/pr33426-ivdep-4.cc

shows that the C++11 range-based loop has loop versioning, even though it shouldn't due to GCC ivdep:

g++.dg/vect/pr33426-ivdep-4.cc:13:19: note: loop vectorized
g++.dg/vect/pr33426-ivdep-4.cc:13:19: note: loop versioned for vectorization because of possible aliasing
g++.dg/vect/pr33426-ivdep-4.cc:13:19: note: loop peeled for vectorization to enhance alignment


The function is simply:

#include <vector>

template<class T, class T2>
void Loop(T *b, T2 c) {
#pragma GCC ivdep
  for (auto &i : *b) {
    i *= *c;
  }
}

void foo(std::vector<int> *ar, int *b) {
 Loop<std::vector<int>, int*>(ar, b);
}


---


### compiler : `gcc`
### title : `operator== between std::string and const char* slower than strcmp`
### open_at : `2013-11-08T10:59:48Z`
### last_modified_date : `2022-06-14T20:21:19Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=59048
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `libstdc++`
### version : `4.9.0`
### severity : `normal`
### contents :
Template functions
bool operator==( const char*, const std::string& ) and
bool operator==( const std::string&, const char* )
creates unecessary temporary std::string object. I'm using mainly GCC 4.4.7, but I have tested GCC 4.8.3 and the behavior is exactly the same.

Look at this simple example:
1) here we call operator==(std::string&, const char*):
size_t f(const std::string &str)
{
    size_t result = 0;
    size_t len = str.size();
    for (size_t i=0; i<len; ++i)
        if (str == "ST")
            result += i;
    return result;
}

2) here we call operator==(const char*, const std::string&)
size_t h(const std::string &str)
{
    size_t result = 0;
    size_t len = str.size();
    for (size_t i=0; i<len; ++i)
        if ("ST" == str)
            result += i;
    return result;
}

3) here a basic const char* version
size_t ii(const char *str)
{
    size_t result = 0;
    size_t len = strlen(str);
    for (size_t i=0; i<len; ++i)
        if (0 == strcmp(str,"ST"))
            result += i;
    return result;
}

4) here a mixed version: std::string compared with strcmp().
size_t g(const std::string &str)
{
    size_t result = 0;
    size_t len = str.size();
    for (size_t i=0; i<len; ++i)
        if (0 == strcmp(str.c_str(),"ST"))
            result += i;
    return result;
}

This is the main I used to test these functions:
int main(int argc, char **argv )
{
    long how_many_times=atol( argv[1] );
    std::string events[]={ "CASH", "EQ", "FI", "FT", "FWD", "OP", "ST" };
    size_t result=0;
    for (size_t i=0; i<how_many_times; ++i)
        for (size_t j=0; j<elements(events); ++j)
            result += f(events[j]);

    std::cout <<result <<std::endl;
    return 0;
}

Few things to notice: running time ./a.out
f() will produce:
bash-4.1$ time ./a.out 10000000
10000000
real    0m4.222s

g() will produce:
bash-4.1$ time ./a.out 10000000
10000000
real    0m1.036s

h() will produce:
bash-4.1$ time ./a.out 10000000
10000000
real    0m4.223s

ii() (if we change in main() std::string events[]={...} into const char* events[]={...}) will produce:
bash-4.1$ time ./a.out 10000000
10000000
real    0m1.266s
if I remove the call to strlen() will be basically 0seconds.

Which is the problem?
The problem here is that: why f()/h() are taking basically 4times more then g()? The only different is how we compare strings. It seems like that f() and h() are creating a temporary std::string object. Shouldn't we have the same performance? It seems like the compare() method of the char_trait<char> could be better implemented.

As a final notice: I have compiled all examples with g++ -O3 (Linux 64 and MacOS Snow Lion).


---


### compiler : `gcc`
### title : `poor code generated at -Os (affecting all gcc versions): 10+ sec vs. 1 sec at -O0`
### open_at : `2013-11-09T16:11:45Z`
### last_modified_date : `2021-08-15T05:53:22Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=59062
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.9.0`
### severity : `normal`
### contents :
The current gcc trunk (as well as 4.6, 4.7, and 4.8) produces poor code for the  following testcase on x86_64-linux-gnu at -Os in both 32-bit and 64-bit modes. 

The produced code has the same or very similar size. 

$ gcc-trunk -v
Using built-in specs.
COLLECT_GCC=gcc-trunk
COLLECT_LTO_WRAPPER=/usr/local/gcc-trunk/libexec/gcc/x86_64-unknown-linux-gnu/4.9.0/lto-wrapper
Target: x86_64-unknown-linux-gnu
Configured with: ../gcc-trunk/configure --enable-languages=c,c++,objc,obj-c++,fortran,lto --disable-werror --enable-checking=release --with-gmp=/usr/local/gcc-trunk --with-mpfr=/usr/local/gcc-trunk --with-mpc=/usr/local/gcc-trunk --with-cloog=/usr/local/gcc-trunk --prefix=/usr/local/gcc-trunk
Thread model: posix
gcc version 4.9.0 20131109 (experimental) [trunk revision 204611] (GCC) 
$ 
$ gcc-trunk -O0 small.c       
$ time a.out
1.02user 0.00system 0:01.05elapsed 97%CPU (0avgtext+0avgdata 1584maxresident)k
0inputs+0outputs (0major+142minor)pagefaults 0swaps
$ gcc-trunk -O1 small.c
$ time a.out
0.68user 0.00system 0:00.68elapsed 98%CPU (0avgtext+0avgdata 1568maxresident)k
0inputs+0outputs (0major+140minor)pagefaults 0swaps
$ gcc-trunk -Os small.c
$ time a.out
12.84user 0.00system 0:12.86elapsed 99%CPU (0avgtext+0avgdata 1568maxresident)k
0inputs+0outputs (0major+140minor)pagefaults 0swaps
$ 


--------------------------------


#pragma pack(1)
struct 
{
  int f0:23;
  unsigned int f1:23;
  unsigned int f2:7;
} b, c; 

unsigned int a; 

int 
main ()
{
  for (; a != 14; a += 9)
    c = b; 
  return 0;
}


---


### compiler : `gcc`
### title : `requesting optimization of safe rotate function`
### open_at : `2013-11-13T04:30:55Z`
### last_modified_date : `2019-11-22T05:31:31Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=59100
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `enhancement`
### contents :
Here is the obvious rotate idiom in C (this code is from Nettle):

#define ROTL32(n,x) (((x)<<(n)) | ((x)>>(32-(n))))

GCC does an admirable job of recognizing the code and turning it into a rotate instruction, when one is available.

The problem is that this code executes undefined behavior when n==0 or n==32.

Most crypto libraries are careful not to rotate by 32, but out of 10 libraries that I examined, 5 execute undefined behavior when rotating by zero.

We can make the obvious modification to protect against undefined rotate by 0:

#define ROTL32(n,x) ((n)==0?(x):(((x)<<(n)) | ((x)>>(32-(n)))))

Notice that this can be turned into exactly the same object code as the earlier macro since the rotate-by-0 special case is already handled by the rotate instruction.  However, this isn't what we get out of the compiler:

rotl32c:
	movl	%edi, %eax
	movb	%sil, %cl
	roll	%cl, %eax
	testl	%esi, %esi
	cmove	%edi, %eax
	ret

I'm in the process of trying to convince crypto library maintainers to fix their rotate functions and macros, and this will be easier if the fix doesn't have a performance penalty.

So would it be possible for you folks to teach the compiler to emit the better code for the safe rotate idiom?


---


### compiler : `gcc`
### title : `atomic ops on a non-escaped variable don't need atomicity`
### open_at : `2013-11-19T14:56:07Z`
### last_modified_date : `2021-12-28T05:43:06Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=59190
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `enhancement`
### contents :
#include <atomic>
int f(){
  std::atomic_int i(0);
  ++i;
  --i;
  return i;
}

As in PR 48987, I would like to see this replaced by return 0 (and probably a memory barrier), but for a different reason: no other thread can know about i, so the operations don't need to be atomic. Once you make them regular operations on an int, other optimizations should handle the rest.

Note that in my real use case, i is not an automatic variable, it is instead in memory locally allocated by malloc, but that should still be doable.

The idea is to allow people to have a single type for global and local use and still get the safety for one without losing too much speed for the other.


---


### compiler : `gcc`
### title : `if-conversion doesn't handle basic-blocks with only critical predecessor edges`
### open_at : `2013-11-22T11:42:28Z`
### last_modified_date : `2021-12-12T10:52:23Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=59249
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.2`
### severity : `normal`
### contents :
I am doing some investigation on loops can be vectorized by LLVM, but not GCC. One example is loop that contains more than one if-else constructs.

typedef signed char int8;
#define FFT         128

typedef struct {
    int8   exp[FFT];
} feq_t;

void test(feq_t *feq)
{
    int k;
    int feqMinimum = 15;
    int8 *exp = feq->exp;

    for (k=0;k<FFT;k++) {
	exp[k] -= feqMinimum;
	if(exp[k]<-15) exp[k] = -15;
	if(exp[k]>15) exp[k]  = 15;
    }
}

Compile it with 4.8.2 on x86_64
~/install-4.8/bin/gcc ghs-algorithms_380.c -O2 -fdump-tree-ifcvt-details -ftree-vectorize  -save-temps

It is not vectorized because if-else constructs inside the loop cannot be if-converted. Looking into .ifcvt file, this is due to bad if-else structure (ifcvt pass complains "only critical predecessors"). One branch jumps directly into another branch. Digging a bit deeper, I found such structure is generated by dom1 pass doing jump threading optimization. 

So recompile with 

~/install-4.8/bin/gcc ghs-algorithms_380.c -O2 -fdump-tree-ifcvt-details -ftree-vectorize  -save-temps -fno-tree-dominator-opts

It is magically if-converted and vectorized! Same on our target, performance is improved greatly in this example.

It seems to me that doing jump threading for architectures support if-conversion is not a good idea. Original if-else structures are damaged so that if-conversion cannot proceed, so are vectorization and maybe other optimizations. Should we try to identify those "bad" jump threading and skip them for such architectures? 

Andrew Pinski slightly modified the code and -fno-tree-dominator-opts trick won't work any more. 

#define FFT         128

typedef struct {
    signed char   exp[FFT];
} feq_t;

void test(feq_t *feq)
{
    int k;
    int feqMinimum = 15;
    signed char *exp = feq->exp;

    for (k=0;k<FFT;k++) {
signed char temp = exp[k] - feqMinimum;
        if(temp<-15) temp = -15;
        if(temp>15) temp  = 15;
exp[k] = temp;
    }
}

But this time is due to jump threading in VRP pass that causes the trouble. With -fno-tree-vrp, the code can be if-converted and vectorized again.


---


### compiler : `gcc`
### title : `We do not sink loads`
### open_at : `2013-11-26T13:37:00Z`
### last_modified_date : `2021-08-08T20:08:55Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=59299
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `normal`
### contents :
When fixing PR57517 I noticed that we don't sink loads leading to that PR

int x[1024], y[1024], z[1024], w[1024];
void foo (void)
{
  int i;
  for (i = 1; i < 1024; ++i)
    {
      int a = x[i];
      int b = y[i];
      int c = x[i-1];
      int d = y[i-1];
      if (w[i])
        z[i] = (a + b) + (c + d);
    }
}

results in

  <bb 4>:
  # i_18 = PHI <i_15(3), 1(2)>
  a_5 = x[i_18];
  b_6 = y[i_18];
  _7 = i_18 + -1;
  c_8 = x[_7];
  d_9 = y[_7];
  _10 = w[i_18];
  if (_10 != 0)
    goto <bb 5>;
  else
    goto <bb 8>;

  <bb 8>:
  goto <bb 6>;

  <bb 5>:
  _11 = a_5 + b_6;
  _12 = c_8 + d_9;
  _13 = _11 + _12;
  z[i_18] = _13;

  <bb 6>:
  i_15 = i_18 + 1;
  if (i_15 != 1024)
    goto <bb 3>;
  else
    goto <bb 7>;

instead of

  <bb 4>:
  # i_18 = PHI <i_15(3), 1(2)>
  _10 = w[i_18];
  if (_10 != 0)
    goto <bb 5>;
  else
    goto <bb 8>;

  <bb 8>:
  goto <bb 6>;

  <bb 5>:
  a_5 = x[i_18];
  b_6 = y[i_18];
  _7 = i_18 + -1;
  c_8 = x[_7];
  d_9 = y[_7];
  _11 = a_5 + b_6;
  _12 = c_8 + d_9;
  _13 = _11 + _12;
  z[i_18] = _13;

  <bb 6>:
  i_15 = i_18 + 1;
  if (i_15 != 1024)
    goto <bb 3>;
  else
    goto <bb 7>;

note that we eventually sink all computations into the if arm but only
stop at the loads.

tree-ssa-sink.c says:

@@ -294,8 +285,6 @@ statement_sink_location (gimple stmt, ba
      be seen by an external routine that needs it depending on where it gets
      moved to.
 
-     We don't want to sink loads from memory.
-
      We can't sink statements that end basic blocks without splitting the
      incoming edge for the sink location to place it there.
 
but doesn't give a good reason IMHO.

I have a simple patch.


---


### compiler : `gcc`
### title : `[11/12/13/14 Regression] Performance regression in GCC 4.8/9/10/11/12 and later versions.`
### open_at : `2013-12-02T17:58:58Z`
### last_modified_date : `2023-07-07T10:30:07Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=59371
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.9.0`
### severity : `normal`
### contents :
If I compile this program with -O2 on MIPS:

int foo(int *p, unsigned short c)
{
	signed short i;
	int x = 0;
	for (i = 0; i < c; i++) {
		x = x + *p; p++;
	}
	return x;
}

With GCC 4.7.* or earlier I get loop code that looks like:

$L3:
	lw	$5,0($4)
	addiu	$3,$3,1
	seh	$3,$3
	addu	$2,$2,$5
	bne	$3,$6,$L3
	addiu	$4,$4,4

With GCC 4.8 and later I get:

$L3:
	lw	$7,0($4)
	addiu	$3,$3,1
	seh	$3,$3
	slt	$6,$3,$5
	addu	$2,$2,$7
	bne	$6,$0,$L3
	addiu	$4,$4,4

This loop has one more instruction in it and is slower.
A version of this bug appears in EEMBC 1.1.  If I change the loop
index to be unsigned then I get the better code but I can't change
the benchmark I am testing so I am trying to figure out what changed
in GCC and how to generate the faster code.


---


### compiler : `gcc`
### title : `Unused code generated`
### open_at : `2013-12-05T11:06:41Z`
### last_modified_date : `2021-12-23T08:04:47Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=59394
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.8.2`
### severity : `normal`
### contents :
Created attachment 31385
source code

GCC:
avr-gcc -v
Using built-in specs.
COLLECT_GCC=avr-gcc
COLLECT_LTO_WRAPPER=/usr/lib/gcc/avr/4.8.2/lto-wrapper
Target: avr
Configured with: /build/avr-gcc/src/gcc-4.8.2/configure --disable-cloog-version-check --disable-install-libiberty --disable-libssp --disable-libstdcxx-pch --disable-libunwind-exceptions --disable-linker-build-id --disable-nls --disable-werror --enable-__cxa_atexit --enable-checking=release --enable-clocale=gnu --enable-cloog-backend=isl --enable-gnu-unique-object --enable-gold --enable-languages=c,c++ --enable-ld=default --enable-lto --enable-plugin --enable-shared --infodir=/usr/share/info --libdir=/usr/lib --libexecdir=/usr/lib --mandir=/usr/share/man --prefix=/usr --target=avr --with-as=/usr/bin/avr-as --with-gnu-as --with-gnu-ld --with-ld=/usr/bin/avr-ld --with-plugin-ld=ld.gold --with-system-zlib
Thread model: single
gcc version 4.8.2 (GCC) 

OS:
Arch Linux 
Linux 3.12.0-1-ARCH #1 SMP PREEMPT Wed Nov 6 09:06:27 CET 2013 x86_64 GNU/Linux

Command line:
avr-gcc -Wall -mmcu=atxmega64a3 -DF_CPU=16000000UL  -mno-interrupts -Os -pedantic-errors -pedantic -std=c++11 -Wfatal-errors -Wall    -I/usr/avr/include  -c main.cpp -o obj/Release/main.o
main.cpp: In function 'int main()':
main.cpp:55:21: warning: variable 'tval32' set but not used [-Wunused-but-set-variable]
   volatile uint32_t tval32;
                     ^
avr-g++  -o bin/Release/lambda_test.elf obj/Release/main.o   -mmcu=atxmega64a3 -Wl,-Map=bin/Release/lambda_test.map,--cref  
Output size is 7,92 KB
Running project post-build steps
avr-size bin/Release/lambda_test.elf
   text	   data	    bss	    dec	    hex	filename
    850	      0	   2400	   3250	    cb2	bin/Release/lambda_test.elf
avr-objdump -h -S bin/Release/lambda_test.elf > bin/Release/lambda_test.lss
Process terminated with status 0 (0 minutes, 0 seconds)
0 errors, 1 warnings (0 minutes, 0 seconds)

Source file: attached main.cpp
Generated assembly: attached lambda_test.lss

Problem.
A. As you can see in generated assembly:
1. function Sort_OldStyle(_Z13Sort_OldStylev) contain(as inline) functions Sort and Sort_OldStyle_Internal
2. function Sort_NewStyle(_Z13Sort_NewStylev) contain(as inline) functions Sort and lambda-expression

B. But also generated code contain unneded:
1. function Sort(_Z4SortPV5SPairS1_PFvRS0_E)
2. function Sort_OldStyle_Internal(_Z22Sort_OldStyle_InternalRV5SPair)
3. lambda-expression(_ZZ13Sort_NewStylevENUlRV5SPairE_4_FUNES1_)

Why gcc include functions from B-list if they already exist in functions of list A? Also why gcc use inline for function Sort and don't use call with -Os used?


---


### compiler : `gcc`
### title : `Optimization issue on min/max`
### open_at : `2013-12-09T06:01:24Z`
### last_modified_date : `2023-05-08T07:41:02Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=59424
### status : `RESOLVED`
### tags : `missed-optimization, patch`
### component : `middle-end`
### version : `4.7.2`
### severity : `enhancement`
### contents :
gcc seems to be having problems optimizing float min/max code and behaves unpredictably. If I compile the following code on an x86-64 (SSE enabled):

#include <math.h>

float func1(float a, float b) {
  return (a < b ? a : b);
}

float func2(float a, float b) {
  return sqrtf(a < b ? a : b);
}

float func3(float a, float b) {
  return fabsf(a < b ? a : b);
}

I get the following disassembly:

0000000000000000 <func1>:
func1():
   0:   f3 0f 5d c1             minss  %xmm1,%xmm0
   4:   c3                      retq   
   5:   66 66 2e 0f 1f 84 00    data32 nopw %cs:0x0(%rax,%rax,1)
   c:   00 00 00 00 

0000000000000010 <func2>:
func2():
  10:   f3 0f 5d c1             minss  %xmm1,%xmm0
  14:   f3 0f 51 c0             sqrtss %xmm0,%xmm0
  18:   c3                      retq   
  19:   0f 1f 80 00 00 00 00    nopl   0x0(%rax)

0000000000000020 <func3>:
func3():
  20:   0f 2f c8                comiss %xmm0,%xmm1
  23:   77 13                   ja     38 <func3+0x18>
  25:   f3 0f 10 05 00 00 00    movss  0x0(%rip),%xmm0        # 2d <func3+0xd>
  2c:   00 
  2d:   0f 54 c1                andps  %xmm1,%xmm0
  30:   c3                      retq   
  31:   0f 1f 80 00 00 00 00    nopl   0x0(%rax)
  38:   f3 0f 10 0d 00 00 00    movss  0x0(%rip),%xmm1        # 40 <func3+0x20>
  3f:   00 
  40:   0f 54 c1                andps  %xmm1,%xmm0
  43:   c3                      retq   


So gcc is correctly using maxss in func1 and func2, but not in func2. In practice, I'm using MIN/MAX macros extensively in libopus and gcc is missing the optimization most of the time, slowing down the code.


---


### compiler : `gcc`
### title : `Missed optimization opportunity in qsort-style comparison functions`
### open_at : `2013-12-09T11:35:28Z`
### last_modified_date : `2023-08-19T21:35:15Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=59429
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.1`
### severity : `enhancement`
### contents :
The following code:

extern int comLG(int, int);
extern int comLE(int, int);
extern int comEL(int, int);
extern int comEG(int, int);
extern int comGL(int, int);
extern int comGE(int, int);
int comLG(int a, int b) { return (a < b) ? -1 : (a > b) ? 1 : 0; }
int comLE(int a, int b) { return (a < b) ? -1 : (a == b) ? 0 : 1; }
int comEL(int a, int b) { return (a == b) ? 0 : (a < b) ? -1 : 1; }
int comEG(int a, int b) { return (a == b) ? 0 : (a > b) ? 1 : -1; }
int comGL(int a, int b) { return (a > b) ? 1 : (a < b) ? -1 : 0; }
int comGE(int a, int b) { return (a > b) ? 1 : (a == b) ? 0 : -1; }

when compiled with:

Using built-in specs.
COLLECT_GCC=gcc
COLLECT_LTO_WRAPPER=/usr/lib64/gcc/x86_64-suse-linux/4.8/lto-wrapper
Target: x86_64-suse-linux
Configured with: ../configure --prefix=/usr --infodir=/usr/share/info --mandir=/usr/share/man --libdir=/usr/lib64 --libexecdir=/usr/lib64 --enable-languages=c,c++,objc,fortran,obj-c++,java,ada --enable-checking=release --with-gxx-include-dir=/usr/include/c++/4.8 --enable-ssp --disable-libssp --disable-plugin --with-bugurl=http://bugs.opensuse.org/ --with-pkgversion='SUSE Linux' --disable-libgcj --disable-libmudflap --with-slibdir=/lib64 --with-system-zlib --enable-__cxa_atexit --enable-libstdcxx-allocator=new --disable-libstdcxx-pch --enable-version-specific-runtime-libs --enable-linker-build-id --program-suffix=-4.8 --enable-linux-futex --without-system-libunwind --with-arch-32=i586 --with-tune=generic --build=x86_64-suse-linux
Thread model: posix
gcc version 4.8.1 20130909 [gcc-4_8-branch revision 202388] (SUSE Linux) 

yields object code with different realizations and sizes.
What I observe:

$ gcc -Os -c cmp.c
(also shows with -O3)

$ readelf -s cmp.o
   Num:    Value          Size Type    Bind   Vis      Ndx Name
     8: 0000000000000000    16 FUNC    GLOBAL DEFAULT    1 comLG
     9: 0000000000000010    16 FUNC    GLOBAL DEFAULT    1 comLE
    10: 0000000000000020    18 FUNC    GLOBAL DEFAULT    1 comEL
    11: 0000000000000032    18 FUNC    GLOBAL DEFAULT    1 comEG
    12: 0000000000000044    18 FUNC    GLOBAL DEFAULT    1 comGL
    13: 0000000000000056    18 FUNC    GLOBAL DEFAULT    1 comGE

$ objdump -d cmp.o -Mintel
0000000000000000 <comLG>:
   0:   31 d2                   xor    edx,edx
   2:   39 f7                   cmp    edi,esi
   4:   b8 ff ff ff ff          mov    eax,0xffffffff
   9:   0f 9f c2                setg   dl
   c:   0f 4d c2                cmovge eax,edx
   f:   c3                      ret    

0000000000000010 <comLE>:
  10:   31 d2                   xor    edx,edx
  12:   39 f7                   cmp    edi,esi
  14:   b8 ff ff ff ff          mov    eax,0xffffffff
  19:   0f 95 c2                setne  dl
  1c:   0f 4d c2                cmovge eax,edx
  1f:   c3                      ret    

0000000000000020 <comEL>:
  20:   39 f7                   cmp    edi,esi
  22:   74 0b                   je     2f <comEL+0xf>
  24:   0f 9d c0                setge  al
  27:   0f b6 c0                movzx  eax,al
  2a:   8d 44 00 ff             lea    eax,[rax+rax*1-0x1]
  2e:   c3                      ret    
  2f:   31 c0                   xor    eax,eax
  31:   c3                      ret    

0000000000000032 <comEG>:
  32:   39 f7                   cmp    edi,esi
  34:   74 0b                   je     41 <comEG+0xf>
  36:   0f 9f c0                setg   al
  39:   0f b6 c0                movzx  eax,al
  3c:   8d 44 00 ff             lea    eax,[rax+rax*1-0x1]
  40:   c3                      ret    
  41:   31 c0                   xor    eax,eax
  43:   c3                      ret    

0000000000000044 <comGL>:
  44:   39 f7                   cmp    edi,esi
  46:   b8 01 00 00 00          mov    eax,0x1
  4b:   7f 08                   jg     55 <comGL+0x11>
  4d:   0f 9c c0                setl   al
  50:   0f b6 c0                movzx  eax,al
  53:   f7 d8                   neg    eax
  55:   c3                      ret    

0000000000000056 <comGE>:
  56:   39 f7                   cmp    edi,esi
  58:   b8 01 00 00 00          mov    eax,0x1
  5d:   7f 08                   jg     67 <comGE+0x11>
  5f:   0f 95 c0                setne  al
  62:   0f b6 c0                movzx  eax,al
  65:   f7 d8                   neg    eax
  67:   c3                      ret    

What I expected instead:

All functions to have the same asm.


---


### compiler : `gcc`
### title : `missed zero-extension elimination in the combiner`
### open_at : `2013-12-10T23:12:57Z`
### last_modified_date : `2019-09-10T14:05:31Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=59461
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.9.0`
### severity : `enhancement`
### contents :
This is a spin-off of PR rtl-optimization/58295.  The zero-extension is not (and has never been) eliminated on the SPARC at -O2:

ee_isdigit2:
        sethi   %hi(zeb_test_array), %g1
        or      %g1, %lo(zeb_test_array), %g1
        ldub    [%g1+%o0], %g1
        mov     0, %o0
        add     %g1, -48, %g1
        and     %g1, 0xff, %g1
        cmp     %g1, 9
        jmp     %o7+8
         movleu %icc, 1, %o0
        .size   ee_isdigit2, .-ee_isdigit2

The instruction "and %g1, 0xff, %g1" is redundant like on the ARM and the combiner should eliminate it.  The difference between the ARM and the SPARC is that the former explicitly zero-extends the load from memory while the latter does it only implicitly via LOAD_EXTEND_OP.  This shouldn't matter in the end, but does here because of some weakness of the nonzero_bits machinery.


---


### compiler : `gcc`
### title : `Inefficient vector assignment code`
### open_at : `2013-12-31T14:50:19Z`
### last_modified_date : `2021-08-21T22:05:32Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=59650
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.2`
### severity : `enhancement`
### contents :
Consider the following snippet:

    typedef double v4d __attribute__((vector_size(32)));

    v4d set1(double *v)
    {
        v4d tmp = { v[0], v[1], v[2], v[3] };
        return tmp;
    }

    v4d set2(double *v)
    {
        v4d tmp;
        
        tmp[0] = v[0];
        tmp[1] = v[1];
        tmp[2] = v[2];
        tmp[3] = v[3];
        
        return tmp;
    }

if my understanding of the vector extensions is correct they should both do the same thing.  Compiling with GCC 4.8.2 with -O3 -march=native on a Sandy Bridge system gives:

0000000000000000 <_Z4set1Pd>:
   0:   c5 fb 10 57 10          vmovsd 0x10(%rdi),%xmm2
   5:   c5 fb 10 1f             vmovsd (%rdi),%xmm3
   9:   c5 e9 16 47 18          vmovhpd 0x18(%rdi),%xmm2,%xmm0
   e:   c5 e1 16 4f 08          vmovhpd 0x8(%rdi),%xmm3,%xmm1
  13:   c4 e3 75 18 c0 01       vinsertf128 $0x1,%xmm0,%ymm1,%ymm0
  19:   c3                      retq   
  1a:   66 0f 1f 44 00 00       nopw   0x0(%rax,%rax,1)

0000000000000020 <_Z4set2Pd>:
  20:   c5 fb 10 07             vmovsd (%rdi),%xmm0
  24:   c5 f9 28 c0             vmovapd %xmm0,%xmm0
  28:   c5 f9 28 c8             vmovapd %xmm0,%xmm1
  2c:   c5 f1 16 4f 08          vmovhpd 0x8(%rdi),%xmm1,%xmm1
  31:   c4 e3 7d 18 c1 00       vinsertf128 $0x0,%xmm1,%ymm0,%ymm0
  37:   c4 e3 7d 19 c1 01       vextractf128 $0x1,%ymm0,%xmm1
  3d:   c5 f1 12 4f 10          vmovlpd 0x10(%rdi),%xmm1,%xmm1
  42:   c4 e3 7d 18 c1 01       vinsertf128 $0x1,%xmm1,%ymm0,%ymm0
  48:   c4 e3 7d 19 c1 01       vextractf128 $0x1,%ymm0,%xmm1
  4e:   c5 f1 16 4f 18          vmovhpd 0x18(%rdi),%xmm1,%xmm1
  53:   c4 e3 7d 18 c1 01       vinsertf128 $0x1,%xmm1,%ymm0,%ymm0
  59:   c3                      retq  

where I note the functions are different.  For set1 I note that four moves are issued whereas I was expecting two 128-bit unaligned moves.  The code for set2 also appears to be inefficient.


---


### compiler : `gcc`
### title : `large zero-initialized std::array compile time excessive`
### open_at : `2014-01-02T15:25:35Z`
### last_modified_date : `2023-04-05T17:21:28Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=59659
### status : `RESOLVED`
### tags : `compile-time-hog, memory-hog, missed-optimization`
### component : `c++`
### version : `4.8.2`
### severity : `normal`
### contents :
Compiling the below with any of the zero-initialization forms of std::atomic takes at least several hours (3GhZ Intel).   The default-initialized and non-atomic forms compile immediately.

g++ --std=c++11 -O0 : no other compile flags

reproducible under 4.8.2 and 4.7.2


#include <iostream>
#include <array>
#include <algorithm>
#include <atomic>

int main(int argc, char* argv[]) {

    // std::array<std::atomic<int>, 1000000>  arr;         // default initialization (i.e., random data) = FAST

    std::array<std::atomic<int>, 1000000>  arr{{}};   // zero initialization = FOREVER

    //std::array<std::atomic<int>, 1000000>  arr{};   // zero initialization = FOREVER

    //std::array<std::atomic<int>, 1000000>  arr={{}};     // zero init via assignment = FOREVER

    //std::array<int, 1000000>  arr={{}};     // zero init non-atomic = FAST

    std::cerr << "sum = " << std::accumulate(arr.begin(), arr.end(), 0) << std::endl;
}


---


### compiler : `gcc`
### title : `We fail to optimize common boolean checks pre-inlining`
### open_at : `2014-01-02T20:33:18Z`
### last_modified_date : `2023-08-18T20:42:52Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=59660
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `unknown`
### severity : `enhancement`
### contents :
We fail to inline the following function from graphite-poly.h:
/* Determine whether CHREC is an affine evolution function or not.  */

static inline bool
evolution_function_is_affine_p (const_tree chrec)
{
  return chrec
    && TREE_CODE (chrec) == POLYNOMIAL_CHREC
    && evolution_function_is_invariant_p (CHREC_RIGHT (chrec),
                                          CHREC_VARIABLE (chrec))
    && (TREE_CODE (CHREC_RIGHT (chrec)) != POLYNOMIAL_CHREC
        || evolution_function_is_affine_p (CHREC_RIGHT (chrec)));
}


It is tail recursive, but the recursion is easy to remove and handled by late tail recursion pass (post inlining).  Pre-inlining we stop at:
  <bb 6>:
  _15 = evolution_function_is_affine_p (_12);
  if (_15 != 0)
    goto <bb 7>;
  else
    goto <bb 8>;

  <bb 7>:

  <bb 8>:
  # iftmp.121_1 = PHI <1(7), 0(3), 0(2), 0(6), 0(4), 1(5)>
  return iftmp.121_1;


The conditional here is autogenerated by the boolean expression but is pointless. Phiopt gets it into:
  <bb 6>:
  _15 = evolution_function_is_affine_p (_12);

  <bb 7>:
  # iftmp.121_1 = PHI <1(5), 0(3), 0(2), _15(6), 0(4)>
  return iftmp.121_1;


This seems rather common pattern suggesting that perhaps we may phiopt pre-inline or do the same trick in one of existing early opts?


---


### compiler : `gcc`
### title : `Nios2: Missing gprel optimization`
### open_at : `2014-01-07T11:02:04Z`
### last_modified_date : `2019-11-13T16:24:39Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=59710
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `unknown`
### severity : `normal`
### contents :
The compiler doesn't generate gprel load/store operations for variables external to the translation unit (this is unlike the PowerPC target for example).  Consider the following test case:

gprel-ok.c:

int iii;
int jjj = 456;

void gprel_ok(void)
{
        iii = 123;
        jjj = 789;
}

gprel-not-ok.c:

extern int iii;
extern int jjj;

void gprel_not_ok(void)
{
        iii = 123;
        jjj = 789;
}

nios2-elf-gcc -O2 -fno-common -S gprel-ok.c
nios2-elf-gcc -O2 -fno-common -S gprel-not-ok.c

gprel-ok.s:

        .file   "gprel-ok.c"
        .section        .text
        .align  2
        .global gprel_ok
        .type   gprel_ok, @function
gprel_ok:
        movi    r2, 123
        stw     r2, %gprel(iii)(gp)
        movi    r2, 789
        stw     r2, %gprel(jjj)(gp)
        ret
        .size   gprel_ok, .-gprel_ok
        .global jjj
        .section        .sdata,"aws",@progbits
        .align  2
        .type   jjj, @object
        .size   jjj, 4
jjj:
        .long   456
        .global iii
        .section        .sbss,"aws",@nobits
        .align  2
        .type   iii, @object
        .size   iii, 4
iii:
        .zero   4
        .ident  "GCC: (GNU) 4.9.0 20140103 (experimental)"

gprel-not-ok.s:

        .file   "gprel-not-ok.c"
        .section        .text
        .align  2
        .global gprel_not_ok
        .type   gprel_not_ok, @function
gprel_not_ok:
        movi    r3, 123
        movhi   r2, %hiadj(iii)
        addi    r2, r2, %lo(iii)
        stw     r3, 0(r2)
        movi    r3, 789
        movhi   r2, %hiadj(jjj)
        addi    r2, r2, %lo(jjj)
        stw     r3, 0(r2)
        ret
        .size   gprel_not_ok, .-gprel_not_ok
        .ident  "GCC: (GNU) 4.9.0 20140103 (experimental)"


---


### compiler : `gcc`
### title : `missed optimization: attribute ((pure)) with aggregate returns`
### open_at : `2014-01-09T16:43:03Z`
### last_modified_date : `2021-12-22T09:07:03Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=59739
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `c++`
### version : `4.8.2`
### severity : `enhancement`
### contents :
Created attachment 31786
Script for demonstration

Attached is a script (t.sh) that creates two .cc files, compiles and executes them.

It tests whether attribute ((pure)) is used on different functions with this signatures:

struct Struct { int val; };
int globalInt();
Struct globalStruct();
struct Class {
  int classInt();
  Struct classStruct();
  virtual int classVirtualInt();
  virtual Struct classVirtualStruct();
};

The output with GCC is 4.8.2 is this:

globalInt: 1
globalStruct: 0
classInt: 1
classStruct: 0
classVirtualInt: 0
classVirtualStruct: 0

Meaning only globalInt and classInt are optimised.

All other functions are also candidates for attribute-pure optimisation.


---


### compiler : `gcc`
### title : `GIMPLE invariant motion misses opportunity to reduce register pressure`
### open_at : `2014-01-13T13:43:19Z`
### last_modified_date : `2021-12-25T07:24:32Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=59786
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `enhancement`
### contents :
For the following testcase LIM doesn't hoist a + b out of the loop (use -O1)

int x[1024];
void foo (int a, int b)
{
  int i;
  for (i = 0; i < 1024; ++i)
    x[i] = a + b;
}

_6 = a_4(D) + b_5(D);
  invariant up to level 1, cost 1.

but

/* The cost of expression in loop invariant motion that is considered
   expensive.  */
DEFPARAM(PARAM_LIM_EXPENSIVE,
         "lim-expensive",
         "The minimum cost of an expensive expression in the loop invariant motion",
         20, 0, 0)

and we only hoist "expensive" computations.  What is considered expensive
should consider the effect on register pressure.

Note that PRE happily moves all invariants without cost consideration.

For the testcase later RTL invariant motion hoists the addition.


---


### compiler : `gcc`
### title : `tail-call elimination didn't fire for left-shift of char to cout`
### open_at : `2014-01-14T21:35:28Z`
### last_modified_date : `2021-07-22T21:49:42Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=59813
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.2`
### severity : `normal`
### contents :
#include <iostream>
using namespace std;

void foo()
{
    cout << "x" << endl; // ok
    cout << 'x' << endl; // kills tail-call elimination in gcc 4.8.2
    foo();
}

int main() { foo(); return 0; }

// core-dups by long stack while in 4.7.3 works as expected (infinite loop)


---


### compiler : `gcc`
### title : `const array in function is placed on stack`
### open_at : `2014-01-17T18:50:54Z`
### last_modified_date : `2023-02-20T20:56:20Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=59863
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.8.2`
### severity : `normal`
### contents :
Created attachment 31875
Source file to reproduce the issue

This source code

int f(int i) {
  const int a[] = {1, 2, 3, 4};
  return a[i];
}

int g(int i) {
  static const int a[] = {1, 2, 3, 4};
  return a[i];
}

generates different code with GCC 4.8.2 on x86_64 for f() and g(). In f(), the const array is really created on the stack, and initialized one element at a time, instead of being placed in .rodata as it is for g().

With GCC on ARM (4.7), both arrays from f() and g() are placed in .rodata, but the code to access them is different:

	.text
	.align	2
	.global	f
	.type	f, %function
f:
	@ args = 0, pretend = 0, frame = 16
	@ frame_needed = 0, uses_anonymous_args = 0
	@ link register save eliminated.
	str	r4, [sp, #-4]!
	ldr	r3, .L2
	sub	sp, sp, #20
	mov	ip, r0
	ldmia	r3, {r0, r1, r2, r3}
	add	r4, sp, #16
	stmdb	r4, {r0, r1, r2, r3}
	add	ip, r4, ip, asl #2
	ldr	r0, [ip, #-16]
	add	sp, sp, #20
	ldmfd	sp!, {r4}
	bx	lr
.L3:
	.align	2
.L2:
	.word	.LANCHOR0
	.size	f, .-f
	.align	2
	.global	g
	.type	g, %function
g:
	@ args = 0, pretend = 0, frame = 0
	@ frame_needed = 0, uses_anonymous_args = 0
	@ link register save eliminated.
	ldr	r3, .L5
	add	r0, r3, r0, asl #2
	ldr	r0, [r0, #16]
	bx	lr
.L6:
	.align	2
.L5:
	.word	.LANCHOR0
	.size	g, .-g
	.section	.rodata
	.align	2
	.set	.LANCHOR0,. + 0
.LC0:
	.word	1
	.word	2
	.word	3
	.word	4
	.type	a.4057, %object
	.size	a.4057, 16
a.4057:
	.word	1
	.word	2
	.word	3
	.word	4

Note that on x86_64, clang generates the same code for f() and g() and even unifies both const arrays in .rodata.

Is there anything in the C standard preventing a const array declared in a function from being put in .rodata or are those missed optimizations?


---


### compiler : `gcc`
### title : `Missed C++ front-end devirtualizations`
### open_at : `2014-01-19T19:09:21Z`
### last_modified_date : `2023-08-04T21:42:43Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=59883
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `c++`
### version : `4.9.0`
### severity : `enhancement`
### contents :
I believe the following testcase:
     struct A 
    {
       virtual int foo (void) {return foo();}
    }; 

    struct B {
       struct A a;
    };
    struct A a[7]; 

    int test(void)
    {
      return a[3].foo();
    } 

    int test2(struct B *b)
    {
      return b->a.foo();
    }
ought to get devirtualized by C++ FE based on the fact that the object is contained within an structure or array. (this is related to PR46507)

In the following testcase:
namespace {
  struct A 
  {
    virtual int foo (void) {return 42;}
  };
}
int test(void)
{
  struct A a, *b=&a;
  return b->foo();
}

We can now probably use ipa-devirt's type inheritance graph to work out right away that A is a final class.

And finally:
struct A 
{
   virtual int foo (void) {return foo();}
};
IMO allows devirtualization of self recursive functions


---


### compiler : `gcc`
### title : `[11/12/13/14 Regression] Performance regression from 4.7.x to 4.8.x (loop not unrolled)`
### open_at : `2014-01-28T13:12:45Z`
### last_modified_date : `2023-07-07T10:30:12Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=59967
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.8.2`
### severity : `normal`
### contents :
Created attachment 31967
preprocessed source of ray/src/rt/ambient.c

gcc 4.8.x generates 10-15% slower code compared to 4.7.x for Mark Stock's radiance benchmark (http://markjstock.org/pages/rad_bench.html).

I observed this regression on Linux x86_64, and with different CPUs (Ivy Bridge, Haswell, AMD Phenom, Kaveri). I had suspected the new register allocator, but the actual cause is a difference in loop unrolling.

The hotspot is the nested loops with the recursive call at the end of the sumambient() function. When using -Ofast, gcc 4.7.x will unroll the outer loop, which results in some optimization possibilities in the inner loop. gcc 4.8.x does not unroll the outer loop. -funroll-loops does not change the behavior.


---


### compiler : `gcc`
### title : `Unnecessary edges in the CFG due to setjmp`
### open_at : `2014-01-29T16:48:45Z`
### last_modified_date : `2021-12-25T07:33:23Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=59986
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `enhancement`
### contents :
In a function with a setjmp call, we create unnecessary edges in the CFG.

An example from 59919:

typedef int jmp_buf[10];
struct S
{
  int i;
  jmp_buf buf;
};

void setjmp (jmp_buf);
void foo (int *);
__attribute__ ((__noreturn__, __nonnull__)) void bar (struct S *);

void
baz (struct S *p)
{
  bar (p);
  setjmp (p->buf);
  foo (&p->i);
}

In this case bar() is considered as ending a basic block (due to its noreturn attribute) and we create an abnormal outgoing edge from the block (due to the setjmp call later)

Conceptually ISTM that if we were to partition calls into two sets, those that are not reached by a setjmp and those which are reached by a setjmp.  The former do not need outgoing abnormal edges from their blocks.  Note that in turn may make some setjmp calls unreachable (as in the example above) which implies some kind of worklist algorithm.

The big question in my mind is how often we're able to eliminate those unnecessary edges and do we actually gain anything in real world code as a result of removing those unnecessary edges from the CFG.

Obviously if experiments show there isn't much gained, I'd suggest we just close/wontfix.


---


### compiler : `gcc`
### title : `VRP fails to fold identical unsigned comparisons`
### open_at : `2014-01-30T22:07:46Z`
### last_modified_date : `2021-07-20T07:27:25Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=60001
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `enhancement`
### contents :
void f(unsigned p,unsigned q){
  if(p>=q) throw 42;
  if(p>=q) throw 33;
}

VRP fails to eliminate the redundant comparison, only DOM manages to do it. Since VRP manages with either s/unsigned/int/ or s/>=/>/, I assume it should be doable.

(in practice, p is an index, q the size of an array, and I wish using unsigned for anything but bitops and modular arithmetic could be banned)


---


### compiler : `gcc`
### title : `suboptimal asm generated for a loop (store/load false aliasing)`
### open_at : `2014-02-05T22:41:08Z`
### last_modified_date : `2023-08-15T16:03:07Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=60086
### status : `NEW`
### tags : `inline-asm, missed-optimization`
### component : `rtl-optimization`
### version : `4.7.3`
### severity : `normal`
### contents :
Created attachment 32060
source code that compiles

Hello,

I am seeing suboptimal performance of the following loop compiled with
gcc 4.7.3 (but also 4.4.7, Ubuntu, full test code attached):

    for(i=0; i<NSIZE; i++){
      a[i] += b[i];
      c[i] += d[i];
    }

Arrays are dynamically allocated and aligned to page boundary, declared
with __restrict__ and __attribute__((aligned(32))). I am running on
Intel i7-2620M (Sandy Bridge).

The problem is IMHO related to '4k aliasing'. It happens for the most
common case of a/b/c/d starting at page boundary (e.g., natural result
of malloc). To demonstrate, here is the assembly generated with 'gcc
-mtune=native -mavx -O3':

.L8:
        vmovapd (%rdx,%rdi), %ymm0		#1 load b
        addq    $1, %r8				#2
        vaddpd  (%rcx,%rdi), %ymm0, %ymm0	#3 load a and add
        vmovapd %ymm0, (%rdx,%rdi)		#4 store a
        vmovapd (%rax,%rdi), %ymm0		#5 load d
        vaddpd  (%rsi,%rdi), %ymm0, %ymm0	#6 load c and add
        vmovapd %ymm0, (%rax,%rdi)		#7 store c
        addq    $32, %rdi			#8
        cmpq    %r8, %r12			#9
        ja      .L8				#10

The 4k aliasing problem is caused by lines 4 and 5 (writing result to
array a and reading data from either c or d). From my tests this seems
to be the default behavior for both AVX and SSE2 instruction sets, and
for both vectorized and non-vectorized cases.

It is easy to fix the problem by placing the two writes together, at the
end of the iteration, e.g.:

.L8:
        vmovapd (%rdx,%rdi), %ymm1		#1
        addq    $1, %r8				#2
        vaddpd  (%rcx,%rdi), %ymm1, %ymm1	#3
        vmovapd (%rax,%rdi), %ymm0		#4
        vaddpd  (%rsi,%rdi), %ymm0, %ymm0	#5
        vmovapd %ymm1, (%rdx,%rdi)		#6
        vmovapd %ymm0, (%rax,%rdi)		#7
        addq    $32, %rdi			#8
        cmpq    %r8, %r12			#9
        ja      .L8				#10

In this case the writes happen after all the loads. The above code is
(almost) what ICC generates for this case. For problem sizes small
enough to fit in L1 the speedup is roughly 50%.


---


### compiler : `gcc`
### title : `Complex arithmetic instructions`
### open_at : `2014-02-06T06:46:26Z`
### last_modified_date : `2023-06-25T22:10:33Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=60089
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.8.2`
### severity : `minor`
### contents :
Hello.

I'm porting gcc on some architecture which has complex addition, subtraction and multiplication instructions.

I was trying to define addchi3, subchi3 but it doesn't work.
I've figured out that complex operations are lowered at the tree-level.

Is there any way to support these instructions?

Thanks.


---


### compiler : `gcc`
### title : `load not folded into indirect branch on x86-64`
### open_at : `2014-02-07T00:17:20Z`
### last_modified_date : `2021-08-19T05:20:18Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=60104
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.8.2`
### severity : `enhancement`
### contents :
Created attachment 32075
a C testcase

The attached testcase is a greatly reduced interpreter loop, containing a simple load and indirect branch:

  goto *addresses[*pc++]

gcc 4.8.2 (as well as older versions) with -O2 produces the following x86-64 output:

  movq	addresses.1721(,%rax,8), %rax
  jmp	*%rax

Since the loaded value is not used after the branch, there's no need to hold it in a register, so the load could be folded into the branch. This would improve code size and instruction count.


---


### compiler : `gcc`
### title : `simd reduction clause suppresses simd auto-vectorization when -fopenmp is set`
### open_at : `2014-02-08T16:15:45Z`
### last_modified_date : `2021-08-21T18:53:47Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=60117
### status : `UNCONFIRMED`
### tags : `missed-optimization, openmp`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `normal`
### contents :
Created attachment 32082
source code reproducer

gcc version 4.9.0 20140203
gcc -O2 -ftree-vectorize -std=c99 -march=core-avx2 -fopt-info -S -fopenmp s314.c
This uses vmaxss instruction in the main loop body, in spite of the fairly positive vectorization report.
-O3 makes no significant difference, so -O2 is used in practice for stability elsewhere in gcc source code.
If the omp simd is disabled by removing -fopenmp, excellent code is produced using vmaxps.  Performance test shows 10x speedup with max-unroll-times=2.


---


### compiler : `gcc`
### title : `improve code for conditional sibcall`
### open_at : `2014-02-12T11:23:57Z`
### last_modified_date : `2021-08-19T03:31:33Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=60159
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `unknown`
### severity : `enhancement`
### contents :
If I compile this code for x86-64 I get:

$ cat jcc.c
extern int f(int x);
int g(int x) { return x > 3 ? f(x) : x; }

$ cc1 -quiet -O3 jcc.c -o -
...
g:
.LFB0:
        .cfi_startproc
        cmpl    $3, %edi
        jg      .L4
        movl    %edi, %eax
        ret
        .p2align 4,,10
        .p2align 3
.L4:
        jmp     f
        .cfi_endproc

This code would be simpler and shorter if the jg-to-jmp sequence was replaced with a single "jg f" instruction.

I'm using gcc built from svn trunk r207717.


---


### compiler : `gcc`
### title : `IVOPT has no idea of inline asm`
### open_at : `2014-02-14T21:52:20Z`
### last_modified_date : `2021-09-13T21:33:39Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=60206
### status : `UNCONFIRMED`
### tags : `inline-asm, missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `enhancement`
### contents :
Created attachment 32141
Testcase

This bug is found in google branch but I think the same problem also exists on trunk (but not exposed).

For the testcase 1.c attached (1.c is extracted from libgcc/soft-fp/divtf3.c), use trunk compiler gcc-r202164 (Target: x86_64-unknown-linux-gnu) + the patch r204497 could expose the problem.

The command:
gcc -v -O2 -fno-omit-frame-pointer -fpic -c -S -m32 1.c

The error:
./1.c: In function ‘__divtf3’:
./1.c:64:1194: error: ‘asm’ operand has impossible constraints

The inline asm in error message is as follow:
do {
 __asm__ (
"sub{l} {%11,%3|%3,%11}\n\t"
"sbb{l} {%9,%2|%2,%9}\n\t"
"sbb{l} {%7,%1|%1,%7}\n\t"
"sbb{l} {%5,%0|%0,%5}"
: "=r" ((USItype) (A_f[3])), "=&r" ((USItype) (A_f[2])), "=&r" ((USItype) (A_f[1])), "=&r" ((USItype) (A_f[0])) : "0" ((USItype) (B_f[2])), "g" ((USItype) (A_f[2])), "1" ((USItype) (B_f[1])), "g" ((USItype) (A_f[1])), "2" ((USItype) (B_f[0])), "g" ((USItype) (A_f[0])), "3" ((USItype) (0)), "g" ((USItype) (_n_f[_i])));
} while ()

Because -fno-omit-frame-pointer is turned on and the command line uses -fpic, there are only 5 registers for register allocation.

Before IVOPT,
%0, %1, %2, %3 require 4 registers. The index variable i of _n_f[_i] requires another register. So 5 registers are used up here.

After IVOPT, MEM reference _n_f[_i] is converted to MEM[base: _874, index: ivtmp.22_821, offset: 0B]. base and index require 2 registers, Now 6 registers are required, so LRA cannot find enough registers to allocate.

trunk compiler doesn't expose the problem because of patch r202165. With patch r202165, IVOPT doesn't change _n_f[_i] in inline asm above. But it just hided the problem.

Should IVOPT care about the constraints in inline-asm and restrict its optimization in some case?


---


### compiler : `gcc`
### title : `Redundant static initialization check`
### open_at : `2014-02-22T20:09:19Z`
### last_modified_date : `2021-12-22T09:09:10Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=60320
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `enhancement`
### contents :
Hello,

I think it would be nice if g++ realized that static variables that have been initialized don't later on become uninitialized again. A simple example:

extern int e;
static int b(){
  static const int a = e;
  return a;
}
int g(){
  return b()-b();
}

gets "optimized" to:

<bb 2>:
  _7 = MEM[(char *)&_ZGVZL1bvE1a];
  if (_7 == 0)
    goto <bb 3>;
  else
    goto <bb 9>;

  <bb 3>:
  _8 = __cxa_guard_acquire (&_ZGVZL1bvE1a);
  if (_8 != 0)
    goto <bb 5>;
  else
    goto <bb 4>;

  <bb 4>:
  pretmp_26 = a;
  goto <bb 6>;

  <bb 5>:
  e.2_9 = e;
  a = e.2_9;
  __cxa_guard_release (&_ZGVZL1bvE1a);

  <bb 6>:
  # prephitmp_27 = PHI <e.2_9(5), pretmp_26(4)>
  _11 = MEM[(char *)&_ZGVZL1bvE1a];
  if (_11 == 0)
    goto <bb 7>;
  else
    goto <bb 9>;

  <bb 7>:
  _12 = __cxa_guard_acquire (&_ZGVZL1bvE1a);
  if (_12 != 0)
    goto <bb 8>;
  else
    goto <bb 9>;

  <bb 8>:
  e.2_13 = e;
  a = e.2_13;
  __cxa_guard_release (&_ZGVZL1bvE1a);
  pretmp_5 = prephitmp_27 - e.2_13;

  <bb 9>:
  # prephitmp_3 = PHI <0(6), _12(7), pretmp_5(8), 0(2)>
  return prephitmp_3;


There may be a dup but I couldn't find it. It doesn't seem that easy to teach gcc about it. Maybe LTO-inlining of __cxa_guard_* functions would help (or not). We could emit _ZGVZL1bvE1a=1 after the release call, but that seems ugly. We could have special code that, for a MEM_REF[&var42], looks for a dominating call to __cxa_guard_release(&var42), and in that case asserts it is non-zero (is that, or a slight variant, valid?).


---


### compiler : `gcc`
### title : `ARM: inefficient code for vget_lane_f32 intrinsic`
### open_at : `2014-03-04T10:57:44Z`
### last_modified_date : `2021-08-30T03:41:25Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=60408
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.9.0`
### severity : `normal`
### contents :
Consider this trivial function:

#include <arm_neon.h>
float foo(float32x2_t v)
{
    return vget_lane_f32(v, 0) + vget_lane_f32(v, 1);
}

Compiling with gcc 4.9 trunk from 2014-03-02 yields this (non-code output removed):

$ gcc -O3 -march=armv7-a -mfpu=neon -S -o - test.c
foo:
        vmov.32 r3, d0[0]
        vmov.32 r2, d0[1]
        fmsr    s15, r3
        fmsr    s0, r2
        fadds   s0, s0, s15
        bx      lr

A simple "fadds s0, s0, s1" is what one would expect from code like this.


---


### compiler : `gcc`
### title : `superfluous arithmetic generated for uneven tail handling`
### open_at : `2014-03-04T14:53:10Z`
### last_modified_date : `2021-11-29T07:13:51Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=60412
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.8.2`
### severity : `enhancement`
### contents :
Created attachment 32262
Testcase showing superfluous arithmetic in assembly

The attached function processes a (possibly long) memory range. If more than 7 bytes are available, those are processed using g1(), which is able to process 8 bytes in one call. The tail end is then handled by g2(), one byte at a time. 

(In my application, the g1 and g2 functions are the Intel built-in CRC-32C operations.)

On Intel x86-64, the following superfluous assembly code is produced between the calls to g1() and g2():

$ gcc -v -O3 -Wall -Wextra  -c opt-tail.c 
...
Target: x86_64-unknown-linux-gnu
...
GNU C (GCC) version 4.8.2 (x86_64-unknown-linux-gnu)
        compiled by GNU C version 4.8.2, GMP version 5.1.2, MPFR version 3.1.1-p2, MPC version 1.0.1

$ objdump -C -D opt-tail.o
...
  44:   4c 89 e2                mov    %r12,%rdx
  47:   48 29 da                sub    %rbx,%rdx
  4a:   48 83 ea 08             sub    $0x8,%rdx
  4e:   48 c1 ea 03             shr    $0x3,%rdx
  52:   48 8d 5c d3 08          lea    0x8(%rbx,%rdx,8),%rbx

This seems to be completely redundant.


---


### compiler : `gcc`
### title : `X86 vectorization improve: pack instead of pshufb`
### open_at : `2014-03-06T22:32:43Z`
### last_modified_date : `2021-08-16T08:33:39Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=60451
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `unknown`
### severity : `enhancement`
### contents :
Created attachment 32294
test case

Currently vectorizer use 2 "pshufb" and "or" for even/odd permutation.
(odd case)
 pshufb  %xmm5, %xmm1
 pshufb  %xmm4, %xmm0
 por     %xmm0, %xmm1

 where
 %xmm4 0 2 4 6 8 a c e -1 -1 -1 -1 -1 -1 -1 -1
 %xmm5 -1 -1 -1 -1 -1 -1 -1 -1 0 2 4 6 8 a c e

gcc/config/i386/i386.c (expand_vec_perm_even_odd_1):

    case V16QImode: 
      if (TARGET_SSSE3) 
        return expand_vec_perm_pshufb2 (d);

However in case of even/odd we can use:

2 "pand" and 1 "packuswb"

  pand     %xmm6, %xmm0
  pand     %xmm6, %xmm1
  packuswb %xmm1, %xmm0
  
  where
  %xmm6 is 0x00ff00ff00ff00ff


This will improve performance for architectures with slow pshufb instructions and reduce code size on 1 constant.

For attached test Silvermont performance improve is 30%.


---


### compiler : `gcc`
### title : `gcc 4.8.2 fails to do optimization on global register variables when compiling on x86_64 Linux.`
### open_at : `2014-03-10T06:55:57Z`
### last_modified_date : `2021-12-24T04:22:16Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=60480
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.8.2`
### severity : `normal`
### contents :
gcc 4.8.2 fails to do optimization on  global register variables when compiling on x86_64 Linux.

Consider the following code:

     include <stdint.h>   

register uint64_t i0_BP __asm__ ("r14");
register uint64_t i0_SP __asm__ ("r15");

void test(void) {
        *((uint64_t*) (i0_SP - 8)) = i0_BP;
        i0_BP = i0_SP - 0x8;
        i0_SP -= 0x100;
        i0_SP = i0_BP;
        i0_BP = *((uint64_t*) i0_SP);
        i0_SP += 0x8;
        return;
}

Apply either ‘-O3’ or ‘-Os’ option to gcc, the final object file gives the same results as follows:

<test>:
   0:   lea    0xfffffffffffffff8(%r15),%rcx
   4:   mov    %r14,%rdx
   7:   mov    %r15,%rax
   a:   mov    %r14,0xfffffffffffffff8(%r15)
   e:   mov    %rcx,%r14
  11:   mov    %rcx,%r15
  14:   mov    %rdx,%r14
  17:   mov    %rax,%r15
  1a:   retq

Here we just try to emulate a frame establishment. In the object file, there are apparently lots of redundant ‘mov’s between registers. It seems to be a bug in gcc since we have already apply the maximum optimization level possible.

Environment:

On CentOS 5.10 (Linux 2.6.18 x86_64) using GCC 4.8.2

Using built-in specs.
COLLECT_GCC=gcc4
COLLECT_LTO_WRAPPER=/usr/local/GNU/gcc-4.8.2/libexec/gcc/x86_64-unknown-linux-gnu/4.8.2/lto-wrapper
Target: x86_64-unknown-linux-gnu
Configured with: ../gcc-4.8.2/configure --prefix=/usr/local/GNU/gcc-4.8.2 --enable-clocale=generic
Thread model: posix
gcc version 4.8.2 (GCC)


---


### compiler : `gcc`
### title : `Loop header copying code bloat for simple loops that don't benefit`
### open_at : `2014-03-15T13:10:14Z`
### last_modified_date : `2021-11-29T08:14:22Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=60537
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `enhancement`
### contents :
I have noticed this on SH, maybe it also applies to other targets (checked on 4.9 r208241).

The following simple loop (simple strlen implementation):

unsigned int test (const char* s0)
{
  const char* s1 = s0;

  while (*s1)
    s1++;

  return s1 - s0;
}

With -O2 -m4 gets compiled to:

        mov.b   @r4,r1
        tst     r1,r1
        bt/s    .L4
        mov     r4,r1
        add     #1,r1
	.align 2
.L3:
        mov     r1,r0
        mov.b   @r0,r2
        tst     r2,r2
        bf/s    .L3
        add     #1,r1
        rts
        sub     r4,r0
        .align 1
.L4:
        rts
        mov     #0,r0


With -Os -m4 it is basically just the inner loop:
        mov	r4,r1
.L2:
        mov     r1,r0
        mov.b   @r0,r2
        tst     r2,r2
        bf/s    .L2
        add     #1,r1
        rts
        sub     r4,r0


The additional loop test in the loop header in the -O2 version seems a bit pointless.  If the loop exists at the first iteration, it simply falls through.  The additional test and jump around the loop doesn't gain anything in this case but just increases code size unnecessarily.


---


### compiler : `gcc`
### title : `Don't convert int to float when comparing int with float (double) constant`
### open_at : `2014-03-15T14:59:12Z`
### last_modified_date : `2021-08-07T19:57:21Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=60540
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.9.0`
### severity : `enhancement`
### contents :
This is probably not something that one would write on purpose, but I've seen it somewhere:

bool test (int a)
{
  return a > 1.0;
}

On SH with -O2 -m4 this compiles to:

        lds     r4,fpul
        mova    .L3,r0
        fmov.s  @r0+,fr5    // load double constant 1.0
        fmov.s  @r0+,fr4

        float   fpul,dr2    // convert 'a' to double

        fcmp/gt dr4,dr2     // double > double
        rts
        movt    r0
.L4:
        .align 2
.L3:
        .long   0
        .long   1072693248

In this case an integer comparison could be done instead, which does not require converting the integer variable to float/double.  This seems like a target independent issue.


---
