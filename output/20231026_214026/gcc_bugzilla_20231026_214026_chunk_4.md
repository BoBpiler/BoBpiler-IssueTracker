### Total Bugs Detected: 4649
### Current Chunk: 4 of 30
### Bugs in this Chunk: 160 (From bug 481 to 640)
---


### compiler : `gcc`
### title : `gcc should vectorize this loop through if-conversion`
### open_at : `2010-03-18T18:01:11Z`
### last_modified_date : `2021-09-14T06:34:39Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=43423
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.5.0`
### severity : `enhancement`
### contents :
chfang@pathscale:~/gcc$ cat foo.c
int a[100], b[100], c[100];

void foo(int n, int mid)
{
  int i;
  for(i=0; i<n; i++)
    {
      if (i < mid)
        a[i] = a[i] + b[i];
      else
        a[i] = a[i] + c[i];
    }
}


chfang@pathscale:~/gcc$ gcc -O3 -ftree-vectorizer-verbose=7 -c foo.c

foo.c:6: note: not vectorized: control flow in loop.
foo.c:3: note: vectorized 0 loops in function.

This loop can be vectorized by icc.

For this case, I would expect to see two loops with iteration range
of [0, mid) and [mid, n). Then both loops can be vectorized.

I am not sure which pass in gcc should do this iteration range splitting.


---


### compiler : `gcc`
### title : `Missed vectorization: "unhandled data-ref"`
### open_at : `2010-03-18T21:51:06Z`
### last_modified_date : `2021-07-21T02:43:19Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=43436
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.5.0`
### severity : `enhancement`
### contents :
This kernel from FFmpeg is not vectorized with:
gcc-4.5 -c sub_hfyu_median_prediction.c -O3 -ffast-math -ftree-vectorizer-verbose=7 -msse2
[...]
sub_hfyu_median_prediction.c:18: note: not vectorized: unhandled data-ref 

Looking with GDB at it, I get:
(gdb) p debug_data_references (datarefs)
(Data Ref: 
  stmt: D.2736_16 = *D.2735_15;
  ref: *D.2735_15;
  base_object: *src1_14(D);
  Access function 0: {0B, +, 1}_1
)
(Data Ref: 
  stmt: 
  ref: 
  base_object: 
)

I think it is the dst data ref that is NULL.  Might be an aliasing
problem for the data dep analysis, but still, the data ref should be
analyzed correctly first.


typedef short DCTELEM;
typedef unsigned char uint8_t;
typedef long int x86_reg;
typedef unsigned int uint32_t;
typedef unsigned long int uint64_t;

void
sub_hfyu_median_prediction_c (uint8_t * dst, const uint8_t * src1,
			      const uint8_t * src2, int w, int *left,
			      int *left_top)
{
  int i;
  uint8_t l, lt;

  l = *left;
  lt = *left_top;

  for (i = 0; i < w; i++)
    {
      const int pred = mid_pred (l, src1[i], (l + src1[i] - lt) & 0xFF);
      lt = src1[i];
      l = src2[i];
      dst[i] = l - pred;
    }

  *left = l;
  *left_top = lt;
}

void add_hfyu_median_prediction_c(uint8_t *dst, const uint8_t *src1, const uint8_t *diff, int w, int *left, int *left_top)
{
  int i;
  uint8_t l, lt;

  l= *left;
  lt= *left_top;

  for(i=0; i<w; i++)
    {
      l= mid_pred(l, src1[i], (l + src1[i] - lt)&0xFF) + diff[i];
      lt= src1[i];
      dst[i]= l;
    }

  *left= l;
  *left_top= lt;
}


---


### compiler : `gcc`
### title : `Unnecessary temporary for global register variable`
### open_at : `2010-03-23T14:21:44Z`
### last_modified_date : `2023-05-26T02:32:26Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=43491
### status : `NEW`
### tags : `missed-optimization, ra`
### component : `tree-optimization`
### version : `4.5.0`
### severity : `enhancement`
### contents :
gcc sometimes allocates a temporary register for a variable that is global and has a fixed register. This happens when:
 a. the global is a register-fixed variable
 b. global is a pointer to structure
 c. an address of structure's field is passed as argument to inlined function
 d. the global is marked as constant


code:

struct b {
        unsigned g,h,j;
};

register struct b *const reg asm("r4");

static inline int diff(unsigned *p)
{
        return *p;
}

void c(void);

void d(void)
{
        while (diff(&reg->j))
                c();
}


generates:

d:
        @ args = 0, pretend = 0, frame = 0
        @ frame_needed = 0, uses_anonymous_args = 0
        ldr     r3, [r4, #8]    @ first ok
        push    {r5, lr}
        mov     r5, r4          @ an temporary even when r4 is marked const
        cbz     r3, .L1
.L4:   
        bl      c
        ldr     r3, [r5, #8]    @ accesses via temporary
        cmp     r3, #0
        bne     .L4
.L1:   
        pop     {r5, pc}


---


### compiler : `gcc`
### title : `G++ doesn't optimize away empty loop when index is a double`
### open_at : `2010-03-25T23:42:15Z`
### last_modified_date : `2023-08-08T01:38:43Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=43529
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.4.1`
### severity : `enhancement`
### contents :
Empty loops where the loop index is an integer are optimized away, but the following loop is not (presumably because it is more difficult to prove that it terminates in finite time?)

int main()
{
        for(double i=0; i<1e9; i+=1);
}

Command line: g++ -O3


---


### compiler : `gcc`
### title : `Reorder the statements in the loop can vectorize it`
### open_at : `2010-03-26T17:58:53Z`
### last_modified_date : `2021-08-24T23:59:43Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=43543
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.5.0`
### severity : `enhancement`
### contents :
int a[100], b[100], c[100], d[100];

void foo ()
{
  int i;
  for(i=1; i< 99; i++)
  {
    a[i] = b[i-1] + c[i];
    b[i] = b[i+1] + d[i];
  }
}

gcc -O3 -ffast-math -ftree-vectorizer-verbose=2 -c foo.c

foo.c:6: note: not vectorized, possible dependence between data-refs b[D.2728_3] and b[i_17]
foo.c:3: note: vectorized 0 loops in function.

However, if we reorder the two statements in the loop, then it can be vectorized. open64 can do this reordering.


---


### compiler : `gcc`
### title : `Missed address comparison folding of DECL_COMMONs`
### open_at : `2010-03-29T11:04:19Z`
### last_modified_date : `2019-09-06T21:45:46Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=43565
### status : `NEW`
### tags : `alias, missed-optimization`
### component : `tree-optimization`
### version : `4.5.0`
### severity : `enhancement`
### contents :
We should be able to optimize the comparison in the following testcase:


int *const g_82;
int *g_85[2][1];

int main (void)
{
  int **l_109 = &g_85[1][0];
  if (&g_82 != l_109)
    ;
  else
    link_error ();
  return 0;
}

it works with initializers for the variables with 4.4 but not with 4.5.


---


### compiler : `gcc`
### title : `Extra register move`
### open_at : `2010-04-01T07:25:28Z`
### last_modified_date : `2023-05-16T23:39:15Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=43616
### status : `RESOLVED`
### tags : `missed-optimization, ra`
### component : `rtl-optimization`
### version : `4.5.0`
### severity : `enhancement`
### contents :
Compile the following code with options -Os -march=armv7-a -mthumb

extern long long foo();
void bar2(long long* p)
{
  long long t = foo();
  *p = t;
}

GCC generates:

bar2:
        push    {r4, lr}
        mov     r4, r0
        bl      foo
        mov     r2, r0     // A
        mov     r3, r1     // B
        strd    r2, [r4]   // C
        pop     {r4, pc}

1. The register moves in instructions AB is a regression relate to gcc4.4.0. The result of gcc4.4 is:

        push    {r4, lr}
        mov     r4, r0
        bl      foo
        strd    r0, [r4]
        pop     {r4, pc}

The regression may be caused by some changes in ira. Before ira both versions have similar rtx sequence:

(call_insn 6 3 7 2 src/tb.c:4 (parallel [
            (set (reg:DI 0 r0)
                (call (mem:SI (symbol_ref:SI ("foo") [flags 0x41]  <function_decl 0x7f623ba6a600 foo>) [0 S4 A32])
                    (const_int 0 [0x0])))
            (use (const_int 0 [0x0]))
            (clobber (reg:SI 14 lr))
        ]) 255 {*call_value_insn} (nil)
    (nil))

(insn 7 6 8 2 src/tb.c:4 (set (reg/v:DI 133 [ t ])
        (reg:DI 0 r0)) 657 {*thumb2_movdi} (nil))

(insn 8 7 0 2 src/tb.c:5 (set (mem:DI (reg/v/f:SI 134 [ p ]) [2 S8 A64])
        (reg/v:DI 133 [ t ])) 657 {*thumb2_movdi} (expr_list:REG_DEAD (reg/v/f:SI 134 [ p ])
        (expr_list:REG_DEAD (reg/v:DI 133 [ t ])
            (nil))))

After ira, gcc4.5 generates:

(call_insn 6 3 7 2 src/tb.c:4 (parallel [
            (set (reg:DI 0 r0)
                (call (mem:SI (symbol_ref:SI ("foo") [flags 0x41]  <function_decl 0x7f623ba6a600 foo>) [0 S4 A32])
                    (const_int 0 [0x0])))
            (use (const_int 0 [0x0]))
            (clobber (reg:SI 14 lr))
        ]) 255 {*call_value_insn} (nil)
    (nil))

(insn 7 6 8 2 src/tb.c:4 (set (reg/v:DI 2 r2 [orig:133 t ] [133])
        (reg:DI 0 r0)) 657 {*thumb2_movdi} (expr_list:REG_EQUIV (mem:DI (reg/v/f:SI 4 r4 [orig:134 p ] [134]) [2 S8 A64])
        (nil)))

(insn 8 7 11 2 src/tb.c:5 (set (mem:DI (reg/v/f:SI 4 r4 [orig:134 p ] [134]) [2 S8 A64])
        (reg/v:DI 2 r2 [orig:133 t ] [133])) 657 {*thumb2_movdi} (nil))

But gcc4.4 generates:

(call_insn 6 3 8 2 src/tb.c:4 (parallel [
            (set (reg:DI 0 r0)
                (call (mem:SI (symbol_ref:SI ("foo") [flags 0x41] <function_decl 0xf7d1c880 foo>) [0 S4 A32])
                    (const_int 0 [0x0])))
            (use (const_int 0 [0x0]))
            (clobber (reg:SI 14 lr))
        ]) 257 {*call_value_insn} (nil)
    (nil))

(insn 8 6 16 2 src/tb.c:5 (set (mem:DI (reg/v/f:SI 4 r4 [orig:134 p ] [134]) [2 S8 A64])
        (reg/v:DI 0 r0 [orig:133 t ] [133])) 651 {*thumb2_movdi} (nil))

2. Since r4 is never used again after instruction C, it can also be written as a stm instruction. In thumb2, strd is a 32bit instruction, but stm is 16 bit.


---


### compiler : `gcc`
### title : `Incorrect sse2_cvtX2Y pattern`
### open_at : `2010-04-01T13:40:09Z`
### last_modified_date : `2022-07-04T06:24:38Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=43618
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.5.0`
### severity : `enhancement`
### contents :
Many SSE cvt instructions take 64bit memory source
instead of 128bit. In

(define_insn "sse2_cvtps2pd"
  [(set (match_operand:V2DF 0 "register_operand" "=x") 
        (float_extend:V2DF
          (vec_select:V2SF
            (match_operand:V4SF 1 "nonimmediate_operand" "xm") 
            (parallel [(const_int 0) (const_int 1)]))))]
  "TARGET_SSE2"
  "%vcvtps2pd\t{%1, %0|%0, %1}"
  [(set_attr "type" "ssecvt")
   (set_attr "prefix" "maybe_vex")
   (set_attr "mode" "V2DF")
   (set_attr "prefix_data16" "0")
   (set_attr "amdfam10_decode" "direct")])

memory operand is V2SF, not V4SF. As the result, we get

[hjl@gnu-6 tmp]$ cat x.c
float v2sf[8] __attribute ((aligned(16)));
double v4df[8] __attribute ((aligned(16)));
void
foo ()
{
  int i;
  for (i = 0; i < 8; i++)
    v4df[i] = v2sf[i];
}
[hjl@gnu-6 tmp]$ /usr/gcc-4.5/bin/gcc -S -O3 x.c
[hjl@gnu-6 tmp]$ cat x.s
	.file	"x.c"
	.text
	.p2align 4,,15
.globl foo
	.type	foo, @function
foo:
.LFB0:
	.cfi_startproc
	movaps	v2sf(%rip), %xmm1
	cvtps2pd	%xmm1, %xmm0
	movapd	%xmm0, v4df(%rip)
	xorps	%xmm0, %xmm0
	movhlps	%xmm1, %xmm0
	movaps	v2sf+16(%rip), %xmm1
	cvtps2pd	%xmm0, %xmm0
	movapd	%xmm0, v4df+16(%rip)
	cvtps2pd	%xmm1, %xmm0
	movapd	%xmm0, v4df+32(%rip)
	xorps	%xmm0, %xmm0
	movhlps	%xmm1, %xmm0
	cvtps2pd	%xmm0, %xmm0
	movapd	%xmm0, v4df+48(%rip)
	ret

instead of

[hjl@gnu-6 tmp]$ /opt/intel/Compiler/11.1/059/bin/intel64/icc -S -O2 x.c
[hjl@gnu-6 tmp]$ cat x.s
# -- Machine type EFI2
# mark_description "Intel(R) C++ Compiler for applications running on Intel(R) 64, Version 11.1    Build 20091012 %s";
# mark_description "-S -O2";
	.file "x.c"
	.text
..TXTST0:
# -- Begin  foo
# mark_begin;
       .align    16,0x90
	.globl foo
foo:
..B1.1:                         # Preds ..B1.0
..___tag_value_foo.1:                                           #5.1
        cvtps2pd  v2sf(%rip), %xmm0                             #8.15
        cvtps2pd  8+v2sf(%rip), %xmm1                           #8.15
        cvtps2pd  16+v2sf(%rip), %xmm2                          #8.15
        cvtps2pd  24+v2sf(%rip), %xmm3                          #8.15
        movaps    %xmm0, v4df(%rip)                             #8.5
        movaps    %xmm1, 16+v4df(%rip)                          #8.5
        movaps    %xmm2, 32+v4df(%rip)                          #8.5
        movaps    %xmm3, 48+v4df(%rip)                          #8.5
        ret                                                     #9.1


---


### compiler : `gcc`
### title : `Struct with two floats generates poor code`
### open_at : `2010-04-04T06:40:39Z`
### last_modified_date : `2021-08-16T01:16:37Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=43640
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `unknown`
### severity : `enhancement`
### contents :
struct u1
{
	float x;
	float y;
};

float foo(struct u1 u)
{
	return u.x + u.y;
}

compiles into
gcc-4.5 -O3 tgcc.c -c -o tgcc.o

   0x0000000000000000 <+0>:     movq   %xmm0,-0x20(%rsp)
   0x0000000000000006 <+6>:     mov    -0x20(%rsp),%rax
   0x000000000000000b <+11>:    mov    %eax,-0x14(%rsp)
   0x000000000000000f <+15>:    shr    $0x20,%rax
   0x0000000000000013 <+19>:    mov    %eax,-0x10(%rsp)
   0x0000000000000017 <+23>:    movss  -0x14(%rsp),%xmm0
   0x000000000000001d <+29>:    addss  -0x10(%rsp),%xmm0
   0x0000000000000023 <+35>:    retq

The instructions dealing with rax/eax can be elided if the movss and addss load from the correct stack locations.

A better sequence, avoiding memory, might be

pshufd %xmm0, %xmm1, 1
addss %xmm1, %xmm0
retq


---


### compiler : `gcc`
### title : `__uint128_t missed optimizations.`
### open_at : `2010-04-04T23:58:25Z`
### last_modified_date : `2023-08-01T08:21:53Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=43644
### status : `NEW`
### tags : `missed-optimization, ra`
### component : `target`
### version : `4.5.0`
### severity : `enhancement`
### contents :
__uint128_t foo1(__uint128_t x, __uint128_t y)
{
	return x + y;
}

   0x0000000000000520 <+0>:     mov    %rdx,%rax
   0x0000000000000523 <+3>:     mov    %rcx,%rdx
   0x0000000000000526 <+6>:     push   %rbx
   0x0000000000000527 <+7>:     add    %rdi,%rax
   0x000000000000052a <+10>:    adc    %rsi,%rdx
   0x000000000000052d <+13>:    pop    %rbx
   0x000000000000052e <+14>:    retq

%rbx isn't used, yet is saved and restored.

__uint128_t foo2(__uint128_t x, unsigned long long y)
{
	return x + y;
}
   0x0000000000000550 <+0>:     mov    %rdx,%rax
   0x0000000000000553 <+3>:     push   %rbx
   0x0000000000000554 <+4>:     xor    %edx,%edx
   0x0000000000000556 <+6>:     mov    %rsi,%rbx
   0x0000000000000559 <+9>:     add    %rdi,%rax
   0x000000000000055c <+12>:    adc    %rbx,%rdx
   0x000000000000055f <+15>:    pop    %rbx
   0x0000000000000560 <+16>:    retq

%rbx is used, but doesn't need to be. %rcx can be used instead, saving a push-pop pair.

__uint128_t foo3(unsigned long long x, __uint128_t y)
{
	return x + y;
}

   0x0000000000000580 <+0>:     mov    %rdi,%rax
   0x0000000000000583 <+3>:     push   %rbx
   0x0000000000000584 <+4>:     mov    %rdx,%rbx
   0x0000000000000587 <+7>:     xor    %edx,%edx
   0x0000000000000589 <+9>:     add    %rsi,%rax
   0x000000000000058c <+12>:    adc    %rbx,%rdx
   0x000000000000058f <+15>:    pop    %rbx
   0x0000000000000590 <+16>:    retq

Similar problems as with the previous two functions, with the addition of the fact that %rdx can now be used in-situ as an output, avoiding one of the mov instructions.  i.e. the function could be optimized to be:

mov    %rdi,%rax
xor    %ecx,%ecx
add    %rsi,%rax
adc    %rcx,%rdx
retq


---


### compiler : `gcc`
### title : `GCC doesn't duplicate computed gotos for functions marked as "hot"`
### open_at : `2010-04-08T12:46:22Z`
### last_modified_date : `2021-07-24T06:03:27Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=43686
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.4.3`
### severity : `normal`
### contents :
I've found the bug working on direct threaded interpreter for PHP. Moving from GCC 4.3 to GCC 4.4 caused a significant performance degradation. Looking into produced assembler code I realized that GCC 4.4 doesn't replace all jmps to indirect jmp with indirect jmp itself. The reason is the following new condition in function duplicate_computed_gotos() bb-reorder.c 

if (!optimize_bb_for_size_p (bb))
  continue;

I thought I would able to fix the problem using "hot" attribute, but
according to this condition, in case I mark function with __attribute__((hot)) duplication doesn't work, and in case I mark it with __attribute__((cold)) it starts work. As result "hot" function works slower than "cold".

You can use the simplified code to verify it. I ran it with 'gcc -O2 -S direct.c'

direct.c
--------
#define NEXT goto **ip++
#define guard(n) asm("#" #n)

__attribute__((cold)) void *emu (void **prog)
{
  static void  *labels[] = {&&next1,&&next2,&&next3,&&next4,&&next5,&&next6,&&next7,&&next8,&&next9,&&loop};
  void **ip;
  int    count;

  if (!prog) {
	  return labels;
  }  

  ip=prog;
  count = 10000000;

  
  NEXT;
 next1:
  guard(1);
  NEXT;
 next2:
  guard(2);
  NEXT;
 next3:
  guard(3);
  NEXT;
 next4:
  guard(4);
  NEXT;
 next5:
  guard(5);
  NEXT;
 next6:
  guard(6);
  NEXT;
 next7:
  guard(7);
  NEXT;
 next8:
  guard(8);
  NEXT;
 next9:
  guard(9);
  NEXT;
 loop:
  if (count>0) {
    count--;
    ip=prog;
    NEXT;
  }
  return 0;
}


int main() {
	void *prog[]   = {(void*)0,(void*)1,
	                  (void*)0,(void*)2,
	                  (void*)0,(void*)3,
	                  (void*)0,(void*)4,
	                  (void*)0,(void*)9};
	void **labels = emu(0);
	int i;
	for (i=0; i < sizeof(prog)/sizeof(prog[0]); i++) {
		prog[i] = labels[(int)prog[i]];
	}
	emu(prog);
	return 0;
}

I saw that the check causing the slowdown was removed in trunk, however I can't check that it was done in a proper way.


---


### compiler : `gcc`
### title : `Failure to optimise (a/b) and (a%b) into single __aeabi_idivmod call`
### open_at : `2010-04-11T20:39:10Z`
### last_modified_date : `2018-11-19T15:32:59Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=43721
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.4.3`
### severity : `enhancement`
### contents :
Consider the following code:

int divmod(int a, int b)
{
    int q = a / b;
    int r = a % b;
    return q + r;
}

For an ARM EABI target, this results in one __aeabi_idivmod() call and one
__aeabi_idiv() call even though the former already calculates the quotient.


---


### compiler : `gcc`
### title : `Poor instructions selection, scheduling and registers allocation for ARM NEON intrinsics`
### open_at : `2010-04-12T07:27:06Z`
### last_modified_date : `2021-09-27T07:21:09Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=43725
### status : `NEW`
### tags : `missed-optimization, ra`
### component : `target`
### version : `4.5.0`
### severity : `enhancement`
### contents :
gcc version 4.5.0-rc20100406

/**************/
#include <arm_neon.h>

void x(int32x4_t a, int32x4_t b, int32x4_t *p)
{
        #define X(n) p[n] = vaddq_s32(p[n], a); p[n] = vorrq_s32(p[n], b);
        X(0); X(1); X(2); X(3); X(4); X(5); X(6); X(7);
        X(8); X(9); X(10); X(11); X(12);
}
/**************/

# gcc -O2 -mcpu=cortex-a8 -mfpu=neon -mfloat-abi=hard -c test.c
# objdump -d test.o

00000000 <x>:
   0:   edd0eb2c        vldr    d30, [r0, #176] ; 0xb0
   4:   edd0fb2e        vldr    d31, [r0, #184] ; 0xb8
   8:   ecd02b04        vldmia  r0, {d18-d19}         
   c:   ed2d8b10        vpush   {d8-d15}              
  10:   ed904b30        vldr    d4, [r0, #192]  ; 0xc0
  14:   ed905b32        vldr    d5, [r0, #200]  ; 0xc8
  18:   e24dd020        sub     sp, sp, #32           
  1c:   f22ec8c0        vadd.i32        q6, q15, q0   
  20:   f26228c0        vadd.i32        q9, q9, q0    
  24:   edd04b08        vldr    d20, [r0, #32]        
  28:   edd05b0a        vldr    d21, [r0, #40]  ; 0x28
  2c:   edd0cb18        vldr    d28, [r0, #96]  ; 0x60
  30:   edd0db1a        vldr    d29, [r0, #104] ; 0x68
  34:   f264e840        vadd.i32        q15, q2, q0   
  38:   f26448c0        vadd.i32        q10, q10, q0  
  3c:   f26cc8c0        vadd.i32        q14, q14, q0  
  40:   edd00b04        vldr    d16, [r0, #16]        
  44:   edd01b06        vldr    d17, [r0, #24]        
  48:   edd0ab14        vldr    d26, [r0, #80]  ; 0x50
  4c:   edd0bb16        vldr    d27, [r0, #88]  ; 0x58
  50:   ec8dcb04        vstmia  sp, {d12-d13}         
  54:   f222c1d2        vorr    q6, q9, q1            
  58:   f26008c0        vadd.i32        q8, q8, q0    
  5c:   f26aa8c0        vadd.i32        q13, q13, q0  
  60:   edd06b0c        vldr    d22, [r0, #48]  ; 0x30
  64:   edd07b0e        vldr    d23, [r0, #56]  ; 0x38
  68:   edd08b10        vldr    d24, [r0, #64]  ; 0x40
  6c:   edd09b12        vldr    d25, [r0, #72]  ; 0x48
  70:   ed906b1c        vldr    d6, [r0, #112]  ; 0x70
  74:   ed907b1e        vldr    d7, [r0, #120]  ; 0x78
  78:   ed908b20        vldr    d8, [r0, #128]  ; 0x80
  7c:   ed909b22        vldr    d9, [r0, #136]  ; 0x88
  80:   ed90ab24        vldr    d10, [r0, #144] ; 0x90
  84:   ed90bb26        vldr    d11, [r0, #152] ; 0x98
  88:   ed90eb28        vldr    d14, [r0, #160] ; 0xa0
  8c:   ed90fb2a        vldr    d15, [r0, #168] ; 0xa8
  90:   edcdeb04        vstr    d30, [sp, #16]        
  94:   edcdfb06        vstr    d31, [sp, #24]        
  98:   ec80cb04        vstmia  r0, {d12-d13}         
  9c:   f224c1d2        vorr    q6, q10, q1           
  a0:   f26c41d2        vorr    q10, q14, q1          
  a4:   ecddcb04        vldmia  sp, {d28-d29}         
  a8:   f26021d2        vorr    q9, q8, q1            
  ac:   f26888c0        vadd.i32        q12, q12, q0  
  b0:   f26ae1d2        vorr    q15, q13, q1          
  b4:   f26668c0        vadd.i32        q11, q11, q0  
  b8:   f26ca1d2        vorr    q13, q14, q1          
  bc:   f2266840        vadd.i32        q3, q3, q0    
  c0:   f2288840        vadd.i32        q4, q4, q0    
  c4:   f22aa840        vadd.i32        q5, q5, q0    
  c8:   f22ee840        vadd.i32        q7, q7, q0    
  cc:   edddcb04        vldr    d28, [sp, #16]        
  d0:   eddddb06        vldr    d29, [sp, #24]        
  d4:   f22601d2        vorr    q0, q11, q1           
  d8:   f22841d2        vorr    q2, q12, q1           
  dc:   f2680152        vorr    q8, q4, q1            
  e0:   f26a6152        vorr    q11, q5, q1           
  e4:   f26e8152        vorr    q12, q7, q1           
  e8:   edc02b04        vstr    d18, [r0, #16]        
  ec:   edc03b06        vstr    d19, [r0, #24]        
  f0:   f2662152        vorr    q9, q3, q1            
  f4:   f22c21d2        vorr    q1, q14, q1           
  f8:   ed80cb08        vstr    d12, [r0, #32]        
  fc:   ed80db0a        vstr    d13, [r0, #40]  ; 0x28
 100:   ed800b0c        vstr    d0, [r0, #48]   ; 0x30
 104:   ed801b0e        vstr    d1, [r0, #56]   ; 0x38
 108:   ed804b10        vstr    d4, [r0, #64]   ; 0x40
 10c:   ed805b12        vstr    d5, [r0, #72]   ; 0x48
 110:   edc0eb14        vstr    d30, [r0, #80]  ; 0x50
 114:   edc0fb16        vstr    d31, [r0, #88]  ; 0x58
 118:   edc04b18        vstr    d20, [r0, #96]  ; 0x60
 11c:   edc05b1a        vstr    d21, [r0, #104] ; 0x68
 120:   edc02b1c        vstr    d18, [r0, #112] ; 0x70
 124:   edc03b1e        vstr    d19, [r0, #120] ; 0x78
 128:   edc00b20        vstr    d16, [r0, #128] ; 0x80
 12c:   edc01b22        vstr    d17, [r0, #136] ; 0x88
 130:   edc06b24        vstr    d22, [r0, #144] ; 0x90
 134:   edc07b26        vstr    d23, [r0, #152] ; 0x98
 138:   edc08b28        vstr    d24, [r0, #160] ; 0xa0
 13c:   edc09b2a        vstr    d25, [r0, #168] ; 0xa8
 140:   edc0ab2c        vstr    d26, [r0, #176] ; 0xb0
 144:   edc0bb2e        vstr    d27, [r0, #184] ; 0xb8
 148:   ed802b30        vstr    d2, [r0, #192]  ; 0xc0
 14c:   ed803b32        vstr    d3, [r0, #200]  ; 0xc8
 150:   e28dd020        add     sp, sp, #32
 154:   ecbd8b10        vpop    {d8-d15}
 158:   e12fff1e        bx      lr

This shows multiple performance problems:
1. The use of inherently slower VLDR/VSTR instructions instead of VLD1/VST1
2. Failure to make proper use of ARM Cortex-A8 NEON LS/ALU dual issue
3. Unnecessary spills to stack

This is a general issue with NEON intrinsics, causing serious performance problems for practically any nontrivial code. I guess this itself can be a meta-bug, with each individual performance issue tracked separately.


---


### compiler : `gcc`
### title : `[avr] g++ puts VTABLES in SRAM`
### open_at : `2010-04-13T08:15:31Z`
### last_modified_date : `2021-11-05T23:18:38Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=43745
### status : `RESOLVED`
### tags : `addr-space, missed-optimization`
### component : `c++`
### version : `4.7.0`
### severity : `enhancement`
### contents :
On AVR target g++ generates code which copies object&#8217;s VTABLES from FLASH to SRAM wasting the memory. Due to the Harvard architecture of AVR processors the solution is not trivial. This behavior can be observed in any c++ program which has object with virtual method, e.g:
Class test
{
	virtual void example();
};

The VTABLE of class test will be generated in FLASH and next copied to SRAM, any reference to virtual example() method will take the method address from SRAM.


---


### compiler : `gcc`
### title : `-Os creates larger binaries than before in some cases (-falign-... options enabled)`
### open_at : `2010-04-22T23:48:23Z`
### last_modified_date : `2022-01-05T10:48:30Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=43861
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.4.3`
### severity : `normal`
### contents :
Hi,

I just noticed that some of my libraries are greater when compiled with gcc 4.4.3 instead of gcc 4.3.2. Diffing the output of "gcc --help=optimizers -Q -Os" shows this in 4.3.2:

  -falign-jumps                        [disabled]
  -falign-labels                       [disabled]
  -falign-loops                        [enabled]

and this for 4.4.3:

  -falign-functions                     [enabled]
  -falign-jumps                         [enabled]
  -falign-labels                        [enabled]
  -falign-loops                         [disabled]

when explicitely disabling the alignment options then the code size shrinks. For libxml2 in my case from 704256 to 675584 bytes.

The manual says:

  -Os disables the following optimization flags: -falign-functions
           -falign-jumps  -falign-loops -falign-labels  -freorder-blocks
           -freorder-blocks-and-partition -fprefetch-loop-arrays
           -ftree-vect-loop-version

which is not true (even not for 4.3.2 since loop alignment was enabled). Some other opts like -freorder-blocks is enabled as well.

So is this actually a bug or is the documentation outdated or even both?


---


### compiler : `gcc`
### title : `missed optimization of constant __int128_t modulus`
### open_at : `2010-04-25T05:06:38Z`
### last_modified_date : `2021-12-29T10:06:52Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=43883
### status : `NEW`
### tags : `missed-optimization, ra`
### component : `middle-end`
### version : `4.5.0`
### severity : `enhancement`
### contents :
The following function gets optimized at -O3 to:

long long tmod2(long long x)
{
	return x % 2;
}


mov    %rdi,%rdx                                                   
shr    $0x3f,%rdx                                                  
lea    (%rdi,%rdx,1),%rax                                          
and    $0x1,%eax                                                   
sub    %rdx,%rax                                                   
retq

This is very good code.  Unfortunately, the 128 bit version doesn't get optimized nearly so well.

__int128_t tmod2(__int128_t x)
{
	return x % 2;
}

mov    %rsi,%rdx
mov    %rdi,%r8
xor    %ecx,%ecx
shr    $0x3f,%rdx
push   %rbx
add    %rdx,%r8
xor    %edi,%edi
mov    %r8,%rsi
mov    %rdi,%r9
and    $0x1,%esi
mov    %rsi,%r8
sub    %rdx,%r8
sbb    %rcx,%r9
mov    %r8,%rax
mov    %r9,%rdx
pop    %rbx
retq

It looks like this simple variation of the 64bit algorithm will work for the 128 bit version:

mov    %rsi,%rdx    <--- Just changed rdi into rsi
shr    $0x3f,%rdx   <--- nicely already calculates high bytes in rdx
lea    (%rdi,%rdx,1),%rax
and    $0x1,%eax
sub    %rdx,%rax
retq


---


### compiler : `gcc`
### title : `[4.4/4.5/4.6 Regression] Performance degradation for simple fibonacci numbers calculation`
### open_at : `2010-04-25T07:18:25Z`
### last_modified_date : `2021-12-26T12:35:34Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=43884
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.4.3`
### severity : `normal`
### contents :
I ran this simple example with the argument 45 through various versions of gcc (option -O3):

#include <stdlib.h>
#include <stdio.h>

int fib(int AnArg) {
 if (AnArg <= 2) return (1);
 return (fib(AnArg-1)+fib(AnArg-2));
}

int main(int argc, char* argv[]) {
 int n = atoi(argv[1]);
 printf("fib(%i)=%i\n", n, fib(n));
}

Here are the average runtimes I got:
version    time
4.3.1      3.930s
4.3.2      3.500s
4.3.3      3.470s
4.4.1      3.930s
4.4.3      3.940s
4.5.0      3.860s

I ran ~10 samples so values are approximate, but it's quite obvious that 4.5.0 has very significant degradation compared to 4.3.3.

Is there a performance suite for gcc that is ran for each release, are results available online?

This case is pretty simple, basic. I would expect gcc to produce quite optimal code for it.


---


### compiler : `gcc`
### title : `PowerPC suboptimal "add with carry" optimization`
### open_at : `2010-04-26T13:33:22Z`
### last_modified_date : `2023-08-29T17:43:33Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=43892
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `target`
### version : `4.3.4`
### severity : `enhancement`
### contents :

PowerPC suboptimal "add with carry" optimization

Environment:
System: Linux gentoo-jocke 2.6.31-gentoo-r6 #1 SMP PREEMPT Sun Feb 28 22:54:53 CET 2010 i686 Intel(R) Core(TM)2 Duo CPU E8500 @ 3.16GHz GenuineIntel GNU/Linux


	
host: i686-pc-linux-gnu
build: i686-pc-linux-gnu
target: i686-pc-linux-gnu
configured with: /var/tmp/portage/sys-devel/gcc-4.3.4/work/gcc-4.3.4/configure --prefix=/usr --bindir=/usr/i686-pc-linux-gnu/gcc-bin/4.3.4 --includedir=/usr/lib/gcc/i686-pc-linux-gnu/4.3.4/include --datadir=/usr/share/gcc-data/i686-pc-linux-gnu/4.3.4 --mandir=/usr/share/gcc-data/i686-pc-linux-gnu/4.3.4/man --infodir=/usr/share/gcc-data/i686-pc-linux-gnu/4.3.4/info --with-gxx-include-dir=/usr/lib/gcc/i686-pc-linux-gnu/4.3.4/include/g++-v4 --host=i686-pc-linux-gnu --build=i686-pc-linux-gnu --disable-altivec --disable-fixed-point --enable-nls --without-included-gettext --with-system-zlib --disable-checking --disable-werror --enable-secureplt --disable-multilib --enable-libmudflap --disable-libssp --enable-libgomp --disable-libgcj --with-arch=i686 --enable-languages=c,c++,treelang,fortran --enable-shared --enable-threads=posix --enable-__cxa_atexit --enable-clocale=gnu --with-bugurl=http://bugs.gentoo.org/ --with-pkgversion='Gentoo 4.3.4 p1.0, pie-10.1.5'

How-To-Repeat:
Noticed that gcc 4.3.4 doesn't optimize "add with carry" properly:

static u32
add32carry(u32 sum, u32 x)
{
  u32 z = sum + x;
  if (sum + x < x)
      z++;
  return z;
}
Becomes:
add32carry:
	add 3,3,4
	subfc 0,4,3
	subfe 0,0,0
	subfc 0,0,3
	mr 3,0
Instead of:
	addc 3,3,4
	addze 3,3

This slows down the the Internet checksum sigificantly

Also, doing this in a loop can be further optimized:

for(;len; --len)
   sum = add32carry(sum, *++buf);


	addic 3, 3, 0 /* clear carry */
.L31:
	lwzu 0,4(9)
	adde 3, 3, 0 /* add with carry */
	bdnz .L31

	addze 3, 3 /* add in final carry */


---


### compiler : `gcc`
### title : `Redundant conditionals [4.5 only] - unnecessary mov of a constant after unrolling.`
### open_at : `2010-04-27T12:05:54Z`
### last_modified_date : `2021-07-26T08:15:56Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=43908
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.5.0`
### severity : `enhancement`
### contents :
The following code:

    struct A { int r0; int r1; };
    void sigh(struct A *a, const int d)
    {
        int i;
        for (i = 0; i < 8; ++i) {
            if (d & (1U << i))
                a->r0 = 1;
            else
                a->r1 = 1;
        }
    }

compiled using

    arm-none-eabi-gcc -mcpu=arm7tdmi -marm -O3 -S -o- tmp2.c

produces very poor code:

    sigh:
	@ Function supports interworking.
	@ args = 0, pretend = 0, frame = 0
	@ frame_needed = 0, uses_anonymous_args = 0
	@ link register save eliminated.
	tst	r1, #1
	moveq	r3, #1
	movne	r3, #1
	streq	r3, [r0, #4]
	strne	r3, [r0, #0]
	tst	r1, #2
	moveq	r3, #1
	movne	r3, #1
	streq	r3, [r0, #4]
	strne	r3, [r0, #0]
	tst	r1, #4
	moveq	r3, #1
	movne	r3, #1
	streq	r3, [r0, #4]
	strne	r3, [r0, #0]
	tst	r1, #8
	moveq	r3, #1
	movne	r3, #1
	streq	r3, [r0, #4]
	strne	r3, [r0, #0]
	tst	r1, #16
	moveq	r3, #1
	movne	r3, #1
	streq	r3, [r0, #4]
	strne	r3, [r0, #0]
	tst	r1, #32
	moveq	r3, #1
	movne	r3, #1
	streq	r3, [r0, #4]
	strne	r3, [r0, #0]
	tst	r1, #64
	moveq	r3, #1
	movne	r3, #1
	streq	r3, [r0, #4]
	strne	r3, [r0, #0]
	tst	r1, #128
	movne	r3, #1
	moveq	r3, #1
	strne	r3, [r0, #0]
	streq	r3, [r0, #4]
	bx	lr

Note the silly occurrences of:

        moveq   r1, #1
        movne   r1, #1

More importantly, there is no need to load the constant 1 into r3 in every iteration.  It should be loaded only once before the (unrolled) loop.


---


### compiler : `gcc`
### title : `redundant predicated checks not removed by VRP or jump-threading`
### open_at : `2010-05-03T06:17:54Z`
### last_modified_date : `2021-07-26T08:22:17Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=43966
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.5.0`
### severity : `enhancement`
### contents :
On attached test case GCC keeps the index range checks in
Vector::getValue although they're always true due to loop conditions

 # GNU C++ (GCC) version 4.5.0 (mingw32)
 # options passed:  -fpreprocessed yy5.ii -march=atom -mtune=atom -O2 -Wall


---


### compiler : `gcc`
### title : `missed optimization of  min/max_expr or strict overflow warnings for intended code.`
### open_at : `2010-05-06T09:35:59Z`
### last_modified_date : `2021-11-25T06:54:53Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=44011
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.5.0`
### severity : `enhancement`
### contents :
hi,

please consider following code snippet from large CairoMM base application.
it creates a planar region with top left and bottom right points from two
points passed to RegionT constructor.

$ cat 0.cpp

        static inline int min( int a, int b ) {
                if ( a < b ) return a;
                return b;
        }
        static inline int max( int a, int b ) {
                if ( a > b ) return a;
                return b;
        }
        struct PointT {
                explicit PointT () { x = 0; y = 0; }
                explicit PointT ( int xVal, int yVal ) : x( xVal ), y( yVal ) {}
                int x, y;
        };
        struct RegionT {
                explicit RegionT ( PointT const& p1, PointT const& p2 ) {
                        // calculate top_left and bottom_right coordinates.
                        // (0,0) ---> X
                        //  |
                        //  |
                        //  \/
                        //  Y
#ifdef WARN_AND_OPTIMIZE
                        if ( p1.x < p2.x ) {
                                tl.x = p1.x;
                                br.x = p2.x;
                        } else {
                                tl.x = p2.x;
                                br.x = p1.x;
                        }
                        if ( p1.y < p2.y ) {
                                tl.y = p1.y;
                                br.y = p2.y;
                        } else {
                                tl.y = p2.y;
                                br.y = p1.y;
                        }
#else
                        tl.x = min( p1.x, p2.x );
                        tl.y = min( p1.y, p2.y );
                        br.x = max( p1.x, p2.x );
                        br.y = max( p1.y, p2.y );
#endif
                }
                PointT tl, br;
        };

the application contains lots of places where a region is created
from one base point and constant offsets, e.g.:

        RegionT foo ( PointT const& p ) {
                RegionT r ( p, PointT ( p.x - 2, p.y + 2 ) );
                return r;
        }

for such constructions and -DWARN_AND_OPTIMIZE gcc optimizes RegionT
coordinates calculation at compile time and produces warnings about
strict overflow assumptions.

$ g++ 0.cpp -c -Wall -O2 -fdump-tree-optimized --save-temps -DWARN_AND_OPTIMIZE
0.cpp: In function 'RegionT foo(const PointT&)':
0.cpp:23:4: warning: assuming signed overflow does not occur when assuming that (X - c) > X is always false
0.cpp:30:4: warning: assuming signed overflow does not occur when assuming that (X + c) >= X is always true

RegionT foo(const PointT&) (const struct PointT & p)
{
  int r$tl$y;
  int r$tl$x;
  struct RegionT D.2181;
<bb 2>:
  r$tl$y_2 = p_1(D)->y;
  r$tl$y_3 = r$tl$y_2 + 2;
  r$tl$x_4 = p_1(D)->x;
  r$tl$x_5 = r$tl$x_4 + -2;
  D.2181.tl.x = r$tl$x_5;
  D.2181.tl.y = r$tl$y_2;
  D.2181.br.x = r$tl$x_4;
  D.2181.br.y = r$tl$y_3;
  return D.2181;
}

i known signed integer overflow rules but such construction is human
readable and intended, so i would like to still have '-Wall -Werror'
in action for all code and avoid disabling strict-overflow warings for
*global* scope (originally RegionT is implemented as a template in header).

for now, i've hacked in ugly way the if-logic in RegionT constructor
to std::min/max variant. it doesn't warn but produces unoptimal code
with CMOVs for compile time constants.

RegionT foo(const PointT&) (const struct PointT & p)
{
  int a;
  int a;
  struct RegionT D.2182;
  const int D.2178;

<bb 2>:
  D.2178_2 = p_1(D)->y;
  a_3 = D.2178_2 + 2;
  a_4 = p_1(D)->x;
  a_7 = a_4 + -2;
  a_41 = MIN_EXPR <a_7, a_4>;
  a_45 = MIN_EXPR <a_3, D.2178_2>;
  a_42 = MAX_EXPR <a_7, a_4>;
  a_46 = MAX_EXPR <a_3, D.2178_2>;
  D.2182.tl.x = a_41;
  D.2182.tl.y = a_45;
  D.2182.br.x = a_42;
  D.2182.br.y = a_46;
  return D.2182;
}

_Z3fooRK6PointT:
        movl    (%rdi), %edx
        movl    4(%rdi), %eax
        leal    -2(%rdx), %esi
        leal    2(%rax), %ecx
        movl    %edx, %edi
        cmpl    %edx, %esi
        cmovle  %esi, %edi
        cmpl    %eax, %ecx
        movl    %edi, -24(%rsp)
        movl    %eax, %edi
        cmovle  %ecx, %edi
        cmpl    %edx, %esi
        cmovge  %esi, %edx
        cmpl    %eax, %ecx
        movl    %edi, -20(%rsp)
        cmovge  %ecx, %eax
        movl    %edx, -16(%rsp)
        movl    %eax, -12(%rsp)
        movq    -24(%rsp), %rax
        movq    -16(%rsp), %rdx
        ret


how can i disable these warnings for intended part of source code
and get nicely optimized binaries? the gcc rejects my attempts to
'#pragma GCC diagnostic ignore' inside RegionT contstructor with
error: #pragma GCC diagnostic not allowed inside functions :/

thanks in advance for creative hints.


---


### compiler : `gcc`
### title : `Multiple load 0 to register`
### open_at : `2010-05-07T13:19:01Z`
### last_modified_date : `2023-05-16T23:41:59Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=44025
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.6.0`
### severity : `enhancement`
### contents :
Compile the attached source code with options -Os -march=armv7-a -mthumb, gcc generates:

bar4:
        push    {r3, r4, r5, lr}
        ldr     r2, [r0, #520]
        mov     r4, r0
        mov     r3, r0
        mov     r1, r0
        movs    r0, #0        // A
        b       .L2
.L4:
        ldrb    r5, [r3], #1    @ zero_extendqisi2
        cmp     r5, #10
        itt     eq
        moveq   r1, r3
        strbeq  r0, [r3, #-1]
        subs    r2, r2, #1
.L2:
        cmp     r2, #0
        bgt     .L4
        cmp     r1, r4
        bne     .L8
        movs    r3, #0         //B
        strb    r3, [r1, #512] //C
        b       .L1
.L8:
        ldr     r3, [r4, #520]
        adds    r3, r4, r3
        cmp     r1, r3
        bcc     .L7
        movs    r3, #0         //D
        str     r3, [r4, #520] //E
        b       .L1
.L7:
        subs    r5, r1, r4
        mov     r0, r4
        mov     r2, r5
        bl      memmove
        str     r5, [r4, #520]
.L1:
        pop     {r3, r4, r5, pc}

Instructions B load constant 0 into register r3, and instruction C store 0 into memory. Actually instruction A has already loaded 0 into register r0, and at instruction C it is still available, so we can use r0 directly in instruction C and remove B. Register r2 also contains 0 at instruction C, but it is more difficult to detect. R0 can also be used at instruction E and remove D.

When compile with -O2 the result is similar.

Should this be handled by any cse pass and rematerialize it if there is high register pressure?


---


### compiler : `gcc`
### title : `x86 constants could be unduplicated for -Os`
### open_at : `2010-05-11T08:14:07Z`
### last_modified_date : `2023-07-24T21:54:35Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=44073
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.6.0`
### severity : `enhancement`
### contents :
void f1(int *a, int *b, int *c)
{
    int d = 0xE0E0E0E0;
    
    *a = *b = *c = d;
}

produces
_f1:
LFB0:
	movl	$-522133280, (%rdx)
	movl	$-522133280, (%rsi)
	movl	$-522133280, (%rdi)
	ret

on x86-64 at -Os. It would save instruction space and probably not be any slower to actually assign d to a register, but this is only done for 64-bit constants.


---


### compiler : `gcc`
### title : `[4.3/4.4/4.5/4.6 Regression] G++ emits unnecessary EH code`
### open_at : `2010-05-13T20:54:57Z`
### last_modified_date : `2021-12-17T11:19:54Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=44127
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `c++`
### version : `4.6.0`
### severity : `normal`
### contents :
The following code calls terminate() at runtime because copying the exception object into the catch parameter throws an exception:

struct A
{
  A() { }
  A (const A&) { throw 1; }
};

int main()
{
  try
    {
      throw A();
    }
  catch (A) { }
}

In G++ 3.4 this was handled by just leaving the copy constructor call out of the LSDA action table, so the personality function knew to call terminate.  As of the tree-ssa merge, this changed so that we started emitting code to check the exception against a random filter and then call terminate from within the function.  This is a significant code size regression: a 25% jump in text size from 3.4 to 4.0.

4.0 and up also unnecessarily think that __cxa_end_catch might throw; since A has a trivial destructor, it can't throw in this case.


---


### compiler : `gcc`
### title : `va_list usage missed optimization.`
### open_at : `2010-05-24T21:15:58Z`
### last_modified_date : `2021-03-04T21:01:56Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=44262
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.5.0`
### severity : `enhancement`
### contents :
This function generates the following asm under -O3 in version 4.5

#include <stdarg.h>
void va_overload2(int p1, int p2);
void va_overload3(int p1, int p2, int p3);

void va_overload(int p1, int p2, ...)
{
	if (p2 == 7)
	{
		va_list v;
		va_start(v, p2);
		
		int p3 = va_arg(v, int);
		va_end(v);
		va_overload3(p1, p2, p3);
		
		return;
	}

	va_overload2(p1, p2);
}

Dump of assembler code for function va_overload:
   0x0000000000400520 <+0>:     sub    $0x58,%rsp
   0x0000000000400524 <+4>:     cmp    $0x7,%esi
   0x0000000000400527 <+7>:     mov    %rdx,0x30(%rsp)
   0x000000000040052c <+12>:    je     0x400540 <va_overload+32>
   0x000000000040052e <+14>:    callq  0x4004f0 <va_overload2>
   0x0000000000400533 <+19>:    add    $0x58,%rsp
   0x0000000000400537 <+23>:    retq   
   0x0000000000400538 <+24>:    nopl   0x0(%rax,%rax,1)
   0x0000000000400540 <+32>:    lea    0x60(%rsp),%rax
   0x0000000000400545 <+37>:    mov    0x30(%rsp),%edx
   0x0000000000400549 <+41>:    movl   $0x18,(%rsp)
   0x0000000000400550 <+48>:    mov    %rax,0x8(%rsp)
   0x0000000000400555 <+53>:    lea    0x20(%rsp),%rax
   0x000000000040055a <+58>:    mov    %rax,0x10(%rsp)
   0x000000000040055f <+63>:    callq  0x400500 <va_overload3>
   0x0000000000400564 <+68>:    add    $0x58,%rsp
   0x0000000000400568 <+72>:    retq

This could be replaced with the much more compact:
	cmp		$0x7, %esi
	je		1f
	jmp		va_overload2
1:	jmp		va_overload3
since the third parameter is passed in a register, and will still be there after the comparison.  (Actually, if it were passed on the stack it still wouldn't matter, because we can tail-call here.)


---


### compiler : `gcc`
### title : `Union cast leads to wrong code generation. (Strict aliasing not warned about?)`
### open_at : `2010-05-25T18:01:57Z`
### last_modified_date : `2021-07-25T01:53:29Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=44275
### status : `RESOLVED`
### tags : `missed-optimization, wrong-code`
### component : `tree-optimization`
### version : `4.5.0`
### severity : `normal`
### contents :
struct s1
{
	int a;
	int b;
	
	double c;
};

struct s2
{
	long long a;
	long long b;
};

union us
{
	struct s1 us1;
	struct s2 us2;
};

void foo1(struct s1 s)
{
	printf("Got %d %d %f\n", s.a, s.b, s.c);
}

void __attribute__((noinline, used, noclone)) foo(void)
{
	struct s1 s = {1, 2, 3.0};

	asm("");
	
	foo1(s);
	
	foo1(((union us *)&s)->us1);
}

Neither gcc 4.4 or 4.5 warn about the union cast, however 4.4 will mention a strict-aliasing problem if foo1() is forced not to be inlined.  gcc 4.5 outputs incorrect results.  4.4 outputs the correct 1,2,3 unless foo1() is forced to be not inlined, in which case it also has incorrect output.

My understanding is that casting to the union type is okay because union us contains struct s1 as a member.  We then access the union member that corresponds to the original type. (No undefined behaviour.)  So it looks like the lack of strict aliasing warning in 4.5 is correct.  However, the wrong code generation that results is obviously then problematic.


---


### compiler : `gcc`
### title : `Use ubfx to extract unsigned bit fields at the low end`
### open_at : `2010-05-26T02:41:36Z`
### last_modified_date : `2021-07-26T08:48:00Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=44278
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.6.0`
### severity : `enhancement`
### contents :
Compile the following code with options -march=armv7-a -mthumb -O2

unsigned int foo6(unsigned u)
{
  return (u >> 0) & 0x1ff;
}

GCC generates:

        lsls    r0, r0, #23
        lsrs    r0, r0, #23
        bx      lr

The two shifts can be merged into 
        UBFX     r1,r0,#0,#9

If I change the source code into
  return (u >> 1) & 0x1ff;
Then gcc can generate ubfx instruction. So this case only occurs at the low end of a register.

The same problem exists with option -Os and arm instructions.


---


### compiler : `gcc`
### title : `x86-64 unnecessary parameter extension`
### open_at : `2010-06-14T07:22:20Z`
### last_modified_date : `2019-03-04T11:12:34Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=44532
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.6.0`
### severity : `enhancement`
### contents :
Source:
int f1(short a, int b)
{
    return a * b;
}

int f2(unsigned short a, int b)
{
    return a * b;
}

> gcc -O3 -fomit-frame-pointer -S paramext.c

_f1:
LFB0:
	movl	%esi, %eax
	movswl	%di, %edi <-
	imull	%edi, %eax
	ret
...
_f2:
LFB1:
	movl	%esi, %eax
	movzwl	%di, %edi <-
	imull	%edi, %eax
	ret

AFAIK integer parameters should already be extended to int, so those instructions are redundant. llvm doesn't generate them.


---


### compiler : `gcc`
### title : `Inefficient code to return a large struct`
### open_at : `2010-06-25T22:46:36Z`
### last_modified_date : `2021-09-23T01:22:44Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=44675
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.6.0`
### severity : `enhancement`
### contents :
Compile the following code with options -march=armv7-a -mthumb -Os

typedef struct {
  int buf[7];
} A;

A foo();
void hahaha(A* p)
{
  *p = foo();
}

GCC generates:

hahaha:
        push    {r4, r5, lr}
        sub     sp, sp, #36
        mov     r5, sp
        mov     r4, r0
        mov     r0, sp
        bl      foo
        ldmia   r5!, {r0, r1, r2, r3}
        stmia   r4!, {r0, r1, r2, r3}
        ldmia   r5, {r0, r1, r2}
        stmia   r4, {r0, r1, r2}
        add     sp, sp, #36
        pop     {r4, r5, pc}

GCC first allocates temporary memory on the stack and passes its address into function foo, function foo will return the new struct in this memory area. After function return, gcc copies the contents of temporary memory into another area pointed to by pointer p. Actually we can simply pass the pointer p into function foo, then we get

hahaha:
        /* pointer p is already in register r0 */
        /* we can also apply tail function call optimization here. */
        b      foo

Any combination of arm/thumb Os/O2 generates similar results. The inefficient code is generated at expand pass. This may also affect other targets with similar ABI that needs temporary memory and an extra parameter to return large object.

Following is another similar case.

typedef struct {
  int buf[7];
} A;

A foo();
void bar(A*);
void hahaha(A* p)
{
  A t;
  t = foo();
  bar(&t);
}


---


### compiler : `gcc`
### title : `PRE doesn't remove equivalent computations of induction variables`
### open_at : `2010-06-29T11:00:00Z`
### last_modified_date : `2021-07-26T08:37:12Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=44711
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.6.0`
### severity : `normal`
### contents :
For the following loop 

  for (i = 0; i < N; i++)
    if (arr[i] < limit)
      {
        pos = i + 1;
        limit = arr[i];
      }

PRE fails to eliminate redundant i_24 + 1 computation. 

Here is Richard's analysis from http://gcc.gnu.org/ml/gcc-patches/2010-06/msg02982.html:

So the reason is our heuristic in PRE to not introduce new IVs:

Found partial redundancy for expression {plus_expr,i_24,1} (0005)
Skipping insertion of phi for partial redundancy: Looks like an
induction variable
Inserted pretmp.4_2 = i_13 + 1;
 in predecessor 8
Found partial redundancy for expression {plus_expr,i_24,1} (0005)
Inserted pretmp.4_22 = i_24 + 1;
 in predecessor 7
Created phi prephitmp.5_21 = PHI <pretmp.4_22(7), pos_11(4)>
 in block 5
Found partial redundancy for expression {plus_expr,i_24,1} (0005)
Skipping insertion of phi for partial redundancy: Looks like an
induction variable
Replaced i_24 + 1 with prephitmp.5_21 in i_13 = i_24 + 1;
Removing unnecessary insertion:pretmp.4_2 = i_13 + 1;

we do not want to insert into block 3, so we are left with

<bb 3>:
  # pos_23 = PHI <pos_1(8), 1(2)>
  # i_24 = PHI <i_13(8), 0(2)>
  # limit_25 = PHI <limit_4(8), 1.28e+2(2)>
  limit_9 = arr[i_24];
  D.3841_10 = limit_9 < limit_25;
  if (D.3841_10 != 0)
    goto <bb 4>;
  else
    goto <bb 7>;

<bb 7>:
  pretmp.4_22 = i_24 + 1;
  goto <bb 5>;

<bb 4>:
  pos_11 = i_24 + 1;

<bb 5>:
  # pos_1 = PHI <pos_23(7), pos_11(4)>
  # limit_4 = PHI <limit_25(7), limit_9(4)>
  # prephitmp.5_21 = PHI <pretmp.4_22(7), pos_11(4)>
  i_13 = prephitmp.5_21;

where there is no full redundancy for i_24 + 1 now (that is,
we did some useless half-way PRE because of that IV
heuristic ...).


---


### compiler : `gcc`
### title : `pre- and post-loops should not be unrolled.`
### open_at : `2010-07-02T23:54:17Z`
### last_modified_date : `2023-04-19T11:55:09Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=44794
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.6.0`
### severity : `enhancement`
### contents :
void foo(int *a, int *b, int n)
{
  int i;
  for(i = 0; i < n; i++)
     a[i] = a[i] + b[i];
}

For this simple loop, the vectorizer does its job and peels the last few 
iterations as post-loop that is not vectorized. But the RTL loop unroller
does not know that it just has a few (at most 3 in this case) iterations,
and will unroll the post-loop.

What is worse, if you compile it with:
  gcc -O3 -fprefetch-loop-arrays -funroll-loops

You may find the prefetch pass will also unroll the post-loop, and generate
a new post-loop (post-post-loop) for this post-loop. Again, the RTL loop
unroller could not recognize this post-post-loop, and will unroll it.
(the RTL loop unroller will generate yet another post loop (post-post-post-loop) for the post-post-loop :-))

 This will cause compilation time and code size increase dramastically without
any performance benefit.


---


### compiler : `gcc`
### title : `Combine separate shift and add instructions into a single one`
### open_at : `2010-07-08T23:18:14Z`
### last_modified_date : `2021-09-26T22:43:09Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=44883
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.6.0`
### severity : `normal`
### contents :
Compile the following code with options -march=armv7-a -mthumb -Os

struct S1
{
    int f1;
    int f2;
    int f3[6];
};

struct S2
{
    struct S1* pS1;
};

void aaaaaaaaa(struct S2* pS2, int count)
{
        int idx;
        for (idx = 0; idx < count; idx++) {
            struct S1* pS1 = &pS2->pS1[idx];
            foo(pS1->f1);
            pS1->f2 = 6;
        }
}

GCC generates:

aaaaaaaaa:
        push    {r4, r5, r6, r7, r8, lr}
        mov     r4, r0
        mov     r7, r1
        movs    r5, #0
        movs    r6, #6
        b       .L2
.L3:
        ldr     r2, [r4, #0]
        lsls    r3, r5, #5       // A
        adds    r5, r5, #1
        add     r8, r2, r3       // B
        ldr     r0, [r2, r3]     // C
        bl      foo
        str     r6, [r8, #4]
.L2:
        cmp     r5, r7
        blt     .L3
        pop     {r4, r5, r6, r7, r8, pc}

Instructions AB can be merged into one instruction and C should be modified accordingly

      add r8, r2, r5 << 5
      ldr     r0, [r8]

The related rtl insns before fwprop2 pass is:

(insn 13 12 14 3 src/to.c:13 (set (reg:SI 143)
        (ashift:SI (reg/v:SI 135 [ idx ])
            (const_int 5 [0x5]))) 119 {*arm_shiftsi3} (nil))

(insn 15 14 16 3 src/to.c:17 (set (reg/v/f:SI 137 [ pS1 ])
        (plus:SI (reg/f:SI 144 [ pS2_4(D)->pS1 ])
            (reg:SI 143))) 4 {*arm_addsi3} (expr_list:REG_DEAD (reg/f:SI 144 [ pS2_4(D)->pS1 ])
        (expr_list:REG_DEAD (reg:SI 143)
            (nil))))

(insn 16 15 17 3 src/to.c:18 (set (reg:SI 0 r0)
        (mem/s:SI (reg/v/f:SI 137 [ pS1 ]) [5 pS1_8->f1+0 S4 A32])) 661 {*thumb2_movsi_insn} (nil))

It looks can be handled by combine pass. But the fwprop2 pass propagates the following expression into memory load

    (plus:SI (reg/f:SI 144 [ pS2_4(D)->pS1 ])
            (reg:SI 143))

So now we get:

(insn 13 12 14 3 src/to.c:13 (set (reg:SI 143)
        (ashift:SI (reg/v:SI 135 [ idx ])
            (const_int 5 [0x5]))) 119 {*arm_shiftsi3} (nil))

(insn 15 14 16 3 src/to.c:17 (set (reg/v/f:SI 137 [ pS1 ])
        (plus:SI (reg/f:SI 144 [ pS2_4(D)->pS1 ])
            (reg:SI 143))) 4 {*arm_addsi3} (expr_list:REG_DEAD (reg/f:SI 144 [ pS2_4(D)->pS1 ])
        (expr_list:REG_DEAD (reg:SI 143)
            (nil))))

(insn 16 15 17 3 src/to.c:18 (set (reg:SI 0 r0)
        (mem/s:SI (plus:SI (reg/f:SI 144 [ pS2_4(D)->pS1 ])
                (reg:SI 143)) [5 pS1_8->f1+0 S4 A32])) 661 {*thumb2_movsi_insn} (nil))

Now r143 is used in both insn 15 and insn 16. Combine insn 13 and insn 15 can't bring any benefit.

So in function fwprop_addr before deciding propagate an expression should we also check if it is the only use of the corresponding def?


---


### compiler : `gcc`
### title : `reductions with short variables do not get vectorized`
### open_at : `2010-07-18T05:18:14Z`
### last_modified_date : `2021-02-23T10:14:30Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=44976
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.6.0`
### severity : `normal`
### contents :
short variables do not get vectorized the same as unsigned short variables


---


### compiler : `gcc`
### title : `struct passed as argument in memory compiles to dead stores`
### open_at : `2010-07-21T21:05:57Z`
### last_modified_date : `2021-08-14T21:31:50Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=45026
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.6.0`
### severity : `enhancement`
### contents :
Consider this test case:
typedef struct teststruct
{
  double d;
  char f1;
  int arr[15];
} teststruct;

void
copystruct5 (teststruct param)
{
  return;
}

The mighty copystruct5 function does absolutely nothing, so I expect this to be compiled to absolutely nothing. But not so with r162374 at -O2:

        .file   "t.c"
        .pred.safe_across_calls p1-p5,p16-p63
        .text
        .align 16
        .align 64
        .global copystruct5#
        .type   copystruct5#, @function
        .proc copystruct5#
copystruct5:
        .prologue
        .spill 48
        .mmi
        .fframe 48
        adds r12 = -48, r12
[.L2:]  
        .body
        ;;
        mov r14 = r12
        adds r15 = 16, r12
        ;;
        .mmi
        st8 [r14] = r32, 8
        st8 [r15] = r34
        nop 0
        ;;
        .mmi
        st8 [r14] = r33
        nop 0
        adds r14 = 24, r12
        ;;
        .mmi
        st8 [r14] = r35
        nop 0
        adds r14 = 32, r12
        ;;
        .mmi
        st8 [r14] = r36
        nop 0
        adds r14 = 40, r12
        ;;
        .mmi
        st8 [r14] = r37
        nop 0
        adds r14 = 48, r12
        ;;
        .mmi
        st8 [r14] = r38
        nop 0
        adds r14 = 56, r12
        ;;
        .mib
        st8 [r14] = r39
        .restore sp
        adds r12 = 48, r12
        br.ret.sptk.many b0
        .endp copystruct5#
        .ident  "GCC: (GNU) 4.6.0 20100721 (experimental) [trunk revision 162374]"

What's that?!


---


### compiler : `gcc`
### title : `Missed optimization in ifcvt/crossjump`
### open_at : `2010-07-22T18:52:03Z`
### last_modified_date : `2021-08-19T05:21:23Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=45032
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.6.0`
### severity : `enhancement`
### contents :
int f(int x, int y);
int g(int x, int z)
{
  int r;
  if (z == 0)
    r = f(x, 1);
  else
    r = f(x, 0);
  return r + 1;
}

could be optimized to 

  r = f(x, (z == 0 ? 1 : 0));

which would reduce the size of the generated code, and for
most targets allow further simplifications on the COND_EXPR
leading to branchless assembly.


---


### compiler : `gcc`
### title : `GCC doesn't create functions with multiple entry points.`
### open_at : `2010-07-24T18:13:27Z`
### last_modified_date : `2021-08-28T03:49:16Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=45058
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.5.0`
### severity : `enhancement`
### contents :
A possible optimization in some cases is to construct a function with multiple entry points.  This can save in both size and speed in certain cases.

#include <stdio.h>

/* Example function that does something complex enough not to be optimized away */
static foo(int x)
{
	int i;
	int j = x;
	for (i = 0; i < 1024; i++)
	{
		j += printf("%d%d%d\n", i);
	}
	
	return j;
}

/* Since foo is static and whose address is never taken, foo1 can have the same address as foo. */
int foo1(int x)
{
	return foo(x);
}

/* This function could point to an "add $1, %rdi" instruction immediately before foo. (Giving foo two entry points.) */ 
int foo2(int x)
{
	return foo(x + 1);
}

At the moment, GCC will at -O3 construct two cloned versions of foo for foo1 and foo2.  At -Os, it will jump to foo in foo1 and foo2.  With multiple entry points, the code can be as fast as generated for -O3 but be half the size, slightly smaller than the current -Os.


---


### compiler : `gcc`
### title : `x86_64 passing structure by value to a non-inlined function causes register-resident structures to flush to stack`
### open_at : `2010-07-26T21:15:46Z`
### last_modified_date : `2021-08-05T21:58:12Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=45090
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.5.0`
### severity : `enhancement`
### contents :
I am running 4.5.0, built locally from a gcc.gnu.org distribution, on Ubuntu 10.04. 

When switching from -m32 to -m64 a dispatch loop in my code gets noticeably slower (20% slower in 4.3.4 and 4.4.3, 10% slower in 4.5.0).

Investigation of the generated assembly shows that register-resident structures are being flushed to locations on the stack around a call through a function pointer. If I change the function call to take scalar arguments rather than a structure passed by value, then the stack writes go away and perforamance improves to be about 10% faster than the 32-bit code. 

The small testcase below includes three examples. One with a pass-by-value through a function pointer which exhibits the problem. Second with passing scalars instead of a structure which shows the workaround, and a third trivial example with an empty structure being passed, which also exhibits a version of the problem.

FWIW, my production code exhibits a particularly egregious version of the problem, but I cannot seem to reproduce it in a small example: the non-inlined function call is at the bottom of several layers of inlined function, and a single register-resident structure is being flushed to multiple stack locations (one per inlined stack frame?) around each call to the function.



Output of "g++ -v -save-temps -O3 -S test.cpp":

Using built-in specs.
COLLECT_GCC=gcc
COLLECT_LTO_WRAPPER=/usr/local/libexec/gcc/x86_64-unknown-linux-gnu/4.5.0/lto-wrapper
Target: x86_64-unknown-linux-gnu
Configured with: ./configure
Thread model: posix
gcc version 4.5.0 (GCC) 
COLLECT_GCC_OPTIONS='-v' '-save-temps' '-O3' '-S' '-mtune=generic' '-march=x86-64'
 /usr/local/libexec/gcc/x86_64-unknown-linux-gnu/4.5.0/cc1plus -E -quiet -v -D_GNU_SOURCE test.cpp -mtune=generic -march=x86-64 -O3 -fpch-preprocess -o test.ii
ignoring nonexistent directory "/usr/local/lib/gcc/x86_64-unknown-linux-gnu/4.5.0/../../../../x86_64-unknown-linux-gnu/include"
#include "..." search starts here:
#include <...> search starts here:
 /usr/local/lib/gcc/x86_64-unknown-linux-gnu/4.5.0/../../../../include/c++/4.5.0
 /usr/local/lib/gcc/x86_64-unknown-linux-gnu/4.5.0/../../../../include/c++/4.5.0/x86_64-unknown-linux-gnu
 /usr/local/lib/gcc/x86_64-unknown-linux-gnu/4.5.0/../../../../include/c++/4.5.0/backward
 /usr/local/include
 /usr/local/lib/gcc/x86_64-unknown-linux-gnu/4.5.0/include
 /usr/local/lib/gcc/x86_64-unknown-linux-gnu/4.5.0/include-fixed
 /usr/include
End of search list.
COLLECT_GCC_OPTIONS='-v' '-save-temps' '-O3' '-S' '-mtune=generic' '-march=x86-64'
 /usr/local/libexec/gcc/x86_64-unknown-linux-gnu/4.5.0/cc1plus -fpreprocessed test.ii -quiet -dumpbase test.cpp -mtune=generic -march=x86-64 -auxbase test -O3 -version -o test.s
GNU C++ (GCC) version 4.5.0 (x86_64-unknown-linux-gnu)
	compiled by GNU C version 4.5.0, GMP version 4.3.2, MPFR version 2.4.2-p1, MPC version 0.8.1
GGC heuristics: --param ggc-min-expand=100 --param ggc-min-heapsize=131072
GNU C++ (GCC) version 4.5.0 (x86_64-unknown-linux-gnu)
	compiled by GNU C version 4.5.0, GMP version 4.3.2, MPFR version 2.4.2-p1, MPC version 0.8.1
GGC heuristics: --param ggc-min-expand=100 --param ggc-min-heapsize=131072
Compiler executable checksum: 469157b70a6e6ab9e09e15344033d953
COMPILER_PATH=/usr/local/libexec/gcc/x86_64-unknown-linux-gnu/4.5.0/:/usr/local/libexec/gcc/x86_64-unknown-linux-gnu/4.5.0/:/usr/local/libexec/gcc/x86_64-unknown-linux-gnu/:/usr/local/lib/gcc/x86_64-unknown-linux-gnu/4.5.0/:/usr/local/lib/gcc/x86_64-unknown-linux-gnu/
LIBRARY_PATH=/usr/local/lib/gcc/x86_64-unknown-linux-gnu/4.5.0/:/usr/local/lib/gcc/x86_64-unknown-linux-gnu/4.5.0/../../../../lib64/:/lib/../lib64/:/usr/lib/../lib64/:/usr/local/lib/gcc/x86_64-unknown-linux-gnu/4.5.0/../../../:/lib/:/usr/lib/
COLLECT_GCC_OPTIONS='-v' '-save-temps' '-O3' '-S' '-mtune=generic' '-march=x86-64'



And the contents of test.ii afterwards:

# 1 "test.cpp"
# 1 "<built-in>"
# 1 "<command-line>"
# 1 "test.cpp"
struct bitPointer {
    unsigned int * a;
    unsigned int b;
};

extern void (*gCausesFlushToStack)(bitPointer p);

void test1(unsigned int* a, int x) {
    bitPointer p = { a, 0 };

    for (int i = 0; i < x; ++i) {
        gCausesFlushToStack(p);

        p.a += (p.b + 1) >> 3;
        p.b = (p.b + 1) & 0x7;
    }
}

extern void (*gSameValuesAsScalarsDoesntCauseFlush)(unsigned int* a, unsigned int b);

void test2(unsigned int* a, int x) {
    bitPointer p = { a, 0 };

    for (int i = 0; i < x; ++i) {
        gSameValuesAsScalarsDoesntCauseFlush(p.a, p.b);

        p.a += (p.b + 1) >> 3;
        p.b = (p.b + 1) & 0x7;
    }
}

struct emptyObject { };
extern void (*gEvenEmptyStructureCanCauseFlush)(emptyObject object);

void test3(unsigned int* a, int x) {
    bitPointer p = { a, 0 };

    for (int i = 0; i < x; ++i) {
        gEvenEmptyStructureCanCauseFlush(emptyObject());

        p.a += (p.b + 1) >> 3;
        p.b = (p.b + 1) & 0x7;
    }
}


---


### compiler : `gcc`
### title : `pure functions returning structs are not optimized.`
### open_at : `2010-07-28T19:45:32Z`
### last_modified_date : `2023-02-02T10:15:13Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=45115
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `unknown`
### severity : `enhancement`
### contents :
compiling this with 'gcc -O3 -S x.c'

-------- x.c -----------
#define PURE __attribute__((pure))

struct res {int u; };
extern struct res calc_1() PURE; 
extern int        calc_2() PURE;

int fun_1() 
{
        return calc_1().u+calc_1().u;
}
int fun_2() 
{
        return calc_2()+calc_2();
}
--------------------

yields code which calls calc_2() *once* in fun_2() but calls calc_1() *twice* in fun_1(). Obviously, fun_1 misses an optimization.

Tested on gcc 4.4.3 (Ubuntu 10.04), gcc 4.5.0/4.4.4/4.3.5 (MacPorts)


---


### compiler : `gcc`
### title : `SRA optimization issue of bit-field`
### open_at : `2010-07-30T15:12:10Z`
### last_modified_date : `2019-03-04T12:31:57Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=45144
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.6.0`
### severity : `normal`
### contents :
For the following code:

void baz (unsigned);

extern unsigned buf[];

struct A
{
  unsigned a1:10;
  unsigned a2:3;
  unsigned:19;
};

union TMP
{
  struct A a;
  unsigned int b;
};

static unsigned
foo (struct A *p)
{
  union TMP t;
  struct A x;

  x = *p;
  t.a = x;
  return t.b;
}

void
bar (unsigned orig, unsigned *new)
{
  struct A a;
  union TMP s;

  s.b = orig;
  a = s.a;
  if (a.a1)
    baz (a.a2);
  *new = foo (&a);
}

"arm-none-eabi-gcc -O2" generates:

bar:
        @ Function supports interworking.
        @ args = 0, pretend = 0, frame = 0
        @ frame_needed = 0, uses_anonymous_args = 0
        stmfd   sp!, {r3, r4, r5, r6, r7, lr}
        mov     r4, r0, asl #22
        mov     r5, r0, lsr #10
        movs    r4, r4, lsr #22
        mov     r6, r1
        and     r5, r5, #7
        mov     r7, r0, lsr #13
        movne   r0, r5
        blne    baz
.L2:
        orr     r4, r4, r5, asl #10
        orr     r7, r4, r7, asl #13
        str     r7, [r6, #0]
        ldmfd   sp!, {r3, r4, r5, r6, r7, lr}
        bx      lr

while "arm-none-eabi-gcc -O2 -fno-tree-sra" generates:

bar:
        @ Function supports interworking.
        @ args = 0, pretend = 0, frame = 0
        @ frame_needed = 0, uses_anonymous_args = 0
        stmfd   sp!, {r3, r4, r5, lr}
        movs    r3, r0, asl #22
        mov     r4, r0
        mov     r5, r1
        movne   r0, r0, lsr #10
        andne   r0, r0, #7
        blne    baz
.L2:
        str     r4, [r5, #0]
        ldmfd   sp!, {r3, r4, r5, lr}
        bx      lr


---


### compiler : `gcc`
### title : `CDDCE doesn't eliminate conditional code in infinite loop`
### open_at : `2010-08-04T09:46:11Z`
### last_modified_date : `2023-09-17T06:42:14Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=45178
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.6.0`
### severity : `enhancement`
### contents :
Reduced from gcc.dg/tree-ssa/ssa-dce-3.c:

int main(void)
{
  unsigned j = 0;
  while (1)
    {
      j += 500;
      if (j % 7)
        j++;
      else
        j--;
    }
  return 0;
}


---


### compiler : `gcc`
### title : `Unnecessary spill slot for highpart extraction of xmm reg`
### open_at : `2010-08-05T15:02:53Z`
### last_modified_date : `2019-03-04T11:14:59Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=45198
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.6.0`
### severity : `enhancement`
### contents :
When building g++.dg/torture/pr36445.C at -O2 you can see

        call    _Z5func2v
        movaps  %xmm0, (%rsp)
        movq    (%rsp), %rdx
        movq    8(%rsp), %rax
        movq    %rdx, 16(%rsp)
        movl    %eax, 24(%rsp)

where the stack-slot spills are caused by

(insn 26 5 27 2 (set (reg:V4SF 72)
        (reg:V4SF 21 xmm0)) /space/rguenther/src/svn/trunk/gcc/testsuite/g++.dg/torture/pr36445.C:20 1054 {*movv4sf_internal}
     (nil))

(insn 27 26 28 2 (set (reg:DI 70 [ D.2130 ])
        (subreg:DI (reg:V4SF 72) 0)) /space/rguenther/src/svn/trunk/gcc/testsuite/g++.dg/torture/pr36445.C:20 61 {*movdi_internal_rex64}
     (nil))

(insn 28 27 24 2 (set (reg:DI 71 [ D.2130+8 ])
        (subreg:DI (reg:V4SF 72) 8)) /space/rguenther/src/svn/trunk/gcc/testsuite/g++.dg/torture/pr36445.C:20 61 {*movdi_internal_rex64}
     (nil))

where we are unable to verify the constraints for insn 28 because there
is no move pattern that would special case hipart extraction (which
could use movhps).


---


### compiler : `gcc`
### title : `Tree-optimization misses a trick with bit tests`
### open_at : `2010-08-06T21:28:58Z`
### last_modified_date : `2023-06-02T05:09:38Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=45215
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.6.0`
### severity : `enhancement`
### contents :
The following testcase

int x (int t)
{
  if (t & 256)
    return -26;
  return 0;
}

can be implemented as a sequence of two shifts and one and operation:
	movl	4(%esp), %eax
	sall	$23, %eax
	sarl	$31, %eax
	andl	$-26, %eax
	ret

Initial RTL generation produces a more complicated sequence which is not optimized unless the combiner is extended to handle four insns.  The tree optimizers could be enhanced to handle this pattern and related ones, although it would have to take costs into account, as on some targets other sequences may be better.


---


### compiler : `gcc`
### title : `Tree optimizations do not recognize partial stores`
### open_at : `2010-08-06T22:24:39Z`
### last_modified_date : `2021-06-08T10:17:46Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=45217
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.6.0`
### severity : `enhancement`
### contents :
unsigned int bplpt;

void BPLPTH (unsigned short x)
{
  bplpt = (bplpt & 0xFFFF) | (x << 16);
}

void BPLPTL (unsigned short x)
{
  bplpt = (bplpt & 0xFFFF0000) | x;
}

Here, nothing at the tree level recognizes that these functions implement 16-bit stores into a larger object.  This is handled by the combiner, but in its current state it fails to optimize BPLPTL as there are too many insns to look at.

This bug should stay open until there is a tree-level solution that does not rely on the RTL combiner.


---


### compiler : `gcc`
### title : `Mathematical simplification missed at tree-level`
### open_at : `2010-08-06T22:39:23Z`
### last_modified_date : `2023-05-15T04:57:02Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=45218
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.6.0`
### severity : `enhancement`
### contents :
Consider
  a = (x / 39) * 32 + (x % 39)

If we have no instruction to produce both the quotient and the remaineder, this can be computed as
  y = x / 39
  z = x - y * 39
  a = y * 32 + z

The last line can be simplified by substituting:
  a = y * 32 + x - y * 39
  a = y * (32 - 39) + x
  a = x - y * 7

Testcase:

int i_size;

extern void foo (void);
int udf_check_anchor_block(int block)
{
 i_size = ( ( ( (block) / 39 ) << 5 ) + ( block % 39 ));
 return 1;
}

The tree optimization phase misses this, and this PR should stay open until that is resolved.  The combiner can handle it if it is able to look at 4 instructions.


---


### compiler : `gcc`
### title : `missed optimization with multiple bases and casting`
### open_at : `2010-08-07T01:27:57Z`
### last_modified_date : `2023-05-06T18:14:49Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=45221
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `c++`
### version : `4.6.0`
### severity : `enhancement`
### contents :
Even under -O3, the assembly generated for foo1 and foo2 is vastly inferior to the one generated for foo3, even though code-wise all three are identical.


class Base1 { int data; };
class Base2 { int data; };
class Derived : public Base1, public Base2 { public: int data; };

int foo1(Base2* x) {
    return static_cast<Derived&>(*x).data;
}

int foo2(Base2* x) {
    return static_cast<Derived*>(x)->data;
}

int foo3(Base2* x) {
    Base2& y = *x;
    return static_cast<Derived&>(y).data;
}


---


### compiler : `gcc`
### title : `Non-volatile variables don't need to be constantly modified at -Os (no loop header copy)`
### open_at : `2010-08-09T23:06:02Z`
### last_modified_date : `2022-01-05T10:26:49Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=45243
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.5.0`
### severity : `enhancement`
### contents :
void foo (int& sz, int n)
{
    for (++n; --n;)
        sz += 5;
}

Produces (-Os):

_Z3fooRii:
        incl    %esi
        jmp     .L2
.L3:
        addl    $5, (%rdi)
.L2:
        decl    %esi
        jne     .L3
        ret

gcc thinks that every little change to sz needs to be stored in memory, causing the above inefficiency of emitting a loop instead of a multiplication. It would be desirable to treat sz as a local variable and optimize as if:

void bar (int& sz, int n)
{
    int tmp = sz;
    for (++n; --n;)
        tmp += 5;
    sz = tmp;
}

Which compiles to:

_Z3barRii:
        leal    (%rsi,%rsi,4), %esi
        addl    %esi, (%rdi)
        ret

much better code. If somebody really does need each variable access to be a memory access, that variable should be declared volatile.

If you don't want to fix this, at least provide a variable attribute to tell the compiler that it's ok to omit stores.


---


### compiler : `gcc`
### title : `unnecessary register move`
### open_at : `2010-08-11T03:39:57Z`
### last_modified_date : `2023-05-15T05:07:39Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=45252
### status : `NEW`
### tags : `missed-optimization, needs-bisection`
### component : `target`
### version : `4.6.0`
### severity : `normal`
### contents :
Compile the following code with options -march=armv7-a -mthumb -Os

struct S{
    int f1;
    int reserved[3];
};

void ts()
{
        struct S map;
        map.f1 = 0;
        foo(&map);
}

GCC 4.6 generates:

ts:
        push    {r0, r1, r2, r3, r4, lr}
        add     r0, sp, #16        // A
        movs    r3, #0
        str     r3, [r0, #-16]!    // B
        mov     r0, sp             // C
        bl      foo
        add     sp, sp, #20
        pop     {pc}

After instruction B, register r0 already contains the value of sp, so instruction C is not required, as shown in following.

ts:
        push    {r0, r1, r2, r3, r4, lr}
        add     r0, sp, #16        
        movs    r3, #0
        str     r3, [r0, #-16]!    
        bl      foo
        add     sp, sp, #20
        pop     {pc}

The RTL insns before IRA

(insn 12 5 6 2 (set (reg/f:SI 134)
        (reg/f:SI 25 sfp)) src/ts.c:9 694 {*thumb2_movsi_insn}
     (nil))

(insn 6 12 8 2 (set (mem/s/c:SI (pre_modify:SI (reg/f:SI 134)
                (plus:SI (reg/f:SI 134)
                    (const_int -16 [0xfffffffffffffff0]))) [3 map.f1+0 S4 A64])
        (reg:SI 133)) src/ts.c:9 694 {*thumb2_movsi_insn}
     (expr_list:REG_DEAD (reg:SI 133)
        (expr_list:REG_INC (reg/f:SI 134)
            (expr_list:REG_EQUAL (const_int 0 [0])
                (nil)))))

(insn 8 6 9 2 (set (reg:SI 0 r0)
        (reg/f:SI 134)) src/ts.c:10 694 {*thumb2_movsi_insn}
     (expr_list:REG_DEAD (reg/f:SI 134)
        (expr_list:REG_EQUAL (plus:SI (reg/f:SI 25 sfp)
                (const_int -16 [0xfffffffffffffff0]))
            (nil))))

It shows the address register in insn 6 can be used in insn 8 directly. At RA stage, physical register r0 is assigned to pseudo register r134, so insn 8 should be
    mov  r0, r0
which should be removed in later pass.

But gcc also finds out from note that r134 is equal to (sfp - 16) which is equal to sp at the same time. So it generates 
    mov r0, sp


There is even better result:

ts:
        push    {r0, r1, r2, r3, r4, lr}
        movs    r3, #0
        str     r3, [sp]
        mov     r0, sp
        bl      foo
        add     sp, sp, #20
        pop     {pc}

It contains same number of instructions, but the instructions are simpler and shorter. Actually the IL was in this form after expand

(insn 5 2 6 2 (set (reg:SI 133)
        (const_int 0 [0])) src/ts.c:9 694 {*thumb2_movsi_insn}
     (nil))

(insn 6 5 7 2 (set (mem/s/c:SI (plus:SI (reg/f:SI 25 sfp)
                (const_int -16 [0xfffffffffffffff0])) [3 map.f1+0 S4 A64])
        (reg:SI 133)) src/ts.c:9 694 {*thumb2_movsi_insn}
     (expr_list:REG_DEAD (reg:SI 133)
        (expr_list:REG_EQUAL (const_int 0 [0])
            (nil))))

(insn 7 6 8 2 (set (reg/f:SI 134)
        (plus:SI (reg/f:SI 25 sfp)
            (const_int -16 [0xfffffffffffffff0]))) src/ts.c:10 4 {*arm_addsi3}
     (nil))

(insn 8 7 9 2 (set (reg:SI 0 r0)
        (reg/f:SI 134)) src/ts.c:10 694 {*thumb2_movsi_insn}
     (expr_list:REG_DEAD (reg/f:SI 134)
        (expr_list:REG_EQUAL (plus:SI (reg/f:SI 25 sfp)
                (const_int -16 [0xfffffffffffffff0]))
            (nil))))

After pass auto_inc_dec, (sfp - 16) is identified as an opportunity for auto_inc_dec optimization. But it doesn't bring any benefit for this case, and causes more complex instructions.


---


### compiler : `gcc`
### title : `Missed arithmetic simplification at tree level`
### open_at : `2010-08-11T15:18:38Z`
### last_modified_date : `2021-09-15T00:54:09Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=45256
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.6.0`
### severity : `enhancement`
### contents :
I'll attach a testcase, which shows a missed simplification at tree level:

  D.2276_42 = i_53 + 1;
  D.2277_43 = D.2276_42 * 32;
  iftmp.3_55 = __fswab32 (xb_54);
  __asm__("clz  %0, %1" : "=r" ret_56 : "r" iftmp.3_55 : "cc");
  ret_58 = 32 - ret_56;
  ret_59 = D.2277_43 - ret_58;

In effect, the constant 32 is both added and subtracted from the result.  With a four-insn combiner, this is caught at the RTL stage (compiling for Thumb-1):

-       add     r2, r2, #1
        lsl     r2, r2, #5
-       add     r3, r3, r2
-       sub     r3, r3, #32
+       add     r3, r2, r3


---


### compiler : `gcc`
### title : `__restrict__ type qualifier does not work on pointers to bitfields`
### open_at : `2010-08-13T07:06:14Z`
### last_modified_date : `2021-12-22T09:53:39Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=45274
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.6.0`
### severity : `enhancement`
### contents :
I tested an svn build from 20100813 with the following code:

struct bar {
        unsigned int a:1, b:1, c:1, d:1, e:28;
};

void foo(struct bar * __restrict__ src, struct bar * __restrict__ dst)
{
        dst->a = src->a;
        dst->b = src->b;
        dst->c = src->c;
        dst->d = src->d;
        dst->e = src->e;
}

Built as 32bit, we see loads and stores as if the compiler is following pointer aliasing rules:

# gcc -m32 -O2 -S foo.c 

foo:
	lwz 9,0(3)
	lwz 0,0(4)
	rlwimi 0,9,0,0,0
	stw 0,0(4)
	lwz 9,0(3)
	rlwimi 0,9,0,1,1
	stw 0,0(4)
	lwz 9,0(3)
	rlwimi 0,9,0,2,2
	stw 0,0(4)
	lwz 9,0(3)
	rlwimi 0,9,0,3,3
	stw 0,0(4)
	lwz 9,0(3)
	rlwimi 0,9,0,4,31
	stw 0,0(4)
	blr

Apologies if I am misusing or misinterpreting the use of __restrict__ here.

Also, when built as 64bit things are considerably more complex. Is there a reason why we can't use the same code as 32bit?

# gcc -m64 -O2 -S foo.c
...
.L.foo:
	lwz 9,0(4)
	lwz 0,0(3)
	rlwinm 9,9,0,1,31
	rlwinm 0,0,0,0,0
	or 0,9,0
	stw 0,0(4)
	rlwinm 0,0,1,1,31
	rlwinm 0,0,31,0xffffffff
	lwz 9,0(3)
	rldicl 9,9,34,63
	slwi 9,9,30
	or 0,0,9
	stw 0,0(4)
	rlwinm 9,0,2,1,31
	rlwinm 9,9,30,0xffffffff
	lwz 0,0(3)
	rldicl 0,0,35,63
	slwi 0,0,29
	or 0,9,0
	stw 0,0(4)
	rlwinm 0,0,3,1,31
	rlwinm 0,0,29,0xffffffff
	lwz 9,0(3)
	rldicl 9,9,36,63
	slwi 9,9,28
	or 0,0,9
	stw 0,0(4)
	rlwinm 0,0,0,0,3
	lwz 9,0(3)
	rlwinm 9,9,0,4,31
	or 0,0,9
	stw 0,0(4)
	blr


---


### compiler : `gcc`
### title : `[6 Regression] Issues with integer narrowing conversions`
### open_at : `2010-08-24T13:19:21Z`
### last_modified_date : `2018-11-19T11:53:44Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=45397
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.6.0`
### severity : `normal`
### contents :
In http://gcc.gnu.org/ml/gcc/2010-08/msg00326.html
Revital complained about MAX_EXPR no longer being recognized in:
int foo (const unsigned char *tmp, int i, int val)
{
  return (unsigned char)(((tmp[i] + val)>0xFF)?0xFF:(((tmp[i] + val)<0)?0:(tmp[i] + val)));
}
It is still recognized when using:
int bar (const unsigned char *tmp, int i, int val)
{
  int x = (((tmp[i] + val)>0xFF)?0xFF:(((tmp[i] + val)<0)?0:(tmp[i] + val)));
  return (unsigned char)x;
}
The regression is caused by folding being delayed in the C FE, while before
the inner COND_EXPR has been optimized by fold_ternary* into MAX_EXPR, now it isn't immediately, thus convert_to_integer on the narrowing conversion propagates the (unsigned char) narrowing casts down into the operands and when fold_ternary* is actually called, it is too late, as the operands aren't considered equal.

Perhaps it would be nice for -O2 to consider for e.g. int a and b
that (unsigned char) (a + b) is the same as (unsigned char) a + (unsigned char) b during VN.


---


### compiler : `gcc`
### title : `constant not optimized / propagated across printf calls`
### open_at : `2010-08-26T05:13:13Z`
### last_modified_date : `2021-11-24T08:52:12Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=45410
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.4.3`
### severity : `enhancement`
### contents :
gcc -Wall -O3 -S test.c
doesn't seem to propagate constants correctly.

Notice that ss is declared static, therefor everything is known at compile time.

Code:
#include <stdio.h>

struct s {int i;int j;};
struct s static ss={77,2};

int
main() 
{
        ss.j += 88;
        printf("%d\n",sizeof(ss));
        return ss.i+ss.j;
};


---


### compiler : `gcc`
### title : `x86 missed optimization: use high register (ah, bh, ch, dh) when available to make comparisons`
### open_at : `2010-08-27T23:02:34Z`
### last_modified_date : `2021-08-14T20:56:42Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=45434
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `unknown`
### severity : `enhancement`
### contents :
It is unnecessary to shift a value in a high register position (ah, bh, ch, dh) down to a low register position (al, bl, cl, dl) to perform a machine comparison. X86-64 Linux ABI exhaustive example:

#include <assert.h>
#include <stdbool.h>
#include <stdint.h>

__attribute__ ((noinline)) bool check_via_c(uint64_t i) {
  if ((i & 0xFF) == ((i & 0xFF00) >> 8)) return true;
  return false;
}

__attribute__ ((noinline)) bool check_via_asm(uint64_t i) {
  bool result;
  __asm__ ("mov %%rdi, %%rax\n"
	   "cmp %%al, %%ah\n"
	   "sete %0\n" : "=r" (result));
  return result;
}

int main() {
  for (uint64_t i=0; i <= 0xFFFFFFFFFFFFFFFF; ++i) {
    assert(check_via_c(i) == (check_via_asm(i)));
  }
}

gcc-4.5 -O3 -std=gnu99 ah_bh_ch_dh_missed_optimization.c && objdump -d -m i386:x86-64 a.out |less

GCC generates:
0000000000400530 <check_via_c>:
  400530:       48 89 f8                mov    %rdi,%rax
  400533:       48 c1 e8 08             shr    $0x8,%rax
  400537:       40 38 f8                cmp    %dil,%al
  40053a:       0f 94 c0                sete   %al
  40053d:       c3                      retq   

A superior solution:
0000000000400540 <check_via_asm>:
  400540:       48 89 f8                mov    %rdi,%rax
  400543:       38 c4                   cmp    %al,%ah
  400545:       0f 94 c0                sete   %al
  400548:       c3                      retq


---


### compiler : `gcc`
### title : `PRE misses oppurtunity for statement folding.`
### open_at : `2010-09-03T15:58:19Z`
### last_modified_date : `2021-07-20T07:45:47Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=45522
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.6.0`
### severity : `enhancement`
### contents :
Hi,
compiling the attached testcase (reduced from tree.c) with -O2 leads to vrp folding:
  if (D.2762_2 == 6)
    goto <bb 3>;
  else
    goto <bb 9>;
  
<bb 3>:
  D.2766_5 = (int) D.2762_2;
  D.2767_6 = tree_code_type[D.2766_5];

into
  D.2762_2 = type_1(D)->base.code;
  if (D.2762_2 == 6)
    goto <bb 3>;
  else
    goto <bb 9>;
  
<bb 3>:
  D.2766_5 = 6;
  D.2767_6 = tree_code_type[6];

this is good transform, however tree_code_type is constant initialized array and we miss possibility to fold it into constant until expansion triggering code in expr.c I would like to retire.

We can fold tree_code_type[6], so apparently just no one calls fold_gimple_stmt on it?


---


### compiler : `gcc`
### title : `Add with carry - missed optimization on x86`
### open_at : `2010-09-05T17:59:13Z`
### last_modified_date : `2021-09-11T14:35:26Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=45548
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.4.1`
### severity : `enhancement`
### contents :
This is very related to this bug (43892):
http://gcc.gnu.org/bugzilla/show_bug.cgi?id=43892

There are many ways to try to add with carry - and difficult to catch them all. I really 'tried to think like a compiler' when I wrote the following
(C++ Intel 32bit code) code:
(not even strict correctly c++. It won't work with AMD64 - since long long is 64 bit - just like unsigned long - and __int128 isn't quite there yet).

// Data structures:
struct Skew1Even
{
  unsigned long long data; // This could be an array 
  unsigned long unused;
};

struct Skew2Odd
{
  unsigned long unused;
  unsigned long long data;  // This could be an array
};

struct ULongLongLong
{
  union
  {
    unsigned long m_data[3];
    Skew1 m_rep1;
    Skew2 m_rep2;
  };
  ULongLongLong()
  {
    m_data[0]=0;
    m_data[1]=0;
    m_data[2]=0;
  }
//  void print() {  std::cout << m_data[0] << "," << m_data[1] << "," << // m_data[2] << "\n";}
  void addtest(const ULongLongLong &b); // operator += 
};

The addtest is the important part:
void ULongLongLong::addtest(const ULongLongLong &b)
{
//  if (this==&b) // removed to make the example easier
//    doTimes2();    
  m_rep1.data+=b.m_data[0];
  m_rep2.data+=b.m_data[1];
  m_data[2]+=b.m_data[2];
}

The main point in my code is also in the compiled code (but not used by the compiler). What I hoped to happen was that gcc saw that adding 0 with carry 'quickly' followed by a normal add would be the same as just the last add (but) with carry.

I however only get the code:
.globl _ZN13ULongLongLong7addtestERKS_
	.type	_ZN13ULongLongLong7addtestERKS_, @function
_ZN13ULongLongLong7addtestERKS_:
.LFB964:
	.cfi_startproc
	.cfi_personality 0x0,__gxx_personality_v0
	pushl	%ebp
	.cfi_def_cfa_offset 8
	movl	%esp, %ebp
	.cfi_offset 5, -8
	.cfi_def_cfa_register 5
	movl	12(%ebp), %edx
	movl	8(%ebp), %eax
	pushl	%ebx
	xorl	%ebx, %ebx
	.cfi_offset 3, -12
	movl	(%edx), %ecx
	addl	%ecx, (%eax)
	adcl	%ebx, 4(%eax)
	xorl	%ebx, %ebx
	movl	4(%edx), %ecx
	addl	%ecx, 4(%eax)
	adcl	%ebx, 8(%eax)
	movl	8(%edx), %edx
	addl	%edx, 8(%eax)
	popl	%ebx
	popl	%ebp
	ret
	.cfi_endproc

What I wanted was this code:
globl _ZN13ULongLongLong7addtestERKS_
        .type   _ZN13ULongLongLong7addtestERKS_, @function
_ZN13ULongLongLong7addtestERKS_:
.LFB1001:
        .cfi_startproc
        .cfi_personality 0x0,__gxx_personality_v0
        pushl   %ebp
        .cfi_def_cfa_offset 8
        movl    %esp, %ebp
        .cfi_offset 5, -8
        .cfi_def_cfa_register 5
        movl    12(%ebp), %edx
        movl    8(%ebp), %eax
/*      pushl   %ebx */  /* not needed anymore - we don't use it */
/*      xorl    %ebx, %ebx   No need to reset ebx */
        .cfi_offset 3, -12
        movl    (%edx), %ecx
        addl    %ecx, (%eax)
/*      adcl    %ebx, 4(%eax)   */
/*      xorl    %ebx, %ebx     Why do it at all - ebx was already 0 !?*/
        movl    4(%edx), %ecx
        adcl    %ecx, 4(%eax) /* modified addl to adcl */
/*      adcl    %ebx, 8(%eax)  */
        movl    8(%edx), %edx
        adcl    %edx, 8(%eax)  /* modified addl to adcl */
/*      popl    %ebx */
        popl    %ebp
        ret
        .cfi_endproc

However - the code I want is:
Note: It seems like adding could be replaced with subtraction.

It may still be better to make carry work a bit more in general - and I understand that this might be a won't fix - especially if you provide a clear way to add with carry in general.
 
However this might just be a much easier peephole(-like) optimization.

PS: Thanks for a really great compiler.


---


### compiler : `gcc`
### title : `Suboptimal code generation on arm`
### open_at : `2010-09-09T21:39:25Z`
### last_modified_date : `2021-11-28T00:21:48Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=45622
### status : `WAITING`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.5.0`
### severity : `normal`
### contents :
Vorbis author, Timothy Terriberry, was complaining about gcc inefficiency on arm, so I asked him write it up in case it would be of use to gcc devs to improve gcc. Is this a useful?

His description follows:

You asked me at the summit to describe some of the problems gcc has on ARM. I'll start with the function oc_huff_token_decode from libtheora, which is the last function in http://svn.xiph.org/experimental/derf/theora-ptalarbvorm/lib/huffdec.c
This is the primary function for bitstream decoding, and may get called a few hundred thousand times per frame. Unlike most of the other time-critical functions in a video codec, it can't really be accelerated with SIMD asm, though given how badly gcc does, regular asm might be worth it.

This the result of using arm-none-linux-gnueabi-gcc (Gentoo 4.5.0 p1.1) 4.5.0 with -O3 -fomit-frame-pointer -funroll-loops (this last makes a fairly big difference on x86, and so is part of the default flags for the library).

oc_huff_token_decode:
        @ Function supports interworking.
        @ args = 0, pretend = 0, frame = 8
        @ frame_needed = 0, uses_anonymous_args = 0
        @ link register save eliminated.
        stmfd   sp!, {r4, r5, r6, r7, r8, r9, sl, fp}
        sub     sp, sp, #8

So, the next two lines already start off bad:

        str     r0, [sp, #4]
        ldr     r4, [sp, #4]

Spilling the register to the stack might be okay, but then loading it back from the stack when it's still in r0?

        ldr     ip, [r0, #4]
        ldr     r3, [r0, #8]
        ldr     r2, [r4, #12]
        ldr     r0, [r0, #0]

And then continuing to use _both_ the copy in r0 and r4? What did we even make the copy for? r0 is now clobbered, and r4 gets clobbered before it gets used again.

Maybe I'm missing some subtlety here:

        mov     fp, r1

but it seems to me this mov could easily be eliminated by swapping the roles of fp and r1 everywhere below (that may not be the best solution, but it's certainly _a_ solution). This is one of the larger problems with gcc on ARM: it emits way too many moves for something that's supposed to be compiling for a three-address ISA.

        mov     r7, #0
.L418:
        mov     r1, r7, asl #1
        ldrsh   r5, [fp, r1]
        cmp     r2, r5

The "fast path" here takes this branch instead of falling through, but that's probably my fault for not using PGO or __builtin_expect().

        bge     .L414
        cmp     ip, r0
        bcs     .L419
        rsb     r1, r2, #24
        ldrb    r6, [ip], #1    @ zero_extendqisi2
        subs    r4, r1, #8
        add     r2, r2, #8
        orr     r3, r3, r6, asl r1
        bmi     .L414

So here we're checking if ptr - stop has 4 byte alignment so that we can do 4 iterations at once without testing the if-block inside the loop. This is all well and good, except that the loop can only iterate 3 times. All of the unrolling it does to get the alignment right would already have been enough to execute the entire loop. gcc continues to generate code like this even when n and available are declared as unsigned (so that overflow would be required to get "shift" larger than 24, instead of just loading a negative value for available) and when -funsafe-loop-optimizations is used (though I don't think this is what that flag actually controls). I'd be happy to hear other suggestions for rewriting this so that gcc can recognize the iteration limit, as I doubt that's just an ARM problem.

        rsb     r6, ip, r0
        ands    r6, r6, #3
        mov     r1, ip
        beq     .L434
        cmp     r0, ip
        bls     .L419

So here we... copy ip into r1, then immediately clobber the original ip, then put r1 _back_ into ip. Two more wasted instructions.

        mov     r1, ip
        ldrb    ip, [r1], #1    @ zero_extendqisi2
        add     r2, r2, #8
        orr     r3, r3, ip, asl r4
        subs    r4, r4, #8
        mov     ip, r1

        bmi     .L414
        cmp     r6, #1
        beq     .L434
        cmp     r6, #2
        beq     .L429
        ldrb    ip, [r1], #1    @ zero_extendqisi2
        add     r2, r2, #8
        orr     r3, r3, ip, asl r4
        subs    r4, r4, #8
        mov     ip, r1
        bmi     .L414
.L429:
        ldrb    ip, [r1], #1    @ zero_extendqisi2
        add     r2, r2, #8
        orr     r3, r3, ip, asl r4
        subs    r4, r4, #8
        mov     ip, r1
        bmi     .L414

So here's another minor disaster of excess mov's. r7 is copied into r9 so that r7 can be used inside the loop... except this loop is self-contained and could just as well have used r9.

.L434:
        mov     r9, r7
.L415:

Also, since we just branched here so we could compare ptr to stop once every four (of three total) iterations, the first thing we do is... compare ptr against stop. So in the best case this "optimization" actually does three comparisons instead of two if the loop iterates twice (including the alignment test), and only if we iterate three times (the maximum) and happened to have the correct alignment (1 in 4 chance) does it break even.

        cmp     r0, r1

What is actually put in r7? Why, one of _two_ copies of r1. r1 really contains the value of ip, which we uselessly copied to it above, and using it here means we needed to add _another_ useless copy of ip to r1 in the other path to this label.

        mov     r7, r1
        add     r2, r2, #8

This is the one that really takes the cake: just in case we branch here, we'll copy r1 back into ip (note that ip already contains r1), and then if we don't branch we immediately clobber it. It does this every time.

        mov     ip, r1
        bls     .L437
        ldrb    ip, [r7], #1    @ zero_extendqisi2
        subs    r6, r4, #8
        orr     r3, r3, ip, asl r4
        mov     r8, r2
        mov     ip, r7

This one is also pretty fantastic. So, this time we're going to do the load using r1, instead of r7 like we did above (why do we have two copies? I still don't know! actually three if you count ip). That means we need to increment r7 manually instead of doing it as part of the load. And just for giggles, we do that _before_ the branch here, which goes to an instruction that immediately clobbers r7.

        add     r7, r7, #1
        bmi     .L436
        ldrb    ip, [r1, #1]    @ zero_extendqisi2
        subs    sl, r6, #8
        orr     r3, r3, ip, asl r6
        add     r2, r2, #8
        mov     ip, r7
        bmi     .L436
        ldrb    r6, [r7, #0]    @ zero_extendqisi2
        subs    r7, r4, #24
        add     ip, r1, #3
        add     r2, r8, #16
        orr     r3, r3, r6, asl sl
        bmi     .L436
        ldrb    ip, [r1, #3]    @ zero_extendqisi2
        subs    r4, r4, #32
        add     r1, r1, #4
        orr     r3, r3, ip, asl r7
        add     r2, r8, #24

Yeah, better copy r1 into ip again so we can... copy r1 into ip again after the jump. Fortunately the iteration limit means we can never actually get here.

        mov     ip, r1
        bpl     .L415
.L436:
        mov     r7, r9
.L414:
        rsb     r1, r5, #32
        add     r1, r7, r3, lsr r1
        add     r7, fp, r1, asl #1
        ldrsh   r7, [r7, #2]
        cmp     r7, #0

Again, the fast path takes this branch.

        ble     .L417
.L438:
        mov     r3, r3, asl r5
        rsb     r2, r5, r2
        b       .L418
.L437:
        mov     r7, r9
.L419:
        rsb     r1, r5, #32
        add     r1, r7, r3, lsr r1
        add     r7, fp, r1, asl #1
        ldrsh   r7, [r7, #2]
        mov     r2, #1073741824
        cmp     r7, #0
        bgt     .L438
.L417:
        rsb     r7, r7, #0
        mov     r0, r7, asr #8
        mov     r3, r3, asl r0

Yeah! We can finally load back that value we stashed on the stack! Maybe if we hadn't made three or four copies of ptr, we might have been able to keep it in a register.

        ldr     r1, [sp, #4]
        rsb     r2, r0, r2
        str     ip, [r1, #4]
        and     r0, r7, #255
        str     r3, [r1, #8]
        str     r2, [r1, #12]
        add     sp, sp, #8
        ldmfd   sp!, {r4, r5, r6, r7, r8, r9, sl, fp}
        bx      lr



Things are a little better without -funroll-loops, mostly because the function is much shorter, but there are still obvious problems, e.g., in the epilogue:

        and     r8, r8, #255
        stmib   r0, {r3, ip}    @ phole stm
        str     r2, [r0, #12]
        mov     r0, r8

If the and was re-ordered, it could take the place of the mov (the -funroll-loops version gets this right). Or the prologue:

        ldmib   r0, {r3, ip}    @ phole ldm
        ldr     r4, [r0, #0]
        ldr     r2, [r0, #12]

It isn't clear to me why it picked registers that were out of order, when it could have loaded all four with one ldm. But hey, at least that's better than the -funroll-loops versions, which did four individual loads! Fixing this would also likely have allowed combining the  stmib/str in the epilogue.


---


### compiler : `gcc`
### title : `const function pointer propagation issues with inlining`
### open_at : `2010-09-10T08:50:09Z`
### last_modified_date : `2021-08-05T23:57:05Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=45632
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.6.0`
### severity : `enhancement`
### contents :
The attached test case is testing inlining of const function pointers
in a typical "OO code written in C" situation.

The code shows two optimization problems:

- a_foo is inlined into main, b_foo is not.
The only difference is that new_a() returns a const pointer 
and new_b() does not. I would have assumed that gcc detects that the pointer coming out of new_b() is const.

- p->ops->op2 is never inlined, not even for a, even though the compiler
should have enough information to do so (everything that is passed in is 
const). I assume this is because cloning does not work through
function pointers?


---


### compiler : `gcc`
### title : `Unnecessary runtime versioning for aliasing`
### open_at : `2010-09-29T14:00:48Z`
### last_modified_date : `2022-12-26T06:39:43Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=45833
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.6.0`
### severity : `normal`
### contents :
union U { unsigned char c[32]; unsigned short s[16]; };

void
foo (union U *d, union U *s)
{
  int i;
  for (i = 0; i < 16; i++)
    d->s[i] += s->s[i];
}

void
bar (union U *d, union U *s)
{
  d->s[0] += s->s[0];
  d->s[1] += s->s[1];
  d->s[2] += s->s[2];
  d->s[3] += s->s[3];
  d->s[4] += s->s[4];
  d->s[5] += s->s[5];
  d->s[6] += s->s[6];
  d->s[7] += s->s[7];
  d->s[8] += s->s[8];
  d->s[9] += s->s[9];
  d->s[10] += s->s[10];
  d->s[11] += s->s[11];
  d->s[12] += s->s[12];
  d->s[13] += s->s[13];
  d->s[14] += s->s[14];
  d->s[15] += s->s[15];
}

has in foo unnecessary runtime versioning for aliasing, even when we should be able to conclude that either d == s (but that is fine for vectorizing it, as
the result is stored after the sources are read), or d->s[0] ... d->s[15] doesn't overlap with s->s[0] ... s->s[15].

test.c:7: note: === vect_analyze_dependences ===
test.c:7: note: dependence distance  = 0.
test.c:7: note: dependence distance == 0 between d_3(D)->s[i_14] and d_3(D)->s[i_14]
test.c:7: note: versioning for alias required: can't determine dependence between s_5(D)->s[i_14] and d_3(D)->s[i_14]
test.c:7: note: mark for run-time aliasing test between s_5(D)->s[i_14] and d_3(D)->s[i_14]

In bar SLP isn't done, although when adding __restrict qualifiers it is done.


---


### compiler : `gcc`
### title : `Possible missed optimization - array ops vs shift-and-mask`
### open_at : `2010-10-01T18:31:54Z`
### last_modified_date : `2021-06-03T02:54:54Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=45861
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.5.1`
### severity : `enhancement`
### contents :
Created attachment 21938
test case

The attached .c file contains two functions, which (unless I screwed up) compute exactly the same (mathematical) function - they take an array of 8 bytes, permute its elements, and stuff them into a 64-bit integer, which is then returned.  However, GCC generates very different code for each (on x86-64).  There seem to be two missed optimization opportunities here:

1) I don't know *which* of the two code generation possibilities here is better, but it seems like GCC ought to know and ought to generate that code for both functions.

2) Could we be taking advantage of SSEn vector permute instructions here?


---


### compiler : `gcc`
### title : `unnecessary load of 32/64bit variable when only 8 bits are needed`
### open_at : `2010-10-05T22:58:31Z`
### last_modified_date : `2021-08-16T22:19:18Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=45903
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.6.0`
### severity : `enhancement`
### contents :
Created attachment 21967
testcase for both cases

For the following testcase:

uint8_t f64(uint64_t a, uint64_t b)
{
	return (a >> 8) + (b >> 8);
}

gcc (r164716) generates this code:

$ gcc -O3 -S -m32 tst10.s tst10.c -masm=intel

f64:
        push    ebx
        mov     ecx, DWORD PTR [esp+8]
        mov     ebx, DWORD PTR [esp+12]
        mov     eax, DWORD PTR [esp+16]
        mov     edx, DWORD PTR [esp+20]
        shrd    ecx, ebx, 8
        pop     ebx
        shrd    eax, edx, 8
        add     eax, ecx
        ret

while it could use just something like:
f64:
mov al, DWORD PTR [esp+5]
add al, DWORD PTR [esp+9]
ret


The situation is better for 32bit case:

uint8_t f32(uint32_t a, uint32_t b)
{
	return (a >> 8) + (b >> 8);
}

where gcc generates:
$ gcc -O3 -S -m32 tst10.s tst10.c -masm=intel

f32:
        mov     eax, DWORD PTR [esp+4]
        mov     edx, DWORD PTR [esp+8]
        shr     eax, 8
        shr     edx, 8
        add     eax, edx
        ret

while it could generate the same code as for f64:
f32:
mov al, DWORD PTR [esp+5]
add al, DWORD PTR [esp+9]
ret


---


### compiler : `gcc`
### title : `Use not in stead of add to generate new constant`
### open_at : `2010-10-12T08:42:41Z`
### last_modified_date : `2023-05-15T05:10:29Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=45980
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.6.0`
### severity : `enhancement`
### contents :
Compile the following code:

typedef struct {
      unsigned long state[5];
      unsigned long count[2];
} SHA1_CTX;

void SHA1Init(SHA1_CTX* context)
{
      /* SHA1 initialization constants */
      context->state[0] = 0x67452301;
      context->state[1] = 0xEFCDAB89;
      context->state[2] = 0x98BADCFE;
      context->state[3] = 0x10325476;
      context->state[4] = 0xC3D2E1F0;
      context->count[0] = context->count[1] = 0;
}

With options -march=armv7-a -mthumb -Os, gcc generates:

SHA1Init:
        ldr     r3, .L2
        str     r3, [r0, #0]
        add     r3, r3, #-2004318072    
        str     r3, [r0, #4]
        ldr     r3, .L2+4
        str     r3, [r0, #8]
        sub     r3, r3, #-2004318072     
        str     r3, [r0, #12]
        ldr     r3, .L2+8
        str     r3, [r0, #16]
        movs    r3, #0
        str     r3, [r0, #24]
        str     r3, [r0, #20]
        bx      lr
.L3:
        .align  2
.L2:
        .word   1732584193
        .word   -1732584194
        .word   -1009589776

This function needs to store 5 large constants to memory. Instead of load the 5 constants from constant pool, gcc found two of them can be computed out by a single add/sub constant instruction. But we can do better, notice that

0x67452301 + 0x98BADCFE = 0xFFFFFFFF
0xEFCDAB89 + 0x10325476 = 0xFFFFFFFF

So if we have one such constant, the other one can be computed out by bitwise not. So a shorter result could be:

SHA1Init:
        ldr     r3, .L2
        str     r3, [r0, #0]
        add     r2, r3, #-2004318072    
        str     r2, [r0, #4]
        movns     r3, r3
        str     r3, [r0, #8]
        movns     r2, r2
        str     r2, [r0, #12]
        ldr     r3, .L2+4
        str     r3, [r0, #16]
        movs    r3, #0
        str     r3, [r0, #24]
        str     r3, [r0, #20]
        bx      lr
.L3:
        .align  2
.L2:
        .word   1732584193
        .word   -1009589776


---


### compiler : `gcc`
### title : `gfortran.dg/vect/fast-math-pr38968.f90 times out on 32-bit Solaris 10/x86`
### open_at : `2010-10-12T18:04:10Z`
### last_modified_date : `2021-12-25T22:39:57Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=45988
### status : `NEW`
### tags : `missed-optimization, testsuite-fail`
### component : `target`
### version : `4.7.0`
### severity : `normal`
### contents :
The 32-bit gfortran.dg/vect/fast-math-pr38968.f90 execution test regularly times
out on Solaris 10/x86:

WARNING: program timed out.
FAIL: gfortran.dg/vect/fast-math-pr38968.f90 execution test

at least when run with a make -j16 -k check on a Sun Fire X4450 (4 x Xeon X7350,
2.93 GHz).

When run on an otherwise idle machine, it takes about 1:31 min, well below the
default dejagnu timeout of 5 minutes.  Perhaps the timeout factor 4.0 that was
present until 4.5 needs to be reinstantiated?


---


### compiler : `gcc`
### title : `vectorization outside of loops starting from loads`
### open_at : `2010-10-13T14:23:45Z`
### last_modified_date : `2023-06-21T13:17:07Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=46006
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.6.0`
### severity : `enhancement`
### contents :
Are there any plans to try to vectorize parts of code like:
struct A
{
  double x, y, z;
};

struct B
{
  struct A a, b;
};

struct C
{
  struct A c;
  double d;
};

__attribute__((noinline, noclone)) int
foo (const struct C *u, struct B v)
{
  double a, b, c, d;

  a = v.b.x * v.b.x + v.b.y * v.b.y + v.b.z * v.b.z;
  b = 2.0 * v.b.x * (v.a.x - u->c.x)
      + 2.0 * v.b.y * (v.a.y - u->c.y) + 2.0 * v.b.z * (v.a.z - u->c.z);
  c = u->c.x * u->c.x + u->c.y * u->c.y + u->c.z * u->c.z
      + v.a.x * v.a.x + v.a.y * v.a.y + v.a.z * v.a.z
      + 2.0 * (-u->c.x * v.a.x - u->c.y * v.a.y - u->c.z * v.a.z)
      - u->d * u->d;
  if ((d = b * b - 4.0 * a * c) < 0.0)
    return 0;
  return d;
}

int
main (void)
{
  int i, j;
  struct C c = { { 1.0, 1.0, 1.0 }, 1.0 };
  struct B b = { { 1.0, 1.0, 1.0 }, { 1.0, 1.0, 1.0 } };
  for (i = 0; i < 100000000; i++)
    {
      asm volatile ("" : : "r" (&c), "r" (&b) : "memory");
      j = foo (&c, b);
      asm volatile ("" : : "r" (j));
    }
  return 0;
}
(this is the hot spot from c-ray benchmark, the function is actually larger but at least according to callgrind in most cases the early return on < 0.0 happens;
as the function is large and called from multiple spots, it isn't inlined).
I'd say (though, haven't tried to code it by hand using intrinsics) that by
doing many of the multiplications/additions in parallel (especially for AVX) there could be significant speedups (-O3 -ffast-math).


---


### compiler : `gcc`
### title : `256bit vectorizer failed on int->double`
### open_at : `2010-10-14T08:53:36Z`
### last_modified_date : `2021-02-23T10:48:38Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=46012
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.6.0`
### severity : `enhancement`
### contents :
For

---
double a[1024];
float b[1024];
int c[1024];

void dependence_distance_4_mixed_0 (void)
{
  int i;
  for (i = 0; i < 1020; ++i)
    a[i + 4] = a[i] + a[i + 4] + c[i];
}
---

with -O3 -ffast-math -mavx, vect256 branch generates:

.L2:
	vmovapd	a(%rax,%rax), %ymm0
	vcvtdq2pd	c(%rax), %ymm1
	vaddpd	a+32(%rax,%rax), %ymm0, %ymm0
	vaddpd	%ymm1, %ymm0, %ymm0
	vmovapd	%ymm0, a+32(%rax,%rax)
	addq	$16, %rax
	cmpq	$4080, %rax
	jne	.L2

Trunk at revision 165455 generates

.L2:
	vmovapd	16(%rax), %xmm2
	vaddpd	-16(%rax), %xmm2, %xmm2
	vmovdqa	(%rdx), %xmm0
	addq	$16, %rdx
	vpshufd	$238, %xmm0, %xmm1
	vcvtdq2pd	%xmm0, %xmm0
	vcvtdq2pd	%xmm1, %xmm1
	vaddpd	%xmm1, %xmm2, %xmm1
	vmovapd	(%rax), %xmm2
	vaddpd	-32(%rax), %xmm2, %xmm2
	vmovapd	%xmm1, 16(%rax)
	vaddpd	%xmm0, %xmm2, %xmm0
	vmovapd	%xmm0, (%rax)
	addq	$32, %rax
	cmpq	%rax, %rcx
	jne	.L2


---


### compiler : `gcc`
### title : `openmp inhibits loop vectorization`
### open_at : `2010-10-15T07:23:20Z`
### last_modified_date : `2022-03-02T02:14:29Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=46032
### status : `RESOLVED`
### tags : `missed-optimization, patch`
### component : `tree-optimization`
### version : `4.5.1`
### severity : `enhancement`
### contents :
The use of openmp to parallelize loop inhibits auto-vectorization.
This defeats all benefits of parallelization making the parallel code slower than the "sequential one".
Is it foreseen a version of openmp that preserve auto-vectorization?

Example
on
Linux  2.6.18-194.11.3.el5.cve20103081 #1 SMP Thu Sep 16 15:17:10 CEST 2010 x86_64 x86_64 x86_64 GNU/Linux
using
GNU C++ (GCC) version 4.6.0 20100408 (experimental) (x86_64-unknown-linux-gnu)
	compiled by GNU C version 4.6.0 20100408 (experimental), GMP version 4.3.2, MPFR version 2.4.2, MPC version 0.8.1
GGC heuristics: --param ggc-min-expand=30 --param ggc-min-heapsize=4096
compiling this simple example
cat openmpvector.cpp
int main()
{

 const unsigned int nEvents = 1000;
 double results[nEvents] = {0};
 double pData[nEvents] = {0};
 double coeff = 12.2;

#pragma omp parallel for
 for (int idx = 0; idx<(int)nEvents; idx++) {
   results[idx] = coeff*pData[idx];
 }

 return resultsCPU[0]; // avoid optimization of "dead" code

}

gives
g++  -O2 -fopenmp -ftree-vectorize -ftree-vectorizer-verbose=7 openmpvector.cpp

openmpvector.cpp:11: note: not vectorized: loop contains function calls or data references that cannot be analyzed
openmpvector.cpp:9: note: vectorized 0 loops in function.


---


### compiler : `gcc`
### title : `missed optimization: x86 bt/btc/bts instructions`
### open_at : `2010-10-20T05:42:00Z`
### last_modified_date : `2018-11-19T12:10:02Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=46091
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.3.5`
### severity : `enhancement`
### contents :
The following code, at least when optimizing for space, should use x86 bt/btc/bts instructions.

#include <limits.h>
#include <stddef.h>

void set_bit(size_t* a, size_t b)
{
  const unsigned c = sizeof(size_t) * CHAR_BIT;
  a[b / c] |= (((size_t)1) << (b % c));
}
 
void clear_bit(size_t* a, size_t b)
{
  const unsigned c = sizeof(size_t) * CHAR_BIT;
  a[b / c] &=  ~(((size_t)1) << (b % c));
}
 
int get_bit(size_t* a, size_t b)
{
  const unsigned c = sizeof(size_t) * CHAR_BIT;
  return !!(a[b / c] & (((size_t)1) << (b % c)));
}


---


### compiler : `gcc`
### title : `Use 16bit add instead of 32bit in thumb2`
### open_at : `2010-10-22T07:32:22Z`
### last_modified_date : `2023-05-15T05:11:59Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=46127
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.6.0`
### severity : `enhancement`
### contents :
Compile the following code with options -march=armv7-a -mthumb -Os

unsigned long compressBound (unsigned long sourceLen)
{
      return sourceLen + (sourceLen >> 12) + (sourceLen >> 14) +
                     (sourceLen >> 25) + 13;
}

GCC 4.6 generates:

compressBound:
        add     r3, r0, #13           // A
        add     r3, r3, r0, lsr #12
        add     r3, r3, r0, lsr #14
        add     r0, r3, r0, lsr #25
        bx      lr

We can change the instruction order and register a little

compressBound:
        add     r3, r0, r0, lsr #12
        add     r3, r3, r0, lsr #14
        add     r0, r3, r0, lsr #25
        add     r0, r0, #13           // B
        bx      lr

Now instruction A becomes instruction B. Instruction A is 32 bit, instruction B is 16 bit, so it becomes shorter.

Don't know how to handle it in compiler.


---


### compiler : `gcc`
### title : `Clang creates code running 1600 times faster than gcc's`
### open_at : `2010-10-26T14:27:00Z`
### last_modified_date : `2021-08-28T23:42:14Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=46186
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.5.1`
### severity : `minor`
### contents :
Created attachment 22161
C file

The attached code compiles into an executable that takes 1.6 seconds to run, when compiled with clang, it takes 0.001 seconds (both with -O2 as the only compiler option).


---


### compiler : `gcc`
### title : `pmovmskb, useless sign extension`
### open_at : `2010-10-28T08:30:29Z`
### last_modified_date : `2021-07-26T09:25:58Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=46209
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.6.0`
### severity : `enhancement`
### contents :
Hello,

$ cat movemsk.c
#include <xmmintrin.h>
typedef long unsigned int uint64_t;
uint64_t foo128(__m128i x) { return _mm_movemask_epi8(x); }
uint64_t foo64(__m64 x) { return _mm_movemask_pi8(x); }
$ /usr/local/gcc-4.6-20101026/bin/gcc  -O3 -march=native movemsk.c -S -o -
foo128:
.LFB516:
	.cfi_startproc
	pmovmskb	%xmm0, %eax
	cltq
	ret
foo64:
.LFB517:
	.cfi_startproc
	movdq2q	%xmm0, %mm0
	movq	%xmm0, -8(%rsp)
	pmovmskb	%mm0, %eax
	cltq
	ret

I won't discuss the interesting mmx code generation but to point that in both cases, as per Intel doc, there's no need to extend the result; a sign extension is even slightly more wrong.

$ /usr/local/gcc-4.6-20101026/bin/gcc  -v
Using built-in specs.
COLLECT_GCC=/usr/local/gcc-4.6-20101026/bin/gcc
COLLECT_LTO_WRAPPER=/usr/local/gcc-4.6-20101026/bin/../libexec/gcc/x86_64-unknown-linux-gnu/4.6.0/lto-wrapper
Target: x86_64-unknown-linux-gnu
Configured with: ../configure --prefix=/usr/local/gcc-4.6.0 --enable-languages=c,c++ --enable-threads=posix --disable-nls --with-system-zlib --disable-bootstrap --enable-mpfr --enable-gold --enable-lto --with-ppl --with-cloog --with-arch=native --enable-checking=release
Thread model: posix
gcc version 4.6.0 20101026 (experimental) (GCC)


---


### compiler : `gcc`
### title : `Generate indirect jump instruction on x86-64`
### open_at : `2010-10-28T22:52:15Z`
### last_modified_date : `2021-11-28T05:48:52Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=46219
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.9.1`
### severity : `enhancement`
### contents :
Is there a less brutal way to coax gcc into generating an indirect jump instruction on x86-64?

typedef void (*dispatch_t)(long offset);

dispatch_t dispatch[256];

void make_indirect_jump(long offset) {
  dispatch[offset](offset);
}

void force_use_of_indirect_jump_instruction(long offset) {
  asm ("jmp *dispatch( ,%0, 8)\n" : : "r" (offset));
  __builtin_unreachable();
}

int main() {
  return 0;
}

$ gcc-snapshot.sh -std=gnu99 -O3 use-indirect-jump-instruction.c && objdump -d -m i386:x86-64:intel a.out|less

0000000000400480 <make_indirect_jump>:
  400480:       48 8b 04 fd 20 12 60    mov    rax,QWORD PTR [rdi*8+0x601220]
  400487:       00 
  400488:       ff e0                   jmp    rax
  40048a:       66 0f 1f 44 00 00       nop    WORD PTR [rax+rax*1+0x0]

0000000000400490 <force_use_of_indirect_jump_instruction>:
  400490:       ff 24 fd 20 12 60 00    jmp    QWORD PTR [rdi*8+0x601220]
  400497:       66 0f 1f 84 00 00 00    nop    WORD PTR [rax+rax*1+0x0]
  40049e:       00 00 

This combination of inline assembly and __builtin_unreachable() is not a generally usable architecture-specific solution (there needs to be a way to ensure the results of modified input arguments end up in the same registers for the opaque tail call. It works in this case because offset remains unmodified, satisfying the ABI for dispatch_t).


---


### compiler : `gcc`
### title : `inefficient bittest code generation`
### open_at : `2010-10-30T00:17:20Z`
### last_modified_date : `2023-07-07T10:02:00Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=46235
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.6.0`
### severity : `normal`
### contents :
Test case:

int foo(int a, int x, int y)
{
   if  (a & (1 << x)) 
       return a;
   return 1;
}

Trunk gcc generates:


foo:
.LFB0:
	.cfi_startproc
	movl	%edi, %eax
	movl	%edi, %edx
	movl	%esi, %ecx
	sarl	%cl, %edx
	andl	$1, %edx
	movl	$1, %edx
	cmove	%edx, %eax
	ret


Trunk llvm (with clang) generates:

foo:
.Leh_func_begin0:
	btl	%esi, %edi
	movl	$1, %eax
	cmovbl	%edi, %eax
	ret


---


### compiler : `gcc`
### title : `Local aggregate not eliminated`
### open_at : `2010-10-30T00:37:39Z`
### last_modified_date : `2021-08-10T17:53:13Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=46236
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.6.0`
### severity : `enhancement`
### contents :
Simple Test case:

struct A {
  int a[100];
};

const struct A aa = {1,1,1};

int foo(int i)
{
    int s = 0;
    struct A a; 
 
    a = aa;
    s = a.a[i];
    if (i > 5)
       s+=a.a[i];
     
   return s;
}

// Trunk gcc generates: (O2)

foo:
.LFB0:
	.cfi_startproc
	subq	$280, %rsp
	.cfi_def_cfa_offset 288
	movl	%edi, %edx
	xorl	%eax, %eax
	leaq	-120(%rsp), %rdi
	cmpl	$6, %edx
	movl	$50, %ecx
	rep stosq
	movl	$1, -120(%rsp)
	movl	$1, -116(%rsp)
	movl	$1, -112(%rsp)
	movslq	%edx, %rax
	movl	-120(%rsp,%rax,4), %eax
	leal	(%rax,%rax), %ecx
	cmovge	%ecx, %eax
	addq	$280, %rsp
	.cfi_def_cfa_offset 8
	ret


// Trunk LLVM generates: (O2)
foo:
.Leh_func_begin0:
	movslq	%edi, %rcx
	movl	aa(,%rcx,4), %eax
	cmpl	$6, %ecx
	jl	.LBB0_2
	addl	%eax, %eax
.LBB0_2:
	ret


---


### compiler : `gcc`
### title : `Missing ifcvt`
### open_at : `2010-11-02T00:37:09Z`
### last_modified_date : `2021-11-21T07:21:47Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=46265
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.6.0`
### severity : `normal`
### contents :
Compile the following code with -O2

int *gp;
int g, g2;
int foo(int p)
{
   int t = 0;
   if (p)
      t = *gp + 1;       

   return (*gp + t);
}


Trunk gcc produces:


	movq	gp(%rip), %rax
	xorl	%edx, %edx
	movl	(%rax), %eax
	testl	%edi, %edi
	je	.L3
	leal	1(%rax), %edx
.L3:
	addl	%edx, %eax
	ret


llvm (with clang) produces:


	movq	gp(%rip), %rax
	movl	(%rax), %ecx
	leal	1(%rcx), %edx
	testl	%edi, %edi
	movl	$0, %eax
	cmovnel	%edx, %eax
	addl	%ecx, %eax
	ret


Gcc's ifcvt seems weak. If changing t=*gp + 1 to t = g then the assignment can be ifcvted by gcc.

David


---


### compiler : `gcc`
### title : `cmov not hoisted out of the loop`
### open_at : `2010-11-02T21:27:51Z`
### last_modified_date : `2021-07-20T00:45:35Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=46279
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.6.0`
### severity : `normal`
### contents :
Simple test case:

extern int gen_int(int);
extern void ref_int_p(int*);

void kernel3 ()
{
  int i;
  int j;
  int k;
  int l;
  int m;
  int a[200];

  j = gen_int (0);
  k = gen_int (0);

  for (i = 0; i < 200; i++)
    {
      if (j < k)
        a[i] = 1;
      else
        a[i] = j;
    }

  ref_int_p (&a[0]);

  return;
}


Code generated by trunk gcc at O2:

kernel3:
.LFB0:
	.cfi_startproc
	pushq	%rbx
	.cfi_def_cfa_offset 16
	.cfi_offset 3, -16
	xorl	%edi, %edi
	subq	$800, %rsp
	.cfi_def_cfa_offset 816
	call	gen_int
	xorl	%edi, %edi
	movl	%eax, %ebx
	call	gen_int
	movq	%rsp, %rdx
	leaq	800(%rsp), %rdi
	movl	$1, %esi
	.p2align 4,,10
	.p2align 3
.L4:
	cmpl	%eax, %ebx
	movl	%esi, %ecx
	cmovge	%ebx, %ecx
	movl	%ecx, (%rdx)
	addq	$4, %rdx
	cmpq	%rdi, %rdx
	jne	.L4
	movq	%rsp, %rdi
	call	ref_int_p
	addq	$800, %rsp
	.cfi_def_cfa_offset 16
	popq	%rbx
	.cfi_def_cfa_offset 8
	ret

The loop header is L4.


LLVM generates:

.Leh_func_begin0:
	pushq	%rbx
.Ltmp0:
	subq	$800, %rsp
.Ltmp1:
	xorl	%edi, %edi
	callq	gen_int
	movl	%eax, %ebx
	xorl	%edi, %edi
	callq	gen_int
	cmpl	%eax, %ebx
	movl	$1, %eax
	cmovgel	%ebx, %eax
	xorl	%ecx, %ecx
	.align	16, 0x90
.LBB0_1:
	movl	%eax, (%rsp,%rcx,4)
	incq	%rcx
	cmpq	$200, %rcx
	jne	.LBB0_1
	leaq	(%rsp), %rdi
	callq	ref_int_p
	addq	$800, %rsp
	popq	%rbx

The loop (LBB0_1) is much tighter.

David


---


### compiler : `gcc`
### title : `Inefficient unswitching (too many copies)`
### open_at : `2010-11-02T22:23:11Z`
### last_modified_date : `2021-07-26T09:34:32Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=46281
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.6.0`
### severity : `enhancement`
### contents :
Compiling the following program with -O3:

extern int gen_int(int);
extern void ref_int_p(int*);

void kernel3 ()
{
  int i;
  int j;
  int k;
  int l;
  int m;
  int a[200];

  j = gen_int (0);
  k = gen_int (0);
  l = gen_int (0);
  m = gen_int (0);

  for (i = 0; i < 200; i++)
    {
      if (j < k || j < l || j < m ) // || j << 3 || k << 4)
        a[i] = 1;
      else
        a[i] -= j;
    }

  ref_int_p (&a[0]);

  return;
}


Gcc unswitches the loop, but generate three copies of the loop -- it should only generate 2 copies.

LLVM correctly generates two copies.

David


---


### compiler : `gcc`
### title : `Lack of proper optimization for certain SSE operations, and weird behavior with similar source codes`
### open_at : `2010-11-02T23:48:22Z`
### last_modified_date : `2023-05-15T06:07:26Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=46284
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.6.0`
### severity : `enhancement`
### contents :
I am using this source code: http://pastebin.com/tMpQ2Bzv
Compile with -O3 -march=core2 -std=c++0x
Notice that the line 178 has been commented.
GCC will produce the following assembly in the final binary to initialize v1 and v2:
mov     dword ptr [esp+60h+var_30], 3F800000h
mov     dword ptr [esp+60h+var_30+4], 40000000h
mov     dword ptr [esp+60h+var_30+8], 40400000h
mov     dword ptr [esp+60h+var_30+0Ch], 40800000h
mov     dword ptr [esp+60h+var_20], 41000000h
mov     dword ptr [esp+60h+var_20+4], 40E00000h
mov     dword ptr [esp+60h+var_20+8], 40C00000h
mov     dword ptr [esp+60h+var_20+0Ch], 40A00000h

Removing the comment on that line will change the assembly and the initialization will be changed to:
movaps  xmm1, oword ptr ds:oword_47D090
movaps  xmm0, oword ptr ds:oword_47D0A0
movaps  oword ptr [esp+80h+var_50], xmm1
movaps  oword ptr [esp+80h+var_40], xmm0

which seems to make no sense.

Also, the assembly for the first case would look like this:
mov     dword ptr [esp+60h+var_30], 3F800000h
mov     dword ptr [esp+60h+var_30+4], 40000000h
mov     dword ptr [esp+60h+var_30+8], 40400000h
mov     dword ptr [esp+60h+var_30+0Ch], 40800000h
mov     dword ptr [esp+60h+var_20], 41000000h
mov     dword ptr [esp+60h+var_20+4], 40E00000h
mov     dword ptr [esp+60h+var_20+8], 40C00000h
mov     dword ptr [esp+60h+var_20+0Ch], 40A00000h
movaps  xmm0, oword ptr [esp+60h+var_30]
mov     [esp+60h+var_60], offset aResultadoFFFF ; "Resultado: %f %f %f %f\n"
addps   xmm0, oword ptr [esp+60h+var_20]
movaps  oword ptr [esp+60h+var_10], xmm0
fld     dword ptr [esp+60h+var_10+0Ch]
fstp    [esp+60h+var_44]
fld     dword ptr [esp+60h+var_10+8]
fstp    [esp+60h+var_4C]
fld     dword ptr [esp+60h+var_10+4]
fstp    [esp+60h+var_54]
fld     dword ptr [esp+60h+var_10]
fstp    [esp+60h+var_5C]
call    printf
xor     eax, eax

But the object creation for those vectors should be dropped at all, and it should work on SSE registers when possible.


---


### compiler : `gcc`
### title : `inefficient code generated for array accesses`
### open_at : `2010-11-04T19:15:02Z`
### last_modified_date : `2021-07-20T07:01:34Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=46306
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.6.0`
### severity : `enhancement`
### contents :
//Example:

int foo (int i, int *p, int t)
{
    int p2 = p[i];
    int temp = 0;
    int temp2 = 1;
    int temp3 = 4;
    if (p[i+1] > t)
     {
       temp = p2;
       temp2 = p2 + 2;
       temp3 = p2 + 3;
     }
    return p[temp] + p [temp2] + p[temp3];
}

Two problems seen the code generated by trunk gcc at -O2

1) all the shift operation are redundant and should be folded as the stride in the memory operand
2) unnecessary code duplication 

(may be handled by a pass that converts memory access with linear address into target memref in straight line code)

foo:
.LFB0:
	.cfi_startproc
	movslq	%edi, %rdi
	movl	(%rsi,%rdi,4), %eax
	cmpl	%edx, 4(%rsi,%rdi,4)
	jle	.L3
	movslq	%eax, %rdi
	leal	2(%rax), %ecx
	salq	$2, %rdi
	leal	3(%rax), %edx
	movslq	%ecx, %rcx
	movl	(%rsi,%rdi), %eax
	salq	$2, %rcx
	movslq	%edx, %rdx
	addl	(%rsi,%rcx), %eax
	salq	$2, %rdx
	addl	(%rsi,%rdx), %eax
	ret
	.p2align 4,,10
	.p2align 3
.L3:
	movl	$16, %edx
	movl	$4, %ecx
	xorl	%edi, %edi
	movl	(%rsi,%rdi), %eax
	addl	(%rsi,%rcx), %eax
	addl	(%rsi,%rdx), %eax
	ret


// The following code is generated by another compiler -- not ideal, but better:
foo:
.Leh_func_begin0:
	pushq	%rbp
.Ltmp0:
	movq	%rsp, %rbp
.Ltmp1:
	movslq	%edi, %rax
	leal	1(%rax), %ecx
	movslq	%ecx, %rcx
	cmpl	%edx, (%rsi,%rcx,4)
	jg	.LBB0_2
	movl	$1, %eax
	xorl	%ecx, %ecx
	movl	$4, %edx
	jmp	.LBB0_3
.LBB0_2:
	movslq	(%rsi,%rax,4), %rcx
	leal	3(%rcx), %eax
	movslq	%eax, %rdx
	leal	2(%rcx), %eax
	movslq	%eax, %rax
.LBB0_3:
	movl	(%rsi,%rax,4), %eax
	addl	(%rsi,%rcx,4), %eax
	addl	(%rsi,%rdx,4), %eax
	popq	%rbp
	ret


---


### compiler : `gcc`
### title : `Unnecessary movzx instruction`
### open_at : `2010-11-08T05:52:33Z`
### last_modified_date : `2021-08-15T10:29:31Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=46357
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.5.1`
### severity : `normal`
### contents :
Originally reported to the gcc-help list.

Tested with gcc Ubuntu/Linaro 4.5.1-7ubuntu2, but I get the same code with gcc 4.4.

The following C code generates assembly code with what appears to be an unnecessary call to movzx:

  char skip[] = { /* ... */ };

  int foo(const unsigned char *str, int len)
  {
    int result = 0;
    int i = 7;

    while (i < len) {
      if (str[i] == '_' && str[i-1] == 'D') {
        result |= 2;
      }
      i += skip[str[i]];
    }

    return result;
  }

0000000000000000 <foo>:
  0:   31 c0                   xor    eax,eax
  2:   83 fe 07                cmp    esi,0x7
  5:   ba 07 00 00 00          mov    edx,0x7
  a:   7f 14                   jg     20 <foo+0x20>
  c:   eb 32                   jmp    40 <foo+0x40>
  e:   66 90                   xchg   ax,ax

// Beginning of loop

 10:   0f b6 c9                movzx  ecx,cl
 13:   0f be 89 00 00 00 00    movsx  ecx,BYTE PTR [rcx+0x0]
 1a:   01 ca                   add    edx,ecx
 1c:   39 d6                   cmp    esi,edx
 1e:   7e 20                   jle    40 <foo+0x40>
 20:   4c 63 c2                movsxd r8,edx
 23:   42 0f b6 0c 07          movzx  ecx,BYTE PTR [rdi+r8*1]
 28:   80 f9 5f                cmp    cl,0x5f
 2b:   75 e3                   jne    10 <foo+0x10>

// Likely end of loop (i.e. branch above is likely taken)

 2d:   41 89 c1                mov    r9d,eax
 30:   41 83 c9 02             or     r9d,0x2
 34:   41 80 7c 38 ff 44       cmp    BYTE PTR [r8+rdi*1-0x1],0x44
 3a:   41 0f 44 c1             cmove  eax,r9d
 3e:   eb d0                   jmp    10 <foo+0x10>
 40:   f3 c3                   repz ret


The movzx on line 10 sets everything except the least-significant bit of ecx to zero.  This is unnecessary since line 23 dominates line 10, so we're guaranteed that ecx contains zeros everywhere except in its least-significant bit by the time we get to line 10.

If I change |str| in the C code to a signed char, then line 10 becomes movsx (now a necessary instruction). Perhaps this gives a hint as to where the errant instruction is coming from.


---


### compiler : `gcc`
### title : `false dependencies are computed after vectorization (#2)`
### open_at : `2010-11-09T12:35:29Z`
### last_modified_date : `2021-09-08T11:04:07Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=46391
### status : `RESOLVED`
### tags : `alias, missed-optimization`
### component : `rtl-optimization`
### version : `4.6.0`
### severity : `normal`
### contents :
Created attachment 22343
preprocessed file

When compiling function with ia64:
int nor(char* __restrict__ c, char* __restrict__ d)
{
    int i, sum = 0;
    for (i = 0; i < 256; i++)
        d[i] = c[i];
    return sum;
}

before sched1 we have:

(insn 91 329 330 4 (set (mem:V8QI (reg/v/f:DI 435 [ d ]) [0 MEM[(char *)d_43]+0 S8 A64])
        (reg:V8QI 430 [ vect_var_?25 ])) a.c:5 384 {*movv8qi_internal}
     (expr_list:REG_DEAD (reg:V8QI 430 [ vect_var_?25 ])
        (nil)))

(insn 330 91 253 4 (set (reg/f:DI 450)
        (plus:DI (reg/v/f:DI 435 [ d ])
            (const_int 8 [0x8]))) a.c:5 205 {adddi3}
     (nil))

(insn 253 330 254 4 (set (reg:V8QI 455 [ vect_var_?25 ])
        (mem:V8QI (reg:DI 449) [0 MEM[(char *)D.2084_33]+0 S8 A64])) a.c:5 384 {*movv8qi_internal}
     (nil))
 
insn 91 is a store and 253 is a load from a different location (two different
restrict pointers). These insns should not have a dependency between them but
we can see in sched1 that they do have:

;;   ======================================================
;;   -- basic block 4 from 89 to 340 -- before reload
;;   ======================================================

;;   --------------- forward dependences: ------------ 

;;   --- Region Dependences --- b 4 bb 0 
;;      insn  code    bb   dep  prio  cost   reservation
;;      ----  ----    --   ---  ----  ----   -----------
;;       89   384     4     0     1     1   2_M_only_um01	: 340 321 320 310 299 288 277 266 255 91 
;;      329   205     4     0     3     1   2_A	: 340 320 254 253 
;;       91   384     4     1     0     1   2_M_only_um23	: 340 322 321 319 310 308 299 297 288 286 277 275 266 264 255 253 
;;      330   205     4     0     2     1   2_A	: 340 322 256 255 
;;      253   384     4     2     1     1   2_M_only_um01	: 340 321 310 299 288 277 266 255 
;;      254   205     4     1     2     1   2_A	: 340 264 
;;      255   384     4     4     0     1   2_M_only_um23	: 340 321 319 310 308 299 297 288 286 277 275 266 264  

A similar bug was fixed a few months ago (http://gcc.gnu.org/bugzilla/show_bug.cgi?id=44479). Might be connected.

Using built-in specs.
COLLECT_GCC=./xgcc
Target: ia64-linux-elf
Configured with:
Thread model: single
gcc version 4.6.0 20101106 (experimental) (GCC)
COLLECT_GCC_OPTIONS='-v' '-save-temps' '-O3' '-funroll-loops' '-fdump-rtl-all' '-fsched-verbose=8'
 cc1 -E -quiet -v -iprefix /home/swproj/sw/users/eyalhar/ia64-new/gcc/../lib/gcc/ia64-linux-elf/4.6.0/ a.c -funroll-loops -fdump-rtl-all -fsched-verbose=8 -O3 -fpch-preprocess -o a.i
ignoring nonexistent directory "/home/swproj/sw/users/eyalhar/ia64-new/gcc/../lib/gcc/ia64-linux-elf/4.6.0/include"
ignoring nonexistent directory "/home/swproj/sw/users/eyalhar/ia64-new/gcc/../lib/gcc/ia64-linux-elf/4.6.0/include-fixed"
ignoring nonexistent directory "/home/swproj/sw/users/eyalhar/ia64-new/gcc/../lib/gcc/ia64-linux-elf/4.6.0/../../../../ia64-linux-elf/sys-include"
ignoring nonexistent directory "/home/swproj/sw/users/eyalhar/ia64-new/gcc/../lib/gcc/ia64-linux-elf/4.6.0/../../../../ia64-linux-elf/include"
ignoring nonexistent directory "/home/swproj/sw/users/eyalhar/ia64-new/gcc/../lib/gcc/../../lib/gcc/ia64-linux-elf/4.6.0/include"
ignoring nonexistent directory "/home/swproj/sw/users/eyalhar/ia64-new/gcc/../lib/gcc/../../lib/gcc/ia64-linux-elf/4.6.0/include-fixed"
ignoring nonexistent directory "/home/swproj/sw/users/eyalhar/ia64-new/gcc/../lib/gcc/../../lib/gcc/ia64-linux-elf/4.6.0/../../../../ia64-linux-elf/sys-include"
ignoring nonexistent directory "/home/swproj/sw/users/eyalhar/ia64-new/gcc/../lib/gcc/../../lib/gcc/ia64-linux-elf/4.6.0/../../../../ia64-linux-elf/include"
#include "..." search starts here:
#include <...> search starts here:
End of search list.
COLLECT_GCC_OPTIONS='-v' '-save-temps' '-O3' '-funroll-loops' '-fdump-rtl-all' '-fsched-verbose=8'
 cc1 -fpreprocessed a.i -quiet -dumpbase a.c -auxbase a -O3 -version -funroll-loops -fdump-rtl-all -fsched-verbose=8 -o a.s
GNU C (GCC) version 4.6.0 20101106 (experimental) (ia64-linux-elf)
        compiled by GNU C version 4.1.2 20080704 (Red Hat 4.1.2-44), GMP version 4.3.2, MPFR version 2.4.2, MPC version 0.8.1
GGC heuristics: --param ggc-min-expand=30 --param ggc-min-heapsize=4096
GNU C (GCC) version 4.6.0 20101106 (experimental) (ia64-linux-elf)
        compiled by GNU C version 4.1.2 20080704 (Red Hat 4.1.2-44), GMP version 4.3.2, MPFR version 2.4.2, MPC version 0.8.1
GGC heuristics: --param ggc-min-expand=30 --param ggc-min-heapsize=4096
Compiler executable checksum: 48128c38ed97d38ae5641e25d3ca761e
COLLECT_GCC_OPTIONS='-v' '-save-temps' '-O3' '-funroll-loops' '-fdump-rtl-all' '-fsched-verbose=8'
 as -N so -o a.o a.s


---


### compiler : `gcc`
### title : `std::get and devirtualization on non-automatic variables`
### open_at : `2010-11-16T17:57:40Z`
### last_modified_date : `2023-08-04T21:40:27Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=46507
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.6.0`
### severity : `normal`
### contents :
My understanding is that std::tuple should offer largely the same optimization opportunities as std::pair (while being more flexible).

However gcc-4.6 seems to miss some optimizations with std::tuple that it doesn't with pair.

E.g. the following code ("tp.cc"):

---- start ----
   #include <tuple>
   #include <utility>

   struct A
   {
     virtual void f () const;
   };

   void arg_tuple_test (const std::tuple<A> &t)
   {
     std::get<0>(t).f ();
   }

   void extern_tuple_test ()
   {
     extern const std::tuple<A> &t;
     std::get<0>(t).f ();
   }

   void arg_pair_test (const std::pair<A,A> &t)
   {
     t.first.f ();
   }
---- end ----

compiled with:

  g++-snapshot -std=c++0x -O2 -march=amdfam10 -S tp.cc

results in the following assembly:

   arg_tuple_test(std::tuple<A> const&):
	   movq	(%rdi), %rax
	   movq	(%rax), %rax
	   jmp	*%rax

   extern_tuple_test():
	   movq	t(%rip), %rdi
	   movq	(%rdi), %rax
	   movq	(%rax), %rax
	   jmp	*%rax

   arg_pair_test(std::pair<A, A> const&):
	   jmp	A::f() const

	   .ident	"GCC: (Debian 20101114-1) 4.6.0 20101114 (experimental) [trunk revision 166728]"


It seems like all of these functions should use a direct jump to A::f, but the tuple versions do not.

Note that when I tried this same test yesterday, on a different machine (but the same compiler version), "extern_tuple_test" (but not "arg_tuple_test") _did_ result in a direct jump to A::f!  So maybe something funny is going on...


Thanks,

-Miles


---


### compiler : `gcc`
### title : `128-bit shifts on x86_64 generate silly code unless the shift amount is constant`
### open_at : `2010-11-17T01:37:30Z`
### last_modified_date : `2021-08-23T23:08:15Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=46514
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.5.1`
### severity : `minor`
### contents :
Created attachment 22428
Preprocessed source

I'm using 4.5.1 (Fedora 14) with -O3, but -O2 does the same thing.

This really easy case:

uint64_t shift_test_31(__uint128_t x, uint32_t shift)
{
  if (shift != 31)
    __builtin_unreachable();

  return (uint64_t)(x >> shift);
}

generates:

0000000000000050 <shift_test_31>:
  50:   48 89 f8                mov    %rdi,%rax
  53:   48 0f ac f0 1f          shrd   $0x1f,%rsi,%rax
  58:   c3                      retq   
  59:   0f 1f 80 00 00 00 00    nopl   0x0(%rax)

which is entirely sensible.  But this:

uint64_t shift_test_le_31(__uint128_t x, uint32_t shift)
{
  if (shift >= 32)
    __builtin_unreachable();

  return (uint64_t)(x >> shift);
}

generates this:

0000000000000060 <shift_test_le_31>:
  60:   89 d1                   mov    %edx,%ecx
  62:   48 89 6c 24 f8          mov    %rbp,-0x8(%rsp)
  67:   48 89 f5                mov    %rsi,%rbp
  6a:   48 0f ad f7             shrd   %cl,%rsi,%rdi
  6e:   48 d3 ed                shr    %cl,%rbp
  71:   f6 c2 40                test   $0x40,%dl
  74:   48 89 5c 24 f0          mov    %rbx,-0x10(%rsp)
  79:   48 0f 45 fd             cmovne %rbp,%rdi
  7d:   48 8b 5c 24 f0          mov    -0x10(%rsp),%rbx
  82:   48 8b 6c 24 f8          mov    -0x8(%rsp),%rbp
  87:   48 89 f8                mov    %rdi,%rax
  8a:   c3                      retq   

which contains a pointless shr, test, and cmovne.  (Even if I change the __builtin_unreachable() into a real branch, I get the same code.)


---


### compiler : `gcc`
### title : `Generate complex addressing mode CMP instruction in x86-64`
### open_at : `2010-11-19T02:53:15Z`
### last_modified_date : `2021-08-13T22:58:28Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=46551
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.6.0`
### severity : `minor`
### contents :
Thanks for the improvements in GCC snapshot. Here's a simplified example where GCC does not emit the instruction cmp (%rsi,%rax,8),%rdx. Instead it generates mov (%rsi,%rax,8),%rcx; cmp %rdx,%rcx:


#include <stdint.h>

typedef struct {
  int64_t index[2];
  uint64_t cell[16];
} vm_t;

typedef void (*inst_t)(uint32_t *inst, vm_t *vm, uint64_t a);

void branch_upon_complex_compare(uint32_t *inst, vm_t *vm, uint64_t a) {
  if (vm->cell[vm->index[0] - 2] != a) {
    uint64_t dispatch = inst[-1];
    inst -= 1;
    ((inst_t) dispatch)(inst, vm, a);
  } else {
    uint64_t dispatch = inst[1];
    inst += 1;
    ((inst_t) dispatch)(inst, vm, a);
  }
}

int main() {
  return 0;
}


0000000000400480 <branch_upon_complex_compare>:
  400480:       48 8b 06                mov    (%rsi),%rax
  400483:       48 8b 0c c6             mov    (%rsi,%rax,8),%rcx
  400487:       48 39 d1                cmp    %rdx,%rcx
  40048a:       74 0c                   je     400498 <branch_upon_complex_compare+0x18>
  40048c:       8b 47 fc                mov    -0x4(%rdi),%eax
  40048f:       48 83 ef 04             sub    $0x4,%rdi
  400493:       ff e0                   jmpq   *%rax
  400495:       0f 1f 00                nopl   (%rax)
  400498:       8b 47 04                mov    0x4(%rdi),%eax
  40049b:       48 89 ca                mov    %rcx,%rdx
  40049e:       48 83 c7 04             add    $0x4,%rdi
  4004a2:       ff e0                   jmpq   *%rax
  4004a4:       66 66 66 2e 0f 1f 84    nopw   %cs:0x0(%rax,%rax,1)
  4004ab:       00 00 00 00 00 


[I found this inefficient instruction generation while trying to pinpoint an increase in runtime. I reduced the runtime using asm goto to replace the pair of instructions with a single complex addressing mode CMP instruction.]


---


### compiler : `gcc`
### title : `[11/12/13/14 Regression] PHI RTL expansion leads to CSiBE regression`
### open_at : `2010-11-19T08:26:47Z`
### last_modified_date : `2023-09-11T17:00:47Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=46555
### status : `NEW`
### tags : `missed-optimization, needs-bisection`
### component : `middle-end`
### version : `4.6.0`
### severity : `normal`
### contents :
Created attachment 22452
testcase (OpenTCP-1.0.4/icmp.c)

Hi,
the problem here seems to be worse regalloc and also
  # D.4060_6 = PHI <-1(2), -1(9), -1(11), -1(14), 0(15), -1(10)>
used to be optimized into since set of var to -1 (4 bytes), while now we
produce 3 different copies. 

Crossjumping would unify it, but very late in the game. The problem is that
ifcvt actually moves the set before conditoinal guarding the BB in question, so
the individual sets are drifted earlier to different places in the program.

Doing so might also complicate the regalloc.

Michael, perhaps we can tell out-of-ssa to unify such cases?  They are not that
infrequent (and I think old tree based out-of-ssa did that?)


---


### compiler : `gcc`
### title : `Possible enhancement for inline stringops with -Os`
### open_at : `2010-11-22T10:34:32Z`
### last_modified_date : `2021-09-11T23:43:26Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=46599
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `target`
### version : `4.5.1`
### severity : `enhancement`
### contents :
GCC 4.5.1 20100924 "-Os -minline-all-stringops"  on Core i7

int
main( int argc, char *argv[] )
{
  int i, a[256], b[256];

  for( i = 0; i < 256; ++i )  // discourage optimization
	a[i] = rand();

  memcpy( b, a, argc * sizeof(int) );

  printf( "%d\n", b[rand()] );  // discourage optimization

  return 0;
}

I wonder if its possible to improve the -Os code generation for inline stringops when
the length is known to be a multiple of 4 bytes?

That is, instead of:

	movsx   rcx, ebp    # argc
	sal rcx, 2
	rep movsb

it would be nice to see:

	movsx   rcx, ebp    # argc
	rep movsd

Note that  memcpy( b, a, 1024 ) generates:

	mov ecx, 256
	rep movsd

This is for -Os which normally emits a movs, not a loop.  The same applies to stos.

The reason I think this might be possible is this:-

Use -mstringop-strategy=rep_4byte to force the use of movsd.

For memcpy( b, a, argc * sizeof(int) ) we get:

	movsx   rcx, ebp    # argc
	sal rcx, 2
	cmp rcx, 4
	jb  .L5 #,
	shr rcx, 2
	rep movsd
.L5:


For memcpy( b, a, argc ) we get:

	movsx   rax, ebp    # argc, argc
	mov rdi, rsp    # tmp76,
	lea rsi, [rsp+1024] # tmp77,
	cmp rax, 4  # argc,
	jb  .L3 #,
	mov rcx, rax    # tmp78, argc
	shr rcx, 2  # tmp78,
	rep movsd
.L3:
	xor edx, edx    # tmp80
	test    al, 2   # argc,
	je  .L4 #,
	mov dx, WORD PTR [rsi]  # tmp82,
	mov WORD PTR [rdi], dx  #, tmp82
	mov edx, 2  # tmp80,
.L4:
	test    al, 1   # argc,
	je  .L5 #,
	mov al, BYTE PTR [rsi+rdx]  # tmp85,
	mov BYTE PTR [rdi+rdx], al  #, tmp85
.L5:

In the former case "memcpy(b, a, argc * sizeof(int))" gcc has omitted all the code do deal with 1,
2, and 3 bytes so the stringop code generation has apparently spotted that the length
is a multiple of 4 bytes.

I can see that the expression code for the length is separate from the stringop
stuff.  Though it does do the right thing with a literal.

Incidentally, for the second case, memcpy( b, a, argc ), the Visual Studio
compiler generates code like this:

	mov eax, ecx
	shr ecx, 2
	rep movsd
	mov ecx, eax
	and ecx, 3
	rep movsb

which seems cleaner (no jumps) than the GCC code, though knowing GCC there is
probably a good reason for its choice as it generally seems to have a far more
sophisticated optimizer.


---


### compiler : `gcc`
### title : `gcc 4.5: missed optimization: copy global to local, prefetch`
### open_at : `2010-12-02T09:56:15Z`
### last_modified_date : `2021-09-12T05:10:10Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=46763
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.5.1`
### severity : `enhancement`
### contents :
Created attachment 22601
gy.i.bz2

I made a simple change to OCaml's GC: copy a global to a local var (and restore before calling external function), and add a prefetchnta.
The global optimization is worth ~4% speedup, the prefetchnta alone is ~8% speedup, and both ~10% speedup.
I would expect GCC to do this optimization by itself (at least the global to register one).

Attached is a testcase to show the missed optimization, the relevant function is sweep_slice (and its manually optimized variants sweep_slice2, ...):
$ gcc-4.5 gy.i -O2 -lm
$ ./a.out
             default: 1.325195s ( 100.0%)
            glob2loc: 1.268875s ( 95.8% +- 1.024%)
         prefetchnta: 1.207342s ( 91.1% +- 0.4986%)
            prefetch: 1.277638s ( 96.4% +- 0.1179%)
glob2loc+prefetchnta: 1.199906s ( 90.5% +- 0.3629%)


default is the original function (sweep_slice), glob2loc is my manual optimization of caml_gc_sweep_hp, prefetchnta and prefetch are __builtin_prefetch added by me (non-temporal prefetch is very good here), the last one is both manual optimizations at once, resulting in a 9.5% speedup.

The attached testcase is quite large, because I dumped the sizes of all objects from the GC to have a realistic run of the GC, I also included all functions needed for the GC to run.

gcc-4.5 and gcc-4.4 both have this missed optimization, didn't try older ones.
BTW OCaml uses just -O -fno-defer-pop to compile, instead of -O2, but using -O or -O2 doesn't make much difference on this testcase, so I used -O2.

$ gcc-4.5 -v
Using built-in specs.
COLLECT_GCC=gcc-4.5
COLLECT_LTO_WRAPPER=/usr/lib/gcc/x86_64-linux-gnu/4.5.1/lto-wrapper
Target: x86_64-linux-gnu
Configured with: ../src/configure -v --with-pkgversion='Debian 4.5.1-11' --with-bugurl=file:///usr/share/doc/gcc-4.5/README.Bugs --enable-languages=c,c++,fortran,objc,obj-c++ --prefix=/usr --program-suffix=-4.5 --enable-shared --enable-multiarch --enable-linker-build-id --with-system-zlib --libexecdir=/usr/lib --without-included-gettext --enable-threads=posix --with-gxx-include-dir=/usr/include/c++/4.5 --libdir=/usr/lib --enable-nls --enable-clocale=gnu --enable-libstdcxx-debug --enable-libstdcxx-time=yes --enable-plugin --enable-gold --enable-ld=default --with-plugin-ld=ld.gold --enable-objc-gc --with-arch-32=i586 --with-tune=generic --enable-checking=release --build=x86_64-linux-gnu --host=x86_64-linux-gnu --target=x86_64-linux-gnu
Thread model: posix
gcc version 4.5.1 (Debian 4.5.1-11)

CPU: AMD Phenom(tm) II X6 1090T Processor
uname -a: Linux debian 2.6.36-phenom #107 SMP PREEMPT Sat Oct 23 10:30:01 EEST 2010 x86_64 GNU/Linux


---


### compiler : `gcc`
### title : `missed optimization of zero_extract with constant inputs`
### open_at : `2010-12-10T16:58:56Z`
### last_modified_date : `2022-12-01T00:02:56Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=46888
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.6.0`
### severity : `enhancement`
### contents :
The compiler fails to do constant folding for bit fields, at least on ARM targets, and instead builds the constant at run time.

Test case:

  struct bits
  {
     unsigned a:5;
     unsigned b:5;
     unsigned c:5;
     unsigned d:5;
  };

  struct bits
  f (unsigned int a)
  {
     struct bits bits = {0,0,0,0};
     bits.a = 1;
     bits.b = 2;
     bits.c = 3;
     bits.d = a;
     return bits;
  }

Output, compiled for ARM with "-O2 -mcpu=cortex-a8 -mthumb":
        movs    r2, #1
        movs    r3, #0
        bfi     r3, r2, #0, #5
        movs    r2, #2
        bfi     r3, r2, #5, #5
        movs    r2, #3
        bfi     r3, r2, #10, #5
        bfi     r3, r0, #15, #5
        mov     r0, r3
        bx      lr


---


### compiler : `gcc`
### title : `Unnecessary ZERO_EXTEND`
### open_at : `2010-12-14T17:34:29Z`
### last_modified_date : `2023-05-20T01:57:12Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=46943
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.6.0`
### severity : `enhancement`
### contents :
In http://blog.regehr.org/archives/320 Example 4
unsigned long long v;
unsigned short
foo (signed char x, unsigned short y)
{
  v = (unsigned long long) y;
  return (unsigned short) ((int) y / 3);
}
we emit a redundant zero-extension:
        movzwl  %si, %eax
        movq    %rax, v(%rip)
        movzwl  %si, %eax
        imull   $43691, %eax, %eax
        shrl    $17, %eax
        ret
The reason why the second movzwl %si, %eax wasn't CSEd with the first one is
because the first one is (set (reg:DI reg1) (zero_extend:DI (reg:HI reg2))
while the second one is (set (reg:SI reg3) (zero_extend:SI (reg:HI reg2))
Wonder if we can't teach CSE to optimize it (say that reg3 is actually
(subreg:SI (reg:DI reg1) 0), or if e.g. one of the zee/see passes (implicit-zee e.g.) couldn't handle such cases.  Combiner can't do anything here, as there is no data dependency, so try_combine won't see them together.


---


### compiler : `gcc`
### title : `http://blog.regehr.org/archives/320 Example 1`
### open_at : `2010-12-15T14:47:15Z`
### last_modified_date : `2021-08-10T17:47:58Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=46957
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.6.0`
### severity : `enhancement`
### contents :
void foo (void);
long a, b;
void
foo (void)
{
  int i;

  b = -1L;
  i = 0;
  while (i < 63)
    {
      b *= 2L;
      i++;
    }
  a = -(b + 1L);
}

doesn't have the loop optimized out, as we don't have {-1L, *, 2}_1 style chrecs, only , +, style.  I wonder if we couldn't for << or multiplication by power of two express {-1L, *, 2}_1 instead as -1L << ({0, +, 1}_1), or
for other multiplication, say {a, *, b}_1, as a * pow (b, {0, +, 1}_1) and use that in compute_overall_effect_of_inner_loop etc. to sccp it.

Of course only if the resulting expression is cheap enough.


---


### compiler : `gcc`
### title : `Replace 32 bit instructions with 16 bit instructions in thumb2`
### open_at : `2010-12-16T00:39:36Z`
### last_modified_date : `2023-05-15T05:19:08Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=46975
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.6.0`
### severity : `enhancement`
### contents :
Compile the following c code with options -march=armv7-a -mthumb -Os

int gzeof (int s)
{
    return s == 1;
}

GCC 4.6 generates:

00000000 <gzeof>:
   0:	f1a0 0301 	sub.w	r3, r0, #1	// A
   4:	4258      	negs	r0, r3
   6:	eb40 0003 	adc.w	r0, r0, r3      // B
   a:	4770      	bx	lr

Notice that instructions A and B are 32 bits, we can change them to subs and adcs so both will be 16 bits.

The code sequence is generated by the following peephole2

 8731 ;; Attempt to improve the sequence generated by the compare_scc splitters
 8732 ;; not to use conditional execution.
 8733 (define_peephole2
 8734   [(set (reg:CC CC_REGNUM)
 8735         (compare:CC (match_operand:SI 1 "register_operand" "")
 8736                     (match_operand:SI 2 "arm_rhs_operand" "")))
 8737    (cond_exec (ne (reg:CC CC_REGNUM) (const_int 0))
 8738               (set (match_operand:SI 0 "register_operand" "") (const_int 0)))
 8739    (cond_exec (eq (reg:CC CC_REGNUM) (const_int 0))
 8740               (set (match_dup 0) (const_int 1)))
 8741    (match_scratch:SI 3 "r")]
 8742   "TARGET_32BIT"
 8743   [(set (match_dup 3) (minus:SI (match_dup 1) (match_dup 2)))
 8744    (parallel
 8745     [(set (reg:CC CC_REGNUM)
 8746           (compare:CC (const_int 0) (match_dup 3)))
 8747      (set (match_dup 0) (minus:SI (const_int 0) (match_dup 3)))])
 8748    (set (match_dup 0)
 8749         (plus:SI (plus:SI (match_dup 0) (match_dup 3))
 8750                  (geu:SI (reg:CC CC_REGNUM) (const_int 0))))])
 8751 

We should change the new instructions to use subs and adcs.


---


### compiler : `gcc`
### title : `missed optimization in length comparison`
### open_at : `2010-12-18T16:10:51Z`
### last_modified_date : `2023-09-21T14:15:54Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=47004
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.6.0`
### severity : `enhancement`
### contents :
Created attachment 22811
Preprocessed source to reproduce

The attached C test case shows missed optimization, where lenzero could be optimized to generate the same code as lenzero2. This pattern is very common in Ada, where the 'Length attribute for arrays expands to the same code as that for len. As this is all simple integer code without any aliasing issues, I have some hope that GCC can do better here.

Regards,
  -Geert 

cat lenzero.c && gcc -O3 -fomit-frame-pointer -save-temps -c lenzero.c && otool -tv lenzero.o
int len(int f, int l) {
 return l < f ? 0 : l - f + 1;
}

int lenzero(int f, int l) {
 return len(f, l) == 0;
}

int lenzero2(int f, int l) {
 return l < f;
}

lenzero.o:
(__TEXT,__text) section
_len:
0000000000000000	xorl	%eax,%eax
0000000000000002	cmpl	%edi,%esi
0000000000000004	jl	0x0000000b
0000000000000006	subl	%edi,%esi
0000000000000008	leal	0x01(%rsi),%eax
000000000000000b	repz/ret
000000000000000d	nop
000000000000000e	nop
_lenzero:
0000000000000010	cmpl	%esi,%edi
0000000000000012	movl	$0x00000001,%eax
0000000000000017	jg	0x00000023
0000000000000019	subl	%edi,%esi
000000000000001b	xorl	%eax,%eax
000000000000001d	cmpl	$0xff,%esi
0000000000000020	sete	%al
0000000000000023	repz/ret
0000000000000025	nop
0000000000000026	nopw	%cs:0x00000000(%rax,%rax)
_lenzero2:
0000000000000030	xorl	%eax,%eax
0000000000000032	cmpl	%edi,%esi
0000000000000034	setl	%al
0000000000000037	ret


---


### compiler : `gcc`
### title : `Missed optimization: x86-64 prologue not deleted`
### open_at : `2010-12-19T02:43:02Z`
### last_modified_date : `2021-08-23T23:09:23Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=47010
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.5.1`
### severity : `normal`
### contents :
Created attachment 22818
pre-processed bzipped source code

The following code is generated by g++ 4.5.1 on an x86-64 architecture (Mac OS 10.6). This is a static function where g++ may even have modified the argument list. I believe the three instructions "pushq", "movq", and "leave" are not necessary. This routine is called in a compute-intensive inner loop that has problems fitting into the level 1 instruction cache.

The disassembled routine is:

__ZL20PDstandardNth11_implPKdll.clone.1:
0000000000000140        pushq   %rbp
0000000000000141        movupd  0x10(%rdi),%xmm3
0000000000000146        movupd  0xf0(%rdi),%xmm0
000000000000014b        movupd  0x08(%rdi),%xmm2
0000000000000150        addpd   %xmm3,%xmm0
0000000000000154        movupd  0xf8(%rdi),%xmm1
0000000000000159        movq    %rsp,%rbp
000000000000015c        addpd   %xmm2,%xmm1
0000000000000160        mulpd   0x000a0578(%rip),%xmm1
0000000000000168        addpd   %xmm0,%xmm1
000000000000016c        movupd  (%rdi),%xmm0
0000000000000170        mulpd   0x000a0578(%rip),%xmm0
0000000000000178        leave
0000000000000179        addpd   %xmm1,%xmm0
000000000000017d        ret

The original function is defined as:

static CCTK_REAL_VEC PDstandardNth11_impl(CCTK_REAL const* restrict const u, ptrdiff_t const dj, ptrdiff_t const dk) __attribute__((pure)) __attribute__((noinline)) __attribute__((unused));

static CCTK_REAL_VEC PDstandardNth11_impl(CCTK_REAL const* restrict const u, ptrdiff_t const dj, ptrdiff_t const dk)
{ return kmadd(ToReal(30),vec_loadu_maybe3(0,0,0,(u)[(0)+dj*(0)+dk*(0)]),kmadd(ToReal(-16),kadd(vec_loadu_maybe3(-1,0,0,(u)[(-1)+dj*(0)+dk*(0)]),vec_loadu_maybe3(1,0,0,(u)[(1)+dj*(0)+dk*(0)])),kadd(vec_loadu_maybe3(-2,0,0,(u)[(-2)+dj*(0)+dk*(0)]),vec_loadu_maybe3(2,0,0,(u)[(2)+dj*(0)+dk*(0)])))); }

where CCTK_REAL is double, and CCTK_REAL_VEC is __m128d, the SSE2 vector of doubles. The function body contains macros that translate directly to Intel SSE2 vector instructions.

The code was compiled with gcc 4.5.1 with the options

g++-mp-4.5 -g3 -m128bit-long-double -march=native -std=gnu++0x -O3 -funsafe-loop-optimizations -fsee -ftree-loop-linear -ftree-loop-im -fivopts -fvect-cost-model -funroll-loops -funroll-all-loops -fvariable-expansion-in-unroller -fprefetch-loop-arrays -ffast-math -fassociative-math -freciprocal-math -fno-trapping-math -fexcess-precision=fast -fopenmp -Wall -Wshadow -Wpointer-arith -Wcast-qual -Wcast-align -Woverloaded-virtual 

I attach the complete pre-processed and bzipped source code. The source code itself is auto-generated.


---


### compiler : `gcc`
### title : `loop distribution has problems on sane testcases`
### open_at : `2010-12-21T19:19:12Z`
### last_modified_date : `2021-12-26T12:35:34Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=47033
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `unknown`
### severity : `normal`
### contents :
The following patch:
Index: predict.c
===================================================================
--- predict.c   (revision 168047)
+++ predict.c   (working copy)
@@ -126,7 +126,7 @@ maybe_hot_frequency_p (int freq)
   if (node->frequency == NODE_FREQUENCY_EXECUTED_ONCE
       && freq <= (ENTRY_BLOCK_PTR->frequency * 2 / 3))
     return false;
-  if (freq < BB_FREQ_MAX / PARAM_VALUE (HOT_BB_FREQUENCY_FRACTION))
+  if (freq < ENTRY_BLOCK_PTR->frequency / PARAM_VALUE
(HOT_BB_FREQUENCY_FRACTION))
     return false;
   return true;
 }
makes the testcase gcc.dg/tree-ssa/ldist-pr45948.c  to fail.

The testcase seems to test if the loop is converted to memsets. The problem is that with the patch above the code is considered hot and loop gets header copied as a result the code in loop distribution seems confused.
Profile info is wrong and one copy of loop stays in the code.


---


### compiler : `gcc`
### title : `code size opportunity for boolean expression evaluation`
### open_at : `2010-12-31T08:05:42Z`
### last_modified_date : `2021-07-29T22:40:06Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=47133
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.6.0`
### severity : `normal`
### contents :
Compile the following code with options -march=armv7-a -mthumb -Os

struct S
{
  int f1, f2;
};

int t04(int x, struct S* p)
{
  return p->f1 == 9 && p->f2 == 0;
}

GCC 4.6 generates:

t04:
	ldr	r3, [r1, #0]
	cmp	r3, #9             // A
	bne	.L3
	ldr	r0, [r1, #4]
	rsbs	r0, r0, #1
	it	cc
	movcc	r0, #0
	bx	lr                 // C
.L3:
	movs	r0, #0             // B
	bx	lr


Instruction B can be moved before instruction A, and instruction C can be removed. 

t04:
	ldr	r3, [r1, #0]
        movs    r0, #0
	cmp	r3, #9            
	bne	.L3
	ldr	r0, [r1, #4]
	rsbs	r0, r0, #1
	it	cc
	movcc	r0, #0
.L3:
	bx	lr

When compiled to arm instructions, it has the same problem.

It should be enabled for code size optimization only because it may execute one more instruction run time.

Looks like an if-conversion opportunity.


---


### compiler : `gcc`
### title : `-O2 moves invariant address load INTO loop`
### open_at : `2011-01-06T09:33:04Z`
### last_modified_date : `2021-07-29T22:47:21Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=47186
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `target`
### version : `4.5.1`
### severity : `normal`
### contents :
gcc -O1 try.c -S -masm=intel -o try.s

In the example below, the address load to esi for the movsd is moved into the loop when -O2 is used.  With -O1 its outside the loop.

Perhaps this is something to do with scheduling?  I tried with various x86 targets and it always happened, although the position of the address load within the loop changed between atom and core2 for example.

--------------------------------------
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int mike[100], joe[100];

int main( int argc, char *argv[] )
{
  int i;
  for( i = 0; i < 100; ++i )
    mike[i] = rand();
  memcpy( joe, mike, sizeof(joe) );
}
--------------------------------------
Compile with -O1 produces ...

.L2:
    call    rand
    mov DWORD PTR mike[0+ebx*4], eax
    add ebx, 1
    cmp ebx, 100
    jne .L2
    mov edi, OFFSET FLAT:joe
    mov esi, OFFSET FLAT:mike
    mov ecx, 100
    rep movsd

Now repeat with -O2, and esi is loaded within the loop

.L2:
    call    rand
    mov esi, OFFSET FLAT:mike
    mov DWORD PTR mike[0+ebx*4], eax
    add ebx, 1
    cmp ebx, 100
    jne .L2
    mov ecx, ebx
    mov edi, OFFSET FLAT:joe
    rep movsd


---


### compiler : `gcc`
### title : `GCC emits optimized out noinline function`
### open_at : `2011-01-07T11:01:54Z`
### last_modified_date : `2021-08-30T04:54:33Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=47205
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.6.0`
### severity : `enhancement`
### contents :
$ gcc -O2 -flto -fwhole-program main.c foo.c
$ nm a.out | grep foo
08048380 t foo.1988

========= main.c ========
extern int foo(void);

int main(void)
{
  return foo() * 0;
}
=========================

========= foo.c =========
__attribute__((noinline))
int foo(void)
{
  return 0x2a;
}
=========================


---


### compiler : `gcc`
### title : `Conditional jump to tail function is not generated`
### open_at : `2011-01-11T00:45:23Z`
### last_modified_date : `2023-05-13T17:51:07Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=47253
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.6.0`
### severity : `enhancement`
### contents :
I hope the summary is descriptive enough.
Take the following code:

----- testcase.c -----
void bar(void);

void foo(int c)
{
	if (c) bar();
}
----------------------

With -O3, gcc generated this code:
foo:
.LFB0:
	.cfi_startproc
	test	edi, edi	# c
	jne	.L4	#,
	rep
	ret
	.p2align 4,,10
	.p2align 3
.L4:
	jmp	bar	#
	.cfi_endproc


and with -Os:
foo:
.LFB0:
	.cfi_startproc
	test	edi, edi	# c
	je	.L1	#,
	jmp	bar	#
.L1:
	ret
	.cfi_endproc


while better would be:
foo:
	test	edi, edi
	jne	.L1
	rep # only without -Os
	ret

I tested 3.3.6, 3.4.6, 4.4.5, 4.6.0, neither generates the "better" code.


---


### compiler : `gcc`
### title : `Missed CSE optimization with inline functions, and __attribute__((const))`
### open_at : `2011-01-11T02:35:43Z`
### last_modified_date : `2021-11-28T04:54:57Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=47255
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.5.2`
### severity : `enhancement`
### contents :
Created attachment 22942
Test program exhibiting missed optimization

Using gcc 4.5.2 on gentoo (or gcc 4.1.2 on RHEL 5.5), gcc fails to optimize a case where a const function is called in a const way inside a loop, if the const function is elgible for inlining.

The test case should print three lines if it succeeds.  In fact, the "World" line is printed once per loop iteration.

How-To-Repeat:

Compile the attach test-case with -O3 or "-O -finline-small-functions -finline-functions" -- more than three lines are printed.  Compile with -O2, the correct number of lines (three) for full optimization are printed.

Release:
----------------------------------------------------------------------
Using built-in specs.
Target: x86_64-redhat-linux
Configured with: ../configure --prefix=/usr --mandir=/usr/share/man --infodir=/usr/share/info --enable-shared --enable-threads=posix --enable-checking=release --with-system-zlib --enable-__cxa_atexit --disable-libunwind-exceptions --enable-libgcj-multifile --enable-languages=c,c++,objc,obj-c++,java,fortran,ada --enable-java-awt=gtk --disable-dssi --enable-plugin --with-java-home=/usr/lib/jvm/java-1.4.2-gcj-1.4.2.0/jre --with-cpu=generic --host=x86_64-redhat-linux
Thread model: posix
gcc version 4.1.2 20080704 (Red Hat 4.1.2-48)
----------------------------------------------------------------------
Using built-in specs.
COLLECT_GCC=/usr/x86_64-pc-linux-gnu/gcc-bin/4.5.2/gcc
COLLECT_LTO_WRAPPER=/usr/libexec/gcc/x86_64-pc-linux-gnu/4.5.2/lto-wrapper
Target: x86_64-pc-linux-gnu
Configured with: /n/startide/proj/startide/var-tmp/portage/sys-devel/gcc-4.5.2/work/gcc-4.5.2/configure --prefix=/usr --bindir=/usr/x86_64-pc-linux-gnu/gcc-bin/4.5.2 --includedir=/usr/lib/gcc/x86_64-pc-linux-gnu/4.5.2/include --datadir=/usr/share/gcc-data/x86_64-pc-linux-gnu/4.5.2 --mandir=/usr/share/gcc-data/x86_64-pc-linux-gnu/4.5.2/man --infodir=/usr/share/gcc-data/x86_64-pc-linux-gnu/4.5.2/info --with-gxx-include-dir=/usr/lib/gcc/x86_64-pc-linux-gnu/4.5.2/include/g++-v4 --host=x86_64-pc-linux-gnu --build=x86_64-pc-linux-gnu --disable-altivec --disable-fixed-point --without-ppl --without-cloog --disable-lto --enable-nls --without-included-gettext --with-system-zlib --disable-werror --enable-secureplt --enable-multilib --enable-libmudflap --disable-libssp --enable-libgomp --enable-cld --with-python-dir=/share/gcc-data/x86_64-pc-linux-gnu/4.5.2/python --enable-checking=release --disable-libgcj --enable-languages=c,c++ --enable-shared --enable-threads=posix --enable-__cxa_atexit --enable-clocale=gnu --with-bugurl=http://bugs.gentoo.org/ --with-pkgversion='Gentoo 4.5.2 p1.0, pie-0.4.5'
Thread model: posix
gcc version 4.5.2 (Gentoo 4.5.2 p1.0, pie-0.4.5)
----------------------------------------------------------------------


---


### compiler : `gcc`
### title : `unnecessary versioning in the vectorizer, not implemented affine-affine test`
### open_at : `2011-01-18T10:50:46Z`
### last_modified_date : `2021-12-22T08:44:13Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=47341
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.6.0`
### severity : `enhancement`
### contents :
with current trunk:

> cat test.f90
   SUBROUTINE HARD_NN_4_4_4_5_1_2_4(C,A,B)
      REAL(KIND=8) :: C(4,*)
      REAL(KIND=8) :: B(4,*), A(4,*)
      INTEGER ::i,j,l
      l=           1
      DO j=           1 ,           4 ,           2
      DO i=           1 ,           4 ,           1
        C(i+0,j+0)=C(i+0,j+0)+A(i+0,l+0)*B(l+0,j+0)
        C(i+0,j+0)=C(i+0,j+0)+A(i+0,l+1)*B(l+1,j+0)
        C(i+0,j+0)=C(i+0,j+0)+A(i+0,l+2)*B(l+2,j+0)
        C(i+0,j+0)=C(i+0,j+0)+A(i+0,l+3)*B(l+3,j+0)
        C(i+0,j+1)=C(i+0,j+1)+A(i+0,l+0)*B(l+0,j+1)
        C(i+0,j+1)=C(i+0,j+1)+A(i+0,l+1)*B(l+1,j+1)
        C(i+0,j+1)=C(i+0,j+1)+A(i+0,l+2)*B(l+2,j+1)
        C(i+0,j+1)=C(i+0,j+1)+A(i+0,l+3)*B(l+3,j+1)
      ENDDO
      ENDDO
    END SUBROUTINE

> gfortran-trunk -c -O2 -fno-unroll-loops -ftree-vectorize -ftree-vectorizer-verbose=1 -march=core2 -msse4.2 test.f90

test.f90:7: note: created 1 versioning for alias checks.

test.f90:7: note: LOOP VECTORIZED.
test.f90:1: note: vectorized 1 loops in function.

The compiler should not need to generate various version of these loops. With the bounds info provided, nothing can alias (I think).


---


### compiler : `gcc`
### title : `avoid goto table to reduce code size when optimized for size`
### open_at : `2011-01-20T08:53:52Z`
### last_modified_date : `2021-11-28T04:47:22Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=47373
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.6.0`
### severity : `enhancement`
### contents :
Created attachment 23040
modified testcase

When I compiled the infback.c from zlib 1.2.5 with options -march=armv7-a -mthumb -Os, gcc 4.6 generates following code for a large switch statement:

	subs	r3, r3, #11
	cmp	r3, #18
	bhi	.L16
	tbh	[pc, r3, lsl #1]
.L23:
	.2byte	(.L17-.L23)/2
	.2byte	(.L16-.L23)/2
	.2byte	(.L18-.L23)/2
	.2byte	(.L16-.L23)/2
	.2byte	(.L16-.L23)/2
	.2byte	(.L154-.L23)/2
	.2byte	(.L16-.L23)/2
	.2byte	(.L16-.L23)/2
	.2byte	(.L16-.L23)/2
	.2byte	(.L20-.L23)/2
	.2byte	(.L16-.L23)/2
	.2byte	(.L16-.L23)/2
	.2byte	(.L16-.L23)/2
	.2byte	(.L16-.L23)/2
	.2byte	(.L16-.L23)/2
	.2byte	(.L16-.L23)/2
	.2byte	(.L16-.L23)/2
	.2byte	(.L21-.L23)/2
	.2byte	(.L121-.L23)/2
.L17:

GCC generates a goto table for 19 cases. The table and the instructions which manipulate it occupies 19*2 + 10 = 48 bytes.

Actually most of the targets in the table are same. There are only 6 targets other than .L16. So if we generate a sequence of cmp & br instructions, we need only 6 cmp&br and one br to default, that's only 4*6+2=26 bytes.

When I randomly modified the source code, gcc sometimes generate the absolute address in the goto table, double the table size, make result worse. The modified source code is attached.


---


### compiler : `gcc`
### title : `Alignment of array element is not optimal in AVX mode due to use of TARGET_MEM_REFs`
### open_at : `2011-01-21T13:57:30Z`
### last_modified_date : `2021-09-12T05:41:45Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=47397
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.6.0`
### severity : `normal`
### contents :
In

---
double a[NUM], b[NUM];

void foo()
{
   for (i = 0; i < N; i++)
   {
      b[i] = a[i+2] * 10.0;
   }
}
---

both "a" and "b" are aligned at 32byte/256bits. However, RTL dump from
"-O3 -mavx" shows that alignment of a[i+2] is 64bits instead of 128bits
as expected:

(insn 39 38 40 4 (set (mem:V4DF (plus:DI (reg/f:DI 95)
                (reg:DI 80 [ ivtmp.21 ])) [2 MEM[symbol: b, index: ivtmp.21_20,
offset: 16B]+0 S32 A64])
        (unspec:V4DF [
                (reg:V4DF 93)
            ] UNSPEC_MOVU)) align.c:64 -1
     (nil))


---


### compiler : `gcc`
### title : `Constant Propagation and Virtual Function Tables`
### open_at : `2011-01-22T17:22:29Z`
### last_modified_date : `2019-10-05T04:07:28Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=47413
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.5.2`
### severity : `enhancement`
### contents :
The tested GCC version does not fully use its knowledge about (constant) function pointers. In some cases (with LTO), this occurs frequently. The following example should illustrate it and it's relevance:


	#include <stdio.h>
	#include <stdlib.h>


	/* the types */

	struct obj;

	struct vtab {
		int (*f)(struct obj *obj);
	};

	struct obj {
		const struct vtab *vtab;
	};


	static int f1337(struct obj *obj)
	{
		return 1337;
	}

	static const struct vtab vtab1337 = {
		.f = f1337
	};


	/* the functions */

	static struct obj *create()
	{
		struct obj *obj;

		if (!(obj = malloc(sizeof(struct obj)))) {
			return NULL;
		}

		obj->vtab = &vtab1337;

		return obj;
	}

	static int call(struct obj *obj)
	{
		return obj->vtab->f(obj);
	}


	/* the program */

	int main()
	{
		struct obj *obj;

		if (!(obj = create())) {
			return 0;
		}

		printf("%d\n", call(obj));
		return 1;
	}

When compiling with -O3, I'd expect GCC to just pass 1337 to printf, as it does without a virtual function table. Instead, it uses its knowledge about obj to call vtab1337.f(), as in

	call *vtab1337

but doesn't simplify *vtab1337 to f1337, or the entire call to 1337.


---


### compiler : `gcc`
### title : `STL size() == 0 does unnecessary shift`
### open_at : `2011-02-01T18:22:45Z`
### last_modified_date : `2022-11-27T06:32:21Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=47579
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.6.0`
### severity : `enhancement`
### contents :
Consider this C++ code:

#include <vector>
extern void b1(), b2();
void foo(const std::vector<int>& v) { if (v.size() == 0) b1(); else b2(); }

When I compile it with current mainline with -O2 on x86_64, I get this:

        movq    8(%rdi), %rax
        subq    (%rdi), %rax
        sarq    $2, %rax
        testq   %rax, %rax
        ...

That sarq instruction is useless.  We know that the two values being subtracted are both aligned pointers, so we should know that the two least significant bits of the result are zero.  And that should be enough to let us know that we don't need to shift before comparing for equality with zero.


---


### compiler : `gcc`
### title : `Redundant NULL check`
### open_at : `2011-02-09T23:44:41Z`
### last_modified_date : `2021-07-26T09:49:17Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=47673
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.6.0`
### severity : `normal`
### contents :
Consider this C code:

struct s1 { int x; };
struct s2 { struct s1 *p1; };
extern void f1(struct s1 *);
static inline void inline_func(struct s1 *p1) { if (p1) f1 (p1); }
void global_function(struct s2 *p2) {
  if (p2->p1 != 0 && p2->p1 != (struct s1 *) -1)
    inline_func(p2->p1);
}

When I compile this with -O2 with current mainline on x86_64, I get this:

	movq	(%rdi), %rdi
	leaq	-1(%rdi), %rax
	cmpq	$-3, %rax
	ja	.L1
	testq	%rdi, %rdi
	je	.L1
	jmp	f1

If %rdi is 0, %rax will be -1, and the ja branch will be taken.  Therefore, the je following the testq %rdi,%rdi will never be taken.  The test and branch should be eliminated.


---


### compiler : `gcc`
### title : `[missed optimization] use of btr (bit test and reset)`
### open_at : `2011-02-16T18:43:57Z`
### last_modified_date : `2022-10-22T22:32:02Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=47769
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.5.0`
### severity : `enhancement`
### contents :
The code:

tmp &= ~(1 << bit);

gets translated to

actual shift, not, and and instructions. Instead GCC could emit one btr instruction (which modifies the flags - unwanted but acceptable):

btr %[bit], %[tmp]

The btr instruction has a latency of 1 cycle and throughput of 0.5 cycles on all recent Intel CPUs and thus outperforms the shift + not + and combination.

Rationale:
I make use of this pattern for iteration over a bitmask. I use bsf (_bit_scan_forward(bitmask)) to find the lowest set bit. To find the next one I have to mask off the last found bit and currently have to use inline assembly to get a btr instruction there. Alternatively an intrinsic for btr and friends might make sense.


---


### compiler : `gcc`
### title : `avoid if-conversion if the conditional instructions and following conditional branch has the same condition`
### open_at : `2011-02-21T09:58:14Z`
### last_modified_date : `2021-06-03T02:35:20Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=47831
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.6.0`
### severity : `enhancement`
### contents :
Created attachment 23423
testcase

Compile the attached source code with options -march=armv7-a -mthumb -Os, GCC 4.6 generates

ras_validate:
	@ args = 0, pretend = 0, frame = 8
	@ frame_needed = 0, uses_anonymous_args = 0
	push	{r0, r1, r4, r5, r6, lr}
	add	r4, sp, #4
	movs	r2, #4
	mov	r1, r4
	mov	r5, r0
	bl	foo
	cmp	r0, #0
	it	ge        // A
	movge	r6, r0    // B
	bge	.L3       // C
	b	.L7       // D
.L4:
	adds	r3, r6, r4
	mov	r0, r5
	subs	r6, r6, #1
	ldrb	r1, [r3, #-1]	@ zero_extendqisi2
	bl	bar
	adds	r3, r0, #1
	beq	.L2
.L3:
	cmp	r6, #0
	bne	.L4
	mov	r0, r6
	b	.L2
.L7:
	mov	r0, #-1
.L2:
	pop	{r2, r3, r4, r5, r6, pc}

Instruction sequence ABCD can be replaced with

       blt    .L7
       mov    r6, r0
       b      .L3

In both cases (lt or ge) the executed instructions is not longer than original code. So it's shorter and faster.


---


### compiler : `gcc`
### title : `missed cbnz optimization`
### open_at : `2011-02-23T09:30:00Z`
### last_modified_date : `2021-09-09T23:25:30Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=47855
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.6.0`
### severity : `enhancement`
### contents :
Created attachment 23440
testcase

Compile the attached source code with options -march=armv7-a -mthumb -Os, GCC 4.6 generates 

pnm_gethdr:
	@ args = 0, pretend = 0, frame = 8
	@ frame_needed = 0, uses_anonymous_args = 0
	push	{r0, r1, r2, r4, r5, lr}
	mov	r5, r0
	mov	r4, r1
	bl	foo2
	cmp	r0, #0                // A
	bne	.L13                  // B
	adds	r1, r4, #4
	mov	r0, r5
	bl	foo3
	cmp	r0, #0                // C
	bne	.L13                  // D
	add	r1, r4, #8
	mov	r0, r5
	bl	foo1
	cbnz	r0, .L13              // E
	ldr	r0, [r4, #0]
	bl	pnm_type
	cmp	r0, #2
	beq	.L3
	mov	r0, r5
	add	r1, sp, #4
	bl	pnm_getsintstr
	cbz	r0, .L4
	b	.L13
.L3:
	movs	r3, #1
	str	r3, [sp, #4]
.L4:
	ldr	r3, [sp, #4]
	cmp	r3, #0
	bge	.L5
	negs	r3, r3
	str	r3, [r4, #16]
	movs	r3, #1
	b	.L14
.L5:
	str	r3, [r4, #16]
	movs	r3, #0
.L14:
	strb	r3, [r4, #20]
	ldr	r0, [r4, #0]
	bl	pnm_type
	cmp	r0, #0
	beq	.L8
	blt	.L7
	cmp	r0, #2
	bgt	.L7
	movs	r3, #1
	movs	r0, #0
	str	r3, [r4, #12]
	b	.L2
.L8:
	movs	r3, #3
	str	r3, [r4, #12]
	b	.L2
.L7:
	bl	abort
.L13:
	mov	r0, #-1
.L2:
	pop	{r1, r2, r3, r4, r5, pc}

The branch distance of cbz/cbnz is 126 bytes. The size of the whole function is 124 bytes. So instructions AB and CD can be replaced by

     cbnz    r0,  .L13

same as instruction E.


---


### compiler : `gcc`
### title : `is vectorization of "condition in nested loop" supported`
### open_at : `2011-02-23T14:41:37Z`
### last_modified_date : `2021-08-16T04:39:21Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=47860
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.6.0`
### severity : `normal`
### contents :
In
http://gcc.gnu.org/projects/tree-ssa/vectorization.html#nested
I read that "condition in nested loop" was committed in the main line in 2009-12-03
for 4.6.0 I still get it non vectorize.
what is the real situation of the feature described ion the page above?

 for instance

nestedCond.cc:2: note: not vectorized: control flow in loop.
nestedCond.cc:7: note: not vectorized: data ref analysis failed next_a_22 = *D.2335_21;

full details below

cat nestedCond.cc
void nestedCond( double * __restrict__ x_in,  double * __restrict__ x_out,  double * __restrict__ a,  double * __restrict__ c, unsigned int M, unsigned int N) {   
for (unsigned int j = 0; j < M; j++)
    {
      double x = x_in[j];
      double curr_a = a[0];

      for (unsigned int i = 0; i < N; i++)
        {
          double next_a = a[i+1];
          curr_a = x > c[i] ? curr_a : next_a;
        }

      x_out[j] = curr_a;
    }
}

 g++ $CXXFLAGS $OPTFLAGS -v -c nestedCond.cc
Using built-in specs.
COLLECT_GCC=g++
COLLECT_LTO_WRAPPER=/usr/local/libexec/gcc/x86_64-unknown-linux-gnu/4.6.0/lto-wrapper
Target: x86_64-unknown-linux-gnu
Configured with: ./configure --enable-gold=yes --enable-lto --with-fpmath=avx
Thread model: posix
gcc version 4.6.0 20110205 (experimental) (GCC) 
COLLECT_GCC_OPTIONS='-O2' '-std=gnu++0x' '-mavx' '-mtune=corei7-avx' '-ftree-vectorize' '-ftree-vectorizer-verbose=7' '-pthread' '-fPIC' '-fassociative-math' '-freciprocal-math' '-fno-math-errno' '-fno-signed-zeros' '-fno-trapping-math' '-ffinite-math-only' '-v' '-c' '-shared-libgcc' '-march=x86-64'
 /usr/local/libexec/gcc/x86_64-unknown-linux-gnu/4.6.0/cc1plus -quiet -v -D_GNU_SOURCE -D_REENTRANT nestedCond.cc -quiet -dumpbase nestedCond.cc -mavx -mtune=corei7-avx -march=x86-64 -auxbase nestedCond -O2 -std=gnu++0x -version -ftree-vectorize -ftree-vectorizer-verbose=7 -fPIC -fassociative-math -freciprocal-math -fno-math-errno -fno-signed-zeros -fno-trapping-math -ffinite-math-only -o /tmp/innocent/ccmT7uly.s
GNU C++ (GCC) version 4.6.0 20110205 (experimental) (x86_64-unknown-linux-gnu)
	compiled by GNU C version 4.6.0 20110205 (experimental), GMP version 4.3.2, MPFR version 2.4.2, MPC version 0.8.1
GGC heuristics: --param ggc-min-expand=30 --param ggc-min-heapsize=4096
ignoring nonexistent directory "/usr/local/lib/gcc/x86_64-unknown-linux-gnu/4.6.0/../../../../x86_64-unknown-linux-gnu/include"
#include "..." search starts here:
#include <...> search starts here:
 /usr/local/lib/gcc/x86_64-unknown-linux-gnu/4.6.0/../../../../include/c++/4.6.0
 /usr/local/lib/gcc/x86_64-unknown-linux-gnu/4.6.0/../../../../include/c++/4.6.0/x86_64-unknown-linux-gnu
 /usr/local/lib/gcc/x86_64-unknown-linux-gnu/4.6.0/../../../../include/c++/4.6.0/backward
 /usr/local/lib/gcc/x86_64-unknown-linux-gnu/4.6.0/include
 /usr/local/include
 /usr/local/lib/gcc/x86_64-unknown-linux-gnu/4.6.0/include-fixed
 /usr/include
End of search list.
GNU C++ (GCC) version 4.6.0 20110205 (experimental) (x86_64-unknown-linux-gnu)
	compiled by GNU C version 4.6.0 20110205 (experimental), GMP version 4.3.2, MPFR version 2.4.2, MPC version 0.8.1
GGC heuristics: --param ggc-min-expand=30 --param ggc-min-heapsize=4096
Compiler executable checksum: 0d52c927b640361d99f7371685058a2b

nestedCond.cc:2: note: not vectorized: control flow in loop.
nestedCond.cc:7: note: not vectorized: data ref analysis failed next_a_22 = *D.2335_21;

nestedCond.cc:1: note: vectorized 0 loops in function.
COLLECT_GCC_OPTIONS='-O2' '-std=gnu++0x' '-mavx' '-mtune=corei7-avx' '-ftree-vectorize' '-ftree-vectorizer-verbose=7' '-pthread' '-fPIC' '-fassociative-math' '-freciprocal-math' '-fno-math-errno' '-fno-signed-zeros' '-fno-trapping-math' '-ffinite-math-only' '-v' '-c' '-shared-libgcc' '-march=x86-64'
 as --64 -msse2avx -o nestedCond.o /tmp/innocent/ccmT7uly.s
COMPILER_PATH=/usr/local/libexec/gcc/x86_64-unknown-linux-gnu/4.6.0/:/usr/local/libexec/gcc/x86_64-unknown-linux-gnu/4.6.0/:/usr/local/libexec/gcc/x86_64-unknown-linux-gnu/:/usr/local/lib/gcc/x86_64-unknown-linux-gnu/4.6.0/:/usr/local/lib/gcc/x86_64-unknown-linux-gnu/
LIBRARY_PATH=/usr/local/lib/gcc/x86_64-unknown-linux-gnu/4.6.0/:/usr/local/lib/gcc/x86_64-unknown-linux-gnu/4.6.0/../../../../lib64/:/lib/../lib64/:/usr/lib/../lib64/:/usr/local/lib/gcc/x86_64-unknown-linux-gnu/4.6.0/../../../:/lib/:/usr/lib/
COLLECT_GCC_OPTIONS='-O2' '-std=gnu++0x' '-mavx' '-mtune=corei7-avx' '-ftree-vectorize' '-ftree-vectorizer-verbose=7' '-pthread' '-fPIC' '-fassociative-math' '-freciprocal-math' '-fno-math-errno' '-fno-signed-zeros' '-fno-trapping-math' '-ffinite-math-only' '-v' '-c' '-shared-libgcc' '-march=x86-64'


---


### compiler : `gcc`
### title : `Missed optimization for -Os using xchg instead of mov.`
### open_at : `2011-03-02T05:30:44Z`
### last_modified_date : `2022-08-04T18:23:01Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=47949
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.6.0`
### severity : `enhancement`
### contents :
xchg %eax, reg is a one-byte instruction.  If reg is dead, this instruction could replace the two-byte mov reg, %eax for a one-byte savings.

ie:

int foo(int x)
{
	return x;
}

currently compiles to

mov    %edi,%eax
retq

with -Os, whereas the following may be better:

xchg %eax, %edi
retq

(Similar cases exist with mov reg, %rax; mov reg, %ax; and mov reg, %al)

Note that xchg is slower than mov, so this is only an optimization when size is more important than speed.


---


### compiler : `gcc`
### title : `Missed promotion of double precision constants to single precision for -funsafe-math-optimizations`
### open_at : `2011-03-04T14:42:27Z`
### last_modified_date : `2021-12-26T13:00:14Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=47990
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.6.0`
### severity : `enhancement`
### contents :
In 482.sphinx3 we have code like

float foo (float x, float y)
{
  return ((int)(x/y + 0.5)) * y;
}

where the addition of 0.5 is performed in double precision.  With
-funsafe-math-optimizations we can demote 0.5 to single precision
(its exactly representable) also because the result of the addition
does not take part of further floating point computation but is
immediately converted to int.

The unsafe part of this optimization occurs when x/y is FLT_MAX
and we'd truncate to a 64bit integer type.  For 32bit integers
it would probably be safe to do this optimization unconditionally.


---


### compiler : `gcc`
### title : `Missed optimization: unnecessary register moves`
### open_at : `2011-03-09T03:32:11Z`
### last_modified_date : `2021-08-19T20:05:26Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=48037
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.6.0`
### severity : `enhancement`
### contents :
Created attachment 23587
Source code

I want to perform certain operations on an SSE double precision vector. I am using the intrinsics offered by emmintrin.h to decompose the vector into two scalars, perform the operation on both elements, and reconstruct the vector. As example operation I calculate the square root using scalar instructions. I am aware that there is a vector instruction for this; I am only using this as a placeholder to simplify the code.

I use gcc 4.6.0:

$ g++-mp-4.6 --version
g++-mp-4.6 (GCC) 4.6.0 20110305 (experimental)

on a MacBook Pro:

$ uname -a
Darwin erik-schnetters-macbook-pro.local 10.6.0 Darwin Kernel Version 10.6.0: Wed Nov 10 18:13:17 PST 2010; root:xnu-1504.9.26~3/RELEASE_I386 i386

with a 2.66 GHz Intel Core i7 processor and I compile with the options

$ g++-mp-4.6 -S -O3 -march=native -ffast-math vecmath.cc

I tried four different ways of extracting the scalars for the vector, and I find that gcc generates unnecessary register-register moves in almost every case.


---


### compiler : `gcc`
### title : `Optimizer produces suboptimal code for e.g. x = x ^ (x >> 1)`
### open_at : `2011-03-10T19:30:42Z`
### last_modified_date : `2021-12-25T04:47:47Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=48064
### status : `NEW`
### tags : `missed-optimization, ra`
### component : `rtl-optimization`
### version : `4.5.2`
### severity : `enhancement`
### contents :
When I compile the following OPT.CPP with gcc 4.5.2 (mingw) under Windows-32...
===
int test(int x)
{
   x = x ^ (x >> 1);

   int x1=x;
   x = x >> 2;
   x = x ^ x1;

   return x;
}
===

...a call to
gpp -O3 -S OPT.CPP
produces this OPT.s:
===
         .file   "OPT.CPP"
         .text
         .p2align 2,,3
.globl __Z4testi
         .def    __Z4testi;      .scl    2;      .type   32;     .endef
__Z4testi:
LFB0:
         pushl   %ebp
LCFI0:
         movl    %esp, %ebp
LCFI1:
         movl    8(%ebp), %eax
         movl    %eax, %edx
         sarl    %edx
         xorl    %eax, %edx
         movl    %edx, %eax
         sarl    $2, %eax
         xorl    %edx, %eax
         leave
LCFI2:
         ret
LFE0:
===

The problem I see is that in
         movl    %eax, %edx
         sarl    %edx
         xorl    %eax, %edx

         movl    %edx, %eax
         sarl    $2, %eax
         xorl    %edx, %eax
gcc produces code which presumably costs 6 cycles
(edx and then eax is modified 3 times in a row)
whereas the equivalent statements
         movl    %eax, %edx
         sarl    %eax
         xorl    %eax, %edx

         movl    %edx, %eax
         sarl    $2, %edx
         xorl    %edx, %eax
cost only 4 cycles since the mov and the shift can go in parallel.
I would have expected this at least for explicit form in
   int x1=x;
   x = x >> 2;
   x = x ^ x1;
I found no way to get gcc to output my version.

A speed test reveals that the proposed form only costs about
2/3 of the time on Intel Atom N450 and 3/4 of the time on Intel i7.

Have I missed something?


By the way: If I produce an output in Intel syntax
the statement "sar eax" should be "sar eax,1".
Otherwise some assemblers will complain.


---


### compiler : `gcc`
### title : `associative property of builtins is not exploited on GIMPLE`
### open_at : `2011-03-12T14:57:24Z`
### last_modified_date : `2023-05-12T05:46:17Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=48092
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.7.0`
### severity : `enhancement`
### contents :
Is there any reason why (with -Ofast or -ffast-math) associative properties of sqrt are not exploited as for instance those of division?

examples
division (ok)

float div1(float a, float x, float y) {
   return a/x/y;
   0:   f3 0f 59 ca             mulss  %xmm2,%xmm1
   4:   f3 0f 5e c1             divss  %xmm1,%xmm0
}

sqrt

float sqrt1(float a, float x, float y) {
   return a*std::sqrt(x)*std::sqrt(y);
  10:   f3 0f 51 d2             sqrtss %xmm2,%xmm2
  14:   f3 0f 51 c9             sqrtss %xmm1,%xmm1
  18:   f3 0f 59 ca             mulss  %xmm2,%xmm1
  1c:   f3 0f 59 c8             mulss  %xmm0,%xmm1
}
  20:   0f 28 c1                movaps %xmm1,%xmm0

and


float rsqrt1(float a, float x, float y) {
   return a/std::sqrt(x)/std::sqrt(y);
  30:   f3 0f 51 c9             sqrtss %xmm1,%xmm1
  34:   f3 0f 51 d2             sqrtss %xmm2,%xmm2
  38:   f3 0f 59 d1             mulss  %xmm1,%xmm2
  3c:   f3 0f 5e c2             divss  %xmm2,%xmm0
}

in this second case I would have at least expected the use of 
"rsqrtss" to take precedence above the associative property of "div"
emitting the same code as below

float rsqrt2(float a, float x, float y) {
   return a/sqrtf(x*y);
  70:   f3 0f 59 ca             mulss  %xmm2,%xmm1
  74:   f3 0f 52 d9             rsqrtss %xmm1,%xmm3
  78:   f3 0f 59 cb             mulss  %xmm3,%xmm1
  7c:   f3 0f 59 cb             mulss  %xmm3,%xmm1
  80:   f3 0f 59 1d 00 00 00    mulss  0(%rip),%xmm3        # 88 <rsqrt2(float, float, float)+0x18>
  87:   00 
                        84: R_X86_64_PC32       .LC1+0xfffffffffffffffc
  88:   f3 0f 58 0d 00 00 00    addss  0(%rip),%xmm1        # 90 <rsqrt2(float, float, float)+0x20>
  8f:   00 
                        8c: R_X86_64_PC32       .LC0+0xfffffffffffffffc
  90:   f3 0f 59 cb             mulss  %xmm3,%xmm1
  94:   f3 0f 59 c8             mulss  %xmm0,%xmm1
}
  98:   0f 28 c1                movaps %xmm1,%xmm0


---


### compiler : `gcc`
### title : `Excessive code generated for vectorized loop`
### open_at : `2011-03-15T00:01:52Z`
### last_modified_date : `2021-08-27T05:24:12Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=48128
### status : `RESOLVED`
### tags : `missed-optimization, ra`
### component : `rtl-optimization`
### version : `4.6.0`
### severity : `normal`
### contents :
Created attachment 23658
Testcase (compile with `-O3 -march=pentium3')


---


### compiler : `gcc`
### title : `"rep ret" generated for -march=core2`
### open_at : `2011-03-22T06:54:19Z`
### last_modified_date : `2021-12-29T04:12:06Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=48227
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.5.4`
### severity : `normal`
### contents :
gcc 4.5 will use "rep; ret" for K8, Athlon, AMDFam10, Core2, and
generic.  Looking into the change history, we can see that gcc has padded
returns for Core2 ever since Core2 support was added here:
http://gcc.gnu.org/ml/gcc-patches/2006-11/msg00860.html

It is suspected
that Vlad just copied the generic tunings for Core2, and didn't notice
that there was no particular reason to pad returns for Core2.


---


### compiler : `gcc`
### title : `C frontend emit invalid promotions (TARGET_PROMOTE_PROTOTYPES )`
### open_at : `2011-03-24T13:47:04Z`
### last_modified_date : `2021-07-19T22:28:21Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=48274
### status : `NEW`
### tags : `missed-optimization`
### component : `c`
### version : `4.7.0`
### severity : `normal`
### contents :
This came up in the context of a stricter consistency checker for types in
our middle end.  I believe the C frontend emits invalid promotions for calls
to prototyped functions:

% cat x.c
unsigned passchar (char c);
unsigned passflt (float f);
unsigned passva (int i, ...);
char blachar (char c, float f)
{
  return passchar (c) + passflt (f) + passva(1, f);
}
% ./cc1 x.c -fdump-tree-original
% cat x.c.003t.original
;; Function blachar (null)
;; enabled by -tree-original
{
  return (char) (((unsigned char) passchar ((int) c) + (unsigned char) passflt (f)) + (unsigned char) passva (1, (double) f));
}

The emitted code doesn't depend on the -std=xxx setting.  What I believe
is invalid here is the call to passchar().  First, it's a prototyped
function, hence 6.5.2.2 #7 is invoked:

#7: ... the arguments are implicitly converted, as if by assignment, to the
    types of the corresponding parameters, taking the type of each parameter
    to be the unqualiﬁed version of its declared type. The ellipsis notation
    ...

Hence, as if by assignment.  types of assignment expressions is that of the
left operand after lvalue conversions.  In this case the left operand is
the corresponding parameter (char c), hence I don't think there's much
leeway to read this as actually passing an 'int'.

This sort of looks as if the argument passer applies either default argument
promotions (6.5.2.2 #6, but that would mean it also had to promote the
float in passflt() call to double), or integer promotions (which would be
completely off) to arguments for calls to prototyped functions.


---


### compiler : `gcc`
### title : `Suboptimal optimization of boolean expression addition`
### open_at : `2011-03-27T10:53:23Z`
### last_modified_date : `2021-09-18T21:25:31Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=48297
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.6.0`
### severity : `enhancement`
### contents :
gcc does not seem to recognize that boolean expressions, such as (a==b), are at most 1.  At least not when performing math on them.

Take the following function:

int foo( int a, int b, int c, int x )
{
    return (a==x)+(b==x)+(c==x);
}

With -O3 -fomit-frame-pointer -march=core2 on x86_64, gcc compiles this to:

   0:   39 cf                   cmp    edi,ecx
   2:   40 0f 94 c7             sete   dil
   6:   31 c0                   xor    eax,eax
   8:   39 ce                   cmp    esi,ecx
   a:   40 0f b6 ff             movzx  edi,dil
   e:   0f 94 c0                sete   al
  11:   01 f8                   add    eax,edi
  13:   39 ca                   cmp    edx,ecx
  15:   0f 94 c2                sete   dl
  18:   0f b6 d2                movzx  edx,dl
  1b:   01 d0                   add    eax,edx
  1d:   c3                      ret

As can be seen, gcc extends the inputs to 32-bit (with xor or movzx) and uses 32-bit additions, even though it could avoid this by using 8-bit additions and a single movzx at the end.

Let's try to force it:

int bar( int a, int b, int c, int x )
{
    return (uint8_t)((uint8_t)((uint8_t)(a==x)+(uint8_t)(b==x))+(uint8_t)(c==x));
}

0000000000000020 <bar>:
  20:   39 ce                   cmp    esi,ecx
  22:   40 0f 94 c6             sete   sil
  26:   39 cf                   cmp    edi,ecx
  28:   0f 94 c0                sete   al
  2b:   01 f0                   add    eax,esi
  2d:   39 ca                   cmp    edx,ecx
  2f:   0f 94 c2                sete   dl
  32:   01 d0                   add    eax,edx
  34:   0f b6 c0                movzx  eax,al
  37:   c3                      ret

Closer -- we saved two instructions -- but this is actually worse: the additions will have false dependencies on the previous contents of those registers.  What we WANT is this:

cmp    esi,ecx
sete   sil
cmp    edi,ecx
sete   al
add    al,sil
cmp    edx,ecx
sete   dl
add    al,dl
movzx  eax,al
ret

But gcc won't generate it no matter how much I attempt to massage it into doing so.

Is this a missing optimization or an optimization bug?


---


### compiler : `gcc`
### title : `missed CSE / reassoc with array offsets`
### open_at : `2011-03-28T13:56:24Z`
### last_modified_date : `2021-12-08T08:10:59Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=48316
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.7.0`
### severity : `enhancement`
### contents :
int
foo (int *p, int i)
{
  int i1 = i + 1;
  int i2 = i + 2;
  return p[i1] + p[i2];
}

int
bar (int *p, unsigned long i)
{
  unsigned long i1 = i + 1;
  unsigned long i2 = i + 2;
  return p[i1] + p[i2];
}

For both testcases (the latter being the more "optimal" input due to
pointer-plus-expr constraints) we miss to CSE the multiplication
of i by 4 which makes the memory references not trivially independent
(based on the same pointer, offsetted by different constants).  Such
a case causes vectorization for alias checks being inserted for
gfortran.dg/reassoc_4.f with --param max-completely-peeled-insns=4000

IL on x86_64 is

<bb 2>:
  i1_2 = i_1(D) + 1;
  i2_3 = i_1(D) + 2;
  D.2702_4 = (long unsigned int) i1_2;
  D.2703_5 = D.2702_4 * 4;
  D.2704_7 = p_6(D) + D.2703_5;
  D.2705_8 = MEM[(int *)D.2704_7];
  D.2706_9 = (long unsigned int) i2_3;
  D.2707_10 = D.2706_9 * 4;
  D.2708_11 = p_6(D) + D.2707_10;
  D.2709_12 = MEM[(int *)D.2708_11];
  D.2701_13 = D.2705_8 + D.2709_12;
  return D.2701_13;

vs.

<bb 2>:
  i1_2 = i_1(D) + 1;
  i2_3 = i_1(D) + 2;
  D.2694_4 = i1_2 * 4;
  D.2695_6 = p_5(D) + D.2694_4;
  D.2696_7 = MEM[(int *)D.2695_6];
  D.2697_8 = i2_3 * 4;
  D.2698_9 = p_5(D) + D.2697_8;
  D.2699_10 = MEM[(int *)D.2698_9];
  D.2693_11 = D.2696_7 + D.2699_10;
  return D.2693_11;

For the reassoc_4.f testcase the question is whether either SCEV or
data-dependence can be enhanced to handle the cases (the multiplications
are in BB2, outside of any loop).


---


### compiler : `gcc`
### title : `Recursion not converted into a loop`
### open_at : `2011-03-30T12:15:48Z`
### last_modified_date : `2021-08-10T23:18:28Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=48363
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.7.0`
### severity : `enhancement`
### contents :
For the following Fortran program, the recursion could be replaced by a loop. That's what happening for the related C program, but for the Fortran program the recursion remains. (Tried with -O3.)

(I guess the I/O statement (_gfortran_st_write* and _gfortran_transfer_*_write) confuse the ME, but I do not see why that should prevent the loop transformation. Hints how to modify the FE to help the ME are welcome, too.)

! Fortran version
call x (1)
contains
  recursive subroutine x (i)
    use iso_fortran_env
    integer, value :: i
    if (mod (i, 1000000) == 0) write (error_unit,'(a,i0)')'i=', i
    call x (i+1)
  end subroutine x
end


/* C version */
#include <stdio.h>
static void
x (int i) {
  if (!(i % 1000000))
    fprintf(stderr, "i=%d\n", i);
  x(i + 1);
}
int main () {
  x (1);
}


---


### compiler : `gcc`
### title : `ARM __attribute__((interrupt("FIQ"))) not optimizing register allocation`
### open_at : `2011-04-03T21:46:26Z`
### last_modified_date : `2019-05-08T09:02:33Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=48429
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.4.5`
### severity : `enhancement`
### contents :
Created attachment 23866
Source, intermediate and object code demonstrating the problem

On ARM (at least for ARM966, which is the platform for which this GCC was compiled), fast interrupt queue, or FIQ, has a private copy of registers r8 through r14, and those do not need to be saved if used by the interrupt service routine.

When creating an interrupt handler, GCC is obviously aware of this fact, as it does not save the frame pointer at the beginning of the function (which it does if a different type of interrupt is requested). It still, however, begin allocation of registers from r2 and r3, and that forces it to save them at the beginning of the function. Beginning the allocation at r8 and r9 would have saved all register saving, and made the function more efficient.

Problem happens even when compiled with -O3. Function in attachment could have easily been implemented without the need for either save or restore of any registers at all.

Shachar


---


### compiler : `gcc`
### title : `Does not vectorize loops involving casts from floating point to unsigned integer types`
### open_at : `2011-04-08T07:00:43Z`
### last_modified_date : `2021-08-24T23:06:49Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=48510
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.5.2`
### severity : `enhancement`
### contents :
The following code vectorizes with the command line options:

-march=native -mtune=native -ftree-vectorizer-verbose=12 -O3 -std=c99 -ffast-math -funsafe-math-optimizations -lm  main.c

#include <stdio.h>
#include <math.h>
int main() {
  double g[1000];
  for(int i=0; i<1000; i++) {
    g[i]=2*(g[i]);
  }
  for(int i=0; i<1000; i++) {
   printf("%f\n",g[i]);
  }
}

but the following code does not with the same options:


#include <stdio.h>
#include <math.h>
int main() {
  double g[1000];
  for(int i=0; i<1000; i++) {
    g[i]=2*((unsigned long)g[i]);
  }
  for(int i=0; i<1000; i++) {
   printf("%f\n",g[i]);
  }
}

If I understand correctly, there are SSE instructions for casting doubles to long integers on the platform I'm on (Intel Atom) which GCC could use.  (or perhaps there could be a benefit to vectorizing other parts of the loop, even if the cast does not utilize SIMD instructions.)


---


### compiler : `gcc`
### title : `missed optimization: integer overflow checks`
### open_at : `2011-04-12T18:36:06Z`
### last_modified_date : `2023-08-09T22:29:13Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=48580
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.6.0`
### severity : `enhancement`
### contents :
To the best of my knowledge, this is the only safe way (without -fwrapv) to check whether the product of two signed integers overflowed:

bool product_does_not_overflow(signed x, signed y)
{
  unsigned tmp = x * unsigned(y);

  return signed(tmp) > 0 && tmp / x == unsigned(y);
}

(I believe C and C++ are the same in this regard but I could be wrong.  If there is a better way to write this test I would love to know about it.)

g++ 4.6 produces this assembly dump on x86-64:

_Z25product_does_not_overflowii:
	movl	%esi, %edx
	xorl	%eax, %eax
	imull	%edi, %edx
	testl	%edx, %edx
	jle	.L2
	movl	%edx, %eax
	xorl	%edx, %edx
	divl	%edi
	cmpl	%eax, %esi
	sete	%al
.L2:
	rep
	ret

but, if I understand the semantics of IMUL correctly, it could do this instead:

_Z25product_does_not_overflowii:
	xorl	%eax, %eax
	imull	%edi, %esi
	setno	%al
	ret

which is a pretty substantial micro-win, particularly in getting rid of a divide.


---


### compiler : `gcc`
### title : `Inefficient complex float parameter passing`
### open_at : `2011-04-14T12:50:52Z`
### last_modified_date : `2021-08-02T18:06:42Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=48607
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.7.0`
### severity : `normal`
### contents :
[hjl@gnu-6 pr1000]$ cat z.i 
typedef _Complex float SCtype;
SCtype
foo (SCtype x1, SCtype x2, SCtype x3, SCtype x4, SCtype x5, SCtype x6,
     SCtype x7, SCtype x8, SCtype a, SCtype b)
{
  return x2;
}
[hjl@gnu-6 pr1000]$ /usr/gcc-4.7/bin/gcc -O2 -S z.i
[hjl@gnu-6 pr1000]$ cat z.s
	.file	"z.i"
	.text
	.p2align 4,,15
	.globl	foo
	.type	foo, @function
foo:
.LFB0:
	.cfi_startproc
	movq	%xmm1, -16(%rsp)
	movl	-16(%rsp), %eax
	movl	%eax, -72(%rsp)
	movl	-12(%rsp), %eax
	movl	%eax, -68(%rsp)
	movq	-72(%rsp), %xmm0
	ret
	.cfi_endproc
.LFE0:
	.size	foo, .-foo
	.ident	"GCC: (GNU) 4.7.0 20110406 (experimental) [trunk revision 172062]"
	.section	.note.GNU-stack,"",@progbits
[hjl@gnu-6 pr1000]$ 

We should simply do

movaps    %xmm1, %xmm0  

or

movq   %xmm1,%xmm0


---


### compiler : `gcc`
### title : `Inefficient complex float argument passing/return`
### open_at : `2011-04-14T13:57:30Z`
### last_modified_date : `2023-05-15T07:22:12Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=48609
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.7.0`
### severity : `normal`
### contents :
[hjl@gnu-6 pr1000]$ cat s2.i
typedef _Complex float SCtype;
extern SCtype bar;
void
foo (SCtype x)
{
  bar = x;
}
[hjl@gnu-6 pr1000]$ /usr/gcc-4.7/bin/gcc -S -O2 s2.i   
[hjl@gnu-6 pr1000]$ cat s2.s
	.file	"s2.i"
	.text
	.p2align 4,,15
	.globl	foo
	.type	foo, @function
foo:
.LFB0:
	.cfi_startproc
	movq	%xmm0, -8(%rsp)
	movl	-8(%rsp), %eax
	movl	%eax, bar(%rip)
	movl	-4(%rsp), %eax
	movl	%eax, bar+4(%rip)
	ret
	.cfi_endproc
.LFE0:
	.size	foo, .-foo

We should simply do

movq	%xmm0, bar(%rip)


---


### compiler : `gcc`
### title : `Missed optimization for use of __builtin_ctzll() and __builtin_clzll`
### open_at : `2011-04-15T20:49:51Z`
### last_modified_date : `2021-07-26T19:53:02Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=48634
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.6.0`
### severity : `enhancement`
### contents :
unsigned long long foo(unsigned long long x)
{
	return __builtin_ctzll(x);
}

Compiles into

bsf    %rdi,%rax
cltq
retq

at -O3 with 4.6.0
The cltq instruction isn't needed because the bitscan instruction will zero out the upper 32 bits of rax.  Basically, the return value of these intrinsics should be unsigned long long instead of int on 64 bit machines.  The ABI means that the reverse process of truncating back down to an int costs zero instructions.


---


### compiler : `gcc`
### title : `Horrible bitfield code generation on x86`
### open_at : `2011-04-20T04:25:05Z`
### last_modified_date : `2023-02-25T06:41:36Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=48696
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.5.2`
### severity : `normal`
### contents :
gcc (tried 4.5.1 and 4.6.0) generates absolutely horrid code for some common bitfield accesses due to minimizing the access size.

Trivial test case:

  struct bad_gcc_code_generation {
	unsigned type:6,
		 pos:16,
		 stream:10;
  };

  int show_bug(struct bad_gcc_code_generation *a)
  {
	a->type = 0;
	return a->pos;
  }

will generate code like this on x86-64 with -O2:

	andb	$-64, (%rdi)
	movl	(%rdi), %eax
	shrl	$6, %eax
	movzwl	%ax, %eax
	ret

where the problem is that byte access write, followed by a word access read.

Most (all?) modern x86 CPU's will come to a screeching halt when they see a read that hits a store buffer entry, but cannot be fully forwarded from it. The penalty can be quite severe, and this is _very_ noticeable in profiles.

This code would be _much_ faster either using an "andl" (making the store size match the next load, and thus forwarding through the store buffer), or by having the load be done first. 

(The above code snippet is not the real code I noticed it on, obviously, but real code definitely sees this, and profiling shows very clearly how the 32-bit load from memory basically stops cold due to the partial store buffer hit)

Using non-native accesses to memory is fine for loads (so narrowing the access for a pure load is fine), but for store or read-modify-write instructions it's almost always a serious performance problem to try to "optimize" the memory operand size to something smaller.

Yes, the constants often shrink, but the code becomes *much* slower unless you can guarantee that there are no loads of the original access size that follow the write.


---


### compiler : `gcc`
### title : `[missed optimization] GCC fails to use aliasing of ymm and xmm registers`
### open_at : `2011-04-20T13:25:58Z`
### last_modified_date : `2023-05-16T20:33:16Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=48701
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.6.0`
### severity : `enhancement`
### contents :
The two functions in the attached test case demonstrate the problem. The intermediate stores/loads on the stack really should be optimized away.

testStore output now:
vmovdqa %xmm1,-0x30(%rsp)   
vmovdqa %xmm0,-0x20(%rsp)   
vmovdqa -0x30(%rsp),%ymm0   
vmovdqa %ymm0,(<blackhole>)

should be either:
vinsertf128 $1,%xmm0,%ymm1,%ymm0
vmovdqa %ymm0,(<blackhole>)

or:
vmovdqa %xmm1,(<blackhole>)
vmovdqa %xmm0,0x10(<blackhole>)

depending on the target microarchitecture and accompanying code.

likewise the testLoad output now is:
vmovdqa (<blackhole>),%ymm0
vmovdqa %ymm0,-0x30(%rsp)
vmovdqa -0x20(%rsp),%xmm1
vmovdqa -0x30(%rsp),%xmm0

and should be either:
vmovdqa (<blackhole>),%ymm0
vextractf128 $1,%ymm0,%xmm1

or:
vmovdqa (<blackhole>),%xmm0
vmovdqa 0x10(<blackhole>),%xmm1


---


### compiler : `gcc`
### title : `~0ULL % (a / (a & -a)) == 0 is not optimized to false on the tree level`
### open_at : `2011-04-26T23:45:08Z`
### last_modified_date : `2023-08-18T13:57:16Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=48783
### status : `NEW`
### tags : `missed-optimization, TREE`
### component : `tree-optimization`
### version : `4.5.2`
### severity : `normal`
### contents :
Created attachment 24107
Preprocessed source

When compiled, the attached code refers to the 64 bit unsigned divmod helper function '__aeabi_uldivmod' even though the function is never called.  This causes a link error when cross-compiling an ARM Linux 2.6.38 kernel.

To reproduce:
 * Make a arm-linux-gnueabi cross compiler configured with --with-mode=thumb --with-arch=armv7-a --with-tune=cortex-a9 --with-float=softfp --with-fpu=neon
 * Compile the attached code with 'arm-linux-gnueabi-gcc -O2 -S wm8974.i'
 * See a '.global __aeabi_uldivmod' in the header of wm8974_set_dai_pll

Marking pll_factors() as noinline or putting asm("" : "+r"(source)); before the call to do_div() works around the problem.


---


### compiler : `gcc`
### title : `optimizing integer power of 2`
### open_at : `2011-04-28T20:24:44Z`
### last_modified_date : `2021-07-26T18:39:09Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=48812
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.4.5`
### severity : `enhancement`
### contents :
gcc correctly optimize
int divu(uint a, uint b)
{
        return a / (1<<b);
}
to
divu:
        mov     r0, r0, lsr r1
        mov     pc, lr

but it fails to optimize
int divu3(uint a, uint b)
{
        return a / ((1U<<b) / 4);
}

gcc generate
(arm-linux-gnueabi-gcc -Os  p.c -march=armv4 -mno-thumb-interwork -S)
divu3:
        stmfd   sp!, {r3, lr}
        mov     r3, #1
        mov     r1, r3, asl r1
        mov     r1, r1, lsr #2
        bl      {{{__}}}aeabi_uidiv
        ldmfd   sp!, {r3, pc}
or
(gcc p.c -S -O3 -fomit-frame-pointer -mregparm=3)
divu3:
        pushl   %ebx
        movl    %edx, %ecx
        movl    $1, %ebx
        xorl    %edx, %edx
        sall    %cl, %ebx
        shrl    $2, %ebx
        divl    %ebx
        popl    %ebx
        ret

but ((1U<<b) / 4) is 0 or a power of 2. Div by 0 is undefined in C ( C99 6.5.5p5)

So why can we generate : 
        mov     r3, #1
        mov     r1, r3, asl r1
        mov     r1, r1, lsr #2
        mov     r0, r0, lsr r1

?

Note that gcc correctly optimize
int divu5(uint a, uint b)
{
        return a / ((1U<<b) * 4);
}


---


### compiler : `gcc`
### title : `Atomic update merging`
### open_at : `2011-05-13T10:26:10Z`
### last_modified_date : `2021-08-30T01:59:43Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=48987
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.6.0`
### severity : `enhancement`
### contents :
Not being a GCC developer I am not sure if this is RTL or tree
level optimization, so the the component selection is guesstimated.

The problem: GCC does not merge atomic modifications of the
same location. An example is given below:

void yyy(int* p) {

    __sync_fetch_and_add(p, 1);
    __sync_fetch_and_add(p, 1);
}

On x86 GCC emits multiple independent modifications:

0040edd0 <__Z3yyyPi>:
  40edd0:	8b 44 24 04          	mov    0x4(%esp),%eax
  40edd4:	f0 ff 00             	lock incl (%eax)
  40edd7:	f0 ff 00             	lock incl (%eax)
  40edda:	c3                   	ret     

The lock prefix implies a full memory barrier, so if there
were no memory references in between, the code is equivalent to:

    lock addl $0x02, (%eax)

The example above is purely artificial, but real C++ programs
using smart pointers generate similar patterns. Atomic operations
are expensive, so GCC should minimize their count, namely it
should check the invocation graph/tree and try merge subsequent
modifications. A pattern with high probability of occurence is
equivalent to:

void yyy(int* p) {

    __sync_fetch_and_add(p, 1);
    __sync_fetch_and_add(p, -1);
}

which on most platforms technically is a NOP with membar semantics
and can be implemented as such. On x86/x64 supporting SSE3 the update
interferes with the monitor/mwait mechanism (i.e. processor wakes up
after specified cache line modification) and shouldn't be replaced
by mfence -- a dummy store should be performed and the correct pattern
then is:

    lock add $0x00, (addr)

In fact it can be the only pattern, as mfence and lock add are
of comparable performance and none of them wastes a register, as,
for example, xadd does.


---


### compiler : `gcc`
### title : `Missed optimization of pointer arithmetic`
### open_at : `2011-05-17T17:13:59Z`
### last_modified_date : `2021-08-14T20:53:25Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=49028
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.6.0`
### severity : `enhancement`
### contents :
The following examples come from x64, but I believe the problem
shows on other architectures too. 

I have implemented an object recycler based on a circular buffer of pointers
with a single cursor. N is the capacity of the buffer; powers of two are highly preferred, so let we assume N = 16.


template <unsigned int N> struct R {

    void*  m_Data[N];
    void** m_Cursor;

    void xxx_release(void* p) __attribute__((__noinline__));
};

template <unsigned int N> void R<N>::xxx_release(void* p) {

    m_Cursor = m_Data + ((m_Cursor + 1 - m_Data) % N);
    *m_Cursor = p;
}

int main(int argc, char *argv[]) {      

    R<16> rrr;
    rrr.xxx_release(0);
    return 0;
}

This generates (-O3 -msse -msse2 -msse4.2 -mfpmath=sse -march=core2 -mtune=core2):

000000000041a910 <_ZN1RILj16EE11xxx_releaseEPv>:
  41a910:	48 8b 97 80 00 00 00 	mov    0x80(%rdi),%rdx
  41a917:	48 83 c2 08          	add    $0x8,%rdx
  41a91b:	48 29 fa             	sub    %rdi,%rdx
  41a91e:	48 89 d0             	mov    %rdx,%rax
  41a921:	48 c1 fa 3f          	sar    $0x3f,%rdx
  41a925:	48 c1 ea 3c          	shr    $0x3c,%rdx
  41a929:	48 c1 f8 03          	sar    $0x3,%rax
  41a92d:	48 01 d0             	add    %rdx,%rax
  41a930:	83 e0 0f             	and    $0xf,%eax
  41a933:	48 29 d0             	sub    %rdx,%rax
  41a936:	48 8d 14 c7          	lea    (%rdi,%rax,8),%rdx
  41a93a:	48 89 34 c7          	mov    %rsi,(%rdi,%rax,8)
  41a93e:	48 89 97 80 00 00 00 	mov    %rdx,0x80(%rdi)
  41a945:	c3                   	retq   

The sequence is far from being optimal. The compiler should not move pointer arithmetic to the type-independent integer domain (i.e. were (p + 1 - p) == 1),
but notice that the actual increment, whis is M = sizeof(void*), is a power of 2, in this case 8, so the final modulo result in integer domain for (p + 1) % N will be the same as (((char*) p) + M) % (N * M). To cut a long story short: instead of the above it should just generate:

000000000041a910 <_ZN1RILj16EE11xxx_releaseEPv>:
    mov    0x80(%rdi),%rdx
    add    $0x08, %rdx
    sub    %rdi, %rdx
    and    $0x7f, %rdx
    add    %rdi, %rdx
    mov    %rsi, (%rdx)
    mov    %rdx, 0x80(%rdi)
    retq

I'm not sure I understand what is GCC trying to achieve with the shifts.
Secondly, my example above uses only simple addressing modes, but GCC
uses the most complex mode twice: in lea and in the subsequent mov.
Complex lea has 3 cycles of latency on SandyBridge, according to the
Intel Optimization Manual, p. 3.5.1.3, so it should best be avoided.


---


### compiler : `gcc`
### title : `useless cmp+jmp generated for switch when "default:" is unreachable`
### open_at : `2011-05-18T21:44:18Z`
### last_modified_date : `2023-05-13T17:57:26Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=49054
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.6.0`
### severity : `enhancement`
### contents :
gcc (Debian 4.6.0-7) 4.6.1 20110507 (prerelease)

When I compile the following switch, GCC generates code to 
check that id <= 4 and to conditionally jump to... the next instruction.


% cat foo.c
unsigned f(void);
unsigned g(void);
unsigned h(void);
unsigned i(void);
unsigned j(void);

unsigned int baz(unsigned int id)
{
  switch (id)
    {
    case 0:
      return f();
    case 1:
      return g();
    case 2:
      return h();
    case 3:
      return i();
    case 4:
      return j();
    default:
      __builtin_unreachable();
    }
}
% gcc -march=core2 -m64 -O3 foo.c -c -o foo.o
% objdump -DC foo.o | head -23

foo.o:     file format elf64-x86-64


Disassembly of section .text:

0000000000000000 <baz>:
   0:   83 ff 05                cmp    $0x4,%edi
   3:   76 03                   jbe    8 <baz+0x8>
   5:   0f 1f 00                nopl   (%rax)
   8:   89 ff                   mov    %edi,%edi
   a:   ff 24 fd 00 00 00 00    jmpq   *0x0(,%rdi,8)
  11:   0f 1f 80 00 00 00 00    nopl   0x0(%rax)
  18:   e9 00 00 00 00          jmpq   1d <baz+0x1d>
  1d:   0f 1f 00                nopl   (%rax)
  20:   e9 00 00 00 00          jmpq   25 <baz+0x25>
  25:   0f 1f 00                nopl   (%rax)
  28:   e9 00 00 00 00          jmpq   2d <baz+0x2d>
  2d:   0f 1f 00                nopl   (%rax)
  30:   e9 00 00 00 00          jmpq   35 <baz+0x35>
  35:   0f 1f 00                nopl   (%rax)
  38:   e9 00 00 00 00          jmpq   3d <baz+0x3d>


What is the point of the first three instructions?  I would have expected baz to start at adress 8.


---


### compiler : `gcc`
### title : `[x86/x64]: broken alias analysis leads vectorizer to emit poor code`
### open_at : `2011-05-19T13:59:18Z`
### last_modified_date : `2021-08-14T21:59:11Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=49064
### status : `RESOLVED`
### tags : `alias, missed-optimization`
### component : `target`
### version : `4.6.0`
### severity : `normal`
### contents :
On an x86 capable of SSE2 or x64 (which has SSE2 by definition) GCC tries
to vectorize as much integer code as possible, but ends up witch code much
worse than without vectorization. The SSE2-based version unnecessarily
recomputes all the m_Data pointers, as demonstrated by the following C++
snippet. I guess the reason is unsophisticated alias analysis, but the
actual reason may in fact be different.


struct X {

    __m128i*    m_Data;
    std::size_t m_Len;

    void xor_all(const X& v1, const X& v2);    
    void xor_all2(const X& v1, const X& v2);    
};


void X::xor_all(const X& v1, const X& v2) {

    for(std::size_t i = 0; i != m_Len; ++i) {

        m_Data[i] = v1.m_Data[i] ^ v2.m_Data[i];
    }
}

void X::xor_all2(const X& v1, const X& v2) {

    __m128i* p0 = m_Data;
    __m128i* p1 = v1.m_Data;
    __m128i* p2 = v2.m_Data;

    for(std::size_t i = 0; i != m_Len; ++i) {

        p0[i] = p1[i] ^ p2[i];
    }
}

As can be seen, xor_all2 produces nice code and xor_all doesn't:

0000000000447c70 <_ZN1X7xor_allERKS_S1_>:
  447c70:	48 83 7f 08 00       	cmpq   $0x0,0x8(%rdi)
  447c75:	74 35                	je     447cac <_ZN1X7xor_allERKS_S1_+0x3c>
  447c77:	31 c0                	xor    %eax,%eax
  447c79:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)
  447c80:	4c 8b 12             	mov    (%rdx),%r10
  447c83:	48 89 c1             	mov    %rax,%rcx
  447c86:	48 83 c0 01          	add    $0x1,%rax
  447c8a:	4c 8b 0e             	mov    (%rsi),%r9
  447c8d:	48 c1 e1 04          	shl    $0x4,%rcx
  447c91:	4c 8b 07             	mov    (%rdi),%r8
  447c94:	66 41 0f 6f 04 0a    	movdqa (%r10,%rcx,1),%xmm0
  447c9a:	66 41 0f ef 04 09    	pxor   (%r9,%rcx,1),%xmm0
  447ca0:	66 41 0f 7f 04 08    	movdqa %xmm0,(%r8,%rcx,1)
  447ca6:	48 39 47 08          	cmp    %rax,0x8(%rdi)
  447caa:	75 d4                	jne    447c80 <_ZN1X7xor_allERKS_S1_+0x10>
  447cac:	f3 c3                	repz retq 


0000000000447cb0 <_ZN1X8xor_all2ERKS_S1_>:
  447cb0:	48 83 7f 08 00       	cmpq   $0x0,0x8(%rdi)
  447cb5:	48 8b 0f             	mov    (%rdi),%rcx
  447cb8:	48 8b 36             	mov    (%rsi),%rsi
  447cbb:	4c 8b 02             	mov    (%rdx),%r8
  447cbe:	74 26                	je     447ce6 <_ZN1X8xor_all2ERKS_S1_+0x36>
  447cc0:	31 c0                	xor    %eax,%eax
  447cc2:	31 d2                	xor    %edx,%edx
  447cc4:	0f 1f 40 00          	nopl   0x0(%rax)
  447cc8:	66 41 0f 6f 04 00    	movdqa (%r8,%rax,1),%xmm0
  447cce:	48 83 c2 01          	add    $0x1,%rdx
  447cd2:	66 0f ef 04 06       	pxor   (%rsi,%rax,1),%xmm0
  447cd7:	66 0f 7f 04 01       	movdqa %xmm0,(%rcx,%rax,1)
  447cdc:	48 83 c0 10          	add    $0x10,%rax
  447ce0:	48 39 57 08          	cmp    %rdx,0x8(%rdi)
  447ce4:	75 e2                	jne    447cc8 <_ZN1X8xor_all2ERKS_S1_+0x18>
  447ce6:	f3 c3                	repz retq


---


### compiler : `gcc`
### title : `[x32] Extra instruction in compare`
### open_at : `2011-05-21T13:17:57Z`
### last_modified_date : `2021-09-13T04:30:43Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=49101
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `target`
### version : `4.7.0`
### severity : `normal`
### contents :
[hjl@gnu-6 ilp32-41]$ cat foo.c
extern void abort (void);
typedef __SIZE_TYPE__ size_t;
extern size_t strcspn (const char *, const char *);
extern char *strcpy (char *, const char *);

int
main (void)
{
  char *s1 = "hello world";
  char dst[64], *d2;
  
  strcpy (dst, s1);
  d2 = dst;
  if (strcspn (++d2+5, "") != 5)
    abort();

  return 0;
}
[hjl@gnu-6 ilp32-41]$ make foo.s
/export/build/gnu/gcc-x32/build-x86_64-linux/gcc/xgcc -B/export/build/gnu/gcc-x32/build-x86_64-linux/gcc/ -mx32 -S -o foo.s -mx32 -O   foo.c
[hjl@gnu-6 ilp32-41]$ cat foo.s
	.file	"foo.c"
	.text
	.globl	main
	.type	main, @function
main:
.LFB0:
	.cfi_startproc
	subq	$72, %rsp
	.cfi_def_cfa_offset 80
	movl	$1819043176, (%rsp)
	movl	$1870078063, 4(%rsp)
	movl	$6581362, 8(%rsp)
	leaq	6(%rsp), %rdi
	movl	$0, %eax
	movq	$-1, %rcx
	repnz scasb
	notq	%rcx
	cmpl	$6, %ecx
	je	.L2
	call	abort
.L2:
	movl	$0, %eax
	addq	$72, %rsp
	.cfi_def_cfa_offset 8
	ret
	.cfi_endproc
.LFE0:
	.size	main, .-main
	.ident	"GCC: (GNU) 4.7.0 20110521 (experimental)"
	.section	.note.GNU-stack,"",@progbits
[hjl@gnu-6 ilp32-41]$ /export/build/gnu/gcc-x32/build-x86_64-linux/gcc/xgcc -B/export/build/gnu/gcc-x32/build-x86_64-linux/gcc/ -S -o 64.s -O foo.c
[hjl@gnu-6 ilp32-41]$ diff -up 64.s foo.s
--- 64.s	2011-05-21 06:16:11.260010306 -0700
+++ foo.s	2011-05-21 06:15:38.076996129 -0700
@@ -14,7 +14,8 @@ main:
 	movl	$0, %eax
 	movq	$-1, %rcx
 	repnz scasb
-	cmpq	$-7, %rcx
+	notq	%rcx
+	cmpl	$6, %ecx
 	je	.L2
 	call	abort
 .L2:
[hjl@gnu-6 ilp32-41]$ 

X32 generates

	notq	%rcx
	cmpl	$6, %ecx

instead of

        cmpq	$-7, %rcx


---


### compiler : `gcc`
### title : `Support constructors tied to a variable`
### open_at : `2011-05-22T11:43:52Z`
### last_modified_date : `2019-01-18T00:37:53Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=49108
### status : `WAITING`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.7.0`
### severity : `normal`
### contents :
Follow up to PR 49106.

There should be the possibility to tie (nested) constructors to a variable (of the parent function), such that the constructor is optimized away if the parent function is optimized way.

Fortran example (with -fcoarray=lib):

program main
contains
  subroutine foo()
    integer :: a[*] 
    a = 8
  end subroutine
end program main

Here, "foo()" is never called. With -fcoarray=lib gfortran creates a constructor function to register the coarray "a" with the library. The constructor is nested in "foo" - and obviously not needed if the function (or the variable "a") is optimized away.

Expected: By tying the constructor to the variable, the constructor can be optimized away if the variable is needed.


Dump of the Fortran program above:

_caf_init.1 ()
{
  a = (integer(kind=4) * restrict)
        _gfortran_caf_register (4, 0, &caf_token.0, 0B, 0B, 0);
}

foo ()
{
  static void * caf_token.0;
  static integer(kind=4) * restrict a;
  void _caf_init.1 (void);

  *a = 8;
}


---


### compiler : `gcc`
### title : `-Os generates constant mov instead of instruction xor and mov when zeroing`
### open_at : `2011-05-23T15:15:52Z`
### last_modified_date : `2021-07-26T18:54:55Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=49127
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.6.0`
### severity : `enhancement`
### contents :
void zero (void* p) { *reinterpret_cast<ulong*>(p) = 0; }

Generates:

48 c7 07 00 00 00 00    movq   $0x0,(%rdi)

This is shorter by 2 bytes:

31 c0                   xor    %eax,%eax
48 89 07                mov    %rax,(%rdi)

And can be reused in further assignments of zero for more savings:

31 c0                   xor    %eax,%eax
48 89 07                mov    %rax,(%rdi)
48 89 47 04             mov    %rax,0x4(%rdi)


---


### compiler : `gcc`
### title : `Certain expressions take an extremely long time for no apparent reason`
### open_at : `2011-05-24T18:51:54Z`
### last_modified_date : `2021-12-26T12:49:19Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=49148
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.4.3`
### severity : `minor`
### contents :
Created attachment 24349
This is a commented test case of an expression that takes 100 times longer to evaluate than it should. See other files for even more minimal examples (without comments).

I have been doing work on 1-D Jacobi stencils. Basically, this involves a lot of repeated operations. For some reason, however, I have been getting extremely long run times for certain expressions. What is weird is that if I TAKE OUT a multiply operation, the function takes about 100 times longer to run than if I left it in.

The line that causes the problems is marked in the source code. It reads:

     new[i] = (A[i-1] + A[i] + A[i+1]) / 4.0;

If I change this to the following, there is no problem:

     new[i] = (A[i-1] + 2*A[i] + A[i+1]) / 4.0;

As another example, the following line runs slowly:

     new[i] = (A[i-1] + A[i] + A[i+1]) * 0.3;

while this line runs quickly:

     new[i] = (A[i-1] + 2*A[i] + A[i+1]) * 0.333;

The reason I think this is a bug is that it does not happen with older versions of GCC (for example, 4.1.2), nor with the Intel C Compiler.


---


### compiler : `gcc`
### title : `Unnecessary stack save/restore code generated for a leaf function (arm-elf-gcc)`
### open_at : `2011-05-25T10:08:32Z`
### last_modified_date : `2021-12-19T00:39:01Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=49157
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.6.0`
### severity : `enhancement`
### contents :
For the following example:
struct  Complex16{
  short a;
  short b;
};


short foo (struct Complex16 s)
{
  return s.a + s.b;
}


Compile with:

arm-elf-gcc tst.c -O2 -S -mstructure-size-boundary=8

It produces:
foo:
	@ args = 0, pretend = 0, frame = 4
	@ frame_needed = 0, uses_anonymous_args = 0
	@ link register save eliminated.
	mov	r3, r0, asl #16
	mov	r3, r3, lsr #16
	add	r0, r3, r0, lsr #16
	mov	r0, r0, asl #16
	sub	sp, sp, #4
	mov	r0, r0, asr #16
	add	sp, sp, #4
	bx	lr

The problem is with struct-size-boundary=8, the structure has BLKmode and mapped to memory after RTL expand. However, memory accesses are optimized away later. But GCC records a stack item anyway and generates stack frame save/restore code for this leaf function. 

If we compile without -mstructure-size-boundary=8 (default is 32), it generates much better code.

foo:
	@ args = 0, pretend = 0, frame = 0
	@ frame_needed = 0, uses_anonymous_args = 0
	@ link register save eliminated.
	add	r0, r0, r0, asr #16
	mov	r0, r0, asl #16
	mov	r0, r0, asr #16
	bx	lr

This is not limited to ARM gcc. Our target has the same issue because STRUCTURE_SIZE_BOUNDARY = 8 to save data memory size.

Though I only tested gcc 4.6, I believe trunk gcc probably has the same problem.


---


### compiler : `gcc`
### title : `missed-optimization: useless expressions not moved out of loop`
### open_at : `2011-05-27T22:03:33Z`
### last_modified_date : `2021-06-08T21:29:12Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=49203
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.7.0`
### severity : `enhancement`
### contents :
Hi all,

Below is (a simplified version of) some real code I recently
encountered. The stores to the 'output' array are written in the inner
loop, but the intention was probably to have them in the outer loop.

Gcc is able to 'correct' this programming mistake, but only partly:
the stores itself are moved to the outer loop, but the instructions that
calculate those values remain in the inner loop.

For this particular example, the best solution is of course to fix the
C code. But maybe this missed-optimization can also occur in other,
more valid, contexts.

Below I've included the generated x86_64 code for this example by
recent versions of both gcc and llvm.

///////////////////////////////////////////////////////////////////

unsigned char input[100];
unsigned char output[100];

void f() {
	for (int i = 0; i < 32; i += 4) {
		unsigned tmp = 0;
		for (int j = 0; j < 16; ++j) {
			tmp = (tmp << 2) | (input[i + j] & 0x03);
			output[i + 0] = (tmp >> 24) & 0xFF;
			output[i + 1] = (tmp >> 16) & 0xFF;
			output[i + 2] = (tmp >>  8) & 0xFF;
			output[i + 3] = (tmp >>  0) & 0xFF;
		}
	}
}

///////////////////////////////////////////////////////////////////

g++ (GCC) 4.7.0 20110527 (experimental)
g++ -O2 -S

        movl    $output, %r10d
        movq    %r10, %r9
        .p2align 4,,10
        .p2align 3
.L2:
        movl    %r9d, %esi
        xorl    %edx, %edx
        xorl    %eax, %eax
        subl    %r10d, %esi
        .p2align 4,,10
        .p2align 3
.L3:
        leal    0(,%rax,4), %ecx
        leal    (%rdx,%rsi), %eax
        addl    $1, %edx
        cltq
        movzbl  input(%rax), %eax
        andl    $3, %eax
        orl     %ecx, %eax
        movl    %eax, %r8d
        movl    %eax, %edi
        movl    %eax, %ecx
        shrl    $24, %r8d
        shrl    $16, %edi
        shrl    $8, %ecx
        cmpl    $16, %edx
        jne     .L3
        movb    %r8b, (%r9)
        movb    %dil, 1(%r9)
        movb    %cl, 2(%r9)
        movb    %al, 3(%r9)
        addq    $4, %r9
        cmpq    $output+32, %r9
        jne     .L2
        rep
        ret

///////////////////////////////////////////////////////////////////

clang version 3.0 (http://llvm.org/git/clang.git 855f41963e545172a935d07b4713d079e258a207)
clang++ -O2 -S

# BB#0:                                 # %entry
        xorl    %eax, %eax
        .align  16, 0x90
.LBB0_1:                                # %for.cond4.preheader
                                        # =>This Loop Header: Depth=1
                                        #     Child Loop BB0_2 Depth 2
        xorl    %esi, %esi
        movq    $-16, %rdx
        .align  16, 0x90
.LBB0_2:                                # %for.body7
                                        #   Parent Loop BB0_1 Depth=1
                                        # =>  This Inner Loop Header: Depth=2
        movl    %esi, %ecx
        movzbl  input+16(%rdx,%rax), %edi
        andl    $3, %edi
        leal    (,%rcx,4), %esi
        orl     %edi, %esi
        incq    %rdx
        jne     .LBB0_2
# BB#3:                                 # %for.inc44
                                        #   in Loop: Header=BB0_1 Depth=1
        movb    %sil, output+3(%rax)
        movl    %ecx, %edx
        shrl    $6, %edx
        movb    %dl, output+2(%rax)
        movl    %ecx, %edx
        shrl    $14, %edx
        movb    %dl, output+1(%rax)
        shrl    $22, %ecx
        movb    %cl, output(%rax)
        addq    $4, %rax
        cmpq    $32, %rax
        jne     .LBB0_1
# BB#4:                                 # %for.end47
        ret


---


### compiler : `gcc`
### title : `__sync or __atomic builtins will not emit 'lock bts/btr/btc'`
### open_at : `2011-05-31T19:24:34Z`
### last_modified_date : `2021-11-10T09:17:21Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=49244
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `unknown`
### severity : `enhancement`
### contents :
I want to be able to code this function:

bool
set_and_test (int *a,
              int bit)
{
  uint mask = (1u << bit);

  return (__sync_fetch_and_or (a, mask) & mask) != 0;
}

and have GCC not emit a loop on amd64 and x86.


GCC presently emits a loop for __sync_fetch_and_or() in this case.  That's because asm "lock or" discards the previous value, so it can only be used in cases that the result is ignored.  Since we do a comparison with the value, GCC has to do the loop.

This special case (set and test a single bit) corresponds quite directly to the 'lock bts' assembly instruction, though.  GCC could emit that instead.

It would be nice if GCC could detect (by magic?) that I am only interested in this single bit or (probably much easier) expose an intrinsic that lets me access this functionality on platforms that it exists and falls back to using __sync_fetch_and_or() otherwise.


---


### compiler : `gcc`
### title : `register allocation worse`
### open_at : `2011-06-10T02:53:54Z`
### last_modified_date : `2021-12-18T22:57:46Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=49357
### status : `SUSPENDED`
### tags : `missed-optimization, ra`
### component : `rtl-optimization`
### version : `4.7.0`
### severity : `normal`
### contents :
Compare the prologue for the test-case in attachment 24471 to PR49154 and compiled according to those instructions, <http://gcc.gnu.org/bugzilla/attachment.cgi?id=24471> between 4.3.3 (everything before the first "add"):
	subq 4,$sp
	move $srp,[$sp]
	subq 12,$sp
	movem $r2,[$sp]
	move.d $r10,$r2
	move.d $r10,$r9
	move.d $r11,$r10

to that of trunk at r174114 as well as r174870:
        subq 4,$sp
        move $srp,[$sp]
        subq 16,$sp
        movem $r3,[$sp]
        subq 4,$sp
        move.d $r8,[$sp]
        move.d $r10,$r8
        move.d $r11,$r9

So, we have a regression from 3 to 5 registers, and with a hole compared to reg_alloc_order.  Note that the source uses DFmode and DImode and derived unions; at a glance "normal" code is less affected.  Building on a 32-bit host seems to aggravate the situation.

Just put here as a note for the time being.


---


### compiler : `gcc`
### title : `missed optimization with __restrict field`
### open_at : `2011-06-10T17:20:54Z`
### last_modified_date : `2023-01-19T06:17:59Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=49367
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.7.0`
### severity : `enhancement`
### contents :
GCC fails to optimize away the call to g() in this C testcase.  It should recognize that since we've established that a1 is different from a2, their pointer fields must also be disjoint.  This is necessary to be able to improve optimization of C++ container classes, which currently have worse performance than raw restricted pointers.

typedef struct A
{
  int *__restrict p;
} A;

void g();

void f (A* a1, A* a2)
{
  if (a1 == a2)
    return;

  *a1->p = 0;
  *a2->p = 1;
  if (*a1->p != 0)
    g();
}

int main()
{
  A a,b;
  f (&a,&b);
}


---


### compiler : `gcc`
### title : `[11/12/13/14 Regression] Misaligned store support pessimization`
### open_at : `2011-06-16T14:57:15Z`
### last_modified_date : `2023-07-07T10:29:30Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=49442
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.6.0`
### severity : `normal`
### contents :
__attribute__((noinline, noclone))
void baz (double *out1, double *out2, double *out3, double *in1, double *in2, int len)
{
  for (int i = 0; i < len; ++i)
    {
      out1[i] = in1[i] * in2[i];
      out2[i] = in1[i] + in2[i];
      out3[i] = in1[i] - in2[i];
    }
}

double a[50000] __attribute__((aligned (32)));
int
main ()
{
  int i;
  for (i = 0; i < 500000; i++)
    baz (a + 0, a + 10000, a + 20000, a + 30000, a + 40000, 10000);
  return 0;
}

is measurably slower in 4.6 compared to 4.4 with -m64 -O3 -mtune=generic, apparently starting with http://gcc.gnu.org/viewcvs?root=gcc&view=rev&rev=148211
at least on Intel CPUs.
with r148210:
Strip out best and worst realtime result
minimum: 6.603036509 sec real / 0.000086529 sec CPU
maximum: 6.720307841 sec real / 0.000159148 sec CPU
average: 6.629486345 sec real / 0.000133896 sec CPU
stdev  : 0.024886889 sec real / 0.000020014 sec CPU
with r148211:
Strip out best and worst realtime result
minimum: 6.969550715 sec real / 0.000072647 sec CPU
maximum: 7.564913575 sec real / 0.000162211 sec CPU
average: 7.192333688 sec real / 0.000135634 sec CPU
stdev  : 0.101616835 sec real / 0.000022659 sec CPU


---


### compiler : `gcc`
### title : `DOM inhibits if-conversion and vectorization`
### open_at : `2011-06-23T06:55:00Z`
### last_modified_date : `2023-05-02T00:46:44Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=49513
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.7.0`
### severity : `major`
### contents :
in the simple example below the first loop vectorize, the second not
I'm using
gcc version 4.7.0 20110528 (experimental) (GCC) 

#include<cmath>
float __attribute__ ((aligned(16))) a[1024];
float __attribute__ ((aligned(16))) s[1024];
float __attribute__ ((aligned(16))) c[1024];


inline float bar(float y, float x ){
  float xx = fabs(x);
  float yy = fabs(y);
    
  float tmp =0.0f;
  if (yy>xx) {
    tmp = yy;
    yy=xx; xx=tmp;
  }
  float t=yy/xx;
  return t;
}

void foo1() {
  for (int i=0; i!=1024; ++i) {
    float z = i;
    a[i] = bar(s[i],c[i]);  
  }
}
void foo2() {
  for (int i=0; i!=1024; ++i) {
    float z = i;
    a[i] = bar(z*s[i],z*c[i]);  
 }
}



c++   -std=c++0x -Ofast -c vectBug.cc -ftree-vectorizer-verbose=7

vectBug.cc:21: note: vect_model_load_cost: aligned.
vectBug.cc:21: note: vect_get_data_access_cost: inside_cost = 1, outside_cost = 0.
vectBug.cc:21: note: vect_model_load_cost: aligned.
vectBug.cc:21: note: vect_get_data_access_cost: inside_cost = 2, outside_cost = 0.
vectBug.cc:21: note: vect_model_store_cost: aligned.
vectBug.cc:21: note: vect_get_data_access_cost: inside_cost = 3, outside_cost = 0.
vectBug.cc:21: note: vect_model_load_cost: aligned.
vectBug.cc:21: note: vect_model_load_cost: inside_cost = 1, outside_cost = 0 .
vectBug.cc:21: note: vect_model_load_cost: aligned.
vectBug.cc:21: note: vect_model_load_cost: inside_cost = 1, outside_cost = 0 .
vectBug.cc:21: note: vect_model_simple_cost: inside_cost = 1, outside_cost = 0 .
vectBug.cc:21: note: vect_model_simple_cost: inside_cost = 1, outside_cost = 0 .
vectBug.cc:21: note: vect_model_simple_cost: inside_cost = 1, outside_cost = 0 .
vectBug.cc:21: note: vect_model_store_cost: aligned.
vectBug.cc:21: note: vect_model_store_cost: inside_cost = 1, outside_cost = 0 .
vectBug.cc:21: note: Cost model analysis: 
  Vector inside of loop cost: 6
  Vector outside of loop cost: 0
  Scalar iteration cost: 8
  Scalar outside cost: 0
  prologue iterations: 0
  epilogue iterations: 0
  Calculated minimum iters for profitability: 1

vectBug.cc:21: note:   Profitability threshold = 3

vectBug.cc:21: note: LOOP VECTORIZED.
vectBug.cc:20: note: vectorized 1 loops in function.

vectBug.cc:27: note: not vectorized: control flow in loop.
vectBug.cc:26: note: vectorized 0 loops in function.


---


### compiler : `gcc`
### title : `extra move instruction for smmul`
### open_at : `2011-06-24T22:44:06Z`
### last_modified_date : `2021-08-16T08:13:06Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=49526
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.7.0`
### severity : `enhancement`
### contents :
$ cat test.c

int smmul(int a, int b) { return ((long long)a * b) >> 32; }

$ arm-none-linux-gnueabi-gcc -O2 -S -mcpu=cortex-a8 test.c
$ cat test.s
        .cpu cortex-a8
        .fpu softvfp
        .eabi_attribute 20, 1
        .eabi_attribute 21, 1
        .eabi_attribute 23, 3
        .eabi_attribute 24, 1
        .eabi_attribute 25, 1
        .eabi_attribute 26, 2
        .eabi_attribute 30, 2
        .eabi_attribute 18, 4
        .file   "test.c"
        .text
        .align  2
        .global smmul
        .type   smmul, %function
smmul:
        @ args = 0, pretend = 0, frame = 0
        @ frame_needed = 0, uses_anonymous_args = 0
        @ link register save eliminated.
        smull   r0, r1, r0, r1
        mov     r0, r1
        bx      lr
        .size   smmul, .-smmul
        .ident  "GCC: (GNU) 4.7.0 20110624 (experimental)"
        .section        .note.GNU-stack,"",%progbits


---


### compiler : `gcc`
### title : `missed optimization: test for zero remainder after division by a constant.`
### open_at : `2011-06-27T19:01:32Z`
### last_modified_date : `2019-02-09T09:42:31Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=49552
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.7.0`
### severity : `enhancement`
### contents :
Just like there are tricks to transform a division by a constant into a multiplication and some shifts, there are also tricks to test if the remainder of some division by a constant will be equal to zero.

Some examples:

bool is_mod3_zero(unsigned x)
{
    // equivalent to: return (x % 3) == 0;
    return (x * 0xaaaaaaab) <= (0xffffffff / 3);
}

bool is_mod28_zero(unsigned x)
{
    // equivalent to: return (x % 28) == 0;
    // return !(x & 3) && ((x * 0xb6db6db7) <= (0xffffffff / 7));
    return rotateRight(x * 0xb6db6db7, 2) <= (0xffffffff / 28);
}

bool is_signed_mod28_zero(int x)
{
    // equivalent to: return (x % 28) == 0;
    const unsigned c = (0x7fffffff / 7) & -(1 << 2);
    unsigned q = rotateRight((x * 0xb6db6db7) + c, 2);
    return q <= (c >> (2 - 1));
}


I found this trick in the book "Hacker's delight", chapter 10-16 "Test for Zero Remainder after Division by a Constant". The book also explains the theory behind this transformation.

It would be nice if gcc could automatically perform this optimization.



Bonus:

bool is_mod3_one(unsigned x)
{
    // equivalent to: return (x % 3) == 1;
    // only correct if 'x + 2' does not overflow
    //    (sometimes this can be derived from VRP)
    return ((x + (3 - 1)) * 0xaaaaaaab) <= (0xffffffff / 3);
}


---


### compiler : `gcc`
### title : `passing nested function to inline function causes a trampoline call`
### open_at : `2011-07-07T03:46:07Z`
### last_modified_date : `2021-12-25T22:37:46Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=49666
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.6.0`
### severity : `enhancement`
### contents :
#include <stdio.h>
static inline int identity(int (*f)()) {
  return f();
}

int n = 0;
int f() {
  return n;
}

int main() {
  int m = 0;
  int g() {
    return m;
  }
  printf("%d\n", identity(f)); /* inlines all the way */
  printf("%d\n", identity(g)); /* calls g through trampoline */
  printf("%d\n", g()); /* inline's g */
}


---


### compiler : `gcc`
### title : `conditional moves for stores`
### open_at : `2011-07-10T10:03:54Z`
### last_modified_date : `2023-05-19T07:44:24Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=49695
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.7.0`
### severity : `enhancement`
### contents :
for (i = 0; i < point1->len; i++)
    {
      if (point1->arr[i].val)
        {
          point1->arr[i].val ^= (unsigned long long) res;
        }
    }

For the above loop if-conversion is not been done in the tree level (compiled with trunk -r176116). Seemingly this case is similar to the one in PR27313.
When using -ftree-loop-if-convert-stores I get 'tree could trap...' message although I'm not sure why as there is a read in every iteration of the loop to the memory location we write to.
Similar case appears in SPEC2006/libquantum.

Here's a snippet from .ifcvt file:

<bb 3>:
  pretmp.6_33 = point1_3(D)->arr;

<bb 4>:
  # i_27 = PHI <i_22(7), 0(3)>
  i.0_6 = (unsigned int) i_27;
  D.3689_7 = i.0_6 * 8;
  D.3690_8 = pretmp.6_33 + D.3689_7;
  D.3691_9 = D.3690_8->val;
  if (D.3691_9 != 0)
    goto <bb 5>;
  else
    goto <bb 6>;

<bb 5>:
  D.3694_20 = (long long unsigned int) res_19(D);
  D.3695_21 = D.3694_20 ^ D.3691_9;
  D.3690_8->val = D.3695_21;

<bb 6>:
  i_22 = i_27 + 1;
  if (i_22 < D.3696_29)
    goto <bb 7>;
  else
    goto <bb 8>;

<bb 7>:
  goto <bb 4>;


---


### compiler : `gcc`
### title : `loop not vectorized if inside another loop`
### open_at : `2011-07-13T10:42:35Z`
### last_modified_date : `2021-12-04T23:58:02Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=49730
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.7.0`
### severity : `enhancement`
### contents :
I've this simple double loop (used in benchmark)
the inner loop (sloop) is not vectorized when invoked inside the longer loop (dloop)

 c++ -Ofast -c vectdloop.cc -ftree-vectorizer-verbose=7
vectdloop.cc:9: note:   Profitability threshold = 6

vectdloop.cc:9: note: Profitability threshold is 6 loop iterations.
vectdloop.cc:9: note: LOOP VECTORIZED.
vectdloop.cc:7: note: vectorized 1 loops in function.

vectdloop.cc:20: note: not vectorized: unexpected loop form.
vectdloop.cc:16: note: vectorized 0 loops in function.


#include<cmath>

inline float fn(float x) {
  return 2.f*x+std::sqrt(x);
}

void sloop(float * __restrict__ s, float const * __restrict__ xx) {
  const int ls=16;
  for (int j=0; j < ls; ++j) {
    s[j] = fn(xx[j]);
  } 
}

int dloop(float yyy) {
  int niter = 100000;
  float x = 0.5f; yyy=0;
  const int ls=16;
  for (int i=0; i < niter; ++i) { 
    float s[ls]; float xx[ls];
    for (int j=0; j < ls; ++j) xx[j] =x+(5*(j&1));
    sloop(s,xx);
    // for (int j=0; j < ls; ++j)  s[j] = fn(xx[j]); 
    x += 1e-6f;
    for (int j=0; j < ls; ++j) yyy+=s[j];
  }
  if (yyy == 2.32132323232f) niter--; 
  return niter;
}


---


### compiler : `gcc`
### title : `Missed optimization: Variable value not propagated to remove "if" condition`
### open_at : `2011-07-13T13:10:32Z`
### last_modified_date : `2019-11-22T10:07:41Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=49733
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.7.0`
### severity : `normal`
### contents :
Based on the discussion at http://gcc.gnu.org/ml/gcc/2011-07/msg00208.html.

In Fortran, the "if" condition can be removed in the following example as "call some_function()" may not modify it. This optimization is done by the Fortran compilers of NAG, Cray, Sun, Open64 and PathScale. But gfortran (and Intel's and PGI's compiler) do not optimize the "if" away, which can be seen from the presence of the "foobar_" function in the dump.


   subroutine sub(non_aliasing_var)
     interface
       subroutine some_function()
       end subroutine some_function
     end interface


     integer :: non_aliasing_var
     non_aliasing_var = 5
     call some_function()
     if (non_aliasing_var /= 5) call foobar_()
   end subroutine sub

Optimized dump:

sub (integer(kind=4) & restrict non_aliasing_var)
{
  integer(kind=4) D.1550;
<bb 2>:
  *non_aliasing_var_1(D) = 5;
  some_function ();
  D.1550_2 = *non_aliasing_var_1(D);
  if (D.1550_2 != 5)
    goto <bb 3>;
  else
    goto <bb 4>;
<bb 3>:
  foobar_ (); [tail call]
<bb 4>:
  return;
}


NOTE: Fortran has a case (coarrays, ASYNCHRONOUS), where the current behaviour is correct: That is, no aliasing of variables in the scoping unit, but the value might change due to asynchronous I/O / data communication (ASYNCHRONOUS) - or via one-sided communication (coarrays), where the "WAIT" or SYNC might be hidden in some function call. For those cases, the current behaviour with "restrict" is correct.
Cf. ASYNCHRONOUS: F2008, Sect. 5.3.4 and PDTR 29113 (ftp://ftp.nag.co.uk/sc22wg5/N1851-N1900/N1866.pdf)
Cf. Coarray: F2008; especially Section 8.5 and, in particular, Subsection 8.5.2.


Regarding the example above, one finds in the Fortran standard (F2008, ftp://ftp.nag.co.uk/sc22wg5/N1851-N1900/N1866.pdf) the following, which applies as the dummy argument "non_aliasing_var" is neither a POINTER nor has it the TARGET attribute.

"While an entity is associated with a dummy argument, the following restrictions hold.
[...]
"(3) Action that affects the value of the entity or any subobject of it shall be taken only through the dummy argument unless
(a) the dummy argument has the POINTER attribute or
(b) the dummy argument has the TARGET attribute, the dummy argument does not have INTENT(IN), the dummy argument is a scalar object or an assumed-shape array without the CONTIGUOUS attribute, and the actual argument is a target other than an array section with a vector subscript.

(4) If the value of the entity or any subobject of it is affected through the dummy argument, then at any time during the invocation and execution of the procedure, either before or after the definition, it may be referenced only through that dummy argument unless
(a) the dummy argument has the POINTER attribute or
(b) the dummy argument has the TARGET attribute, the dummy argument does not have INTENT(IN), the dummy argument is a scalar object or an assumed-shape array without the CONTIGUOUS attribute, and the actual argument is a target other than an array section with a
vector subscript."


---


### compiler : `gcc`
### title : `restrict keyword ignored if in structure`
### open_at : `2011-07-16T09:52:08Z`
### last_modified_date : `2022-12-26T06:39:29Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=49761
### status : `NEW`
### tags : `alias, missed-optimization`
### component : `tree-optimization`
### version : `4.7.0`
### severity : `enhancement`
### contents :
in this example no alias checks are generated for the first function while there are generated when inlined in the second and third functions.

Is it correct to declare an array "restricted" in a structure?

compiled with 
c++ -Wall -ftree-vectorizer-verbose=7 -Ofast -c 
gcc version 4.7.0 20110528 (experimental) (GCC) 

struct SoA {
  int *  __restrict__ a;
  float * __restrict__ b;
  float * __restrict__ c;
  int size;
};

struct SoB {
  int *  __restrict__ a;
  float * __restrict__ b;
  int size;
};

void loop(  int const *  __restrict__ in_a, 
	    float const * __restrict__ in_b,
	    float const * __restrict__ in_c,
	    int *  __restrict__ out_a,
	    float * __restrict__ out_b,
	    int N, int & k) {
  int j=k;
  for (int i=0; i!=N; ++i) {
    out_b[j] = in_c[i]+in_b[i];
    out_a[j] = in_a[i];
   ++ j;
  }
  k = j;
}


void loop2(SoA const & in, SoB & out, int & k) {
  loop(in.a,in.b,in.c,
       out.a,out.b, 
       in.size, k);
}

void loop3(SoA const & in, SoB & out, int & k) {
  int j=k;
  int N=in.size;
  for (int i=0; i!=N; ++i) {
    out.b[j] = in.c[i]+in.b[i];
    out.a[j] = in.a[i];
    ++j;
  }
  k = j;
}


---


### compiler : `gcc`
### title : `use of class data members prevent vectorization`
### open_at : `2011-07-18T07:19:37Z`
### last_modified_date : `2023-08-05T01:40:27Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=49773
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.7.0`
### severity : `enhancement`
### contents :
in this example below the loop in the first method does not vectorize, the second does.


struct Foo {
  float a;
  float b;

  void compute1(float * __restrict__ x, float const * __restrict__ y, int N) const;
  void compute2(float * __restrict__ x, float const * __restrict__ y, int N) const;

};

void Foo::compute1(float * __restrict__ x, float const * __restrict__ y, int N) const {
  for (int i=0; i!=N; ++i)
    x[i] = a + b*y[i];
}

void Foo::compute2(float * __restrict__ x, float const * __restrict__ y, int N) const {
  float la=a, lb=b;
  for (int i=0; i!=N; ++i)
    x[i] = la + lb*y[i];
}


test/vectClass.cpp:11: note: not vectorized: loop contains function calls or data references that cannot be analyzed
test/vectClass.cpp:10: note: vectorized 0 loops in function.
vs

test/vectClass.cpp:17: note: Profitability threshold is 5 loop iterations.
test/vectClass.cpp:17: note: LOOP VECTORIZED.
test/vectClass.cpp:15: note: vectorized 1 loops in function.


---


### compiler : `gcc`
### title : `Missed optimization due to dependency analysis`
### open_at : `2011-07-19T07:19:30Z`
### last_modified_date : `2021-08-11T03:04:04Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=49782
### status : `NEW`
### tags : `missed-optimization, wrong-code`
### component : `tree-optimization`
### version : `4.7.0`
### severity : `normal`
### contents :
In the pr49771.c testcase:

static int a[1000];

int
foo (void)
{
  int j;
  int i;
  for (i = 0; i < 1000; i++)
    for (j = 0; j < 1000; j++)
      a[j] = a[i] + 1;
  return a[0];
}

the dependency analysis doesn't figure out that a[i] for any i between 0 and 999
(but due to size of the array for any i) always overlaps the a[j] from 0 to 999.


---


### compiler : `gcc`
### title : `vectorization of conditional code happens only on local variables`
### open_at : `2011-07-20T11:45:08Z`
### last_modified_date : `2023-08-24T07:44:53Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=49795
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.7.0`
### severity : `enhancement`
### contents :
in this example loop1 does not vectorize, loop2 does 
const int N=64;
float c[N];
float d[N];

void loop1() {
  for (int i=0; i!=N; ++i) {
    if (c[i]<0) d[i] = -d[i];
  }
}

void loop2() {
  for (int i=0; i!=N; ++i) {
    float tmp = d[i];
    if (c[i]<0) tmp = -tmp;
    d[i]=tmp;
  }
}


---


### compiler : `gcc`
### title : `Missed byte (subreg) extraction when storing to volatile mem`
### open_at : `2011-07-21T19:31:48Z`
### last_modified_date : `2022-09-27T23:37:56Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=49807
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.6.1`
### severity : `enhancement`
### contents :
This C source:

#define SPDR (*((char volatile*) 0x2c))

void read_adc (long big)
{ 
   SPDR = big >> 24;
   SPDR = big >> 16;
   SPDR = big >> 8; 
   SPDR = big;
} 

compiles with 
   avr-gcc -S -Os -dp -mmcu=atmega8
to:

read_adc:
	movw r26,r24	 ;  2	*movsi/1	[length = 2]
	movw r24,r22
	mov r20,r27	 ;  28	*ashrsi3_const/3	[length = 6]
	clr r23
	sbrc r20,7
	com r23
	mov r21,r23
	mov r22,r23
	out 44-0x20,r20	 ;  9	*movqi/3	[length = 1]
	movw r20,r26	 ;  29	*ashrsi3_const/3	[length = 5]
	clr r23
	sbrc r21,7
	com r23
	mov r22,r23
	out 44-0x20,r20	 ;  13	*movqi/3	[length = 1]
	mov r20,r25	 ;  30	*ashrsi3_const/3	[length = 6]
	mov r21,r26
	mov r22,r27
	clr r23
	sbrc r22,7
	dec r23
	out 44-0x20,r20	 ;  17	*movqi/3	[length = 1]
	out 44-0x20,r24	 ;  20	*movqi/3	[length = 1]
	ret	 ;  26	return	[length = 1]

The shifts are done explicitely where the bytes could be saved directly.

Combiner tries insns like

Failed to match this instruction:
(set (mem/v:QI (const_int 44))
     (subreg:QI (reg:SI 49) 1))

But they don't match because of MEM_VOLATILE_P so that the MEM
does not match memory_operand as obviously volatile_ok is 0 at that moment.

Must the backend split such insns by hand?

Changing the source like

#define SPDR0 (*((char*) 0x2c))
#define SPDR1 (*((char*) 0x2d))
#define SPDR2 (*((char*) 0x2e))
#define SPDR3 (*((char*) 0x2f))

void read_adc (long big)
{ 
   SPDR0 = big >> 24;
   SPDR1 = big >> 16;
   SPDR2 = big >> 8;
   SPDR3 = big;
}


and it compiles fine:

read_adc:
	out 44-0x20,r25	 ;  8	*movqi/3	[length = 1]
	out 45-0x20,r24	 ;  11	*movqi/3	[length = 1]
	out 46-0x20,r23	 ;  14	*movqi/3	[length = 1]
	out 47-0x20,r22	 ;  16	*movqi/3	[length = 1]
	ret	 ;  26	return	[length = 1]


== configure ==

Target: avr
Configured with: ../../gcc.gnu.org/gcc-4_6-branch/configure --target=avr --prefix=/local/gnu/install/gcc-4.6-mingw32 --host=i586-mingw32 --build=i686-linux-gnu --enable-languages=c,c++ --disable-nls --disable-shared --with-dwarf2
Thread model: single
gcc version 4.6.1 20110620 (prerelease) (GCC)


---


### compiler : `gcc`
### title : `Use constants in registers preferably to inline constants (-Os)`
### open_at : `2011-07-25T13:20:17Z`
### last_modified_date : `2021-08-15T05:04:26Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=49839
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.6.1`
### severity : `enhancement`
### contents :
When GCC needs to zero out an integer in memory, and it already has one register at value zero, it takes less code bytes to write the register than inline a constant, i.e.:

etienne@etienne-server:~/projet$ gcc -v
Using built-in specs.
COLLECT_GCC=gcc
COLLECT_LTO_WRAPPER=/usr/lib/i386-linux-gnu/gcc/i486-linux-gnu/4.6.1/lto-wrapper
Target: i486-linux-gnu
Configured with: ../src/configure -v --with-pkgversion='Debian 4.6.1-4' --with-bugurl=file:///usr/share/doc/gcc-4.6/README.Bugs --enable-languages=c,c++,fortran,objc,obj-c++,go --prefix=/usr --program-suffix=-4.6 --enable-shared --enable-multiarch --with-multiarch-defaults=i386-linux-gnu --enable-linker-build-id --with-system-zlib --libexecdir=/usr/lib/i386-linux-gnu --without-included-gettext --enable-threads=posix --with-gxx-include-dir=/usr/include/c++/4.6 --libdir=/usr/lib/i386-linux-gnu --enable-nls --enable-clocale=gnu --enable-libstdcxx-debug --enable-libstdcxx-time=yes --enable-plugin --enable-objc-gc --enable-targets=all --with-arch-32=i586 --with-tune=generic --enable-checking=release --build=i486-linux-gnu --host=i486-linux-gnu --target=i486-linux-gnu
Thread model: posix
gcc version 4.6.1 (Debian 4.6.1-4) 

etienne@etienne-server:~/projet$ cat tmp.c
unsigned a, b;
unsigned fct (void)
  {
  a = b = 0;
  return 0;
  }
etienne@etienne-server:~/projet$ gcc -Os -fomit-frame-pointer tmp.c -c -o tmp.o
etienne@etienne-server:~/projet$ objdump -d tmp.o

tmp.o:     file format elf32-i386


Disassembly of section .text:

00000000 <fct>:
   0:	c7 05 00 00 00 00 00 	movl   $0x0,0x0
   7:	00 00 00 
   a:	31 c0                	xor    %eax,%eax
   c:	c7 05 00 00 00 00 00 	movl   $0x0,0x0
  13:	00 00 00 
  16:	c3                   	ret    
etienne@etienne-server:~/projet$ 

It would be shorter to get this assembly:
0:    31 c0                	xor    %eax,%eax
2:    a3 00 00 00 00            mov    %eax,a
7:    a3 00 00 00 00            mov    %eax,b
c:    c3                        ret

Regards,
Etienne.


---


### compiler : `gcc`
### title : `loop optimization prevents vectorization`
### open_at : `2011-07-26T07:45:57Z`
### last_modified_date : `2021-09-12T05:21:11Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=49849
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.7.0`
### severity : `normal`
### contents :
In the following example I suspect that some sort of loop merging at O3 prevent the optimization of the second inner loop in "bar"
compare
c++ -Wall -O2 -ftree-vectorize -ftree-vectorizer-verbose=7 -c vectHist.cpp -ffast-math
c++ -Wall -O3 -ftree-vectorize -ftree-vectorizer-verbose=7 -c vectHist.cpp -ffast-math



what I do not understand is that if (following man page) I compare O2 and O3 with
gcc -c -Q -O3 --help=optimizers > /tmp/O3-opts
gcc -c -Q -O2 --help=optimizers > /tmp/O2-opts
diff /tmp/O2-opts /tmp/O3-opts | grep enabled
>   -fgcse-after-reload         		[enabled]
>   -finline-functions          		[enabled]
>   -fipa-cp-clone              		[enabled]
>   -fpredictive-commoning      		[enabled]
>   -ftree-loop-distribute-patterns 	[enabled]
>   -ftree-vectorize            		[enabled]
>   -funswitch-loops            		[enabled]

I still get
c++ -std=gnu++0x -DNDEBUG -Wall -O2 -ftree-vectorize -msse4 -fvisibility-inlines-hidden -ftree-vectorizer-verbose=2 --param vect-max-version-for-alias-checks=30 -funsafe-loop-optimizations -ftree-loop-distribution -ftree-loop-if-convert-stores -fipa-pta -Wunsafe-loop-optimizations -fgcse-sm -fgcse-las -c vectHist.cpp -ffast-math -funswitch-loops -ftree-loop-distribute-patterns -fpredictive-commoning -finline-functions -fipa-cp-clone -fgcse-after-reload

vectHist.cpp:17: note: not vectorized: data ref analysis failed x_5 = co[D.4986_4];

vectHist.cpp:16: note: vectorized 0 loops in function.

vectHist.cpp:35: note: not vectorized: data ref analysis failed D.4977_30 = hist[D.4976_29];

vectHist.cpp:33: note: LOOP VECTORIZED.
vectHist.cpp:31: note: not vectorized: data ref analysis failed D.4957_13 = co[D.4956_12];

vectHist.cpp:25: note: vectorized 1 loops in function.

while changing just O2 in 03 (that at this point should be not really effective as I added all options by hand) does not vectorize…
c++ -std=gnu++0x -DNDEBUG -Wall -O3 -mavx -ftree-vectorize -msse4 -fvisibility-inlines-hidden -ftree-vectorizer-verbose=2 --param vect-max-version-for-alias-checks=30 -funsafe-loop-optimizations -ftree-loop-distribution -ftree-loop-if-convert-stores -fipa-pta -Wunsafe-loop-optimizations -fgcse-sm -fgcse-las -c vectHist.cpp -ffast-math -funswitch-loops -ftree-loop-distribute-patterns -fpredictive-commoning -finline-functions -fipa-cp-clone -fgcse-after-reload 
vectHist.cpp:17: note: not vectorized: data ref analysis failed x_5 = co[D.5125_4];

vectHist.cpp:17: note: not vectorized: data ref analysis failed x_5 = co[D.5125_4];

vectHist.cpp:16: note: vectorized 0 loops in function.

vectHist.cpp:30: note: not vectorized: data ref analysis failed D.5096_55 = co[D.5095_54];

vectHist.cpp:30: note: not vectorized: data ref analysis failed D.5096_55 = co[D.5095_54];

vectHist.cpp:25: note: vectorized 0 loops in function.

note how it does not report anything about loops at lines 31,33 and 35

---------------------------
// a classroom example
#include<cmath>

const int N=1024;

float __attribute__ ((aligned(16))) a[N];
float __attribute__ ((aligned(16))) b[N];
float __attribute__ ((aligned(16))) c[N];
float __attribute__ ((aligned(16))) d[N];
int __attribute__ ((aligned(16)))   k[N];



float __attribute__ ((aligned(16))) co[12];
float __attribute__ ((aligned(16))) hist[100];


// do not expect GCC to vectorize (yet)
void foo() {
  for (int i=0; i!=N; ++i) {
    float x = co[k[i]];
    float y = a[i]/std::sqrt(x*b[i]);
    ++hist[int(y)];
  } 
}


// let's give it an hand: split the loop so that the "heavy duty one" vectorize
void bar() {
  const int S=8;
  int loops = N/S;
  float x[S];
  float y[S];
  for (int j=0; j!=loops; ++j) {
    for (int i=0; i!=S; ++i)
      x[i] = co[k[j+i]];
    for (int i=0; i!=S; ++i) // this should vectorize
      y[i] = a[j+i]/std::sqrt(x[i]*b[j+i]);
    for (int i=0; i!=S; ++i)
      ++hist[int(y[i])];
  } 
}


---


### compiler : `gcc`
### title : `[4.7 Regression] Unnecessary reload causes small bloat`
### open_at : `2011-07-27T11:24:54Z`
### last_modified_date : `2019-09-24T04:19:29Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=49865
### status : `RESOLVED`
### tags : `missed-optimization, ra`
### component : `target`
### version : `4.7.0`
### severity : `minor`
### contents :
Comparing 4.6.1 with gcc-snapshot from Debian:

gcc version 4.7.0 20110709 (experimental) [trunk revision 176106] (Debian 20110709-1) 

Given this code:

fugl:~> cat test.cpp 
#include <string.h>

class MyClass {
	void func();

        float f[1024];
        int i;
};

void MyClass::func()
{
	memset(f, 0, sizeof(f));
	i = 0;
}

and compiling with

fugl:~> /usr/lib/gcc-snapshot/bin/g++ -Os -c test.cpp

g++ produces, according to objdump:

00000000 <_ZN7MyClass4funcEv>:
   0:	55                   	push   %ebp
   1:	31 c0                	xor    %eax,%eax
   3:	89 e5                	mov    %esp,%ebp
   5:	b9 00 04 00 00       	mov    $0x400,%ecx
   a:	57                   	push   %edi
   b:	8b 7d 08             	mov    0x8(%ebp),%edi
   e:	f3 ab                	rep stos %eax,%es:(%edi)
  10:	8b 45 08             	mov    0x8(%ebp),%eax
  13:	c7 80 00 10 00 00 00 	movl   $0x0,0x1000(%eax)
  1a:	00 00 00 
  1d:	5f                   	pop    %edi
  1e:	5d                   	pop    %ebp
  1f:	c3                   	ret    

while 4.6.1 has a more efficient sequence:

00000000 <_ZN7MyClass4funcEv>:
   0:	55                   	push   %ebp
   1:	b9 00 04 00 00       	mov    $0x400,%ecx
   6:	89 e5                	mov    %esp,%ebp
   8:	31 c0                	xor    %eax,%eax
   a:	8b 55 08             	mov    0x8(%ebp),%edx
   d:	57                   	push   %edi
   e:	89 d7                	mov    %edx,%edi
  10:	f3 ab                	rep stos %eax,%es:(%edi)
  12:	c7 82 00 10 00 00 00 	movl   $0x0,0x1000(%edx)
  19:	00 00 00 
  1c:	5f                   	pop    %edi
  1d:	5d                   	pop    %ebp
  1e:	c3                   	ret   

It seems 4.6 is able to take a copy of the "this" pointer from a register before the "rep stos" operation, which is one byte smaller than reloading it from the stack when it needs to clear "i".

Of course, the _most_ efficient code sequence here would be doing the i = 0 before the memset, but I'm not sure if this is legal. However, eax should still contain zero, so the mov could be done from eax instead of from a constant.


---


### compiler : `gcc`
### title : `Excessive loop versioning done by vectorization + predictive commoning`
### open_at : `2011-07-27T14:20:09Z`
### last_modified_date : `2021-08-06T07:33:11Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=49869
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.7.0`
### severity : `normal`
### contents :
SUBROUTINE ANYAVG(NLVLS,HTS,PARRAY,ZBOT,NDXABV,ZTOP,NDXBLW,VALAVG)
      IMPLICIT NONE
      INTEGER I , NLVLS , NDXABV , NDXBLW
      REAL HTS(NLVLS) , PARRAY(NLVLS) , ZBOT , ZTOP , SUM , VALAVG
      REAL VALBOT , VALTOP
      IF ( ZBOT.LT.0.5 ) THEN
         ZBOT = 0.5
         NDXABV = 2
      ENDIF
      IF ( ZTOP.LT.0.51 ) THEN
         ZTOP = 0.51
         NDXBLW = 2
      ENDIF
      IF ( NDXBLW.LE.NDXABV ) GOTO 200
      DO I = NDXABV + 1 , NDXBLW
         SUM = SUM + (HTS(I)-HTS(I-1))*0.5*(PARRAY(I)+PARRAY(I-1))
      ENDDO
 200  CONTINUE
      VALAVG = SUM/(ZTOP-ZBOT)
      END

ends up with 5 loop copies.


---


### compiler : `gcc`
### title : `Missed optimization: Could coalesce neighboring memsets`
### open_at : `2011-07-27T16:51:03Z`
### last_modified_date : `2021-08-21T23:57:14Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=49872
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.7.0`
### severity : `enhancement`
### contents :
Given the following code:

#include <string.h>

struct S {
	int f[1024];
	int g[1024];
};

void func(struct S* s)
{
	memset(s->f, 0, sizeof(s->f));
	memset(s->g, 0, sizeof(s->g));
}

GCC currently generates two memsets. The code with -O2 is a bit hard to read, so I'm just pasting the -Os assembly for clarity:

00000000 <func>:
   0:	55                   	push   %ebp
   1:	31 c0                	xor    %eax,%eax
   3:	89 e5                	mov    %esp,%ebp
   5:	b9 00 04 00 00       	mov    $0x400,%ecx
   a:	57                   	push   %edi
   b:	8b 7d 08             	mov    0x8(%ebp),%edi
   e:	f3 ab                	rep stos %eax,%es:(%edi)
  10:	8b 55 08             	mov    0x8(%ebp),%edx
  13:	66 b9 00 04          	mov    $0x400,%cx
  17:	81 c2 00 10 00 00    	add    $0x1000,%edx
  1d:	89 d7                	mov    %edx,%edi
  1f:	f3 ab                	rep stos %eax,%es:(%edi)
  21:	5f                   	pop    %edi
  22:	5d                   	pop    %ebp
  23:	c3                   	ret    

Ideally GCC should also be able to coalesce this together with memsets not written as memset, e.g. s->g[0] = 0;.


---


### compiler : `gcc`
### title : `Thread jumps confuse loop unrolling`
### open_at : `2011-08-02T14:40:57Z`
### last_modified_date : `2021-12-09T09:30:40Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=49946
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `unknown`
### severity : `enhancement`
### contents :
Created attachment 24892
test for loop unrolling

I see exactly the case that was mentioned here - http://gcc.gnu.org/ml/gcc/2010-01/msg00057.html:

exp_gcc/gcc -c -O3 test_unroll.c -fno-tree-dominator-opts performs complete unroll and

exp_gcc/gcc -c -O3 test_unroll.c does not do the unroll


---


### compiler : `gcc`
### title : `GOT relocation for -fPIE is excessive`
### open_at : `2011-08-02T19:43:47Z`
### last_modified_date : `2021-08-02T17:54:21Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=49950
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.4.7`
### severity : `minor`
### contents :
FAIL: gcc (GCC) 4.4.7 20110802 (prerelease)
FAIL: gcc (GCC) 4.5.4 20110802 (prerelease)
FAIL: gcc (GCC) 4.6.2 20110802 (prerelease)
FAIL: gcc (GCC) 4.7.0 20110802 (experimental)

echo 'int i; int f (void) { return i; }' | gcc -c -o 20.o -Wall -fPIE -x c -
readelf -Wr 20.o
0000000000000007  0000000800000009 R_X86_64_GOTPCREL      0000000000000004 i - 4

none:  R_X86_64_PC32     is correct
-fPIE: R_X86_64_GOTPCREL is excessive - this Bug
-fPIC: R_X86_64_GOTPCREL is correct

Jakub:
the difference between -fPIE and -fPIC is that the former assumes that you can't override its symbols
so if it sees some symbol defined in the current source file, it knows that it will be the definition at runtime
for -shared libraries that is not true, other shared libraries defining the same symbol can override it, so they need more runtime relocations


---
