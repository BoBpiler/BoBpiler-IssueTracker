### Total Bugs Detected: 4649
### Current Chunk: 2 of 30
### Bugs in this Chunk: 160 (From bug 161 to 320)
---


### compiler : `gcc`
### title : `struct whos size is > 64bit is always on the stack`
### open_at : `2005-12-02T18:13:51Z`
### last_modified_date : `2021-08-16T01:07:00Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=25227
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.2.0`
### severity : `enhancement`
### contents :
The following test program spills res onto the stack when the value res.result, which is already in a register, should be passed in a register to 
foo();

/* compile with: gcc -fomit-frame-pointer -S */
struct rw_res {
        long result;
        long pos_update;
};

struct file {
        long f_pos;
};

struct rw_res vfs_read(long pos);
long foo(long bar);

long sys_read(struct file *file)
{
        struct rw_res res;
        res = vfs_read(file->f_pos);
        return foo(res.result);
}


---


### compiler : `gcc`
### title : `__sync_add_and_fetch does not use condition flags from subl`
### open_at : `2005-12-02T20:09:16Z`
### last_modified_date : `2021-07-26T05:22:34Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=25230
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.2.0`
### severity : `enhancement`
### contents :
The program below should generate code that looks something like:

fput:
 addl $-1,(%rdi)
 jne .L4
 jmp release
.L4:
 ret

But instead generates:

fput:
        movl    $-1, %eax
        lock
        xaddl   %eax, (%rdi)
        decl    %eax
        jne     .L4
        jmp     release
        .p2align 4,,7
.L4:
        rep ; ret

test program:
struct file {
        int counter;
};

void release(struct file *file);

void fput(struct file *file)
{
        if (__sync_add_and_fetch(&file->counter, -1) == 0)
                release(file);
}


---


### compiler : `gcc`
### title : `PPC has conditional indirect jumps if ra allocates the a in ctr before the jumps`
### open_at : `2005-12-06T21:07:20Z`
### last_modified_date : `2022-03-08T16:20:47Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=25287
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.2.0`
### severity : `enhancement`
### contents :
Code:
int f(void *a, int b)
{
  if (b ==1) goto *a;
  g();
  if (b ==2) goto *a;
  g();
  return 1
}

This is very minor but I thought it would be cool if GCC could do something like:
.f:
        mflr %r0
        cmpwi %cr7,%r4,1
        std %r30,-16(%r1)
        std %r31,-8(%r1)
        mr %r30,%r3
        mr %r31,%r4
        std %r0,16(%r1)
        stdu %r1,-128(%r1)
        mtctr %r30
        beqctr %cr7,.L3
        bl .g
        nop
        cmpwi %cr7,%r31,2
        mtctr %r30
        beqctr %cr7,.L3
        bl .g
        li %r3
        blr
.L3:
        mtctr %r30
        bctr


---


### compiler : `gcc`
### title : `PHI-OPT could be rewritten so that is uses match`
### open_at : `2005-12-07T03:10:24Z`
### last_modified_date : `2023-10-21T21:31:47Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=25290
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.2.0`
### severity : `enhancement`
### contents :
PHI-OPT could be rewritten so that it uses fold_ternary (type, COND_EXPR, cond, op1, op2) and that it could remove code which is already done in fold_ternary.

A patch like
http://gcc.gnu.org/ml/gcc-patches/2004-06/msg00153.html
will work but it needs to be reworked for the changes which made it into 4.1.


---


### compiler : `gcc`
### title : `Suboptimal code generated for comparisons`
### open_at : `2005-12-18T22:36:46Z`
### last_modified_date : `2021-07-19T23:39:23Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=25489
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.0.2`
### severity : `normal`
### contents :
This code:

typedef struct {
  int protected_mode;
  int x;
} TScreen;

extern void ClearRight (TScreen *screen, int n);
extern void ClearLeft(TScreen * screen);
extern void ClearLine(TScreen * screen);

void
do_erase_line(TScreen * screen, int param, int mode)
{
    int saved_mode = screen->protected_mode;

    if (saved_mode == 1
	&& saved_mode != mode)
	screen->protected_mode = 0;

    switch (param) {
    case -1:			/* DEFAULT */
    case 0:
	ClearRight(screen, -1);
	break;
    case 1:
	ClearLeft(screen);
	break;
    case 2:
	ClearLine(screen);
	break;
    }
    screen->protected_mode = saved_mode;
}

is compiled to: (when using -O2 -mcpu=ultrasparc using gcc-4.0.2 and gcc-4.2)
do_erase_line:
	save	%sp, -112, %sp
	ld	[%i0], %l0
	xor	%l0, 1, %g1     <- from here
	xor	%l0, %i2, %i2
	subcc	%g0, %g1, %g0
	subx	%g0, -1, %g2
	subcc	%g0, %i2, %g0
	addx	%g0, 0, %g1
	andcc	%g2, %g1, %g0   <- to here
	bne,a,pt %icc, .LL2
	 st	%g0, [%i0]
.LL2:
	cmp	%i1, 1
	be,pn	%icc, .LL6
	 nop
[snip]


The code generated for the "if" can be better implemented
as (pseudoassembly):
 xor save_mode, 1, tmp1
 xnor save_mode, mode, tmp2
 orcc tmp1, tmp2

I don't know if this is a Sparc specific problem, or a general problem.


---


### compiler : `gcc`
### title : `Missed optimization when unrolling the loop (splitting up the sum) (only with -ffast-math)`
### open_at : `2006-01-01T12:40:07Z`
### last_modified_date : `2023-09-23T21:08:40Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=25621
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.2.0`
### severity : `enhancement`
### contents :
The following doesn't run as fast as the 'hand-optimised' routine provided as well (using current 4.2 on an opteron) using -ffast-math -O2 (makes a factor of 2 difference here). I've tried a number of further switches, but didn't manage to find a case where the simply loop was as fast as the other. 

! simple loop
! assume N is even
SUBROUTINE S31(a,b,c,N)
 IMPLICIT NONE
 integer :: N
 real*8  :: a(N),b(N),c
 integer :: i
 c=0.0D0
 DO i=1,N
   c=c+a(i)*b(i)
 ENDDO
END SUBROUTINE

! 'improved' loop
SUBROUTINE S32(a,b,c,N)
 IMPLICIT NONE
 integer :: N
 real*8  :: a(N),b(N),c,tmp
 integer :: i
 c=0.0D0
 tmp=0.0D0
 DO i=1,N,2
    c=c+a(i)*b(i)
    tmp=tmp+a(i+1)*b(i+1)
 ENDDO
 c=c+tmp
END SUBROUTINE


---


### compiler : `gcc`
### title : `VRP does not remove -fbounds-check for Fortran`
### open_at : `2006-01-02T19:54:10Z`
### last_modified_date : `2023-09-03T20:06:33Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=25643
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.2.0`
### severity : `enhancement`
### contents :
Testcase:
subroutine mysub(n,v)
  integer :: n
  real    :: v(n)

  if (n<=0) return
  do i=1, n
    v(i) = i*i
  end do
  return
end subroutine mysub
------
Compile with -fbounds-checking -O2, and notice that there is still _gfortran_runtime_error left in the asm.


---


### compiler : `gcc`
### title : `test_bit() compilation does not expand to "bt" instruction`
### open_at : `2006-01-04T15:24:53Z`
### last_modified_date : `2021-08-19T20:49:32Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=25671
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.0.2`
### severity : `enhancement`
### contents :
the code

int test_bit(unsigned long *words, int bit)
{
    int wsize = (sizeof *words) * 8;
    return (words[bit / wsize] & (1 << (bit % wsize))) != 0;
}

can compile to

    xor %rax, %rax
    bt  %rsi, (%rdi)
    setc %al

but instead compiles to a much longer sequence, using many more registers, which is probably slower as well. If gcc recognized this common idiom (like it recognizes bit rotate sequences), smaller and more optimal code would be generated (especially if the result of the test is in an if statement - it could boil down to a bt; jc sequence).


---


### compiler : `gcc`
### title : `[meta-bug] missed optimization in SPEC (2k17, 2k and 2k6 and 95)`
### open_at : `2006-02-07T18:16:22Z`
### last_modified_date : `2023-09-27T22:14:26Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=26163
### status : `NEW`
### tags : `meta-bug, missed-optimization`
### component : `middle-end`
### version : `4.2.0`
### severity : `enhancement`
### contents :
Just a meta-bug for all the missed optimizations that are known currently in the SPEC benchmarks.


---


### compiler : `gcc`
### title : `combine misses some distributivity`
### open_at : `2006-02-09T09:06:34Z`
### last_modified_date : `2023-10-12T03:33:42Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=26190
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.2.0`
### severity : `enhancement`
### contents :
In this code,

  unsigned short
  crc (unsigned short crc, unsigned char data)
  {
    unsigned char i, x16;
    for (i = 0; i < 8; i++)
      {
        x16 = (data ^ (unsigned char) crc) & 1;
        data >>= 1;
        if (x16)
          {
            crc ^= 0x4002;
            crc >>= 1;
            crc |= 0x8000;
          }
        else
          crc >>= 1;
      }
    return crc;
  }

the `then' branch of the if-statement should become

  crc >>= 1;
  crc ^= 0xA001;

Seems related to bug 16798.

Paolo


---


### compiler : `gcc`
### title : `suboptimal register allocation for return register`
### open_at : `2006-02-27T04:50:12Z`
### last_modified_date : `2022-02-06T09:39:57Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=26479
### status : `NEW`
### tags : `missed-optimization, ra`
### component : `rtl-optimization`
### version : `4.2.0`
### severity : `enhancement`
### contents :
For this code, at -O2, R13 is needlessly used, where R10 would suffice.
(Leading to two extra move insns.)  Curiously, if-conversion exposes
the suboptimal allocation; with -fno-if-conversion you get the better
allocation, but looking at the assembled code, there's no reason to not
use r10.  Observed with 108225 and 111226.  Code is from bzip2recover.c.

extern int _IO_getc (void *) ;
extern int *__errno_location (void) __attribute__ ((__const__));
void readError ( void );
typedef
   struct {
      void* handle;
      int buffer;
      int buffLive;
      char mode;
   }
   BitStream;

int bsGetBit ( BitStream* bs )
{  
   if (bs->buffLive > 0) {
      bs->buffLive --;
      return ( ((bs->buffer) >> (bs->buffLive)) & 0x1 );
   } else {
      int retVal = _IO_getc (bs->handle);
      if ( retVal == (-1) ) {
         if ((*__errno_location ()) != 0) readError();
         return 2;
      }
      bs->buffLive = 7;
      bs->buffer = retVal;
      return ( ((bs->buffer) >> 7) & 0x1 );
   }
}


---


### compiler : `gcc`
### title : `Storing float to int into two different pointers requires stack space`
### open_at : `2006-03-01T05:21:49Z`
### last_modified_date : `2022-03-08T16:20:39Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=26505
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.2.0`
### severity : `enhancement`
### contents :
Testcase (modified from testcase which Chris Latter was looking at):
void foo(float a, int *b) { b[0] = b[1] = a; }
----
Currently we get:
        fctiwz f0,f1
        addi r2,r1,-24
        stfiwx f0,0,r2
        lwz r0,-24(r1)
        stw r0,0(r4)
        stw r0,4(r4)

------
We should be able to get:
fctiwz f0,f1
stfiwx f0,0,r4
li r2, 4
stfiwx f0,r2,r4
---- or -----
fctiwz f0,f1
stfiwx f0,0,r4
addi r4, r4, 4
stfiwx f0,0,r4
Depending on a lot of stuff
I don't know how much this shows up in real code.


---


### compiler : `gcc`
### title : `missed optimization with respect of vector intrinsics`
### open_at : `2006-03-03T11:44:26Z`
### last_modified_date : `2021-12-06T23:49:13Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=26546
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.8.0`
### severity : `enhancement`
### contents :
Consider this example:

#include <xmmintrin.h>

typedef union
{
  __m128 vec;
  float data[4];
  struct
  {
    float x,y,z,w;
  };
} vec4f_t;

static inline float __attribute__((__always_inline__))
acc(vec4f_t src)
{
  float a;
  src.vec = _mm_add_ps(src.vec, _mm_movehl_ps(src.vec, src.vec,));
  _mm_store_ss(&a, _mm_add_ss(src.vec, _mm_shuffle_ps(src.vec, src.vec, _MM_SHUFFLE(3,2,1,1))));
  return a;
}

int
main(int argc, char *argv[])
{
  vec4f_t b;
  printf("%f\n", acc(b));
  return 0;
}

This gets compiled to:

        .section        .rodata.str1.1,"aMS",@progbits,1
.LC0:
        .string "%f\n"
        .text
        .p2align 4,,15
.globl main
        .type   main, @function
main:
.LFB506:
        subq    $40, %rsp
.LCFI0:
        movl    $.LC0, %edi
        movq    16(%rsp), %rax
        movq    %rax, (%rsp)
        movq    24(%rsp), %rax
        movq    %rax, 8(%rsp)
        movl    $1, %eax
        movaps  (%rsp), %xmm1
        movaps  %xmm1, %xmm0
        movhlps %xmm1, %xmm0
        addps   %xmm1, %xmm0
        movaps  %xmm0, %xmm1
        shufps  $229, %xmm0, %xmm1
        addss   %xmm1, %xmm0
        cvtss2sd        %xmm0, %xmm0
        call    printf
        xorl    %eax, %eax
        addq    $40, %rsp
        ret

As we can see the union is passed on the stack instead of a value in %xmm0 this would make sense if this would not be an inline function and members other than the __m128 would be accessed.

Using the same code as above but passing __m128 directly instead of the union gets compiled to:

        .section        .rodata.str1.1,"aMS",@progbits,1
.LC0:
        .string "%f\n"
        .text
        .p2align 4,,15
.globl main
        .type   main, @function
main:
.LFB506:
        movhlps %xmm0, %xmm0
        subq    $8, %rsp
.LCFI0:
        movl    $.LC0, %edi
        movl    $1, %eax
        addps   %xmm0, %xmm0
        movaps  %xmm0, %xmm1
        shufps  $229, %xmm0, %xmm1
        addss   %xmm1, %xmm0
        cvtss2sd        %xmm0, %xmm0
        call    printf
        xorl    %eax, %eax
        addq    $8, %rsp
        ret


---


### compiler : `gcc`
### title : `Optimization flaw on conditional set of a bit.`
### open_at : `2006-03-12T19:11:11Z`
### last_modified_date : `2021-07-26T19:18:39Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=26656
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `3.4.5`
### severity : `enhancement`
### contents :
I'm on Gentoo Linux, my the use flags affecting GCC are "fortran" and "nls". I have tried the following with -O2. If I write a piece of code that looks like one of these :
example 1 : a = (b == 1 ? 1 : 0);
example 2 : a = (b == 1 ? 2 : 0);
example 3 : if( b == 1 )
                a = 2;
            else
                a = 0;

The compiler optimizes it by using the sete/setne instruction instead of a potentially slow conditional jump and then doing a bit shift if necessary. However, while code like
example 4 : a |= (b == 1 ? 1 : 0)
example 5 : if( b == 1 )
                a |= 1;

is optimized the same way, code like 
example 4 : a |= (b == 1 ? 2 : 0)
example 5 : if( b == 1 )
                a |= 2;

is not optimized with a sete/setne, a conditional jump is used. Since there is a workaround to make GCC use a sete/setne
workaround : t = (b == 1 ? 2 : 0);  // or if( b == 1 ) t = 2; else t = 0;
             a |= 2;

I could compare the performance of sete/setne like operations vs conditional jumps on my AMD Ahlon XP 1700+. It turns out that, without -march=athlon-xp, the workaround, using a if() or a ?: as constant speed that is faster than code like example 4 and 5, except when the probability is very close to 1/2. The further from 1/2, the slower, on the extreme, it can be more than 2x slower. At 1/2, the conditional jump is faster, but not by much. For some reason, code like example 4 is slower than code like example 5.
With -march=athlon-xp, code like example 5 and the workaround behaves the same, but code like example 4 as a constant time that is however slower than the workaround but faster than most other cases when compiled without -march=athlon-xp. Disassembly shows that it is using a conditional move.


---


### compiler : `gcc`
### title : `__builtin_constant_p fails to recognise function with constant return`
### open_at : `2006-03-17T07:06:26Z`
### last_modified_date : `2023-04-11T08:28:44Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=26724
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.2.0`
### severity : `enhancement`
### contents :
We noticed that __builtin_constant_p() sometimes fails to recognise a function that always returns 0 as being constant.

The code snippet below shows that gcc can work it out if we force the evaluation into an inline function. It looks like this postpones the evaluation of __builtin_constant_p to a later stage when we know the function always returns 0.

static inline int baz(void)
{
        return 0;
}

void inline foo(int A)
{
        if (!__builtin_constant_p(A))
                FAIL();
}

void good()
{
        foo(baz());
}

void bad()
{
        if (!__builtin_constant_p(baz()))
                FAIL();
}


---


### compiler : `gcc`
### title : `Jump threading gets in the way of loops`
### open_at : `2006-03-17T17:31:31Z`
### last_modified_date : `2023-08-07T08:23:48Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=26731
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.2.0`
### severity : `enhancement`
### contents :
Jump threading causes bad interactions with loops:
int f(int t, int a, int x)
{
  int n, g;
  if (t)
   n = a;
  else
   n = 4;
  for (g=0; g<n; g++)
    x++;
  return x;
}

This should be optimized to:
int f(int t, int a, int x)
{
  int n, g;
  if (t)
   n = a;
  else
   n = 4;
  x+=n;
  return x;
}
But is not because of jump threading getting in the way to dect that the loop is finite.


---


### compiler : `gcc`
### title : `missed optimization during x87 args load with inline-asm`
### open_at : `2006-03-28T14:54:58Z`
### last_modified_date : `2021-09-13T21:14:16Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=26902
### status : `UNCONFIRMED`
### tags : `inline-asm, missed-optimization`
### component : `target`
### version : `4.1.1`
### severity : `enhancement`
### contents :
double plus_1( double x )
{
    asm volatile
    (
        "fadd %2"
        : "=t" (x)
        : "0" (x), "u" (1.0)
    );
    return x;
}

with -fomit-frame-pointer gcc produces:

plus_1:
        fldl    4(%esp)     \
        fld1                 |- why just not "fld1 ; fldl 4(%esp)" ?
        fxch    %st(1)      /
#APP
        fadd %st(1)
#NO_APP
        fstp    %st(1)
        ret


---


### compiler : `gcc`
### title : `lack of conditional moves with floating point`
### open_at : `2006-03-29T10:30:11Z`
### last_modified_date : `2019-03-05T16:19:51Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=26914
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.1.1`
### severity : `enhancement`
### contents :
flags: -O2 -ffast-math -march=i686 -fomit-frame-pointer

double signum_dbl_gcc( double x )
{
    if ( x < 0.0 )
        return -1.0;
    if ( x > 0.0 )
        return 1.0;
    return 0.0;
}

.LC1:   .long   3212836864

signum_dbl_gcc:
        fldz
        fldl    4(%esp)
        fcomip  %st(1), %st
        jb      .L11
        fld1
        fcmovbe %st(1), %st
        fstp    %st(1)
        ret
.L11:   fstp    %st(0)
        flds    .LC1
        ret

int signum_int_gcc( int x )
{
    if ( x < 0 )
        return -1;
    if ( x > 0 )
        return 1;
    return 0;
}

signum_int_gcc:
        cmpl    $0, 4(%esp)
        movl    $-1, %eax
        jl      .L15
        setne   %al
        movzbl  %al, %eax
.L15:   ret


custom version without branches.

double signum_user_dbl( double x )
{
    asm volatile
    (
        "fld1                                   \n\t"
        "fchs                                   \n\t"
        "fld1                                   \n\t"
        "fldz                                   \n\t"
        "fucomi         %%st(3)                 \n\t"
        "fcmovnbe       %%st(2), %%st(0)        \n\t"
        "fcmovb         %%st(1), %%st(0)        \n\t"
        "fstp           %%st(1)                 \n\t"
        "fstp           %%st(1)                 \n\t"
        "fstp           %%st(1)                 \n\t"
        : "=t" (x)
        : "0" (x)
    );
    return x;
}

int signum_user_int( int x )
{
    int retval;
    asm volatile
    (
        "xor            %%al, %%al      \n\t"
        "mov            $-1, %%cl       \n\t"
        "mov            $1, %%dl        \n\t"
        "cmp            $0, %1          \n\t"
        "cmovl          %%ecx, %%eax    \n\t"
        "cmovg          %%edx, %%eax    \n\t"
        "movsx          %%al, %%eax     \n\t"
        : "=a" (retval)
        : "m" (x)
    );
    return retval;
}


---


### compiler : `gcc`
### title : `missed sized opt returning -1.0`
### open_at : `2006-03-29T10:42:45Z`
### last_modified_date : `2021-10-18T11:18:55Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=26915
### status : `RESOLVED`
### tags : `missed-optimization, patch`
### component : `target`
### version : `4.1.1`
### severity : `enhancement`
### contents :
double minus1() { return -1.0; }

.LC0:    .long   3212836864
minus1:  flds    .LC0
         ret

for -Os gcc should use `fld1;fchs'.


---


### compiler : `gcc`
### title : `loop number of iterations analysis not working`
### open_at : `2006-03-30T11:06:41Z`
### last_modified_date : `2021-11-28T04:22:29Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=26939
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.2.0`
### severity : `minor`
### contents :
/* { dg-do compile } */
/* { dg-options "-O2 -fdump-tree-sccp-details" } */

void bar(int);
void foo(int i1, int j1)
{
  int i, j;

  for (j=0; j<=j1; ++j)
    for (i=0; i<=i1; ++i)
      bar(j+1);
}

/* { dg-final { scan-tree-dump-not "set_nb_iterations_in_loop = scev_not_known" "sccp"} } */
/* { dg-final { cleanup-tree-dump "sccp" } } */


Compare to using j-1 in the inner loop, which makes # iterations analysis
succeed.


---


### compiler : `gcc`
### title : `Structures are copied byte by byte into function arguments`
### open_at : `2006-04-06T11:46:52Z`
### last_modified_date : `2021-08-15T04:13:44Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=27055
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.1.0`
### severity : `normal`
### contents :
I tried the following testcase with various GCC versions available as Debian packages. With 3.3.5, the copy from *a to the stack frame of g is done word-by-word with rep movsl. With 3.4.4, it is done by memcpy. Both previous methods are fine. With 3.4.6, the copy is done byte-by-byte without string opcodes. With 4.0.3 and 4.1.0, it is done byte-by-byte and out-of-line: there are two jumps for each copied byte! So argument copy got broken for x86 during GCC 3.4 cycle and it did not get any better with GCC 4.

typedef struct A { int a[1000]; } A;
void g(A);
void f(A *a) { g(*a); }

Assembly output with GCC4 and -O3 optimization:

        pushl   %ebp
        xorl    %edx, %edx
        movl    %esp, %ebp
        subl    $4008, %esp
        movl    8(%ebp), %ecx
.L3:
        cmpl    $4000, %edx
        jb      .L2
        call    g
        leave
        ret
        .p2align 4,,7
.L2:
        movzbl  (%ecx,%edx), %eax
        movb    %al, (%esp,%edx)
        incl    %edx
        .p2align 4,,3
        jmp     .L3

$ LANG=C gcc-3.4 -v
Reading specs from /usr/lib/gcc/i486-linux-gnu/3.4.6/specs
Configured with: ../src/configure -v --enable-languages=c,c++,f77,pascal --prefix=/usr --libexecdir=/usr/lib --with-gxx-include-dir=/usr/include/c++/3.4 --enable-shared --with-system-zlib --enable-nls --without-included-gettext --program-suffix=-3.4 --enable-__cxa_atexit --enable-clocale=gnu --enable-libstdcxx-debug --with-tune=i686 i486-linux-gnu
Thread model: posix
gcc version 3.4.6 (Debian 3.4.6-1)

$ LANG=C gcc-4.1 -v
Using built-in specs.
Target: i486-linux-gnu
Configured with: ../src/configure -v --enable-languages=c,c++,java,fortran,objc,obj-c++,ada,treelang --prefix=/usr --enable-shared --with-system-zlib --libexecdir=/usr/lib --without-included-gettext --enable-threads=posix --enable-nls --program-suffix=-4.1 --enable-__cxa_atexit --enable-clocale=gnu --enable-libstdcxx-debug --enable-java-awt=gtk --enable-gtk-cairo --with-java-home=/usr/lib/jvm/java-1.4.2-gcj-4.1-1.4.2.0/jre --enable-mpfr --with-tune=i686 --enable-checking=release i486-linux-gnu
Thread model: posix
gcc version 4.1.0 (Debian 4.1.0-1)


---


### compiler : `gcc`
### title : `Simplify "a - 10 > 150" into "a > 160" when range of a is known (in VRP or somewhere else)`
### open_at : `2006-04-11T02:04:17Z`
### last_modified_date : `2023-08-10T02:38:41Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=27109
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.2.0`
### severity : `enhancement`
### contents :
Kinda like PR 14490 but for the -fwrapv and unsigned cases:

void bar (void);

void
foo (unsigned a)
{
  if (a < 100)
    return;
  if (200 < a)
    return;

  if (a - 10 > 150)
    bar ();
}


---


### compiler : `gcc`
### title : `20 % increase code size in 4.1 vs 3.4.5`
### open_at : `2006-04-29T12:35:09Z`
### last_modified_date : `2023-07-22T02:46:56Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=27357
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.1.0`
### severity : `normal`
### contents :
Here is a 20 % increase code size, because the compiler tries too much to
 jump to UI_plotHline() instead of just calling the function and then doing
 a standard return at the end of drawbutton()...


[etienne@localhost projet]$ cat tmp.c
typedef struct {
    unsigned short x, y;        /* x should be the easyest to read */
    } __attribute__ ((packed)) coord;

extern inline void
UI_plotHline (coord xy, unsigned short xend, unsigned color) {
    extern UI_function_plotHline (coord xy, unsigned xend, unsigned color);
    UI_function_plotHline (xy, xend, color);
    }

extern inline void
UI_setpixel (coord xy, unsigned color) {
    extern UI_function_setpixel (coord xy, unsigned color);
    UI_function_setpixel (xy, color);
    }

extern inline void bound_stack (void)
  {
/*
 * limit included - but add 2 to high limit for reg16, and 4 for reg32
 * if not in bound, exception #BR generated (INT5).
 * iret from INT5 will retry the bound instruction.
 */
  extern unsigned STATE_stack_limit;
  asm volatile (" bound %%esp,%0 " : : "m" (STATE_stack_limit) );
  }

void
drawbutton (coord    upperleft, coord  lowerright,
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

  UI_plotHline (upperleft, lowerright.x, lowerrightrcolor);     /* bottom line */
  }}

[etienne@localhost projet]$ gcc -v
Using built-in specs.
Target: i386-redhat-linux
Configured with: ../configure --prefix=/usr --mandir=/usr/share/man --infodir=/usr/share/info --enable-shared --enable-threads=posix --enable-checking=release --with-system-zlib --enable-__cxa_atexit --disable-libunwind-exceptions --enable-libgcj-multifile --enable-languages=c,c++,objc,obj-c++,java,fortran,ada --enable-java-awt=gtk --disable-dssi --with-java-home=/usr/lib/jvm/java-1.4.2-gcj-1.4.2.0/jre --with-cpu=generic --host=i386-redhat-linux
Thread model: posix
gcc version 4.1.0 20060304 (Red Hat 4.1.0-3)
[etienne@localhost projet]$ gcc -Os -c tmp.c && size *.o
   text    data     bss     dec     hex filename
    276       0       0     276     114 tmp.o
[etienne@localhost projet]$ toolchain-3.4.5/bin/gcc -v
Reading specs from /home/etienne/projet/toolchain-3.4.5/bin/../lib/gcc/i686-pc-linux-gnu/3.4.5/specs
Configured with: ../configure --prefix=/home/etienne/projet/toolchain --enable-languages=c
Thread model: posix
gcc version 3.4.5
[etienne@localhost projet]$ toolchain-3.4.5/bin/gcc -Os -c tmp.c && size *.o
   text    data     bss     dec     hex filename
    227       0       0     227      e3 tmp.o
[etienne@localhost projet]$


---


### compiler : `gcc`
### title : `zero extension not eliminated`
### open_at : `2006-05-07T09:17:32Z`
### last_modified_date : `2019-06-14T19:28:03Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=27469
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.2.0`
### severity : `enhancement`
### contents :
unsigned parity(unsigned x) {
    x ^= x >> 16;
    x ^= x >> 8;
    x ^= x >> 4;
    x &= 0xf;
    return (0x6996 >> x) & 1;
}

gcc 4.2.0 20060506 produces:
	extwl   a0,0x2,t2
	lda     v0,27030
	xor     t2,a0,t2
	zapnot  t2,0xf,t1 # redundant zero-extension
	srl     t1,0x8,t1
	xor     t1,t2,t1
	zapnot  t1,0xf,t0 # redundant zero-extension
	srl     t0,0x4,t0
	xor     t0,t1,t0
	and     t0,0xf,t0
	sra     v0,t0,v0
	and     v0,0x1,v0

-fsee doesn't change anything here.


---


### compiler : `gcc`
### title : `TLS accesses use one more instruction than necessary`
### open_at : `2006-05-08T07:23:33Z`
### last_modified_date : `2022-03-08T16:20:46Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=27479
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `target`
### version : `4.0.4`
### severity : `enhancement`
### contents :
To access a TLS variable in the local-exec model, gcc will emit three instructions, for instance (for a 64-bit compile):
  addis 9,13,x@tprel@ha
  addi 9,9,x@tprel@l
  lwz 3,0(9)
when two instructions would suffice:
  addis 9,13,x@tprel@ha
  lwz 3,x@tprel@l(9)

This can be seen with a simple little program like this:

__thread int x;
int foo(void)
{
        return x;
}


---


### compiler : `gcc`
### title : `x && (x & y) not optimized to x & y`
### open_at : `2006-05-08T19:27:59Z`
### last_modified_date : `2023-10-12T18:00:37Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=27504
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.2.0`
### severity : `enhancement`
### contents :
Example:

falk@juist:/tmp% cat test.c 
int f(int x) { return x && (x & 0x55); }

falk@juist:/tmp% gcc -c -O3  test.c && objdump -d test.o
0000000000000000 <f>:
   0:   00 04 ff 47     clr     v0
   4:   02 00 00 e6     beq     a0,10 <f+0x10>
   8:   01 b0 0a 46     and     a0,0x55,t0
   c:   a0 03 e1 43     cmpult  zero,t0,v0
  10:   01 80 fa 6b     ret


---


### compiler : `gcc`
### title : `missed-optimization transforming a byte array to unsigned long`
### open_at : `2006-05-18T17:58:17Z`
### last_modified_date : `2023-05-31T08:28:51Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=27663
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.2.0`
### severity : `enhancement`
### contents :
Hi,
this code:

unsigned long f (unsigned char  *P)
{
  unsigned long C;
  C  = ((unsigned long)P[1] << 24)
     | ((unsigned long)P[2] << 16)
     | ((unsigned long)P[3] <<  8)
     | ((unsigned long)P[4] <<  0);
  return C;
}

compiles to this:

00000000 <f>:
   0:   f9 2f           mov     r31, r25
   2:   e8 2f           mov     r30, r24
   4:   61 81           ldd     r22, Z+1        ; 0x01
   6:   77 27           eor     r23, r23
   8:   88 27           eor     r24, r24
   a:   99 27           eor     r25, r25
   c:   96 2f           mov     r25, r22
   e:   88 27           eor     r24, r24
  10:   77 27           eor     r23, r23
  12:   66 27           eor     r22, r22
  14:   22 81           ldd     r18, Z+2        ; 0x02
  16:   33 27           eor     r19, r19
  18:   44 27           eor     r20, r20
  1a:   55 27           eor     r21, r21
  1c:   53 2f           mov     r21, r19
  1e:   42 2f           mov     r20, r18
  20:   33 27           eor     r19, r19
  22:   22 27           eor     r18, r18
  24:   62 2b           or      r22, r18
  26:   73 2b           or      r23, r19
  28:   84 2b           or      r24, r20
  2a:   95 2b           or      r25, r21
  2c:   24 81           ldd     r18, Z+4        ; 0x04
  2e:   33 27           eor     r19, r19
  30:   44 27           eor     r20, r20
  32:   55 27           eor     r21, r21
  34:   62 2b           or      r22, r18
  36:   73 2b           or      r23, r19
  38:   84 2b           or      r24, r20
  3a:   95 2b           or      r25, r21
  3c:   23 81           ldd     r18, Z+3        ; 0x03
  3e:   33 27           eor     r19, r19
  40:   44 27           eor     r20, r20
  42:   55 27           eor     r21, r21
  44:   54 2f           mov     r21, r20
  46:   43 2f           mov     r20, r19
  48:   32 2f           mov     r19, r18
  4a:   22 27           eor     r18, r18
  4c:   62 2b           or      r22, r18
  4e:   73 2b           or      r23, r19
  50:   84 2b           or      r24, r20
  52:   95 2b           or      r25, r21
  54:   08 95           ret

using this cmd line:
avr-gcc -c -Os f.c

IMO, most of the or, eor and mov instructions are unnecessary.


---


### compiler : `gcc`
### title : `Some cse optimizations require hash collisions`
### open_at : `2006-06-20T19:40:18Z`
### last_modified_date : `2021-09-01T02:58:06Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=28108
### status : `NEW`
### tags : `internal-improvement, missed-optimization`
### component : `rtl-optimization`
### version : `4.2.0`
### severity : `normal`
### contents :
cse.c:hash_rtx has the same problem as found before in cse.c:cselib_hash_rtx
(PR rtl-optimization/22445).  Hence, some optimiztions will only be done
if there is a convenient hash collision.

I.e. the MODE should not be used to calculate the hash value.


---


### compiler : `gcc`
### title : `optimize redundant memset + assignment`
### open_at : `2006-06-22T03:29:19Z`
### last_modified_date : `2022-07-19T13:21:58Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=28134
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.7.0`
### severity : `enhancement`
### contents :
In a compiler built from svn revision 114878, a memset(,0,) followed by storing 0 into some of the just-cleared locations produces redundant stores.

#include <string.h>
struct blob { int a[3]; void *p; };
void foo (struct blob *bp) {
    int i;
    memset (bp, 0, 1024 * sizeof(*bp));
    /* Null pointer not required by ANSI to be all-bits-0, so: */
    for (i = 0; i < 1024; i++) bp[i].p = 0;
}

With "gcc -O9 -fomit-frame-pointer -march=pentiumpro -mtune=pentiumpro" the assembly code produces a call to memset, then a loop storing 0 into the pointer slots.  But on this platform, since a pointer has all bits clear, the loop is redundant.  If I add "-minline-all-stringops", it doesn't help; the memset call is replaced by a sequence using "rep stosl", and the following loop is still there.

If I change the array size from 1024 to 1, then gcc expands the memset inline (no loop), and figures out the redundancy.

Same issue with storing zero in bit fields after memset:

#include <string.h>
struct blob { unsigned char a:1, b:7; };
void foo (struct blob *bp) {
    int i;
    memset(bp, 0, 1024 * sizeof(*bp));
    for (i = 0; i < 1024; i++) bp[i].a = 0;
}

The memset is followed by a loop with "andb $-2,...".

A possible optimization I'm less would be allowed for odd cases: If I change the second example to use "bp[i].a = 1", is the compiler allowed to optimize this into memset(,1,)?  If so, add that to the wish list. :-)


---


### compiler : `gcc`
### title : `const / pure call with ignored argument emitted.`
### open_at : `2006-07-07T16:52:16Z`
### last_modified_date : `2019-03-06T10:39:57Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=28306
### status : `NEW`
### tags : `missed-optimization`
### component : `c`
### version : `4.2.0`
### severity : `normal`
### contents :
There is code in the expanders which is supposed to avoid emitting calls
to pure functions which have their result ignored, but it doesn't appear to
work when the function called is represented as a COND_EXPR.


---


### compiler : `gcc`
### title : `poor optimization choices when iterating over a std::string (probably not c++-specific)`
### open_at : `2006-07-12T22:32:56Z`
### last_modified_date : `2018-12-19T11:10:40Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=28364
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.1.2`
### severity : `normal`
### contents :
Consider the following test program:

#include <string>
bool has_bad_chars(std::string const & path)
{
  for (std::string::const_iterator c = path.begin(); c != path.end(); c++)
    {
      unsigned char x = static_cast<unsigned char>(*c);
      if (x <= 0x1f || x == 0x5c || x == 0x7f)
        return true;
    }
  return false;
}

At -O2, GCC 4.1 chooses to duplicate the entire body of the loop for no good reason; the code is not rendered more straight-line by this, and in fact it executes strictly more instructions even for a single-character string.  I'll attach an assembly file showing what it did (Z13has_bad_charsRKSs) and what it should have done (_Z14has_bad_chars2RKSs).  The bad transformation is done by the .t45.ch pass, which acronym does not mean anything to me.


---


### compiler : `gcc`
### title : `Divide with vectors cause extra stores (and more stack space) (with VMX)`
### open_at : `2006-07-13T02:22:01Z`
### last_modified_date : `2022-03-08T16:20:59Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=28366
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.2.0`
### severity : `enhancement`
### contents :
Compile the following code with -maltivec -O2 -mabi=altivec -m64:
#define vector __attribute__((vector_size(16)))
vector float f(vector float t, vector float t1)
{
  return t / t1;
}
We currently get:
        addi 9,1,-36
        stvewx 2,0,9
        addi 9,1,-20
        stvewx 3,0,9
        addi 9,1,-144
        stvewx 2,0,9
        addi 9,1,-128
        stvewx 3,0,9
        addi 9,1,-108
        stvewx 2,0,9
        addi 9,1,-92
        stvewx 3,0,9
        addi 9,1,-72
        stvewx 2,0,9
        addi 9,1,-56
        stvewx 3,0,9
        addi 9,1,-16
....

Which is storing out each element of the vector one by one, instead of just storing the whole vector out:
stvx 2, ...
stvx 3, ...


---


### compiler : `gcc`
### title : `accessing via union on a vector does not cause vec_extract to be used`
### open_at : `2006-07-13T02:43:47Z`
### last_modified_date : `2023-05-15T06:07:26Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=28367
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.2.0`
### severity : `enhancement`
### contents :
Take the following code and compile with -O2 -m64 -maltivec -mabi=altivec:
#define vector __attribute__((vector_size(16)))
float f(vector float t)
{
  union {
    vector float t1;
    float t2[4];
  }t5;
  t5.t1 = t;
  return t5.t2[0];
}

Currently we get:
        addi 12,1,-32
        stvx 2,0,12
        ld 11,0(12)
        srdi 9,11,32
        stw 9,-16(1)
        lfs 1,-16(1)
        blr

Which is bad for at least the Cell as we now hit two store load hazards.  We can remove one if the compile uses the vec_extract patterns causing us to use stvewx and lfs.

This does not effect x86 as the union is recorded as BLKmode but x86_64 has the same issue, maybe even worse as there is no need to go through memory there.
X86_64 produces:
f:
.LFB2:
        movaps  %xmm0, -24(%rsp)
        movss   -24(%rsp), %xmm0
        ret
When really it should produce just a ret.


---


### compiler : `gcc`
### title : `suboptimal 'division by constant' optimization`
### open_at : `2006-07-18T08:34:01Z`
### last_modified_date : `2019-12-08T05:18:07Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=28417
### status : `NEW`
### tags : `missed-optimization, patch`
### component : `middle-end`
### version : `4.1.1`
### severity : `normal`
### contents :
It looks like expmed.c::choose_multiplier(), which is responsible for finding parameters needed for replacing division by constant with mul+shift, sometimes fails to find optimal parameters.

One example: A/1577682821 can be calculated by executing A*365384439 >> (27+32), for any 32-bit unsigned A. However, gcc-4.1.1 and all previous versions generate much more elaborate code.

The below program demonstrates tis and also two more similar examples. It also checks that mul+shift works for any unsigned A, by testing all possibe values of A.

#include <stdint.h>
#include <stdio.h>

unsigned v;
void f9188_mul365384439_shift27(unsigned A) { v = A/(unsigned)1577682821; }
void f9188_mul365384439_shift27_prime(unsigned A) { v = (((uint64_t)A)*(unsigned)365384439) >> (27+32); }
void f8399_mul2283243215_shift29(unsigned A) { v = A/(unsigned)1009898111; }
void f8399_mul2283243215_shift29_prime(unsigned A) { v = (((uint64_t)A)*(unsigned)2283243215) >> (29+32); }
void f8267_mul2482476753_shift30(unsigned A) { v = A/(unsigned)1857695551; }
void f8267_mul2482476753_shift30_prime(unsigned A) { v = (((uint64_t)A)*(unsigned)2482476753) >> (30+32); }

/* Generated code is suboptimal (gcc 4.1.1):
void f9188_mul365384439_shift27(unsigned A) { v = A/1577682821; }
f9188_mul365384439_shift27:
	pushl	%edi
	pushl	%esi
	pushl	%ebx
	movl	16(%esp), %ebx
	movl	$1551183727, %ecx
	movl	%ebx, %eax
	mull	%ecx
	subl	%edx, %ebx
	shrl	%ebx
	leal	(%ebx,%edx), %eax
	shrl	$30, %eax
	movl	%eax, v
	popl	%ebx
	popl	%esi
	popl	%edi
	ret
void f8399_mul2283243215_shift29(unsigned A) { v = A/1009898111; }
f8399_mul2283243215_shift29:
	pushl	%edi
	pushl	%esi
	pushl	%ebx
	movl	16(%esp), %ebx
	movl	$271519133, %ecx
	movl	%ebx, %eax
	mull	%ecx
	subl	%edx, %ebx
	shrl	%ebx
	leal	(%ebx,%edx), %eax
	shrl	$29, %eax
	movl	%eax, v
	popl	%ebx
	popl	%esi
	popl	%edi
	ret
void f8267_mul2482476753_shift30(unsigned A) { v = A/1857695551; }
f8267_mul2482476753_shift30:
	pushl	%edi
	pushl	%esi
	pushl	%ebx
	movl	16(%esp), %ebx
	movl	$669986209, %ecx
	movl	%ebx, %eax
	mull	%ecx
	subl	%edx, %ebx
	shrl	%ebx
	leal	(%ebx,%edx), %eax
	shrl	$30, %eax
	movl	%eax, v
	popl	%ebx
	popl	%esi
	popl	%edi
	ret

These operations can be done like this:
f9188_mul365384439_shift27_prime:
	movl	$365384439, %eax
	mull	4(%esp)
	movl	%edx, %eax
	shrl	$27, %eax
	movl	%eax, v
	ret
f8399_mul2283243215_shift29_prime:
	movl	$-2011724081, %eax
	mull	4(%esp)
	movl	%edx, %eax
	shrl	$29, %eax
	movl	%eax, v
	ret
f8267_mul2482476753_shift30_prime:
	movl	$-1812490543, %eax
	mull	4(%esp)
	movl	%edx, %eax
	shrl	$30, %eax
	movl	%eax, v
	ret

(Why there is that silly movl %edx, %eax - that's another good question...)

The verification program is below. Was compiled with -Os
(in order to force gcc to use div insn for a/b - we want to do true
division for the purpose of correctness check!)
and didn't report a failure.
*/

int main()
{
	unsigned A=0,u,v;
	while(++A) {
		(A & 0xffff) || printf("A=%u\r",A);

		u = (((uint64_t)A)*(unsigned)365384439) >> (27+32);
		v = A / (unsigned)1577682821;
		if(u!=v) { printf("1: A=%u u=%u v=%u\n", A,u,v); return 0; }

		u = (((uint64_t)A)*(unsigned)2283243215) >> (29+32);
		v = A / (unsigned)1009898111;
		if(u!=v) { printf("2: A=%u u=%u v=%u\n", A,u,v); return 0; }

		u = (((uint64_t)A)*(unsigned)2482476753) >> (30+32);
		v  =A / (unsigned)1857695551;
		if(u!=v) { printf("3: A=%u u=%u v=%u\n", A,u,v); return 0; }
	}
	puts("");
	return 0;
}


---


### compiler : `gcc`
### title : `[4.3/4.4/4.5 Regression] uses memory where it can use registers`
### open_at : `2006-07-25T14:44:44Z`
### last_modified_date : `2021-07-26T08:07:21Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=28481
### status : `RESOLVED`
### tags : `missed-optimization, ra`
### component : `target`
### version : `4.1.1`
### severity : `normal`
### contents :
The attached test program uses 5 local variables and this fits into i386 available registers. gcc 3.4.3 manages to do it with -O3.

gcc-4.1.1 -O2 and -O3 are identical and both are worse than gcc-3.4.3 -O3:

# wc -l *.s
  1498 serpent343-O2.s
  1252 serpent343-O3.s <- gcc 3.4.3 is smaller!
  1313 serpent411-O2.s
  1313 serpent411-O3.s

gcc-4.1.1 -Os is better than -O3, but still a tiny bit worse than gcc-3.4.3:

# wc -l serpent343-O3.s serpent411-Os.s
 1252 serpent343-O3.s
 1275 serpent411-Os.s

# size serpent343-O3.o serpent411-Os.o
   3262       0       0    3262     cbe serpent343-O3.o
   3347       0       0    3347     d13 serpent411-Os.o

Additional ingo is in the testcase itself.

(btw does it make sense to include this into testsuite?)


---


### compiler : `gcc`
### title : `Not forcing alignment of arrays in structs  with -fsection-anchors`
### open_at : `2006-08-07T07:07:20Z`
### last_modified_date : `2021-05-04T12:31:49Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=28628
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.2.0`
### severity : `enhancement`
### contents :
Since the fix to PR27770, we now miss opportunities to align some arrays when -fsection-anchors is enabled. The patch for PR27770 increases the alignment of (global) arrays only. We have a few testcases though (e.g. section-anchors-vect-69.c) that have global structs that contain fields that are arrays. Aligning the beginning of these structs can sometime align one/some of their array fields. Since the new function cgraph_increase_alignment does notattempt to do that, we have cases that will be vectorized less efficiently. To solve this we need to extend the optimization to align global structs that have array fields that could become aligned as a result.


---


### compiler : `gcc`
### title : `[4.2 Regression] duplicate members of arrays`
### open_at : `2006-08-16T17:28:47Z`
### last_modified_date : `2019-02-08T12:48:53Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=28755
### status : `RESOLVED`
### tags : `missed-optimization, patch`
### component : `middle-end`
### version : `4.1.1`
### severity : `normal`
### contents :
See attached test case. Observe the number of times certain lines of the 'vesa_modes' array are emitted. This isn't particularly optimal, especially as it happens even with -Os.

 $ make
cc -Os -c -o fbmon.o fbmon.i -save-temps
grep 39682 fbmon.s
        .long   39682
        .long   39682


---


### compiler : `gcc`
### title : `missed optimization with non-COND_EXPR and vrp and comparisions`
### open_at : `2006-08-21T23:24:38Z`
### last_modified_date : `2023-08-08T15:43:13Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=28794
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.2.0`
### severity : `enhancement`
### contents :
int f(int x, int y)
{
  int t;
  for (t = 0; t < 50; t++)
    g(t>0);
}
void f1(int x, int y)
{
  int t;
  for (t = 0; t < 50; t++)
    g(t!=0);
}

--------------
The above two functions should produce the same code with f1 being better than f.

If we change it to:
void f2(int x, int y)
{
  int t;
  for (t = 0; t < 50; t++)
  {
    int tt;
    if (t>0)
      tt = 1;
   else
      tt = 0;
   g(tt);
  }
}

-----
We get f1 so we are only folding comparisions in a COND_EXPR which is wrong, we should also be doing them in MODIFY_EXPRs too.


---


### compiler : `gcc`
### title : `[11/12/13/14 Regression] Aggregate copy not elided when using a return value as a pass-by-value parameter`
### open_at : `2006-08-24T02:52:19Z`
### last_modified_date : `2023-07-15T07:43:02Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=28831
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.2.0`
### severity : `normal`
### contents :
Bug 23372 was a missed optimization with respect to GCC 3.4. It is now fixed when the parameter is a reference. But there is still a regression when the parameter is the return value of another function. Testcase: (-Wall -O3 --march=i386)

struct A { int a[1000]; };
struct A f();
void g(struct A);
void h() { g(f()); }

GCC 3.3 and 3.4 first allocate the stack frame of g and then require f to directly store its return value in the parameter location. GCC 4.0, 4.1, and 4.2 (as of 2006-08-23) use another stack location for the return value of f, then allocate the stack frame of g, and finally copy the value to this new frame (possibly using a byte-by-byte copy, see bug 27055). The code generated by GCC 3.x is optimal, the one by GCC 4.x is not.

GCC 3.4:
        movl    %esp, %eax
        subl    $12, %esp
        pushl   %eax
        call    f
        addl    $12, %esp
        call    g

GCC 4.2:
        leal    -4004(%ebp), %ebx
        pushl   %ebx
        call    f
        subl    $3988, %esp
        movl    %esp, %eax
        pushl   %edx
        pushl   $4000
        pushl   %ebx
        pushl   %eax
        call    memcpy
        addl    $16, %esp
        call    g

$ LANG=C /opt/gcc/bin/gcc -v
Using built-in specs.
Target: i686-pc-linux-gnu
Configured with: ../gcc/configure --enable-languages=c,c++ --prefix=/opt/gcc
Thread model: posix
gcc version 4.2.0 20060823 (experimental)


---


### compiler : `gcc`
### title : `missed call -> jmp transformation; redundant unwind stuff with empty finally`
### open_at : `2006-08-25T20:39:45Z`
### last_modified_date : `2021-12-25T06:12:41Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=28850
### status : `NEW`
### tags : `EH, missed-optimization`
### component : `tree-optimization`
### version : `4.1.2`
### severity : `enhancement`
### contents :
$ cat fake_bomber.cpp

struct bomber
{
        bomber() : bum( false ) { }
        ~bomber() { if ( bum ) throw 0; }  // this will never throw
private:
        bool bum;
};

void zoo() { }

void bar( void ( *f )() )
{
#ifndef CALL2JMP
        bomber b; // fake bomber
#endif
        f();
}

void foo()
{
#ifndef CALL2JMP
        bomber b; // fake bomber
#endif
        bar( &zoo );
}

int main()
{
        foo();
        return 0;
}

$ g++ fake_bomber.cpp -o fake_bomber -O3 -fno-rtti --save-temps

zoo():
        rep ; ret

bar(void (*)()):
        subq    $8, %rsp
        call    *%rdi
        addq    $8, %rsp
        ret
        movq    %rax, %rdi
        call    _Unwind_Resume

foo():
        subq    $8, %rsp
        movl    zoo(), %edi
        call    bar(void (*)())
        addq    $8, %rsp
        ret
        movq    %rax, %rdi
        call    _Unwind_Resume

main:
        subq    $8, %rsp
        call    foo()
        xorl    %eax, %eax
        addq    $8, %rsp
        ret

$ g++ fake_bomber.cpp -o fake_bomber -O3 -fno-rtti --save-temps -DCALL2JMP

zoo():
        rep ; ret

bar(void (*)()):
        movq    %rdi, %r11
        jmp     *%r11

foo():
        rep ; ret

main:
        xorl    %eax, %eax
        ret


---


### compiler : `gcc`
### title : `IV selection is messed up`
### open_at : `2006-09-01T01:54:08Z`
### last_modified_date : `2021-07-26T02:49:23Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=28919
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.2.0`
### severity : `enhancement`
### contents :
With code like this (see attachement for a complete silly test case),
unsigned int quad = 0;
for (unsigned int dec=node.count/4; dec; --dec) {
	_mm_prefetch(1024+(const char *)&base[quad], _MM_HINT_NTA);
	sampler.countl[0] = _mm_add_epi32(sampler.countl[0], _mm_cmpgt_epi32(sampler.pos[0], base[quad+0]));
	sampler.countl[1] = _mm_add_epi32(sampler.countl[1], _mm_cmpgt_epi32(sampler.pos[1], base[quad+0]));
	sampler.countl[0] = _mm_add_epi32(sampler.countl[0], _mm_cmpgt_epi32(sampler.pos[0], base[quad+1]));
	sampler.countl[1] = _mm_add_epi32(sampler.countl[1], _mm_cmpgt_epi32(sampler.pos[1], base[quad+1]));
	sampler.countl[0] = _mm_add_epi32(sampler.countl[0], _mm_cmpgt_epi32(sampler.pos[0], base[quad+2]));
	sampler.countl[1] = _mm_add_epi32(sampler.countl[1], _mm_cmpgt_epi32(sampler.pos[1], base[quad+2]));
	sampler.countl[0] = _mm_add_epi32(sampler.countl[0], _mm_cmpgt_epi32(sampler.pos[0], base[quad+3]));
	sampler.countl[1] = _mm_add_epi32(sampler.countl[1], _mm_cmpgt_epi32(sampler.pos[1], base[quad+3]));
	quad += 4;
}

g++ 4.2 insists to use the same register for addressing 'base[quad]' and prefetching 1k away from it. Horrible encoding ensues.

With gcc-4.2-20060311/gcc-4.2-20060826 -O3 -march=k8 i get something like
  401080:       66 0f 6f c2             movdqa %xmm2,%xmm0
  401084:       0f 18 00                prefetchnta (%eax)
  401087:       66 0f 66 80 00 fc ff ff         pcmpgtd 0xfffffc00(%eax),%xmm0
  40108f:       66 0f fe 42 20          paddd  0x20(%edx),%xmm0
  401094:       0f 29 42 20             movaps %xmm0,0x20(%edx)
  401098:       66 0f 6f c1             movdqa %xmm1,%xmm0
  40109c:       66 0f 66 80 00 fc ff ff         pcmpgtd 0xfffffc00(%eax),%xmm0
  4010a4:       66 0f fe 42 30          paddd  0x30(%edx),%xmm0
  4010a9:       0f 29 42 30             movaps %xmm0,0x30(%edx)
  4010ad:       66 0f 6f c2             movdqa %xmm2,%xmm0
  4010b1:       66 0f 66 80 10 fc ff ff         pcmpgtd 0xfffffc10(%eax),%xmm0
  4010b9:       66 0f fe 42 20          paddd  0x20(%edx),%xmm0
  4010be:       0f 29 42 20             movaps %xmm0,0x20(%edx)
  4010c2:       66 0f 6f c1             movdqa %xmm1,%xmm0
etc...

There's other issues with the code produced, ie gcc writing back values instead of just keeping them live, but i can kludge around them.
But i cannot fix that silly encoding.

msvc8, icc9.1 and g++ 3.4.4 do a much better job, here's g++ 3.4.4
 401084:       prefetchnta 0x400(%eax)
 40108b:       movdqa %xmm5,%xmm2
 40108f:       movdqa %xmm4,%xmm1
 401093:       movdqa %xmm3,%xmm0
 401097:       pcmpgtd (%eax),%xmm2
 40109b:       paddd  %xmm2,%xmm6
 40109f:       movaps %xmm6,0x20(%edx)
 4010a3:       movdqa %xmm5,%xmm2
 4010a7:       pcmpgtd (%eax),%xmm1
 4010ab:       paddd  %xmm1,%xmm0
 4010af:       movaps %xmm0,0x30(%edx)
 4010b3:       movdqa %xmm4,%xmm1
 4010b7:       pcmpgtd 0x10(%eax),%xmm2
 4010bc:       paddd  %xmm2,%xmm6
 4010c0:       movaps %xmm6,0x20(%edx)
 
Note that -fprefetch-loop-arrays's heuristic is way off the mark and counterproductive, even for that simplified testcase.


---


### compiler : `gcc`
### title : `Missing if-conversion. If-conversion dependent on operand order. Inconsistent if-conversion.`
### open_at : `2006-09-19T15:51:06Z`
### last_modified_date : `2023-06-02T06:04:41Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=29144
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `3.4.5`
### severity : `enhancement`
### contents :
Four ways of coding a conditional assignment yields 1 conditional move using 
gcc 3.4.5 20051201 (Red Hat 3.4.5-2). gcc 4.0.2 20051130 (Red Hat 4.0.2-14.EL4) 
produces none. IMHO, four cmov's should have been produced. I further expect all four functions to generates the exact same code.

All recent new commercial compilers tested generates four cmov's:
 - intel 8.1, 9.0, and 9.1
 - pgi 5.2, 6.0, 6.1, and 6.2
 - pathscale 2.1, 2.2, 2.3, 2.4


Version-Release number of selected component (if applicable):


How reproducible:
allways


Steps to Reproduce:
gcc -O2 -S if_conversion.c;egrep cmov\|^[a-d]: if_conversion.s

  
Actual results:
a:
b:
c:
d:
        cmove   %ecx, %esi


Expected results:

One cmovX per function, four in total.

Here is the source code:

---------------------------------------------------------------------
/* if construct, near obvious cse */
int a(int c, int a, int b, int o) {
  int r;

  if (c) {
     r = a - b;
  } else {
     r = a + o - b;
  }

  return r;
}

/* if construct, absolute obvious cse */
int b(int c, int a, int b, int o) {
  int r;

  if (c) {
     r = a - b;
  } else {
     r = a - b + o;
  }

  return r;
}

/* conditional assignment, near obvious cse */
int c(int c, int a, int b, int o) {
  int r;

  r = (c) ?  a - b : a + o - b;

  return r;
}

/* conditional assignment, absolute obvious cse */
int d(int c, int a, int b, int o) {
  int r;

  r = (c) ?  a - b : a - b + o;

  return r;
}
---------------------------------------------------------------------


---


### compiler : `gcc`
### title : `[11/12/13/14 regression] loop performance regression`
### open_at : `2006-09-27T18:29:40Z`
### last_modified_date : `2023-07-17T08:29:50Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=29256
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.2.0`
### severity : `normal`
### contents :
Compiler configure with --enable-e500_double

The compiler generates inferior code then with gcc-4.1.

The source code is:
# define N	2000000
static double	a[N],c[N];
void tuned_STREAM_Copy()
{
	int j;
        for (j=0; j<N; j++)
            c[j] = a[j];
}

Attached is stream.s-4.1 and stream.s-4.2

When compiled with 4.2, the command line is:
/temp/gnu_toolchain/install_area/gcc-trunk/gcc-trunk-20060926-e500v2/bin/powerpc-unknown-linux-gnuspe-gcc -O3 -funroll-loops -funroll-all-loops -S stream.c -v
Using built-in specs.
Target: powerpc-unknown-linux-gnuspe
Configured with: ../gcc-trunk/configure --prefix=/temp/gnu_toolchain/install_area/gcc-trunk/gcc-trunk-20060926-e500v2 --with-local-prefix=/temp/gnu_toolchain/install_area/gcc-trunk/gcc-trunk-20060926-e500v2 --enable-languages=c,c++,fortran --enable-threads --target=powerpc-unknown-linux-gnuspe --with-gmp=/proj/ppc/sysperf/sw/gnu_toolchain/gcc_support/linuxAMD64 --with-mpfr=/proj/ppc/sysperf/sw/gnu_toolchain/gcc_support/linuxAMD64 --disable-shared --disable-multilib --disable-linux-futex --enable-e500_double
Thread model: posix
gcc version 4.2.0 20060926 (experimental)
 /temp/gnu_toolchain/install_area/gcc-trunk/gcc-trunk-20060926-e500v2/libexec/gcc/powerpc-unknown-linux-gnuspe/4.2.0/cc1 -quiet -v -D__unix__ -D__gnu_linux__ -D__linux__ -Dunix -D__unix -Dlinux -D__linux -Asystem=linux -Asystem=unix -Asystem=posix stream.c -quiet -dumpbase stream.c -auxbase stream -O3 -version -funroll-loops -funroll-all-loops -o stream.s
#include "..." search starts here:
#include <...> search starts here:
 /temp/gnu_toolchain/install_area/gcc-trunk/gcc-trunk-20060926-e500v2/lib/gcc/powerpc-unknown-linux-gnuspe/4.2.0/include
 /temp/gnu_toolchain/install_area/gcc-trunk/gcc-trunk-20060926-e500v2/lib/gcc/powerpc-unknown-linux-gnuspe/4.2.0/../../../../powerpc-unknown-linux-gnuspe/sys-include
 /temp/gnu_toolchain/install_area/gcc-trunk/gcc-trunk-20060926-e500v2/lib/gcc/powerpc-unknown-linux-gnuspe/4.2.0/../../../../powerpc-unknown-linux-gnuspe/include
End of search list.
GNU C version 4.2.0 20060926 (experimental) (powerpc-unknown-linux-gnuspe)
        compiled by GNU C version 3.4.3.
GGC heuristics: --param ggc-min-expand=30 --param ggc-min-heapsize=4096
Compiler executable checksum: af19c94719eeca398c0b645020867b59





And when compiled with 4.1 the command line is:
/temp/gnu_toolchain/install_area/gcc-4_1-branch/gcc-4_1-branch-20060926-e500v2/bin/powerpc-unknown-linux-gnuspe-gcc -O3 -funroll-loops -funroll-all-loops -S stream.c -v
Using built-in specs.
Target: powerpc-unknown-linux-gnuspe
Configured with: ../gcc-4_1-branch/configure --prefix=/temp/gnu_toolchain/install_area/gcc-4_1-branch/gcc-4_1-branch-20060926-e500v2 --with-local-prefix=/temp/gnu_toolchain/install_area/gcc-4_1-branch/gcc-4_1-branch-20060926-e500v2 --enable-languages=c,c++,fortran --enable-threads --target=powerpc-unknown-linux-gnuspe --with-gmp=/proj/ppc/sysperf/sw/gnu_toolchain/gcc_support/linuxAMD64 --with-mpfr=/proj/ppc/sysperf/sw/gnu_toolchain/gcc_support/linuxAMD64 --disable-shared --disable-multilib --disable-shared --disable-multilib --enable-e500_double
Thread model: posix
gcc version 4.1.2 20060926 (prerelease)
 /temp/gnu_toolchain/install_area/gcc-4_1-branch/gcc-4_1-branch-20060926-e500v2/libexec/gcc/powerpc-unknown-linux-gnuspe/4.1.2/cc1 -quiet -v -D__unix__ -D__gnu_linux__ -D__linux__ -Dunix -D__unix -Dlinux -D__linux -Asystem=linux -Asystem=unix -Asystem=posix stream.c -quiet -dumpbase stream.c -auxbase stream -O3 -version -funroll-loops -funroll-all-loops -o stream.s
ignoring nonexistent directory "/temp/gnu_toolchain/install_area/gcc-4_1-branch/gcc-4_1-branch-20060926-e500v2/lib/gcc/powerpc-unknown-linux-gnuspe/4.1.2/../../../../powerpc-unknown-linux-gnuspe/include"
#include "..." search starts here:
#include <...> search starts here:
 /temp/gnu_toolchain/install_area/gcc-4_1-branch/gcc-4_1-branch-20060926-e500v2/lib/gcc/powerpc-unknown-linux-gnuspe/4.1.2/include
 /temp/gnu_toolchain/install_area/gcc-4_1-branch/gcc-4_1-branch-20060926-e500v2/lib/gcc/powerpc-unknown-linux-gnuspe/4.1.2/../../../../powerpc-unknown-linux-gnuspe/sys-include
End of search list.
GNU C version 4.1.2 20060926 (prerelease) (powerpc-unknown-linux-gnuspe)
        compiled by GNU C version 3.4.3.
GGC heuristics: --param ggc-min-expand=100 --param ggc-min-heapsize=131072
Compiler executable checksum: 565818e6f0c83f0e9f8781118c7d40c3


---


### compiler : `gcc`
### title : `need to generalize realignment support in the vectorizer`
### open_at : `2006-09-28T10:41:16Z`
### last_modified_date : `2021-08-16T04:22:21Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=29268
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.2.0`
### severity : `enhancement`
### contents :
details in theis thread:
http://gcc.gnu.org/ml/gcc/2006-09/msg00503.html

Need to add other ways to handle realignment, that are applicable to targets that can't support the realign_load the way it is currently defined.


---


### compiler : `gcc`
### title : `Jump threading getting in the way of PHI-OPT`
### open_at : `2006-10-03T16:03:54Z`
### last_modified_date : `2021-11-16T02:15:26Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=29333
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.2.0`
### severity : `enhancement`
### contents :
There are cases in which phiopt doesn't recognize MAX_EXPRs or MIN_EXPRs patterns.
In particular, source codes that look very similar at first sight may induce phiopt to behave differently.

Let's consider the following two functions:

-----------------------------
int minmax_correct(int a)
{
        if (a > 32767) a = 32767;
        else if (a < -32768) a = -32768;

        return a;
}

int minmax_wrong(int a)
{
        if (a > 32767) a = 32767;
        if (a < -32768) a = -32768;

        return a;
}
-----------------------------

MIN_EXPRs and MAX_EXPRs are generated for the first function, but not for the second.

Here is the contents of trace file minmax.c.042t.phicprop1:

-----------------------------
;; Function minmax_correct (minmax_correct)

minmax_correct (a)
{
<bb 2>:
  if (a_2 > 32767) goto <L3>; else goto <L1>;

<L1>:;
  if (a_2 < -32768) goto <L2>; else goto <L3>;

<L2>:;

  # a_1 = PHI <32767(2), a_2(3), -32768(4)>;
<L3>:;
  <retval> = a_1;
  return <retval>;

}

;; Function minmax_wrong (minmax_wrong)

Removing basic block 6
minmax_wrong (a)
{
<bb 2>:
  if (a_3 > 32767) goto <L6>; else goto <L1>;

<L1>:;
  if (a_3 < -32768) goto <L3>; else goto <L6>;

  # a_9 = PHI <a_3(3), 32767(2)>;
<L6>:;

  # a_2 = PHI <a_9(4), -32768(3)>;
<L3>:;
  <retval> = a_2;
  return <retval>;

}
-----------------------------

And here is minmax.c.043t.phiopt1:

-----------------------------
;; Function minmax_correct (minmax_correct)

Removing basic block 4
Removing basic block 3
Merging blocks 2 and 5
minmax_correct (a)
{
<bb 2>:
  a_7 = MAX_EXPR <-32768, a_2>;
  a_8 = MIN_EXPR <a_7, 32767>;
  <retval> = a_8;
  return <retval>;

}

;; Function minmax_wrong (minmax_wrong)

minmax_wrong (a)
{
<bb 2>:
  if (a_3 > 32767) goto <L6>; else goto <L1>;

<L1>:;
  if (a_3 < -32768) goto <L3>; else goto <L6>;

  # a_9 = PHI <a_3(3), 32767(2)>;
<L6>:;

  # a_2 = PHI <a_9(4), -32768(3)>;
<L3>:;
  <retval> = a_2;
  return <retval>;

}
-----------------------------


---


### compiler : `gcc`
### title : `Missed constant propagation into loops`
### open_at : `2006-11-06T11:01:32Z`
### last_modified_date : `2021-06-03T03:05:46Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=29738
### status : `RESOLVED`
### tags : `missed-optimization, xfail`
### component : `tree-optimization`
### version : `4.3.0`
### severity : `enhancement`
### contents :
For the following testcase

int i;
void foo (void);
void bar (void)
{
  int j;
  i = 0;
  for (j = 0; j < 10000; j++)
    if (i)
      foo ();
}

we cannot see that foo is never called and so the loop is empty.  The problem
is that i is part of the loop evolution and so appears in a PHI node so we
cannot figure out i is zero:

<bb 2>:
  #   i_3 = V_MUST_DEF <i_2>;
  i = 0;
  
  # NONLOCAL.6_19 = PHI <NONLOCAL.6_9(5), NONLOCAL.6_11(2)>;
  # i_18 = PHI <i_7(5), i_3(2)>;
  # j_17 = PHI <j_6(5), 0(2)>;
<L0>:;
  #   VUSE <i_18>;
  i.0_5 = i;
  if (i.0_5 != 0) goto <L1>; else goto <L2>;
  
<L1>:;
  #   i_12 = V_MAY_DEF <i_18>;
  #   NONLOCAL.6_13 = V_MAY_DEF <NONLOCAL.6_19>;
  foo ();
  
  # NONLOCAL.6_9 = PHI <NONLOCAL.6_19(3), NONLOCAL.6_13(4)>;
  # i_7 = PHI <i_18(3), i_12(4)>;
<L2>:;
  j_6 = j_17 + 1;
  if (j_6 <= 9999) goto <L0>; else goto <L4>;


I have no idea what optimization could catch this, though ;)


---


### compiler : `gcc`
### title : `SSE intrinsics hard to use without redundant temporaries appearing`
### open_at : `2006-11-07T22:22:55Z`
### last_modified_date : `2021-12-07T08:22:56Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=29756
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.1.2`
### severity : `enhancement`
### contents :
I've been adapting some old codes' simple 4-float vector class to use SSE by use of the intrinsic functions.  It seems to be quite hard to avoid the generated assembly code being rather diluted by apparently redundant spills of intermediate results to the stack.

On inspecting the assembly produced from the file to be attached, compare the code generated for matrix44f::transform_good and matrix44f::transform_bad.
The former is 20 instructions and apparently optimal.  However, it was only arrived at by prodding the latter version of the function (which does exactly the same thing but expressed more naturally, but results in 32 instructions) until the stack temporaries went away.  It would be nice if both versions of the function generated optimal code and there doesn't seem to be any particular reason they shouldn't.

Both versions' assembly contain the same expected numbers of shuffle, multiply and add instructions, the excess seems to all involve extra stack temporaries.

[I'm not sure what the "triplet" codes on this form are.
I'm using a gcc in Debian Etch  gcc --version shows "gcc (GCC) 4.1.2 20060901 (prerelease) (Debian 4.1.1-13)"; platform is a Pentium3.  Sorry if the "inline-asm" component is a completely inappropriate thing to assign to.]


---


### compiler : `gcc`
### title : `result of ffs/clz/ctz/popcount/parity are already sign-extended`
### open_at : `2006-11-09T07:10:45Z`
### last_modified_date : `2023-03-21T11:54:14Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=29776
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.3.0`
### severity : `normal`
### contents :
unfortunately the ffs/clz/ctz/popcount/parity builtins are defined to return signed types despite the fact they are either undefined or return a non-negative integer.  as a result unnecessary sign extension occurs.  for example in this case the result of bsf could be used directly in the mask[] index.

-dean

% cat ctz.c
unsigned mask[8];

unsigned foo(unsigned y, unsigned char x)
{
  return y & mask[__builtin_ctz(x)];
}
% ~/gcc/bin/gcc -g -O3 -Wall -c ctz.c
% objdump -dr ctz.o

ctz.o:     file format elf64-x86-64

Disassembly of section .text:

0000000000000000 <foo>:
   0:   40 0f b6 f6             movzbl %sil,%esi
   4:   0f bc f6                bsf    %esi,%esi
   7:   48 63 f6                movslq %esi,%rsi
   a:   23 3c b5 00 00 00 00    and    0x0(,%rsi,4),%edi
                        d: R_X86_64_32S mask
  11:   89 f8                   mov    %edi,%eax
  13:   c3                      retq
% ~/gcc/bin/gcc -v
Using built-in specs.
Target: x86_64-unknown-linux-gnu
Configured with: ../gcc/configure --prefix=/home/odo/gcc --enable-languages=c --enable-targets=x86_64-unknown-linux-gnu x86_64-unknown-linux-gnu : (reconfigured) ../gcc/configure --prefix=/home/odo/gcc --enable-languages=c --without-mudflap --disable-biarch x86_64-unknown-linux-gnu : (reconfigured) ../gcc/configure --prefix=/home/odo/gcc --enable-languages=c --disable-multilib --disable-biarch x86_64-unknown-linux-gnu
Thread model: posix
gcc version 4.3.0 20061104 (experimental)


---


### compiler : `gcc`
### title : `missed optimization: model missing vec_pack/unpack  idioms for ia64`
### open_at : `2006-11-09T10:18:50Z`
### last_modified_date : `2021-09-03T06:13:58Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=29778
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `target`
### version : `4.3.0`
### severity : `enhancement`
### contents :
We need to port the ia64 support for vectorization of multiple-datatypes from autovect-branch. This is the patch missing from mainline (wasn't included in http://gcc.gnu.org/ml/gcc-patches/2006-08/msg00166.html cause I cauldn't test this):

2005-12-02  Richard Henderson  <rth@redhat.com>

        * config/ia64/ia64.c (TARGET_VECTORIZE_BUILTIN_EXTRACT_EVEN): New.
        (TARGET_VECTORIZE_BUILTIN_EXTRACT_ODD): New.
        (TARGET_VECTORIZE_BUILTIN_MUL_WIDEN_EVEN,
        TARGET_VECTORIZE_BUILTIN_MUL_WIDEN_ODD, ia64_builtin_mul_widen_even,
        ia64_builtin_mul_widen_odd, builtin_ia64_pmpy_r, builtin_ia64_pmpy_l,
        IA64_BUILTIN_PMPY_R, IA64_BUILTIN_PMPY_L): New
        (ia64_init_builtins): Initialize builtin_ia64_pmpy_[rl].
        (ia64_expand_builtin): Expand them.
        (ia64_expand_unpack): New.
        * config/ia64/vect.md (smulv4hi3_highpart, umulv4hi3_highpart): New.
        (vec_pack_ssat_v4hi): Rename from pack2_sss.
        (vec_pack_usat_v4hi): Rename from pack2_uss.
        (vec_pack_ssat_v2si): Rename from pack4_sss.
        (vec_pack_mod_v4hi, vec_pack_mod_v2si): New.
        (vec_interleave_lowv8qi): Rename from unpack1_l.
        (vec_interleave_highv8qi): Rename from unpack1_h.
        (vec_interleave_lowv4hi): Rename from unpack2_l.
        (vec_interleave_highv4hi): Rename from unpack2_h.
        (vec_interleave_lowv2si): Rename from unpack4_l.
        (vec_interleave_highv2si): Rename from unpack4_h.
        (vec_unpacku_hi_v8qi, vec_unpacks_hi_v8qi): New.
        (vec_unpacku_lo_v8qi, vec_unpacks_lo_v8qi): New.
        (vec_unpacku_hi_v4hi, vec_unpacks_hi_v4hi): New.
        (vec_unpacku_lo_v4hi, vec_unpacks_lo_v4hi): New.
        * config/ia64/ia64-protos.h (ia64_expand_unpack): Declare.

Once the above is merged, we can add ia64 to the lists of targets that support the following functions in testsuite/lib/target-support.exp:
check_effective_target_vect_sdot_hi
check_effective_target_vect_udot_qi
check_effective_target_vect_sdot_qi
check_effective_target_vect_widen_sum_qi_to_hi
check_effective_target_vect_widen_sum_hi_to_si


---


### compiler : `gcc`
### title : `comment / code incosistency in cfgcleanup.c:flow_find_cross_jump`
### open_at : `2006-11-15T23:28:41Z`
### last_modified_date : `2019-03-05T09:18:11Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=29860
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.3.0`
### severity : `minor`
### contents :
http://gcc.gnu.org/ml/gcc/2005-01/msg00700.html

onsideriing this code:

 if (onlyjump_p (i2)
     || (returnjump_p (i2) && !side_effects_p (PATTERN (i2))))
   {
     last2 = i2;
     /* Count everything except for unconditional jump as insn.  */
     if (!simplejump_p (i2) && !returnjump_p (i2) && last1)
       ninsns++;
     i2 = PREV_INSN (i2);
   }


you count unconditional jumps with a clobber, but you don't count
conditional returns (, or even an instruction that solves a travelling
salesman problem and returns if it finds a solution within a given cost bound).


---


### compiler : `gcc`
### title : `union causes inefficient code`
### open_at : `2006-11-17T22:43:07Z`
### last_modified_date : `2021-06-08T09:26:08Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=29881
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.1.0`
### severity : `enhancement`
### contents :
hello!

I'm writing fast approximations of some complex math functions. I'm trying do them as low-level as possible, far from hand-written assembly though. I often check the assembly code to verify the quality of it. During one of the checkups i found that gcc (i checked 3.4.5/win32 and 4.0/4.1/fc5) doesn't make a good use of the xmm registers when writing a mixed SSE/SSE2 code.

example code:

#include <emmintrin.h>

typedef union {
        __m128i i;
        __m128 f;
} __vec128;

void array_sample_fun(__m128 *dst, const __m128  *src, int length) {
        __m128 af = _mm_set1_ps(1.20f);
        __m128 bf = _mm_set1_ps(2.88f);
        __m128 cf = _mm_set1_ps(-2.44f);
        __m128 df = _mm_set1_ps(4.06f);
        __m128 ef = _mm_set1_ps(-12.04f);

        __m128i mask = _mm_set1_epi32(0xff << 23);
        __m128i bias = _mm_set1_epi32(0x7f << 23);

        while (length-- != 0) {
                __vec128 vec;

                vec.f = *src++;
                __m128 arg = _mm_cvtepi32_ps(_mm_srai_epi32(_mm_sub_epi32(_mm_and_si128(vec.i, mask), bias), 23));
                vec.i = _mm_or_si128(_mm_andnot_si128(mask, vec.i), bias);
                *dst++ = _mm_add_ps(arg, _mm_add_ps(_mm_mul_ps(_mm_add_ps(_mm_mul_ps(_mm_add_ps(_mm_mul_ps(_mm_add_ps(
                        _mm_mul_ps(af, vec.f), bf), vec.f), cf), vec.f), df), vec.f), ef));
        }
}

the main loop of the function looks like this:

.L4:
        movaps  (%rsi), %xmm0
        addl    $1, %eax
        movdqa  %xmm4, %xmm2
        addq    $16, %rsi
        movaps  %xmm0, -24(%rsp)
        movdqa  -24(%rsp), %xmm0
        pandn   %xmm0, %xmm2
        movdqa  %xmm0, %xmm1
        movdqa  %xmm2, %xmm0
        pand    %xmm4, %xmm1
        por     %xmm3, %xmm0
        psubd   %xmm3, %xmm1
        psrad   $23, %xmm1
        cvtdq2ps        %xmm1, %xmm1
        movdqa  %xmm0, -24(%rsp)
        movaps  %xmm9, %xmm0
        movaps  -24(%rsp), %xmm2
        mulps   %xmm2, %xmm0
        addps   %xmm8, %xmm0
        mulps   %xmm2, %xmm0
        addps   %xmm7, %xmm0
        mulps   %xmm2, %xmm0
        addps   %xmm6, %xmm0
        mulps   %xmm2, %xmm0
        addps   %xmm5, %xmm0
        addps   %xmm0, %xmm1
        movaps  %xmm1, (%rdi)
        addq    $16, %rdi
        cmpl    %edx, %eax
        jne     .L4

As you can see whenever i try to access a float vector from integer SSE2 unit the compiler saves the register on the stack using movaps just to load it back to same register using movdqa one instruction later - which is totally unnecessary/inefficient! Same goes for accessing an integer value by SSE unit. Is this behavior 'patchable'?


---


### compiler : `gcc`
### title : `should do more loops transformations to enable more biv widening`
### open_at : `2006-11-22T19:20:25Z`
### last_modified_date : `2019-03-05T09:24:52Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=29944
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.3.0`
### severity : `normal`
### contents :
At the moment, we only do biv (basic induction variable) widening when we
can argue that overflow cuases undefined behaviour, as in:

int
f (int start, int end, int x, int y)
{
  short i;

  for (i = start; i < end; i++)
    x <<= y;
  return x;
}

However, for -ftrapv, we get the wrong result (it doesn't trap in case of
overflow), and for -fwrapv, no biv widening is done.

Likewise, if the biv is unsigned, as in:

int
f (int start, int end, int x, int y)
{
  unsigned short i;

  for (i = start; i < end; i++)
    x <<= y;
  return x;
}

we fail to do any biv widening.

Using suitable loop transformations, biv widening can be done safely without
a change in observable program behaviour.

If a cheap vector addition is available that adds units as wide as the
original biv size, proper updates of a narrow unsigned biv can be obtained
by making sure the biv is properly zero-extended at the loop entry,
and using the vector addition to do the increment.

If no cheap vector addition is available, or if defined operation on a
narrow signed biv is required, biv widening can be done safely by
transforming the loop into two nested loops, where end value of the inner
loop is calculated so that if the biv should overflow, the value of the biv
during the last iteration will be the value prior to the overflow.
The outer loop can then, if required, trap, calculate the new biv
value to archive wrap-around semantics, and continue looping.


---


### compiler : `gcc`
### title : `should use floating point registers for block copies`
### open_at : `2006-11-24T12:03:13Z`
### last_modified_date : `2023-07-22T02:50:51Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=29969
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.3.0`
### severity : `enhancement`
### contents :
In integer-dominated code, it is often useful to use floating point
registers to do block copies.  If suitable alignment is available,
64 bit loads / stores allow to do the copy with half as many memory
operations.  If the source is loop invariant, the loads can be
hoisted out of the loop; register pressure usually makes this
unfeasible for integer registers.
The destination, and, if not loop invariant, the source need to be
at least 32 bit aligned for this to be profitable (or at least there must
be a known constant offset to such an alignment.  At -O3, preconditioning
could be used to cover all possible offsets and select the code at
run-time).  Also, a minimum size is required.  The total size need not be
aligned, as smaller pieces can be copied in integer registers.

A testcase for this is the main loop of dhrystone, where
the two strings fit into 4 64-bit values each (after padding),
and cse allows to fit them in 5 64-bit values together.
Four of these fit into the call saved registers dr12, dr14, xd12 and xd14,
thus their loads can be hoisted out of the loop.

The tree of the current function could be examined for heuristics to
determine if using floating point registers for block copies makes sense
(look for high integer register pressure and low floating point register
pressure - call saved registers if a loop invariant crosses a call; might
also take different integer / floating point memory latencies into account
if the block is relatively short, by checking if there appear to be a
sufficient number of other instructions to hide some of the latency.
Alternatively or additionally, an option and/or parameters used in the
heuristics can be used to control the behaviour.

To increase the incidence of suitably aligned copies, constant alignment and
data alignment for block copy destinations of suitable size which are
defined in the current compilation unit should be increased to 64 bit,
and such data items should also be padded to 64 bits.
This may be controlled by an invocation option.
(If the last 64 bit item would contain no more than 32 bits, and the
 register pressure is too high to hoist out all loads, padding to fit 8
/ 16 / 32 bit is sufficient.  The latter padding is useful for integer
 copies in general)
When doing LTO, this might be expanded to items which are defined in other compilation units, and to special cases of indirect references.

The actual copy is best done exploiting post-increment for load and
pre-decrement for store, and is thus highly machine specific.  It therefore
seems best to do this in sh.c:expand_block_move.
Thus, STORE_BY_PIECES_P and MOVE_BY_PIECES_P will have to reject the
size and alignment combinations of copies that we want to handle this way.

Due to a quirk in the SH4 specification, we need a third fp_mode value
for 64 bit loads / stores (unless FMOVD_WORKS is true).
This mode has FPSCR.PR cleared and FPSCR.SZ set.
To get the full benefit for copies that are in a loop that does calls,
we should fix rtl-optimization/29349 first.
When using the -m4-single ABI, the new mode can be generated from the
normal mode by issuing one fschg instruction; we can switch back with
another fschg instruction.
For -m4a or -m4-300, we need both an fpchg and an fschg; -m4 must load
the new mode from a third value in fpscr_values.

The actual loads and stores must not look like ordinary SImode or DImode
loads and stores, because that would give - via GO_IF_LEGITIMATE_ADDRESS -
the wrong message to the optimizers about the available addressing modes.
Moreover, POST_INC / PRE_DEC are currently not allowed at rtl generation
time.
A possible sulution is to use patterns that pair the load / store
with an explicit set of the address register.  I'd prefer to use
two match_dup to keep the address register in sync, since otherwise
the optimizers can too easily hijack the pattern for something inappropriate.
The MEMs are probably best using SFmode / DFmode, but wrapping them in an
SImode / DImode unspec; however, care must be taken to still get the
right alias set for the MEM.


---


### compiler : `gcc`
### title : `Variable-length arrays (VLA) should be converted to normal arrays if possible`
### open_at : `2006-12-02T10:30:14Z`
### last_modified_date : `2023-08-07T09:55:53Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=30049
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.3.0`
### severity : `enhancement`
### contents :
The following program (split off from PR30032) needs with
"gcc -march=opteron -ffast-math -funroll-loops -ftree-vectorize -msse3
-O3 -g"
  0m6.478s
but if I use   #define NODES 2500  it only needs only
  0m1.390s

(The Intel compiler seems to do this conversion automatically and needs 0m1.879s for the VLA version of the program.)


void eos(const int NODES, const float CGAMMA, float CS[NODES], float PRES[NODES], const float DENS[NODES])
{
  int j;
  for(j = 0; j < NODES; j ++)
  {
    CS[j] = sqrt(CGAMMA*PRES[j]/DENS[j]);
  }
}

int main() {
  const int NODES = 25000;
  float CGAMMA;
  float DENS[NODES], CS[NODES], PRES[NODES];
  int i,j;
  for(i = 0; i < NODES; i++) {
     DENS[i] = 3.0;
     PRES[i] = 0.25;
  }
  CGAMMA = 2.0;
  for(i = 0; i < 20000; i++) {
    eos(NODES, CGAMMA, &CS, &PRES, &DENS);
    CGAMMA = CGAMMA + CS[1];
  }
  return (int)CGAMMA;
}


---


### compiler : `gcc`
### title : `Could use indexed addressing to reduce const costs`
### open_at : `2006-12-04T19:12:39Z`
### last_modified_date : `2021-11-06T07:32:35Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=30065
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.3.0`
### severity : `enhancement`
### contents :
Sometimes constants could be replaced by smaller, cheaper constants by
making use of scaled indices.


---


### compiler : `gcc`
### title : `Expansion of lceil and lfloor could use if-conversion`
### open_at : `2006-12-06T09:19:32Z`
### last_modified_date : `2021-08-23T02:37:43Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=30082
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.3.0`
### severity : `enhancement`
### contents :
> - ceiling
>       cvtss2si %xmmMM, %rNN
>       cvtsi2ss %rNN, %xmmJJ ;; scratch
>       ucomiss %xmmMM, %xmmJJ
>       adc $0, %rNN                    <<
>
> - floor
>       cvtss2si %xmmMM, %rNN
>       cvtsi2ss %rNN, %xmmJJ ;; scratch
>       ucomiss %xmmJJ, %xmmMM
>       sbb $0, %rNN                    <<

can be emitted directly using appropriate IF_THEN_ELSE rtx and not rely
on ifcvt figuring out itself (which it doesn't in most cases).


---


### compiler : `gcc`
### title : `missed value numbering optimization (conditional-based assertions)`
### open_at : `2006-12-07T05:55:50Z`
### last_modified_date : `2021-07-26T05:07:10Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=30099
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.3.0`
### severity : `enhancement`
### contents :
The following 2 functions should be compiled to the same assembly. 
This is one of Briggs' compiler benchmarks.

void vnum_test10(int *data)
{
  int i = data[0];
  int m = i + 1;
  int j = data[1];
  int n = j + 1;
  data[2] = m + n;
  if (i == j)
    data[3] = (m - n) * 21;
}
void vnum_result10(int *data)
{
  int i = data[0];
  int m = i + 1;
  int j = data[1];
  int n = j + 1;
  data[2] = m + n;
  if (i == j)
    data[3] = 0;
}


---


### compiler : `gcc`
### title : `missed value numbering optimization (cprop+valnum)`
### open_at : `2006-12-07T05:58:36Z`
### last_modified_date : `2021-07-26T20:39:36Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=30101
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.3.0`
### severity : `enhancement`
### contents :
The following 2 functions should be compiled to the same assembly. 
This is one of Briggs' compiler benchmarks.

void vnum_test12(int *data)
{
  int n;
  int stop = data[3];
  int j = data[1];
  int k = j;
  int i = 1;
  for (n=0; n<stop; n++) {
    if (j != k) i = 2;
    i = 2 - i;
    if (i != 1) k = 2;
    data[data[2]] = 2;
  }
  data[1] = i;
}
void vnum_result12(int *data)
{
  int n;
  int stop = data[3];
  for (n=0; n<stop; n++)
    data[data[2]] = 2;
  data[1] = 1;
}


---


### compiler : `gcc`
### title : `missed strength reduction optimization (irreducible loops)`
### open_at : `2006-12-07T06:00:40Z`
### last_modified_date : `2021-08-29T01:04:46Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=30102
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.3.0`
### severity : `enhancement`
### contents :
The following 2 functions should be compiled to the same assembly. 
This is one of Briggs' compiler benchmarks.


void strength_test4(int *data)
{
  int i;
  if (data[1]) {
    i = 2;
    goto here;
  }
  i = 0;
  do {
    i = i + 1;
here:
    data[data[2]] = 2;
  } while (i * 21 < data[3]);
}
void strength_result4(int *data)
{
  int i;
  if (data[1]) {
    i = 42;
    goto here;
  }
  i = 0;
  do {
    i = i + 21;
here:
    data[data[2]] = 2;
  } while (i < data[3]);
}


---


### compiler : `gcc`
### title : `missed strength reduction optimization (test replacement)`
### open_at : `2006-12-07T06:09:59Z`
### last_modified_date : `2021-12-03T10:31:36Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=30103
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.3.0`
### severity : `enhancement`
### contents :
The following 2 functions should be compiled to the same assembly. 
This is one of Briggs' compiler benchmarks.

void strength_test10(int *data)
{
  int stop = data[3];
  int i = 0;
  do {
    data[data[2]] = 21 * i;
    i = i + 1;
  } while (i < stop);
}
void strength_result10(int *data)
{
  int stop = data[3] * 21;
  int i = 0;
  do {
    data[data[2]] = i;
    i = i + 21;
  } while (i < stop);
}


---


### compiler : `gcc`
### title : `byte independent store not done in some cases due to truncation of addition too early`
### open_at : `2006-12-09T03:05:27Z`
### last_modified_date : `2021-12-25T07:53:55Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=30128
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.1.0`
### severity : `enhancement`
### contents :
The program...

/* ------------------------------------------- */
#define GSF_LE_SET_GUINT32(p, dat)				\
	((*((char *)(p) + 0) = (char) ((dat))       & 0xff),	\
	 (*((char *)(p) + 1) = (char) ((dat) >>  8) & 0xff),	\
	 (*((char *)(p) + 2) = (char) ((dat) >> 16) & 0xff),	\
	 (*((char *)(p) + 3) = (char) ((dat) >> 24) & 0xff))

void bar (void *);

void
foo (unsigned i)
{
  char buffer[4];
  unsigned len = i + 1;

  GSF_LE_SET_GUINT32 (buffer, len + 1);

  bar (buffer);
}
/* ------------------------------------------- */

...generates the code below.  Note, that there are two additions in the
generated code and that an extra register is used.  It is as-if the least
significant byte is seen as unrelated to the three others.

foo:
        pushl   %ebp
        movl    %esp, %ebp
        subl    $24, %esp
        movl    8(%ebp), %eax
        leal    2(%eax), %edx          <-- one addition into edx
        addl    $2, %eax               <-- second one to eax
        shrl    $8, %eax
        movb    %al, -3(%ebp)
        shrl    $8, %eax
        movb    %al, -2(%ebp)
        shrl    $8, %eax
        movb    %al, -1(%ebp)
        leal    -4(%ebp), %eax
        movb    %dl, -4(%ebp)
        movl    %eax, (%esp)
        call    bar
        leave
        ret


---


### compiler : `gcc`
### title : `accessing an element via a "pointer" on a vector does not cause vec_extract to be used (non constant index)`
### open_at : `2006-12-12T22:35:50Z`
### last_modified_date : `2020-01-22T11:38:58Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=30187
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.3.0`
### severity : `enhancement`
### contents :
#define vector __attribute__((vector_size(16)))
float f(vector float t, int i)
{
  return ((float*)&t)[i];
}


---


### compiler : `gcc`
### title : `gcc doesn't unroll nested loops`
### open_at : `2006-12-13T16:22:32Z`
### last_modified_date : `2021-08-29T21:43:30Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=30201
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.1.1`
### severity : `enhancement`
### contents :
While developing a Free C++ library, I am facing what I think is a bug in gcc: it doesn't unroll nested loops. Namely, in the example program that I paste below, there is a nested loop like

for( int i = 0; i < 3; i++ )
  for( int j = 0; j < 3; j++ )
    do_something( i, j );

and only the inner loop gets completely unrolled (the loop on j), the outer loop (on i) is only partially unrolled (this is according to I. L. Taylor on gcc@gcc.gnu.org, I don't have the skill to read the binary code).

This is a huge problem for me, not only a detail, as the performance of my code is about 15% of what it would be if the loops got unrolled.

I cannot unroll loops by hand because this is a template library and the loops depend on template parameters.

I have made a minimal standalone example program. I paste it below (toto.cpp).

This program does a nested loop if UNROLL is not defined, and does the same thing but with the loops unrolled by hand if UNROLL is defined. On my machine, the speed difference is huge:

g++ -DUNROLL -O3 toto.cpp -o toto   ---> toto runs in 0.3 seconds
g++ -O3 toto.cpp -o toto            ---> toto runs in 1.9 seconds

Again, this is not an academic example but something found in a real library, Eigen (http://eigen.tuxfamily.org). Granted, it's a math library, but still one that is used in real apps, so fixing this gcc bug would benefit real apps.

So here is the example program toto.cpp:

-----------------------------------------------------------------------

#include<iostream>

class Matrix
{
public:
    double data[9];
    double & operator()( int i, int j )
    {
        return data[i + 3 * j];
    }
    void loadScaling( double factor );
};

void Matrix::loadScaling( double factor)
{
#ifdef UNROLL
    (*this)( 0, 0 ) = factor;
    (*this)( 1, 0 ) = 0;
    (*this)( 2, 0 ) = 0;
    (*this)( 0, 1 ) = 0;
    (*this)( 1, 1 ) = factor;
    (*this)( 2, 1 ) = 0;
    (*this)( 0, 2 ) = 0;
    (*this)( 1, 2 ) = 0;
    (*this)( 2, 2 ) = factor;
#else
    for( int i = 0; i < 3; i++ )
        for( int j = 0; j < 3; j++ )
            (*this)(i, j) = (i == j) * factor;
#endif
}

int main( int argc, char *argv[] )
{
    Matrix m;
    for( int i = 0; i < 100000000; i++ )
        m.loadScaling( i );
    std::cout << "m(0,0) = " << m(0,0) << std::endl;
    return 0;
}


---


### compiler : `gcc`
### title : `folding (~ -x) >= (-2147483647-1) to x != -2147483648`
### open_at : `2006-12-20T14:35:40Z`
### last_modified_date : `2023-10-02T03:37:47Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=30267
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.1.1`
### severity : `minor`
### contents :
This program shows that some range propagation became worse between
gcc 4.0.2 and gcc 4.1.1.

=========================== foo.c ========================
int notneg (int x)
{
  return (~ -x) >= (-2147483647-1);
}
int negnot (int x)
{
  return (- ~x) <= 2147483647;
}
==========================================================


# With gcc 4.0.2 on i686-pc-linux-gnu the code is fully optimized:

$ gcc -O2 -fomit-frame-pointer -S foo.c && cat foo.s
        .file   "foo.c"
        .text
        .p2align 4,,15
.globl notneg
        .type   notneg, @function
notneg:
        movl    $1, %eax
        ret
        .size   notneg, .-notneg
        .p2align 4,,15
.globl negnot
        .type   negnot, @function
negnot:
        movl    $1, %eax
        ret
        .size   negnot, .-negnot
        .ident  "GCC: (GNU) 4.0.2"
        .section        .note.GNU-stack,"",@progbits


# With gcc 4.1.1 on i686-pc-linux-gnu the code is fully optimized with -fwrapv
# but not without -fwrapv:

$ gcc -O2 -fomit-frame-pointer -S foo.c && cat foo.s
        .file   "foo.c"
        .text
        .p2align 4,,15
.globl notneg
        .type   notneg, @function
notneg:
        xorl    %eax, %eax
        cmpl    $-2147483648, 4(%esp)
        setne   %al
        ret
        .size   notneg, .-notneg
        .p2align 4,,15
.globl negnot
        .type   negnot, @function
negnot:
        xorl    %eax, %eax
        cmpl    $2147483647, 4(%esp)
        setne   %al
        ret
        .size   negnot, .-negnot
        .ident  "GCC: (GNU) 4.1.1"
        .section        .note.GNU-stack,"",@progbits

$ gcc -O2 -fomit-frame-pointer -fwrapv -S foo.c && cat foo.s
        .file   "foo.c"
        .text
        .p2align 4,,15
.globl notneg
        .type   notneg, @function
notneg:
        movl    $1, %eax
        ret
        .size   notneg, .-notneg
        .p2align 4,,15
.globl negnot
        .type   negnot, @function
negnot:
        movl    $1, %eax
        ret
        .size   negnot, .-negnot
        .ident  "GCC: (GNU) 4.1.1"
        .section        .note.GNU-stack,"",@progbits

So somehow this seems to be linked to flag_wrapv. But regardless which
value is the result after signed overflow, any int >= INT_MIN and
any int <= INT_MAX should evaluate to 1 unconditionally.


---


### compiler : `gcc`
### title : `-mstrict-align can an store extra for struct agrument passing`
### open_at : `2006-12-21T02:49:05Z`
### last_modified_date : `2022-03-08T16:20:48Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=30271
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `target`
### version : `4.3.0`
### severity : `normal`
### contents :
Testcase:
struct a { short t, t1;};
int f(struct a b) { return b.t; }
Without -mstrict-align, we get:
.L.f:
        srawi 3,3,16
        extsw 3,3
        blr

But with we get:
.L.f:
        stw 3,48(1)
        nop
        nop
        nop
        lha 3,48(1)
        extsw 3,3
        blr


---


### compiler : `gcc`
### title : `tail call with additional arguments`
### open_at : `2006-12-24T23:08:30Z`
### last_modified_date : `2021-07-26T09:38:00Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=30288
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.3.0`
### severity : `enhancement`
### contents :
This tail call could be optimized:  Just
push the final 0, then jump.

$ cat tail.c
int foo (int, int);

int bar (int i)
{
  return foo (i, 0);
}
$ gcc -fomit-frame-pointer -S -O3  tail.c
$ cat tail.s
        .file   "tail.c"
        .text
        .p2align 4,,15
.globl bar
        .type   bar, @function
bar:
        subl    $12, %esp
        movl    16(%esp), %eax
        movl    $0, 4(%esp)
        movl    %eax, (%esp)
        call    foo
        addl    $12, %esp
        ret
        .size   bar, .-bar
        .ident  "GCC: (GNU) 4.3.0 20061211 (experimental)"
        .section        .note.GNU-stack,"",@progbits


---


### compiler : `gcc`
### title : `printf->puts optimization prevented by %%`
### open_at : `2006-12-26T15:27:14Z`
### last_modified_date : `2022-01-05T23:30:06Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=30306
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.2.0`
### severity : `enhancement`
### contents :
If %% is used in printf formats without any actual format requiring substitution being used, gcc still does not perform the optimization.

#include <stdio.h>
int
main (void)
{
  printf ("hello %%%%!\n");
  return  0;
}

This code is compiled to call printf even though it should lead to code calling puts with the string containing "hello %%!".


---


### compiler : `gcc`
### title : `optimize multiply-by-constant overflow (wrap) test`
### open_at : `2006-12-28T06:46:08Z`
### last_modified_date : `2023-05-18T09:37:39Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=30314
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `unknown`
### severity : `enhancement`
### contents :
I was experimenting with some code to test for overflow (wrapping) in unsigned multiplication in C.  My test code:

typedef unsigned long size_t;
extern void *malloc(size_t), abort(void);
void *allocate(size_t num) {
    const size_t size = 140;
    size_t total = num * size;

    if (total / size != num) abort();
    /* call malloc, whatever */
    return 0;
}

With snapshot gcc-4.3-20061223, hosted on ppc Mac, targeted for i386-linux, options "-O9 -fomit-frame-pointer -fexpensive-optimizations -S", the generated assembly code is:

allocate:
        subl    $12, %esp
        movl    16(%esp), %ecx
        leal    (%ecx,%ecx,4), %eax
        leal    0(,%eax,8), %edx
        subl    %eax, %edx
        andl    $1073741823, %edx
        movl    $981706811, %eax
        mull    %edx
        shrl    $3, %edx
        cmpl    %ecx, %edx
        jne     .L6
        xorl    %eax, %eax
        addl    $12, %esp
        ret
.L6:
        call    abort

In this assembly code, the division has been implemented via multiplication, and the result is compared against the original value.

Dividing 2**32-1 by 140 gives 30678337 and a fraction.  If the supplied NUM is larger than that, it can't be equal to the quotient of any 32-bit number divided by 140.  If it's 30678337 or less, the multiplication can't wrap, and thus the quotient must be equal to the original value.

Since the quotient, as such, isn't of any other use in this code, I think it would be more efficient, and give the same result, to test NUM<=30678337, and omit the division altogether.  (And since the malloc call in the comment isn't actually made in this example, the product stored in TOTAL isn't needed either, if we don't do the division.)

I think on x86 we could also test the carry flag after the multiply operation.


---


### compiler : `gcc`
### title : `optimize unsigned-add overflow test on x86 to use cpu flags from addl`
### open_at : `2006-12-28T07:09:00Z`
### last_modified_date : `2019-06-06T12:28:20Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=30315
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `target`
### version : `unknown`
### severity : `enhancement`
### contents :
Using gcc-4.3-20061223 targeting i386-linux and options "-O9 -fomit-frame-pointer -fexpensive-optimizations -S", my test program to detect unsigned integer overflow:

extern void abort(void);
unsigned foo(unsigned a, unsigned b) {
    unsigned sum = a + b;
    if (sum < a) abort(); /* check for overflow (wrapping) */
    if (sum < b) abort(); /* redundant */
    return sum;
}

compiles to:

foo:
        subl    $12, %esp
        movl    16(%esp), %eax
        movl    20(%esp), %edx
        addl    %eax, %edx
        cmpl    %edx, %eax
        ja      .L7
        cmpl    %edx, 20(%esp)
        ja      .L7
        movl    %edx, %eax
        addl    $12, %esp
        ret
.L7:
        call    abort

After the addition, which sets the ALU flags, the compiler issues two compare instructions and conditional branches.  This sequence could be replaced by a conditional branch following the addl, testing one of the flags (overflow? carry? I forget which) set by it.

I realize for other processors (e.g., with -march=pentiumpro), the addl may be replaced by something like leal, which may not set the flags the same way.  But if the flags are set when building for a certain architecture, use them....  And is leal+cmp with data dependence still going to be better than addl?

(Also, I think a different set of register selections could eliminate the last "movl" instruction, by putting the result of the addition into the return-value register.)


---


### compiler : `gcc`
### title : `-Os doesn't optimize a/CONST even if it saves size.`
### open_at : `2007-01-02T22:09:42Z`
### last_modified_date : `2021-12-21T11:42:00Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=30354
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `target`
### version : `4.1.1`
### severity : `enhancement`
### contents :
gcc -O2 usually optimizes a/CONST. In many cases code is not only significantly faster, but also smaller:

unsigned f(unsigned a) { return a/10; }

gcc 4.1.1 -O2:
        movl    $-858993459, %eax
        mull    4(%esp)
        shrl    $3, %edx
        movl    %edx, %eax
        ret

gcc 4.1.1 -Os:
        movl    4(%esp), %eax
        movl    $10, %edx
        movl    %edx, %ecx
        xorl    %edx, %edx
        divl    %ecx
        ret

Unfortunately, gcc -S never uses this optimization.

Note that with code proposed in bug 28417 a/CONST can be optimized even further (we can use smaller mul constant and avoid shrl) when we know from VRP that value of a is always small enough.


---


### compiler : `gcc`
### title : `memmove for string operations`
### open_at : `2007-01-06T22:05:43Z`
### last_modified_date : `2020-11-11T09:31:30Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=30398
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.3.0`
### severity : `enhancement`
### contents :
The compiler should be able to detect that s and c
are not aliased, so a call to memcpy instead of memmove
could be issued.

$ cat memmove.f90
program main
  character(len=1) :: s
  character(len=2) :: c
  s = 'a'
  c = repeat(s,2)
end program main
$ gfortran -fdump-tree-original memmove.f90
$ cat memmove.f90.003t.original
MAIN__ ()
{
  char c[1:2];
  char s[1:1];

  _gfortran_set_std (70, 127, 0);
  s[1]{lb: 1 sz: 1} = "a"[1]{lb: 1 sz: 1};
  {
    char str.0[2];

    _gfortran_string_repeat ((char[1:] *) &str.0, 1, &s, 2);
    __builtin_memmove (&c, (char[1:] *) &str.0, 2);
  }
}


---


### compiler : `gcc`
### title : `Expanded array initialization can use memset builtin function`
### open_at : `2007-01-11T19:53:35Z`
### last_modified_date : `2022-01-28T23:47:52Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=30442
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.3.0`
### severity : `enhancement`
### contents :
Array initialization could use memset builtin function. In following two testcases, array is initialized without use of memset:

--cut here--
long long foo(long long *);

long long test1(void)
{
  long long a[32];

  a[0] = 0;
  a[1] = 0;
  a[2] = 0;
  a[3] = 0;
  a[4] = 0;
  a[5] = 0;
  a[6] = 0;
  a[7] = 0;
  a[8] = 0;
  a[9] = 0;
  a[10] = 0;
  a[11] = 0;
  a[12] = 0;
  a[13] = 0;
  a[14] = 0;
  a[15] = 0;
  a[16] = 0;
  a[17] = 0;
  a[18] = 0;
  a[19] = 0;
  a[20] = 0;
  a[21] = 0;
  a[22] = 0;
  a[23] = 0;
  a[24] = 0;
  a[25] = 0;
  a[26] = 0;
  a[27] = 0;
  a[28] = 0;
  a[29] = 0;
  a[30] = 0;
  a[31] = 0;

  return foo(a);
}

long long test2(void)
{
  long long a[32];
  int i;

  for (i = 0; i < 32; i++)
    a[i] = 0;

  return foo(a);
}
--cut here--

gcc -O3 -m32 -S -fomit-frame-pointer

test1:
        subl    $268, %esp
        leal    8(%esp), %eax
        movl    $0, 8(%esp)
        movl    $0, 12(%esp)
        movl    $0, 16(%esp)
        movl    $0, 20(%esp)
        movl    $0, 24(%esp)
        movl    $0, 28(%esp)
        movl    $0, 32(%esp)
        movl    $0, 36(%esp)
        movl    $0, 40(%esp)
        movl    $0, 44(%esp)
        movl    $0, 48(%esp)
        movl    $0, 52(%esp)
        movl    $0, 56(%esp)
        movl    $0, 60(%esp)
        movl    $0, 64(%esp)
        movl    $0, 68(%esp)
        movl    $0, 72(%esp)
        movl    $0, 76(%esp)
        movl    $0, 80(%esp)
        movl    $0, 84(%esp)
        movl    $0, 88(%esp)
        movl    $0, 92(%esp)
        movl    $0, 96(%esp)
        movl    $0, 100(%esp)
        movl    $0, 104(%esp)
        movl    $0, 108(%esp)
        movl    $0, 112(%esp)
        movl    $0, 116(%esp)
        movl    $0, 120(%esp)
        movl    $0, 124(%esp)
        movl    $0, 128(%esp)
        movl    $0, 132(%esp)
        movl    $0, 136(%esp)
        movl    $0, 140(%esp)
        movl    $0, 144(%esp)
        movl    $0, 148(%esp)
        movl    $0, 152(%esp)
        movl    $0, 156(%esp)
        movl    $0, 160(%esp)
        movl    $0, 164(%esp)
        movl    $0, 168(%esp)
        movl    $0, 172(%esp)
        movl    $0, 176(%esp)
        movl    $0, 180(%esp)
        movl    $0, 184(%esp)
        movl    $0, 188(%esp)
        movl    $0, 192(%esp)
        movl    $0, 196(%esp)
        movl    $0, 200(%esp)
        movl    $0, 204(%esp)
        movl    $0, 208(%esp)
        movl    $0, 212(%esp)
        movl    $0, 216(%esp)
        movl    $0, 220(%esp)
        movl    $0, 224(%esp)
        movl    $0, 228(%esp)
        movl    $0, 232(%esp)
        movl    $0, 236(%esp)
        movl    $0, 240(%esp)
        movl    $0, 244(%esp)
        movl    $0, 248(%esp)
        movl    $0, 252(%esp)
        movl    $0, 256(%esp)
        movl    $0, 260(%esp)
        movl    %eax, (%esp)
        call    foo
        addl    $268, %esp
        ret

test2:
        subl    $268, %esp
        movl    $2, %eax
        movl    $0, 8(%esp)
        leal    8(%esp), %edx
        movl    $0, 12(%esp)
        .p2align 4,,7
.L2:
        movl    $0, -8(%edx,%eax,8)
        movl    $0, -4(%edx,%eax,8)
        addl    $1, %eax
        cmpl    $33, %eax
        jne     .L2
        movl    %edx, (%esp)
        call    foo
        addl    $268, %esp
        ret

IIRC, this optimization was recently implemented in gfrortran...


---


### compiler : `gcc`
### title : `GCC should know about errno`
### open_at : `2007-01-23T10:37:38Z`
### last_modified_date : `2023-03-21T04:16:54Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=30555
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.3.0`
### severity : `enhancement`
### contents :
On systems where possible, GCC should get knowledge about the errno location so
it can clobber the right memory location for calls only setting errno.

On glibc the errno location is obtained using a call to the __errno_location ()
library function, so the obvious thing would be to introduce __builtin_errno_location () on this (or similar) system(s) and teach aliasing
the special property of its return value and its relation to errno setting
functions.


---


### compiler : `gcc`
### title : `extra register zero extends on x86_64`
### open_at : `2007-02-17T04:50:36Z`
### last_modified_date : `2023-07-06T01:50:08Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=30829
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.3.0`
### severity : `normal`
### contents :
this may or may not be the same as #29775.

% cat extra-mov.c <<EOF
unsigned *table;
unsigned shift;

unsigned foo1(unsigned p)
{
  unsigned block = p >> shift;
  unsigned value = table[block];
  return (value >> 8);
}
EOF
% gcc -g -O3 -Wall   -c -o extra-mov.o extra-mov.c
% objdump -dr extra-mov.o

extra-mov.o:     file format elf64-x86-64

Disassembly of section .text:

0000000000000000 <foo1>:
   0:   8b 0d 00 00 00 00       mov    0(%rip),%ecx        # 6 <foo1+0x6>
                        2: R_X86_64_PC32        shift+0xfffffffffffffffc
   6:   48 8b 05 00 00 00 00    mov    0(%rip),%rax        # d <foo1+0xd>
                        9: R_X86_64_PC32        table+0xfffffffffffffffc
   d:   d3 ef                   shr    %cl,%edi
   f:   89 ff                   mov    %edi,%edi
  11:   8b 04 b8                mov    (%rax,%rdi,4),%eax
  14:   c1 e8 08                shr    $0x8,%eax
  17:   c3                      retq

the "mov %edi,%edi" is presumably there as a 32->64 extend... but it's not necessary because %edi was written in previous instruction.

% gcc -v
Using built-in specs.
Target: x86_64-unknown-linux-gnu
Configured with: ../gcc/configure --prefix=/home/odo/gcc --disable-multilib --disable-biarch x86_64-unknown-linux-gnu --enable-languages=c
Thread model: posix
gcc version 4.3.0 20070217 (experimental)

i've seen it in 4.1.1 too.

-dean


---


### compiler : `gcc`
### title : `duplicated data in .rodata / .rodata.cst sections.`
### open_at : `2007-03-05T14:29:05Z`
### last_modified_date : `2021-08-24T05:10:28Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=31043
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.1.2`
### severity : `enhancement`
### contents :
$ cat pi.cpp
#include <cmath>
extern double const pi = M_PI;
extern double foo() { return pi; }


        .section        .rodata.cst8,"aM",@progbits,8
        .align 8

.LC0:   .long   1413754136
        .long   1074340347

.globl pi
        .section        .rodata
        .align 8

pi:     .long   1413754136
        .long   1074340347

_Z3foov:
        pushl   %ebp
        movl    %esp, %ebp
        fldl    .LC0
        popl    %ebp
        ret


---


### compiler : `gcc`
### title : `missed auto-vectorization optimization, when there is float to int conversion`
### open_at : `2007-03-06T12:44:31Z`
### last_modified_date : `2022-03-08T16:20:47Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=31055
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.3.0`
### severity : `enhancement`
### contents :
On powerpc, current auto-vectorizer does not vectorize loops that have conversion from float to int statement in it.
For example, in case we have the following program:

#include <stdarg.h>

#define N 32

int main1 ()
{
  int i;
  int ib[N]; 
  float fa[N] = {0.2,3.1,6.7,6.9,9.8,12.3,15.4,18.9,21.0,24,27,30,33,36,39,42,45,0,3,6,9,12,15,18,21,24,27,30,33,36,39,42};

  /* int -> float */
  for (i = 0; i < N; i++)
    {
      ib[i] = (int) fa[i];      
    }

    /* check results:  */
  for (i = 0; i < N; i++)
    {
      if (ib[i] != (int)fa[i]) 
        abort (); 
    }   

  return 0;
}

The vectorizer output is:
"not vectorized: relevant stmt not supported: D.2488_7 = (int) D.2487_6"
since there is no target hook for float to int conversion in rs6000 (altivec).


---


### compiler : `gcc`
### title : `[7 Regression] VRP no longer derives range for division after negation`
### open_at : `2007-03-11T11:43:02Z`
### last_modified_date : `2021-09-14T07:09:21Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=31130
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.3.0`
### severity : `normal`
### contents :
extern void link_error ();
void foo (int a)
{
  if (a < 0)
    {
      int y;
      a = -a;
      y  = a / 7;
      if (y > 1 << 30)
        link_error ();
    }
}

int main()
{
  return 0;
}

Before the VRP overflow handling changes we have after the first VRP pass:

Value ranges after VRP:

a_1(D): VARYING
a_2: [1, +INF]  EQUIVALENCES: { } (0 elements)
y_3: [0, 306783378]  EQUIVALENCES: { } (0 elements)
a_4: [-INF, -1]  EQUIVALENCES: { a_1(D) } (1 elements)

Substituing values and folding statements

Folding predicate y_3 > 1073741824 to 0
Folded statement: if (y_3 > 1073741824) goto <L1>; else goto <L2>;
            into: if (0) goto <L1>; else goto <L2>;

void foo(int) (a)
{
  int y;

<bb 2>:
  if (a_1(D) < 0) goto <L0>; else goto <L2>;

<L0>:;
  a_2 = -a_1(D);
  y_3 = a_2 / 7;

<L2>:;
  return;

}


while now we get

Value ranges after VRP:

a_1(D): VARYING
a_2: [1, +INF(OVF)]  EQUIVALENCES: { } (0 elements)
y_3: [0, +INF(OVF)]  EQUIVALENCES: { } (0 elements)
a_4: [-INF, -1]  EQUIVALENCES: { a_1(D) } (1 elements)

Substituing values and folding statements

foo (a)
{
  int y;

<bb 2>:
  if (a_1(D) < 0) goto <L0>; else goto <L2>;

<L0>:;
  a_2 = -a_1(D);
  y_3 = a_2 / 7;
  if (y_3 > 1073741824) goto <L1>; else goto <L2>;

<L1>:;
  link_error ();

<L2>:;
  return;

}


without -Wstrict-overflow=N warning about the issues with signed negation
and the [1, +INF(OVF)] derived range.  Note that the testcase is simple
enough that expansion optimizes the comparison, so it will not fail to link.


---


### compiler : `gcc`
### title : `cmpxchgq not emitted.`
### open_at : `2007-03-14T09:59:28Z`
### last_modified_date : `2021-05-31T00:39:50Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=31170
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `target`
### version : `4.2.0`
### severity : `enhancement`
### contents :
long emit_cmpxchg( long volatile* p, long from, long to )
{
        long v = *p;
        if ( v == from )
                *p = to;
        return v;
}

gcc should be able to optimize this.


---


### compiler : `gcc`
### title : `reorder class data members to minimize space waste`
### open_at : `2007-03-14T17:36:48Z`
### last_modified_date : `2021-08-16T12:54:39Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=31176
### status : `NEW`
### tags : `ABI, missed-optimization`
### component : `c++`
### version : `4.1.0`
### severity : `enhancement`
### contents :
While discussing how today's C++ compilers lay out data members of structs and classes on the C++ committee's mailing list the observation was made that no known implementation, including gcc, takes advantage of the permission to rearrange members declared with their own access specifier (see c++std-core-11977). For example, the data members of the following struct are laid out in declaration order even though a more space efficient order is possible:

    struct S { public: char c; public: int i; public: char d; };

This problem is especially hard to solve in template code where the sizes of one or more data members are not known, such as:

    template <class T, class U, class V>
    struct Triple { public: T a; public: U b; public: V c; };

Since reordering of existing structs would introduce a binary incompatibility I would like to propose that a mechanism be provided whereby authors of new code can mark up their types and/or data members in order to permit the compiler to rearrange them in a space efficient manner, until gcc implements a new ABI where the reordering algorithm becomes the default.

For example, a new type and/or variable attribute could be added (call it reorder), that could be used to mark up types and/or data members to participate in the reordering. To allow the compiler to arrange Triple members in an efficient way the template would be marked up as follows:

    template <class T, class U, class V>
    struct Triple __attribute__ ((reorder)) {
       public: T a; public: U b; public: V c;
    };

or, alternatively, like so:

    template <class T, class U, class V>
    struct Triple {
       public: T a __attribute__ ((reorder));
       public: U b __attribute__ ((reorder));
       public: V c __attribute__ ((reorder));
    };

The order of members declared in the same section (introduced and closed by an access specifier) without the attribute would not participate in the reordering with one another.

Members of reordered aggregates would be initialized in declaration order.


---


### compiler : `gcc`
### title : `VRP can infer a range for b in a >> b and a << b`
### open_at : `2007-03-14T21:12:52Z`
### last_modified_date : `2022-04-06T13:16:27Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=31178
### status : `NEW`
### tags : `easyhack, missed-optimization`
### component : `tree-optimization`
### version : `4.3.0`
### severity : `enhancement`
### contents :
namely [0, n) where n is the width of type a.  (Or better type a's mode to be safe).  Look at infer_value_range().


---


### compiler : `gcc`
### title : `Too many instructions as not reversing loop`
### open_at : `2007-03-17T10:15:39Z`
### last_modified_date : `2021-11-29T05:42:19Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=31238
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.1.1`
### severity : `normal`
### contents :
Build the following code with "gcc -std=c99 -Wall -Wextra -Werror -Os -S":
void q(const unsigned int);
void f() {for (unsigned int x = 0; x != 10; ++x) q(77);}

The loop becomes:
.L2:
        subl    $12, %esp
        incl    %ebx
        pushl   $77
        call    q
        addl    $16, %esp
        cmpl    $10, %ebx
        jne     .L2

This is 7 instructions, which is too much. The following equivalent program:
void q(const unsigned int);
void f() {for (unsigned int x = 10; x; --x) q(77);}

becomes:
.L2:
        subl    $12, %esp
        pushl   $77
        call    q
        addl    $16, %esp
        decl    %ebx
        jne     .L2

which is only 6 instructions. Since the programs are equivalent (both just call q(77) 10 times) and the second version becomes shorter than the first, the first version is not optimized properly.

The corresponding Ada program with q.ads:
procedure Q(N : in Natural);

and f.adb:
with Q;
procedure F is begin for i in 1 .. 10 loop Q(77); end loop; end F;

built with "gnatgcc -Os -Wall -Wextra -Wextra -Werror -S f.adb" produces the following loop:
.L5:
       pushl   $77
.LCFI3:
       call    _ada_q
       popl    %eax
       decl    %ebx
       jns     .L5

which is only 5 instructions. I know that situations are often encountered where C code can not be optimized as much as Ada code, because it would break some bizarre C feature. I do not know it this is such a situation, or if the C code could actually become as tight as the Ada code when compiled and optimized.

But at least the first version of the C code should be optimized to be as tight as the second version.

(Tested with gcc 4.1.1 (Gentoo 4.1.1-r3) and gnatgcc 3.4.5 (from Gentoo dev-lang/gnat-3.45).)


---


### compiler : `gcc`
### title : `Post Increment opportunity missed`
### open_at : `2007-03-17T14:10:36Z`
### last_modified_date : `2022-07-12T06:03:47Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=31241
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.2.0`
### severity : `enhancement`
### contents :
A simple code that adds a 'value' too all the elements of an array should generate post increments while loading/storing values from/into the array. The code looks something like this
  
for (i = 0; i < 10; i++) {
    *(intArray++) |= value;
}

However a post increment is not generated at O3 ( that causes the tree-optimizer to unroll the loop)

Here is the information of the toolchain and the code produced.

$>arm-none-eabi-gcc -v -O3 -S enhance.c --save-temps -o-
Using built-in specs.
Target: arm-none-eabi
Configured with: /mnt/tools/fsf/build/combined-arm-none-eabi-gcc-4.2-branch-2007-03-16/configure --target=arm-none-eabi --prefix=/mnt/tools/fsf/install/arm-none-eabi-gcc-4.2-branch-2007-03-16 --enable-languages=c,c++ --disable-nls --with-newlib --disable-gdbtk --disable-libssp
Thread model: single
gcc version 4.2.0 20070315 (prerelease)
 /mnt/tools/fsf/install/arm-none-eabi-gcc-4.2-branch-2007-03-16/libexec/gcc/arm-none-eabi/4.2.0/cc1 -E -quiet -v -D__USES_INITFINI__ enhance.c -O3 -fpch-preprocess -o enhance.i
ignoring nonexistent directory "/mnt/tools/fsf/install/arm-none-eabi-gcc-4.2-branch-2007-03-16/lib/gcc/arm-none-eabi/4.2.0/../../../../arm-none-eabi/sys-include"
ignoring nonexistent directory "/mnt/tools/fsf/install/arm-none-eabi-gcc-4.2-branch-2007-03-16/lib/gcc/arm-none-eabi/4.2.0/../../../../arm-none-eabi/include"#include "..." search starts here:
#include <...> search starts here:
 /mnt/tools/fsf/install/arm-none-eabi-gcc-4.2-branch-2007-03-16/lib/gcc/arm-none-eabi/4.2.0/include
End of search list.
 /mnt/tools/fsf/install/arm-none-eabi-gcc-4.2-branch-2007-03-16/libexec/gcc/arm-none-eabi/4.2.0/cc1 -fpreprocessed enhance.i -quiet -dumpbase enhance.c -auxbase-strip - -O3 -version -o-
GNU C version 4.2.0 20070315 (prerelease) (arm-none-eabi)
        compiled by GNU C version 4.0.3 (Ubuntu 4.0.3-1ubuntu5).
GGC heuristics: --param ggc-min-expand=97 --param ggc-min-heapsize=127206
Compiler executable checksum: 31464fade10aeea055a352aa873c9729
        .file   "enhance.c"
        .text
        .align  2
        .global ShouldUsePostModify
        .type   ShouldUsePostModify, %function
ShouldUsePostModify:
        @ Function supports interworking.
        @ args = 0, pretend = 0, frame = 0
        @ frame_needed = 0, uses_anonymous_args = 0
        @ link register save eliminated.
        ldr     ip, [r0, #0]
        mov     r3, r0
        orr     ip, ip, r1
        str     ip, [r3], #4
        ldr     r2, [r0, #4]
        orr     r2, r2, r1
        str     r2, [r0, #4]
        ldr     r0, [r3, #4]
        orr     r0, r0, r1
        str     r0, [r3, #4]
        add     r3, r3, #4
        ldr     r2, [r3, #4]
        orr     r2, r2, r1
        str     r2, [r3, #4]
        add     r3, r3, #4
        ldr     r2, [r3, #4]
        orr     r2, r2, r1
        str     r2, [r3, #4]
        add     r3, r3, #4
        ldr     r2, [r3, #4]
        orr     r2, r2, r1
        str     r2, [r3, #4]
        add     r3, r3, #4
        ldr     r2, [r3, #4]
        orr     r2, r2, r1
        str     r2, [r3, #4]
        add     r3, r3, #4
        ldr     r2, [r3, #4]
        orr     r2, r2, r1
        str     r2, [r3, #4]
        add     r3, r3, #4
        ldr     r2, [r3, #4]
        orr     r2, r2, r1
        str     r2, [r3, #4]
        add     r3, r3, #4
        ldr     r2, [r3, #4]
        orr     r2, r2, r1
        @ lr needed for prologue
        str     r2, [r3, #4]
        bx      lr
        .size   ShouldUsePostModify, .-ShouldUsePostModify
        .ident  "GCC: (GNU) 4.2.0 20070315 (prerelease)"

However this problem vanishes when I use -fno-tree-lrs, this is becuase, then each copy of intArray created by the unroller gets combined and the load/ store can be combined with the increment of intArray. However, I dont think that this ( the use of -fno-tree-lrs) is the way to go.


---


### compiler : `gcc`
### title : `pseudo-optimization with sincos/cexpi`
### open_at : `2007-03-17T21:11:36Z`
### last_modified_date : `2022-03-08T16:20:49Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=31249
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.3.0`
### severity : `minor`
### contents :
With gfortran and g++ the computation of cos(x) and sin(x) is "optimized" by taking
the real and imaginary parts of cexpi(x) (at least it is what I understand). This is working
if and only if the computation of cexpi(x) is faster than the sum of the separate computations 
of cos(x) and sin(x). 

Now consider the following code:

integer, parameter :: n=1000000
integer :: i
real(8) :: pi, ss, sc, t, dt
pi = acos(-1.0d0)
dt=pi/n
sc=0
ss=0
t=0
do i= 1, 100*n
  sc = sc + cos(t-dt)
  ss = ss + sin(t)
  t = t+dt
end do
print *, sc, ss
end

the result is (G5 1.8Ghz, OSX 10.3.9):

[karma] bug/timing% gfc -O3 sincos.f90 
[karma] bug/timing% time a.out 
 -6.324121638644320E-002 -2.934958087315009E-003
13.020u 0.050s 0:13.59 96.1%    0+0k 0+2io 0pf+0w

It is easy to see that I have fooled the optimizer with the line

  sc = sc + cos(t-dt)

If I replace it by:

  sc = sc + cos(t)

the result is now (over a 50% increase of the CPU time):

[karma] bug/timing% gfc -O3 sincos_o.f90
[karma] bug/timing% time a.out
 -6.324121573032526E-002 -2.934958087315009E-003
21.740u 0.080s 0:22.18 98.3%    0+0k 0+2io 0pf+0w

to be compared with the result of the code:

integer, parameter :: n=1000000
integer :: i
real(8) :: pi, ss, sc, t, dt
complex(8) :: z, dz
pi = acos(-1.0d0)
dt=pi/n
dz=cmplx(0.0d0,dt,8)
sc=0
ss=0
z=0
do i= 1, 100*n
  sc = sc + real(exp(z))
  ss = ss + aimag(exp(z))
  z = z+dz
end do
print *, sc, ss
end

is

[karma] bug/timing% gfc -O3 cexp.f90
[karma] bug/timing% time a.out
 -6.324121573032526E-002 -2.934958087315009E-003
20.850u 0.110s 0:21.45 97.7%    0+0k 0+2io 0pf+0w

Following the comments in PR #30969, 30980, and 31161, I have understood that
on OSX cexpi "fallback" to cexp in perfect agreement with the above timings.

So it would probably nice to disable the sincos "optimisation" on platforms that
do not support fast cexpi such as OSX (as presently configured).

Note that on Sat, 30 Sep 2006 in

http://gcc.gnu.org/ml/fortran/2006-09/msg00454.html

I have reported (in vain) a timing regression for the fatigue.f90 polyhedron test case.
Is this related to this pseudo-optimization or to another change?


---


### compiler : `gcc`
### title : `addressing modes are not selected correcly for x86 always`
### open_at : `2007-03-19T13:52:03Z`
### last_modified_date : `2021-12-25T21:27:29Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=31263
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.1.2`
### severity : `enhancement`
### contents :
I'm not sure, if this can be called a bug, but it is at least a really bad case of poor optimization.

The following program calls the function 'Square' several times, either with x=1000 or x=i*2-i-i+1000 (which is also 1000). The second version is executed much FASTER. I see no reason, why this should be so. I tested it with gcc 4.1.1 and 4.1.2. The timings are more or less equal.

> gcc -O2 f_demo.c f_demo2.c -o f_demo
> time f_demo

real    0m1.537s
user    0m1.183s
sys     0m0.345s

> gcc -D VARIABLE_PAR -O2 f_demo.c f_demo2.c -o f_demo
> time f_demo

real    0m0.700s
user    0m0.368s
sys     0m0.329s

--- f_demo.c -----------------------------------------------------------
#include <stdlib.h>

double Square(double x);

#ifdef VARIABLE_PAR
#define PAR i*2-i-i+1000
#else
#define PAR 1000
#endif

int main()
{
  const int iSize=50000000;
  int i;
  double *pdA=malloc(iSize*sizeof(double));
  for(i=0;i<iSize;i++) {
    pdA[i]=Square(PAR);
  }
}

--- f_demo2.c ----------------------------------------------------
double Square(double x)
{
  return x*x;
}


---


### compiler : `gcc`
### title : `Missing simple optimization`
### open_at : `2007-03-19T22:22:47Z`
### last_modified_date : `2023-05-20T02:48:38Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=31271
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.3.0`
### severity : `enhancement`
### contents :
The following shows a missing easy optimization for GCC:

int
in_canforward(unsigned int in)
{
        if ((in & ~0xffffff0f) == 0xf0 || (in & ~0xffffff0f) == 0xe0)
                return 0;
        return 1;
}

results in (@ -O2):

in_canforward:
        andl    $240, %edi
        cmpl    $240, %edi
        sete    %al
        cmpl    $224, %edi
        sete    %dl
        orl     %edx, %eax
        xorl    $1, %eax
        movzbl  %al, %eax
        ret

given that 0xf0 and 0xe0 only differ by one bit, there is no reason to test for that bit so the comparision could be: (in & 0xffffff1f) == 0xe0.  More generally
the optimization is:

given           (x & m) == a0 || (x & m) == a1
where m, a0, and a1 are all constant
let             b = (a0 ^ a1)
then if         (b & (b - 1)) == 0 [b is a power of 2]
rewrite to:     (x & (m|b)) == (a0 & ~b)


---


### compiler : `gcc`
### title : `gcc is being too clever`
### open_at : `2007-03-19T22:42:30Z`
### last_modified_date : `2021-09-11T23:40:32Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=31272
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.3.0`
### severity : `enhancement`
### contents :
[This problem occurs in 4.1.2 and 4.1.3 as well]
Given the following source:

int
in_canforward(unsigned int in)
{
        unsigned int net;
 
        if ((in & ~0xffffff0f) == 0xf0 || (in & ~0xffffff0f) == 0xe0)
                return 0;
        if ((in & 0x80) == 0) {
                net = in & 0xff;
                if (net == 0 || net == 0x7f)
                        return 0;
        }
        return 1;

"cc1 -O2 -quiet" emit:  

#NO_APP
        .file   "inc.c"
        .text
        .align 1
.globl in_canforward
        .type   in_canforward, @function
in_canforward:
        .word 0x0
        subl2 $4,%sp
        movl 4(%ap),%r1
        bicl3 $-241,%r1,%r0
        cmpl %r0,$240
        jeql .L2
        cmpl %r0,$224
        jeql .L2
        bicb3 $127,%r1,%r0
        jneq .L12
        bicl2 $-256,%r1
        jneq .L13
.L2:
        clrl %r0
        ret
.L12:
        movl $1,%r0
        ret
.L13:
        cmpl %r1,$127
        jeql .L14
        xorb2 $1,%r0
        movzbl %r0,%r0
        ret
.L14:
        movb $1,%r0
        xorb2 $1,%r0
        movzbl %r0,%r0
        ret
        .size   in_canforward, .-in_canforward
        .ident  "GCC: (GNU) 4.3.0 20070319 (experimental)"

Notice the code at .L14?  Why go through all extra that effort?  Why not just do clrl %r0 and ret or preferrably branch to .L2 which already does that?  The same argument goes for the xorb2/movzbl right  before .L14.   movl $1,%r0 and ret or preferably branch to .L12 which already does that.

Now if you move .L13 before .L12 (so it can all fall through) and take the mentioned branches, the almost-optimal version becomes:

in_canforward:
        .word 0x0
        subl2 $4,%sp
        movl 4(%ap),%r1
        bicl3 $-241,%r1,%r0
        cmpl %r0,$240
        jeql .L2
        cmpl %r0,$224
        jeql .L2
        bicb3 $127,%r1,%r0
        jneq .L12
        bicl2 $-256,%r1
        jneq .L13
.L2:
        clrl %r0
        ret
.L13:
        cmpl %r1,$127
        jeql .L2
.L12:
        movl $1,%r0
        ret


---


### compiler : `gcc`
### title : `consecutive strcmps are not merged`
### open_at : `2007-03-22T15:12:26Z`
### last_modified_date : `2021-07-26T02:58:12Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=31313
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.3.0`
### severity : `enhancement`
### contents :
I just ran into some code which did something like

int strcmp(const char *, const char *);

int f (const char *c)
{
  return (strcmp (c, "aaa") == 0 || strcmp (c, "aab") == 0);
}

It would be possible to optimize this into something like (hopefully I get it right)
int f (const char *c)
{
  if (strncmp (c, "aa", 2))
    return 0;
  return ((c[2] == 'a' || c[2] == 'b') && !c[3]);
}

Instead, we scan through the whole string twice, as can be seen in the assembly.

Likewise, more complicated combinations of comparisons could be reduced into an optimal matching sequence.  Putting this into component rtl-optimization, because the strcmp calls survive all of the tree optimizers unchanged.


---


### compiler : `gcc`
### title : `C complex numbers, amd64 SSE, missed optimization opportunity`
### open_at : `2007-04-05T12:29:39Z`
### last_modified_date : `2023-10-01T18:45:28Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=31485
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.1.2`
### severity : `enhancement`
### contents :
Considering that "complex" turns basically any basic type into a vector type, complex number addition and subtraction could utilize SSE instructions to perform the operation on real and imaginary parts simultaneously. (Only applies to addition and subtraction.)

Code:

#include <complex.h>

typedef float complex ss1;
typedef float ss2 __attribute__((vector_size(sizeof(ss1))));

ss1 add1(ss1 a, ss1 b) { return a + b; }
ss2 add2(ss2 a, ss2 b) { return a + b; }

Produces:

add1:
        movq    %xmm0, -8(%rsp)
        movq    %xmm1, -16(%rsp)
        movss   -4(%rsp), %xmm0
        movss   -8(%rsp), %xmm1
        addss   -12(%rsp), %xmm0
        addss   -16(%rsp), %xmm1
        movss   %xmm0, -20(%rsp)
        movss   %xmm1, -24(%rsp)
        movq    -24(%rsp), %xmm0
        ret
add2:
        movlps  %xmm0, -16(%rsp)
        movlps  %xmm1, -24(%rsp)
        movaps  -24(%rsp), %xmm0
        addps   -16(%rsp), %xmm0
        movaps  %xmm0, -56(%rsp)
        movlps  -56(%rsp), %xmm0
        ret

Command line:
    gcc -msse  -O3 -S test2.c
    (Results are same with -ffast-math)
Architecture:
CPU=AMD Athlon(tm) 64 X2 Dual Core Processor 4600+
CPU features=fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ht syscall nx mmxext fxsr_opt lm 3dnowext 3dnow pni lahf_lm cmp_legacy

GCC is:
Target: x86_64-linux-gnu
Configured with: ../src/configure -v --enable-languages=c,c++,fortran,objc,obj-c++,treelang --prefix=/usr --enable-shared --with-system-zlib --libexecdir=/usr/lib --without-included-gettext --enable-threads=posix --enable-nls --program-suffix=-4.1 --enable-__cxa_atexit --enable-clocale=gnu --enable-libstdcxx-debug --enable-mpfr --enable-checking=release x86_64-linux-gnu
Thread model: posix
gcc version 4.1.2 20061115 (prerelease) (Debian 4.1.1-21)


---


### compiler : `gcc`
### title : `A microoptimization of isnegative of signed integer`
### open_at : `2007-04-10T19:05:26Z`
### last_modified_date : `2023-10-16T17:03:21Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=31531
### status : `RESOLVED`
### tags : `missed-optimization, patch, TREE`
### component : `middle-end`
### version : `4.1.3`
### severity : `enhancement`
### contents :
/* Given X an unsigned of 32 bits, and Y a bool. Try to translate optimizing
*
* Y = X >  2147483647;   to   Y = ((signed)X) < 0;
* Y = X >= 2147483648;   to   Y = ((signed)X) < 0;
*
* [ Another optimization is to Y = (X >> 31) ]
*
* The opposite (ELSE):
*
* Y = X <= 2147483647;   to   Y = ((signed)X) >= 0;
* Y = X <  2147483648;   to   Y = ((signed)X) >= 0;
*
* [ Another optimization is to Y = ((~X) >> 31) ]
*
* 2147483647=0x7FFFFFFF   2147483648=0x80000000
*
* The unsigned comparison is become to signed comparison.
*
* by J.C. Pizarro */

# gcc version 4.1.3 20070326 (prerelease)
Full test of isnegative is PASSED.

notl    %eax
shrl    $31, %eax
xorl    $1, %eax

IS WORSE THAN

shrl $31, %eax

---------------------

xorl    %eax, %eax
cmpl    $0, 4(%esp)
sets    %al

IS WORSE THAN

movl    4(%esp), %eax
shrl    $31, %eax

------------------------------------------------------------------------------

Full info with src code and tarball is in
http://gcc.gnu.org/ml/gcc/2007-04/msg00317.html

I'm sorry, i did want to say 2 billions, not 2 millions.

J.C. Pizarro


---


### compiler : `gcc`
### title : `__builtin_cabsf(z) squared should be optimized`
### open_at : `2007-04-12T15:27:07Z`
### last_modified_date : `2021-07-26T02:57:24Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=31548
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.3.0`
### severity : `enhancement`
### contents :
The following Fortran program

program test
 complex :: z
 real :: r
 r = abs(z)**2
 print *, r
end program test

produces the following tree:
    D.1352 = __builtin_cabsf (z);
    D.1353 = D.1352 * D.1352;
    r = D.1353;

The complex value is naively calculated as:
  sqrt( (_Real_ z)*(_Real_ z) + (_Imag_ z)*(_Imag_ z) )

However, since the value is squared afterwards, the square root can be simply removed.

Calculating |...|^2 is not that uncommon in some codes.


---


### compiler : `gcc`
### title : `return 0x80000000UL code gen can be improved`
### open_at : `2007-04-12T22:10:29Z`
### last_modified_date : `2022-03-08T16:20:41Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=31557
### status : `REOPENED`
### tags : `missed-optimization`
### component : `target`
### version : `4.3.0`
### severity : `enhancement`
### contents :
Testcase:
unsigned int f(void)
{
  return 0x80000001UL;
}

This should be able to done in three instructions:
.f:
        li 3,1
        oris 3,3,0x8000
        blr

Right now it is done as:
.L.f:
        li 3,0
        ori 3,3,32768
        sldi 3,3,16
        ori 3,3,1
        blr
Which is (0x8000 << 16) | 1 but (0x8000 << 16) is what is done for oris.


---


### compiler : `gcc`
### title : `Folding of  A & (1 << B) pessimizes FRE`
### open_at : `2007-04-19T10:56:48Z`
### last_modified_date : `2023-05-20T02:29:12Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=31631
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.3.0`
### severity : `enhancement`
### contents :
void
foo (int control2, unsigned long *state, int size)
{
  int i;

  for(i=0; i<size; i++)
    {
       if (state[i] & ((unsigned long) 1 << control2))
         state[i] ^= ((unsigned long) 1 << control2);
    }
}

FRE does not recognize the ((unsigned long) 1 << control2) redundancy
because it looks like

<L0>:;
  D.1989_4 = (long unsigned int) i_1;
  D.1990_5 = D.1989_4 * 8;
  D.1991_6 = (long unsigned int *) D.1990_5;
  D.1992_8 = D.1991_6 + state_7(D);
  # VUSE <SMT.4_28>
  D.1993_9 = *D.1992_8;
  D.1994_11 = D.1993_9 >> control2_10(D);
  D.1995_12 = (int) D.1994_11;
  D.1996_13 = D.1995_12 & 1;
  if (D.1996_13 != 0) goto <L1>; else goto <L2>;
  
<L1>:;
  D.1989_19 = D.1989_4;
  D.1990_20 = D.1990_5;
  D.1991_21 = D.1991_6;
  D.1992_22 = D.1992_8;
  D.1993_23 = D.1993_9;
  D.1998_24 = 1 << control2_10(D);
  D.1999_25 = D.1993_23 ^ D.1998_24;
  # SMT.4_30 = VDEF <SMT.4_28>
  *D.1992_22 = D.1999_25;

This is related to PR29789 where this transformation causes other
pessimization.


---


### compiler : `gcc`
### title : `mmintrin calls are slower than plain C`
### open_at : `2007-04-23T03:00:48Z`
### last_modified_date : `2021-08-11T07:36:21Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=31661
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `target`
### version : `4.1.0`
### severity : `enhancement`
### contents :
hi,

this thread:
 http://gcc.gnu.org/ml/gcc-help/2007-04/msg00201.html
details my problems.  (duplicated here)

i want to sum an array of longs using mmx.  i use the functions:
   _mm_set_pi32 and _m_paddd
but the resultant binary contains significantly less efficient code
than inline asm or even plain C ( for(i=0;i<n;i++)total+=a[i]; ).
here's the relevant function:

simd_mmintrin(n, is)
I *is;
{   __m64 q,r;
  I i;
  _m_empty();
  q=_m_from_int(0);
  for (i=0; i < n; i+=W) {
      r=_mm_set_pi32(is[i],is[i+1]);
      q=_m_paddd(q,r);
  }
  union {long a[2];__m64 m;}u;
  u.m=q;
  return u.a[0]+u.a[1];
}

i have a script RUNME.sh:

$ sh RUNME.sh
---
expect: 199990000
impl: C (SISD)
199990000


real    0m0.604s
user    0m0.580s
sys     0m0.004s



---
expect: 199990000
impl: ASM (SIMD)
199990000



real    0m0.377s
user    0m0.360s
sys     0m0.008s



---
expect: 199990000
impl: MMINTRIN (SIMD)
199990000


real    0m1.235s
user    0m1.228s
sys     0m0.004s




$ cat RUNME.sh
#!/bin/sh
repeats=4000        # number of times to repeat the test
vectorsize=10000   # size of the vector in 32 bit ints
gcc -O -mmmx v.c -o v
for which in 0 1 2; do time ./v $repeats $vectorsize $which; done


$ cat v.c
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <mmintrin.h>


typedef long I;typedef unsigned long J;
typedef char C;
#define IZ sizeof(I)
#define W 2



simd_mmintrin(n, is)
I *is;
{   __v2si q,r;
  I i;
  _m_empty();
  q=_m_from_int(0);
  for (i=0; i < n; i+=W) {
      memcpy(&r,is+i,IZ*W);
      q=_m_paddd(q,r);
  }
  I*qq=(I*)&q;
  return qq[0]+qq[1];
}


simd_asm(n, is)
I *is;
{   I i,*r=malloc(IZ*W*8);
  asm("emms");
  asm("pxor %mm0,%mm0");
  for (i=0; i < n; i+=W) {
      asm("movq %0,%%mm1\n\t"
          "paddd %%mm1,%%mm0"
          :
          :"m"(is[i])           );
  }
  asm("movq %%mm0,%0":"=m"(*(__m64*)r));
  return r[0]+r[1];
}


sisd(n, is)
I *is;
{
  I i = 0, j = 0;
  for (i = 0; i < n; i++)
      j += is[i];
  return j;
}


main(c, v)
C **v;
{
  I n=atol(v[1]), z=atol(v[2]), m=atol(v[3]);
  I result, *is=malloc(IZ*(z*=2)), i;
  int(*fs[])()={sisd,simd_asm,simd_mmintrin,0};
  C*ss[]={"C (SISD)","ASM (SIMD)","MMINTRIN (SIMD)"};
  for(i=0;i<z;i++)is[i]=i;
  printf("\n\n---\nexpect: %d\n",(z)*(z-1)/2);
  printf("impl: %s\n",ss[m]);
  while (n--)
      result=fs[m](z, is);
  printf("%d\n",result);
}



[jack@fedora i]$ gcc -v
Using built-in specs.
Target: i386-redhat-linux
Configured with: ../configure --prefix=/usr --mandir=/usr/share/man --infodir=/u
sr/share/info --enable-shared --enable-threads=posix --enable-checking=release -
-with-system-zlib --enable-__cxa_atexit --disable-libunwind-exceptions --enable-
libgcj-multifile --enable-languages=c,c++,objc,obj-c++,java,fortran,ada --enable
-java-awt=gtk --disable-dssi --with-java-home=/usr/lib/jvm/java-1.4.2-gcj-1.4.2.
0/jre --with-cpu=generic --host=i386-redhat-linux
Thread model: posix
gcc version 4.1.0 20060304 (Red Hat 4.1.0-3)


---


### compiler : `gcc`
### title : `Integer extensions vectorization could be improved`
### open_at : `2007-04-23T15:27:25Z`
### last_modified_date : `2021-08-21T21:44:10Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=31667
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.3.0`
### severity : `enhancement`
### contents :
SSE4.1 has pmovzx and pmovsx. For code like:

[hjl@gnu-2 vect]$ cat pmovzxbw.c
typedef unsigned char vec_t;
typedef unsigned short vecx_t;

extern __attribute__((aligned(16))) vec_t x [64];
extern __attribute__((aligned(16))) vecx_t y [64];

void
foo ()
{
  int i;

  for (i = 0; i < 64; i++)
    y [i]  = x [i];
}

Icc generates

        pmovzxbw  x(%rip), %xmm0                                #13.14
        pmovzxbw  8+x(%rip), %xmm1                              #13.14
        pmovzxbw  16+x(%rip), %xmm2                             #13.14
        pmovzxbw  24+x(%rip), %xmm3                             #13.14
        pmovzxbw  32+x(%rip), %xmm4                             #13.14
        pmovzxbw  40+x(%rip), %xmm5                             #13.14
        pmovzxbw  48+x(%rip), %xmm6                             #13.14
        pmovzxbw  56+x(%rip), %xmm7                             #13.14
        movdqa    %xmm0, y(%rip)                                #13.5
        movdqa    %xmm1, 16+y(%rip)                             #13.5
        movdqa    %xmm2, 32+y(%rip)                             #13.5
        movdqa    %xmm3, 48+y(%rip)                             #13.5
        movdqa    %xmm4, 64+y(%rip)                             #13.5
        movdqa    %xmm5, 80+y(%rip)                             #13.5
        movdqa    %xmm6, 96+y(%rip)                             #13.5
        movdqa    %xmm7, 112+y(%rip)                            #13.5
        ret                                                     #14.1


---


### compiler : `gcc`
### title : `__builtin_ctzll slower than 2*__builtin_ctz`
### open_at : `2007-04-25T09:16:58Z`
### last_modified_date : `2023-06-13T05:44:26Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=31695
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.1.1`
### severity : `enhancement`
### contents :
int func1( unsigned long long val )
{
  return __builtin_ctzll( val );
}

int func2( unsigned long long val )
{
  unsigned lo = (unsigned)val;
  return lo ? __builtin_ctz(lo) : __builtin_ctz(unsigned(val>>32)) + 32;
}

func1 is more than 2 times slower than func2.  
But it should be at least as fast as func2

__builtin_ctzll is not expanded inline like __builtin_ctz.


---


### compiler : `gcc`
### title : `Use reciprocal and reciprocal square root with -ffast-math`
### open_at : `2007-04-27T09:07:24Z`
### last_modified_date : `2019-10-10T05:01:14Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=31723
### status : `RESOLVED`
### tags : `missed-optimization, patch`
### component : `middle-end`
### version : `4.3.0`
### severity : `enhancement`
### contents :
I did some analysis of why gfortran does badly at the gas_dyn benchmark of the Polyhedron benchmark suite. See my analysis at

http://gcc.gnu.org/ml/fortran/2007-04/msg00494.html

In short, GCC should use reciprocal and reciprocal square root instructions (available in single precision for SSE and Altivec) when possible. These instructions are very fast, a few cycles vs. dozens or hundreds of cycles for normal division and square root instructions. However, as these instructions are accurate only to 12 bits, they should be enabled only with -ffast-math (or some separate option that gets included with -ffast-math).

The following C program demonstrates the issue, for all the functions it should be possible to use reciprocal and/or reciprocal square root instructions instead of normal div and sqrt:

#include <math.h>

float recip1 (float a)
{
  return 1.0f/a;
}

float recip2 (float a, float b)
{
  return a/b;
}

float rsqrt1 (float a)
{
  return 1.0f/sqrtf(a);
}

float rsqrt2 (float a, float b)
{
  /* Mathematically equivalent to 1/sqrt(b*(1/a))  */
  return sqrtf(a/b);
}

asm output (compiled with -std=c99 -O3 -c -Wall -pedantic -march=k8 -mfpmath=sse -ffast-math -S):

        .file   "recip.c"
        .text
        .p2align 4,,15
.globl recip1
        .type   recip1, @function
recip1:
        pushl   %ebp
        movl    %esp, %ebp
        subl    $4, %esp
        movss   .LC0, %xmm0
        divss   8(%ebp), %xmm0
        movss   %xmm0, -4(%ebp)
        flds    -4(%ebp)
        leave
        ret
        .size   recip1, .-recip1
        .p2align 4,,15
.globl recip2
        .type   recip2, @function
recip2:
        pushl   %ebp
        movl    %esp, %ebp
        movss   8(%ebp), %xmm0
        divss   12(%ebp), %xmm0
        movss   %xmm0, 8(%ebp)
        flds    8(%ebp)
        leave
        ret
        .size   recip2, .-recip2
        .p2align 4,,15
.globl rsqrt2
        .type   rsqrt2, @function
rsqrt2:
        pushl   %ebp
        movl    %esp, %ebp
        subl    $4, %esp
        movss   8(%ebp), %xmm0
        divss   12(%ebp), %xmm0
        sqrtss  %xmm0, %xmm0
        movss   %xmm0, -4(%ebp)
        flds    -4(%ebp)
        leave
        ret
        .size   rsqrt2, .-rsqrt2
        .p2align 4,,15
.globl rsqrt1
        .type   rsqrt1, @function
rsqrt1:
        pushl   %ebp
        movl    %esp, %ebp
        subl    $4, %esp
        movss   .LC0, %xmm0
        sqrtss  8(%ebp), %xmm1
        divss   %xmm1, %xmm0
        movss   %xmm0, -4(%ebp)
        flds    -4(%ebp)
        leave
        ret
        .size   rsqrt1, .-rsqrt1
        .section        .rodata.cst4,"aM",@progbits,4
        .align 4
.LC0:
        .long   1065353216
        .ident  "GCC: (GNU) 4.3.0 20070426 (experimental)"
        .section        .note.GNU-stack,"",@progbits


As can be seen, it uses divss and sqrtss instead of rcpss and rsqrtss. Of course, there are vectorized versions of these functions too, rcpps and rsqrtps, that should be used when appropriate (vectorization is important e.g. for gas_dyn).


---


### compiler : `gcc`
### title : `Fortran dot product vectorization is restricted`
### open_at : `2007-04-28T20:29:39Z`
### last_modified_date : `2021-08-16T04:39:51Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=31738
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.3.0`
### severity : `normal`
### contents :
It seems that dot products are vectorized only for very restricted cases. For the following example

subroutine testvectdp (a, b, c, n)
  integer, intent(in) :: n
  real, intent(in) :: a(n), b(n)
  real, intent(out) :: c
  c = dot_product (a, b)
end subroutine testvectdp

subroutine testvectdp2 (a, b, c, n)
  integer, intent(in) :: n
  real, intent(in) :: a(n), b(n)
  real, intent(out) :: c
  integer :: i
  c = 0.0
  do i = 1, n
     c = c + a(i) * b(i)
  end do
end subroutine testvectdp2

module testvec
contains
  subroutine testvecm (a, b, c)
    real, intent(in) :: a(:), b(:)
    real, intent(out) :: c
    c = dot_product (a, b)
  end subroutine testvecm
  
  subroutine testvecm2 (a, b, c)
    real, intent(in) :: a(:), b(:)
    real, intent(out) :: c
    integer :: i
    c = 0.0
    do i = 1, size (a)
       c = c + a(i) * b(i)
    end do
  end subroutine testvecm2
end module testvec

program testvec_p
  use testvec
  implicit none
  real :: a(9), b(9), c
  external testvectdp, testvectdp2

  call random_number(a)
  call random_number(b)

  call testvectdp(a,b,c,9)
  print *, c
  call testvectdp2(a,b,c,9)
  print *, c
  call testvecm(a,b,c)
  print *, c
  call testvecm2(a,b,c)
  print *, c
end program testvec_p
  
Only the first one, testvectdp vectorizes.


---


### compiler : `gcc`
### title : `-floop-interchange is not working on some fortran loops`
### open_at : `2007-04-29T14:56:06Z`
### last_modified_date : `2023-01-10T18:22:59Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=31756
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.2.0`
### severity : `enhancement`
### contents :
Given the following Fortran source:

      SUBROUTINE SUB(A, B, N, M)
      DIMENSION A(N, M), B(N, M)
      DO I = 1, N
         DO J = 1, M
            A(I, J) = B(I, J)
         ENDDO
      ENDDO
      END

It should be vectorized using the following compile time options:

-O2 -ftree-vectorize -ftree-vectorizer-verbose=2 -ftree-loop-linear 

Unfortunately, it doesn't.


---


### compiler : `gcc`
### title : `SSE2 performance is deteriorating when __m128 is placed in union`
### open_at : `2007-05-03T19:27:37Z`
### last_modified_date : `2021-08-05T21:00:32Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=31802
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.1.2`
### severity : `enhancement`
### contents :
When I compile the following testcase with '-O3 -msse3' options it runs in 
22.562sec, without 'union' clause it runs in 0.280sec. And should be the same time.

-- begin testcase --
typedef float __v2df __attribute__ ((__vector_size__ (16)));
typedef __v2df __m128;

static __inline __m128 _mm_sub_pd (__m128 __A, __m128 __B) { return
(__m128)__builtin_ia32_subps ((__v2df)__A, (__v2df)__B); }
static __inline __m128 _mm_add_pd (__m128 __A, __m128 __B) { return
(__m128)__builtin_ia32_addps ((__v2df)__A, (__v2df)__B); }
static __inline __m128 _mm_setr_ps (float __Z, float __Y, float __X, float __W)
{ return __extension__ (__m128)(__v2df){ __Z, __Y, __X, __W }; }

struct FF {
  union {__m128 d; float f[4];}; // problem
  // __m128 d; // no problem

  __inline FF() { }
  __inline FF(__m128 new_d) : d(new_d) { }
  __inline FF(float f) : d(_mm_setr_ps(f, f, f, f)) { }

  __inline FF operator+(FF other) { return (FF(_mm_add_pd(d,other.d))); }
  __inline FF operator-(FF other) { return (FF(_mm_sub_pd(d,other.d))); }
};

float f[1024*1024];

int main() {
  int i;

  for (i = 0; i < 1024*1024; i++) { f[i] = 1.f/(1024*1024 + 10 - i); }

  FF total(0.f);

  for (int rpt = 0; rpt < 1000; rpt++) {
  FF p1(0.f), p2(0.), c;

  __m128 *pf = (__m128*)f;
  for (i = 0; i < 1024*1024/4; i++) {
    FF c(*pf++);

    total = total + c - p2 + p1;

    p1 = p2;
    p2 = c;
  }
  }
}
-- end testcase

This bug has similar testcase as 25500 (that's fixed now). Only 'union' clause was added.

Yuri


---


### compiler : `gcc`
### title : `Loop IM and other optimizations harmful for -fopenmp`
### open_at : `2007-05-08T08:59:00Z`
### last_modified_date : `2021-07-20T22:47:26Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=31862
### status : `NEW`
### tags : `missed-optimization, openmp, wrong-code`
### component : `tree-optimization`
### version : `4.2.0`
### severity : `normal`
### contents :
See http://openmp.org/pipermail/omp/2007/000840.html
and the rest of the lengthy threads:
Memory consistency contradiction between 2.5 specification and GCC
OpenMP spec 2.5 seems to have incorrect flush example on page 12
Two simpler examples (Re: OpenMP spec 2.5 seems to have incorrect flush example on page 12)

Some GCC optimizations are harmful for threaded code, e.g. loop invariant motion
of global variables:

int var;
void
foo (int x)
{
  int i;
  for (i = 0; i < 100; i++)
    {
      if (i > x)
        var = i;
    }
}

When some other thread modifies var at the same time while foo (200) is executed,
the compiler inserted a race which doesn't really exist in the original program,
as it will do reg = var; ... var = reg; even when var was never modified.

Even if we prove a variable is always written to within a loop, but there is some kind of barrier (a function call which might contain a barrier, __sync_synchronize (), #pragma omp barrier, #pragma omp flush (does a volatile var read resp. write count as one too?)), if the variable is not written to
after the barrier, the compiler is still introducing a race which didn't exist originally.

I wonder if we shouldn't disable some optimizations (like loop IM if the var is a global variable) for -fopenmp (or perhaps add also a -fthread-safe option
implied by -fopenmp).  Does if conversion cause similar problems?  What else?


---


### compiler : `gcc`
### title : `missed optimization: we don't move "invariant casts" out of loops`
### open_at : `2007-05-09T07:13:08Z`
### last_modified_date : `2021-09-20T03:00:23Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=31873
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.3.0`
### severity : `normal`
### contents :
This PR was originally opened against PRE (PR25809), but turns out PRE can't solve this problem, so here's a new PR instead:

In testcases that have reduction, like gcc.dg/vect/vect-reduc-2char.c and
gcc.dg/vect-reduc-2short.c, the following casts appear:

        signed char sdiff;
        unsigned char ux, udiff; 
        sdiff_0 = ...
        loop:
           # sdiff_41 = PHI <sdiff_39, sdiff_0>;
           .....
           ux_36 = ....
           udiff_37 = (unsigned char) sdiff_41;  
           udiff_38 = x_36 + udiff_37;
           sdiff_39 = (signed char) udiff_38;
        end_loop

although these casts could be taken out of loop all together. i.e., transform
the code into something like the following:

        signed char sdiff;
        unsigned char ux, udiff;
        sdiff_0 = ...
        udiff_1 = (unsigned char) sdiff_0;
        loop:
           # udiff_3 = PHI <udiff_2, udiff_1>;
           .....
           ux_36 = ....
           udiff_2 = ux_36 + udiff_3;
        end_loop
        sdiff_39 = (signed char) udiff_2;

see this discussion thread:
http://gcc.gnu.org/ml/gcc-patches/2005-12/msg01827.html


---


### compiler : `gcc`
### title : `compiler misses opportunity to combine multiple identical function return paths`
### open_at : `2007-05-10T06:03:47Z`
### last_modified_date : `2023-09-03T03:44:16Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=31889
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `unknown`
### severity : `normal`
### contents :
The source file I'm submitting has two implementations of an inline function, and a second function which calls it and then prints one of two strings depending on the return value.  With the simpler implementation of the inline function, one call to puts() is followed by a jump to the return sequence emitted after the other puts() call.  With the more complicated (but functionally equivalent) implementation of the inline function, the caller's two paths aren't combined; two sets of instructions are emitted to restore the same registers from the same stack slots before returning.  It should still be able to combine them.

(A second possible missed optimization?  The branch could've been done to the puts call, instead of to just after, saving one call instruction.  Unless a branch to a call is slower than a call that returns to a branch instruction on these processors.)


---


### compiler : `gcc`
### title : `optimization: Loop not optimized away because of static`
### open_at : `2007-05-10T10:08:00Z`
### last_modified_date : `2020-08-31T09:25:32Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=31892
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.3.0`
### severity : `normal`
### contents :
Expected: The following loop is optimized way using gfortran -O3.
------------
      program prova
      implicit none
      integer :: i, j, Nx, Ny
      parameter(Nx=10000,Ny=10000)
      real(8) :: A(Nx,Ny)
      do j=1,Ny
        do i=1,Nx
          A(i,j)=sin(1.d0+i+j);
        end do
      end do
      end program
------------

In an equivalent C program the loop is optimized away and the run time drops from 10.927s to 0.001s: gcc -O3
------------
#include <math.h>
#define NX 10000
#define NY 10000
int main() {
  double A[NX][NY];
  int i, j;
  for(i = 0; i < NX; i++)
    for(j = 0; j < NY; j++)
      A[i][j] = sin(3.0+i+j);
  return 0;
}


---


### compiler : `gcc`
### title : `Please provide an "inout" attribute for function parameters.`
### open_at : `2007-05-10T11:00:44Z`
### last_modified_date : `2019-09-29T22:03:09Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=31893
### status : `RESOLVED`
### tags : `diagnostic, missed-optimization`
### component : `middle-end`
### version : `unknown`
### severity : `enhancement`
### contents :
Here is what I mean. When you write code like:

int foo(void) {
    static bar_t bar;

    call_some_function(&bar);
    return 0;
}

gcc assumes that call_some_function will initialize bar properly. Though, sometimes call_some_function is a function that will modify 'bar' but also need it to be properly initialized. In that case, the parameter is inout. (I must say I'm unsure what gcc thinks if call_some_function prototype is: void call_some_function(const bar_t *); maybe it suffers from the same problem).

That'd be great to have an __attribute__((inout(1,2,3...))) to say that the 1st, 2nd, 3rd, ... variables of the function need their argument to be initialized. That would make gcc issue warning about variables beeing used uninitialized properly.

Maybe "inout" is a very lousy name, and I don't care much about it. My point is, I'd really like to be able to express in the function prototypes that a structure needs to be initialized before that function can be called. WIth this attribute, the call_some_function prototype would be:

int call_some_function(bar_t *) __attribute__((inout(1)));


---


### compiler : `gcc`
### title : `Wide operations (i.e. adddi3) are split too late`
### open_at : `2007-05-18T14:19:16Z`
### last_modified_date : `2023-06-30T19:31:35Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=31985
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.3.0`
### severity : `enhancement`
### contents :
Following test generates unoptimized code for test_c(). Generated code should look like code, generated for test_asm():

--cut here--
typedef unsigned SI __attribute__ ((mode (SI)));
typedef unsigned DI __attribute__ ((mode (DI)));


#define add_ssaaaa_c(sh, sl, ah, al, bh, bl)	\
 {						\
   DI __a = (al) | ((DI) ah << 32);		\
   DI __b = (bl) | ((DI) bh << 32);		\
						\
   DI __c = __a + __b;				\
						\
   (sl) = (SI) (__c & 0xffffffff);		\
   (sh) = (SI) (__c >> 32);			\
 }


#define add_ssaaaa_asm(sh, sl, ah, al, bh, bl)	\
 __asm__ ("addl %5,%1\n\tadcl %3,%0"		\
	   : "=r" ((SI) (sh)),			\
	     "=&r" ((SI) (sl))			\
	   : "%0" ((SI) (ah)),			\
	     "g" ((SI) (bh)),			\
	     "%1" ((SI) (al)),			\
	     "g" ((SI) (bl)))


void test_c (SI a, SI b, SI c, SI d)
{
 volatile SI x, y;


 add_ssaaaa_c (x, y, a, b, c, d);
}


void test_asm (SI a, SI b, SI c, SI d)
{
 volatile SI x, y;


 add_ssaaaa_asm (x, y, a, b, c, d);
}
--cut here--

gcc -O2 -fomit-frame-pointer:

test_c:
       subl    $28, %esp       #,
       xorl    %edx, %edx      #
       movl    40(%esp), %eax  # c, tmp66
       movl    44(%esp), %ecx  # d, d
       movl    %esi, 20(%esp)  #,
       movl    %ebx, 16(%esp)  #,
       movl    %eax, %edx      # tmp66,
       movl    $0, %eax        #, tmp66
       movl    %eax, %esi      #, tmp74
       movl    32(%esp), %eax  # a, tmp70
       movl    %edx, %ebx      # tmp75, __c
       orl     %ecx, %esi      # d, tmp74
       xorl    %edx, %edx      #
       movl    %esi, %ecx      # tmp74, __c
       movl    36(%esp), %esi  # b, b
       movl    %edi, 24(%esp)  #,
       movl    24(%esp), %edi  #,
       movl    %eax, %edx      # tmp70,
       movl    $0, %eax        #, tmp70
       orl     %esi, %eax      # b, tmp72
       movl    20(%esp), %esi  #,
       addl    %eax, %ecx      # tmp72, __c
       adcl    %edx, %ebx      #, __c
       movl    %ecx, 8(%esp)   # __c, y
       movl    %ebx, %ecx      # __c, __c
       xorl    %ebx, %ebx      # __c
       movl    16(%esp), %ebx  #,
       movl    %ecx, 12(%esp)  # __c, x
       addl    $28, %esp       #,
       ret


test_asm:
       subl    $16, %esp       #,
       movl    20(%esp), %eax  # a, a
       movl    24(%esp), %edx  # b, b
#APP
       addl 32(%esp),%edx      # d, tmp63
       adcl 28(%esp),%eax      # c, tmp62
#NO_APP
       movl    %eax, 12(%esp)  # tmp62, x
       movl    %edx, 8(%esp)   # tmp63, y
       addl    $16, %esp       #,
       ret

This issue needs to be fixed in order to implement effective i386 (DImode) and x86_64 (TImode) wide operations in longlong.h. As discussed in thread starting at [1], it was found that the problem is, that wide operations are split after reload [2] due to FLAGS_REG link between "add" and "adc" insns. FLAGS_REG can be accidetally clobbered by reload.

[1] http://gcc.gnu.org/ml/gcc-patches/2007-05/msg01084.html
[2] http://gcc.gnu.org/ml/gcc-patches/2007-05/msg01187.html


---


### compiler : `gcc`
### title : `Loop unrolling does not exploit VRP for loop bound`
### open_at : `2007-05-24T18:45:24Z`
### last_modified_date : `2021-11-28T09:38:59Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=32073
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.2.0`
### severity : `enhancement`
### contents :
Loops with a bounded, small number of iterations unroll too much. They should be peeled away instead. For example, if I compile the following function with ``-O3 -funroll-loops'':

void short_loop(int* dest, int* src, int count) {
  // same happens for assert(count <= 4) and if(count > 4) exit(-1)
  if(count > 4)
    count = 4;

  for(int i=0; i < count; i++)
    dest[i] = src[i];
}

The assembly output (for i686-pc-cygwin) is an 8x duff's device, of which 75% of the code will never execute (translated back to C++ here for readability):

void short_loop(int* dest, int* src, int count) {
  // same happens for assert(count <= 4) and if(count > 4) exit(-1)
  if(count > 4)
    count = 4;

  int mod = count % 8;
  switch(mod) {
  case 7:
    // loop body
    count--;
  case 6:
    // loop body
    count--;
  case 5:
    // loop body
    count--;
  case 4:
    // loop body
    count--;
  case 3:
    // loop body
    count--;
  case 2:
    // loop body
    count--;
  case 1:
    // loop body
    count--;
  default:
    for(int i=0; i < count; i+=8)
      // 8x unrolled loop body
  }
}

We need <25% of that code:

void short_loop(int* dest, int* src, int count) {
  // same happens for assert(count <= 4) and if(count > 4) exit(-1)
  if(count > 4)
    count = 4;

  switch(count) {
  case 4:
    // loop body
  case 3:
    // loop body
  case 2:
    // loop body
  case 1:
    // loop body
  default:
    break;
  }
}


---


### compiler : `gcc`
### title : `bad codegen for vector initialization in Altivec`
### open_at : `2007-05-27T21:14:14Z`
### last_modified_date : `2022-03-08T16:20:53Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=32107
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.3.0`
### severity : `enhancement`
### contents :
Compiling the folloxing testcase:

#define vector __attribute__((__vector_size__(16) ))
float fa[100] __attribute__ ((__aligned__(16)));
vector float foo ()
{
  float f = fa[0];
  vector float vf = {f, f, f, f};
  return vf;
}

...with gcc -O2 -maltivec, we get:

ld      r9,0(r2)
lfs     f0,0(r9)
addi    r9,r1,-16
stfs    f0,-16(r1)
lvewx   v2,r0,r9
vspltw  v2,v2,0
blr

My problem is with the {lfs,stfs,lvewx} sequence: we load a value into f0, and then store it (with stfs) into an aligned memory location, so that it could be loaded from there into a vector (with lvewx). However, since the address from which f0 was loaded is known to be aligned, we could directly do an lvewx from there, and avoid the extra {lfs,stfs}, so the following should be enough:
	
ld      r9,0(r2)
lvewx   v2,r0,r9
vspltw  v2,v2,0
blr
  
The problem is that rs6000_expand_vector_init doesn't know that f0 is originated from an aligned address. It gets the following as vals:

(parallel:V4SF [
        (reg/v:SF 119 [ f ])
        (reg/v:SF 119 [ f ])
        (reg/v:SF 119 [ f ])
        (reg/v:SF 119 [ f ])
    ])

We somehow want to expand 'f = fa[0]' and '{f,f,f,f}' together... if expand_vector_init could get this as vals: '{fa[0],fa[0],fa[0],fa[0]}', it could see that the original address is aligned. 
Alternatively, the prospects of getting rid of the redundant load and store later on during some kind of a peephole optimization don't seem so high to me... Thoughts?

This may be related to PR31334 (though there the issue is about initialization with constants, so I'm not sure if the idea for a solution proposed there would help us here).


---


### compiler : `gcc`
### title : `Missed optimization caused by copy loop header (yes a weird case)`
### open_at : `2007-06-05T21:47:15Z`
### last_modified_date : `2023-06-10T01:16:05Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=32226
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.3.0`
### severity : `enhancement`
### contents :
Hi,
  I found this missed optimization when looking into an ICE on the pointer_plus branch.
For this code:
quantize_fs_dither (unsigned width, short *errorptr, int dir)
{
  short bpreverr;
  unsigned col;
  for (col = width; col > 0; col--) 
    errorptr += dir;
  errorptr[0] = (short) bpreverr;
}

We get with -O2 -fomit-frame-pointer:
quantize_fs_dither:
        pushl   %ebx
        movl    8(%esp), %ebx
        movl    12(%esp), %eax
        testl   %ebx, %ebx
        je      .L2
        movl    16(%esp), %ecx
        addl    %ecx, %ecx
        leal    (%eax,%ecx), %edx
        leal    -1(%ebx), %eax
        imull   %ecx, %eax
        leal    (%edx,%eax), %eax
.L2:
        movw    %ax, (%eax)
        popl    %ebx


With -Os we get:
        movl    12(%esp), %edx
        movl    8(%esp), %eax
        addl    %edx, %edx
        imull   4(%esp), %edx
        movw    %ax, (%eax,%edx)
        ret

Which has no branches and is faster as we will most likely mispredict the branch in the -O2 case.

This is related to PR 24574.


---


### compiler : `gcc`
### title : `[11/12/13/14 Regression] redundant && || not eliminated`
### open_at : `2007-06-12T14:45:16Z`
### last_modified_date : `2023-07-15T08:06:28Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=32306
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.3.0`
### severity : `normal`
### contents :
For the following Code Snippet
void bar ()
{

  b1 = foo(1);
  b2 = foo(1);
  b3 = foo(1);
  b4 = foo(1);
  b5 = foo(1);
  b6 = foo(1);
  b7 = foo(1);
  b8 = foo(1);
  b9 = foo(1);
  b10 = foo(1);
  b11 = foo(1);
  b12 = foo(1);

  array[0] = b1 && b2 && b3 && b4 && b5 && b6 && b7 && b8 && b9 && b10 && b11 && b12;
  array[1] = b1 && b2 && b3 && b4 && b5 && b6 && b7 && b8 && b9 && b10 && b11 && b12;
  array[2] = b1 && b2 && b3 && b4 && b5 && b6 && b7 && b8 && b9 && b10 && b11 && b12;
  array[3] = b1 && b2 && b3 && b4 && b5 && b6 && b7 && b8 && b9 && b10 && b11 && b12;
  array[4] = b1 && b2 && b3 && b4 && b5 && b6 && b7 && b8 && b9 && b10 && b11 && b12;
  array[5] = b1 && b2 && b3 && b4 && b5 && b6 && b7 && b8 && b9 && b10 && b11 && b12;
  array[6] = b1 && b2 && b3 && b4 && b5 && b6 && b7 && b8 && b9 && b10 && b11 && b12;
  array[7] = b1 && b2 && b3 && b4 && b5 && b6 && b7 && b8 && b9 && b10 && b11 && b12;
  array[8] = b1 && b2 && b3 && b4 && b5 && b6 && b7 && b8 && b9 && b10 && b11 && b12;
  array[9] = b1 && b2 && b3 && b4 && b5 && b6 && b7 && b8 && b9 && b10 && b11 && b12;
  array[10] = b1 && b2 && b3 && b4 && b5 && b6 && b7 && b8 && b9 && b10 && b11 && b12;

  return;
}

Where b ( from b1 to b12) are all declared static short b1, static short b2 etc.
and array is static short array[11].
This should generate code such as

if (b1 == 0) goto L1 else goto L2
L2:
if (b2 == 0) goto L1 else goto L3
L3:
if (b3 == 0) goto L1 else goto L4
L4:
if (b4 == 0) goto L1 else goto L5
L5:
if (b5 == 0) goto L1 else goto L6
L6:
if (b6 == 0) goto L1 else goto L7
L7:
if (b7 == 0) goto L1 else goto L8
L8:
if (b8 == 0) goto L1 else goto L9
L9:
if (b9 == 0) goto L1 else goto L10
L10:
if (b10 == 0) goto L1 else goto L11
L11:
if (b11 == 0) goto L1 else goto L12
L12:
if (b12 == 0) goto L1 else goto L13
L13:
array[i]=1 (for i from 0 to 10)
return

L1:
array[i]=0 (for i from 0 to 10)
return

This is exactly what 4.1 generates but 4.3 fails to combine the if sequences.
Version Details:
GNU C version 4.3.0 20070316 (experimental) (arm-none-eabi)
        compiled by GNU C version 3.4.6 (Ubuntu 3.4.6-1ubuntu2).
GGC heuristics: --param ggc-min-expand=30 --param ggc-min-heapsize=4096


---


### compiler : `gcc`
### title : `vectorized with alias check: can't determine dependence (array sections)`
### open_at : `2007-06-17T15:02:32Z`
### last_modified_date : `2019-09-26T04:31:41Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=32375
### status : `NEW`
### tags : `alias, missed-optimization`
### component : `tree-optimization`
### version : `4.3.0`
### severity : `enhancement`
### contents :
gfortran -O2  -ftree-vectorize -ftree-vectorizer-verbose=2 -c -v s414a.f

The source and destination sections of aa(:,:) do not overlap, unless there is a subscript over-run.  Even that case could be taken care of by loop reversal.

This is a simplification of a case from:
http://www.netlib.org/benchmark/vectors


---


### compiler : `gcc`
### title : `can't determine dependence (distinct sections of an array)`
### open_at : `2007-06-17T15:35:43Z`
### last_modified_date : `2019-06-26T05:09:30Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=32378
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.3.0`
### severity : `minor`
### contents :
gfortran -O2  -ftree-vectorize -ftree-vectorizer-verbose=2 -c -v s174.f
The two sections of the array are clearly distinct, so it should be vectorized.


---


### compiler : `gcc`
### title : `can't determine dependence (loop reversal required)`
### open_at : `2007-06-17T15:44:19Z`
### last_modified_date : `2023-02-03T21:48:39Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=32379
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.3.0`
### severity : `enhancement`
### contents :
gfortran -O2  -ftree-vectorize -ftree-vectorizer-verbose=2 -c -v s112.f
The case could be vectorized by taking the array elements in reverse order (as specified in the source).
ifort vectorizes by creating a temporary array (when the reversal is removed from the source), losing performance.


---


### compiler : `gcc`
### title : `Support using -mrecip w/o additional Newton-Raphson run`
### open_at : `2007-06-18T14:32:30Z`
### last_modified_date : `2021-09-20T02:59:39Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=32392
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.3.0`
### severity : `enhancement`
### contents :
Paolo Bonzini wrote:
>> That said, there is a whole bunch of applications that would kill for -mrecip, 
> even for 11bit ones. Games are one of them, for sure ;)
> What about -mrecip=0/1/2 for the number of NR steps? Or would two steps be 
> slower than divss?
>
> I was thinking of adding this as a follow-up patch ;) Just look how the 
> operations are grouped together.

As Richard pointed out: Having two NR does not make sense. For some cases doing with out Newton-Raphson is enough. (Example: Games -- or SPEC CPU 2006: http://www.hpcwire.com/hpc/1556972.html)

Other compilers have this option, e.g. Pathscale's -OPT:rsqrt=2 [yes, this is used for SPEC runs ;-)]


---


### compiler : `gcc`
### title : `__builtin_pow[i] - vectorize for other exponents besides 2 and 0.5`
### open_at : `2007-06-25T19:51:00Z`
### last_modified_date : `2021-08-11T05:15:43Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=32503
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.3.0`
### severity : `normal`
### contents :
http://gcc.gnu.org/ml/gcc-patches/2007-06/msg01172.html (PR 32239):

"At the moment the vectorizer only vectorizes builtin_pow if the exponent is either 2 or 0.5. whereas if we expand constant exponents in the gfortran frontend (gfc_conv_cst_int_power) it vectorizes for other constant integer powers as well (the expansion by the frontend generates a number of calls to builtin_pow with exponent 2.0)."

Expected: The same optimization is done for multiple of 2 (and -2) - as it is currently in the Fortran FE. (If this has been implemented in the ME, please inform the Fortraners to remove the expansion there.)

Additionally: It would be great if there would be a variant for long integers
(8 byte integers) and long long (16 byte integers) as PR32239 could only use __builtin_powi for int4 and not for int8 or int16.


---


### compiler : `gcc`
### title : `disastrous scheduling for POWER5`
### open_at : `2007-06-27T16:16:55Z`
### last_modified_date : `2023-01-30T19:53:18Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=32523
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `target`
### version : `4.2.0`
### severity : `normal`
### contents :
Hi,

On the POWER5, gcc 4.2 gets roughly half the performance of gcc 3.3.3 on the best ATLAS DGEMM kernel.  By throwing the flags 
   -fno-schedule-insns -fno-rerun-loop-opt
I'm able to get most of that performance back.  The most important flag is the no-schedule-insns, so I suspect the scheduler was rewritten between these releases.

I will append a tarfile that will build a simplified kernel so you can see the affects yourself.  This kernel is simplified, so it doesn't have quite the performance of the best one, but the general trend is the same (the best kernel is way to complicated to use).

One thing that you might scope out is a feature we have found on the PowerPC970FX (the direct decendent of the POWER5): I went from 69% of peak to 85% by scheduling like instructions in sets of 4 (i.e. do 4 loads, then 4 fmacs, etc, even when this hurts advancing loads).  Instruction alignment is also important on this architecture, despite it being putatitively RISC.  I think both these features are results of it's complicated front-end, which does something similar to RISC-to-VLIW translation on the fly.  I suspect the sets-of-4 rule helps in tracking the groups, but I don't know for sure . . .

This scheduling seems to hurt the POWER4 only slightly.  I have been trying to install gcc 4.2 on PowerPC970FX, but so far no luck (it doesn't seem to like MacOSX).  I will let you know if I get results for the PowerPC970FX.

Let me know if there is something else you need.

Cheers,
Clint


---


### compiler : `gcc`
### title : `missed optimization to eliminate duplicate expressions`
### open_at : `2007-06-29T22:46:42Z`
### last_modified_date : `2021-07-25T01:58:15Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=32553
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.3.0`
### severity : `enhancement`
### contents :
In this example:

int g(void);

void f(int *p, int i)
{
        p[i] = g();
        p[i + 2] = g();
        p[i + 10] = g();
        p[i + 100] = g();
}

the common expression of (p + i * 4) isn't completely eliminated.
It works with the current stable Debian release (gcc (GCC) 4.1.2 20061115), but anything later misses this opportunity.


---


### compiler : `gcc`
### title : `Missing byte swap optimizations`
### open_at : `2007-07-03T08:38:31Z`
### last_modified_date : `2021-12-15T22:33:23Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=32605
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.2.1`
### severity : `enhancement`
### contents :
#include <algorithm>
#include <iterator>
template < typename T >
void reverse( T& t )
{
    unsigned char* bytes = reinterpret_cast< unsigned char* >( &t );
    std::swap_ranges( bytes, bytes + sizeof( T ) / 2,
        std::reverse_iterator< unsigned char* >( bytes + sizeof( T ) ) );
}
template void reverse( std::size_t& );

attached testcase produces massive byte-moves instead of bswap.

$ g++ -Wall swap_ranges.cpp -fomit-frame-pointer -m32 -O3 -c

00000000 <void reverse<unsigned int>(unsigned int&)>:
   0:   8b 44 24 04             mov    0x4(%esp),%eax
   4:   0f b6 08                movzbl (%eax),%ecx
   7:   0f b6 50 03             movzbl 0x3(%eax),%edx
   b:   88 48 03                mov    %cl,0x3(%eax)
   e:   0f b6 48 01             movzbl 0x1(%eax),%ecx
  12:   88 10                   mov    %dl,(%eax)
  14:   0f b6 50 02             movzbl 0x2(%eax),%edx
  18:   88 48 02                mov    %cl,0x2(%eax)
  1b:   88 50 01                mov    %dl,0x1(%eax)
  1e:   c3                      ret

0000000000000000 <void reverse<unsigned long>(unsigned long&)>:
   0:   0f b6 17                movzbl (%rdi),%edx
   3:   0f b6 47 07             movzbl 0x7(%rdi),%eax
   7:   88 57 07                mov    %dl,0x7(%rdi)
   a:   88 07                   mov    %al,(%rdi)
   c:   0f b6 57 01             movzbl 0x1(%rdi),%edx
  10:   0f b6 47 06             movzbl 0x6(%rdi),%eax
  14:   88 57 06                mov    %dl,0x6(%rdi)
  17:   88 47 01                mov    %al,0x1(%rdi)
  1a:   0f b6 57 02             movzbl 0x2(%rdi),%edx
  1e:   0f b6 47 05             movzbl 0x5(%rdi),%eax
  22:   88 57 05                mov    %dl,0x5(%rdi)
  25:   88 47 02                mov    %al,0x2(%rdi)
  28:   0f b6 57 03             movzbl 0x3(%rdi),%edx
  2c:   0f b6 47 04             movzbl 0x4(%rdi),%eax
  30:   88 57 04                mov    %dl,0x4(%rdi)
  33:   88 47 03                mov    %al,0x3(%rdi)
  36:   c3                      retq


---


### compiler : `gcc`
### title : `missing CSE for constant in registers / inefficient memset`
### open_at : `2007-07-05T00:21:48Z`
### last_modified_date : `2021-07-26T22:20:50Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=32629
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.3.0`
### severity : `enhancement`
### contents :
gcc version 4.3.0 20070704 (experimental)

test case derived from linux kernel

struct x { 
        long a,b,c,d,e,f;
        char array[32];
};

void f(struct x *p)
{
        p->a = 0;
        p->b = 0;
        p->c = 0;
        p->d = 0;
        p->e = 0;
        p->f = 0;
        memset(&p->array, 0, 32);
}

compiled with -O2 or -Os gives
        movq    $0, (%rdi)
        movq    $0, 8(%rdi)
        movl    $8, %ecx
        movq    $0, 16(%rdi)
        movq    $0, 24(%rdi)
        xorl    %eax, %eax
        movq    $0, 32(%rdi)
        movq    $0, 40(%rdi)
        addq    $48, %rdi
        rep
        stosl
        ret

This shows several problems:
- the zero in eax should have been used for all the initializations
replacing the immediate giving shorter code [especially with -Os,
but it would have been a win even with -O2 e.g on decode limited CPUs]
In a more test complex case the xorl was even before all the field initializations.

- the rep ; stosl should be rep ; stosq because 8 byte alignment is guaranteed
by the type


---


### compiler : `gcc`
### title : `missed-optimization: bit-manipulation via bool's`
### open_at : `2007-07-06T12:24:50Z`
### last_modified_date : `2023-06-10T01:56:42Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=32648
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.3.0`
### severity : `enhancement`
### contents :
> cat b5-xor-b3.cc
bool f1(int a)
{
        bool b5 = a & 0x20;
        bool b3 = a & 0x08;
        return b5 ^ b3;
}
bool f2(int a)
{
        return (a ^ (a << 2)) & 0x20;
}

> g++ -O3 -c b5-xor-b3.cc
> objdump -d b5-xor-b3.o

b5-xor-b3.o:     file format elf64-x86-64

Disassembly of section .text:

0000000000000000 <_Z2f1i>:
   0:   c1 ef 03                shr    $0x3,%edi
   3:   89 f8                   mov    %edi,%eax
   5:   c1 ef 02                shr    $0x2,%edi
   8:   83 e0 01                and    $0x1,%eax
   b:   83 e7 01                and    $0x1,%edi
   e:   40 38 f8                cmp    %dil,%al
  11:   0f 95 c0                setne  %al
  14:   0f b6 c0                movzbl %al,%eax
  17:   c3                      retq
  18:   0f 1f 84 00 00 00 00    nopl   0x0(%rax,%rax,1)
  1f:   00

0000000000000020 <_Z2f2i>:
  20:   8d 04 bd 00 00 00 00    lea    0x0(,%rdi,4),%eax
  27:   31 f8                   xor    %edi,%eax
  29:   c1 e8 05                shr    $0x5,%eax
  2c:   83 e0 01                and    $0x1,%eax
  2f:   c3                      retq


---


### compiler : `gcc`
### title : `Code to convert double to _Complex double for arguments passing is not good (extra load)`
### open_at : `2007-07-09T03:31:51Z`
### last_modified_date : `2021-08-16T00:55:11Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=32686
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.3.0`
### severity : `enhancement`
### contents :
Testcase:
_Complex double f(_Complex double);
_Complex double g(double a)
{
  return f(a);
}

----- Cut ----
We currently get:
        mflr r0
        bcl 20,31,"L00000000001$pb"
"L00000000001$pb":
        stw r31,-4(r1)
        mflr r31
        stfd f1,-24(r1)
        mtlr r0
        lwz r3,-24(r1)
        lwz r4,-20(r1)
        addis r2,r31,ha16(LC0-"L00000000001$pb")
        lwz r31,-4(r1)
        la r5,lo16(LC0-"L00000000001$pb")(r2)
        lwz r6,4(r5)
        lwz r5,0(r5)
        b L_f$stub

We should be able to get:
        stfd f1,-8(r1)
        li r6,0
        li r5,0
        lwz r3,-8(r1)
        lwz r4,-4(r1)
        b L_f$stub

Without the need for the PIC register.


---


### compiler : `gcc`
### title : `i686 sse2 generates more movdqa than necessary`
### open_at : `2007-07-12T01:29:59Z`
### last_modified_date : `2022-01-11T10:09:41Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=32735
### status : `NEW`
### tags : `missed-optimization, ra`
### component : `target`
### version : `4.3.0`
### severity : `enhancement`
### contents :
Test program attached.

Command line:

mec@hollerith:~/exp-sum-delta$ /home/mec/gcc-4.3-20070707/install/bin/g++ -v -S 
-O2 -msse2 sum-delta.cc 
Using built-in specs.
Target: i686-pc-linux-gnu
Configured with: /home/mec/gcc-4.3-20070707/src/configure --build=i686-pc-linux-
gnu --host=i686-pc-linux-gnu --target=i686-pc-linux-gnu --prefix=/home/mec/gcc-4
.3-20070707/install --enable-languages=c,c++,objc,obj-c++,treelang --with-gmp=/h
ome/mec/gmp-4.2.1/install --with-mpfr=/home/mec/mpfr-2.2.1/install
Thread model: posix
gcc version 4.3.0 20070707 (experimental)
 /home/mec/gcc-4.3-20070707/install/libexec/gcc/i686-pc-linux-gnu/4.3.0/cc1plus 
-quiet -v -D_GNU_SOURCE sum-delta.cc -quiet -dumpbase sum-delta.cc -msse2 -mtune
=generic -auxbase sum-delta -O2 -version -o sum-delta.s
ignoring nonexistent directory "/home/mec/gcc-4.3-20070707/install/lib/gcc/i686-
pc-linux-gnu/4.3.0/../../../../i686-pc-linux-gnu/include"
#include "..." search starts here:
#include <...> search starts here:
 /home/mec/gcc-4.3-20070707/install/lib/gcc/i686-pc-linux-gnu/4.3.0/../../../../
include/c++/4.3.0
 /home/mec/gcc-4.3-20070707/install/lib/gcc/i686-pc-linux-gnu/4.3.0/../../../../
include/c++/4.3.0/i686-pc-linux-gnu
 /home/mec/gcc-4.3-20070707/install/lib/gcc/i686-pc-linux-gnu/4.3.0/../../../../
include/c++/4.3.0/backward
 /usr/local/include
 /home/mec/gcc-4.3-20070707/install/include
 /home/mec/gcc-4.3-20070707/install/lib/gcc/i686-pc-linux-gnu/4.3.0/include
 /home/mec/gcc-4.3-20070707/install/lib/gcc/i686-pc-linux-gnu/4.3.0/include-fixe
d
 /usr/include
End of search list.
GNU C++ version 4.3.0 20070707 (experimental) (i686-pc-linux-gnu)
        compiled by GNU C version 4.3.0 20070707 (experimental), GMP version 4.2
.1, MPFR version 2.2.1.
warning: GMP header version 4.2.1 differs from library version 4.1.4.
GGC heuristics: --param ggc-min-expand=30 --param ggc-min-heapsize=4096
Compiler executable checksum: 1338ea4083517ffee92283f96caf8872

===

The loop for CallSumDeltas2 compiles to:

.L7:
        movdqa  %xmm1, %xmm0
        pslldq  $4, %xmm0
        addl    $1, %eax
        paddd   %xmm1, %xmm0
        cmpl    $100000000, %eax
        movdqa  %xmm0, %xmm1
        pslldq  $8, %xmm1
        paddd   %xmm1, %xmm0
        movdqa  %xmm0, %xmm1
        movdqa  %xmm0, foo1
        jne     .L7

===

This is two more movdqa then the hand-written code in CallSumDeltas3.


---


### compiler : `gcc`
### title : `-Os: shorter load immediates for x86_64`
### open_at : `2007-07-18T06:44:24Z`
### last_modified_date : `2021-12-18T13:49:23Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=32803
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `target`
### version : `4.3.0`
### severity : `enhancement`
### contents :
gcc currently uses "mov $imm32,reg" and "mov $imm64,reg" for loading non-zero immediates... these cost 5 and 11 bytes resp.  for space optimizations there are shorter choices.

for immediates -128..127 the following generates 64-bit sign-extended results in 3 bytes:

  push $imm8
  pop %rax

the following generates immediates 0..255 with only 4 bytes (so given the above sequence it's useful for 128..255):

  xor %eax,%eax
  mov $X,%al

the following generates powers of 2 in only 7 bytes (worthwhile only for powers of 2 above 31):

  xor %eax,%eax
  bts $N,%eax

-dean


---


### compiler : `gcc`
### title : `Missing optimization to remove backward dependencies`
### open_at : `2007-07-18T09:58:32Z`
### last_modified_date : `2023-08-04T19:31:16Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=32806
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.3.0`
### severity : `enhancement`
### contents :
for (i=0; i<N; i++)
{
  D[i] = A[i] + Y;
  A[i+1] = B[i] + X;
}

Even though, this loop contains a backward-carried dependence between A[i+1] and A[i], it is vectorizable  - the stmts of the loop should be interchanged to get:

for (i=0; i<N; i++)
{
  A[i+1] = B[i] + X;
  D[i] = A[i] + Y;
}

which will be vectorizable once the pacth in PR 32377 (comment #14) is committed. 

The interchange is possible since there is no loop-independent dependence between the stmts. This requires working with a dependence graph when vectorizing, or have a separate optimization before the vectorizer to take care of this.

Ira


---


### compiler : `gcc`
### title : `Reduction with nonzero start (arbitrary also) causes an extra add to happen`
### open_at : `2007-07-19T17:11:39Z`
### last_modified_date : `2021-07-19T03:27:19Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=32825
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.3.0`
### severity : `enhancement`
### contents :
Testcase (Compile at -O2 -maltivec -ftree-vectorize):
int a[16*100];
int f(int e)
{
  int i;
  for(i = 0;i<16*100;i++)
    e += a[i];
  return e;
}
--------- Cut -----
Currently we get:
  ivtmp.42 = (long unsigned int) &a;
  vect_var_.36 = { 0, 0, 0, 0 };

<bb 3>:
  vect_var_.36 = MEM[index: ivtmp.42] + vect_var_.36;
  ivtmp.42 = ivtmp.42 + 16;
  if (ivtmp.42 != (long unsigned int) (&a + 6400))
    goto <bb 3>;
  else
    goto <bb 4>;

<bb 4>:
  vect_var_.39 = vect_var_.36 v>> 64;
  vect_var_.47 = vect_var_.39 + vect_var_.36;
  vect_var_.48 = vect_var_.47 v>> 32;
  stmp_var_.38 = BIT_FIELD_REF <vect_var_.48 + vect_var_.47, 32, 96>;
  return stmp_var_.38 + e;

Though the last add is extra and does not need to be done, we can get rid of it by having vect_var_.36 being set initially to {e, 0, 0, 0} .

Note this happens with a non zero start also, that is:
int a[16*100];
int f(int e)
{
  int i;
  e = 1;
  for(i = 0;i<16*100;i++)
    e += a[i];
  return e;
}


---


### compiler : `gcc`
### title : `Reduction into a global variable causes a Load Hit Store Hazard (for the Cell)`
### open_at : `2007-07-19T17:14:43Z`
### last_modified_date : `2022-03-08T16:20:54Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=32826
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.3.0`
### severity : `enhancement`
### contents :
Testcase (compile at -O2 -maltivec -ftree-vectorize):
int a[16*100];
int e;
float f(void)
{
  int i;
  int e1;
  e1 = e;
  for(i = 0;i<16*100;i++)
    e1 += a[i];
  e = e1;
}

----------- cut ------
Currently you get:
        stvewx v1,0,r2
        lis r2,ha16(_e)
        lwz r0,-20(r1)   <---- LHS hazard
        stw r0,lo16(_e)(r2)

Even though the elements of v1 will all be the same, so GCC could do:
        lis r2,ha16(_e)
        add r2, lo16(_e)(r2)
        stvewx v1,0,r2


---


### compiler : `gcc`
### title : `missed optimisation could pull branch out of loop`
### open_at : `2007-08-08T19:03:41Z`
### last_modified_date : `2021-07-19T05:07:46Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=33027
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.3.0`
### severity : `enhancement`
### contents :
The following code could be optimised significantly better (to help C++ with inlined generic-style stuff).

# 1 "doopt.cc"
# 1 "<built-in>"
# 1 "<command-line>"
# 1 "doopt.cc"


unsigned int fn(unsigned int n, unsigned int dmax) throw()
{
  for (unsigned int d = 0; d < dmax; ++d) {
    n += d?d:1;
  }
  return n;
}

There follows the output of g++ -v -save-temps my-options source-file:

Using built-in specs.
Target: x86_64-unknown-linux-gnu
Configured with: ./configure --disable-bootstrap
Thread model: posix
gcc version 4.3.0 20070802 (experimental)
 /usr/local/libexec/gcc/x86_64-unknown-linux-gnu/4.3.0/cc1plus -E -quiet -v -D_GNU_SOURCE -DNEW doopt.cc -mtune=generic -O3 -fpch-preprocess -o doopt.ii
ignoring nonexistent directory "/usr/local/lib/gcc/x86_64-unknown-linux-gnu/4.3.0/../../../../x86_64-unknown-linux-gnu/include"
#include "..." search starts here:
#include <...> search starts here:
 /usr/local/lib/gcc/x86_64-unknown-linux-gnu/4.3.0/../../../../include/c++/4.3.0
 /usr/local/lib/gcc/x86_64-unknown-linux-gnu/4.3.0/../../../../include/c++/4.3.0/x86_64-unknown-linux-gnu
 /usr/local/lib/gcc/x86_64-unknown-linux-gnu/4.3.0/../../../../include/c++/4.3.0/backward
 /usr/local/include
 /usr/local/lib/gcc/x86_64-unknown-linux-gnu/4.3.0/include
 /usr/local/lib/gcc/x86_64-unknown-linux-gnu/4.3.0/include-fixed
 /usr/include
End of search list.
 /usr/local/libexec/gcc/x86_64-unknown-linux-gnu/4.3.0/cc1plus -fpreprocessed doopt.ii -quiet -dumpbase doopt.cc -mtune=generic -auxbase doopt -O3 -version -o doopt.s
GNU C++ version 4.3.0 20070802 (experimental) (x86_64-unknown-linux-gnu)
        compiled by GNU C version 4.1.2 (Ubuntu 4.1.2-0ubuntu4), GMP version 4.2.1, MPFR version 2.2.1.
GGC heuristics: --param ggc-min-expand=30 --param ggc-min-heapsize=4096
Compiler executable checksum: 85805da771cde7753774ab06e3a9f9ac


---


### compiler : `gcc`
### title : `Redundant multiplications for memset`
### open_at : `2007-08-18T05:54:59Z`
### last_modified_date : `2021-08-22T01:26:59Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=33103
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.3.0`
### severity : `enhancement`
### contents :
This report was prompted by a mail on the lkml which was suggesting to hand-craft memset: http://lkml.org/lkml/2007/8/17/309 . So I wondered if the code generated for __builtin_memset was any good, and could be used instead of hand-crafted code. I tested with (Debian) GCC 3.4.6, 4.1.3, 4.2.1, and also with a snapshot of GCC 4.3. All the results are similar, so I will only show them for GCC 4.2 on x86-64. Compilation was done with -O3.

First, the __builtin_memset code:

  void fill1(char *s, int a)
  {
    __builtin_memset(s, a, 15);
  }

GCC generates:

   0:   40 0f b6 c6             movzbl %sil,%eax
   4:   48 ba 01 01 01 01 01    mov    $0x101010101010101,%rdx
   b:   01 01 01 
   e:   40 0f b6 ce             movzbl %sil,%ecx
  12:   48 0f af c2             imul   %rdx,%rax
  16:   40 88 77 0e             mov    %sil,0xe(%rdi)
  1a:   48 89 07                mov    %rax,(%rdi)
  1d:   40 0f b6 c6             movzbl %sil,%eax
  21:   69 c0 01 01 01 01       imul   $0x1010101,%eax,%eax
  27:   89 47 08                mov    %eax,0x8(%rdi)
  2a:   89 c8                   mov    %ecx,%eax
  2c:   c1 e0 08                shl    $0x8,%eax
  2f:   01 c8                   add    %ecx,%eax
  31:   66 89 47 0c             mov    %ax,0xc(%rdi)
  35:   c3                      retq   

Notice that GCC first computes %sil * (01)^8 and puts it into %rax, then it computes %sil * (01)^4 and puts it into %eax (where it already was, due to the previous multiplication), then it computes %sil * (01)^2 and puts it into %ax (where it already was, again).

Second, some code where multiplication results are reused:

  void fill2(char *s, int a)
  {
    unsigned long long int v = (unsigned char)a * 0x0101010101010101ull;
    *(unsigned long long int *)s = v;
    *(unsigned *)(s + 8) = v;
    *(unsigned short *)(s + 12) = v;
    *(s + 15) = v;
  }

GCC generates:

   0:   40 0f b6 f6             movzbl %sil,%esi
   4:   48 b8 01 01 01 01 01    mov    $0x101010101010101,%rax
   b:   01 01 01 
   e:   48 0f af f0             imul   %rax,%rsi
  12:   48 89 37                mov    %rsi,(%rdi)
  15:   89 77 08                mov    %esi,0x8(%rdi)
  18:   66 89 77 0c             mov    %si,0xc(%rdi)
  1c:   40 88 77 0f             mov    %sil,0xf(%rdi)
  20:   c3                      retq   

The function is 21 bytes smaller (-40%), it does not require two additional registers (c and d), and it will not be slower.

The same issue arises on x86_32. The hand-written code (with 32bit integers this time) is 14 bytes smaller for memset(,,15).


---


### compiler : `gcc`
### title : `missed store sinking opportunity`
### open_at : `2007-08-23T10:26:58Z`
### last_modified_date : `2023-05-06T18:37:08Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=33158
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.3.0`
### severity : `enhancement`
### contents :
In gcc.target/i386/cmov4.c no store sinking is performed for this code

  for (i = 0; i < ARCHnodes; i++) {
    nodekind[i] = (int) nodekindf[i];
    if (nodekind[i] == 3)
      nodekind[i] = 1;
  }

I would expect it to be rewritten as

  for (i = 0; i < ARCHnodes; i++) {
    int x = (int) nodekindf[i];
    if (x == 3)
      x = 1;
    nodekind[i] = x;
  }


---


### compiler : `gcc`
### title : `-mminimal-toc register should be psedu-register`
### open_at : `2007-08-29T18:34:02Z`
### last_modified_date : `2022-03-08T16:20:41Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=33236
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.3.0`
### severity : `enhancement`
### contents :
If -minimal-toc is used with a leaf function (that uses global memory), the register r31 is saved/restored which causes a LHS store on the Cell's PowerPC side.
Simple example:
int i;
int f(void)
{
  return i;
}
asm:
        std 30,-16(1)
        ld 30,.LCTOC0@toc(2)
        ld 9,.LC0-.LCTOC1(30)
        lwz 3,0(9)
        ld 30,-16(1)  <--- LHS because this is most likely within 50 cycles
        blr


---


### compiler : `gcc`
### title : `Missed opportunities for vectorization due to unhandled real_type`
### open_at : `2007-08-30T02:47:02Z`
### last_modified_date : `2021-07-21T02:41:50Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=33243
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.3.0`
### severity : `enhancement`
### contents :
There are two time consuming routines in air.f90 of the Polyhedron
benchmark that are not vectorized: lines 1328 and 1354.  These appear
in the top counting of execution time with oprofile:

      SUBROUTINE DERIVY(D,U,Uy,Al,Np,Nd,M)
      IMPLICIT REAL*8(A-H,O-Z)
      PARAMETER (NX=150,NY=150)
      DIMENSION D(NY,33) , U(NX,NY) , Uy(NX,NY) , Al(30) , Np(30)
      DO jm = 1 , M
         jmax = 0
         jmin = 1
         DO i = 1 , Nd
            jmax = jmax + Np(i) + 1
            DO j = jmin , jmax
               uyt = 0.
               DO k = 0 , Np(i)
                  uyt = uyt + D(j,k+1)*U(jm,jmin+k)
               ENDDO
               Uy(jm,j) = uyt*Al(i)
            ENDDO
            jmin = jmin + Np(i) + 1
         ENDDO
      ENDDO
      CONTINUE
      END

./poly_air_1354.f90:12: note: def_stmt: uyt_1 = PHI <0.0(9), uyt_42(11)>
./poly_air_1354.f90:12: note: Unsupported pattern.
./poly_air_1354.f90:12: note: not vectorized: unsupported use in stmt.
./poly_air_1354.f90:12: note: unexpected pattern.
./poly_air_1354.f90:1: note: vectorized 0 loops in function.

This is due to an unsupported type, real_type, for the reduction variable uyt:
(this is on an i686-linux machine)

 <ssa_name 0xb7c47270
    type <real_type 0xb7badb64 real8 DF
        size <integer_cst 0xb7ba0738 constant invariant 64>
        unit size <integer_cst 0xb7ba0754 constant invariant 8>
        align 64 symtab 0 alias set 3 canonical type 0xb7badb64 precision 64
        pointer_to_this <pointer_type 0xb7badca8>>
    visited var <var_decl 0xb7c40000 uyt> def_stmt <phi_node 0xb7c4a380>
    version 1>

Another similar routine that also appears in the top ranked and not
vectorized due to the same unsupported real_type reasons is in air.f90:1181


      SUBROUTINE FVSPLTX2
      IMPLICIT REAL*8(A-H,O-Z)
      PARAMETER (NX=150,NY=150)
      DIMENSION DX(NX,33) , ALX(30) , NPX(30)
      DIMENSION FP1(NX,NY) , FM1(NX,NY) , FP1x(30,NX) , FM1x(30,NX)
      DIMENSION FP2(NX,NY) , FM2(NX,NY) , FP2x(30,NX) , FM2x(30,NX)
      DIMENSION FP3(NX,NY) , FM3(NX,NY) , FP3x(30,NX) , FM3x(30,NX)
      DIMENSION FP4(NX,NY) , FM4(NX,NY) , FP4x(30,NX) , FM4x(30,NX)
      DIMENSION FV2(NX,NY) , DXP2(30,NX) , DXM2(30,NX)
      DIMENSION FV3(NX,NY) , DXP3(30,NX) , DXM3(30,NX)
      DIMENSION FV4(NX,NY) , DXP4(30,NX) , DXM4(30,NX)
      COMMON /XD1   / FP1 , FM1 , FP2 , FM2 , FP3 , FM3 , FP4 , FM4 ,   &
     &                FP1x , FM1x , FP2x , FM2x , FP3x , FM3x , FP4x ,  &
     &                FM4x , FV2 , FV3 , FV4 , DXP2 , DXM2 , DXP3 ,     &
     &                DXM3 , DXP4 , DXM4 , DX , NPX , ALX , NDX , MXPy
 
 
      DO ik = 1 , MXPy
         jmax = 0
         jmin = 1
         DO i = 1 , NDX
            jmax = jmax + NPX(i) + 1
!
! INITIALIZE
!
            FP1x(i,ik) = 0.
            FM1x(i,ik) = 0.
            FP2x(i,ik) = 0.
            FM2x(i,ik) = 0.
            FP3x(i,ik) = 0.
            FM3x(i,ik) = 0.
            FP4x(i,ik) = 0.
            FM4x(i,ik) = 0.
            DXP2(i,ik) = 0.
            DXM2(i,ik) = 0.
            DXP3(i,ik) = 0.
            DXM3(i,ik) = 0.
            DXP4(i,ik) = 0.
            DXM4(i,ik) = 0.
            DO k = 0 , NPX(i)
               jk = jmin + k
               FP1x(i,ik) = FP1x(i,ik) + DX(jmax,k+1)*FP1(jk,ik)
               FM1x(i,ik) = FM1x(i,ik) + DX(jmin,k+1)*FM1(jk,ik)
               FP2x(i,ik) = FP2x(i,ik) + DX(jmax,k+1)*FP2(jk,ik)
               FM2x(i,ik) = FM2x(i,ik) + DX(jmin,k+1)*FM2(jk,ik)
               FP3x(i,ik) = FP3x(i,ik) + DX(jmax,k+1)*FP3(jk,ik)
               FM3x(i,ik) = FM3x(i,ik) + DX(jmin,k+1)*FM3(jk,ik)
               FP4x(i,ik) = FP4x(i,ik) + DX(jmax,k+1)*FP4(jk,ik)
               FM4x(i,ik) = FM4x(i,ik) + DX(jmin,k+1)*FM4(jk,ik)
               DXP2(i,ik) = DXP2(i,ik) + DX(jmax,k+1)*FV2(jk,ik)
               DXM2(i,ik) = DXM2(i,ik) + DX(jmin,k+1)*FV2(jk,ik)
               DXP3(i,ik) = DXP3(i,ik) + DX(jmax,k+1)*FV3(jk,ik)
               DXM3(i,ik) = DXM3(i,ik) + DX(jmin,k+1)*FV3(jk,ik)
               DXP4(i,ik) = DXP4(i,ik) + DX(jmax,k+1)*FV4(jk,ik)
               DXM4(i,ik) = DXM4(i,ik) + DX(jmin,k+1)*FV4(jk,ik)
            ENDDO
            FP1x(i,ik) = FP1x(i,ik)*ALX(i)
            FM1x(i,ik) = FM1x(i,ik)*ALX(i)
            FP2x(i,ik) = FP2x(i,ik)*ALX(i)
            FM2x(i,ik) = FM2x(i,ik)*ALX(i)
            FP3x(i,ik) = FP3x(i,ik)*ALX(i)
            FM3x(i,ik) = FM3x(i,ik)*ALX(i)
            FP4x(i,ik) = FP4x(i,ik)*ALX(i)
            FM4x(i,ik) = FM4x(i,ik)*ALX(i)
            DXP2(i,ik) = DXP2(i,ik)*ALX(i)
            DXM2(i,ik) = DXM2(i,ik)*ALX(i)
            DXP3(i,ik) = DXP3(i,ik)*ALX(i)
            DXM3(i,ik) = DXM3(i,ik)*ALX(i)
            DXP4(i,ik) = DXP4(i,ik)*ALX(i)
            DXM4(i,ik) = DXM4(i,ik)*ALX(i)
            jmin = jmin + NPX(i) + 1
         ENDDO
      ENDDO
      CONTINUE
      END


Here are some kernels from test_fpu.f90 that could be vectorized, 
but are not, due to the exact same problem with the real_type not 
supported.  The places where the vectorization fails are marked 
with a comment at the end of the line: !seb.

SUBROUTINE Crout (a,n)      
USE kinds
IMPLICIT NONE

INTEGER :: n                
REAL(RK8) :: a(n,n)         

INTEGER :: i, j, m, imax(1)      
INTEGER :: index(n)              
REAL(RK8) :: b(n,n), temp(n)     

index = (/(i,i=1,n)/)        

DO j = 1, n        
   DO i = 1, j-1
      b(i, j) = a(i, j)
   END DO
   DO i = j, n
      b(i, j) = a(n+1-j, i+1-j)
   END DO
END DO

DO j = 1, n   

   DO i = j, n    
      b(n-i+j,n+1-i) = b(n-i+j,n+1-i)-DOT_PRODUCT(b(n+1-i:n-i+j-1,n+1-i), b(1:j-1,j))  !seb1
   END DO

   imax = MAXLOC(ABS( (/ (b(j+i-1,i),i=1,n-j+1) /) ))
   m = imax(1)
   b(j+m-1,m) = 1/b(j+m-1,m)

   IF (m /= n+1-j) THEN   
      index((/j,n+1-m/))     = index((/n+1-m,j/))
      b((/j,n+1-m/),n+2-m:n) = b((/n+1-m,j/),n+2-m:n)
      temp(1:n+1-m)          = b(m:n, m)
      b(m:j-1+m, m)          = b(n+1-j:n, n+1-j)
      b(j+m:n, m)            = b(j, j+1:n+1-m)
      b(n+1-j:n, n+1-j)      = temp(1:j)
      b(j, j+1:n+1-m)        = temp(j+1:n+1-m)
   END IF

   DO i = j+1, n   
      b(j,i) = b(n,n+1-j)*(b(j,i)-DOT_PRODUCT(b(n+1-j:n-1,n+1-j),b(1:j-1,i))) !seb2
   END DO
END DO

DO j = 1, n-1     
   temp(1) = b(n, n+1-j)
   DO i = j+1, n
      b(n-i+j,n+1-i) = -DOT_PRODUCT(b(n-i+j:n-1,n+1-i),temp(1:i-j))*b(n,n+1-i)  !seb3
      temp(i-j+1) = b(n-i+j,n+1-i)
   END DO
END DO

DO i = 1, (n+1)/3      
   temp(1:n+2-3*i) = b(2*i:n+1-i,i)
   DO j = 2*i, n+1-i
      b(j, i) = b(n+i-j, n+1-j)
   END DO
   DO j = i, n+1-2*i
      b(i+j-1, j) = b(n+1-i, n+2-i-j)
   END DO
   b(n+1-i, i+1:n+2-2*i) = temp(1:n+2-3*i)
END DO

DO i = 1, n-1      
   DO j = i+1, n
      b(i,j) = -b(i,j)-DOT_PRODUCT(temp(1:j-i-1), b(i+1:j-1,j)) !seb4
      temp(j-i) = b(i,j)
   END DO
END DO

DO i = 1, n-1      
   temp(1:n-i) = b(i,i+1:n)
   DO j = 1,i
      b(i,j) = b(i,j)+DOT_PRODUCT(temp(1:n-i),b(i+1:n,j))  !seb5
   END DO
   DO j = i+1, n
      b(i,j) = DOT_PRODUCT(temp(j-i:n-i),b(j:n,j)) !seb6
   END DO
END DO

END SUBROUTINE Crout


Here are the details about the fails:

seb6: not vectorized because of real_type problem

./test_fpu.f90:80: note: def_stmt: val.75_1012 = PHI <val.75_1028(250), 0.0(248)>
./test_fpu.f90:80: note: Unsupported pattern.
./test_fpu.f90:80: note: not vectorized: unsupported use in stmt.
./test_fpu.f90:80: note: unexpected pattern.(get_loop_exit_condition 

seb5: same real_type problem

./test_fpu.f90:77: note: def_stmt: val.73_887 = PHI <val.73_994(241), 0.0(239)>
./test_fpu.f90:77: note: Unsupported pattern.
./test_fpu.f90:77: note: not vectorized: unsupported use in stmt.

seb4: same real_type problem

./test_fpu.f90:69: note: def_stmt: val.70_980 = PHI <val.70_931(222), 0.0(220)>
./test_fpu.f90:69: note: Unsupported pattern.
./test_fpu.f90:69: note: not vectorized: unsupported use in stmt.

seb3: same real_type problem

./test_fpu.f90:51: note: def_stmt: val.66_229 = PHI <val.66_770(181), 0.0(179)>
./test_fpu.f90:51: note: Unsupported pattern.
./test_fpu.f90:51: note: not vectorized: unsupported use in stmt.

seb2: same real_type problem

./test_fpu.f90:44: note: def_stmt: val.64_260 = PHI <val.64_711(165), 0.0(163)>
./test_fpu.f90:44: note: Unsupported pattern.
./test_fpu.f90:44: note: not vectorized: unsupported use in stmt.

seb1: same real_type problem

./test_fpu.f90:26: note: def_stmt: val.18_1661 = PHI <val.18_244(53), 0.0(51)>
./test_fpu.f90:26: note: Unsupported pattern.
./test_fpu.f90:26: note: not vectorized: unsupported use in stmt.


---


### compiler : `gcc`
### title : `Missed opportunities for vectorization`
### open_at : `2007-08-30T02:55:16Z`
### last_modified_date : `2021-08-11T04:13:04Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=33244
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.3.0`
### severity : `normal`
### contents :
The following loop showing up in the top time users in capacita.f90 is
not vectorized because the loop latch block is non empty:

./capacita.f90:51: note: ===== analyze_loop_nest =====
./capacita.f90:51: note: === vect_analyze_loop_form ===
./capacita.f90:51: note: not vectorized: unexpected loop form.
./capacita.f90:51: note: bad loop form.
./capacita.f90:9: note: vectorized 0 loops in function.

This block contains the following code that comes from the
partial redundancy elimination pass:

      bb_14 (preds = {bb_13 }, succs = {bb_13 })
      {
      <bb 14>:
        # VUSE <SFT.109_593> { SFT.109 }
        pretmp.166_821 = g.dim[1].stride;
        goto <bb 13>;

      }

Now, if I disable the PRE with -fno-tree-pre, I get another problem on
the data dependence analysis:

	base_address: &d1
	offset from base address: 0
	constant offset from base address: 0
	step: 0
	aligned to: 128
	base_object: d1
	symbol tag: d1
	FAILED as dr address is invariant

/home/seb/ex/capacita.f90:46: note: not vectorized: unhandled data-ref 
/home/seb/ex/capacita.f90:46: note: bad data references.
/home/seb/ex/capacita.f90:4: note: vectorized 0 loops in function.

This fail corresponds to the following code in tree-data-ref.c

      /* FIXME -- data dependence analysis does not work correctly for objects with
	 invariant addresses.  Let us fail here until the problem is fixed.  */
      if (dr_address_invariant_p (dr))
	{
	  free_data_ref (dr);
	  if (dump_file && (dump_flags & TDF_DETAILS))
	    fprintf (dump_file, "\tFAILED as dr address is invariant\n");
	  ret = false;
	  break;
	}

Due to the following statement:

# VUSE <d1_143> { d1 }
d1.33_86 = d1;

So here the data reference is for d1 that is a read with the following tree:

    arg 1 <var_decl 0xb7be01cc d1 type <real_type 0xb7b4eaf8 real4>
        addressable used public static SF file /home/seb/ex/capacita.f90 line 11 size <integer_cst 0xb7b4163c 32> unit size <integer_cst 0xb7b41428 4>
        align 32
        chain <var_decl 0xb7be0170 d2 type <real_type 0xb7b4eaf8 real4>
            addressable used public static SF file /home/seb/ex/capacita.f90 line 11 size <integer_cst 0xb7b4163c 32> unit size <integer_cst 0xb7b41428 4>
            align 32 chain <var_decl 0xb7be0114 eps0>>>

I don't really know how this could be handled as a data reference,
because that statement has a VUSE but the type of d1 is scalar.

A reduced testcase is like this:



module solv_cap

  implicit none

  public  :: init_solve

  integer, parameter, public :: dp = selected_real_kind(5)

  real(kind=dp), private :: Pi, Mu0, c0, eps0
  logical,       private :: UseFFT, UsePreco
  real(kind=dp), private :: D1, D2
  integer,       private, save :: Ng1=0, Ng2=0
  integer,       private, pointer,     dimension(:,:)  :: Grid
  real(kind=dp), private, allocatable, dimension(:,:)  :: G

contains

  subroutine init_solve(Grid_in, GrSize1, GrSize2, UseFFT_in, UsePreco_in)
    integer, intent(in), target, dimension(:,:) :: Grid_in
    real(kind=dp), intent(in)  :: GrSize1, GrSize2
    logical,       intent(in)  :: UseFFT_in, UsePreco_in
    integer                    :: i, j

    Pi = acos(-1.0_dp)
    Mu0 = 4e-7_dp * Pi
    c0 = 299792458
    eps0 = 1 / (Mu0 * c0**2)
    
    UseFFT = UseFFT_in
    UsePreco = UsePreco_in

    if(Ng1 /= 0 .and. allocated(G) ) then
      deallocate( G )
    end if

    Grid => Grid_in
    Ng1 = size(Grid, 1)
    Ng2 = size(Grid, 2)
    D1 = GrSize1/Ng1
    D2 = GrSize2/Ng2

    allocate( G(0:Ng1,0:Ng2) )

    write(unit=*, fmt=*) "Calculating G"
    do i=0,Ng1
      do j=0,Ng2
        G(i,j) = Ginteg( -D1/2,-D2/2, D1/2,D2/2, i*D1,j*D2 )
      end do
    end do

    if(UseFFT) then
      write(unit=*, fmt=*) "Transforming G"
      call FourirG(G,1)
    end if

    return
  end subroutine init_solve


  function Ginteg(xq1,yq1, xq2,yq2, xp,yp)  result(G)
    real(kind=dp), intent(in) :: xq1,yq1, xq2,yq2, xp,yp
    real(kind=dp)             :: G
    real(kind=dp)             :: x1,x2,y1,y2,t
    x1 = xq1-xp
    x2 = xq2-xp
    y1 = yq1-yp
    y2 = yq2-yp
 
    if (x1+x2 < 0) then
      t = -x1
      x1 = -x2
      x2 = t
    end if
    if (y1+y2 < 0) then
      t = -y1
      y1 = -y2
      y2 = t
    end if

    G = Vprim(x2,y2)-Vprim(x1,y2)-Vprim(x2,y1)+Vprim(x1,y1)

    return
  end function Ginteg


  function Vprim(x,y)  result(VP)
    real(kind=dp), intent(in) :: x,y
    real(kind=dp)             :: VP
    real(kind=dp)             :: r

    r = sqrt(x**2+y**2)
    VP = y*log(x+r) + x*log(y+r)

    return
  end function Vprim


end module solv_cap


---


### compiler : `gcc`
### title : `Missed opportunities for vectorization due to invariant condition`
### open_at : `2007-08-30T03:00:07Z`
### last_modified_date : `2021-08-28T19:46:38Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=33245
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.3.0`
### severity : `enhancement`
### contents :
The innermost loop in "j" cannot be vectorized because of the
irregular code in that loop, i.e. the condition "IF ( l.NE.k )".  But
the cond expression is invariant in that loop, so the whole condition
can be hoisted outside that loop, versioning the loop, and potentially
allowing the vectorization of the innermost loop.

      SUBROUTINE DGEFA(A,Lda,N,Ipvt,Info)
      INTEGER Lda , N , Ipvt(*) , Info
      DOUBLE PRECISION A(Lda,*)
      DOUBLE PRECISION t
      INTEGER IDAMAX , j , k , kp1 , l , nm1

      Info = 0
      nm1 = N - 1
      IF ( nm1.GE.1 ) THEN
         DO k = 1 , nm1
            kp1 = k + 1
            l = IDAMAX(N-k+1,A(k,k),1) + k - 1
            Ipvt(k) = l
            IF ( A(l,k).EQ.0.0D0 ) THEN
               Info = k
            ELSE
               IF ( l.NE.k ) THEN
                  t = A(l,k)
                  A(l,k) = A(k,k)
                  A(k,k) = t
               ENDIF
               t = -1.0D0/A(k,k)
               CALL DSCAL(N-k,t,A(k+1,k),1)
               DO j = kp1 , N
                  t = A(l,j)
                  IF ( l.NE.k ) THEN
                     A(l,j) = A(k,j)
                     A(k,j) = t
                  ENDIF
                  CALL DAXPY(N-k,t,A(k+1,k),1,A(k+1,j),1)
               ENDDO
            ENDIF
         ENDDO
      ENDIF
      Ipvt(N) = N
      IF ( A(N,N).EQ.0.0D0 ) Info = N
      CONTINUE
      END

The result of the vectorizer on this testcase is:

/home/seb/ex/linpk.f90:24: note: not vectorized: too many BBs in loop.
/home/seb/ex/linpk.f90:24: note: bad loop form.
/home/seb/ex/linpk.f90:1: note: vectorized 0 loops in function.

Okay, if I'm versioning that loop by hand, I get the same error due to
the PRE as for capacita.f90: the PRE inserts in the loop->latch block
some code: 

      <bb 11>:
        # VUSE <PARM_NOALIAS.16_252> { PARM_NOALIAS.16 }
        pretmp.47_297 = *n_13(D);
        goto <bb 10>;

And with PRE disabled, the fail occurs in the data ref analysis:

./linpk_corrected.f90:26: note: not vectorized: data ref analysis failed t.8_70 = (*a_25(D))[D.1406_69]
./linpk_corrected.f90:26: note: bad data references.


---


### compiler : `gcc`
### title : `guaranteed-true test not optimized away when input values later used`
### open_at : `2007-08-31T07:44:32Z`
### last_modified_date : `2021-08-13T22:58:49Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=33257
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `unknown`
### severity : `normal`
### contents :
I wrote a simple test of division and remainder results that should always be true ((a/b)*b+(a%b)==a, with a hardcoded constant for b).  In testing a current source tree (trunk rev 127954), I found that the test properly went away... unless I later printed out the quotient and remainder values.  If I passed them to printf, the test is still performed, even though it can't fail, and its intermediate values are not used.


---


### compiler : `gcc`
### title : `guaranteed-true arithmetic test not optimized away depending on constant`
### open_at : `2007-08-31T07:52:28Z`
### last_modified_date : `2021-08-08T17:42:59Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=33258
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `unknown`
### severity : `normal`
### contents :
As in 33257, I was playing around with division+remainder code, and found another case gcc didn't optimize.  I was using signed and unsigned variants, and tried a couple different constants.  The test case was optimized properly with the constant 3 (signed or unsigned math), and with the constant 128 if unsigned math was used.  Using 128 with signed math, the test didn't get optimized away.


---


### compiler : `gcc`
### title : `stores not commoned by sinking`
### open_at : `2007-09-05T18:53:36Z`
### last_modified_date : `2023-05-15T00:27:10Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=33315
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.3.0`
### severity : `enhancement`
### contents :
if ( x == 8 ) statement1
if ( x != 8 ) statement1
if ( x == 9 ) statement2
if ( x != 9 ) statement2
should be replaced by

statement1
statement2

However this doesnt happen and compare and jumps do get generated.


---


### compiler : `gcc`
### title : `Badly optimized negations on x86 with -frounding-math`
### open_at : `2007-10-06T09:49:38Z`
### last_modified_date : `2021-10-27T12:09:09Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=33675
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.1.2`
### severity : `enhancement`
### contents :
If you compile the function

void assign2(float* a, double b) {
  volatile float v = -b;
  *a = -v;
}

you will see that GCC 4.1.2, e.g., at -O2, produces

        fldl    12(%ebp)
        fchs
        movl    8(%ebp), %eax
        fstps   -20(%ebp)
        flds    -20(%ebp)
        fstps   -4(%ebp)
        flds    -4(%ebp)
        fchs
        fstps   (%eax)

insted of simply

        fldl    12(%ebp)
        fchs
        fstps   -4(%ebp)
        flds    -4(%ebp)
        fchs
        fstps   (%eax)


---


### compiler : `gcc`
### title : `unnecessary checks against inifinity with -ffinite-math-only.`
### open_at : `2007-10-08T08:10:34Z`
### last_modified_date : `2021-07-26T09:58:32Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=33687
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.3.0`
### severity : `enhancement`
### contents :
#include <limits>
template < typename T >
int is_infinity( T value ) throw()
{
        if ( !std::numeric_limits< T >::has_infinity )
                return 0;
        T const inf = std::numeric_limits< T >::infinity();
        if ( value == +inf )
                return +1;
        if ( value == -inf )
                return -1;
        return 0;
}
template int is_infinity( double );

with -ffinite-math-only the <double> specialization could be optimized
to always return 0 but gcc produces checks against +inf
(aka __builtin_huge_val).


---


### compiler : `gcc`
### title : `[11/12/13/14 regression] missing optimization on const addr area store`
### open_at : `2007-10-08T16:54:26Z`
### last_modified_date : `2023-07-07T10:28:55Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=33699
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.3.0`
### severity : `normal`
### contents :
Same problem for
-0s/-02
version 4.1.0
etc...


[Code]

typedef unsigned * ptr_t;
void f (void) {
    ptr_t p = (ptr_t)0xFED0;
    p[0] = 0xDEAD;
    p[2] = 0xDEAD;
    p[4] = 0xDEAD;
    p[6] = 0xDEAD;
}


[Assembly generated by version gcc-4.3-20071005]

00000000 <f>:
   0:	3404dead 	li	a0,0xdead
   4:	3402fee8 	li	v0,0xfee8
   8:	3403fed0 	li	v1,0xfed0
   c:	ac440000 	sw	a0,0(v0)
  10:	ac640000 	sw	a0,0(v1)
  14:	3402fed8 	li	v0,0xfed8
  18:	3403fee0 	li	v1,0xfee0
  1c:	ac440000 	sw	a0,0(v0)
  20:	03e00008 	jr	ra
  24:	ac640000 	sw	a0,0(v1)


[Assembly generated by version 3.4.5 (seems better)]

00000000 <f>:
   0:	3403fed0 	li	v1,0xfed0
   4:	3402dead 	li	v0,0xdead
   8:	ac620018 	sw	v0,24(v1)
   c:	ac620000 	sw	v0,0(v1)
  10:	ac620008 	sw	v0,8(v1)
  14:	03e00008 	jr	ra
  18:	ac620010 	sw	v0,16(v1)
  1c:	00000000 	nop


[Version]

Using built-in specs.
Target: mips-elf
Configured with: ../gcc-4.3-20071005/configure --enable-languages=c,c++ --prefix=/auto/mipaproj/fshvaige/apps/Linux/gcc-4.3-20071005 --target=mips-elf --program-suffix=.mips --without-headers --with-newlib
Thread model: single
gcc version 4.3.0 20071005 (experimental) (GCC) 


[Command line options]

gcc.mips -c -o main.o -v -save-temps -O3 -march=mips64 -mabi=eabi -mexplicit-relocs main.c


---


### compiler : `gcc`
### title : `gcc generates suboptimal code for long long shifts`
### open_at : `2007-10-09T16:20:15Z`
### last_modified_date : `2023-05-15T04:32:05Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=33716
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `target`
### version : `4.3.0`
### severity : `enhancement`
### contents :
Consider this function:

unsigned long long x(unsigned long long l) {
  return l >> 4;
}

gcc will use the shrd instruction here, which is much slower than doing it "by hand" on at least Athlon, Pentium 3, VIA C3.  On Core 2 shrd appears to be faster.

On my Athlon 64, I measured 350 cycles vs 441 for a loop of 100.
On my Core 2, I measured 672 cycles vs 624.

So, my suggestion is: if -march= is set to Pentium 3 or a non-Intel CPU, don't use shrd and shrl.

My benchmark program is on http://dl.fefe.de/shrd.c


---


### compiler : `gcc`
### title : `slow code generated for 64-bit arithmetic`
### open_at : `2007-10-09T16:53:34Z`
### last_modified_date : `2021-12-27T15:05:40Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=33717
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.3.0`
### severity : `enhancement`
### contents :
gcc generates very poor code on some bignum code I wrote.

I put the sample code to http://dl.fefe.de/bignum-add.c for you to look at.

The crucial loop is this (x, y and z are arrays of unsigned int).

  for (i=0; i<100; ++i) {
    l += (unsigned long long)x[i] + y[i];
    z[i]=l;
    l>>=32;
  }

gcc code (-O3 -march=athlon64):

        movl    -820(%ebp,%esi,4), %eax
        movl    -420(%ebp,%esi,4), %ecx
        xorl    %edx, %edx
        xorl    %ebx, %ebx
        addl    %ecx, %eax
        adcl    %ebx, %edx
        addl    -1224(%ebp), %eax
        adcl    -1220(%ebp), %edx
        movl    %eax, -4(%edi,%esi,4)
        incl    %esi
        movl    %edx, %eax
        xorl    %edx, %edx
        cmpl    $101, %esi
        movl    %eax, -1224(%ebp)
        movl    %edx, -1220(%ebp)
        jne     .L4

As you can see, gcc keeps the long long accumulator in memory.  icc keeps it
in registers instead:

        movl      4(%esp,%edx,4), %eax                          #25.30
        xorl      %ebx, %ebx                                    #25.5
        addl      404(%esp,%edx,4), %eax                        #25.5
        adcl      $0, %ebx                                      #25.5
        addl      %esi, %eax                                    #25.37
        movl      %ebx, %esi                                    #25.37
        adcl      $0, %esi                                      #25.37
        movl      %eax, 804(%esp,%edx,4)                        #26.5
        addl      $1, %edx                                      #24.22
        cmpl      $100, %edx                                    #24.15
        jb        ..B1.4        # Prob 99%                      #24.15

The difference is staggering: 2000 cycles for gcc, 1000 for icc.

This only happens on x86, btw.  On amd64 there are enough registers, so gcc and icc are closer (840 vs 924, icc still generates better code here).

Still: both compilers could generate even better code.  I put some inline asm in the file for comparison, which could be improved further by loop unrolling.


---


### compiler : `gcc`
### title : `Could eliminate argument push for the second const function for same arguments`
### open_at : `2007-10-10T12:58:05Z`
### last_modified_date : `2021-08-09T04:42:44Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=33725
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `target`
### version : `4.3.0`
### severity : `enhancement`
### contents :
This testcase:

--cut here--
extern const int foo (int a);
extern const int bar (int a);

int test (int a)
{
  return foo (a) + bar (a);
}
--cut here--

compiles to:

test:
        subl    $12, %esp
        movl    %ebx, 4(%esp)
        movl    16(%esp), %ebx
        movl    %esi, 8(%esp)
        movl    %ebx, (%esp)    (*)
        call    foo
        movl    %ebx, (%esp)    (**)
        movl    %eax, %esi
        call    bar
        movl    4(%esp), %ebx
        addl    %esi, %eax
        movl    8(%esp), %esi
        addl    $12, %esp
        ret

However, since argument is already pushed to the stack for foo(), there is no need to push it again for the bar() function [foo() is const function]. If gcc eliminates the second push, a call-clobbered reg could be used to move argument to (esp), resulting in something like:

test:
        subl    $12, %esp
        movl    16(%esp), %eax
        movl    %esi, 8(%esp)
        movl    %eax, (%esp)
        call    foo
        movl    %eax, %esi
        call    bar
        addl    %esi, %eax
        movl    8(%esp), %esi
        addl    $12, %esp
        ret


---


### compiler : `gcc`
### title : `Extra load/store for float with union`
### open_at : `2007-11-03T17:47:12Z`
### last_modified_date : `2020-01-30T19:10:41Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=33989
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.3.0`
### severity : `enhancement`
### contents :
Testcase:
union a
{
  int i;
  float f;
};

void f(float *a, int *b, float e)
{
  union a c;
  c.f = *a + e;
  *b = c.i;
}

--- CUT ---
Currently we get (on x86):
        subl    $28, %esp
        movl    32(%esp), %eax
        flds    40(%esp)
        fadds   (%eax)
        movl    36(%esp), %eax
        fstps   12(%esp)  <--- extra store
        movl    12(%esp), %edx  <--- extra load
        movl    %edx, (%eax)  <--- store result to *b
        addl    $28, %esp
        ret
Or with -mfpmath=sse:
_f:
        subl    $28, %esp
        movl    32(%esp), %eax
        movss   40(%esp), %xmm0
        addss   (%eax), %xmm0
        movl    36(%esp), %eax
        movss   %xmm0, 12(%esp)  <--- extra store
        movl    12(%esp), %edx <--- extra load
        movl    %edx, (%eax)  <---store result to *b
        addl    $28, %esp
        ret

Or on PPC:
f:
        lfs 0,0(3)
        stwu 1,-16(1)
        fadds 0,1,0
        stfs 0,8(1)  <--- extra store
        lwz 0,8(1)  <--- extra load
        addi 1,1,16
        stw 0,0(4)  <--- store result to *b
        blr

The issue is that SFmode cannot be in integer registers.
The rtl looks like:
(insn 8 7 9 3 t1.c:10 (set (reg:SF 124)
        (mem:SF (reg/v/f:SI 120 [ a ]) [2 S4 A32])) -1 (nil))

(insn 9 8 10 3 t1.c:10 (set (reg:SF 123)
        (plus:SF (reg/v:SF 122 [ e ])
            (reg:SF 124))) -1 (nil))

(insn 10 9 11 3 t1.c:10 (set (subreg:SF (reg/v:SI 119 [ c ]) 0)
        (reg:SF 123)) -1 (nil))

(insn 11 10 16 3 t1.c:11 (set (mem:SI (reg/v/f:SI 121 [ b ]) [3 S4 A32])
        (reg/v:SI 119 [ c ])) -1 (nil))

See how we could translate register 119 (SImode) into a register that is in SFmode and get away with it.


---


### compiler : `gcc`
### title : `Memory load is not eliminated from tight vectorized loop`
### open_at : `2007-11-07T09:05:27Z`
### last_modified_date : `2021-07-26T19:49:07Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=34011
### status : `NEW`
### tags : `missed-optimization, ra`
### component : `tree-optimization`
### version : `4.3.0`
### severity : `normal`
### contents :
Following testcase exposes optimization problem with current SVN gcc:

--cut here--
extern const int srcshift;

void good (const int *srcdata, int *dstdata)
{
  int i;

  for (i = 0; i < 256; i++)
    dstdata[i] = srcdata[i] << srcshift;
}


void bad (const int *srcdata, int *dstdata)
{
  int i;

  for (i = 0; i < 256; i++)
    {
      dstdata[i] |= srcdata[i] << srcshift;
    }
}
--cut here--

Using -O3 -msse2, the loop in above testcase gets vectorized, and produced code differs substantially between good and bad function:

good:
        ...
.L8:
        xorl    %eax, %eax
        movd    srcshift, %xmm1
        .p2align 4,,7
        .p2align 3
.L4:
        movdqu  (%ebx,%eax), %xmm0
        pslld   %xmm1, %xmm0
        movdqa  %xmm0, (%esi,%eax)
        addl    $16, %eax
        cmpl    $1024, %eax
        jne     .L4
        ...

bad:
        ...
.L21:
        movl    %esi, %eax        (2)
        movl    %ebx, %edx
        leal    1024(%esi), %ecx
        .p2align 4,,7
        .p2align 3
.L17:
        movdqu  (%edx), %xmm0
        movd    srcshift, %xmm1   (1)
        pslld   %xmm1, %xmm0
        movdqu  (%eax), %xmm1     (3)
        por     %xmm1, %xmm0
        movdqa  %xmm0, (%eax)
        addl    $16, %eax         (4)
        addl    $16, %edx
        cmpl    %ecx, %eax
        jne     .L17
        popl    %ebx
        popl    %esi
        popl    %ebp
        ret

In addition to memory load in the loop (1), several other problems can be identified: There is no need to move registers (2), because loop is followed by function exit. For some reason, additional IV is used (4) and the same address is accessed with unaligned access (3) as well as aligned access.

Expected code for "bad" case would be something like "good" case with additional movaps+por instructions:

.L8:
        xorl    %eax, %eax
        movd    srcshift, %xmm1
        .p2align 4,,7
        .p2align 3
.L4:
        movdqu  (%ebx,%eax), %xmm0
        movaps  %xmm0, %xmm2
        pslld   %xmm1, %xmm0
        por     %xmm2, %xmm0
        movdqa  %xmm0, (%esi,%eax)
        addl    $16, %eax
        cmpl    $1024, %eax
        jne     .L4

Missing IV elimination could be attributed to tree loop optimizations, but others are IMO RTL optimization problems, because we enter RTL generation with:

good:
<bb 3>:
  MEM[base: dstdata, index: ivtmp.60] = M*(vect_p.29 + ivtmp.60){misalignment: 0} << srcshift.1;

bad:
<bb 4>:
  MEM[index: ivtmp.127] = M*(vector int *) ivtmp.130{misalignment: 0} << srcshift.3 | M*(vector int *) ivtmp.127{misalignment: 0};


---


### compiler : `gcc`
### title : `ARM: missed optimization (conditional store)`
### open_at : `2007-11-11T11:08:36Z`
### last_modified_date : `2021-11-28T04:53:00Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=34064
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.3.0`
### severity : `enhancement`
### contents :
The following code

void f(unsigned *_bss_start, unsigned *_bss_end)
{
  unsigned *p;

  for (p = _bss_start; p < _bss_end; p++)
    *p = 0;
}

when compiled with

  arm-elf-gcc -S -o - -fomit-frame-pointer -mcpu=arm7tdmi-s -Os t.c

produces (GCC 4.3.0 20071107)

f:
        mov     r3, #0
        b       .L2
.L3:
        str     r3, [r0], #4
.L2:
        cmp     r0, r1
        bcc     .L3
        bx      lr

It could be further optimized for both space and speed by emitting

f:
        mov     r3, #0
.L1:
        cmp     r0, r1
        strcc   r3, [r0], #4
        bcc     .L1
        bx      lr


---


### compiler : `gcc`
### title : `unoptimal byte extraction.`
### open_at : `2007-11-12T14:50:49Z`
### last_modified_date : `2023-08-05T21:39:54Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=34072
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.3.0`
### severity : `enhancement`
### contents :
$ cat b.cpp

unsigned char byte0( unsigned long long x ) { return x; }
unsigned char byte1( unsigned long long x ) { return ( x >> 8 ); }
unsigned char byte6( unsigned long long x ) { return ( x >> 48 ); }
unsigned char byte7( unsigned long long x ) { return ( x >> 56 ); }

$ /opt/gcc43/bin/g++ b.cpp -fomit-frame-pointer -m32 -O2 -c && objdump -dC b.o

00000000 <byte0(unsigned long long)>:
   0:   0f b6 44 24 04          movzbl 0x4(%esp),%eax
   5:   c3                      ret

00000010 <byte1(unsigned long long)>:
  10:   8b 44 24 04             mov    0x4(%esp),%eax  \
  14:   8b 54 24 08             mov    0x8(%esp),%edx   = why not movzbl 5(esp)?
  18:   0f ac d0 08             shrd   $0x8,%edx,%eax  /
  1c:   c3                      ret

00000020 <byte6(unsigned long long)>:
  20:   0f b7 44 24 0a          movzwl 0xa(%esp),%eax
  25:   c3                      ret

00000030 <byte7(unsigned long long)>:
  30:   0f b6 44 24 0b          movzbl 0xb(%esp),%eax
  35:   c3                      ret


---


### compiler : `gcc`
### title : `missed optimization with store motion (vectorizer)`
### open_at : `2007-11-22T15:30:23Z`
### last_modified_date : `2021-07-07T11:50:01Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=34195
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.3.0`
### severity : `enhancement`
### contents :
The following loop does not get vectorized 
on powerpc64-linux, r130275, GCC 4.3.0:

#define M 10

struct S
{
  float x;
  float y;
} pS[100];

float a[1000];
float b[1000];

void
foo (int n)
{
  int i, j;

  for (i = 0; i < n; i++)
    {
      pS[i].x = 0;
      pS[i].y = 0;

      for (j = 0; j < M; j++)
        {
          pS[i].x += (a[i]+b[i]);
          pS[i].y += (a[i]-b[i]);
        }
    }
}

Here is a snippet from the vectorizer dump file:

u3.c:17: note: dependence distance modulo vf == 0 between pS[i_37].x and pS[i_37].x
u3.c:17: note: dependence distance  = 0.
u3.c:17: note: accesses have the same alignment.
u3.c:17: note: dependence distance modulo vf == 0 between pS[i_37].y and pS[i_37].y
u3.c:17: note: === vect_analyze_data_ref_accesses ===
u3.c:17: note: Detected interleaving of size 2
u3.c:17: note: not vectorized: complicated access pattern.
u3.c:17: note: bad data access.(get_loop_exit_condition

...

        base_address: &pS
        offset from base address: (<unnamed-signed:32>) ((unsigned int) i_37 * 8)
        constant offset from base address: 0
        step: 0
        aligned to: 8
        base_object: pS[0].x
        symbol tag: pS
        FAILED as dr address is invariant

u3.c:22: note: not vectorized: unhandled data-ref
u3.c:22: note: bad data references.
u3.c:14: note: vectorized 0 loops in function.

[Zdenek's patch which extends lim can help to do store motion and thus help to the vectorizer - http://gcc.gnu.org/ml/gcc-patches/2007-01/msg02331.html, but AFAICT it is not applicable to current mainline)]


---


### compiler : `gcc`
### title : `simplify '(x & A) % B' if 'B > A/2'`
### open_at : `2007-12-10T10:56:11Z`
### last_modified_date : `2021-07-26T20:45:59Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=34417
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.3.0`
### severity : `enhancement`
### contents :
Hi,

In one of my application I need the expression '(x & 0xf) % 9'. Because of the restricted range of (x & 0xf) it's possible to replace the modulo operation with an if (see examples below). It would be nice if gcc could do this optimization automatically. 

unsigned fooA(unsigned x)
{
	return (x & 0xf) % 9;
}
unsigned fooB(unsigned x)
{
	x &= 0xf;
	if (x >= 9) x -= 9;
	return x;
}
unsigned fooC(unsigned x)
{
	x &= 0xf;
	return std::min(x, x - 9);
}


The generated code is pasted below (SVN revision r130738, linux_x86_64, -O3). Version B and C are very close (maybe C is slightly better) but they are clearly better than version A.

fooA:   andl    $15, %edi
        movl    $954437177, %edx
        movl    %edi, %eax
        mull    %edx
        shrl    %edx
        leal    0(,%rdx,8), %eax
        addl    %edx, %eax
        subl    %eax, %edi
        movl    %edi, %eax
        ret

fooB:   andl    $15, %edi
        leal    -9(%rdi), %eax
        cmpl    $9, %edi
        cmovae  %eax, %edi
        movl    %edi, %eax
        ret

fooC:   andl    $15, %edi
        leal    -9(%rdi), %eax
        cmpl    %edi, %eax
        cmova   %edi, %eax
        ret


---


### compiler : `gcc`
### title : `Multiply-by-constant pessimation`
### open_at : `2007-12-13T09:59:25Z`
### last_modified_date : `2021-09-23T12:03:54Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=34452
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `target`
### version : `4.2.2`
### severity : `enhancement`
### contents :
The multiply-by-constant optimization work poorly for x86 targets
with multiply units with short latency.

Try some small values M for a sample program like,

  long f (long x) { return x * M; }

for e.g. the -mtune=k8 subtarget.  One gets slow sequences of
lea, add, sub, sal.

So what's wrong?  Is it expmed.c's synth_mult that doesn't measure
costs correctly?  Or does i386.c provide poor cost measures?

I'd say that synth_mult's cost model is great for 3 operand
machines, but not very good for x86.  It does not see the
additional mov instructions inserted in many of its most clever
sequences, nor does it understand that small shifts are done with
the 2 cycle lea instruction (when src!=dst).

Additionally, synth_mult thinks a 10 operation long sequence that
cost 999 is the way to go if a single mult costs 1000.  It does
not take sequence length into account at all.  Perhaps it should?

Let's look at some examples of generated code for -mtune=k8.

6:  (11 bytes, >= 3 cycles)
        leaq    (%rdi,%rdi), %rax
        salq    $3, %rdi
        subq    %rax, %rdi

10: (12 bytes, >= 4 cycles)
        leaq    0(,%rdi,8), %rax
        leaq    (%rax,%rdi,2), %rax

11: (21 bytes, >= 4 cycles)
        leaq    0(,%rdi,4), %rdx
        movq    %rdi, %rax
        salq    $4, %rax
        subq    %rdx, %rax
        subq    %rdi, %rax

13: (21 bytes, >= 4 cycles)
        leaq    0(,%rdi,4), %rdx
        movq    %rdi, %rax
        salq    $4, %rax
        subq    %rdx, %rax
        addq    %rdi, %rax

etc, etc.

The cycle counts are only if we get ideal parallel execution,
otherwise one additional cycle will be needed.  The imul
instruction needs 4 cycles (64-bit operation) and is not
alignment sensitive and needs just one execution slot.  It can
therefore execute simultaneously with independent instructions,
while the above sequences will use up much decode, execute,
and retire resources.

What can be done about this?

The simple fix is to pretend multiplication is cheaper:

--- /u/gcc/gcc-4.2.2/gcc/config/i386/.~/i386.c.~1~      Sat Sep  1 17:28:30 2007
+++ /u/gcc/gcc-4.2.2/gcc/config/i386/i386.c     Thu Dec 13 10:12:07 2007
@@ -17254,7 +17254,7 @@
                op0 = XEXP (op0, 0), mode = GET_MODE (op0);
            }
 
-         *total = (ix86_cost->mult_init[MODE_INDEX (mode)]
+         *total = (ix86_cost->mult_init[MODE_INDEX (mode)] - 1
                    + nbits * ix86_cost->mult_bit
                    + rtx_cost (op0, outer_code) + rtx_cost (op1, outer_code));

This avoids most of the problems, but we still get a 4 cycle,
2 lea sequence for M = 10.

Potential problem: This might affect other parts of the optimizer
than synth_mult.  That might be bad, but it might also be desirable.

Another fix would perhaps be to teach synth_mult to understand that
it's generating code for a 2.5 operand machine (one that can only
do "a x= b", not "a = b x c", for some operation x).  We should
teach it that there will be moves inserted for sequences that rely
on a source register twice (more or less).

Letting synth_mult take sequence length into account would also
make sense, I think.  A cost of 1 per operation does not seem
unreasonable.

(I wrote synth_mult originally.)


---


### compiler : `gcc`
### title : `inefficient code for long long multiply when only low bits are needed`
### open_at : `2007-12-18T16:49:44Z`
### last_modified_date : `2019-12-19T15:51:25Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=34522
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.3.0`
### severity : `normal`
### contents :
For

int test(long long a, long long b)
{
        return a * b;
}

GCC generates a widening multiply, and cannot remove the DImode operations until after register allocation.  This causes unnecessary splits.

This could be fixed on the tree level by folding to (int)a * (int)b, or alternatively in expand.

expand_expr is called with

 <mult_expr 0x2aaaae9032c0
    type <integer_type 0x2aaaae937840 long long int DI>
    arg 0 <parm_decl 0x2aaaae92d2d0 b type <integer_type 0x2aaaae937840 long
long int>>
    arg 1 <parm_decl 0x2aaaae92d240 a type <integer_type 0x2aaaae937840 long
long int>>>

and tmode SImode, still enough info to choose a better multiply.  However, tmode is not passed on to expand_mult.


---


### compiler : `gcc`
### title : `operation performed unnecessarily in 64-bit mode`
### open_at : `2008-01-03T19:07:26Z`
### last_modified_date : `2021-12-25T07:19:50Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=34653
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.3.0`
### severity : `enhancement`
### contents :
for this code:

extern unsigned long table[];

unsigned long foo(unsigned char *p) {
  unsigned long long tag = *p;
  return table[tag >> 4];
}

gcc generates:

0000000000000000 <foo>:
   0:   0f b6 07                movzbl (%rdi),%eax
   3:   48 c1 e8 04             shr    $0x4,%rax
   7:   48 8b 04 c5 00 00 00    mov    0x0(,%rax,8),%rax
   e:   00
                        b: R_X86_64_32S table
   f:   c3                      retq

that "shr $0x4,%rax" would be better as "shr $0x4,%eax" because it produces the same result (due to dominating movzbl) and it's one byte shorter which favours both space and the narrow decoder on the core2.

thanks
-dean

/home/odo/gcc/bin/gcc -v
Using built-in specs.
Target: x86_64-unknown-linux-gnu
Configured with: ../gcc/configure --prefix=/home/odo/gcc --disable-multilib --disable-biarch x86_64-unknown-linux-gnu --enable-languages=c
Thread model: posix
gcc version 4.3.0 20071128 (experimental) (GCC)


---


### compiler : `gcc`
### title : `[11/12/13/14 Regression] Summing variable should be initialized to the first member before the loop`
### open_at : `2008-01-09T08:31:38Z`
### last_modified_date : `2023-07-07T10:28:58Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=34723
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.3.0`
### severity : `normal`
### contents :
This testcase:

--cut here--
char table[256];

int test(void) {

  char val = 0;
  int i;

  for (i = 0; i < 10; i++)
    val += table[i];

  return val;
}
--cut here--

compiles using gcc-4.2 -O2 to:

test:
        movzbl  table, %eax
        movl    $1, %edx
        .p2align 4,,7
.L2:
        addb    table(%edx), %al
        addl    $1, %edx
        cmpl    $10, %edx
        jne     .L2
        movsbl  %al,%eax
        ret

but using gcc-4.3 -O2 to:

test:
        xorl    %edx, %edx
        xorl    %eax, %eax
        .p2align 4,,7
        .p2align 3
.L2:
        addb    table(%edx), %al
        addl    $1, %edx
        cmpl    $10, %edx
        jne     .L2
        movsbl  %al,%eax
        ret

Note that gcc-4.3 initializes summation variable to zero, where gcc-4.2 initializes summation variable to first array member, saving one loop iteration.

The difference is already present on tree level, where:

gcc-4.2:

test ()
{
  int i;
  char val;

<bb 2>:
  val = (char) (unsigned char) MEM[symbol: table];
  i = 1;

<L0>:;
  val = (char) ((unsigned char) val + (unsigned char) MEM[symbol: table, index: (unsigned int) i]);
  i = i + 1;
  if (i != 10) goto <L0>; else goto <L2>;

<L2>:;
  return (int) val;

}

gcc-4.3:

test ()
{
  int i;
  char val;
  unsigned char D.1186;

<bb 2>:
  i = 0;
  val = 0;

<bb 3>:
  D.1186 = (unsigned char) val + (unsigned char) MEM[symbol: table, index: (unsigned int) i];
  val = (char) D.1186;
  i = i + 1;
  if (i != 10)
    goto <bb 3>;
  else
    goto <bb 4>;

<bb 4>:
  return (int) val;

}


---


### compiler : `gcc`
### title : `Missed autoincrement opportunities due to a different basic block structure.`
### open_at : `2008-01-18T14:15:26Z`
### last_modified_date : `2021-07-26T07:21:32Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=34849
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.3.0`
### severity : `normal`
### contents :
Whilst investigating a missed optimization oppurtunity in comparison to gcc 3.4 I came across this case. 

void foo (int n, int in[], int res[])
{
  int i;
  for (i=0; i<n;i++)
    if (in[i])
      res[i]= 0x1234;
    else
      res[i]= 0x9876;
}

The basic block structure generated is as follows 
foo (n, in, res)
{
  unsigned int ivtmp.19;
  int i;

<bb 2>:
  if (n > 0)
    goto <bb 3>;
  else
    goto <bb 8>;

<bb 3>:
  i = 0;
  ivtmp.19 = 0;

<bb 4>:
  if (MEM[base: in, index: ivtmp.19] != 0)
    goto <bb 5>;
  else
    goto <bb 6>;

<bb 5>:
  MEM[base: res, index: ivtmp.19] = 4660;
  goto <bb 7>;

<bb 6>:
  MEM[base: res, index: ivtmp.19] = 39030;

<bb 7>:
  i = i + 1;
  ivtmp.19 = ivtmp.19 + 4;
  if (n > i)
    goto <bb 4>;
  else
    goto <bb 8>;

<bb 8>:
  return;

}

If you notice ivtmp.19 can be used for post-increment based addressing modes. 


Note that GCC 3.4 did not have another basic block for the else case, the basic block for the else case got merged with the tail block of the loop and hence auto-inc could get generated in the else case and not in the if side of things. Can be reproduced with today's head of 4.3.0


---


### compiler : `gcc`
### title : `array constants after inlining and "staticification"`
### open_at : `2008-01-19T08:08:47Z`
### last_modified_date : `2021-09-25T01:32:28Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=34864
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.3.0`
### severity : `enhancement`
### contents :
Briefly: of all the ldexp variants only straight ldexp consistently get folded.
The overloaded c++ version, std::ldexp, is the easiest to derail, as this testcase demonstrates (note: you can't get much more than 1 such call folded); but it has also happened to me with ldexpf, it's just harder to trigger.

$ cat pr-ldexp.cc
#include <cmath>
#define L1(x) ldexp((float)(x | (1<<23)), -23)
#define L2(x) std::ldexp((float)(x | (1<<23)), -23)
int main(int argc, char *argv[]) {
        const float tbl[] = { L(0), L(1), L(2), L(3) };
        return int(tbl[argc]);
}
$ /usr/local/gcc-4.3-20080104/bin/g++ -O2 -march=k8 -DL=L1 pr-ldexp.cc -o pr1
$ /usr/local/gcc-4.3-20080104/bin/g++ -O2 -march=k8 -DL=L2 pr-ldexp.cc -o pr2

pr1:
 401091:       f3 0f 10 04 9d 00 20    movss  0x402000(,%ebx,4),%xmm0
 40109e:       f3 0f 2c c0             cvttss2si %xmm0,%eax
 4010a2:       c9                      leave

pr2:
 401090:       c7 45 e8 00 00 80 3f    movl   $0x3f800000,0xffffffe8(%ebp)
 401097:       c7 45 ec 01 00 80 3f    movl   $0x3f800001,0xffffffec(%ebp)
 40109e:       c7 45 f0 02 00 80 3f    movl   $0x3f800002,0xfffffff0(%ebp)
 4010a5:       c7 45 f4 03 00 80 3f    movl   $0x3f800003,0xfffffff4(%ebp)
 4010ac:       f3 0f 10 44 9d e8       movss  0xffffffe8(%ebp,%ebx,4),%xmm0
 4010b2:       8b 5d fc                mov    0xfffffffc(%ebp),%ebx
 4010b5:       f3 0f 2c c0             cvttss2si %xmm0,%eax
 4010b9:       c9                      leave 
(k8/sse codegen selected for clarity)


---


### compiler : `gcc`
### title : `contained subroutines called only once are not inlined`
### open_at : `2008-01-23T11:12:54Z`
### last_modified_date : `2021-11-27T01:18:31Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=34940
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.3.0`
### severity : `enhancement`
### contents :
contained subroutines called only once are not inlined, despite the fact that it is always a win (independent of the size of the contained subroutine). It 'only requires' counting the number of calls to cs1 in the routine s1, if it is 1, it should be inlined, as there can not be other callers.

example that shows no inlining at -O3 with 
GNU Fortran (GCC) 4.3.0 20080121 (experimental) [trunk revision 131689]

SUBROUTINE S1(X)
  CALL CS1(X)
CONTAINS
  SUBROUTINE CS1(X)
     CALL RANDOM_NUMBER(X)
     WRITE(6,*) X
  END SUBROUTINE CS1
END SUBROUTINE S1


---


### compiler : `gcc`
### title : `scalar evolution analysis fails with "evolution of base is not affine"`
### open_at : `2008-02-17T07:54:57Z`
### last_modified_date : `2023-08-04T19:57:31Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=35224
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.3.0`
### severity : `enhancement`
### contents :
For the following scalar evolution analysis fails with "evolution of base is not affine":

 for (i__ = 1; i__ <= i__2; ++i__)
        {
          a[i__] = (b[i__] + b[im1] + b[im2]) * .333f;
          im2 = im1;
          im1 = i__;
        }


---


### compiler : `gcc`
### title : `Loop distribution fails to distribute`
### open_at : `2008-02-21T06:41:31Z`
### last_modified_date : `2021-12-28T05:24:43Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=35272
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.4.0`
### severity : `enhancement`
### contents :
Loop distribution (from the patch http://gcc.gnu.org/ml/gcc-patches/2007-12/msg00215.html) fails to distribute the following loop:

for (i = 2; i <= n; ++i)
 {
   a[i] += c[i] * d[i];
   b[i] = a[i] + d[i] + b[i - 1];
 }

dumping "FIXME: Loop 1 not distributed: failed to build the RDG."

(After distribution the first loop will be vectorizable).


---


### compiler : `gcc`
### title : `Missing PRE for globals`
### open_at : `2008-02-22T06:24:26Z`
### last_modified_date : `2020-05-21T19:26:18Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=35286
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.3.0`
### severity : `enhancement`
### contents :
This was discussed with Dan Berlin. File this report as a place holder for the problem. In the following example, load of g1.a at return statement is fully redundant, but not removed. 


int g2;
struct A {
 int a; int b;
}g1;
int foo(int a, int b)
{
   if (a > 0)
   {
      g1.a = a+ b;
   }
   else
      g1.a = b;

   g2 = a+b;

  return g1.a;
}


---


### compiler : `gcc`
### title : `Expression reassociation problem`
### open_at : `2008-02-22T06:36:00Z`
### last_modified_date : `2023-09-24T04:50:13Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=35288
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `unknown`
### severity : `enhancement`
### contents :
The second instance of a1+a2 is not PREed due to missing expression reassociation.

int foo(int a1, int a2, int a3)
{
   int b1,b2;
   b1 = a3 + a2 + a1;
   b2 = a1  + a2;
   return b1 + b2;
}


---


### compiler : `gcc`
### title : `missing CSE of division (lack of reassociation)`
### open_at : `2008-02-22T06:44:08Z`
### last_modified_date : `2021-07-26T04:11:47Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=35289
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.3.0`
### severity : `enhancement`
### contents :
double a,b,c,d,e,f;
// int  a,b,c,d,e,f;

void foo()
{
   e = b*c/d;
   f = b/d*a;
}

Compile with -O3 -ffast-math, b/d should be CSEed.


---


### compiler : `gcc`
### title : `Missing DCE for union fields`
### open_at : `2008-02-22T06:50:42Z`
### last_modified_date : `2019-07-23T20:30:26Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=35291
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.3.0`
### severity : `enhancement`
### contents :
union U {
  struct C
   {
      char c[4];
   }cc;

   int ii;
} u ;

void foo(int i)
{
   u.cc.c[0] = 10; // Dead
   u.cc.c[1] = 10; // Dead too
   u.cc.c[i] = 10; // Dead too
   u.ii  = 20;
}


---
