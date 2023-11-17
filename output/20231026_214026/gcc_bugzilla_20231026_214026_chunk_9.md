### Total Bugs Detected: 4649
### Current Chunk: 9 of 30
### Bugs in this Chunk: 160 (From bug 1281 to 1440)
---


### compiler : `gcc`
### title : `revisit reassoc handling of pow / powi, amend match.pd for powi`
### open_at : `2016-04-28T07:55:00Z`
### last_modified_date : `2018-11-19T14:27:53Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70840
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `6.0`
### severity : `normal`
### contents :
Currently reassoc builds powi from repeated multiplications guarded with
-funsafe-math-optimizations where later expansion of powi is safe for
fp-contract != off.

The acceptable_pow_call cases are globally guarded with flag_unsafe_math_optimizations as well but POWI is always safe
and only POW has to be guarded with flag_unsafe_math_optimizations.

match.pd has quite some patterns involving POW but none involving POWI.
At least for flag_unsafe_math_optimizations POWI can be treated as POW
and whether we emit POW or POWI does not matter for flag_unsafe_math_optimziations.


---


### compiler : `gcc`
### title : `reassoc fails to handle FP division`
### open_at : `2016-04-28T08:22:49Z`
### last_modified_date : `2019-06-18T08:13:23Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70841
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `6.0`
### severity : `normal`
### contents :
reassoc fails to handle

float foo (float x, float y)
{
  return x * y / x;
}

with -freciprocal-math (at least) it could handle this as

  x * y * (1/x)

and simplify ops accordingly (with -funsafe-math-opts or maybe already
with -ffp-contract=fast).  Implementation-wise this could be
handled similar to how we handle minus for plus reassoc.  OTOH
it would be better to rewrite that with a flag on the op "negate"
and division could be handled with a flag "invert".


---


### compiler : `gcc`
### title : `Loop can be vectorized through gathers on AVX2 platforms.`
### open_at : `2016-04-28T13:35:59Z`
### last_modified_date : `2021-12-26T21:08:56Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70849
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `7.0`
### severity : `normal`
### contents :
Simple test which will be attached is not vectorized as not profitable:
test.c:11:5: note: cost model: the vector iteration cost = 2061 divided by the scalar iteration cost = 9 is greater or equal to the vectorization factor = 8.
test.c:11:5: note: not vectorized: vectorization not profitable.
test.c:11:5: note: not vectorized: vector version will never be profitable.

but it can be vectorized as icc does using gathers:
   LOOP BEGIN at test.c(11,5)
      remark #15388: vectorization support: reference c1[j] has aligned access   [ test.c(12,7) ]
      remark #15388: vectorization support: reference c2[j] has aligned access   [ test.c(13,7) ]
      remark #15388: vectorization support: reference c1[j] has aligned access   [ test.c(12,7) ]
      remark #15388: vectorization support: reference c2[j] has aligned access   [ test.c(13,7) ]
      remark #15415: vectorization support: gather was generated for the variable <f[j+base]>, strided by 256   [ test.c(12,16) ]
      remark #15415: vectorization support: gather was generated for the variable <f[j+base+1]>, strided by 256   [ test.c(13,16) ]
      remark #15415: vectorization support: gather was generated for the variable <f[j+base]>, strided by 256   [ test.c(12,16) ]
      remark #15415: vectorization support: gather was generated for the variable <f[j+base+1]>, strided by 256   [ test.c(13,16) ]
      remark #15305: vectorization support: vector length 8
      remark #15300: LOOP WAS VECTORIZED
      remark #15449: unmasked aligned unit stride stores: 4 
      remark #15460: masked strided loads: 4 
      remark #15475: --- begin vector loop cost summary ---
      remark #15476: scalar loop cost: 18 
      remark #15477: vector loop cost: 12.000 
      remark #15478: estimated potential speedup: 1.500 
      remark #15488: --- end vector loop cost summary ---
   LOOP END


---


### compiler : `gcc`
### title : `Improve code generation of switch tables`
### open_at : `2016-04-28T17:48:02Z`
### last_modified_date : `2021-07-26T23:49:46Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70861
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `7.0`
### severity : `enhancement`
### contents :
GCC uses a very basic check to determine whether to use a switch table. A simple example from https://gcc.gnu.org/bugzilla/show_bug.cgi?id=11823 still generates a huge table with mostly default entries with -O2:

int i;
int func(int a)
{
  switch(a)
  {
    case 0:   i = 20; break;
    case 1:   i = 50; break;
    case 2:   i = 29; break;
    case 3:   i = 20; break;
    case 4:   i = 50; break;
    case 5:   i = 29; break;
    case 6:   i = 20; break;
    case 7:   i = 50; break;
    case 8:   i = 29; break;
    case 9:   i = 79; break;
    case 110: i = 27; break;
    default:  i = 77; break;
  }
  return i;
}

This shows several issues:

1. The density calculation is not adjustable depending on the expected size of switch table entries (which depends on the target).
2. A table may contain not only 90% default entries, but they can be consecutive as well. To avoid this the maximum number of default cases should be limited to say 3x the average gap between real cases.
3. There is no reduction in minimum required density for larger switches - the wastage becomes quite significant for larger switches and targets that use 4 bytes per table entry.
4. Dense regions and outlier values are not split off and handled seperately.


---


### compiler : `gcc`
### title : `Assigning constructed temporary of class with nontrivial constructor uses unnecessary temporary`
### open_at : `2016-04-29T06:35:10Z`
### last_modified_date : `2021-12-25T08:29:15Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70868
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `6.1.0`
### severity : `enhancement`
### contents :
It's a common C++ idiom to clear a struct by assigning a default-constructed instance to it:

  struct Foo1 {
    int x;
    int array[2000];
  } foo1;

  void clearFoo1() {
    foo1 = Foo1();
  }

When compiled with -O2, this produces efficient assembly equivalent to "memset(&foo1, 0, sizeof(foo1))". However, throw in a nontrivial constructor via C++11 assignment initialization:

  struct Foo2 {
    int x = 0;
    int array[2000];
  } foo2;

  void clearFoo2() {
    foo2 = Foo2();
  }

While compiled with -cstd=c++11 -O2, the resulting assembly allocates a temporary on the stack and copies it, equivalent to:

  void clearFoo2() {
    char temp[sizeof(foo2)];
    memset(temp, 0, sizeof(foo2));
    memcpy(foo2, temp, sizeof(foo2));
  }

Besides being inefficient, the resulting code uses far more stack than expected. In my case, my embedded firmware was crashing due to stack exhaustion!

Here's a godbolt link with the code above: https://godbolt.org/g/QYLq9L

The resulting x86-64 assembly is:

clearFoo1():
        movl    $foo1, %edi
        movl    $1000, %ecx
        xorl    %eax, %eax
        rep stosq
        movl    $0, (%rdi)
        ret
clearFoo2():
        subq    $7904, %rsp
        xorl    %eax, %eax
        movl    $1000, %ecx
        leaq    -120(%rsp), %rdi
        leaq    -120(%rsp), %rsi
        rep stosq
        movl    $1000, %ecx
        movl    $0, (%rdi)
        movl    $foo2, %edi
        rep movsq
        movl    %eax, (%rdi)
        addq    $7904, %rsp
        ret

The result is the same with a variety of similar idioms:
  foo2 = Foo2();
  foo2 = Foo2{};
  foo2 = {};

The problem appears to have been in all old versions of gcc I've tested, up to 6.1.0. I haven't tested head. Clang >= 3.7 produces efficient code. Clang <= 3.6 produces a temporary and copy for both cases (clearFoo1 and clearFoo2).

In my codebase, assigning a default-constructed object is a common way to clear a struct. Using memset() directly, besides being ugly, would fail to set nontrivial members and members with non-zero default values correctly. The best workaround I've found is to use placement new:

  void clearFoo2PlacementNew() {
    foo2.~Foo2();
    new (&foo2) Foo2();
  }

Ugh.


---


### compiler : `gcc`
### title : `questionable optimisation in fold-const.c`
### open_at : `2016-04-29T09:07:23Z`
### last_modified_date : `2021-07-20T22:55:31Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70871
### status : `ASSIGNED`
### tags : `missed-optimization, wrong-code`
### component : `middle-end`
### version : `5.3.1`
### severity : `normal`
### contents :
typedef struct X
{   
    void *a; 
    long int b;
    int c;
    int d;   
    unsigned int e[3];
    unsigned short f;
    unsigned char g;
    unsigned char h;
    unsigned char i;
    unsigned char j;
    unsigned char k;
    unsigned char l;
    unsigned char m;
    unsigned char n;
};



int somefunc(void)
{
    struct X *pX = (0L);

    extern void call(void*);
    call(&pX);

    if(!pX->n  && !pX->l)
        return 0;

    return 1;
}

for -O1 and higher

 if(!pX->n  && !pX->l)

results in (tree-original)

 if ((BIT_FIELD_REF <*pX, 64, 320> & 280379743272960) == 0)


which eventually results in 
 ASAN_CHECK (6, _1, 8, 8) 
when using -fsantize=address

Wheras ASAN really should be reporting a 2x 1 byte load and not 1x 8.

Thanks


---


### compiler : `gcc`
### title : `Use MSB/LSB pointer-tagging for pointer-to-member representation`
### open_at : `2016-04-30T02:13:13Z`
### last_modified_date : `2022-12-25T06:49:58Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70885
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `c++`
### version : `6.0`
### severity : `enhancement`
### contents :
Currently there are two available pointer-to-member representation options:
  ptrmemfunc_vbit_in_pfn,
  ptrmemfunc_vbit_in_delta

where ptrmemfunc_vbit_in_pfn stores the "is a virtual function" pointer tag in the LSB of the pointer (assuming 16-bit aligned functions).

When using the tagged pointer to make the function call, the tag needs to be tested and the pointer converted into a valid address.  On SH this currently looks like this:

struct test_class
{
  int x;

  void func (void);
};

void test (test_class* c, void (test_class::*f)(void) )
{
  (c->*f) ();
}

compiled with -O2:
	mov	r5,r0      // r5 = r0 = __pfn field
	tst	#1,r0      // test LSB
	add	r6,r4
	bt	.L17       // if LSB not set, goto L17

	mov.l	@r4,r5     // when here, LSB is set
	add	r5,r0
	add	#-1,r0     // subtract 1 to clear LSB
	mov.l	@r0,r0
.L17:
	jmp	@r0
	nop


At least on SH, it's better to do store pointer tags in the MSB.  So that the tagged pointer value becomes:

   tagged_ptr_val = (ptr_val >> 1) | (tag_bit << 31)

This allows for more efficient tag test and pointer value restoration, the code could look like:

        mov     r5,r0
        shll    r5         // __pfn << 1, MSB -> T bit
	add	r6,r4
	bf	.L17       // if MSB not set, goto L17

	mov.l	@r4,r5
	add	r5,r0
	mov.l	@r0,r0
.L17:
	jmp	@r0
	nop

... which saves one instruction.
To enable that, there should be another option "ptrmemfunc_vbit_in_pfn_msb" along with some target specific m-option to enable this as well as a configure option to control the default setting.


---


### compiler : `gcc`
### title : `additional memory access generated in loop if destructor is inlined`
### open_at : `2016-05-01T10:53:54Z`
### last_modified_date : `2021-08-27T18:34:32Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70892
### status : `NEW`
### tags : `missed-optimization, ra`
### component : `rtl-optimization`
### version : `5.3.1`
### severity : `enhancement`
### contents :
Created attachment 38388
testcase

The attached reduced testcase is compiled differently if a simple raii helper type is used.

testcase:
    double array[expected];
    double sum = 0.0;
    for(int j = 0; j < expected; j++)
        array[j] = (double)j;

g++ -std=c++1y -O2 -Wall -Wextra -Werror double_bug_minimal.cc
  400950:	f2 0f 58 00          	addsd  (%rax),%xmm0
  400954:	48 83 c0 08          	add    $0x8,%rax
  400958:	48 39 d0             	cmp    %rdx,%rax
  40095b:	75 f3                	jne    400950 <main+0x70>

g++ -std=c++1y -O2 -Wall -Wextra -Werror -DA double_bug_minimal.cc
  400a98:	f2 0f 10 4c 24 08    	movsd  0x8(%rsp),%xmm1
  400a9e:	48 83 c0 08          	add    $0x8,%rax
  400aa2:	f2 0f 58 48 f8       	addsd  -0x8(%rax),%xmm1
  400aa7:	48 39 d0             	cmp    %rdx,%rax
  400aaa:	f2 0f 11 4c 24 08    	movsd  %xmm1,0x8(%rsp)
  400ab0:	75 e6                	jne    400a98 <main+0x78>


g++ --version | head -n1; cat /etc/fedora-release; uname -a
g++ (GCC) 5.3.1 20160406 (Red Hat 5.3.1-6)
Fedora release 23 (Twenty Three)
Linux lautreamont 4.4.7-300.fc23.x86_64 #1 SMP Wed Apr 13 02:52:52 UTC 2016 x86_64 x86_64 x86_64 GNU/Linux


---


### compiler : `gcc`
### title : `vectorized sin cos is wrongly optimized into scalar sincos`
### open_at : `2016-05-02T10:34:04Z`
### last_modified_date : `2023-08-05T03:38:25Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70901
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `5.3.1`
### severity : `enhancement`
### contents :
Created attachment 38390
testcase

As per title. Compile testcase with 

g++ -std=c++11 -O1 -fopenmp -ffast-math -march=ivybridge -mtune=ivybridge -o vector_sin_cos_to_scalar_sincos vector_sin_cos_to_scalar_sincos.cpp


---


### compiler : `gcc`
### title : `reassociation width needs to be aware of FMA, width of expression, and other architectural details`
### open_at : `2016-05-02T17:15:18Z`
### last_modified_date : `2021-09-06T18:40:21Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70912
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `7.0`
### severity : `normal`
### contents :
Created attachment 38395
test case

This is based on looking at trunk 235605 performance for ppc64le on a power8 system.

If you have an expression of the form

x = a*b+c*d+e*f+g*h ...

With reassociation width 1, you get a single multiply in front followed by a series of dependent multiply-adds. A natural consequence of doing reassociation with width > 1 is that you need to peel additional multiplies off of the front and do additional adds at the end to bring together the final result. But if you have too few overall terms, the cost of additional serialization vs the fused multipy add eats up the gain you might get from the parallelism in the middle.

Some real numbers for this compiler and power8, using --param tree-reassoc-width=N to set the max width. Rows are width 1,2,4 and columns are increasing numbers of terms i.e. "a*b+c*d" would be 4 terms. Table values are reduction in runtime.

	8	12	16	32
1	0.00%	0.00%	0.00%	0.00%
2	-3.37%	4.34%	8.62%	22.83%
4			14.53%	31.47%

So for this arch we do not want to do this at all for the FMA case unless we have at least 10 or 12 total terms. Looking at the reassoc pass output showed it did not try more than width=2 for 8 or 12 terms.

I ran into this when putting together a reassociation_width function for the rs6000 config. I couldn't see a way to avoid this behavior.

Another issue is that this is another place where we might want to modify behavior based on local register pressure. We don't want to introduce a bunch of new temps to do the parallel reassociation only to end up being unable to allocate them.


---


### compiler : `gcc`
### title : `[9 regression] Cross-module inlining for functions having argument passed by reference is no longer working.`
### open_at : `2016-05-03T18:18:26Z`
### last_modified_date : `2022-05-27T08:04:30Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70929
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `lto`
### version : `6.1.0`
### severity : `normal`
### contents :
$ cat a.C
struct s
{
  int a;
  s() {a=1;}
  ~s() {}
};
int t(struct s s);
int main()
{
  s s;
  int v=t(s);
  if (!__builtin_constant_p (v))
    __builtin_abort ();
  return 0;
}
$ cat b.C
struct s
{
  int a;
  s() {a=1;}
  ~s() {}
};
int t(struct s s)
{
  return s.a;
}
$ gcc-4.6 -O3 -flto a.C b.C
$ ./a.out
$ /aux/hubicka/trunk-install/bin/gcc -O3 -flto a.C b.C
$ ./a.out
Aborted


---


### compiler : `gcc`
### title : `Bad interaction between IVOpt and loop unrolling`
### open_at : `2016-05-04T12:04:38Z`
### last_modified_date : `2023-05-16T23:06:20Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70946
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `7.0`
### severity : `enhancement`
### contents :
IVOpt chooses between using indexing for induction variables or incrementing pointers. Due to way loop unrolling works, a decision that is optimal if unrolling is disabled may become very non-optimal with unrolling.

Below are simple examples that show how the choice to use indexing can become a very bad idea when unrolled, while using offset addressing leads to very decent code. To improve this we either to teach IVOpt about unrolling (eg. prioritise base+offset addressing) or add a tree unroller that unrolls small inner loops before IVOpt.


void loop1 (int *p, int *q, int i)
{
   for (i = 0; i < 1000; i++) p[i] = q[i] + 1;
}

void loop2 (int *p, int i)
{
   for (i = 0; i < 1000; i++) p[i] = p[i] + 1;
}

On AArch64 with -O2 -funroll-loops this gives:

loop1:
        mov     x2, 0
        .p2align 2
.L41:
        ldr     w4, [x1, x2]
        add     x3, x2, 4
        add     x10, x2, 8
        add     x9, x2, 12
        add     w5, w4, 1
        str     w5, [x0, x2]
        add     x8, x2, 16
        add     x7, x2, 20
        add     x6, x2, 24
        add     x11, x2, 28
        ldr     w12, [x1, x3]
        add     x2, x2, 32
        cmp     x2, 4000
        add     w13, w12, 1
        str     w13, [x0, x3]
        ldr     w14, [x1, x10]
        add     w15, w14, 1
        str     w15, [x0, x10]
        ldr     w16, [x1, x9]
        add     w17, w16, 1
        str     w17, [x0, x9]
        ldr     w18, [x1, x8]
        add     w4, w18, 1
        str     w4, [x0, x8]
        ldr     w3, [x1, x7]
        add     w10, w3, 1
        str     w10, [x0, x7]
        ldr     w9, [x1, x6]
        add     w5, w9, 1
        str     w5, [x0, x6]
        ldr     w8, [x1, x11]
        add     w7, w8, 1
        str     w7, [x0, x11]
        bne     .L41
        ret
loop2:
        add     x6, x0, 4000
        .p2align 2
.L51:
        mov     x1, x0
        ldr     w2, [x0]
        add     x0, x0, 32
        add     w3, w2, 1
        cmp     x0, x6
        str     w3, [x1], 4
        ldr     w4, [x0, -28]
        add     w5, w4, 1
        str     w5, [x0, -28]
        ldr     w7, [x1, 4]
        add     w8, w7, 1
        str     w8, [x1, 4]
        ldp     w9, w10, [x0, -20]
        ldp     w11, w12, [x0, -12]
        add     w14, w9, 1
        ldr     w13, [x0, -4]
        add     w15, w10, 1
        add     w16, w11, 1
        add     w17, w12, 1
        add     w18, w13, 1
        stp     w14, w15, [x0, -20]
        stp     w16, w17, [x0, -12]
        str     w18, [x0, -4]
        bne     .L51
        ret


---


### compiler : `gcc`
### title : `Regrename ignores preferred_rename_class`
### open_at : `2016-05-05T12:55:16Z`
### last_modified_date : `2021-08-27T06:16:27Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70961
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `7.0`
### severity : `normal`
### contents :
When deciding which register to use regrename.c calls the target function preferred_rename_class. However in pass 2 in find_rename_reg it then just ignores this preference. This results in significantly increased codesize on targets which prefer a subset of allocatable registers in order to use smaller instructions.

Also the computed super_class appears to be the union of all uses and defs instead of the intersection. This should be the intersection as that is the set of registers that all uses and defs support. 

If the preferred class doesn't result in a valid rename then it could search a wider class, but then it would need to check that the size of the newly selected patterns does not increase.


---


### compiler : `gcc`
### title : `[6 Regression] Redundant sign extension with conditional __builtin_clzl`
### open_at : `2016-05-09T08:42:07Z`
### last_modified_date : `2023-09-21T13:55:19Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=71016
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `6.1.0`
### severity : `normal`
### contents :
Consider:
long int foo (long i)
{
  return (i == 0) ? 17 : __builtin_clzl (i);
}

On aarch64 with GCC 5 at -O2 we generate:
foo:
        mov     x2, 17
        clz     x1, x0
        cmp     x0, xzr
        csel    x0, x1, x2, ne
        ret

whereas with GCC 6 and trunk we generate:
foo:
        mov     w1, 17
        clz     x2, x0
        cmp     x0, 0
        csel    w0, w1, w2, eq
        sxtw    x0, w0  //redundant sign-extend
        ret


In GCC 5 the tree structure being expanded is:

  i.1_3 = (long unsigned int) i_2(D);
  _4 = __builtin_clzl (i.1_3);
  iftmp.0_5 = (long int) _4;

;;   basic block 4, loop depth 0
;;    pred:       3
;;                2
  # iftmp.0_1 = PHI <iftmp.0_5(3), 17(2)>
  return iftmp.0_1;

so the RTL optimisers see the DI mode clz followed by a subreg and
a sign-extend and optimise it away.

However trunk now moves the sign-extend out of the conditional:
  i.1_3 = (long unsigned int) i_2(D);
  _4 = __builtin_clzl (i.1_3);

;;   basic block 4, loop depth 0
;;    pred:       3
;;                2
  # _7 = PHI <_4(3), 17(2)>
  prephitmp_8 = (long int) _7;
  return prephitmp_8;

So it's very hard for RTL ifcvt or combine or ree to catch it.


---


### compiler : `gcc`
### title : `GCC prefers register moves over move immediate`
### open_at : `2016-05-09T13:34:03Z`
### last_modified_date : `2021-08-14T02:48:18Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=71022
### status : `NEW`
### tags : `missed-optimization, ra`
### component : `rtl-optimization`
### version : `7.0`
### severity : `enhancement`
### contents :
When assigning the same immediate value to different registers, GCC will always CSE the immediate and emit a register move for subsequent uses. This creates unnecessary register dependencies and increases latency. When the cost of an immediate move is the same as a register move (which should be true for most targets), it should prefer the former. A register move is better only when the immediate requires multiple instructions or is larger with -Os.

It's not obvious where this is best done. The various cprop phases before IRA do the right thing, but cse2 (which runs later) then undoes it. And cprop_hardreg doesn't appear to be able to deal with immediates.

int f1(int x)
{
  int y = 1, z = 1;
  while (x--)
    {
      y += z;
      z += x;
    }
  return y + z;
}

void g(float, float);
void f2(void) { g(1.0, 1.0); g(3.3, 3.3); }

On AArch64 I get:

f1:
	sub	w1, w0, #1
	cbz	w0, .L12
	mov	w0, 1
	mov	w2, w0     *** mov w2, 1
	.p2align 2
.L11:
	add	w2, w2, w0
	add	w0, w0, w1
	sub	w1, w1, #1
	cmn	w1, #1
	bne	.L11
	add	w0, w2, w0
	ret
.L12:
	mov	w0, 2
	ret

f2:
	fmov	s1, 1.0e+0
	str	x30, [sp, -16]!
	fmov	s0, s1    *** fmov s0, 1.0
	bl	g
	adrp	x0, .LC1
	ldr	x30, [sp], 16
	ldr	s1, [x0, #:lo12:.LC1]
	fmov	s0, s1    *** ldr s0, [x0, #:lo12:.LC1] 
	b	g


---


### compiler : `gcc`
### title : `Missing division optimizations`
### open_at : `2016-05-09T16:08:15Z`
### last_modified_date : `2019-06-17T15:29:05Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=71026
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `7.0`
### severity : `enhancement`
### contents :
With -Ofast GCC doesn't reassociate constant multiplies or negates away from divisors to allow for more reciprocal division optimizations. It is also possible to avoid divisions (or multiplies) involving immediates in comparisons that check for a positive/negative result.

float f1(float x, float y) { return x / (y * y); }    // -> x * (1/y) * (1/y)
float f2(float x, float y) { return x / (y * 3.0f); } // -> (x/3) / y
float f3(float x, float y) { return x / -y; }         // -> (-x) / y
int f4(float x) { return (1.0f / x) < 0.0f; }         // -> x < 0.0f
int f5(float x) { return (x / 2.0f) <= 0.0f; }        // -> x <= 0.0f

A quick experiment shows the first transformation could remove almost 100 divisions from SPEC2006, the 2nd 50. The first transformation is only useful if there is at least one other division by y, so likely best done in the division reciprocal optimization phase.


---


### compiler : `gcc`
### title : `abs(f) u>= 0. is always true`
### open_at : `2016-05-09T21:18:51Z`
### last_modified_date : `2023-05-02T05:14:21Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=71034
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `7.0`
### severity : `enhancement`
### contents :
A very simple missed optimization, we optimize abs(x)<0 to false (in forwprop, haven't found the exact place yet) but not abs(x) u>= 0 to true. I noticed it because cdce now produces this comparison for sqrt, which causes a small regression on a dead sqrt(abs(x)).

int f(double x){
  x=__builtin_fabs(x);
  // return x<0;
  return !__builtin_isless(x,0);
}


---


### compiler : `gcc`
### title : `Compiler reports "loop vectorized" but actually  it was not`
### open_at : `2016-05-11T09:20:04Z`
### last_modified_date : `2019-03-04T12:58:59Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=71060
### status : `ASSIGNED`
### tags : `alias, missed-optimization`
### component : `tree-optimization`
### version : `5.3.1`
### severity : `normal`
### contents :
Created attachment 38467
The test case to reproduce the problem

I compile the attached test8.c as follows:

/usr/local/bin/gcc   -O3 -S -mavx -fopt-info-vec-optimized -DSCOUT -Wall -Wextra -Werror -Wno-unknown-pragmas test8.c -o test8.s3

The output is:

test8.c:24:2: note: loop vectorized
test8.c:24:2: note: loop versioned for vectorization because of possible aliasing

But the resulting assembler code contains no vector instructions. 

Other problems related to this test are:

1. The pointers in this function has the restrict specifier, so there should be no loop versioning.

2. I tried to use -ftree-loop-if-convert-stores but it did not help.

Possibly this bug is the same as 65206.


---


### compiler : `gcc`
### title : `[i386, AVX-512, Perf] vpermi2ps instead of vpermps emitted`
### open_at : `2016-05-12T13:20:16Z`
### last_modified_date : `2021-08-15T07:06:37Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=71088
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `7.0`
### severity : `normal`
### contents :
Testcase:

float foo (float *arr1, float *arr2, float *max_x, int M, float s)
{
  float *res = new float[M];

  for (int i = M - 1; i >= 0; i--)
    for (int j = 0; j <= i; j++)
      {
        float x = arr1[j] * arr2[i - j] + s;
        res[j] = x > max_x[j] ? x : max_x[j];
      }

  return res[0];
}

To reproduce:

$ g++ -S test.cpp -Ofast -funroll-loops -march=knl

GCC emits vpermi2ps instruction to rearrange elements of arr2 backwards, however
this instruction writes the result into the index register, therefore there are
additional movs before each vpermi2ps to restore indexes [1].
Also there are some weird movs after each vpermi2ps [2].  It's not clear why the
result from vpermi2ps isn't passed directly to vfmadd132ps.

.L1:
        vmovups       (%r11), %zmm9
        vmovdqa64     %zmm2, %zmm1                  # [1]
        vpermi2ps     %zmm9, %zmm9, %zmm1
        vmovdqa64     %zmm2, %zmm16                 # [1]
        vmovaps       %zmm1, %zmm10                 # [2]
        vmovdqa64     %zmm2, %zmm1                  # [1]
        vmovups       -64(%r11), %zmm12
        vfmadd132ps   (%rax,%r9), %zmm3, %zmm10
        vpermi2ps     %zmm12, %zmm12, %zmm1
        vmaxps        (%rcx,%r9), %zmm10, %zmm11
        vmovaps       %zmm1, %zmm13                 # [2]
        vmovdqa64     %zmm2, %zmm1                  # [1]
        vmovups       -128(%r11), %zmm15
        vfmadd132ps   64(%rax,%r9), %zmm3, %zmm13
        vmovups       -192(%r11), %zmm6
        vpermi2ps     %zmm15, %zmm15, %zmm1
        vpermi2ps     %zmm6, %zmm6, %zmm16
        vmovaps       %zmm1, %zmm4                  # [2]
        vmovaps       %zmm16, %zmm7                 # [2]
        vmaxps        64(%rcx,%r9), %zmm13, %zmm14
        vfmadd132ps   128(%rax,%r9), %zmm3, %zmm4
        vfmadd132ps   192(%rax,%r9), %zmm3, %zmm7
        vmaxps        128(%rcx,%r9), %zmm4, %zmm5
        leal          4(%r15), %r15d
        vmaxps        192(%rcx,%r9), %zmm7, %zmm8
        cmpl          %esi, %r15d
        vmovups       %zmm11, (%r8,%r9)
        leaq          -256(%r11), %r11
        vmovups       %zmm14, 64(%r8,%r9)
        vmovups       %zmm5, 128(%r8,%r9)
        vmovups       %zmm8, 192(%r8,%r9)
        leaq          256(%r9), %r9
        jb            .L1

Instead of this, vpermps can be used.  It doesn't overwrite the index register,
what allows to get rid of 8 movs in this loop:

.L2:
        lea           (,%r12,4), %r10
        negq          %r10
        addq          %rbx, %r10
        vpermps       -64(%r10), %zmm3, %zmm4
        vpermps       -128(%r10), %zmm3, %zmm6
        vpermps       -192(%r10), %zmm3, %zmm8
        vpermps       -256(%r10), %zmm3, %zmm10
        vfmadd132ps   (%r11,%r12,4), %zmm2, %zmm4
        vfmadd132ps   64(%r11,%r12,4), %zmm2, %zmm6
        vfmadd132ps   128(%r11,%r12,4), %zmm2, %zmm8
        vfmadd132ps   192(%r11,%r12,4), %zmm2, %zmm10
        vmaxps        (%r13,%r12,4), %zmm4, %zmm5
        vmovups       %zmm5, (%rdi,%r12,4)
        vmaxps        64(%r13,%r12,4), %zmm6, %zmm7
        vmovups       %zmm7, 64(%rdi,%r12,4)
        vmaxps        128(%r13,%r12,4), %zmm8, %zmm9
        vmovups       %zmm9, 128(%rdi,%r12,4)
        vmaxps        192(%r13,%r12,4), %zmm10, %zmm11
        vmovups       %zmm11, 192(%rdi,%r12,4)
        addq          $64, %r12
        cmpq          %rax, %r12
        jb            .L2


---


### compiler : `gcc`
### title : `Adding "const" to value in constexpr constructor places const object in .bss instead of .rodata`
### open_at : `2016-05-14T10:15:22Z`
### last_modified_date : `2021-08-10T03:52:34Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=71113
### status : `NEW`
### tags : `missed-optimization`
### component : `c++`
### version : `6.1.1`
### severity : `normal`
### contents :
Take a look at following test case:

-- >8 -- >8 -- >8 -- >8 -- >8 -- >8 -- >8 -- >8 --

class X
{
public:

	constexpr X(void* pointer) :
		pointer_{pointer}
	{

	}

private:

	void* pointer_;
};

#define PERIPHERAL1	(void*)0x20000000
const X xxx {PERIPHERAL1};

int main()
{

}

-- >8 -- >8 -- >8 -- >8 -- >8 -- >8 -- >8 -- >8 --

Execute test:

-- >8 -- >8 -- >8 -- >8 -- >8 -- >8 -- >8 -- >8 --

$ g++ test.cpp && objdump -x --syms --demangle a.out | grep xxx
0000000000400608 l     O .rodata	0000000000000008              xxx

-- >8 -- >8 -- >8 -- >8 -- >8 -- >8 -- >8 -- >8 --

Everything's fine. Now just add one trivial change, which does _NOT_ change any logic (at least in my opinion (; ). Replace:

	constexpr X(void* pointer) :

with

	constexpr X(void* const pointer) :

And the object is placed in .bss, not in .rodata...

-- >8 -- >8 -- >8 -- >8 -- >8 -- >8 -- >8 -- >8 --

$ g++ test.cpp && objdump -x --syms --demangle a.out | grep xxx
0000000000600a58 l     O .bss	0000000000000008              xxx

-- >8 -- >8 -- >8 -- >8 -- >8 -- >8 -- >8 -- >8 --

There's no problem if an address of "real" object is used, so for example something like this works fine in both cases:

-- >8 -- >8 -- >8 -- >8 -- >8 -- >8 -- >8 -- >8 --

int something;
const X xxx {&something};

-- >8 -- >8 -- >8 -- >8 -- >8 -- >8 -- >8 -- >8 --

The use case may seem a bit strange, but the macro definition like the one used in the example is used commonly in hardware headers for microcontrollers. They usually look like this:

-- >8 -- >8 -- >8 -- >8 -- >8 -- >8 -- >8 -- >8 --

#define PERIPH_BASE           ((uint32_t)0x40000000U)
#define APB2PERIPH_BASE       (PERIPH_BASE + 0x00010000U)
#define USART1_BASE           (APB2PERIPH_BASE + 0x1000U)
#define USART1              ((USART_TypeDef *) USART1_BASE)

-- >8 -- >8 -- >8 -- >8 -- >8 -- >8 -- >8 -- >8 --

(USART_TypeDef is a typedef of an anonymous struct with layout of peripheral registers)

The behaviour was noticed in GCC compiled for "arm-none-eabi-", version 5.3.1, but the same thing happens in a desktop version 6.1.1 on Arch Linux.


---


### compiler : `gcc`
### title : `[11/12/13/14 Regression] ftois instruction not emitted for float -> int bitcast`
### open_at : `2016-05-14T23:31:03Z`
### last_modified_date : `2023-07-07T10:31:23Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=71118
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `5.3.0`
### severity : `normal`
### contents :
Created attachment 38490
ftois.c

For the attached ftois.c, gcc-4.9.3 -O2 -mcpu=ev67 emits

0000000000000000 <f2i>:
   0:   01 0f 1f 72     ftois   $f16,t0
   4:   00 00 e1 43     sextl   t0,v0
   8:   01 80 fa 6b     ret
   c:   00 00 fe 2f     unop

0000000000000010 <f2l>:
  10:   01 0f 1f 72     ftois   $f16,t0
  14:   20 f6 21 48     zapnot  t0,0xf,v0
  18:   01 80 fa 6b     ret
  1c:   00 00 fe 2f     unop


while gcc-5.3.0 -O2 -mcpu=ev67 emits

0000000000000000 <f2i>:
   0:   f0 ff de 23     lda     sp,-16(sp)
   4:   00 00 1e 9a     sts     $f16,0(sp)
   8:   00 00 1e a0     ldl     v0,0(sp)
   c:   10 00 de 23     lda     sp,16(sp)
  10:   01 80 fa 6b     ret
  14:   00 00 fe 2f     unop
  18:   1f 04 ff 47     nop
  1c:   00 00 fe 2f     unop

0000000000000020 <f2l>:
  20:   01 0f 1f 72     ftois   $f16,t0
  24:   20 f6 21 48     zapnot  t0,0xf,v0
  28:   01 80 fa 6b     ret
  2c:   00 00 fe 2f     unop

In fact, the alpha architecture reference says that ftois is exactly equivalent to an sts/ldl sequence.

f2i should have used ftois, as with gcc-4.9.3.


---


### compiler : `gcc`
### title : `[11/12/13/14 Regression] ftoit instruction not emitted for double -> long bitcast`
### open_at : `2016-05-14T23:35:54Z`
### last_modified_date : `2023-07-07T10:31:25Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=71119
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.9.3`
### severity : `normal`
### contents :
Created attachment 38491
ftoit.c

For the attached ftoit.c, gcc-4.8.5 -O2 -mcpu=ev67 emits

0000000000000000 <f2i>:
   0:   00 0e 1f 72     ftoit   $f16,v0
   4:   00 00 e0 43     sextl   v0,v0
   8:   01 80 fa 6b     ret
   c:   00 00 fe 2f     unop

0000000000000010 <f2l>:
  10:   00 0e 1f 72     ftoit   $f16,v0
  14:   01 80 fa 6b     ret
  18:   1f 04 ff 47     nop
  1c:   00 00 fe 2f     unop

while gcc-4.9.3/gcc-5.3.0 -O2 -mcpu=ev67 emits

0000000000000000 <f2i>:
   0:   00 0e 1f 72     ftoit   $f16,v0
   4:   00 00 e0 43     sextl   v0,v0
   8:   01 80 fa 6b     ret
   c:   00 00 fe 2f     unop

0000000000000010 <f2l>:
  10:   f0 ff de 23     lda     sp,-16(sp)
  14:   00 00 1e 9e     stt     $f16,0(sp)
  18:   00 00 1e a4     ldq     v0,0(sp)
  1c:   10 00 de 23     lda     sp,16(sp)
  20:   01 80 fa 6b     ret
  24:   00 00 fe 2f     unop
  28:   1f 04 ff 47     nop
  2c:   00 00 fe 2f     unop

In fact, the alpha architecture reference says that ftoit is exactly equivalent to an stt/ldq sequence.

f2l should have used ftoit, as with gcc-4.8.5.


---


### compiler : `gcc`
### title : `missing modulo 2 optimization converting result to bool`
### open_at : `2016-05-16T16:33:22Z`
### last_modified_date : `2021-08-18T05:37:32Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=71149
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `7.0`
### severity : `enhancement`
### contents :
One would expect GCC to emit comparably efficient code for all three functions below, but it only does so for odd_mod and odd_and but not for the equivalent odd_mod_cvt function.  Clang emits the same optimal code for all three functions.

$ cat xxx.cpp && /build/gcc-trunk-svn/gcc/xgcc -B /build/gcc-trunk-svn/gcc -Dbool=_Bool -O2 -S -Wall -Wextra -fdump-tree-optimized=/dev/stdout -o/dev/null -xc xxx.cpp
int odd_mod (int a) {
    return (a % 2) != 0;
}

_Bool odd_mod_cvt (int a) {
    return a % 2;
}

int odd_and (int a) {
    return (a & 1) != 0;
}


;; Function odd_mod (odd_mod, funcdef_no=0, decl_uid=1745, cgraph_uid=0, symbol_order=0)

odd_mod (int a)
{
  int _1;

  <bb 2>:
  _1 = a_4(D) & 1;
  return _1;

}



;; Function odd_mod_cvt (odd_mod_cvt, funcdef_no=1, decl_uid=1748, cgraph_uid=1, symbol_order=1)

odd_mod_cvt (int a)
{
  int _1;
  _Bool _3;

  <bb 2>:
  _1 = a_2(D) % 2;
  _3 = _1 != 0;
  return _3;

}



;; Function odd_and (odd_and, funcdef_no=2, decl_uid=1751, cgraph_uid=2, symbol_order=2)

odd_and (int a)
{
  int _1;

  <bb 2>:
  _1 = a_3(D) & 1;
  return _1;

}


---


### compiler : `gcc`
### title : `aarch64 LSE __atomic_fetch_and() generates inversion for constants`
### open_at : `2016-05-16T21:26:17Z`
### last_modified_date : `2022-01-28T00:45:34Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=71153
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `6.1.1`
### severity : `enhancement`
### contents :
Compiling this code:

static __always_inline
void clear_bit_unlock(long bit, volatile unsigned long *addr)
{
	unsigned long mask = 1UL << (bit & (64 - 1));
	addr += bit >> 6;
	__atomic_fetch_and(addr, ~mask, __ATOMIC_RELEASE);
}

void bar_clear_bit_unlock(unsigned long *p)
{
	clear_bit_unlock(22, p);
}

for aarch64-linux-gnu with "-march=armv8-a+lse -Os" generates a double negation of the mask value in the assembly:

000000000000007c <bar_clear_bit_unlock>:
  7c:   92a00801        mov     x1, #0xffffffffffbfffff         // #-4194305
  80:   aa2103e1        mvn     x1, x1
  84:   f8611001        ldclrl  x1, x1, [x0]
  88:   d65f03c0        ret

The instruction at 7c is loading an inverted value into x1 (it's actually a MOVN instruction according to the opcode table that I can find); the value in x1 is then inverted *again* by the MVN instruction.

Now, I can't find a description of how the LDCLRL instruction works, so I can't say that it doesn't invert the parameter a third time (ie. apply an A AND-NOT B operation), but it looks suspicious.  If nothing else, the MOVN and MOV could be condensed into just a MOV.

If a parameter is used instead of a constant:

void foo_clear_bit_unlock(long bit, unsigned long *p)
{
	clear_bit_unlock(bit, p);
}

then two MVN instructions are generated:

0000000000000048 <foo_clear_bit_unlock>:
  48:   12001403        and     w3, w0, #0x3f
  4c:   9346fc02        asr     x2, x0, #6
  50:   d2800020        mov     x0, #0x1                        // #1
  54:   8b020c21        add     x1, x1, x2, lsl #3
  58:   9ac32000        lsl     x0, x0, x3
  5c:   aa2003e0        mvn     x0, x0
  60:   aa2003e2        mvn     x2, x0
  64:   f8621022        ldclrl  x2, x2, [x1]
  68:   d65f03c0        ret

The C code appears to be correct, because on x86_64 it generates:

000000000000004c <bar_clear_bit_unlock>:
  4c:   f0 48 81 27 ff ff bf    lock andq $0xffffffffffbfffff,(%rdi)
  53:   ff 
  54:   c3                      retq


---


### compiler : `gcc`
### title : `powerpc64 __atomics should produce hinted bne- after stdcx.`
### open_at : `2016-05-17T12:50:06Z`
### last_modified_date : `2022-03-08T16:21:00Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=71162
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `target`
### version : `6.1.1`
### severity : `enhancement`
### contents :
On powerpc64, __atomic_fetch_or(), for example, emits a BNE instruction after the STDCX. instruction to work out whether it needs to retry.  For example, compiling this:

static __always_inline
bool iso_test_and_set_bit(long bit, volatile unsigned long *addr, int memorder)
{
	unsigned long mask = 1UL << (bit & (64 - 1));
	unsigned long old;

	addr += bit >> 6;
	old = __atomic_fetch_or(addr, mask, memorder);
	return old & mask;
}

long iso_t_a_s(long bit, volatile unsigned long *addr)
{
	return iso_test_and_set_bit(bit, addr, __ATOMIC_SEQ_CST);
}

produces this:

00000000000000e4 <.iso_t_a_s>:
  e4:   7c 00 04 ac     hwsync
  e8:   54 6a 06 be     clrlwi  r10,r3,26
  ec:   7c 63 36 74     sradi   r3,r3,6
  f0:   39 20 00 01     li      r9,1
  f4:   78 63 1f 24     rldicr  r3,r3,3,60
  f8:   7d 29 50 36     sld     r9,r9,r10
  fc:   7c 84 1a 14     add     r4,r4,r3
 100:   7c 60 20 a8     ldarx   r3,0,r4
 104:   7c 6a 4b 78     or      r10,r3,r9
 108:   7d 40 21 ad     stdcx.  r10,0,r4
 10c:   40 82 ff f4     bne     100 <.iso_t_a_s+0x1c>
 110:   4c 00 01 2c     isync
 114:   7d 29 18 38     and     r9,r9,r3
 118:   30 69 ff ff     addic   r3,r9,-1
 11c:   7c 63 49 10     subfe   r3,r3,r9
 120:   4e 80 00 20     blr

with gcc-6.1.1 targetted at powerpc64-linux-gnu and -Os.

Hopefully the need to retry is unlikely, so BNE- should probably be emitted rather than BNE.


---


### compiler : `gcc`
### title : `std::array with aggregate initialization generates huge code`
### open_at : `2016-05-17T16:22:19Z`
### last_modified_date : `2021-11-25T23:53:06Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=71165
### status : `RESOLVED`
### tags : `compile-time-hog, missed-optimization`
### component : `c++`
### version : `5.3.1`
### severity : `enhancement`
### contents :
[mostly copied from a thread on stackoverflow at http://stackoverflow.com/questions/37260097]

This code takes several seconds to compile and produces a 52,776 byte executable:

#include <array>
#include <iostream>

int main()
{
    constexpr std::size_t size = 4096;

    struct S
    {
        float f;
        S() : f(0.0f) {}
    };

    std::array<S, size> a = {};  // <-- note aggregate initialization

    for (auto& e : a)
        std::cerr << e.f;

    return 0;
}

Increasing 'size' seems to increase compilation time and executable size linearly. I cannot reproduce this behaviour with either clang 3.5 or Visual C++ 2015. Using -Os makes no difference. I've reproduced this on g++ 4.9.2 and 5.3.1, but 6.1 also seems to do the same thing.

$ time g++ -O2 -std=c++11 test.cpp
real    0m4.178s
user    0m4.060s
sys     0m0.068s

Inspecting the assembly code reveals that the initialization of 'a' is unrolled, generating 4096 movl instructions:

main:
.LFB1313:
    .cfi_startproc
    pushq   %rbx
    .cfi_def_cfa_offset 16
    .cfi_offset 3, -16
    subq    $16384, %rsp
    .cfi_def_cfa_offset 16400
    movl    $0x00000000, (%rsp)
    movl    $0x00000000, 4(%rsp)
    movq    %rsp, %rbx
    movl    $0x00000000, 8(%rsp)
    movl    $0x00000000, 12(%rsp)
    movl    $0x00000000, 16(%rsp)

       [...skipping 4000 lines...]

    movl    $0x00000000, 16376(%rsp)
    movl    $0x00000000, 16380(%rsp)

This only happens when T has a non-trivial constructor and the array is initialized using {}. If I do any of the following, g++ generates a simple loop:

 1) Remove S::S();
 2) Remove S::S() and initialize S::f in-class;
 3) Remove the aggregate initialization (= {});
 4) Compile without -O2.

Bugs 59659, 56671 may be relevant. In particular, some of the test cases in bug 59659 seem to still be failing.


---


### compiler : `gcc`
### title : `SLP loop vectorized twice`
### open_at : `2016-05-25T07:55:16Z`
### last_modified_date : `2022-12-19T21:19:18Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=71271
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `7.0`
### severity : `enhancement`
### contents :
Created attachment 38559
Vectorizer pass output

Consider the following code, compiled with -O3 -fno-common:

__attribute__ ((noinline)) int
liveloop (int start, int n, int *x, int *y)
{
  int i = start;
  int n0, n1, n2, n3;
  int j;

  for (j = 0; j < n; ++j)
    {
      i += 1;
      n0 = x[(j*4)];
      n1 = x[(j*4)+1];
      n2 = x[(j*4)+2];
      n3 = x[(j*4)+3];
      y[(j*4)] = n0 +1;
      y[(j*4)+1] = n1 +2;
      y[(j*4)+2] = n2 +7;
      y[(j*4)+3] = n3 +9;
    }
  return 0;
}


The vectorizer pass will split the loop using versioning (due to alias dependencies). One version will be vectorized using SLP, the second will be kept in scalar form.

However, the slp1 pass will then SLP vectorize the second scalar loop.

This results in the final assembler output containing two versions of the loop, both of which are vectorized and are almost identical.

Whilst (i think) the code is correct, the code is not ideal.

Tested on x86 and aarch64.


---


### compiler : `gcc`
### title : `unnecessary call to __strcat_chk emitted after buffer reset`
### open_at : `2016-05-28T00:02:28Z`
### last_modified_date : `2022-03-17T20:20:01Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=71319
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `7.0`
### severity : `normal`
### contents :
Similar to bug 71304, in the following test case, since the string in the destination buffer is truncated at a known offset after it has been copied there by the checked call, the subsequent strcat call doesn't need to expand to a checked call because there is enough space in the buffer to append the source string to its contents.  GCC performs this optimization in the first test case (function f) when the string a truncated by calling strcpy, but it doesn't do the same thing when the string is truncated by inserting a NUL into the same position.

$ cat strcat.c && /home/msebor/build/gcc-6-branch/gcc/xgcc -B/home/msebor/build/gcc-6-branch/gcc -O2 -S -fdump-tree-optimized=/dev/stdout strcat.c
#define strcat(d, s)\
  __builtin___strcat_chk (d, s, __builtin_object_size (d, 0))

#define strcpy(d, s) \
  __builtin___strcpy_chk (d, s, __builtin_object_size (d, 0))

void sink (const char*);

int f (const char *s)
{
  char a [4] = "1";
  strcat (a, "2");   // safe
  strcat (a, s);     // must be checked

  strcpy (a, "1");
  strcat (a, "3");   // safe

  sink (a);
}

int g (const char *s)
{
  char a [4] = "1";
  strcat (a, "2");   // safe
  strcat (a, s);     // must be checked

  a [1] = '\0';
  strcat (a, "3");   // safe but checked (missing optimization)

  sink (a);
}


;; Function f (f, funcdef_no=0, decl_uid=1758, cgraph_uid=0, symbol_order=0)

f (const char * s)
{
  char a[4];

  <bb 2>:
  a = "1";
  __builtin___strcpy_chk (&MEM[(void *)&a + 2B], s_4(D), 4);
  MEM[(char * {ref-all})&a] = 49;
  __builtin_memcpy (&MEM[(void *)&a + 1B], "3", 2);
  sink (&a);
  a ={v} {CLOBBER};
  return;

}



;; Function g (g, funcdef_no=1, decl_uid=1762, cgraph_uid=1, symbol_order=1)

g (const char * s)
{
  char a[4];

  <bb 2>:
  a = "1";
  __builtin___strcpy_chk (&MEM[(void *)&a + 2B], s_4(D), 4);
  a[1] = 0;
  __builtin___strcat_chk (&a, "3", 4);
  sink (&a);
  a ={v} {CLOBBER};
  return;

}


---


### compiler : `gcc`
### title : `[6 Regression] x86: worse code for uint8_t % 10 and / 10`
### open_at : `2016-05-28T02:37:34Z`
### last_modified_date : `2021-09-15T08:12:55Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=71321
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `6.1.0`
### severity : `normal`
### contents :
If we have an integer (0..99), we can modulo and divide by 10 to get two decimal digits, then convert to a pair of ASCII bytes with a newline by adding `00\n`.   When replacing div and mod with a multiplicative inverse, gcc 6.1 uses more instructions than gcc 5.3, due to poor choices.

See also https://godbolt.org/g/vvS5J6

#include <stdint.h>
// assuming little-endian
__attribute__((always_inline)) 
unsigned cvt_to_2digit(uint8_t i, uint8_t base) {
  return ((i / base) | (uint32_t)(i % base)<<8);
}
  // movzbl %dil,%eax    # 5.3 and 6.1, with -O3 -march=haswell
  // div    %sil
  // movzwl %ax,%eax

// at -Os, gcc uses a useless  AND eax, 0xFFF, instead of a movzx eax,ax.  I think to avoid partial-register stalls?
unsigned cvt_to_2digit_ascii(uint8_t i) {
  return cvt_to_2digit(i, 10) + 0x0a3030;    // + "00\n" converts to ASCII
}

Compiling with -O3 -march=haswell
        ## gcc 5.3                         ## gcc 6.1
        movzbl  %dil, %edx                 movzbl  %dil, %eax
        leal    (%rdx,%rdx,4), %ecx        leal    0(,%rax,4), %edx   # requires a 4B zero displacement
        leal    (%rdx,%rcx,8), %edx        movl    %eax, %ecx         # lea should let us avoid mov
        leal    (%rdx,%rdx,4), %edx        addl    %eax, %edx
                                           leal    (%rcx,%rdx,8), %edx
                                           leal    0(,%rdx,4), %eax   # requires a 4B zero displacement
                                           addl    %eax, %edx
        shrw    $11, %dx                   shrw    $11, %dx
        leal    (%rdx,%rdx,4), %eax        leal    0(,%rdx,4), %eax   # requires a 4B zero displacement.  gcc5.3 didn't use any of these
                                           addl    %edx, %eax
        movzbl  %dl, %edx                  movzbl  %dl, %edx       # same after this
        addl    %eax, %eax                 addl    %eax, %eax
        subl    %eax, %edi                 subl    %eax, %edi
        movzbl  %dil, %eax                 movzbl  %dil, %eax
        sall    $8, %eax                   sall    $8, %eax
        orl     %eax, %edx                 orl     %eax, %edx
        leal    667696(%rdx), %eax         leal    667696(%rdx), %eax

with -mtune=haswell, it's  prob. best to merge with   mov ah, dil  or something, rather than movzx/shift/or.  Haswell has no penalty for partial-registers, but still has partial-reg renaming to avoid false dependencies: the best of both worlds.



BTW, with -Os, both gcc versions compile it to

        movb    $10, %dl
        movzbl  %dil, %eax
        divb    %dl
        andl    $4095, %eax      # partial reg stall.  gcc does this even with -march=core2 where it matters
        addl    $667696, %eax

The AND appears to be totally useless, because the upper bytes of eax are already zero (from movzbl %dil, %eax before div).  I thought the movzbl %ax, %eax  in the unknown-divisor version was to avoid partial-register slowdowns, but maybe it's just based on the possible range of the result.

Off-topic, but I noticed this while writing FizzBuzz in asm.  http://stackoverflow.com/a/37494090/224132


---


### compiler : `gcc`
### title : `Suboptimal code generated for "(a & 1) ? (CST1 + CST2) : CST1"`
### open_at : `2016-05-29T22:23:47Z`
### last_modified_date : `2023-08-23T01:58:38Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=71336
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `6.0`
### severity : `enhancement`
### contents :
$ cat test.c
int test(int a) {
    return a & 1 ? 7 : 3;
}
$ gcc -O2 -o- -S test.c
test:
.LFB0:
        .cfi_startproc
        andl    $1, %edi
        cmpl    $1, %edi
        sbbl    %eax, %eax
        andl    $-4, %eax
        addl    $7, %eax
        ret
        .cfi_endproc

The optimal code would look like

        andl    $1, %edi
        leal    3(,%rdi,4), %eax
        ret


---


### compiler : `gcc`
### title : `missed optimization (can't "prove" shift and multiplication equivalence)`
### open_at : `2016-05-30T10:23:01Z`
### last_modified_date : `2023-01-15T19:05:58Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=71343
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `6.2.0`
### severity : `enhancement`
### contents :
this function

unsigned int test12(unsigned int a , unsigned int b)
{
  return ((a << 2) + (b << 2)) ==  a * 4 + b * 4;
}

cannot be reduced to "return 1;". Maybe here https://gcc.gnu.org/viewcvs/gcc/trunk/gcc/simplify-rtx.c?view=markup&pathrev=232689#l2118 needs to add something?

https://godbolt.org/g/vcEqe7 - here clang and ICC is able to reduce this, but not gcc


---


### compiler : `gcc`
### title : `Global constructors (init_array) emitted for trivial initialisation depending on source code ordering`
### open_at : `2016-06-02T12:31:10Z`
### last_modified_date : `2023-09-17T06:21:07Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=71384
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `c++`
### version : `5.3.1`
### severity : `normal`
### contents :
GCC versions 4.7.2/5.3.0/5.3.1 are emitting a global constructor (to the .init_array section) for the following piece of trivial code:

===

struct X
{
  constexpr X(int a);
  const int m_a;
};
X x(999);
inline constexpr X::X(int a):m_a(a) {}

===

Swapping the last two lines, i.e. placing the constructor implementation before the declaration of 'x', causes 'x' to be emitted to the '.data' section with value 999 instead. The latter is desirable as the generate binary is far smaller and does not require global constructors.

How to reproduce:

g++ -std=c++11 -c -save-temps=obj global-constructor.cxx

Occurs regardless of whether you specify -O0, -O1, -O2, -O3. In a complete program, -flto cannot resolve this. The issue occurs on both x86_64 and ARM, so not in the backend. Also occurs with -std=c++14 and -std=c++17 on GCC 5.3.x.

Compiler versions used:

$ g++ -###
Using built-in specs.
COLLECT_GCC=g++
COLLECT_LTO_WRAPPER=/usr/libexec/gcc/x86_64-redhat-linux/5.3.1/lto-wrapper
Target: x86_64-redhat-linux
Configured with: ../configure --enable-bootstrap --enable-languages=c,c++,objc,obj-c++,fortran,ada,go,lto --prefix=/usr --mandir=/usr/share/man --infodir=/usr/share/info --with-bugurl=http://bugzilla.redhat.com/bugzilla --enable-shared --enable-threads=posix --enable-checking=release --enable-multilib --with-system-zlib --enable-__cxa_atexit --disable-libunwind-exceptions --enable-gnu-unique-object --enable-linker-build-id --with-linker-hash-style=gnu --enable-plugin --enable-initfini-array --disable-libgcj --with-isl --enable-libmpx --enable-gnu-indirect-function --with-tune=generic --with-arch_32=i686 --build=x86_64-redhat-linux
Thread model: posix
gcc version 5.3.1 20160406 (Red Hat 5.3.1-6) (GCC)

$ ${CROSS_COMPILE}g++ -###
Using built-in specs.
COLLECT_GCC=/home/niels/workspace/toolchains/build/arm-none-eabi/output/bin/arm-none-eabi-g++
COLLECT_LTO_WRAPPER=/home/niels/workspace/toolchains/build/arm-none-eabi/output/libexec/gcc/arm-none-eabi/5.3.0/lto-wrapper
Target: arm-none-eabi
Configured with: /home/niels/workspace/toolchains/build/arm-none-eabi/work/src/gcc-5.3.0/configure --build=x86_64-build_pc-linux-gnu --host=x86_64-build_pc-linux-gnu --target=arm-none-eabi --prefix=/home/niels/workspace/toolchains/build/arm-none-eabi/output --with-local-prefix=/home/niels/workspace/toolchains/build/arm-none-eabi/output/arm-none-eabi/sysroot --with-sysroot=/home/niels/workspace/toolchains/build/arm-none-eabi/output/arm-none-eabi/sysroot --with-newlib --enable-threads=no --disable-shared --with-float=soft --with-pkgversion='crosstool-NG crosstool-ng-1.22.0-134-ge1d494a' --enable-__cxa_atexit --disable-libgomp --disable-libmudflap --disable-libssp --disable-libquadmath --disable-libquadmath-support --with-gmp=/home/niels/workspace/toolchains/build/arm-none-eabi/work/arm-none-eabi/buildtools --with-mpfr=/home/niels/workspace/toolchains/build/arm-none-eabi/work/arm-none-eabi/buildtools --with-mpc=/home/niels/workspace/toolchains/build/arm-none-eabi/work/arm-none-eabi/buildtools --with-isl=/home/niels/workspace/toolchains/build/arm-none-eabi/work/arm-none-eabi/buildtools --enable-lto --with-host-libstdcxx='-static-libgcc -Wl,-Bstatic,-lstdc++ -lm' --enable-target-optspace --disable-nls --disable-multilib --enable-languages=c,c++
Thread model: single
gcc version 5.3.0 (crosstool-NG crosstool-ng-1.22.0-134-ge1d494a)

$ ${CROSS_COMPILE}g++ -###
Using built-in specs.
COLLECT_GCC=/opt/OSELAS.Toolchain-2012.12.1/arm-v5te-linux-gnueabi/gcc-4.7.2-glibc-2.16.0-binutils-2.22-kernel-3.6-sanitized/bin/arm-v5te-linux-gnueabi-g++
COLLECT_LTO_WRAPPER=/opt/OSELAS.Toolchain-2012.12.1/arm-v5te-linux-gnueabi/gcc-4.7.2-glibc-2.16.0-binutils-2.22-kernel-3.6-sanitized/bin/../libexec/gcc/arm-v5te-linux-gnueabi/4.7.2/lto-wrapper
Target: arm-v5te-linux-gnueabi
Configured with: /home/mol/dude/tmp/OSELAS.Toolchain-2012.12.1/platform-arm-v5te-linux-gnueabi-gcc-4.7.2-glibc-2.16.0-binutils-2.22-kernel-3.6-sanitized/build-cross/gcc-4.7.2/configure --build=x86_64-host-linux-gnu --host=x86_64-host-linux-gnu --target=arm-v5te-linux-gnueabi --with-sysroot=/home/mol/dude/tmp/OSELAS.Toolchain-2012.12.1/inst/opt/OSELAS.Toolchain-2012.12.1/arm-v5te-linux-gnueabi/gcc-4.7.2-glibc-2.16.0-binutils-2.22-kernel-3.6-sanitized/sysroot-arm-v5te-linux-gnueabi --disable-multilib --with-float=soft --with-fpu=vfp --with-cpu=arm926ej-s --enable-__cxa_atexit --disable-sjlj-exceptions --disable-nls --disable-decimal-float --disable-fixed-point --disable-win32-registry --enable-symvers=gnu --with-pkgversion=OSELAS.Toolchain-2012.12.1 --enable-threads=posix --with-system-zlib --with-gmp=/home/mol/dude/tmp/OSELAS.Toolchain-2012.12.1/platform-arm-v5te-linux-gnueabi-gcc-4.7.2-glibc-2.16.0-binutils-2.22-kernel-3.6-sanitized/sysroot-host --with-mpfr=/home/mol/dude/tmp/OSELAS.Toolchain-2012.12.1/platform-arm-v5te-linux-gnueabi-gcc-4.7.2-glibc-2.16.0-binutils-2.22-kernel-3.6-sanitized/sysroot-host --prefix=/home/mol/dude/tmp/OSELAS.Toolchain-2012.12.1/inst/opt/OSELAS.Toolchain-2012.12.1/arm-v5te-linux-gnueabi/gcc-4.7.2-glibc-2.16.0-binutils-2.22-kernel-3.6-sanitized --enable-languages=c,c++ --enable-c99 --enable-long-long --enable-libstdcxx-debug --enable-profile --enable-shared --disable-libssp --enable-checking=release
Thread model: posix
gcc version 4.7.2 (OSELAS.Toolchain-2012.12.1)


---


### compiler : `gcc`
### title : `2x slower than clang  summing small float array, GCC should consider larger vectorization factor for "unrolling" reductions`
### open_at : `2016-06-04T17:55:12Z`
### last_modified_date : `2023-06-07T07:44:46Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=71414
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `6.1.1`
### severity : `normal`
### contents :
Ref https://llvm.org/bugs/show_bug.cgi?id=28002

C source code.

```c
__attribute__((noinline)) float sum32(float *a, size_t n)
{
    /* a = (float*)__builtin_assume_aligned(a, 64); */
    float s = 0;
    for (size_t i = 0;i < n;i++)
        s += a[i];
    return s;
}```


See [this gist](https://gist.github.com/yuyichao/5b07f71c1f19248ec5511d758532a4b0) for assembly output by different compilers. GCC appears to be ~2x slower than clang on the two machines (4702HQ and 6700K) I benchmarked this.


---


### compiler : `gcc`
### title : `Spills to vector registers are sub-optimal.`
### open_at : `2016-06-08T11:36:50Z`
### last_modified_date : `2020-08-21T06:11:50Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=71453
### status : `NEW`
### tags : `missed-optimization, ra`
### component : `target`
### version : `10.0`
### severity : `normal`
### contents :
We notice significant performance regression on one important benchmark after r235523.
Note that fix is not responsible for it. A problem is related to spill/fill to/from vector registers (aka xmm registers). For example, for attached test-case we can see a nimber of redundant "vector registers spills" and movements between them:
vmovd   %ecx, %xmm5
vmovd   %xmm5, %ecx
vmovd   %xmm5, 40(%esp) !! It wil be more profitable to save %ecx on stack.
vmovdqa %xmm3, %xmm5     !! this is completely redundant.
...

There is also another issue with spill to vector registers - we must estimate profitability of such spill in comparison with spill on stack. For example, such spill can be not profitable if fill to register is not required:
movl    %eax, 44(%esp)  !! spill
...
andl    44(%esp), %eax !! fill is not required.


---


### compiler : `gcc`
### title : `missing -Wunused-variable on a static global initialized with another`
### open_at : `2016-06-08T15:19:50Z`
### last_modified_date : `2021-04-10T18:11:25Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=71456
### status : `NEW`
### tags : `diagnostic, missed-optimization`
### component : `c++`
### version : `7.0`
### severity : `normal`
### contents :
While looking into bug 71402 I noticed that -Wunused-variable doesn't diagnose unused static namespace scope variables that are dynamically initialized, while emitting the dynamic initialization for them (see the test case below).

I think this is a problem (defect) for a number of reasons:

1) It doesn't match what the documentation promises:
  -Wunused-variable -- Warn whenever a local or static variable is unused aside from its declaration.
2) The dynamic initialization (even when mostly optimized away at -O) isn't without cost that users might want to know might be taking place unnecessarily (in general, whether or not it is necessary depends on the initializer which may be a function call, but in trivial cases like the one below it could be eliminated altogether).
3) The behavior differs from that of Clang which does issue a warning in the case below and also optimizes the variable out.  (Clang only diagnoses the dynamic initialization with potential side-effects with -Wglobal-constructors, and regardless of whether the static variable is used or not.)

I think the subset of (2) where the dynamic initialization has (or could have) side-effects could be viewed as an enhancement request for a new warning pointing out that it takes places even though the variable is unused.

I view the rest of this report (i.e., the mismatch with documentation noted in (1), and the rest of (2) where the dynamic initializer is known not to have side-effects and could be diagnosed and omitted) as a bug.

$ cat zzz.c && /home/msebor/build/gcc-trunk-svn/gcc/xgcc -B /home/msebor/build/gcc-trunk-svn/gcc -S -Wall -Wextra -Wpedantic -fdump-tree-optimized=/dev/stdout -xc++ zzz.c

static int i;
static int j = i;   // -Wunused-variable warning expected

;; Function void __static_initialization_and_destruction_0(int, int) (_Z41__static_initialization_and_destruction_0ii, funcdef_no=0, decl_uid=2245, cgraph_uid=0, symbol_order=2)

void __static_initialization_and_destruction_0(int, int) (int __initialize_p, int __priority)
{
  int i.0_1;

  <bb 2>:
  if (__initialize_p_3(D) == 1)
    goto <bb 3>;
  else
    goto <bb 5>;

  <bb 3>:
  if (__priority_5(D) == 65535)
    goto <bb 4>;
  else
    goto <bb 5>;

  <bb 4>:
  i.0_1 = i;
  j = i.0_1;

  <bb 5>:
  return;

}



;; Function (static initializers for zzz.c) (_GLOBAL__sub_I_zzz.c, funcdef_no=1, decl_uid=2249, cgraph_uid=1, symbol_order=3)

(static initializers for zzz.c) ()
{
  <bb 2>:
  __static_initialization_and_destruction_0 (1, 65535);
  return;

}


---


### compiler : `gcc`
### title : `missed optimization in conditional assignment`
### open_at : `2016-06-08T18:07:01Z`
### last_modified_date : `2021-07-26T23:47:17Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=71461
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `6.2.0`
### severity : `enhancement`
### contents :
=====================
int i, j;
void f1(bool b, int x) {
    (b ? i : j) = x;
}
void f2(bool b, int x) {
    *(b ? &i : &j) = x;
}
==================

On x86-64 at -O3, gcc outputs different code for f1() vs f2(), using a branch for f1() and a cmove for f2(). Is it something that can/should be optimized?

gcc (version 5, 6, or current trunk) outputs:
==================
f1(bool, int):
        testb   %dil, %dil
        jne     .L6
        movl    %esi, j(%rip)
        ret
.L6:
        movl    %esi, i(%rip)
        ret

f2(bool, int):
        testb   %dil, %dil
        movl    $j, %edx
        movl    $i, %eax
        cmove   %rdx, %rax
        movl    %esi, (%rax)
        ret
==================

vs clang:

==================
f1(bool, int):                                # @f1(bool, int)
        movl    $i, %eax
        movl    $j, %ecx
        testb   %dil, %dil
        cmovneq %rax, %rcx
        movl    %esi, (%rcx)
        retq

f2(bool, int):                                # @f2(bool, int)
        movl    $i, %eax
        movl    $j, %ecx
        testb   %dil, %dil
        cmovneq %rax, %rcx
        movl    %esi, (%rcx)
        retq
==================

In my tests, the branch version of f1() is about 2x-3x slower than f2() if the branch is 50% predicted, and only about 1% faster than f2() if it is 100% predicted.

FWIW, this version:

==================
void f3(bool b, int x) {
    if(b) i = x; else j = x;
}
==================

ends up using a branch on both gcc and clang.

Thanks...

-Lewis


---


### compiler : `gcc`
### title : `Bitfield causes load hit store with larger store than load`
### open_at : `2016-06-12T23:12:14Z`
### last_modified_date : `2022-03-08T16:20:45Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=71509
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `7.0`
### severity : `normal`
### contents :
I notice a nasty load hit store in the following test case built with -O2 on ppc64le. The load is larger than the store, which means on many CPUs the store cannot be forwarded and it has to wait until it completes in the cache.

struct sk_buff a;

struct sk_buff {
        long blah;
        char csum_level:2;
};

void __skb_decr_checksum_unnecessary(struct sk_buff *p1)
{
        p1->csum_level--;
}

void func(void);

void tcp_v4_rcv(void)
{
        struct sk_buff *b = &a;

        func();
        __skb_decr_checksum_unnecessary(b);
        func();
        __skb_decr_checksum_unnecessary(b);
}

We end up with this odd situation where we do both a byte and a double
word load:

# objdump  -d testcase.o | grep r31

  58:	08 00 5f e9 	ld      r10,8(r31)
  5c:	08 00 3f 89 	lbz     r9,8(r31)
  70:	08 00 3f 99 	stb     r9,8(r31)

  7c:	08 00 5f e9 	ld      r10,8(r31)
  84:	08 00 3f 89 	lbz     r9,8(r31)
  a0:	08 00 3f 99 	stb     r9,8(r31)


---


### compiler : `gcc`
### title : `Missing cross-jumping of switch cases`
### open_at : `2016-06-13T10:24:05Z`
### last_modified_date : `2021-11-04T01:41:29Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=71520
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `6.0`
### severity : `enhancement`
### contents :
As mentioned in PR71373, for switch cases we have various issues.

One is that tree cross-jumping fails to handle bbs with labels, therefore anything that is successfor of GIMPLE_SWITCH.

Another one is that the switchconv pass runs very early, before we could do any cross-jumping, and therefore often decides to use inefficient table or bitmask lowering, even when it could do better if it knew some cases can be cross-jumped.

For the first issue, testcase is e.g.
void bar (int);

void
foo (int x)
{
  switch (x)
    {
    case 1:
    case 12:
    case 28:
    case 174:
      bar (1);
      bar (2);
      break;
    case 3:
    case 7:
    case 78:
    case 96:
    case 121:
    default:
      bar (3);
      bar (4);
      bar (5);
      bar (6);
      break;
    case 8:
    case 13:
    case 27:
    case 19:
    case 118:
      bar (3);
      bar (4);
      bar (5);
      bar (6);
      break;
    case 4:
      bar (7);
      break;
    }
}


---


### compiler : `gcc`
### title : `Missing removal of null pointer check`
### open_at : `2016-06-14T21:07:33Z`
### last_modified_date : `2021-07-29T16:40:06Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=71538
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `6.1.1`
### severity : `enhancement`
### contents :
Consider this code:

#include <stdio.h>

extern void f(int *p) 
{
	p = *((int (*)[6])p);

	if(p == NULL)
		printf("NULL");
}


It's obvious (at least for me) that p can't be possibly NULL because it's assigned the value of pointer to the first element of array with 6 elements. However the assembly output of this code for my native machine compiled on linux (x86-64 - dumped using ida pro with general assembler for intel) is:

;f function

		test	rdi, rdi
		jz	short loc_400550
		rep retn
; ---------------------------------------------------------------------------
		align 10h

loc_400550:				
		mov	edi, (offset format+4) ; "NULL"
		xor	eax, eax
		jmp	_printf
;f function end

As you see the branch where printf is called with "NULL" is still present in the code although on theory it should never be reached.

I don't think there is requirement by the standard to disallow evaluation of this expression (as opposed to for example *&p).


---


### compiler : `gcc`
### title : `missed optimization for type short, char and floating point types`
### open_at : `2016-06-16T15:08:51Z`
### last_modified_date : `2023-07-20T20:41:14Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=71558
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `6.1.0`
### severity : `enhancement`
### contents :
for the following code gcc should produce the same code for fun and fun2, but fail for shorts and char with -01 and higher. It also fails for floating types with -0fast
-----------------
#define optimize(type)		\
type fun(type i, type j)	\
{				\
  return i + j;			\
}				\
type fun2(type i, type j)	\
{				\
  if (j == 0)			\
    return i;			\
  else if (i == 0)		\
    return j;			\
  else				\
    return i + j;		\
}


optimize(int);
optimize(char);
optimize(short);
--------------------

For all types the optimization is no longer performed if any type is different from the other 
--------------------
int fun2(unsigned i, int j)
{
  if (i == 0)
    return j;
  else if (j == 0)
    return i;
  else
    return i + j;
}
--------------------
And if we are testing if both i and j are 0 the optimization is no longer performed
------------------
int fun2(int i, int j)
{
  if (i == 0 && j == 0)
    return j; //or "return i + j;" or "return 0;" or "return i;"
  if (i == 0)
    return j;
  else if (j == 0)
    return i;
  else
    return i + j;
}
-------------------
It also fails if one replace the addition with a subtraction or a multiplication (with changed return values.)


---


### compiler : `gcc`
### title : `missing strlen optimization on different array initialization style`
### open_at : `2016-06-22T16:36:39Z`
### last_modified_date : `2020-01-28T14:54:14Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=71625
### status : `RESOLVED`
### tags : `missed-optimization, patch`
### component : `tree-optimization`
### version : `7.0`
### severity : `normal`
### contents :
Hi,

The following two functions shall give the same result 3.
Currently, foo () can be optimized to return a constant.
bar (), however, contains function call to strlen, which is sub-optimal.

int foo ()
{
  char array[] = "abc";
  return __builtin_strlen (array);
}

int bar ()
{
  char array[] = {'a', 'b', 'c', '\0'};
  return __builtin_strlen (array);
}


Clang 3.8 produce optimal code-generation for both cases.
In addition, I have another case here:

int hallo ();
int dummy ()
{
  char array[] = "abc";
  return hallo () + __builtin_strlen (array);
}

the __builtin_strlen is not fold into a const as in foo () above. Presumably,
gcc is too conservative about what hallo () function can do. By adding a pure attribute to hallo (), gcc will generate optimal code.

Clang 3.8 gives optimal code in this case as well.


---


### compiler : `gcc`
### title : `some integer conversions defeat memcpy optimizaton`
### open_at : `2016-06-28T21:07:07Z`
### last_modified_date : `2021-07-15T20:26:55Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=71690
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `7.0`
### severity : `normal`
### contents :
Both functions in the following program are expected to result in comparably efficient code.  In expand_builtin_memcpy, GCC decides whether an invocation of __builtin_memcpy will be expanded inline or result in a library call.  Among the factors it uses to make that decision is the range of sizes of the copy.  The range is obtained from the result of the Value Range Propagation optimization for the size argument, provided the argument is constrained to a subrange of its type.  When the argument's type is other than size_t, VRP makes the range available, and the call to memcpy may be expanded inline (this is the case with the function g below).  But when the argument's type is size_t, VRP does not make its range available, and the expansion results in a library call, thus defeating the optimization.  This seems to be a general problem with VRP, not one limited to memcpy (I just used memcpy as an example).  Any built-in whose expansion depends on the result of VRP of one of its arguments may be affected.

char d [10];
char s [10];

void f (int);

void g (unsigned n)
{
  if (n >= sizeof d) return;

  __builtin_memcpy (d, s, n);
}

void h (unsigned long n)
{
  if (n >= sizeof d) return;

  __builtin_memcpy (d, s, n);
}



The problem can be seen in the generated assembly and also in the vrp dump for the program (see the <<< annotations):

Value ranges after VRP:

...
_1: [0, 9]
.MEM_2: VARYING
n_3(D): VARYING
n_6: [0, 9]  EQUIVALENCES: { n_3(D) } (1 elements)


g (unsigned int n)
{
  long unsigned int _1;

  <bb 2>:
  if (n_3(D) > 9)
    goto <bb 4>;
  else
    goto <bb 3>;

  <bb 3>:
  _1 = (long unsigned int) n_3(D);   <<< constrained to [0, 9]
  __builtin_memcpy (&d, &s, _1);

  <bb 4>:
  return;
}
...
Value ranges after VRP:

.MEM_1: VARYING
n_2(D): VARYING
n_5: [0, 9]  EQUIVALENCES: { n_2(D) } (1 elements)


h (long unsigned int n)
{
  <bb 2>:
  if (n_2(D) > 9)
    goto <bb 4>;
  else
    goto <bb 3>;

  <bb 3>:
  __builtin_memcpy (&d, &s, n_2(D));   <<< n_2(D) is VARYING

  <bb 4>:
  return;

}


---


### compiler : `gcc`
### title : `bogus -Wmaybe-uninitialized warning: gcc misses that non-NULL pointer + offset can never be NULL`
### open_at : `2016-06-29T15:07:30Z`
### last_modified_date : `2021-03-31T21:11:33Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=71699
### status : `RESOLVED`
### tags : `diagnostic, missed-optimization`
### component : `middle-end`
### version : `7.0`
### severity : `normal`
### contents :
gcc does not understand that adding an offset to a pointer returned by a returns_nonnull function can never yield a NULL pointer.  Vis:

$ cat test.c 
char *xstrdup (const char *) __attribute__ ((__returns_nonnull__));

#define PREFIX "some "

int
main ()
{
  char *saveptr;
  char *name = xstrdup (PREFIX "name");

  // name = PREFIX "name";              // this makes the warning go away

  char *tail = name + sizeof (PREFIX) - 1;
  // tail = &name[sizeof (PREFIX) - 1]; // this does not help
  // tail = name;                       // while this makes the warning go away

  if (tail == 0)
    tail = saveptr;
  while (*tail == ' ')
    ++tail;

  return 0;
}
$ /opt/gcc/bin/gcc test.c -c -Wall
test.c: In function ‘main’:
test.c:18:10: warning: ‘saveptr’ may be used uninitialized in this function [-Wmaybe-uninitialized]
     tail = saveptr;
     ~~~~~^~~~~~~~~

Enabling optimization does not make it go away:

$ /opt/gcc/bin/gcc -O2 test.c -c -Wall
test.c: In function ‘main’:
test.c:19:10: warning: ‘saveptr’ may be used uninitialized in this function [-Wmaybe-uninitialized]
   while (*tail == ' ')
          ^~~~~

That was gcc version 7.0.0 20160503 (experimental) built from sources.

Fedora 23's gcc 5.3.1 shows the same.

This is a reduced testcase based on a warning gcc issued when building gdb:
 https://sourceware.org/ml/gdb-patches/2016-06/msg00515.html


---


### compiler : `gcc`
### title : `Simplify (intptr_t)p+4-(intptr_t)(p+4)`
### open_at : `2016-07-01T09:19:43Z`
### last_modified_date : `2023-05-02T05:16:33Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=71726
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `7.0`
### severity : `enhancement`
### contents :
https://gcc.gnu.org/ml/gcc-patches/2016-07/msg00010.html

#include <stdint.h>
intptr_t f(char*p){return (intptr_t)p+4-(intptr_t)(p+4);}

We only manage to simplify this to return 0 in RTL. "maybe we can value-number it
the same with some tricks" but that would not help for (intptr_t)p+8-(intptr_t)(p+4), or even for (intptr_t)(p+4)-4-(intptr_t)p.

"to handle (long)p + 4 - (long)(p + 4) the only thing we need is to
transform (long)(p + 4) to (long)p + 4 ... that would simplify things but
of course we cannot ever undo that canonicalization if the result is
ever converted back to a pointer." Indeed, I don't know if on average it would be a win or a loss (I'd bet a little on "win").

Easiest seems to be to add a few more match.pd patterns as we hit them in real code, and hope they cover enough cases that we can forget about the rest for a while, until someone enhances reassoc.


---


### compiler : `gcc`
### title : `missing tailcall optimization`
### open_at : `2016-07-04T18:27:47Z`
### last_modified_date : `2021-08-10T23:23:00Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=71761
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `6.1.0`
### severity : `enhancement`
### contents :
Currently GCC doesn't optimize tailcall in the following function:

struct token
{
    char const* tok_start;
    char const* tok_end;
    int tok_type;
    unsigned identifier_hash;
};

token f();

token g()
{
  return f();
}

Generated code:

g():
        pushq   %rbx
        movq    %rdi, %rbx
        call    f()
        movq    %rbx, %rax
        popq    %rbx
        ret

Expected:

g():
        jmp     f()


---


### compiler : `gcc`
### title : `Missed trivial rematerialiation oppurtunity`
### open_at : `2016-07-05T16:47:55Z`
### last_modified_date : `2023-05-31T06:02:38Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=71768
### status : `RESOLVED`
### tags : `missed-optimization, ra`
### component : `rtl-optimization`
### version : `7.0`
### severity : `enhancement`
### contents :
Compiling
#define vector __attribute__ ((vector_size (16)))
const vector int cst={10,10,10,10};
int t()
{
  vector int val = cst;
  asm("#%0"::"x"(val));
  e();
  asm("#%0"::"x"(val));
}
Results in:
t:
.LFB0:
        .cfi_startproc
        subq    $24, %rsp
        .cfi_def_cfa_offset 32
        vmovaps .LC0(%rip), %xmm0
#APP
# 6 "t.c" 1
        #%xmm0
# 0 "" 2
#NO_APP
        xorl    %eax, %eax
        vmovaps %xmm0, (%rsp)
        call    e
        vmovaps (%rsp), %xmm0
#APP
# 8 "t.c" 1
        #%xmm0
# 0 "" 2
#NO_APP
        addq    $24, %rsp
        .cfi_def_cfa_offset 8
        ret

Which is clearly suboptimal, because xmm0 can be rematerialized again from LC0. This hits pretty badly the exchange2 benchmark with -O3 -march=bdver2 where the function is self recursive and we end up having many constants cached in XMM registers.


---


### compiler : `gcc`
### title : `Redundant move instruction for sign extension`
### open_at : `2016-07-06T05:26:43Z`
### last_modified_date : `2022-08-03T07:58:43Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=71775
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `6.1.0`
### severity : `enhancement`
### contents :
Created attachment 38838
preprocessed file for the test program

Compiling the following program with g++ -O3 -S:

#include <cstdint>

unsigned long long f(std::uint64_t x) {
  std::uint64_t ans = 0;
  for (; x != 0; x &= (x - 1)) {
    ans ^= __builtin_ctzll(x);
  }
  return ans;
}

yields the following assembly code:

	.text
	.align 4,0x90
	.globl __Z1fy
__Z1fy:
LFB0:
	xorl	%eax, %eax
	testq	%rdi, %rdi
	je	L4
	.align 4,0x90
L3:
	bsfq	%rdi, %rdx
	movslq	%edx, %rdx
	xorq	%rdx, %rax
	leaq	-1(%rdi), %rdx
	andq	%rdx, %rdi
	jne	L3
	ret
L4:
	ret

Note that the movslq instruction inside the loop is redundant. Clang is able to generate code without this move. Benchmark shows, this represents a 5%-10% difference in the running time of this function.


Version info:
Using built-in specs.
COLLECT_GCC=gcc-6
COLLECT_LTO_WRAPPER=/usr/local/Cellar/gcc6/6.1.0/libexec/gcc/x86_64-apple-darwin15.5.0/6.1.0/lto-wrapper
Target: x86_64-apple-darwin15.5.0
Configured with: ../configure --build=x86_64-apple-darwin15.5.0 --prefix=/usr/local/Cellar/gcc6/6.1.0 --libdir=/usr/local/Cellar/gcc6/6.1.0/lib/gcc/6 --enable-languages=c,c++,objc,obj-c++,fortran --program-suffix=-6 --with-gmp=/usr/local/opt/gmp --with-mpfr=/usr/local/opt/mpfr --with-mpc=/usr/local/opt/libmpc --with-isl=/usr/local/opt/isl014 --with-system-zlib --enable-libstdcxx-time=yes --enable-stage1-checking --enable-checking=release --enable-lto --with-build-config=bootstrap-debug --disable-werror --with-pkgversion='Homebrew gcc6 6.1.0' --with-bugurl=https://github.com/Homebrew/homebrew-versions/issues --enable-plugin --disable-nls --enable-multilib --with-native-system-header-dir=/usr/include --with-sysroot=/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.11.sdk
Thread model: posix
gcc version 6.1.0 (Homebrew gcc6 6.1.0)


---


### compiler : `gcc`
### title : `Computed gotos are mostly optimized away`
### open_at : `2016-07-06T23:10:06Z`
### last_modified_date : `2019-11-21T19:44:00Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=71785
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `unknown`
### severity : `normal`
### contents :
Hi,

I'm working on some interpreter like constructs in postgres. To reduce the number of mispredictions I wanted to use the "typical" jump threading approach. Unfortunately with gcc-6 (gcc-6 (Debian 6.1.1-8) 6.1.1 20160630) and up to a recent snapshot (Debian 20160612-1) 7.0.0 20160612 (experimental) [trunk revision 237336]), gcc merges some of the gotos together in a common label, and jumps there.

In the attached file (a small artifical case showing the problem), with -O3 this results in
CASE_OP_A:
	someglobal++;
	op++;
	goto *dispatch_table[op->opcode];
CASE_OP_B:
	do_stuff_b(op->arg);
	op++;
	goto *dispatch_table[op->opcode];

being implemented as
.L5:
	addq	$8, %rbx
	jmp	*%rax
...
.L3:
	movl	(%rbx), %eax
	addl	$1, someglobal(%rip)
	movq	dispatch_table.1772(,%rax,8), %rax
	jmp	.L5
...
.L4:
	movl	-4(%rbx), %edi
	call	do_stuff_b
	movl	(%rbx), %eax
	movq	dispatch_table.1772(,%rax,8), %rax
	jmp	.L5


I've tried -fno-gcse and -fno-crossjumping, and neither seems to fix the problem.

It's also kind of weird how the load from the dispatch table is still performed in the individual branches, just the final jmp *%rax happens in the common location (L5 here).  In the actual case I'm fighting with gcc "inlines" the jmp *%rax in one of the dispatches, but not in the other 8.

Any additional information I can provide?

Regards,

Andres


---


### compiler : `gcc`
### title : `Missing constant prop from const variable`
### open_at : `2016-07-11T01:39:04Z`
### last_modified_date : `2021-07-25T02:37:30Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=71836
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `6.1.0`
### severity : `normal`
### contents :
Take:
#include <stdio.h>
#include <float.h>

int main()
{
	float a[] __attribute__((aligned(0x20))) = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16};
	float maxval = -FLT_MAX;	
	for (size_t i = 0; i < 16; i++)
		maxval = a[i] > maxval ? a[i] : maxval;
			
	printf("%g\n", maxval);
}
---- CUT ----
Currently on aarch64-linux-gnu we get:
  a = *.LC0;
  _17 = a[0];
  iftmp.0_18 = _17 > -3.4028234663852885981170418348451692544e+38 ? _17 : -3.4028234663852885981170418348451692544e+38;
  _24 = a[1];
  iftmp.0_25 = iftmp.0_18 < _24 ? _24 : iftmp.0_18;
  _31 = a[2];


--- CUT ---
Depending on the scheduler, GCC can remove even more extra load/stores (thunderx scheduler will cause GCC not to remove them while cortex-a57 will).  But really any load/stores here is not useful as a[0] can be found in .LC0[0].


---


### compiler : `gcc`
### title : `Optimize FMA when some arguments are simple constants`
### open_at : `2016-07-11T12:37:58Z`
### last_modified_date : `2021-12-28T05:42:03Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=71842
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `7.0`
### severity : `enhancement`
### contents :
#include <math.h>
double f(double x, double y){ return fma(x, y, 0.); }
double g(double x, double y){ return fma(0., x, y); }
double h(double x){ return fma(3., 4., x); }

Depending on compiler options, we could optimize those to x*y, y and 12.+x. fma(1,x,y) might also be x+y.


---


### compiler : `gcc`
### title : `missed vectorization optimization`
### open_at : `2016-07-18T21:00:00Z`
### last_modified_date : `2021-08-25T06:08:12Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=71921
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `6.3.0`
### severity : `enhancement`
### contents :
program below does not auto-vectorize to use the x86 "maxps" instruction even though gcc is smart enough to know there is a "maxss" instruction...


gcc -O3 -ftree-vectorize -fopt-info-vec -fopt-info-vec-missed -march=westmere test.cpp -S -o test.S

does not show any use of maxps in test.S



#include <vector>

void relu(float * __restrict__ output, const float * __restrict__ input, int size)
{
    int i;
    int s2;

    s2 = size / 4;
    for (i = 0; i < s2 * 4; i++) {
        float t;
        t = input[i];
        output[i] = std::max(t, float(0));
    }
}


---


### compiler : `gcc`
### title : `return instruction emitted twice with branch target inbetween`
### open_at : `2016-07-18T23:33:42Z`
### last_modified_date : `2023-07-18T14:29:01Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=71923
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `6.1.0`
### severity : `normal`
### contents :
function

unsigned int fact( unsigned int n) { return n < 1 ? 1 : n*fact(n-1); }

produces

fact:
.LFB0:
        .cfi_startproc
        testl   %edi, %edi
        movl    $1, %eax
        je      .L4
        .p2align 4,,10
        .p2align 3
.L3:
        imull   %edi, %eax
        subl    $1, %edi
        jne     .L3
        rep ret # <-- this instruction can be removed
.L4:
        rep ret
        .cfi_endproc
.LFE0:
        .size   fact, .-fact
        .section        .text.unlikely

can be easily reproduced at http://gcc.godbolt.org/


---


### compiler : `gcc`
### title : `Function multiversioning prohibits inlining`
### open_at : `2016-07-25T11:05:47Z`
### last_modified_date : `2023-05-22T13:39:57Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=71990
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `7.0`
### severity : `normal`
### contents :
Hi,

I'm trying to write a library that uses F16C instructions in certain places, and since they're not really universally accessible (and ld.so hardware capabilities seem to have been long abandoned), I've tried to use function multiversioning for it. However, trying to combine it with inlining seems to draw a blank; a very simplified example:

klump:~> /usr/lib/gcc-snapshot/bin/g++ -v                 
Using built-in specs.                  
COLLECT_GCC=/usr/lib/gcc-snapshot/bin/g++
COLLECT_LTO_WRAPPER=/usr/lib/gcc-snapshot/libexec/gcc/x86_64-linux-gnu/7.0.0/lto-wrapper
Target: x86_64-linux-gnu
Configured with: ../src/configure -v --with-pkgversion='Debian 20160707-1' --with-bugurl=file:///usr/share/doc/gcc-snapshot/README.Bugs --enable-languages=c,ada,c++,java,go,fortran,objc,obj-c++ --prefix=/usr/lib/gcc-snapshot --enable-shared --enable-linker-build-id --disable-nls --with-sysroot=/ --enable-clocale=gnu --enable-libstdcxx-debug --enable-libstdcxx-time=yes --with-default-libstdcxx-abi=new --enable-gnu-unique-object --disable-vtable-verify --enable-libmpx --enable-plugin --with-system-zlib --disable-browser-plugin --enable-java-awt=gtk --enable-gtk-cairo --with-java-home=/usr/lib/jvm/java-1.5.0-gcj-7-snap-amd64/jre --enable-java-home --with-jvm-root-dir=/usr/lib/jvm/java-1.5.0-gcj-7-snap-amd64 --with-jvm-jar-dir=/usr/lib/jvm-exports/java-1.5.0-gcj-7-snap-amd64 --with-arch-directory=amd64 --with-ecj-jar=/usr/share/java/eclipse-ecj.jar --enable-objc-gc --enable-multiarch --with-arch-32=i686 --with-abi=m64 --with-multilib-list=m32,m64,mx32 --enable-multilib --with-tune=generic --disable-werror --enable-checking=yes --build=x86_64-linux-gnu --host=x86_64-linux-gnu --target=x86_64-linux-gnu
Thread model: posix
gcc version 7.0.0 20160707 (experimental) [trunk revision 238117] (Debian 20160707-1) 

klump:~> cat test.cc                     
#include <stdio.h>
 
__attribute__ ((target("default")))
inline int foo()
{
	return 0;
}

__attribute__ ((target("avx")))
inline int foo()
{
	return 1;
}

int bar()
{
	int sum = 0;
	for (int i = 0; i < 100; ++i) {
		sum += foo();
	}
	return sum;
}

int main(void)
{
	printf("%d\n", bar());
}

klump:~> /usr/lib/gcc-snapshot/bin/g++ -O2 -o test test.cc
klump:~> nm --demangle test | egrep 'foo|bar' 
0000000000400c40 i _Z3foov.ifunc()
0000000000400bf0 T bar()
0000000000400c20 W foo()
0000000000400c30 W foo() [clone .avx]
0000000000400c40 W foo() [clone .resolver]

Of course, in reality, my foo() would do something more complicated, like call _cvtss_sh() or similar; this is a toy example. But it illustrates that the function multiversioning blocks inlining.

If I compile with -mavx, the entire multiversioning goes away (only the AVX version is emitted), so I hoped that I could use target cloning on bar():

__attribute__ ((target_clones("avx", "default")))
int bar()
{
    // same code...

but unfortunately, no. There's a bar() clone for AVX emitted, but it still calls the resolving function for foo(); no inlining.

So I really can't find any usable way of using this feature if your architecture switch is in inlined functions (in my case, convert to/from fp16).


---


### compiler : `gcc`
### title : `Missed BB SLP vectorization in GCC`
### open_at : `2016-07-25T11:46:53Z`
### last_modified_date : `2021-08-11T05:44:32Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=71992
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `7.0`
### severity : `enhancement`
### contents :
The below test case fails to vectorize.
gcc version 7.0.0 20160724 (experimental) (GCC)

gcc -Ofast -mavx -fvect-cost-model=unlimited slp.c -S -fdump-tree-slp-all

struct st
{
        double x;
        double y;
        double z;
        double p;
        double q;
}*obj;

double a,b,c;

void slp_test()
{

        obj->x = a*a+3.0;
        obj->y= b*b+c;
        obj->z= a+b*3.0;
        obj->p= a+b*3.0;
        obj->q =a+b+c;

}

LLVM is able to SLP vectorize looks like it is creating vector of [a,c]  and [b*3.0,b*b] and does vector add.

GCC is not SLP vectorizing.  Group slitting also not working. I expected it to get split and vectorize these statements.

  obj->z= a+b*3.0;
  obj->p= a+b*3.0;

Another case 

struct st
{
        double x;
        double y;
        double z;
        double p;
        double q;
}*obj;

double a,b,c;

void slp_test()
{

        obj->x = a*b;
        obj->y= b+c;
        obj->z= a+b*3.0;
        obj->p= a+b*3.0;
        obj->q =a+b+c;

}


LLVM forms vector [b*3.0,a+b] [a,c] and does vector addition.


---


### compiler : `gcc`
### title : `VRP derives poor range for "y = (int)x + C;" when x has an anti-range`
### open_at : `2016-07-26T02:44:49Z`
### last_modified_date : `2021-07-27T13:38:26Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=72443
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `7.0`
### severity : `enhancement`
### contents :
Test case:

void
test (int x)
{
  if (x < 5 || x > 10)
    {
      int y;
      foo (x);
      y = x + 1;
      bar (y);
    }
}

The range for x is ~[5, 10] and so one would expect the range for y to be ~[6, 11].  Yet what's actually derived for y is:

Visiting statement:
y_7 = x_9 + 1;
Meeting
  [-2147483647, 5]
and
  [12, +INF(OVF)]
to
  [-2147483647, +INF(OVF)]
Found new range for y_7: [-2147483647, +INF(OVF)]

which is a less useful range than the expected ~[6, 11].

This range for y is derived by splitting the anti-range of x_9 into two nonintersecting ranges, adjusting them both (by +1 in this case), and then vrp_meet()ing them.  But vrp_meet() turns two non-intersecting ranges into an anti-range only if the lower bound is -INF (which is not the case here) and the upper is +INF.

A possible solution is to also allow vrp_meet() to turn two ranges into an anti-range if either the upper or lower bound is an INF(OVF).  Maybe the number of restricted elements within the corresponding anti-range vs the number within the corresponding union of the two ranges should be considered too in deciding which representation to pick?


---


### compiler : `gcc`
### title : `Missed optimizations: count_if on std::array of constants.`
### open_at : `2016-08-11T03:34:43Z`
### last_modified_date : `2021-08-18T22:25:34Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=73457
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `6.1.0`
### severity : `enhancement`
### contents :
First of all, given how simple this bug report is, I imagine it must be a duplicate, but am not sure what to look for and didn't find anything very relevant. Apologies therefore.

gcc: https://godbolt.org/g/kAhsRr
clang: https://godbolt.org/g/B3fsWi

It seems gcc is unable to fold the std::count_if over the std::array despite it being constant-initialized, while clang optimizes the program away.

Adding constexpr does not change the output. Replacing std::array with an initializer list makes gcc optimize everything: https://godbolt.org/g/chOqnZ


---


### compiler : `gcc`
### title : `Another wrong -Wmaybe-uninitialized warning in switch statement`
### open_at : `2016-08-11T08:43:06Z`
### last_modified_date : `2022-08-31T11:05:45Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=73550
### status : `NEW`
### tags : `diagnostic, missed-optimization`
### component : `tree-optimization`
### version : `7.0`
### severity : `normal`
### contents :
Hi,
GCC trunk gives wrong -Wmaybe-uninitialized warning message on below switch statement:


int fun1 (int, int);
int fun2 (int, int);
int fun3 (int, int);
void swap (int *, int *);
void abort (void);
void bar (void);
void foo (int code, int x, int a, int b)
{
  int (*fp) (int, int);

  switch (code)
    {
    case 1:
      if (x == 1)
	{
	  fp = fun3;
	  break;
	}
    case 2:
      swap (&a, &b);
    case 3:
    case 4:
      fp = fun1;
      break;
    case 11:
      if (x == 1)
	{
	  fp = fun3;
	  break;
	}
    case 12:
      swap (&a, &b);
    case 13:
    case 14:
      fp = fun2;
      break;
    case 5:
    case 6:
    case 7:
    case 8:
      break;
    default:
      abort ();
    }

  switch (code)
    {
    case 1:
    case 3:
    case 11:
    case 13:
      fp (a, b);
      bar ();
      break;
    case 2:
    case 4:
    case 12:
    case 14:
      fp (a, b);
      break;
    case 5:
    case 6:
    case 7:
    case 8:
      bar ();
      break;
    default:
      abort ();
    }
  return;
}

Compiled with:
$ ./gcc -O2 -S x.c -o x.S -Wmaybe-uninitialized
produces:
x.c: In function ‘foo’:
x.c:53:7: warning: ‘fp’ may be used uninitialized in this function [-Wmaybe-uninitialized]
       fp (a, b);
       ^~~~~~~~~

GCC is configured as:
../gcc/configure --prefix=... --disable-bootstrap --disable-libssp --disable-libgomp --disable-libsanitizer --disable-libitm --disable-atomic CXXFLAGS='-g -O0' --enable-languages=c,c++


---


### compiler : `gcc`
### title : `by_pieces_ninsns doesn't support TImode/OImode/XImode`
### open_at : `2016-08-11T15:24:05Z`
### last_modified_date : `2021-08-07T14:52:21Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=74113
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `7.0`
### severity : `normal`
### contents :
TImode/OImode/XImode support load and store with vector registers.  But
by_pieces_ninsns determines the widest mode with MAX_FIXED_MODE_SIZE
which is limited by integer registers.  There is a patch to update
alignment_for_piecewise_move to remove the MAX_FIXED_MODE_SIZE restriction:

https://gcc.gnu.org/ml/gcc-patches/2016-04/msg01506.html

But there is a concern for simplify_immed_subreg:

https://gcc.gnu.org/ml/gcc-patches/2016-04/msg01527.html


---


### compiler : `gcc`
### title : `powerpc64: Very poor code generation for homogeneous vector aggregates passed in registers`
### open_at : `2016-08-11T20:29:07Z`
### last_modified_date : `2020-07-10T20:59:59Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=74585
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `7.0`
### severity : `normal`
### contents :
For the PowerPC64 ELF V2 ABI, homogeneous aggregates of vectors (any combination of structs and arrays containing only vectors) are passed in the first eight vector registers.  Tree-sra does not understand this and performs scalarization on such aggregates, forcing them to memory in the process.  This causes unnecessary stores/reloads to the stack on function entry and exit, resulting in terrible performance.

As an example, consider:

--- SNIP ---
#define VEC_DW_H (1)
#define VEC_DW_L (0)

typedef struct
{
  __vector double vx0;
  __vector double vx1;
  __vector double vx2;
  __vector double vx3;
} vdoublex8_t;

vdoublex8_t
test_vecd8_rotate_left (vdoublex8_t a)
{
  __vector double temp;
  vdoublex8_t result;

  temp = a.vx0;

  /* Copy low dword of vx0 and high dword of vx1 to vx0 high / low.  */
  result.vx0[VEC_DW_H] = a.vx0[VEC_DW_L];
  result.vx0[VEC_DW_L] = a.vx1[VEC_DW_H];
  /* Copy low dword of vx1 and high dword of vx2 to vx1 high / low.  */
  result.vx1[VEC_DW_H] = a.vx1[VEC_DW_L];
  result.vx1[VEC_DW_L] = a.vx2[VEC_DW_H];
  /* Copy low dword of vx2 and high dword of vx2 to vx2 high / low.  */
  result.vx2[VEC_DW_H] = a.vx2[VEC_DW_L];
  result.vx2[VEC_DW_L] = a.vx3[VEC_DW_H];
  /* Copy low dword of vx3 and high dword of vx0 to vx3 high / low.  */
  result.vx3[VEC_DW_H] = a.vx3[VEC_DW_L];
  result.vx3[VEC_DW_L] = temp[VEC_DW_H];

  return (result);
}
--- SNIP ---

After 031t.forwprop, we have:


;; Function test_vecd8_rotate_left (test_vecd8_rotate_left, funcdef_no=0, decl_uid=2364, cgraph_uid=0, symbol_order=0)

test_vecd8_rotate_left (struct vdoublex8_t a)
{
  struct vdoublex8_t result;
  __vector double temp;
  struct vdoublex8_t D.2369;
  __vector double _1;
  double _2;
  double _3;
  double _4;
  double _5;
  double _6;
  double _7;
  double _8;
  double _9;

  <bb 2>:
  _1 = a.vx0;
  temp_23 = _1;
  _2 = BIT_FIELD_REF <a.vx0, 64, 0>;
  BIT_FIELD_REF <result.vx0, 64, 64> = _2;
  _3 = BIT_FIELD_REF <a.vx1, 64, 64>;
  BIT_FIELD_REF <result.vx0, 64, 0> = _3;
  _4 = BIT_FIELD_REF <a.vx1, 64, 0>;
  BIT_FIELD_REF <result.vx1, 64, 64> = _4;
  _5 = BIT_FIELD_REF <a.vx2, 64, 64>;
  BIT_FIELD_REF <result.vx1, 64, 0> = _5;
  _6 = BIT_FIELD_REF <a.vx2, 64, 0>;
  BIT_FIELD_REF <result.vx2, 64, 64> = _6;
  _7 = BIT_FIELD_REF <a.vx3, 64, 64>;
  BIT_FIELD_REF <result.vx2, 64, 0> = _7;
  _8 = BIT_FIELD_REF <a.vx3, 64, 0>;
  BIT_FIELD_REF <result.vx3, 64, 64> = _8;
  _9 = BIT_FIELD_REF <_1, 64, 64>;
  BIT_FIELD_REF <result.vx3, 64, 0> = _9;
  D.2369 = result;
  result ={v} {CLOBBER};
  return D.2369;

}

but after 032t.esra, we have:

test_vecd8_rotate_left (struct vdoublex8_t a)
{
  __vector double result$vx3;
  __vector double result$vx2;
  __vector double result$vx1;
  __vector double result$vx0;
  __vector double a$vx3;
  __vector double a$vx2;
  __vector double a$vx1;
  __vector double a$vx0;
  struct vdoublex8_t result;
  __vector double temp;
  struct vdoublex8_t D.2369;
  __vector double _1;
  double _2;
  double _3;
  double _4;
  double _5;
  double _6;
  double _7;
  double _8;
  double _9;
  __vector double _11;
  __vector double _21;
  __vector double _25;
  __vector double _26;

  <bb 2>:
  a$vx0_27 = MEM[(struct  *)&a];
  a$vx1_28 = MEM[(struct  *)&a + 16B];
  a$vx2_29 = MEM[(struct  *)&a + 32B];
  a$vx3_30 = MEM[(struct  *)&a + 48B];
  _1 = a$vx0_27;
  temp_23 = _1;
  _2 = BIT_FIELD_REF <a$vx0_27, 64, 0>;
  BIT_FIELD_REF <result$vx0, 64, 64> = _2;
  _3 = BIT_FIELD_REF <a$vx1_28, 64, 64>;
  BIT_FIELD_REF <result$vx0, 64, 0> = _3;
  _4 = BIT_FIELD_REF <a$vx1_28, 64, 0>;
  BIT_FIELD_REF <result$vx1, 64, 64> = _4;
  _5 = BIT_FIELD_REF <a$vx2_29, 64, 64>;
  BIT_FIELD_REF <result$vx1, 64, 0> = _5;
  _6 = BIT_FIELD_REF <a$vx2_29, 64, 0>;
  BIT_FIELD_REF <result$vx2, 64, 64> = _6;
  _7 = BIT_FIELD_REF <a$vx3_30, 64, 64>;
  BIT_FIELD_REF <result$vx2, 64, 0> = _7;
  _8 = BIT_FIELD_REF <a$vx3_30, 64, 0>;
  BIT_FIELD_REF <result$vx3, 64, 64> = _8;
  _9 = BIT_FIELD_REF <_1, 64, 64>;
  BIT_FIELD_REF <result$vx3, 64, 0> = _9;
  _21 = result$vx0;
  MEM[(struct  *)&D.2369] = _21;
  _11 = result$vx1;
  MEM[(struct  *)&D.2369 + 16B] = _11;
  _25 = result$vx2;
  MEM[(struct  *)&D.2369 + 32B] = _25;
  _26 = result$vx3;
  MEM[(struct  *)&D.2369 + 48B] = _26;
  result$vx0 ={v} {CLOBBER};
  result$vx1 ={v} {CLOBBER};
  result$vx2 ={v} {CLOBBER};
  result$vx3 ={v} {CLOBBER};
  return D.2369;

}

I will spare you the terrible assembly code that we get as a result, but suffice it to say it is filled with unnecessary memory accesses when all this logic can be done efficiently in registers.

I'm not familiar with the tree-sra code, but a quick scan indicates there isn't any sort of target hook to indicate when pushing parameters to memory is a bad idea.  I'm guessing we need one.  Or is there another way that this behavior can be avoided?

There are a number of criteria in find_param_candidates to preclude scalarization, but nothing seems to obviously fit the condition of "the ABI in effect requests that you leave this guy alone."  The issue is complicated by the fact that scalarization would indeed be a reasonable thing to do if we have run out of protocol registers for a parameter; but I am willing to give that up if we can avoid lousy code in the common case.

Our ABI has the same issues if we replace vectors by float, double, or long double.

Any thoughts on how this should be addressed?


---


### compiler : `gcc`
### title : `re-align optimization blocks vectorization on powerpc`
### open_at : `2016-08-12T16:20:22Z`
### last_modified_date : `2021-10-01T02:58:12Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=74881
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `7.0`
### severity : `normal`
### contents :
Hi,
gcc.dg/vect/vect-117.c starts failing with patch at r238301.  After investigation I think it exposed a latent vectorizer issue.  Before patch, the loop is vectorized but guarded by alias check that is always false.  That is, the vectorized loop will never be executed in reality.  The patch only skips known to be false alias check.

Detailed analysis and possible fix is at https://gcc.gnu.org/ml/gcc-patches/2016-08/msg01035.html


---


### compiler : `gcc`
### title : `Missed VRP optimization`
### open_at : `2016-08-13T17:08:22Z`
### last_modified_date : `2022-01-12T07:14:40Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=76174
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `6.1.0`
### severity : `enhancement`
### contents :
The call to m is not removed from the following code:

void m();

void l(unsigned int r) {
  	unsigned int q = 0;
        unsigned int c = r;
        for (unsigned int x = 0; x<r; x++) {
            if (q == c) {
                m();
                c *= 2;
            }
            q++;
        }
}

if the line 'c *= 2' is removed the optimizer successfully optimizes away the body of the function.


---


### compiler : `gcc`
### title : `[11/12/13/14 Regression] XFAIL: gcc.dg/graphite/scop-dsyr2k.c scan-tree-dump-times graphite "number of SCoPs`
### open_at : `2016-08-15T17:19:21Z`
### last_modified_date : `2023-07-07T10:31:29Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=76957
### status : `NEW`
### tags : `deferred, missed-optimization, testsuite-fail, xfail`
### component : `tree-optimization`
### version : `7.0`
### severity : `normal`
### contents :
Created attachment 39449
graphite dump after r239357

Hi,

Graphite scan directives in gcc.dg/graphite/scop-dsyr2k.c and gcc.dg/graphite/scop-dsyrk.c started to fail on arm-none-eabi targets after r239357.

Number of SCoPs changed from 1 to 0 in both case. Please find attached a dump after the patch. If it is just a testism, please adjust component accordingly.


---


### compiler : `gcc`
### title : `Much worse code generated compared to clang (stack alignment and spills)`
### open_at : `2016-08-18T10:35:34Z`
### last_modified_date : `2021-08-25T06:22:52Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=77287
### status : `NEW`
### tags : `missed-optimization, ra`
### component : `target`
### version : `6.1.0`
### severity : `normal`
### contents :
A simple function (artificial code):

#include <immintrin.h>

int fn(
  const int* px, const int* py,
  const int* pz, const int* pw,
  const int* pa, const int* pb,
  const int* pc, const int* pd) {

  __m256i a0 = _mm256_loadu_si256((__m256i*)px);
  __m256i a1 = _mm256_loadu_si256((__m256i*)py);
  __m256i a2 = _mm256_loadu_si256((__m256i*)pz);
  __m256i a3 = _mm256_loadu_si256((__m256i*)pw);
  __m256i a4 = _mm256_loadu_si256((__m256i*)pa);
  __m256i b0 = _mm256_loadu_si256((__m256i*)pb);
  __m256i b1 = _mm256_loadu_si256((__m256i*)pc);
  __m256i b2 = _mm256_loadu_si256((__m256i*)pd);
  __m256i b3 = _mm256_loadu_si256((__m256i*)pc + 1);
  __m256i b4 = _mm256_loadu_si256((__m256i*)pd + 1);
  
  __m256i x0 = _mm256_packus_epi16(a0, b0);
  __m256i x1 = _mm256_packus_epi16(a1, b1);
  __m256i x2 = _mm256_packus_epi16(a2, b2);
  __m256i x3 = _mm256_packus_epi16(a3, b3);
  __m256i x4 = _mm256_packus_epi16(a4, b4);
  
  x0 = _mm256_add_epi16(x0, a0);
  x1 = _mm256_add_epi16(x1, a1);
  x2 = _mm256_add_epi16(x2, a2);
  x3 = _mm256_add_epi16(x3, a3);
  x4 = _mm256_add_epi16(x4, a4);

  x0 = _mm256_sub_epi16(x0, b0);
  x1 = _mm256_sub_epi16(x1, b1);
  x2 = _mm256_sub_epi16(x2, b2);
  x3 = _mm256_sub_epi16(x3, b3);
  x4 = _mm256_sub_epi16(x4, b4);
  
  x0 = _mm256_packus_epi16(x0, x1);
  x0 = _mm256_packus_epi16(x0, x2);
  x0 = _mm256_packus_epi16(x0, x3);
  x0 = _mm256_packus_epi16(x0, x4);
  return _mm256_extract_epi32(x0, 1);
}

Produces the following asm when compiled by GCC (annotated by me):

  ; GCC 6.1 -O2 -Wall -mavx2 -m32 -fomit-frame-pointer
  lea       ecx, [esp+4]                      ; Return address
  and       esp, -32                          ; Align the stack to 32 bytes
  push      DWORD PTR [ecx-4]                 ; Push returned address
  push      ebp                               ; Save frame-pointer even if I told GCC to not to
  mov       ebp, esp
  push      edi                               ; Save GP regs
  push      esi
  push      ebx
  push      ecx
  sub       esp, 296                          ; Reserve stack for YMM spills
  mov       eax, DWORD PTR [ecx+16]           ; LOAD 'pa'
  mov       esi, DWORD PTR [ecx+4]            ; LOAD 'py'
  mov       edi, DWORD PTR [ecx]              ; LOAD 'px'
  mov       ebx, DWORD PTR [ecx+8]            ; LOAD 'pz'
  mov       edx, DWORD PTR [ecx+12]           ; LOAD 'pw'
  mov       DWORD PTR [ebp-120], eax          ; SPILL 'pa'
  mov       eax, DWORD PTR [ecx+20]           ; LOAD 'pb'
  mov       DWORD PTR [ebp-152], eax          ; SPILL 'pb'
  mov       eax, DWORD PTR [ecx+24]           ; LOAD 'pc'
  vmovdqu   ymm4, YMMWORD PTR [esi]
  mov       ecx, DWORD PTR [ecx+28]           ; LOAD 'pd'
  vmovdqu   ymm7, YMMWORD PTR [edi]
  vmovdqa   YMMWORD PTR [ebp-56], ymm4        ; SPILL VEC
  vmovdqu   ymm4, YMMWORD PTR [ebx]
  mov       ebx, DWORD PTR [ebp-152]          ; LOAD 'pb'
  vmovdqa   YMMWORD PTR [ebp-88], ymm4        ; SPILL VEC
  vmovdqu   ymm4, YMMWORD PTR [edx]
  mov       edx, DWORD PTR [ebp-120]          ; LOAD 'pa'
  vmovdqu   ymm6, YMMWORD PTR [edx]
  vmovdqa   YMMWORD PTR [ebp-120], ymm6       ; SPILL VEC
  vmovdqu   ymm0, YMMWORD PTR [ecx]
  vmovdqu   ymm6, YMMWORD PTR [ebx]
  vmovdqa   ymm5, ymm0                        ; Why to move anything when using AVX?
  vmovdqu   ymm0, YMMWORD PTR [eax+32]
  vmovdqu   ymm2, YMMWORD PTR [eax]
  vmovdqa   ymm1, ymm0                        ; Why to move anything when using AVX?
  vmovdqu   ymm0, YMMWORD PTR [ecx+32]
  vmovdqa   YMMWORD PTR [ebp-152], ymm2
  vmovdqa   ymm3, ymm0                        ; Why to move anything when using AVX?
  vpackuswb ymm0, ymm7, ymm6
  vmovdqa   YMMWORD PTR [ebp-184], ymm5       ; SPILL VEC
  vmovdqa   YMMWORD PTR [ebp-248], ymm3       ; SPILL VEC
  vmovdqa   YMMWORD PTR [ebp-280], ymm0       ; SPILL VEC
  vmovdqa   ymm0, YMMWORD PTR [ebp-56]        ; ALLOC VEC
  vmovdqa   YMMWORD PTR [ebp-216], ymm1       ; SPILL VEC
  vpackuswb ymm2, ymm0, YMMWORD PTR [ebp-152] ; Uses SPILL slot
  vmovdqa   ymm0, YMMWORD PTR [ebp-88]        ; ALLOC VEC
  vpackuswb ymm1, ymm4, YMMWORD PTR [ebp-216] ; Uses SPILL slot
  vpackuswb ymm5, ymm0, YMMWORD PTR [ebp-184] ; Uses SPILL slot
  vmovdqa   ymm0, YMMWORD PTR [ebp-120]       ; ALLOC VEC
  vpaddw    ymm2, ymm2, YMMWORD PTR [ebp-56]  ; Uses SPILL slot
  vpsubw    ymm2, ymm2, YMMWORD PTR [ebp-152] ; Uses SPILL slot
  vpackuswb ymm3, ymm0, YMMWORD PTR [ebp-248] ; Uses SPILL slot
  vpaddw    ymm0, ymm7, YMMWORD PTR [ebp-280] ; Uses SPILL slot
  vpsubw    ymm0, ymm0, ymm6
  vmovdqa   ymm7, YMMWORD PTR [ebp-120]       ; ALLOC VEC
  vpackuswb ymm0, ymm0, ymm2
  vpaddw    ymm2, ymm4, ymm1
  vpsubw    ymm2, ymm2, YMMWORD PTR [ebp-216] ; Uses SPILL slot
  vmovdqa   YMMWORD PTR [ebp-312], ymm3       ; SPILL VEC
  vpaddw    ymm3, ymm5, YMMWORD PTR [ebp-88]  ; Uses SPILL slot
  vpsubw    ymm3, ymm3, YMMWORD PTR [ebp-184] ; Uses SPILL slot
  vpackuswb ymm0, ymm0, ymm3
  vpaddw    ymm1, ymm7, YMMWORD PTR [ebp-312] ; Uses SPILL slot
  vpsubw    ymm1, ymm1, YMMWORD PTR [ebp-248] ; Uses SPILL slot
  vpackuswb ymm0, ymm0, ymm2
  vpackuswb ymm0, ymm0, ymm1
  vpextrd   eax, xmm0, 1                      ; Return value
  vzeroupper
  add       esp, 296
  pop       ecx
  pop       ebx
  pop       esi
  pop       edi
  pop       ebp
  lea       esp, [ecx-4]
  ret

While clang produces just this:

  ; Clang 3.8 -O2 -Wall -mavx2 -m32 -fomit-frame-pointer
  mov       eax, dword ptr [esp + 32]     ; LOAD 'pd'
  mov       ecx, dword ptr [esp + 4]      ; LOAD 'px'
  vmovdqu   ymm0, ymmword ptr [ecx]
  mov       ecx, dword ptr [esp + 8]      ; LOAD 'py'
  vmovdqu   ymm1, ymmword ptr [ecx]
  mov       ecx, dword ptr [esp + 12]     ; LOAD 'pz'
  vmovdqu  ymm2, ymmword ptr [ecx]
  mov       ecx, dword ptr [esp + 16]     ; LOAD 'pw'
  vmovdqu   ymm3, ymmword ptr [ecx]
  mov       ecx, dword ptr [esp + 20]     ; LOAD 'pa'
  vmovdqu   ymm4, ymmword ptr [ecx]
  mov       ecx, dword ptr [esp + 24]     ; LOAD 'pb'
  vmovdqu   ymm5, ymmword ptr [ecx]
  mov       ecx, dword ptr [esp + 28]     ; LOAD 'pc'
  vpackuswb ymm6, ymm0, ymm5
  vpsubw    ymm0, ymm0, ymm5
  vmovdqu   ymm5, ymmword ptr [ecx]
  vpaddw    ymm0, ymm0, ymm6
  vpackuswb ymm6, ymm1, ymm5
  vpsubw    ymm1, ymm1, ymm5
  vmovdqu   ymm5, ymmword ptr [eax]
  vpaddw    ymm1, ymm1, ymm6
  vpackuswb ymm6, ymm2, ymm5
  vpsubw    ymm2, ymm2, ymm5
  vmovdqu   ymm5, ymmword ptr [ecx + 32]
  vpaddw    ymm2, ymm2, ymm6
  vpackuswb ymm6, ymm3, ymm5
  vpsubw    ymm3, ymm3, ymm5
  vmovdqu   ymm5, ymmword ptr [eax + 32]
  vpaddw    ymm3, ymm3, ymm6
  vpackuswb ymm6, ymm4, ymm5
  vpsubw    ymm4, ymm4, ymm5
  vpaddw    ymm4, ymm4, ymm6
  vpackuswb ymm0, ymm0, ymm1
  vpackuswb ymm0, ymm0, ymm2
  vpackuswb ymm0, ymm0, ymm3
  vpackuswb ymm0, ymm0, ymm4
  vpextrd   eax, xmm0, 1                  ; Return value
  vzeroupper
  ret

I have written about this in my blog here:  
  https://asmbits.blogspot.com/2016/08/comparing-register-allocator-of-gcc-and.html

Problems summary:

  1. Spilling GPRs in our case is not needed at all
  2. Spilling YMMs is also questionable as some instructions can be reordered, see clang output
  3. Frame pointer is preserved even when I compiled with -fomit-frame-pointer
  4. Using [ebp-X] instead of [esp+Y] produces longer code when `X > 128 && Y < 128`.

You can quickly verify the outputs by pasting the source here: https://gcc.godbolt.org/


---


### compiler : `gcc`
### title : `missed optimisation when copying/moving union members`
### open_at : `2016-08-19T06:48:53Z`
### last_modified_date : `2021-07-20T23:21:26Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=77295
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `6.1.1`
### severity : `enhancement`
### contents :
Discriminated unions of class types are becoming popular; for example std::variant<...> or std::future<T>.

gcc doesn't optimize copies or moved of discriminated unions well:


// Will usually be a template with user-defined types
// as members of the union
struct discriminated_union {
  unsigned which;
  union {
    int v1;
    long v2;
  };
  discriminated_union(discriminated_union&&);
};

discriminated_union::discriminated_union(discriminated_union&& x) {
  which = x.which;
  switch (x.which) {
  case 1:
    v1 = x.v1;
    break;
  case 2:
    v2 = x.v2;
    break;
  }
}


compiles into

   0:	8b 06                	mov    (%rsi),%eax
   2:	89 07                	mov    %eax,(%rdi)
   4:	8b 06                	mov    (%rsi),%eax
   6:	83 f8 01             	cmp    $0x1,%eax
   9:	74 1d                	je     28 <discriminated_union::discriminated_union(discriminated_union&&)+0x28>
   b:	83 f8 02             	cmp    $0x2,%eax
   e:	75 10                	jne    20 <discriminated_union::discriminated_union(discriminated_union&&)+0x20>
  10:	48 8b 46 08          	mov    0x8(%rsi),%rax
  14:	48 89 47 08          	mov    %rax,0x8(%rdi)
  18:	c3                   	retq   
  19:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)
  20:	f3 c3                	repz retq 
  22:	66 0f 1f 44 00 00    	nopw   0x0(%rax,%rax,1)
  28:	8b 46 08             	mov    0x8(%rsi),%eax
  2b:	89 47 08             	mov    %eax,0x8(%rdi)
  2e:	c3                   	retq   

instead of just copying the 12 bytes from (%rsi) into (rdi); unconditionally copying the long is cheaper than the branching.


---


### compiler : `gcc`
### title : `Bring memset + free optimisation to C++`
### open_at : `2016-08-21T17:19:39Z`
### last_modified_date : `2022-01-18T10:30:16Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=77307
### status : `NEW`
### tags : `missed-optimization`
### component : `c++`
### version : `6.1.1`
### severity : `enhancement`
### contents :
For the following code gcc will remove the call to memset:

void destroy(char *buf, size_t bufsize) {
  memset(buf, 0, bufsize);
  free(buf);
}

However if you change it to delete[] like this:

void destroy(char *buf, size_t bufsize) {
  memset(buf, 0, bufsize);
  delete[] buf;
}

memset is called. Tested on gcc.godbolt.org, Clang and ICC seem to behave in the same way.

In this case there are no destructors to run so the reasoning for removing the memset call should be the same for both cases (assuming the C++ standard does not have some weird requirements of which I am unaware).


---


### compiler : `gcc`
### title : `surprisingly large stack usage for sha512 on arm`
### open_at : `2016-08-21T17:42:28Z`
### last_modified_date : `2019-08-23T16:44:24Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=77308
### status : `RESOLVED`
### tags : `missed-optimization, ra`
### component : `target`
### version : `7.0`
### severity : `normal`
### contents :
Created attachment 39479
test case

I've noticed that openssl with no-asm but without -DOPENSSL_SMALL_FOOTPRINT
uses > 3600 byte of stack for a simple sha512 computation with -O3 on ARM.

Which is surprising, because on i386 the same function uses only 1016 byte,
and x86_64 uses only 256 bytes stack.

See the attached source code witch is stripped down from sha512.c


---


### compiler : `gcc`
### title : `-Wstrict-overflow pessimizes VRP in some cases for ABS_EXPR`
### open_at : `2016-08-26T01:25:30Z`
### last_modified_date : `2022-02-01T12:46:00Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=77387
### status : `RESOLVED`
### tags : `missed-optimization, needs-bisection`
### component : `tree-optimization`
### version : `6.1.0`
### severity : `normal`
### contents :
For testcase:

int foo (int i)
{
  int x = i;
  x = __builtin_abs (i);
  x >>= 24;
  if (x > 256)
    return 0;
  return x;
}

vrp1 dump is:
Value ranges after VRP:

_1: [-INF, 256]
i_2(D): VARYING
x_3: [0, +INF(OVF)]
x_4: VARYING
x_6: [257, +INF]  EQUIVALENCES: { x_4 } (1 elements)
x_7: [-INF, 256]  EQUIVALENCES: { x_4 } (1 elements)


Removing basic block 3
foo (int i)
{
  int x;
  int _1;

  <bb 2>:
  x_3 = ABS_EXPR <i_2(D)>;
  x_4 = x_3 >> 24;
  if (x_4 > 256)
    goto <bb 3>;
  else
    goto <bb 4>;

  <bb 3>:

  <bb 4>:
  # _1 = PHI <0(3), x_4(2)>
  return _1;

}


Note:
x_3: [0, +INF(OVF)]
x_4: VARYING


---


### compiler : `gcc`
### title : `Poor code generation for vector casts and loads`
### open_at : `2016-08-29T10:30:56Z`
### last_modified_date : `2021-08-13T23:00:18Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=77399
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `7.0`
### severity : `enhancement`
### contents :
For the following testcase:

typedef int   v4si __attribute__((vector_size(16)));
typedef float v4sf __attribute__((vector_size(16)));
v4sf vec_cast(v4si f)
{
  return (v4sf){f[0], f[1], f[2], f[3]};
}

(where unfortunately the c-style cast of the vector type has to be spelled out per-component, as '(v4sf)f' would mean a bitwise copy of the vector representation)

on x86-64 the generated should be just:

        cvtdq2ps        %xmm0, %xmm0
        retq

(and that is what Clang/LLVM generates), but GCC generates code that unpacks the input vector and converts each component separately.

Note that the issue arises only with vector types; when auto-vectorizing scalar code, GCC can use 'cvtdq2ps'. I believe this is because the original code is lowered to gimple using 4 BIT_FIELD_REFS, and the vectorizer doesn't handle that.


---


### compiler : `gcc`
### title : `Optimize integer i / abs (i) into the sign of i`
### open_at : `2016-08-29T20:04:26Z`
### last_modified_date : `2021-08-10T21:35:51Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=77407
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `7.0`
### severity : `enhancement`
### contents :
I found this gem in some glibc test case:

  if (c != 0)
    c /= abs (c);

This could turn into:

  if (c < 0)
    c = -1;
  else if (c > 0)
    c = 1;

This would eliminate the division and also paper of the bug (the unexpected 1 result for INT_MIN).


---


### compiler : `gcc`
### title : `Vector lowering should also consider larger vector sizes (MMX -> SSE)`
### open_at : `2016-09-01T02:48:21Z`
### last_modified_date : `2021-12-27T05:19:41Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=77438
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `6.2.1`
### severity : `normal`
### contents :
__m64 __attribute__((noinline)) mmx(__m64 x, __m64 y){return _mm_add_pi8(x,y);}

That gives 6 lines of assembly. (movq,movdq2q,paddb,movq,movq,ret) Stuff even gets moved to the stack. Good code would just do the operation in an xmm register instead of moving it to a mm register. Failing that, gcc could at least avoid using the stack.


---


### compiler : `gcc`
### title : `[7 Regression] Performance drop after r239219 on coremark test`
### open_at : `2016-09-01T12:36:52Z`
### last_modified_date : `2019-12-23T05:53:35Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=77445
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `7.0`
### severity : `normal`
### contents :
We noticed huge (32%) performance drop on coremark-pro/core (former coremark benchmark) after
http://gcc.gnu.org/viewcvs/gcc?view=revision&revision=239219

The problem part is 
   if (optimize_edge_for_speed_p (taken_edge))
which does not look correct since we have a lot of missed opportunities for jump threading optimization like:

test.c.111t.thread2:FSM jump-thread path not considered: duplication of 4 insns is needed and optimizing for size.
test.c.111t.thread2:FSM jump-thread path not considered: duplication of 4 insns is needed and optimizing for size.
test.c.111t.thread2:FSM jump-thread path not considered: duplication of 4 insns is needed and optimizing for size.
test.c.111t.thread2:FSM jump-thread path not considered: duplication of 4 insns is needed and optimizing for size.
test.c.111t.thread2:FSM jump-thread path not considered: duplication of 4 insns is needed and optimizing for size.
test.c.111t.thread2:FSM jump-thread path not considered: duplication of 4 insns is needed and optimizing for size.
test.c.111t.thread2:FSM jump-thread path not considered: duplication of 5 insns is needed and optimizing for size.
test.c.111t.thread2:FSM jump-thread path not considered: duplication of 5 insns is needed and optimizing for size.
test.c.111t.thread2:FSM jump-thread path not considered: duplication of 5 insns is needed and optimizing for size.
test.c.167t.thread3:FSM jump-thread path not considered: duplication of 5 insns is needed and optimizing for size.
test.c.167t.thread3:FSM jump-thread path not considered: duplication of 5 insns is needed and optimizing for size.
test.c.167t.thread3:FSM jump-thread path not considered: duplication of 5 insns is needed and optimizing for size.
test.c.167t.thread3:FSM jump-thread path not considered: duplication of 5 insns is needed and optimizing for size.
test.c.167t.thread3:FSM jump-thread path not considered: duplication of 5 insns is needed and optimizing for size.
test.c.167t.thread3:FSM jump-thread path not considered: duplication of 5 insns is needed and optimizing for size.
test.c.167t.thread3:FSM jump-thread path not considered: duplication of 4 insns is needed and optimizing for size.
test.c.167t.thread3:FSM jump-thread path not considered: duplication of 4 insns is needed and optimizing for size.
test.c.167t.thread3:FSM jump-thread path not considered: duplication of 4 insns is needed and optimizing for size.
test.c.170t.thread4:FSM jump-thread path not considered: duplication of 5 insns is needed and optimizing for size.
test.c.170t.thread4:FSM jump-thread path not considered: duplication of 5 insns is needed and optimizing for size.
test.c.170t.thread4:FSM jump-thread path not considered: duplication of 5 insns is needed and optimizing for size.
test.c.170t.thread4:FSM jump-thread path not considered: duplication of 5 insns is needed and optimizing for size.
test.c.170t.thread4:FSM jump-thread path not considered: duplication of 5 insns is needed and optimizing for size.
test.c.170t.thread4:FSM jump-thread path not considered: duplication of 5 insns is needed and optimizing for size.
test.c.170t.thread4:FSM jump-thread path not considered: duplication of 4 insns is needed and optimizing for size.
test.c.170t.thread4:FSM jump-thread path not considered: duplication of 4 insns is needed and optimizing for size.
test.c.170t.thread4:FSM jump-thread path not considered: duplication of 4 insns is needed and optimizing for size.

If we change it to
  if (!optimize_function_for_size_p (cfun))
performance is back.
I attach the test-case to reproduce issue.


---


### compiler : `gcc`
### title : `Suboptimal code when returning a string generated with a constexpr fn at compile time`
### open_at : `2016-09-02T14:19:36Z`
### last_modified_date : `2021-12-01T23:55:54Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=77456
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `c++`
### version : `7.0`
### severity : `normal`
### contents :
Created attachment 39541
C++ source

I ran into this when converting expression trees to strings at compile time. Though it's surely a rare application, the fix might have positive impact on a wider range of scenarios.

The attached code converts the integers [0..N] to a string at compile time. There are several conversions with differing N's. Also, some conversions calculate the exact size of the resulting strings, others just use a large enough buffer.

Platform is is Debian Jessie, x86-64. Tested w/ 6.x and 7.0. To compile:
g++ -std=c++14 -Wall -Wextra -O3 20160831-constexpr.cpp

Please be patient, this takes almost 30 secs on my machine (AMD FX 8150 @ 4GHz), due to lots of compile-time constexpr work.

foo(): [0..13] w/ a 200 byte buffer. It seems that the initial zero fill of the buffer is not considered in dead-store elimination, so the 200 bytes are rep stos'd, then the actual characters are copied via xmm0 and bytewise literal stores:

Dump of assembler code for function _Z3foov:
   0x0000000000400620 <+0>:     mov    %rdi,%rdx
   0x0000000000400623 <+3>:     movq   $0x0,0xc0(%rdi)
   0x000000000040062e <+14>:    lea    0x8(%rdi),%rdi
   0x0000000000400632 <+18>:    mov    %rdx,%rcx
   0x0000000000400635 <+21>:    movdqa 0x27033(%rip),%xmm0        # 0x427670
   0x000000000040063d <+29>:    and    $0xfffffffffffffff8,%rdi
   0x0000000000400641 <+33>:    xor    %eax,%eax
   0x0000000000400643 <+35>:    sub    %rdi,%rcx
   0x0000000000400646 <+38>:    add    $0xc8,%ecx
   0x000000000040064c <+44>:    shr    $0x3,%ecx
   0x000000000040064f <+47>:    rep stos %rax,%es:(%rdi)
   0x0000000000400652 <+50>:    movups %xmm0,(%rdx)
   0x0000000000400655 <+53>:    movb   $0x38,0x10(%rdx)
   0x0000000000400659 <+57>:    movb   $0x20,0x11(%rdx)
   0x000000000040065d <+61>:    mov    %rdx,%rax
   0x0000000000400660 <+64>:    movb   $0x39,0x12(%rdx)
   0x0000000000400664 <+68>:    movb   $0x20,0x13(%rdx)
   0x0000000000400668 <+72>:    movb   $0x31,0x14(%rdx)
   0x000000000040066c <+76>:    movb   $0x30,0x15(%rdx)
   0x0000000000400670 <+80>:    movb   $0x20,0x16(%rdx)
   0x0000000000400674 <+84>:    movb   $0x31,0x17(%rdx)
   0x0000000000400678 <+88>:    movb   $0x31,0x18(%rdx)
   0x000000000040067c <+92>:    movb   $0x20,0x19(%rdx)
   0x0000000000400680 <+96>:    movb   $0x31,0x1a(%rdx)
   0x0000000000400684 <+100>:   movb   $0x32,0x1b(%rdx)
   0x0000000000400688 <+104>:   movb   $0x20,0x1c(%rdx)
   0x000000000040068c <+108>:   movb   $0x31,0x1d(%rdx)
   0x0000000000400690 <+112>:   movb   $0x33,0x1e(%rdx)
   0x0000000000400694 <+116>:   retq   

Since the buffer is larger, all the movb's could have been converted to another xmm0 load+store. Though an explicit zero byte is written in the C++ code after the last digit, this is missing in the disassembly above, so there is no "movb $0x00, 0x1f(%rdx)" at the end, meaning that the compiler eliminated this store, instead of merging all the 16 byte stores into a single xmm0 operation, and skipping the first 32 bytes in the rep stos.

foo_sized() generates the same string, but first it calculates the needed size. There is no zero fill here in the asm, so it was successfully eliminated, and the characters are initialized via two xmm0 loads/stores, as expected:

Dump of assembler code for function _Z9foo_sizedv:
   0x00000000004006a0 <+0>:     movdqa 0x26fc8(%rip),%xmm0        # 0x427670
   0x00000000004006a8 <+8>:     mov    %rdi,%rax
   0x00000000004006ab <+11>:    movups %xmm0,(%rdi)
   0x00000000004006ae <+14>:    movdqa 0x26fca(%rip),%xmm0        # 0x427680
   0x00000000004006b6 <+22>:    movups %xmm0,0x10(%rdi)
   0x00000000004006ba <+26>:    retq   

bar/bar_sized/bar_static/bar_sized_static(): the same as foo, but the range is [0..42], and the static versions use a static constexpr, and return the buffer pointer, not the buffer by value. 

bar() zero fills and then copies over with xmm0 and byte literals. bar_sized() lacks the zero fill, but initializes the characters the same way. The static versions just return a pointer as expected.

baz_sized() works as expected: since the memory to copy is large, it calls memcpy instead of doing the above xmm0 + literal bytes stuff.

The problem is with baz(). The range is much larger, [0..4200]. There is no DSE here either, so the buffer is first zeroed with memset, but then ALL the characters are initialized via bytewise literal stores, resulting in very large function, around 138K. Why didn't the logic kicked in that replaced the in-place init with memcpy? Or, at least, much of the copy could have been done with xmm0, copying 16 bytes at once.

One more thing: if you disable the return in fixbuf() via setting the #if 1 to 0 at line 76, interesting things will happen:

6.2.1:
g++-6.2.1 -std=c++14 -Wall -Wextra -O3 20160831-constexpr.cpp 
‘
20160831-constexpr.cpp:83: confused by earlier errors, bailing out

In a terminal window with black bg and gray font, the single quote is gray, then the error message on the next line is bold white, and it stays so, so anything I type after this will be bold white.

7.0.0: an earlier version did the same, but two days ago I built a fresh version and now it crashes:
g++-7.0.0 -std=c++14 -Wall -Wextra -O3 20160831-constexpr.cpp 
‘
In function ‘auto foo()’:
Segmentation fault
  constexpr auto x = fixbuf<13, 200>();
                                     ^
Please submit a full bug report,

The exact gcc versions used:

$ g++-6.2.1 -v
Using built-in specs.
COLLECT_GCC=g++-6.2.1
COLLECT_LTO_WRAPPER=/usr/local/libexec/gcc/x86_64-pc-linux-gnu/6.2.1/lto-wrapper
Target: x86_64-pc-linux-gnu
Configured with: ../configure --enable-languages=c,c++ --disable-multilib --program-suffix=-6.2.1 --disable-bootstrap CFLAGS='-O2 -march=native' CXXFLAGS='-O2 -march=native'
Thread model: posix
gcc version 6.2.1 20160831 (GCC) 
git b823cdd4ccc1499a674e3863ce875c7459207727

g++-7.0.0 -v 
Using built-in specs.
COLLECT_GCC=g++-7.0.0
COLLECT_LTO_WRAPPER=/usr/local/libexec/gcc/x86_64-pc-linux-gnu/7.0.0/lto-wrapper
Target: x86_64-pc-linux-gnu
Configured with: ../configure --enable-languages=c,c++ --disable-multilib --program-suffix=-7.0.0 --disable-bootstrap CFLAGS='-O2 -march=native' CXXFLAGS='-O2 -march=native'
Thread model: posix
gcc version 7.0.0 20160831 (experimental) (GCC)
git 14c36b15d931bf299bbc214707b903d0af124449


---


### compiler : `gcc`
### title : `[11/12/13/14 Regression] Regression after code-hoisting, due to combine pass failing to evaluate known value range`
### open_at : `2016-09-06T15:48:41Z`
### last_modified_date : `2023-09-02T21:54:19Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=77499
### status : `NEW`
### tags : `deferred, missed-optimization`
### component : `rtl-optimization`
### version : `7.0`
### severity : `normal`
### contents :
Hello,

We are seeing a regression for arm-none-eabi on a Cortex-M7. This regression was observed after Biener's and Bosscher's GIMPLE code-hoisting patch (https://gcc.gnu.org/ml/gcc-patches/2016-07/msg00360.html). The example below will illustrate the regression:

$ cat t.c
unsigned short foo (unsigned short x, int c, int d, int e)
{
  unsigned short y;

  while (c > d)
    {
      if (c % 3)
	{
	 x = (x >> 1) ^ 0xB121U;
	}
      else
	 x = x >> 1;
      c-= e;
    }
  return x;
}

Comparing:
$ arm-none-eabi-gcc -mcpu=cortex-m7 -mthumb -O2 -S t.c 
vs
$ arm-none-eabi-gcc -mcpu=cortex-m7 -mthumb -O2 -S t.c -fno-code-hoisting

Will illustrate that the code-hoisting version has an extra zero_extension of HImode to SImode. After some digging I found out that during the combine phase, the no-code-hoisting version is able to recognize that the 'last_set_nonzero_bits' are 0x7fff whereas for the code-hoisted version it seems to have lost this knowledge.

Looking at the graph dump for the no-code-hoisting t.c.246r.ud_dce.dot I see the following insns:
23: r125:SI=r113:SI 0>>0x1
24: r111:SI=zero_extend(r125:SI#0)
27: r128:SI=r111:SI^r131:SI
28: r113:SI=zero_extend(r128:SI#0)

These are all in the same basic block. 

For the code-hoisting version we have:

BB A:
...
12: r116:SI=r112:SI 0>>0x1
13: r112:SI=zero_extend(r116:SI#0)
...
BB B:
27: r127:SI=r112:SI^r129:SI
28: r112:SI=zero_extend(r127:SI#0)


Now from what I have observed by debugging the combine pass is that combine will first combine instructions 23 and 24. 
Here combine is able to optimize away the zero_extend, because in 'reg_nonzero_bits_for_combine' the reg_stat[113] has its 'last_set_value' to 'r0' (the unsigned short argument) and its corresponding 'last_set_nonzero_bits' to 0xffffffff0000ffff. Which means the zero_extend is pointless. The code-hoisting version also combines 12 and 13, optimizing away the zero_extend.

However, the next set of instructions is where things get tricky. In the no-code-hoisting case it will end up combining all 4 instructions one by one from the top down and it will end up figuring out that the last zero_extend is also not required. For the code-hoisting case, when it tries to combine 28 with 27 (remember they are not in the basic block as 13 and 14, so it will never try to combine all 4), it will eventually try to evaluate the nonzero bits based on r112 and see that the last_set_value for r112 is:
(lshiftrt:SI (clobber:SI (const_int 0 [0]))
(const_int 1 [0x1]))

The last_set_nonzero_bits will be 0x7fffffff, instead of the expected 0x00007fff. This looks like the result of the code in 'record_value_for_reg' in combine.c that sits bellow the comment:

  /* The value being assigned might refer to X (like in "x++;").  In that
     case, we must replace it with (clobber (const_int 0)) to prevent
     infinite loops.  */

Given that 12 and 13 were combined into:
r112:SI=r112:SI 0>>0x1

This seems to be invalidating the last_set_value and thus leaving us with a weaker 'last_set_nonzero_bits' which isn't enough to optimize away the zero_extend.

Any clue on how to "fix" this?

Cheers,
Andre

PS: I am not sure I completely understand the way the last_set_value stuff works for pseudo's in combine, but it looks to me like each instruction is visited in a top down order per basic block again in a top-down order. And each pseudo will have its 'last_set_value' according to the last time that register was seen being set, without any regards to loop or proper dataflow analysis. Can anyone explain to me how this doesnt go horribly wrong?


---


### compiler : `gcc`
### title : `[11/12/13/14 regression] CSE/PRE/Hoisting blocks common instruction contractions`
### open_at : `2016-09-12T17:59:22Z`
### last_modified_date : `2023-08-03T17:58:47Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=77568
### status : `NEW`
### tags : `FIXME, missed-optimization`
### component : `tree-optimization`
### version : `7.0`
### severity : `normal`
### contents :
The recently introduced code hoisting aggressively moves common subexpressions that might otherwise be mergeable with other operations. This caused a large regression in one benchmark. A simple reduced test shows the issue:

float f(float x, float y, float z, int a)
{
   if (a > 100)
     x += y * z;
   else
     x -= y * z;
   return x;
}

This now produces on AArch64:

f:
	fmul	s2, s1, s2
	cmp	w0, 100
	fadd	s1, s0, s2
	fsub	s0, s0, s2
	fcsel	s0, s0, s1, le
	ret

Note the issue is not limited to hoisting, CSE/PRE cause similar issues:

void g(int, int);
int f2(int x)
{
  g(x, x+1);
  g(x, x+1);
  return x+1;
}

f2:
	stp	x29, x30, [sp, -32]!
	add	x29, sp, 0
	stp	x19, x20, [sp, 16]
	add	w19, w0, 1
	mov	w20, w0
	mov	w1, w19
	bl	g
	mov	w1, w19
	mov	w0, w20
	bl	g
	mov	w0, w19
	ldp	x19, x20, [sp, 16]
	ldp	x29, x30, [sp], 32
	ret

Given x+1 is used as a function argument, there is no benefit in making it available as a CSE after each call - repeating the addition is cheaper than using an extra callee-save and copying it several times.

This shows a similar issue for bit tests. Most targets support ANDS or bit test as a single instruction (or even bit test+branch), so CSEing the (x & C) actually makes things worse:

void f3(char *p, int x)
{
  if (x & 1) p[0] = 0;
  if (x & 2) p[1] = 0;
  if (x & 4) p[2] = 0;
  if (x & 8) p[2] = 0;
  g(0,0);
  if (x & 1) p[3] = 0;
  if (x & 2) p[4] = 0;
  if (x & 4) p[5] = 0;
  if (x & 8) p[6] = 0;
}

This uses 4 callee-saves to hold the (x & C) CSEs. Doing several such bit tests in a more complex function means you quickly run out of registers...

Given it would be much harder to undo these CSEs at RTL level (combine does most contractions but can only do it intra-block), would it be reasonable to block CSEs for these special cases?


---


### compiler : `gcc`
### title : `Missed multiple add (int) for CSEd case`
### open_at : `2016-09-13T14:01:22Z`
### last_modified_date : `2023-05-16T20:06:10Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=77579
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `7.0`
### severity : `enhancement`
### contents :
Take:
float g(float);
void f(float x, float y, float z, float *s)
{
   float t = y * z;
   s[0] = t+x;
   s[1] = x - t;
}


--- CUT ---
This works at -O2.  Now if you change float to int (-Dfloat=int), we don't get madd/msub but if we disable either stores, we do get them.

This might be solved by changing "madd<mode>" to "fma<mode>4" (and making sure the correct order of the operands).  Obviously I have not tried it yet and might not have time any time soon.


---


### compiler : `gcc`
### title : `register allocation shoud not occupy register for return value early`
### open_at : `2016-09-20T18:22:00Z`
### last_modified_date : `2022-02-06T09:39:57Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=77668
### status : `UNCONFIRMED`
### tags : `missed-optimization, ra`
### component : `rtl-optimization`
### version : `7.0`
### severity : `normal`
### contents :
when return value is declared (or, RVO introduced returning this pointer), RA seems to be very greedy on occupying r0(eax/rax) for the return value, even if the return value is not used yet.

With such RA strategy, the quick register reserved for return value is no longer usable for tmp variables.

Here is just one simple example demonstrating this issue:
compile with -m32 -O[anylevel] targeting Intel x86
always able to reproduce on gcc 4.x to 6.2.0 and on 7.0 snapshots.

getA() is where RVO is applied, resulting "this" pointer (for returning) occupying one register.
In total, 4 registers used. The life-scope of "this" pointer and one tmp variable don't overlap, where 1 register should be enough, but 2 registers allocated.

getA_RVO() with the complex syntax is where we 'manually' do the RVO stuff to make the function prototype identical to RVO'ed getA() (calling convention on returning stack poping is not same, though)
in getA_RVO(), I just showed up that we can use the same register for ret (eax) as a temp register before we actually start using it, thus only 3 registers used.

getA_RVO2() is just a simple test to clarify the problem is not caused by RVO, as we manually declare the return var and assign to it, but the return var still extended its life-span. So likely the problem is caused by RA being greedy on ret reg.


struct A {
  int a;
  int b;
  int c;
   
  A(int i, int j) {
    int tmp;
    int h = i;
    int e;
    __asm__ __volatile__( //do something in assembly
      "or $123, %0;"
      "mov %0, %1;"
      "xor $234, %1;"
      "lea 20(%0), %2;"
      : "+r"(h), "=r"(tmp), "=r"(e)
    );
    b = h;
    c = e;
    a = j;
  }
};


A getA(int i, int j) {
  return A(i, j);
}

getA(int, int):
 push   %ebx
 mov    0x8(%esp),%eax
 mov    0xc(%esp),%edx
 or     $0x7b,%edx
 mov    %edx,%ebx
 xor    $0xea,%ebx
 lea    0x14(%edx),%ecx
 mov    %edx,0x4(%eax)
 mov    0x10(%esp),%edx
 mov    %ecx,0x8(%eax)
 mov    %edx,(%eax)
 pop    %ebx
 ret    $0x4

A* getA_RVO(A* src, int i, int j) {
  A* ret;
  int h = i;
  int e;
  __asm__ __volatile__(
    "or $123, %0;"
    "mov %0, %1;"
    "xor $234, %1;"
    "lea 20(%0), %2;"
    "mov %3, %1;"  //switch this line with ret = src
    : "+r"(h), "=r"(ret), "=r"(e)
    : "rm"(src)
  );
  //ret = src;
  ret->b = h;
  ret->c = e;
  ret->a = j;
  return ret;
}

getA_RVO(A*, int, int):
 mov    0x8(%esp),%edx
 or     $0x7b,%edx
 mov    %edx,%eax
 xor    $0xea,%eax
 lea    0x14(%edx),%ecx
 mov    0x4(%esp),%eax
 mov    %edx,0x4(%eax)
 mov    0xc(%esp),%edx
 mov    %ecx,0x8(%eax)
 mov    %edx,(%eax)
 ret    

//switch the commented lines in getA_RVO() to get getA_RVO2

getA_RVO2(A*, int, int):
 push   %ebx
 mov    0x8(%esp),%eax
 mov    0xc(%esp),%edx
 or     $0x7b,%edx
 mov    %edx,%ebx
 xor    $0xea,%ebx
 lea    0x14(%edx),%ecx
 mov    %edx,0x4(%eax)
 mov    0x10(%esp),%edx
 mov    %ecx,0x8(%eax)
 mov    %edx,(%eax)
 pop    %ebx
 ret


---


### compiler : `gcc`
### title : `Missing vectorization lead to huge performance loss`
### open_at : `2016-09-22T10:30:50Z`
### last_modified_date : `2023-07-28T14:19:31Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=77689
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `6.2.1`
### severity : `enhancement`
### contents :
Created attachment 39673
Asm code of the main, generated by gcc and icc

I recently started using auto-vectorization as much as possible. Unfortunately, I discovered that gcc is often unable to vectorize code.
I wrote a very simple MWE which (unfortunately, from my point of view) performs around 11X faster if compiled with icc instead of gcc.

Here is the code:

#include <vector>
#include <cmath>

constexpr unsigned s = 100000000;

int main()
{
    std::vector<float> a, b, c;
    a.reserve(s);
    b.reserve(s);
    c.reserve(s);

    for(unsigned i = 0; i < s; ++i)
    {
        if(i == 0)
            a[i] = b[i] * c[i];
        else
            a[i] = (b[i] + c[i]) * c[i-1] * std::log(i);
    }
}

I attach the generated assembly with both compiler. I hope that it could help someone try improving the vectorization procedures.


---


### compiler : `gcc`
### title : `Optimize away some static constructors`
### open_at : `2016-09-23T09:38:04Z`
### last_modified_date : `2021-08-03T19:14:07Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=77705
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `7.0`
### severity : `enhancement`
### contents :
struct S { int a; };
void baz (S *);
#if __cpp_constexpr >= 200704
constexpr
#endif
inline S foo () { return (S) { 2 }; }

S s = foo ();

for -std=c++98 -O2 we have the runtime initializer.  If we had some pass that would analyze the ctor functions after they were inlined into and if they only write constants into file-scope vars defined in the current TU (except for comdat vars?) turn the ctor function into static initializers for the file-scope vars.
Not sure if we can do it generally for any (non-comdat?) vars, or if e.g. the C++ FE wouldn't have to mark such vars some way for us, or if we wouldn't need to analyze if there aren't some ctors in the same TU that would run earlier (higher (or is that lower?) priority) and could access those vars, or for vars visible outside of the TU if some other TU's ctor couldn't access them.
An argument for some guidance from the C++ FE would be that say in C:
int a __attribute__((nocommon));
static __attribute__((constructor)) void
foo (void)
{
  a = 6;
}
some other TU could say in heither priority ctor expect to see a == 0.


---


### compiler : `gcc`
### title : `Optimize away some local static constructors`
### open_at : `2016-09-23T09:41:14Z`
### last_modified_date : `2021-12-20T20:24:12Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=77706
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `7.0`
### severity : `enhancement`
### contents :
Similar to PR77705, but even harder:

struct S { int a; };
void baz (S *);
#if __cpp_constexpr >= 200704
constexpr
#endif
inline S foo () { return (S) { 2 }; }

void
bar ()
{
  static S t = foo ();
  baz (&t);
}

inline void
bar2 ()
{
  static S t = foo ();
  baz (&t);
}

void
bar3 ()
{
  bar2 ();
}

Here we have:
  static struct S t;
  unsigned char _1;
  int _2;

  <bb 2>:
  _1 = __atomic_load_1 (&_ZGVZ3barvE1t, 2);
  if (_1 == 0)
    goto <bb 4>;
  else
    goto <bb 3>;

  <bb 3>:
  goto <bb 6>;

  <bb 4>:
  _2 = __cxa_guard_acquire (&_ZGVZ3barvE1t);
  if (_2 != 0)
    goto <bb 5>;
  else
    goto <bb 3>;

  <bb 5>:
  MEM[(struct S *)&t] = 2;
  __cxa_guard_release (&_ZGVZ3barvE1t);

  <bb 6>:

it would be nice to turn that into static struct S t = { 2 }; and get rid of the guard var and atomics/__cxa_guard*, but we need to consider ABI issues if the guard var is visible outside of the TU.


---


### compiler : `gcc`
### title : `unnecessary trap checks for pointer subtraction with -ftrapv`
### open_at : `2016-09-28T15:01:07Z`
### last_modified_date : `2021-12-23T05:13:09Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=77779
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `5.4.1`
### severity : `minor`
### contents :
Consider this code:

long diff(long *a, long *b) { return (a - b) + (a - b); }

Compiled with gcc -O2 -ftrapv on x86-64 the resulting code is

diff:
.LFB0:
	.cfi_startproc
	subq	$8, %rsp
	.cfi_def_cfa_offset 16
	call	__subvdi3
	sarq	$3, %rax
	movq	%rax, %rdi
	movq	%rax, %rsi
	call	__addvdi3
	addq	$8, %rsp
	.cfi_def_cfa_offset 8
	ret
	.cfi_endproc
.LFE0:
	.size	diff, .-diff


There are two problems here -- not bugs, but suboptimal code.

1. Pointer subtraction of sizes larger than 2 bytes should not generate a trapping subtract.  In the usual case where pointers and ptrdiff_t are the same size, the result will fit in a ptrdiff_t.

2. The addition can not overflow.  In general, x/A + y/B with A and B both greater than 2 will not overflow.  (This might not be worth fixing, but I think the previous problem is.)

I contrived this C example after seeing the first problem in C++.  The real code is a call to

   std::vector<T>::size()

with type T 4 bytes or larger.  size() can't overflow, but g++ inserts a call to __subvdi3 anyway.  On Linux+ELF this results in a dynamic linker operation.

This is in 5.2 and 5.4.1 20160926.  I have not checked gcc 6+.


---


### compiler : `gcc`
### title : `A jump threading opportunity with conditionals`
### open_at : `2016-10-02T21:04:42Z`
### last_modified_date : `2021-08-22T01:30:11Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=77820
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `7.0`
### severity : `enhancement`
### contents :
Consider the following code:

===
void g(void);

void f(long a, long b, long c, long d, int x)
{
        int t;
        if (x)
                t = a < b;
        else
                t = c < d;
        if (t)
                g();
}
===

On aarch64 we generate: (it is worse on PowerPC, but this is shorter code)

===
f:
        cbz     w4, .L2
        cmp     x0, x1
        cset    w0, lt
        cbnz    w0, .L6
.L1:
        ret
        .p2align 3
.L2:
        cmp     x2, x3
        cset    w0, lt
        cbz     w0, .L1
.L6:
        b       g
===

while if jump threading was a bit smarter we could generate:

===
f:
        cbz     w4, .L2
        cmp     x0, x1
        blt     .L3
.L1:
        ret
        .p2align 3
.L2:
        cmp     x2, x3
        bge     .L1
.L3:
        b       g
===

(i.e., do the "if (t)" in both branches of the first "if").


---


### compiler : `gcc`
### title : `Simplify (x>>4)*16 in gimple`
### open_at : `2016-10-03T20:33:24Z`
### last_modified_date : `2023-07-13T18:31:12Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=77836
### status : `NEW`
### tags : `missed-optimization, TREE`
### component : `tree-optimization`
### version : `7.0`
### severity : `enhancement`
### contents :
unsigned f(unsigned x){ return (x>>4)*16; }

gives the optimized dump

  _1 = x_2(D) >> 4;
  _3 = _1 * 16;

while (x/16)*16 and (x>>4)<<4 are optimized to

  _2 = x_1(D) & 4294967280;


---


### compiler : `gcc`
### title : `Odd code for _Complex float return value`
### open_at : `2016-10-04T22:16:10Z`
### last_modified_date : `2021-08-07T05:28:17Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=77851
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `7.0`
### severity : `normal`
### contents :
[hjl@gnu-6 gcc]$ cat /tmp/c.c 
_Complex float
foo (_Complex float y)
{
  return y;
}
[hjl@gnu-6 gcc]$ ./xgcc -B./ -S /tmp/c.c -O3
[hjl@gnu-6 gcc]$ cat c.s 
	.file	"c.c"
	.text
	.p2align 4,,15
	.globl	foo
	.type	foo, @function
foo:
.LFB0:
	.cfi_startproc
	movq	%xmm0, -8(%rsp)
	movss	-8(%rsp), %xmm0
	movss	%xmm0, -16(%rsp)
	movss	-4(%rsp), %xmm0
	movss	%xmm0, -12(%rsp)
	movq	-16(%rsp), %xmm0
	ret
	.cfi_endproc
.LFE0:
	.size	foo, .-foo
	.ident	"GCC: (GNU) 7.0.0 20161004 (experimental)"
	.section	.note.GNU-stack,"",@progbits
[hjl@gnu-6 gcc]$ 

It should be simply "ret".


---


### compiler : `gcc`
### title : `missed optimization in switch of modulus value`
### open_at : `2016-10-06T00:14:52Z`
### last_modified_date : `2022-02-21T05:22:10Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=77877
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `7.0`
### severity : `enhancement`
### contents :
Compile this code with a recent trunk gcc:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
int zero;
int one;
int two;

extern unsigned compute_mod(unsigned);

void cnt(unsigned n) {
#ifdef HIDE
  n = compute_mod(n);
#else
  n %= 3;
#endif
  switch (n) {
  case 0: ++zero; break;
  case 1: ++one; break;
  case 2: ++two; break;
#ifdef OPT
  default: __builtin_unreachable();
#endif
  }
}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

On x86-64, without HIDE defined, the code compiles with -O3 to:

   0:	89 f8                	mov    %edi,%eax
   2:	ba ab aa aa aa       	mov    $0xaaaaaaab,%edx
   7:	f7 e2                	mul    %edx
   9:	d1 ea                	shr    %edx
   b:	8d 04 52             	lea    (%rdx,%rdx,2),%eax
   e:	29 c7                	sub    %eax,%edi
  10:	83 ff 01             	cmp    $0x1,%edi
  13:	74 1b                	je     30 <_Z3cntj+0x30>
  15:	83 ff 02             	cmp    $0x2,%edi
  18:	75 0e                	jne    28 <_Z3cntj+0x28>
  1a:	83 05 00 00 00 00 01 	addl   $0x1,0x0(%rip)        # 21 <_Z3cntj+0x21>
  21:	c3                   	retq   
  22:	66 0f 1f 44 00 00    	nopw   0x0(%rax,%rax,1)
  28:	83 05 00 00 00 00 01 	addl   $0x1,0x0(%rip)        # 2f <_Z3cntj+0x2f>
  2f:	c3                   	retq   
  30:	83 05 00 00 00 00 01 	addl   $0x1,0x0(%rip)        # 37 <_Z3cntj+0x37>
  37:	c3                   	retq   


This is good, the compiler knows there are only three possible values and does not emit any code for a default case.

If I make sure the compiler doesn't know anything about the arithmetic operation by calling a function but telling the compiler there is no other case by using __builtin_unreachable() then the generated code is even better:

   0:	48 83 ec 08          	sub    $0x8,%rsp
   4:	e8 00 00 00 00       	callq  9 <_Z3cntj+0x9>
   9:	83 f8 01             	cmp    $0x1,%eax
   c:	74 22                	je     30 <_Z3cntj+0x30>
   e:	72 10                	jb     20 <_Z3cntj+0x20>
  10:	83 05 00 00 00 00 01 	addl   $0x1,0x0(%rip)        # 17 <_Z3cntj+0x17>
  17:	48 83 c4 08          	add    $0x8,%rsp
  1b:	c3                   	retq   
  1c:	0f 1f 40 00          	nopl   0x0(%rax)
  20:	83 05 00 00 00 00 01 	addl   $0x1,0x0(%rip)        # 27 <_Z3cntj+0x27>
  27:	48 83 c4 08          	add    $0x8,%rsp
  2b:	c3                   	retq   
  2c:	0f 1f 40 00          	nopl   0x0(%rax)
  30:	83 05 00 00 00 00 01 	addl   $0x1,0x0(%rip)        # 37 <_Z3cntj+0x37>
  37:	48 83 c4 08          	add    $0x8,%rsp
  3b:	c3                   	retq   

There is only one compare instruction.  This is how even the first case should look like.

Even more interesting: just defining the OPT macro does not change anything.  So, there is currently no way to get the optimal behaviour.  We certainly don't want to artificially the function calls.


---


### compiler : `gcc`
### title : `missing optimization on strlen(p + offset) with a bounded offset`
### open_at : `2016-10-06T23:53:44Z`
### last_modified_date : `2021-10-13T16:18:42Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=77889
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `7.0`
### severity : `normal`
### contents :
While testing my patch for bug 77608 I noticed another case of the same limitation, this one in the tree-ssa-strlen pass.  The test case below shows that while (with my patch) __builtin_object_size is able to compute the range the smallest sizes of the string that p points to (i.e., either 2 or 3 bytes), __builtin_strlen is not able to compute the range of lengths of the string that p points to, even though the range of the offsets into the string is available via the get_range_info function.  (The test cases uses _Bool only to constrain the range to small bounds; the problem is general and not specific to a particular type of the offset variable.)

$ cat rng.c && /build/gcc-77608/gcc/xgcc -B /build/gcc-77608/gcc -O2 -S -Wall -Wextra -Wpedantic -fdump-tree-vrp=/dev/stdout rng.c
void f (_Bool i)
{
  const char *p = "abc";
  p += i;

  unsigned long n = __builtin_strlen (p);

  if (n < 2 || 3 < n)
    __builtin_abort ();
}

void g (_Bool i)
{
  const char *p = "ab";
  p += i;

  unsigned long n = __builtin_object_size (p, 2);

  if (n < 2 || 3 < n)
    __builtin_abort ();
}


;; Function f (f, funcdef_no=0, decl_uid=1791, cgraph_uid=0, symbol_order=0)

;; 1 loops found
;;
;; Loop 0
;;  header 0, latch 1
;;  depth 0, outer -1
;;  nodes: 0 1 2 3 4
;; 2 succs { 3 4 }
;; 3 succs { }
;; 4 succs { 1 }

Value ranges after VRP:

_1: [0, 1]
_2: [0, +INF]
i_3(D): VARYING
p_4: VARYING
n_6: VARYING


f (_Bool i)
{
  long unsigned int n;
  const char * p;
  sizetype _1;
  long unsigned int _2;

  <bb 2>:
  _1 = (sizetype) i_3(D);
  p_4 = "abc" + _1;
  n_6 = __builtin_strlen (p_4);
  _2 = n_6 + 18446744073709551614;
  if (_2 > 1)
    goto <bb 3>;
  else
    goto <bb 4>;

  <bb 3>:
  __builtin_abort ();

  <bb 4>:
  return;

}



;; Function f (f, funcdef_no=0, decl_uid=1791, cgraph_uid=0, symbol_order=0)

;; 1 loops found
;;
;; Loop 0
;;  header 0, latch 1
;;  depth 0, outer -1
;;  nodes: 0 1 2 3 4
;; 2 succs { 3 4 }
;; 3 succs { }
;; 4 succs { 1 }

Value ranges after VRP:

_1: [0, 1]
_2: [0, +INF]
i_3(D): VARYING
p_4: VARYING
n_6: VARYING


f (_Bool i)
{
  long unsigned int n;
  const char * p;
  sizetype _1;
  long unsigned int _2;

  <bb 2>:
  _1 = (sizetype) i_3(D);
  p_4 = "abc" + _1;
  n_6 = __builtin_strlen (p_4);
  _2 = n_6 + 18446744073709551614;
  if (_2 > 1)
    goto <bb 3>;
  else
    goto <bb 4>;

  <bb 3>:
  __builtin_abort ();

  <bb 4>:
  return;

}


;; Function g (g, funcdef_no=1, decl_uid=1796, cgraph_uid=1, symbol_order=1)

;; 1 loops found
;;
;; Loop 0
;;  header 0, latch 1
;;  depth 0, outer -1
;;  nodes: 0 1 2
;; 2 succs { 1 }

Value ranges after VRP:

_1: [0, 1]
i_3(D): VARYING
p_4: VARYING
n_6: VARYING


g (_Bool i)
{
  long unsigned int n;
  const char * p;
  sizetype _1;

  <bb 2>:
  _1 = (sizetype) i_3(D);
  p_4 = "ab" + _1;
  n_6 = __builtin_object_size (p_4, 2);
  return;

}



;; Function g (g, funcdef_no=1, decl_uid=1796, cgraph_uid=1, symbol_order=1)

;; 1 loops found
;;
;; Loop 0
;;  header 0, latch 1
;;  depth 0, outer -1
;;  nodes: 0 1 2
;; 2 succs { 1 }

Value ranges after VRP:



g (_Bool i)
{
  long unsigned int n;
  const char * p;

  <bb 2>:
  return;

}


---


### compiler : `gcc`
### title : `VRP simplify_bit_ops_using_ranges should be applied during propagation`
### open_at : `2016-10-07T08:50:32Z`
### last_modified_date : `2021-12-25T09:59:58Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=77893
### status : `RESOLVED`
### tags : `easyhack, missed-optimization`
### component : `tree-optimization`
### version : `7.0`
### severity : `enhancement`
### contents :
A redundant

 _3 = _2 & _1;

that is replaced by _3 = _2; should instead produce a [_2, _2] range for _3
during propagation.


---


### compiler : `gcc`
### title : `incorrect VR_RANGE for a signed char function argument`
### open_at : `2016-10-07T22:12:38Z`
### last_modified_date : `2023-05-16T02:48:53Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=77899
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `7.0`
### severity : `enhancement`
### contents :
Similar to bug 77898 but with different and more wide-ranging symptoms (it persists past even the last invocation of the VRP pass), in the following program the range of the variable i is bounded by its type to [-128, 127].  Thus the result of the (p += i) expression is guaranteed to be in the range [d + 2, d + 257] and the if expression always false.  However, GCC represents the range of the signed char offset by the VR_ANTI_RANGE ~[128, 18446744073709551487] and fails to optimize the if statement away.

This is another case that popped up during the testing of my patch for bug 77608 where it affects the result of __builtin_object_size.

$ cat x.c && /build/gcc-trunk-svn/gcc/xgcc -B /build/gcc-trunk-svn/gcc -O2 -S -Wall -Wextra -Wpedantic -fdump-tree-vrp=/dev/stdout x.c
void f (signed char i)
{
  char d [260];

  const char *p = &d[130];

  p += i;

  if (p < d + 2 || d + 257 < p)
    __builtin_abort ();
}

;; Function f (f, funcdef_no=0, decl_uid=1791, cgraph_uid=0, symbol_order=0)

;; 1 loops found
;;
;; Loop 0
;;  header 0, latch 1
;;  depth 0, outer -1
;;  nodes: 0 1 2 3 4 5
;; 2 succs { 4 3 }
;; 3 succs { 4 5 }
;; 4 succs { }
;; 5 succs { 1 }

SSA replacement table
N_i -> { O_1 ... O_j } means that N_i replaces O_1, ..., O_j

p_7 -> { p_3 }
Incremental SSA update started at block: 2
Number of blocks in CFG: 6
Number of blocks to update: 2 ( 33%)



Value ranges after VRP:

_1: ~[128, 18446744073709551487]
i_2(D): VARYING
p_3: VARYING
p_7: VARYING


f (signed char i)
{
  const char * p;
  char d[260];
  sizetype _1;

  <bb 2>:
  _1 = (sizetype) i_2(D);
  p_3 = &d[130] + _1;
  if (&MEM[(void *)&d + 2B] > p_3)
    goto <bb 4>;
  else
    goto <bb 3>;

  <bb 3>:
  if (&MEM[(void *)&d + 257B] < p_3)
    goto <bb 4>;
  else
    goto <bb 5>;

  <bb 4>:
  __builtin_abort ();

  <bb 5>:
  d ={v} {CLOBBER};
  return;

}



;; Function f (f, funcdef_no=0, decl_uid=1791, cgraph_uid=0, symbol_order=0)

;; 1 loops found
;;
;; Loop 0
;;  header 0, latch 1
;;  depth 0, outer -1
;;  nodes: 0 1 2 3 4
;; 2 succs { 3 4 }
;; 3 succs { }
;; 4 succs { 1 }

Value ranges after VRP:

_1: ~[128, 18446744073709551487]
i_2(D): VARYING
p_3: VARYING
_7: [0, +INF]
_8: [0, +INF]
_9: [0, +INF]


f (signed char i)
{
  const char * p;
  char d[260];
  sizetype _1;
  _Bool _7;
  _Bool _8;
  _Bool _9;

  <bb 2>:
  _1 = (sizetype) i_2(D);
  p_3 = &d[130] + _1;
  _7 = &MEM[(void *)&d + 257B] < p_3;
  _8 = &MEM[(void *)&d + 2B] > p_3;
  _9 = _8 | _7;
  if (_9 != 0)
    goto <bb 3>;
  else
    goto <bb 4>;

  <bb 3>:
  __builtin_abort ();

  <bb 4>:
  d ={v} {CLOBBER};
  return;

}


---


### compiler : `gcc`
### title : `missing tailcall optimization in case when local variable escapes that goes out of scope before the possible tail call site`
### open_at : `2016-10-11T16:53:39Z`
### last_modified_date : `2019-01-25T15:52:49Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=77938
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `6.2.0`
### severity : `enhancement`
### contents :
GCC does not eliminate tailcalls in case when an address of any local variable escapes the function. Consider the following code:

void escape(int& a);
void callee();

void caller()
{
  {
    int local;
    escape(local);
  }
  
  callee();
}

The variable "local" escaped, but it is dead by the time control reaches the call to callee(). Therefore callee can not access it without invoking undefined behavior. As the result the call to callee() can be a tailcall.


---


### compiler : `gcc`
### title : `missing optimization with division`
### open_at : `2016-10-14T03:53:13Z`
### last_modified_date : `2021-08-24T10:18:51Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=77980
### status : `NEW`
### tags : `easyhack, missed-optimization`
### component : `tree-optimization`
### version : `7.0`
### severity : `enhancement`
### contents :
We compiled a program (A.c) by GCC-7.0.0 and clang-3.8.0 with -O3 option.
clang-3.8.0 performed better optimization than GCC-7.0.0.

(A.c)
#include <stdio.h>

int x1 = 0;
unsigned int x2 = 1;

int main ()
{	
　　int t1 = x1*(1/(x2+x2));
　　if (t1 != 0) __builtin_abort();
    return 0;
}
/*
+---------------------------------------+--------------------------------------+
|gcc-7.0.s(gcc-7.0.0 A.c -O3 -S)        |clang.s(clang-3.8.0 A.c -O3 -S)       |
+---------------------------------------+--------------------------------------+
|main:                                  |\t.type\tmain,@function               |
|.LFB11:                                |main:                                 |
|        .cfi_startproc                 |        .cfi_startproc                |
|\tmovl\tx2(%rip), %eax                 |# BB#0:                               |
|        xorl    %edx, %edx             |                                      |
|        leal    (%rax,%rax), %ecx      |                                      |
|        movl    $1, %eax               |                                      |
|        divl    %ecx                   |                                      |
|        imull   x1(%rip), %eax         |                                      |
|        testl   %eax, %eax             |                                      |
|        jne     .L7                    |                                      |
|        xorl    %eax, %eax             |        xorl    %eax, %eax            |
|        ret                            |        retq                          |
|.L7:                                   |.Lfunc_end0:                          |
|        subq    $8, %rsp               |        .size   main, .Lfunc_end0-main|
|        .cfi_def_cfa_offset 16         |                                      |
|        call    abort                  |                                      |
|        .cfi_endproc                   |        .cfi_endproc                  |
|.LFE11:\n                              |\n                                    |
|        .size   main, .-main           |        .type   x1,@object            |
|        .globl  x2                     |                                      |
|        .data                          |                                      |
|        .align 4                       |                                      |
|        .type   x2, @object            |                                      |
|        .size   x2, 4                  |                                      |
|x2:                                    |                                      |
|        .long   1                      |                                      |
|        .globl  x1                     |                                      |
|        .bss                           |        .bss                          |
|        .align 4                       |        .globl  x1                    |
|        .type   x1, @object            |        .align  4                     |
|        .size   x1, 4                  |                                      |
|x1:                                    |x1:                                   |
|        .zero   4                      |        .long   0                     |
|        .ident  "GCC: (GNU) 7.0.0 20...|        .size   x1, 4                 |
|\t.section\t.note.GNU-stack,"",@prog...|\n                                    |
|                                       |        .type   x2,@object            |
|                                       |        .data                         |
|                                       |        .globl  x2                    |
|                                       |        .align  4                     |
|                                       |x2:                                   |
|                                       |        .long   1                     |
|                                       |        .size   x2, 4                 |
|                                       |\n                                    |
|                                       |\n                                    |
|                                       |        .ident  "clang version 3.8....|
|                                       |        .section        ".note.GNU-...|
+---------------------------------------+--------------------------------------+
/*
using built-in specs.
COLLECT_GCC=gcc-7.0
COLLECT_LTO_WRAPPER=/home/kota/opt/gcc/libexec/gcc/x86_64-pc-linux-gnu/7.0.0/lto-wrapper
target: x86_64-pc-linux-gnu
configure woth: ../gcc/configure --prefix=/home/kota/opt/gcc --program-suffix=-7.0 --disable-multilib --enable-languages=c
thred model: posix
gcc version 7.0.0 20161013 (experimental) (GCC)
 

using built-in specs.
clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final)
Target: x86_64-pc-linux-gnu
Thread model: posix
InstalledDir: /usr/bin
Found candidate GCC installation: /usr/bin/../lib/gcc/x86_64-linux-gnu/4.7
Found candidate GCC installation: /usr/bin/../lib/gcc/x86_64-linux-gnu/4.7.4
Found candidate GCC installation: /usr/bin/../lib/gcc/x86_64-linux-gnu/5.4.0
Found candidate GCC installation: /usr/bin/../lib/gcc/x86_64-linux-gnu/6.0.0
Found candidate GCC installation: /usr/lib/gcc/x86_64-linux-gnu/4.7
Found candidate GCC installation: /usr/lib/gcc/x86_64-linux-gnu/4.7.4
Found candidate GCC installation: /usr/lib/gcc/x86_64-linux-gnu/5.4.0
Found candidate GCC installation: /usr/lib/gcc/x86_64-linux-gnu/6.0.0
Selected GCC installation: /usr/bin/../lib/gcc/x86_64-linux-gnu/5.4.0
Candidate multilib: .;@m64
Selected multilib: .;@m64

 */


---


### compiler : `gcc`
### title : `extra sign extend if used to store in 32bit and return 64bit and the upper bits are known to be zeroed.`
### open_at : `2016-10-23T17:32:28Z`
### last_modified_date : `2022-09-26T16:33:14Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=78085
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `6.2.0`
### severity : `enhancement`
### contents :
Created attachment 39873
Preprocesses test code

The attached file includes three functions that perform basic arithmetic operations on an int and return the result as a long in different ways.  The first and the last are compiled to code that contains a cltq instruction, while the second one omits it.  I'd expect the other two to omit it as well because the higher bits are already cleared by the arithmetic operations.  Perhaps the mov instruction in between prevents this elimination?


Using built-in specs.
COLLECT_GCC=gcc
Target: x86_64-linux-gnu
Configured with: ../src/configure -v --with-pkgversion='Debian 6.2.0-6' --with-bugurl=file:///usr/share/doc/gcc-6/README.Bugs --enable-languages=c,ada,c++,java,go,d,fortran,objc,obj-c++ --prefix=/usr --program-suffix=-6 --program-prefix=x86_64-linux-gnu- --enable-shared --enable-linker-build-id --libexecdir=/usr/lib --without-included-gettext --enable-threads=posix --libdir=/usr/lib --enable-nls --with-sysroot=/ --enable-clocale=gnu --enable-libstdcxx-debug --enable-libstdcxx-time=yes --with-default-libstdcxx-abi=new --enable-gnu-unique-object --disable-vtable-verify --enable-libmpx --enable-plugin --with-system-zlib --disable-browser-plugin --enable-java-awt=gtk --enable-gtk-cairo --with-java-home=/usr/lib/jvm/java-1.5.0-gcj-6-amd64/jre --enable-java-home --with-jvm-root-dir=/usr/lib/jvm/java-1.5.0-gcj-6-amd64 --with-jvm-jar-dir=/usr/lib/jvm-exports/java-1.5.0-gcj-6-amd64 --with-arch-directory=amd64 --with-ecj-jar=/usr/share/java/eclipse-ecj.jar --enable-objc-gc --enable-multiarch --with-arch-32=i686 --with-abi=m64 --with-multilib-list=m32,m64,mx32 --enable-multilib --with-tune=generic --enable-checking=release --build=x86_64-linux-gnu --host=x86_64-linux-gnu --target=x86_64-linux-gnu
Thread model: posix
gcc version 6.2.0 20161010 (Debian 6.2.0-6)
COLLECT_GCC_OPTIONS='-v' '-save-temps' '-O2' '-S' '-mtune=generic' '-march=x86-64'
 /usr/lib/gcc/x86_64-linux-gnu/6/cc1 -E -quiet -v -imultiarch x86_64-linux-gnu a.c -mtune=generic -march=x86-64 -O2 -fpch-preprocess -o a.i
ignoring nonexistent directory "/usr/local/include/x86_64-linux-gnu"
ignoring nonexistent directory "/usr/lib/gcc/x86_64-linux-gnu/6/../../../../x86_64-linux-gnu/include"
#include "..." search starts here:
#include <...> search starts here:
 /usr/lib/gcc/x86_64-linux-gnu/6/include
 /usr/local/include
 /usr/lib/gcc/x86_64-linux-gnu/6/include-fixed
 /usr/include/x86_64-linux-gnu
 /usr/include
End of search list.
COLLECT_GCC_OPTIONS='-v' '-save-temps' '-O2' '-S' '-mtune=generic' '-march=x86-64'
 /usr/lib/gcc/x86_64-linux-gnu/6/cc1 -fpreprocessed a.i -quiet -dumpbase a.c -mtune=generic -march=x86-64 -auxbase a -O2 -version -o a.s
GNU C11 (Debian 6.2.0-6) version 6.2.0 20161010 (x86_64-linux-gnu)
        compiled by GNU C version 6.2.0 20161010, GMP version 6.1.1, MPFR version 3.1.5, MPC version 1.0.3, isl version 0.15
GGC heuristics: --param ggc-min-expand=100 --param ggc-min-heapsize=131072
GNU C11 (Debian 6.2.0-6) version 6.2.0 20161010 (x86_64-linux-gnu)
        compiled by GNU C version 6.2.0 20161010, GMP version 6.1.1, MPFR version 3.1.5, MPC version 1.0.3, isl version 0.15
GGC heuristics: --param ggc-min-expand=100 --param ggc-min-heapsize=131072
Compiler executable checksum: 7b884337c1b75b774181841eebd770e3
COMPILER_PATH=/usr/lib/gcc/x86_64-linux-gnu/6/:/usr/lib/gcc/x86_64-linux-gnu/6/:/usr/lib/gcc/x86_64-linux-gnu/:/usr/lib/gcc/x86_64-linux-gnu/6/:/usr/lib/gcc/x86_64-linux-gnu/
LIBRARY_PATH=/usr/lib/gcc/x86_64-linux-gnu/6/:/usr/lib/gcc/x86_64-linux-gnu/6/../../../x86_64-linux-gnu/:/usr/lib/gcc/x86_64-linux-gnu/6/../../../../lib/:/lib/x86_64-linux-gnu/:/lib/../lib/:/usr/lib/x86_64-linux-gnu/:/usr/lib/../lib/:/usr/lib/gcc/x86_64-linux-gnu/6/../../../:/lib/:/usr/lib/
COLLECT_GCC_OPTIONS='-v' '-save-temps' '-O2' '-S' '-mtune=generic' '-march=x86-64'


---


### compiler : `gcc`
### title : `Failure to optimize with __builtin_clzl`
### open_at : `2016-10-25T02:59:19Z`
### last_modified_date : `2021-08-01T20:33:13Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=78103
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `6.2.1`
### severity : `normal`
### contents :
constexpr
unsigned long findLastSet(unsigned long x) {
  return x ? 8 * sizeof(unsigned long) - __builtin_clzl(x) : 0;
}
constexpr
unsigned long findLastSet2(unsigned long x) {
  return x ? ((8 * sizeof(unsigned long) - 1) ^ __builtin_clzl(x)) + 1 : 0;
}

These two functions are the same, but GCC does a better job at compiling the second vs the more idiomatic first

https://godbolt.org/g/B2x5iG

findLastSet(unsigned long):
        xor     eax, eax
        test    rdi, rdi
        je      .L1
        bsr     rdi, rdi
        mov     eax, 64
        xor     rdi, 63
        movsx   rdi, edi
        sub     rax, rdi
.L1:
        rep ret
findLastSet2(unsigned long):
        xor     eax, eax
        test    rdi, rdi
        je      .L6
        bsr     rdi, rdi
        movsx   rax, edi
        add     rax, 1


---


### compiler : `gcc`
### title : `optimizer doesn't grok C++ new/delete yet`
### open_at : `2016-10-25T05:50:33Z`
### last_modified_date : `2022-01-07T06:26:31Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=78104
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `c++`
### version : `unknown`
### severity : `normal`
### contents :
A simple example:

int main() {
  int *ob = new int();
  delete ob;
}

clang optimizes it away:

main:                      # @main
        xorl    %eax, %eax
        retq

gcc doesn't:

main:
        subq    $8, %rsp
        movl    $4, %edi
        call    operator new(unsigned long)
        movl    $4, %esi
        movl    $0, (%rax)
        movq    %rax, %rdi
        call    operator delete(void*, unsigned long)
        xorl    %eax, %eax
        addq    $8, %rsp
        ret


---


### compiler : `gcc`
### title : `Missed optimization for "int modulo 2^31"`
### open_at : `2016-10-26T14:06:49Z`
### last_modified_date : `2023-06-07T15:18:53Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=78115
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `6.2.1`
### severity : `enhancement`
### contents :
Consider the operation of mapping an int to the unique modular representative in [0, 2^31).


Readable code:

#include <climits>

int mod31(int num) {
  if (num < 0) { num = num + 1 + INT_MAX; }
  return num;
}


Paranoid bit-shifter's code:

int mod31shift(int num) {
  return static_cast<unsigned int>(num) % (1U << 31);
}

Clang generates the same machine code for both, but GCC does not: https://godbolt.org/g/2BjNqA


---


### compiler : `gcc`
### title : `Shifted const forming is had`
### open_at : `2016-10-27T06:25:14Z`
### last_modified_date : `2021-07-25T00:53:26Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=78125
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `7.0`
### severity : `normal`
### contents :
Take:
#define CONST1 0x1234567812345678ull
#define CONST2 (CONST1<<1)
#define CONST3 (CONST2<<1)
#define CONST4 (CONST3<<1)
#define CONST5 (CONST4<<1)
#define CONST6 (CONST5<<1)
#define CONST7 (CONST6<<1)
#define CONST8 (CONST7<<1)

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

---- CUT ----

Right now the generated code generates the constant for each of the above constants but we should be able to optimize it using left shifts.  We are able to handle plus but not shifted values (or rotated values, see PR63281).


---


### compiler : `gcc`
### title : `SLP vectorizer: prologue cost biased by redundancies`
### open_at : `2016-10-30T17:17:21Z`
### last_modified_date : `2020-09-14T12:51:58Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=78164
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `7.0`
### severity : `enhancement`
### contents :
From http://stackoverflow.com/q/39947582/1918193

void testfunc_flat(double a, double b, double* dst)
{
  dst[0] = 0.1 + ( a)*(1.0 + 0.5*( a));
  dst[1] = 0.1 + ( b)*(1.0 + 0.5*( b));
  dst[2] = 0.1 + (-a)*(1.0 + 0.5*(-a));
  dst[3] = 0.1 + (-b)*(1.0 + 0.5*(-b));
}

We fail to vectorize with AVX, that's understandable because the operations are different. More surprising is that we reject SSE vectorization

  Vector inside of basic block cost: 14
  Vector prologue cost: 10
  Vector epilogue cost: 0
  Scalar cost of basic block: 22

However, if I disable the cost model, I can see this prologue that is supposed to have cost 10:

  vect_cst__47 = { 1.000000000000000055511151231257827021181583404541015625e-1, 1.000000000000000055511151231257827021181583404541015625e-1 };
  vect_cst__44 = { 1.0e+0, 1.0e+0 };
  vect_cst__42 = { 5.0e-1, 5.0e-1 };
  vect_cst__40 = {a_19(D), b_23(D)};
  vect_cst__38 = {a_19(D), b_23(D)};
  vect_cst__34 = { 1.000000000000000055511151231257827021181583404541015625e-1, 1.000000000000000055511151231257827021181583404541015625e-1 };
  vect_cst__32 = {a_19(D), b_23(D)};
  vect_cst__30 = { 1.0e+0, 1.0e+0 };
  vect_cst__28 = { 5.0e-1, 5.0e-1 };
  vect_cst__27 = {a_19(D), b_23(D)};

Some very basic CSE would bring it down to a cost of 4 and allow vectorizing like llvm.


---


### compiler : `gcc`
### title : `[PowerPC] Missing optimization for local-exec TLS model`
### open_at : `2016-11-03T14:35:33Z`
### last_modified_date : `2022-03-08T16:20:56Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=78199
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `target`
### version : `7.0`
### severity : `enhancement`
### contents :
The following test case:

extern __thread int i;

extern int s;

int fi(void)
{
        return i;
}

int fs(void)
{
        return s;
}

generates:

powerpc-rtems4.12-gcc -O2 -S -ftls-model=local-exec tls.c -o -
        .file   "tls.c"
        .machine ppc
        .section        ".text"
        .align 2
        .globl fi
        .type   fi, @function
fi:
        addis 9,2,i@tprel@ha
        addi 9,9,i@tprel@l
        lwz 3,0(9)
        blr
        .size   fi, .-fi
        .align 2
        .globl fs
        .type   fs, @function
fs:
        lis 9,s@ha
        lwz 3,s@l(9)
        blr
        .size   fs, .-fs
        .ident  "GCC: (GNU) 7.0.0 20161103 (experimental) [master revision bad2001:22427cc:8c7ce92980721624d9f2ac6332fe34188d09b851]"

This can be optimized to:

fi:
        lis 9,2,i@tprel@ha
        lwz 9,i@tprel@l(2)
        blr

This issue seems to be target specific, for example:

gcc -O2 -S -ftls-model=local-exec tls.c -o -
        .file   "tls.c"
        .text
        .p2align 4,,15
        .globl  fi
        .type   fi, @function
fi:
.LFB0:
        .cfi_startproc
        movl    %fs:i@tpoff, %eax
        ret
        .cfi_endproc
.LFE0:
        .size   fi, .-fi
        .p2align 4,,15
        .globl  fs
        .type   fs, @function
fs:
.LFB1:
        .cfi_startproc
        movl    s(%rip), %eax
        ret
        .cfi_endproc
.LFE1:
        .size   fs, .-fs
        .ident  "GCC: (GNU) 7.0.0 20161103 (experimental) [master revision bad2001:22427cc:8c7ce92980721624d9f2ac6332fe34188d09b851]"
        .section        .note.GNU-stack,"",@progbits

However:

gcc -O2 -S -ftls-model=local-exec tls.c -o -
        .file   "tls.c"
        .text
        .p2align 4,,15
        .globl  fi
        .type   fi, @function
fi:
.LFB0:
        .cfi_startproc
        movq    %fs:0, %rax
        movl    i@tpoff(%rax), %eax
        ret
        .cfi_endproc
.LFE0:
        .size   fi, .-fi
        .p2align 4,,15
        .globl  fs
        .type   fs, @function
fs:
.LFB1:
        .cfi_startproc
        movl    s(%rip), %eax
        ret
        .cfi_endproc
.LFE1:
        .size   fs, .-fs
        .ident  "GCC: (SUSE Linux) 4.8.1 20130909 [gcc-4_8-branch revision 202388]"
        .section        .note.GNU-stack,"",@progbits


---


### compiler : `gcc`
### title : `[7 Regression] 429.mcf of cpu2006 regresses in GCC trunk for avx2 target.`
### open_at : `2016-11-03T18:05:25Z`
### last_modified_date : `2019-11-14T09:33:41Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=78200
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `7.0`
### severity : `normal`
### contents :
Noticed 5% regression with 429.mcf of cpu2006 on x86_64 AVX2 (bdver4) with GCC trunk gcc version 7.0.0 20161028 (experimental) (GCC).

Flag used is -O3 -mavx2 -mprefer-avx128

Not seen with GCC 6.1 or with GCC trunk for -O3 -mavx -mprefer-avx128

Assembly difference is observed in hot function primal_bea_mpp of pbeampp.c. 

-O3 -mavx -mprefer-avx128		-O3 -mavx2 -mprefer-avx128

.L98:                                 |  .L98:
  ------------------------------------|          jle     .L97 <==  order of comparison 
          cmpl    $2, %r9d            |          cmpl    $2, %r9d  is different.
          jne     .L97                |          jne     .L97
          testq   %rdi, %rdi          |  -----------------------------------
          jle     .L97                |  -----------------------------------
  .L99:                               |  .L99:
          addq    $1, %r13            |          addq    $1, %r13
          movq    %rdi, %r12          |          movq    %rdi, %r12
          movq    perm(,%r13,8), %r9  |          movq    perm(,%r13,8), %r9
          sarq    $63, %r12           |          sarq    $63, %r12
          movq    %rdi, 8(%r9)        |          movq    %rdi, 8(%r9)
+ +-- 12 lines: xorq %r12, %rdi-------|+ +-- 12 lines: xorq %r12, %rdi------
          jle     .L97                |          jle     .L97
          movq    8(%rax), %r14       |          movq    8(%rax), %r14
          movq    (%rax), %rdi        |          movq    (%rax), %rdi
          subq    (%r14), %rdi        |          subq    (%r14), %rdi
          movq    16(%rax), %r14      |          movq    16(%rax), %r14
          addq    (%r14), %rdi        |          addq    (%r14), %rdi
          jns     .L98                |          cmpq    $0, %rdi
  ------------------------------------|          jge     .L98


Gimple optimzied dump shows 

GCC trunk -O3 -mavx -mprefer-avx128 
;;   basic block 20, loop depth 2, count 0, freq 1067, maybe hot
;;   Invalid sum of incoming frequencies 1216, should be 1067
;;    prev block 19, next block 21, flags: (NEW, REACHABLE, VISITED)
;;    pred:       18 [64.0%]  (FALSE_VALUE,EXECUTABLE)
  # RANGE [0, 1]
  _496 = _512 == 2;
  # RANGE [0, 1]
  _495 = red_cost_503 > 0;
  # RANGE [0, 1]
  _494 = _495 & _496;
  if (_494 != 0)
    goto <bb 21>;
  else
    goto <bb 22>;


GCC trunk -O3 -mavx2 -mprefer-avx128 

;;   basic block 20, loop depth 2, count 0, freq 1067, maybe hot
;;   Invalid sum of incoming frequencies 1216, should be 1067
;;    prev block 19, next block 21, flags: (NEW, REACHABLE, VISITED)
;;    pred:       18 [64.0%]  (FALSE_VALUE,EXECUTABLE)
  # RANGE [0, 1]
  _496 = _512 == 2;
  # RANGE [0, 1]
  _495 = red_cost_503 > 0;  
  # RANGE [0, 1]
  _494 = _495 & _496; <== operation order is different on AVX2.
  if (_494 != 0)
    goto <bb 21>;
  else
    goto <bb 22>;

operation order is changed at pbeampp.c.171t.reassoc2.
;;   basic block 20, loop depth 2, count 0, freq 1067, maybe hot
;;   Invalid sum of incoming frequencies 1216, should be 1067
;;    prev block 19, next block 21, flags: (NEW, REACHABLE, VISITED)
;;    pred:       18 [64.0%]  (FALSE_VALUE,EXECUTABLE)
  _496 = _512 == 2;
  _495 = red_cost_503 > 0;
  _494 = _495 & _496;
  if (_494 != 0)
    goto <bb 21>;
  else
    goto <bb 22>;

Looking backwards further, found that in tree if conversion generates non-canonical gimple. 
pbeampp.c.155t.ifcvt

;;   basic block 27, loop depth 2, count 0, freq 1067, maybe hot
;;   Invalid sum of incoming frequencies 1216, should be 1067
;;    prev block 26, next block 28, flags: (NEW, REACHABLE, VISITED)
;;    pred:       25 [64.0%]  (FALSE_VALUE,EXECUTABLE)
  _496 = _512 == 2;
  _495 = red_cost_503 > 0;
  _494 = _496 & _495;    <== comparison order is same but LHS of "&" has a greater number.
  if (_494 != 0)
    goto <bb 28>;
  else
    goto <bb 29>;
    

pbeampp.c.154t.ch_vect
;;   basic block 23, loop depth 2, count 0, freq 1067, maybe hot
;;   Invalid sum of incoming frequencies 1216, should be 1067
;;    prev block 22, next block 24, flags: (NEW, REACHABLE, VISITED)
;;    pred:       21 [64.0%]  (FALSE_VALUE,EXECUTABLE)
  _340 = _23 == 2;
  _341 = red_cost_86 > 0;
  _338 = _340 & _341;  <==  comparison order is same here.
  if (_338 != 0)
    goto <bb 24>;
  else
    goto <bb 25>;

 

compiling pbeampp.c with -O3 -mavx2 -mprefer-avx128  -fno-tree-loop-if-conversion 
and rest of benchmark changes with  -O3 -mavx2 -mprefer-avx128 brings back the score same as that of 
-O3 -mavx  or GCC 6.1 -O3 -mavx2.


---


### compiler : `gcc`
### title : `missing memcmp optimization with constant arrays`
### open_at : `2016-11-08T18:19:59Z`
### last_modified_date : `2020-08-18T18:59:33Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=78257
### status : `RESOLVED`
### tags : `missed-optimization, patch`
### component : `tree-optimization`
### version : `7.0`
### severity : `enhancement`
### contents :
GCC folds some calls to memcmp involving constants but not others even though it's able to fold equivalent expressions not involving the function.  The test case below shows two such examples.  Using memcmp to compare constant string arrays is folded unless the comparison includes the terminating nul.  Using memcmp to compare arrays of integers is not folded even though comparing the array elements (even recursively) is.

$ cat t.c && gcc -O2 -S -Wall -Wextra -Wpedantic -fdump-tree-optimized=/dev/stdout t.c
const char a[] = "1234";
const char b[] = "1234";

const int i[] = { 1234 };
const int j[] = { 1234 };

int f0 (void)
{
  return __builtin_memcmp (a, b, sizeof a);
}

int f1 (void)
{
  return __builtin_memcmp (a, b, sizeof a - 1);
}

int f2 (void)
{
  return __builtin_memcmp (i, j, sizeof i);
}

int f3 (void)
{
  return *i == *j;
}

int f4 (void)
{
  return __builtin_strcmp (a, b);
}

;; Function f0 (f0, funcdef_no=0, decl_uid=1799, cgraph_uid=0, symbol_order=4)

f0 ()
{
  int _2;

  <bb 2>:
  _2 = __builtin_memcmp (&a, &b, 5); [tail call]
  return _2;

}



;; Function f1 (f1, funcdef_no=6, decl_uid=1802, cgraph_uid=1, symbol_order=5)

f1 ()
{
  <bb 2>:
  return 0;

}



;; Function f2 (f2, funcdef_no=2, decl_uid=1805, cgraph_uid=2, symbol_order=6)

f2 ()
{
  int _2;

  <bb 2>:
  _2 = __builtin_memcmp (&i, &j, 4); [tail call]
  return _2;

}



;; Function f3 (f3, funcdef_no=3, decl_uid=1808, cgraph_uid=3, symbol_order=7)

f3 ()
{
  <bb 2>:
  return 1;

}



;; Function f4 (f4, funcdef_no=4, decl_uid=1811, cgraph_uid=4, symbol_order=8)

f4 ()
{
  <bb 2>:
  return 0;

}


---


### compiler : `gcc`
### title : `"if (x & constant) z |= constant" should not be rendered with jumps and conditional moves`
### open_at : `2016-11-11T15:55:04Z`
### last_modified_date : `2021-07-20T03:16:16Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=78317
### status : `RESOLVED`
### tags : `missed-optimization, TREE`
### component : `tree-optimization`
### version : `6.2.1`
### severity : `normal`
### contents :
Created attachment 40025
Test code

The following code:

	unsigned test1(unsigned x)
	{
		unsigned z = 0;
		if (x & 0x10)
			z |= 0x10;
		return z;
	}

on x86_64 compiled with -Os to:

   0:   89 f8                   mov    %edi,%eax
   2:   ba 10 00 00 00          mov    $0x10,%edx
   7:   83 e0 10                and    $0x10,%eax
   a:   0f 45 c2                cmovne %edx,%eax
   d:   c3                      retq   

when what it should probable do is what clang does:

   0:   83 e7 10                and    $0x10,%edi
   3:   89 f8                   mov    %edi,%eax
   5:   c3                      retq   

as the bit can be transferred by an AND and an OR.

Further, two or more such statements can be combined, for instance:

	unsigned test2(unsigned x)
	{
		unsigned z = 0;
		if (x & 0x10)
			z |= 0x10;
		if (x & 0x40)
			z |= 0x40;
		return z;
	}

but gcc gives the following:

   e:   89 f8                   mov    %edi,%eax
  10:   ba 10 00 00 00          mov    $0x10,%edx
  15:   83 e0 10                and    $0x10,%eax
  18:   0f 45 c2                cmovne %edx,%eax
  1b:   89 c2                   mov    %eax,%edx
  1d:   83 ca 40                or     $0x40,%edx
  20:   40 80 e7 40             and    $0x40,%dil
  24:   0f 45 c2                cmovne %edx,%eax
  27:   c3                      retq   

when clang gives:

   6:   83 e7 50                and    $0x50,%edi
   9:   89 f8                   mov    %edi,%eax
   b:   c3                      retq   


If z isn't passed in, but rather is initialised to another argument, say y:

	unsigned test3(unsigned x, unsigned y)
	{
		unsigned z = y;
		if (x & 0x10)
			z |= 0x10;
		return z;
	}

	unsigned test4(unsigned x, unsigned y)
	{
		unsigned z = y;
		if (x & 0x10)
			z |= 0x10;
		if (x & 0x40)
			z |= 0x40;
		return z;
	}

then gcc gives:

0000000000000028 <test3>:
  28:   89 f2                   mov    %esi,%edx
  2a:   89 f0                   mov    %esi,%eax
  2c:   83 ca 10                or     $0x10,%edx
  2f:   40 80 e7 10             and    $0x10,%dil
  33:   0f 45 c2                cmovne %edx,%eax
  36:   c3                      retq   

0000000000000037 <test4>:
  37:   89 f2                   mov    %esi,%edx
  39:   89 f0                   mov    %esi,%eax
  3b:   83 ca 10                or     $0x10,%edx
  3e:   40 f6 c7 10             test   $0x10,%dil
  42:   0f 45 c2                cmovne %edx,%eax
  45:   89 c2                   mov    %eax,%edx
  47:   83 ca 40                or     $0x40,%edx
  4a:   40 80 e7 40             and    $0x40,%dil
  4e:   0f 45 c2                cmovne %edx,%eax
  51:   c3                      retq   

and clang gives:

000000000000000c <test3>:
   c:   83 e7 10                and    $0x10,%edi
   f:   09 f7                   or     %esi,%edi
  11:   89 f8                   mov    %edi,%eax
  13:   c3                      retq   

0000000000000014 <test4>:
  14:   89 f8                   mov    %edi,%eax
  16:   83 e0 10                and    $0x10,%eax
  19:   09 f0                   or     %esi,%eax
  1b:   83 e7 40                and    $0x40,%edi
  1e:   09 c7                   or     %eax,%edi
  20:   89 f8                   mov    %edi,%eax
  22:   c3                      retq   

Both gcc and clang give suboptimal code for test4().  What they should do is:

        and    $0x50,%edi
        or     %esi,%edi
        mov    %edi,%eax
        retq

Note that gcc also produces similarly suboptimal output for targets other than x86_64.


---


### compiler : `gcc`
### title : `pathological code generation for long logical expression with temporary objects`
### open_at : `2016-11-11T18:25:12Z`
### last_modified_date : `2022-02-03T22:43:01Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=78323
### status : `NEW`
### tags : `compile-time-hog, missed-optimization`
### component : `c++`
### version : `6.2.1`
### severity : `normal`
### contents :
Created attachment 40030
logical-or.cpp

Compiling the attached testcase -O2 -std=c++11 reveals a significant disparity in the code GCC produces versus clang:

froydnj@thor:~$ gcc -O2 -std=c++11 -c logical-or-gcc.cpp 
froydnj@thor:~$ clang -O2 -std=c++11 -c logical-or.cpp  -o logical-or-clang.o
froydnj@thor:~$ size logical-or*.o
   text	   data	    bss	    dec	    hex	filename
 633354	      0	      0	 633354	  9aa0a	logical-or-gcc.o
  17628	      0	      0	  17628	   44dc	logical-or-clang.o

That was with GCC 4.9; a colleague tried it with GCC 6.2.0 and got:

   text    data      bss       dec        hex     filename
 591843       8        0    591851      907eb     logical-or.o 

which is some kind of improvement, but not enough of one.

I gone over the assembly with a fine-toothed comb or looked at the tree dumps, but I think GCC is falling into some kind of O(n^2) situation where it sets a flag for the constructed status of every temporary object after each exit from the chained condition.


---


### compiler : `gcc`
### title : `Improve VRP for ranges for compares which do ranges of [-TYPE_MAX + N, N]`
### open_at : `2016-11-11T21:36:58Z`
### last_modified_date : `2021-08-15T23:21:51Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=78327
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `7.0`
### severity : `enhancement`
### contents :
The following is a test case for the problem brought up in the the thread Re: anti-ranges of signed variables (https://gcc.gnu.org/ml/gcc/2016-11/msg00029.html).

In the test case below, n's range in function g is [-125, 2], making the largest value that (n + 128) can evaluate to and alloca be called with 130.  Yet -Walloca-larger-than=200 emits a warning for the function with a note claiming that the computed value may be as large as 255.  That's incorrect.

Recompiling the same test case with -Walloca-larger-than=100 results in a warning for function h as well (as expected), and with a note correctly indicating the largest value alloca can be called with there given its range of [-125, 1]: 129.  (The warning for g still says 255.)

  c.c:14:3: note: limit is 100 bytes, but argument may be as large as 129

The output of -fdump-tree-vrp confirms that the range GCC computes for n in g is [0, 255], while in h [3, 129].  The same problem seems to affect all signed integers.


$ cat c.c && /build/gcc-trunk-svn/gcc/xgcc -B /build/gcc-trunk-svn/gcc -O2 -S -Wall -Wextra -Walloca-larger-than=200 c.c
void f (void*);

void g (signed char n)
{
  if (n < -125 || 2 < n) n = 0;

  f (__builtin_alloca (n + 128));
}

void h (signed char n)
{
  if (n < -125 || 1 < n) n = 0;

  f (__builtin_alloca (n + 128));
}

c.c: In function ‘g’:
c.c:7:3: warning: argument to ‘alloca’ may be too large [-Walloca-larger-than=]
   f (__builtin_alloca (n + 128));
   ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c.c:7:3: note: limit is 200 bytes, but argument may be as large as 255


---


### compiler : `gcc`
### title : `Fold ~(1 << x) -> (~1 lrotate_expr x) on GIMPLE`
### open_at : `2016-11-13T11:45:29Z`
### last_modified_date : `2021-07-19T01:44:56Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=78335
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `7.0`
### severity : `normal`
### contents :
Hi,
It appears the following transform
~(1 << x) -> (~1 lrotate_expr x)
is done on RTL but not on GIMPLE.

Test-case:
int f(int x)
{
  int t1 = 1 << x;
  int t2 = ~t1;
  return t2;
}

optimized dump shows:

f (int x)
{
  int t2;
  int t1;

  <bb 2>:
  t1_2 = 1 << x_1(D);
  t2_3 = ~t1_2;
  return t2_3;

}

I suppose we want to do the transform on GENERIC/GIMPLE too (in match.pd) ?
Working on a patch.


---


### compiler : `gcc`
### title : `g++ generates sub-optimal assembler code when structs aren't explicitly aligned.`
### open_at : `2016-11-17T16:09:08Z`
### last_modified_date : `2021-12-22T13:23:11Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=78399
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `7.0`
### severity : `enhancement`
### contents :
Created attachment 40070
suboptimal code

Consider the following example:

struct pod { char x[7]; };
pod copy_pod(pod d) { return d; }

gcc (at any optimization level) will general sub-optimal assembler code (see attachment).
The interesting thing is that if we change "pod" to contain a number of bytes that fit into a cpu register (2, 4, 8, 16, 32, 64) then the generated assembler
is optimal (see attachment)

struct pod { char x[8]; };
pod copy_pod(pod d) { return d; }

One workaround I found is to explicitly use alignas:
struct alignas(8) pod { char x[7]; }; 

I'm wondering whether gcc should generate optimal code even without alignas(8).


---


### compiler : `gcc`
### title : `missed optimization of loop condition`
### open_at : `2016-11-19T15:12:02Z`
### last_modified_date : `2020-09-27T06:23:24Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=78427
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `6.2.0`
### severity : `normal`
### contents :
Consider the following code:

void and_1(uint64_t const* a, uint64_t* b, size_t n)
{
    for (size_t i = 0; i != n; ++i)
       b[i] = a[i] & b[i];
}

GCC 6.2 (-O2, -mtune=haswell) generates the following code:

and_1:
        xorl    %eax, %eax
        testq   %rdx, %rdx
        je      .L6
.L5:
        movq    (%rdi,%rax,8), %rcx
        andq    %rcx, (%rsi,%rax,8)
        addq    $1, %rax
        cmpq    %rax, %rdx
        jne     .L5
.L6:
        ret

If we change iteration indices from [0..N) to [-N..0), the end condition of the loop can be simplified. I would prefer the generated code to be like this:

and_1:
        leaq    (%rdi,%rdx,8), %rdi
        leaq    (%rsi,%rdx,8), %rsi
        negq    %rdx
        jnc     .L6
.L5:
        movq    (%rdi,%rdx,8), %rcx
        andq    %rcx, (%rsi,%rdx,8)
        addq    $1, %rdx
        jne     .L5
.L6:
        ret

As you can see the inner loop is 1 instruction shorter (4 instead of 5). Also this code use CF after neg instruction to check for zero.

The result loop is slightly faster. On my haswell machine it is 2% faster (5956 ms instead of 6087 ms). I expect the gain to be bigger on a in-order CPUs, but I can not verify this claim.

I believe this optimization can be applied in many cases of array iteration. The exact performance gain will depend on the operations performed by the loop body, but I don't see the cases when this transformation can hurt the performance of the loop.


---


### compiler : `gcc`
### title : `pure/const functions are assumed not to trap`
### open_at : `2016-11-22T08:11:03Z`
### last_modified_date : `2022-11-29T16:53:01Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=78463
### status : `UNCONFIRMED`
### tags : `documentation, missed-optimization, wrong-code`
### component : `middle-end`
### version : `7.0`
### severity : `enhancement`
### contents :
PR70586 shows that pure/const functions are assumed not to trap (EH / throw is captured separately already).  This makes them fail the has-side-effects check
which can lead to wrong-code issues (see that PR).

We need a more fine-grained analysis (and IPA propagation) of what functions
may do (trap, invoke undefined overflow, use FP math, etc.) to ask the right
questions from optimizations (and enable more optimizations).


---


### compiler : `gcc`
### title : `[7 Regression] Missed opportunities for jump threading`
### open_at : `2016-11-23T15:02:29Z`
### last_modified_date : `2019-11-14T09:38:06Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=78496
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `7.0`
### severity : `normal`
### contents :
Created attachment 40131
test-case to reproduce, compile with -O3 option.

We noticed a huge performance drop on one important benchmark which is caused by hoisting and collecting comparisons participated in conditional branches. Here is comments provided by Richard on it:

Note this is a general issue with PRE which tends to
see partial redundancies when it can compute an expression to a
constant on one edge.  There is nothing wrong with that but the
particular example shows the lack of a cost model with respect
to register pressure (same applies to other GIMPLE optimization passes).

In this case we have a lot of expression anticipated from the same
blocks where on one incoming edge their value is constant.  Profitability
here really depends on the "distance" of the to be inserted PHI and
its use I guess.

We're missing quite some jump-threading here as well:

  <bb 16>:
  # x1_197 = PHI <x1_261(15), x1_435(123), x1_435(105)>
  # _407 = PHI <_16(15), _16(123), 0(105)>
  # aa1_410 = PHI <aa1_185(15), aa1_185(123), aa1_216(105)>
  # d1_413 = PHI <d1_191(15), d1_191(123), d1_432(105)>
  # w1_416 = PHI <w1_260(15), w1_260(123), 0(105)>
  # v1_377 = PHI <v1_558(15), v1_558(123), 0(105)>
  # oo1_371 = PHI <oo1_567(15), oo1_567(123), oo1_194(105)>
  # ss1_376 = PHI <ss1_576(15), ss1_576(123), ss1_192(105)>
  # r1_609 = PHI <r1_585(15), r1_585(123), r1_190(105)>
  # _612 = PHI <_596(15), _596(123), _188(105)>
  # out_ind_lsm.82_322 = PHI <out_ind_lsm.82_321(15),
out_ind_lsm.82_321(123), out_ind_lsm.82_532(105)>
  _549 = w1_416 <= 899;
  _548 = _407 > 839;
  _541 = _548 & _549;
  if (_541 != 0)
    goto <bb 17>;
  else
    goto <bb 124>;

here 105 -> 16 -> 124 (forwarder) -> 18 which would eventually
make PRE behave somewhat saner (avoding the far distances).

The case appears with phicprop1 (or rather DOM, itself missing
a followup transform with respect to folding a degenerate constant
PHI plus the followup secondary threading opportunities).  The
backwards threader doesn't exploit the above opportunity though.
Our forward threaders (like DOM) do.  Unfortunately it requires
quite a few iterations to get all opportunities exploited...
(inserting 9 DOM/phi-only-cprop pass pairs "helps")

I suggest to open a bugreport for this.  Jeff may want to look at
the threading issue (I believe the backward threader _does_ iterate).

I attach a test-case to reproduce an issue.


---


### compiler : `gcc`
### title : `Recursion not optimized for structs`
### open_at : `2016-11-25T15:54:37Z`
### last_modified_date : `2021-06-03T04:52:44Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=78528
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `7.0`
### severity : `enhancement`
### contents :
The following code:

struct Int 
{ 
    constexpr Int(int value) : m_value(value) {} 
 
    constexpr friend Int operator+(Int lhs, Int rhs) { return {lhs.m_value + rhs.m_value}; } 
 
    int m_value; 
}; 
 
Int strlen(const char* s) 
{ 
    return *s == 0 ? 0 : strlen(s+1) + 1; 
} 


when compiled with `-std=c++11 -O3` generates the following assembly for the strlen function:

_Z6strlenPKc: 
.LFB4: 
    .cfi_startproc 
    cmpb    $0, (%rdi) 
    jne .L2 
    xorl    %eax, %eax 
    ret 
    .p2align 4,,10 
    .p2align 3 
.L2: 
    cmpb    $0, 1(%rdi) 
    movl    $1, %eax 
    jne .L12 
.L10: 
    ret 
    .p2align 4,,10 
    .p2align 3 
.L12: 
    cmpb    $0, 2(%rdi) 
    movl    $2, %eax 
    je  .L10 
    subq    $8, %rsp 
    .cfi_def_cfa_offset 16 
    addq    $3, %rdi 
    call    _Z6strlenPKc 
    addq    $8, %rsp 
    .cfi_def_cfa_offset 8 
    addl    $3, %eax 
    ret 
    .cfi_endproc 

As we can see, the generated code is still recursive, I think the optimizer should have optimized that, is it correctly does when we use 'int' instead of 'Int'.


---


### compiler : `gcc`
### title : `SSE4.1 pmovzx shuffle pattern not recognized`
### open_at : `2016-11-28T12:47:10Z`
### last_modified_date : `2021-08-21T18:30:49Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=78563
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `6.1.1`
### severity : `enhancement`
### contents :
An unpack pattern with 0 constant are neither folded nor recognized as a pmovzx instruction.

SSE2 code:
_mm_unpacklo_epi32(X, _mm_setzero_si128())

GCC code:
__builtin_shuffle((__v4si)X, (__v4si)_mm_setzero_si128(), (__v4si){0, 4, 1, 5});

Will both produce the same result of an xor setting 0 and an unpack instruction, while it could with SSE4.1 emit a pmozx instruction.

Note epi32 is just an example here used because it is most compact, this also affects the 8 and 16 bit equivelents.

Looking in config/i386/i386.c it seems like there is no code in the expand_vec_perm_* methods for detecting pmovzx patterns.


---


### compiler : `gcc`
### title : `redundant instruction of the form cmp r0, r0 generated in assembly with  -O2`
### open_at : `2016-11-29T07:54:15Z`
### last_modified_date : `2023-08-08T07:03:50Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=78579
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `7.0`
### severity : `enhancement`
### contents :
Hi,
While investigating PR78529, I came across the following issue:

For the test-case:
char *f(char *dest, char *src)
{
  if (__builtin_strcpy (dest + 5, src) != (dest + 5))
    __builtin_abort ();
}

gcc -O2 generates following assembly:

f:
.LFB0:
        .cfi_startproc
        leaq    5(%rdi), %rdx
        subq    $8, %rsp
        .cfi_def_cfa_offset 16
        movq    %rdx, %rdi
        call    strcpy
        cmpq    %rax, %rax
        jne     .L5
        addq    $8, %rsp
        .cfi_remember_state
        .cfi_def_cfa_offset 8
        ret
.L5:
        .cfi_restore_state
        call    abort
        .cfi_endproc

This seems to start after "pro_and_epligoue" pass, which contains
the following insn in it's dump:
(insn 14 29 15 2 (set (reg:CCZ 17 flags)
        (compare:CCZ (reg/f:DI 0 ax [orig:87 _1 ] [87])
            (reg:DI 0 ax [92]))) "strcpy-foo.c":3 8 {*cmpdi_1}
     (nil))

full dump: http://pastebin.com/TGMRFGyw

Thanks,
Prathamesh


---


### compiler : `gcc`
### title : `gcc doesn't exploit the fact that the result of pointer addition can not be nullptr`
### open_at : `2016-12-02T15:26:50Z`
### last_modified_date : `2022-11-17T15:47:46Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=78655
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `c++`
### version : `7.0`
### severity : `normal`
### contents :
Consider the following piece of code:

#include <memory>

struct blob
{
    void* data;
    size_t size;
};

void uninitialized_copy(blob* first, blob* last, blob* current)
{
    for (; first != last; ++first, (void) ++current) {
        ::new (static_cast<void*>(current)) blob(*first);
    }
}

The nested loop generated for it by GCC 7 is the following:

.L4:
        testq   %rdx, %rdx
        je      .L3
        movdqu  (%rdi), %xmm0
        movups  %xmm0, (%rdx)
.L3:
        addq    $16, %rdi
        addq    $16, %rdx
        cmpq    %rdi, %rsi
        jne     .L4

As you can see after each iteration generated code checks if current is nullptr and omit calling the copy constructor if it is so.

Clang 3.9 doesn't exhibit such behavior. It translates the loop into:

.LBB0_1:                                # =>This Inner Loop Header: Depth=1
        movups  (%rdi), %xmm0
        movups  %xmm0, (%rdx)
        addq    $16, %rdi
        addq    $16, %rdx
        cmpq    %rdi, %rsi
        jne     .LBB0_1

This optimization is valid, because if addition of pointer and integer results in nullptr, the integer was clearly out of bound of allocated memory block thus the addition causes undefined behavior.

Absence of this optimization affects std::uninitialized_copy and any functions that use it (for example std::vector<T>::push_back).

The issue can be reproduced with a simpler piece of code:

bool g(int* a)
{
    return (a + 10) != nullptr;
}

GCC 7:
g(int*):
        cmpq    $-40, %rdi
        setne   %al
        ret

Clang 3.9:
g(int*):                                 # @g(int*)
        movb    $1, %al
        retq

P.S. Another issue is that GCC used mismatched instructions to read from/to memory. movdqu -- is for integer data, movups -- is for single precision floating point. I don't know if it causes any stalls on modern CPUs, I heard that on older CPU writing register with an instruction of one type and reading with an instruction of another might causes stalls. Should I report a separate bug report issue for this?


---


### compiler : `gcc`
### title : `[missed optimization] gcc doesn't use clobbers to optimize constructors`
### open_at : `2016-12-07T14:00:21Z`
### last_modified_date : `2021-07-23T18:35:44Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=78713
### status : `NEW`
### tags : `missed-optimization`
### component : `libstdc++`
### version : `6.2.1`
### severity : `normal`
### contents :
Consider the following code


=== begin code ===

#include <experimental/optional>

using namespace std::experimental;

struct array_of_optional {
  optional<int> v[100];
};

array_of_optional
f(const array_of_optional& a) {
  return a;
}

=== end code ===


Compiling with -O3 (6.2.1), I get:


0000000000000000 <f(array_of_optional const&)>:
   0:    48 8d 8f 20 03 00 00     lea    0x320(%rdi),%rcx
   7:    48 89 f8                 mov    %rdi,%rax
   a:    48 89 fa                 mov    %rdi,%rdx
   d:    0f 1f 00                 nopl   (%rax)
  10:    c6 42 04 00              movb   $0x0,0x4(%rdx)
  14:    80 7e 04 00              cmpb   $0x0,0x4(%rsi)
  18:    74 0a                    je     24 <f(array_of_optional const&)+0x24>
  1a:    44 8b 06                 mov    (%rsi),%r8d
  1d:    c6 42 04 01              movb   $0x1,0x4(%rdx)
  21:    44 89 02                 mov    %r8d,(%rdx)
  24:    48 83 c2 08              add    $0x8,%rdx
  28:    48 83 c6 08              add    $0x8,%rsi
  2c:    48 39 ca                 cmp    %rcx,%rdx
  2f:    75 df                    jne    10 <f(array_of_optional const&)+0x10>
  31:    f3 c3                    repz retq


However, because we're constructing into the return value, we're under no obligation to leave the memory untouched (i.e. the memory can be considered clobbered), so this can be optimized into a memcpy, which can be significantly faster if the optionals are randomly engaged; but gcc doesn't notice that.

This is somewhat similar to using memcpy to copy a struct with holes.


---


### compiler : `gcc`
### title : `no definition of string::find when lowered to gimple`
### open_at : `2016-12-07T17:36:24Z`
### last_modified_date : `2022-08-22T11:46:19Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=78717
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `libstdc++`
### version : `7.0`
### severity : `normal`
### contents :
$ cat test.cpp

#include<string>

int foo(const std::string &s1, const std::string &s2, int i) {
 return s1.find(s2) == i;
}


../gcc/install/usr/bin/g++ -S -o a.s ../a.cpp -fdump-tree-all-all

$ cat a.cpp.004t.gimple

int foo(const string&, const string&, int) (const struct string & s1, const struct string & s2, int i)
{
  intD.9 D.27718;

  # USE = anything
  # CLB = anything
  _1 = _ZNKSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE4findERKS4_mD.18492 (s1D.24055, s2D.24056, 0);
  _2 = (long unsigned intD.14) iD.24057;
  _3 = _1 == _2;
  D.27718 = (intD.9) _3;
  return D.27718;
}


The problem is that now inliner cannot see the definition of std::string::find and hence cannot inline it. Maybe because std::basic_string<char> is an extern template, but I would hope that at least the definition should be visible to the optimizer. That would help improve the performance of programs using string::find.

Thanks,


---


### compiler : `gcc`
### title : `Regression: Splitting unaligned AVX loads also when AVX2 is enabled`
### open_at : `2016-12-10T18:00:24Z`
### last_modified_date : `2020-01-22T22:55:20Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=78762
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `7.0`
### severity : `normal`
### contents :
Created attachment 40295
Test

In gcc 7 when not optimizing for speed or newer Intel architectures unaligned AVX loads are now split.

It appears this is on purpose, and the code related to it quite old, but I haven't been able to trigger it with older versions gcc (tried 4.9, 5 and 6).

However this is a special tuning intended for Sandybridge and possibly AMD cpus. It does not trigger on any AVX2 processor. Therefore it now causes a universal performance degradation in code optimized for generic AVX2.

I suggest this tuning is disabled when avx2 is enabled.


---


### compiler : `gcc`
### title : `GCC7: Copying whole 32 bits structure field by field not optimised into copying whole 32 bits at once`
### open_at : `2016-12-15T11:24:44Z`
### last_modified_date : `2023-04-27T23:16:36Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=78821
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `7.0`
### severity : `normal`
### contents :
Compiling (ia32, -O2) a function to copy whole structure is optimised on GCC7 pre-release (g++ (GCC-Explorer-Build) 7.0.0 20161113 (experimental)):

struct S
{
  char a, b, c, d;
} u, v;

void fct (void) {
  u = v;
}

leads to:
fct():
        movl    v, %eax
        movl    %eax, u
        ret

But other ways to copy the structure are not optimised, both:
void fct (void) {
  u = (struct S){v.a, v.b, v.c, v.d};
}
and:
void fct (void) {
  u.a = v.a;
  u.b = v.b;
  u.c = v.c;
  u.d = v.d;
}

leads to:
        movzbl  v, %eax
        movb    %al, u
        movzbl  v+1, %eax
        movb    %al, u+1
        movzbl  v+2, %eax
        movb    %al, u+2
        movzbl  v+3, %eax
        movb    %al, u+3


---


### compiler : `gcc`
### title : `multiple add should in my opinion be optimized to multiplication`
### open_at : `2016-12-15T21:52:53Z`
### last_modified_date : `2019-03-04T13:06:40Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=78824
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.9.2`
### severity : `normal`
### contents :
Hi

Example  (-O3)

volatile uint16_t y;
uint8_t nvx8;

int main(void) {


	y = nvx8 + nvx8 + nvx8 + nvx8 + nvx8 + nvx8 + nvx8 + nvx8 + nvx8 + nvx8 + nvx8 + nvx8 + nvx8 + nvx8 + nvx8 + nvx8;
}

translated to:
	y = nvx8 + nvx8 + nvx8 + nvx8 + nvx8 + nvx8 + nvx8 + nvx8 + nvx8 + nvx8 + nvx8 + nvx8 + nvx8 + nvx8 + nvx8 + nvx8;
  94:	80 91 00 01 	lds	r24, 0x0100
  98:	28 2f       	mov	r18, r24
  9a:	30 e0       	ldi	r19, 0x00	; 0
  9c:	c9 01       	movw	r24, r18
  9e:	88 0f       	add	r24, r24
  a0:	99 1f       	adc	r25, r25
  a2:	88 0f       	add	r24, r24
  a4:	99 1f       	adc	r25, r25
  a6:	82 0f       	add	r24, r18
  a8:	93 1f       	adc	r25, r19
  aa:	82 0f       	add	r24, r18
  ac:	93 1f       	adc	r25, r19
  ae:	82 0f       	add	r24, r18
  b0:	93 1f       	adc	r25, r19
  b2:	82 0f       	add	r24, r18
  b4:	93 1f       	adc	r25, r19
  b6:	82 0f       	add	r24, r18
  b8:	93 1f       	adc	r25, r19
  ba:	82 0f       	add	r24, r18
  bc:	93 1f       	adc	r25, r19
  be:	82 0f       	add	r24, r18
  c0:	93 1f       	adc	r25, r19
  c2:	82 0f       	add	r24, r18
  c4:	93 1f       	adc	r25, r19
  c6:	82 0f       	add	r24, r18
  c8:	93 1f       	adc	r25, r19
  ca:	82 0f       	add	r24, r18
  cc:	93 1f       	adc	r25, r19
  ce:	82 0f       	add	r24, r18
  d0:	93 1f       	adc	r25, r19
  d2:	82 0f       	add	r24, r18
  d4:	93 1f       	adc	r25, r19
  d6:	90 93 02 01 	sts	0x0102, r25
  da:	80 93 01 01 	sts	0x0101, r24

It should be optimized to multiplication I think.


---


### compiler : `gcc`
### title : `pointer arithmetic from c++ ranged-based for loop not optimized`
### open_at : `2016-12-17T19:32:40Z`
### last_modified_date : `2019-06-15T00:40:26Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=78847
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `7.0`
### severity : `enhancement`
### contents :
GCC has some problems eliminating overhead from C++ range-based for loops. Consider the program

#include <stddef.h>
#include <cstring>
#include <experimental/string_view>
using string_view = std::experimental::string_view;

class Foo {
    constexpr static size_t Length = 9;
    char ascii_[Length];
public:
    Foo();
    string_view view() const {
        return string_view(ascii_, Length);
    }
};

void testWithLoopValue(const Foo foo, size_t ptr, char *buf_) {
  for (auto c : foo.view())
    buf_[ptr++] = c;
}

compiled as
  g++ -O3 -S -std=c++1z k.cpp


ldist determines that this is a memcpy of length expressed as _14

  _18 = (unsigned long) &MEM[(void *)&foo + 9B];
  _4 = &foo.ascii_ + 1;
  _3 = (unsigned long) _4;
  _16 = _18 + 1;
  _14 = _16 - _3;

and dom3 improves this to

  _18 = (unsigned long) &MEM[(void *)&foo + 9B];
  _3 = (unsigned long) &MEM[(void *)&foo + 1B];
  _16 = _18 + 1;
  _14 = _16 - _3;

But this is not further simplified to 9 until combine, where it is too late, and a call to memcpy is generated instead of the expected inlined version.


---


### compiler : `gcc`
### title : `-mtune=generic should keep cmp/jcc together. AMD and Intel both macro-fuse`
### open_at : `2016-12-19T02:06:25Z`
### last_modified_date : `2022-01-11T03:05:50Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=78855
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `7.0`
### severity : `normal`
### contents :
-mtune=generic and -mtune=intel currently don't optimize for macro-fusion of CMP/JCC or TEST/JCC.  They should, since it helps most CPUs from the last ~5 years or so, and I think barely hurts old / low-power (atom) ones at all.

int ffs_loop(unsigned *nums) {
    int total = 0;
    for (int i = 0; i < 1024; i++)
        total +=  __builtin_ffs(nums[i]);
    return total;
}

gcc7.0 20161113 -O3 produces:

        leaq    4096(%rdi), %rsi
        xorl    %eax, %eax
        movl    $-1, %ecx
.L2:
        bsfl    (%rdi), %edx
        cmove   %ecx, %edx
        addq    $4, %rdi

        cmpq    %rdi, %rsi         # can't macro-fuse: separated by LEA
        leal    1(%rdx,%rax), %eax
        jne     .L2                # loop branch
        ret

instead of this (with -mtune=haswell):
        ...
        leal    1(%rdx,%rax), %eax
        cmpq    %rdi, %rsi         # can macro-fuse with jne on AMD and Intel
        jne     .L2

Intel Nehalem and Sandybridge-family can macro-fuse that.  So can AMD Bulldozer-family.  In 32-bit mode, Core2 can also macro-fuse that cmp/jcc.  (See Agner's microarch pdf: http://agner.org/optimize/).  Sandybridge-family can even macro-fuse many ALU ops (like dec and sub) with some flavours of JCC, but AMD can only fuse TEST and CMP (but can do it with any JCC, even obscure ones like JP).

Bizarrely, not even -mtune=intel tries to keep compare-and-branches together.

IMO, that should be enabled in -mtune=generic and -mtune=intel, and only disabled in -mtune=atom, silvermont, k8, and k10.  (and other specific -mtune options for even older CPUs).

The penalty for doing the compare a couple instructions later on CPUs that don't support fusion might increasing the mispredict penalty by a couple cycles, I think.  So I don't think we'd be hurting Atom a lot to help more common CPUs a little.


---


### compiler : `gcc`
### title : `Virtual call after conversion to base class pointer is not devirtualized`
### open_at : `2016-12-20T23:18:54Z`
### last_modified_date : `2021-12-08T08:07:25Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=78873
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `c++`
### version : `7.0`
### severity : `normal`
### contents :
The following test case shows the issue. The generated code for TestDevirtualization<Impl> could perform a direct call to Impl::Foo but it performs a call via the vtable.

#include <stdio.h>

struct Iface {
    virtual void Foo() = 0;
};

struct Impl : public Iface {
    __attribute__ ((noinline))
    void Foo() override final
    {
        printf("Impl::Foo\n");
    }
};

template <typename Type>
__attribute__ ((noinline))
void TestDevirtualuzation(Type *obj)
{
    static_cast<Iface *>(obj)->Foo();
}

int main() {
    Impl impl;
    TestDevirtualuzation(&impl);
    return 0;
}

I have heard arguments that optimizing this would not be legal, with the following test case which supposedly might be valid:

struct Liar : Iface {
  void Foo() {}
};

Impl impl;
TestDevirtualuzation(reinterpret_cast<Liar*>(&impl));

But I think it is not valid; the result of the reinterpret_cast does not point to a Liar object, so the static_cast done in TestDevirtualuzation *should* be invalid. I couldn't find a clear statement in the standard about this though.


---


### compiler : `gcc`
### title : `toupper(x) can be assumed not to be in the range 'a' - 'z'`
### open_at : `2016-12-21T17:11:04Z`
### last_modified_date : `2021-07-26T23:31:47Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=78888
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `7.0`
### severity : `enhancement`
### contents :
The return value of the toupper function is guaranteed not to be in the range 'a' - 'z'.  Similarly, the tolower return value is guaranteed not to be in the range 'A' - 'Z'.  For non-EBCDIC character sets, it would be useful to set the range on the return value reflecting this constrained range.  (The range is actually the intersection of the range [0, UCHAR_MAX] and the anti-range ~['a', 'z'], plus the value EOF).

In addition, it would be useful to issue a warning if the return value is compared against a constant from its anti-range since such a comparison in always false (this might naturally fall out of the optimization).

The following test case shows that GCC does not take advantage of this optimization (it doesn't remove the call to f()) or issue the warning.

$ cat d.c && gcc -O2 -S -Wall -Wextra -Wpedantic -fdump-tree-optimized=/dev/stdout d.c 
void f (void);

void g (int x)
{
  if (__builtin_toupper ((unsigned char)x) == 'a')
    f ();
}

;; Function g (g, funcdef_no=0, decl_uid=1797, cgraph_uid=0, symbol_order=0)

Removing basic block 5
g (int x)
{
  int _1;
  int _6;

  <bb 2> [100.00%]:
  _6 = x_3(D) & 255;
  _1 = __builtin_toupper (_6);
  if (_1 == 97)
    goto <bb 3>; [22.95%]
  else
    goto <bb 4>; [77.05%]

  <bb 3> [22.95%]:
  f (); [tail call]

  <bb 4> [100.00%]:
  return;

}


---


### compiler : `gcc`
### title : `Add warn_unused_attribute for builtins with alloc_size`
### open_at : `2016-12-22T14:09:53Z`
### last_modified_date : `2019-06-10T09:08:50Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=78902
### status : `RESOLVED`
### tags : `diagnostic, missed-optimization`
### component : `tree-optimization`
### version : `unknown`
### severity : `enhancement`
### contents :
This is follow-up of PR78886.


---


### compiler : `gcc`
### title : `suboptimal code for x % C1 == C2`
### open_at : `2016-12-23T23:45:38Z`
### last_modified_date : `2021-10-01T02:59:02Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=78916
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `5.1.0`
### severity : `normal`
### contents :
Everything below applies to the case of unsigned operands; signed division is a whole other matter.

When a is an odd constant, the expression x % a == 0 is equivalent to x*inv(a) <= ~0U/a, where inv(a) is the mod-2^32 multiplicative inverse of a. More generally, x % a == b can be rewritten as x*inv(a) - b*inv(a) <= (~0U - b)/a, where everything but the first multiplication are compile-time constants, and the comparison is unsigned. gcc seems to always compute the full remainder and compare that to the RHS.

For example,

int f(unsigned x) { return x % 3 == 0; }

could compile to

  20:   69 ff ab aa aa aa       imul   $0xaaaaaaab,%edi,%edi
  26:   31 c0                   xor    %eax,%eax
  28:   81 ff 55 55 55 55       cmp    $0x55555555,%edi
  2e:   0f 96 c0                setbe  %al
  31:   c3                      retq   

but gcc generates

   0:   89 f8                   mov    %edi,%eax
   2:   ba ab aa aa aa          mov    $0xaaaaaaab,%edx
   7:   f7 e2                   mul    %edx
   9:   d1 ea                   shr    %edx
   b:   8d 04 52                lea    (%rdx,%rdx,2),%eax
   e:   39 c7                   cmp    %eax,%edi
  10:   0f 94 c0                sete   %al
  13:   0f b6 c0                movzbl %al,%eax
  16:   c3                      retq   

If gcc needs to compute the quotient x/a anyway, computing the remainder from that may be optimal, but in the somewhat realistic case where the quotient is only used if the division is exact, it's much better to compute the tentative quotient as above and test that, e.g.

unsigned f(unsigned x);
unsigned g(unsigned x)
{
	return (x % 7U == 0) ? f(x / 7U) : 0;
}

should/could be compiled as

unsigned h(unsigned x)
{
	return (x * 3067833783U <= (~0U)/7) ? f(x * 3067833783U) : 0;
}

0000000000000080 <g>:
  80:   89 f8                   mov    %edi,%eax
  82:   ba 25 49 92 24          mov    $0x24924925,%edx
  87:   f7 e2                   mul    %edx
  89:   89 f8                   mov    %edi,%eax
  8b:   29 d0                   sub    %edx,%eax
  8d:   d1 e8                   shr    %eax
  8f:   01 c2                   add    %eax,%edx
  91:   c1 ea 02                shr    $0x2,%edx
  94:   8d 04 d5 00 00 00 00    lea    0x0(,%rdx,8),%eax
  9b:   29 d0                   sub    %edx,%eax
  9d:   39 c7                   cmp    %eax,%edi
  9f:   74 07                   je     a8 <g+0x28>
  a1:   31 c0                   xor    %eax,%eax
  a3:   c3                      retq   
  a4:   0f 1f 40 00             nopl   0x0(%rax)
  a8:   89 d7                   mov    %edx,%edi
  aa:   e9 00 00 00 00          jmpq   af <g+0x2f>
  af:   90                      nop

00000000000000b0 <h>:
  b0:   69 ff b7 6d db b6       imul   $0xb6db6db7,%edi,%edi
  b6:   81 ff 24 49 92 24       cmp    $0x24924924,%edi
  bc:   76 0a                   jbe    c8 <h+0x18>
  be:   31 c0                   xor    %eax,%eax
  c0:   c3                      retq   
  c1:   0f 1f 80 00 00 00 00    nopl   0x0(%rax)
  c8:   e9 00 00 00 00          jmpq   cd <h+0x1d>


---


### compiler : `gcc`
### title : `[missed optimization] Useless guard variable in thread_local defaulted constructor`
### open_at : `2016-12-28T11:29:47Z`
### last_modified_date : `2023-03-24T00:56:51Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=78940
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `c++`
### version : `6.3.1`
### severity : `normal`
### contents :
If I write

    extern thread_local std::atomic<int> foo;

gcc will emit guard variables everywhere to ensure it is properly constructed before use.  The workaround is to wrap foo in an inline function, so the compiler can see its definition.  That doesn't work when the constructor is defaulted:

//////////// begin example ////////////////

// following libstdc++ std::atomic
template <typename T>
struct my_atomic {
  T n;
  my_atomic() = default;
  explicit constexpr my_atomic(T n) : n(n) {}
  T load() const { return n; }
};

inline
my_atomic<int>&
a1() {
  static thread_local my_atomic<int> v;
  return v;
}

inline
my_atomic<int>&
a2() {
  static thread_local my_atomic<int> v{0};
  return v;
}

int foo() {
  return a1().load() + a2().load();
}


//////////////// end example //////////////////////


This compiles to

0000000000000000 <foo()>:
   0:	64 80 3c 25 00 00 00 	cmpb   $0x0,%fs:0x0
   7:	00 00 
			4: R_X86_64_TPOFF32	guard variable for a1()::v
   9:	75 09                	jne    14 <foo()+0x14>
   b:	64 c6 04 25 00 00 00 	movb   $0x1,%fs:0x0
  12:	00 01 
			f: R_X86_64_TPOFF32	guard variable for a1()::v
  14:	64 8b 04 25 00 00 00 	mov    %fs:0x0,%eax
  1b:	00 
			18: R_X86_64_TPOFF32	a2()::v
  1c:	64 03 04 25 00 00 00 	add    %fs:0x0,%eax
  23:	00 
			20: R_X86_64_TPOFF32	a1()::v
  24:	c3                   	retq  


The test for "guard variable for a1()::v" is clearly useless, since no initialization of a1()::v takes place.  gcc correctly omits the guard variable for a2()::v.


---


### compiler : `gcc`
### title : `sub-optimal code for (bool)(int ? int : int)`
### open_at : `2016-12-29T02:53:33Z`
### last_modified_date : `2022-01-30T23:01:57Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=78947
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `6.3.0`
### severity : `enhancement`
### contents :
Full version: http://stackoverflow.com/questions/41323911/why-the-difference-in-code-generation-for-bool-bool-int-int


bool condSet(int cond, int a, int b) {
    return cond ? a : b;
}

clang and icc use a cmov to select a or b, and then booleanize that.

g++6.3 -O3 decides to booleanize b, then check the condition and if necessary booleanize a into %al.  This is pretty obviously sub-optimal, even if a branch is better than a cmov for a predictable condition.  (And it differs from what gcc does if the return type is int)

condSet(int, int, int):
        testl   %edx, %edx    # b
        setne   %al           #, <retval>
        testl   %edi, %edi    # cond
        jne     .L6           #,
        rep ret
.L6:
        testl   %esi, %esi    # a
        setne   %al           #, <retval>
        ret



Writing the function as 

  int foo = cond ? a : b;
  return foo;

gets g++ to select an operand with cmov and then booleanize it, like clang does in the first place (looks optimal to me):

        testl   %edi, %edi
        cmovel  %edx, %esi
        testl   %esi, %esi
        setne   %al
        retq


---


### compiler : `gcc`
### title : `[missed optimization] using 3-byte instead of 4-byte variables causes unnecessary work on the stack`
### open_at : `2017-01-01T10:26:01Z`
### last_modified_date : `2021-09-14T17:45:20Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=78963
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `6.3.0`
### severity : `normal`
### contents :
Preliminary notes:
* This bug report stems from a StackOverflow question I asked: http://stackoverflow.com/q/41407257/1593077
* This bug regards the x86_64 architecture, but may apply elsewhere.
* This bug regards -O3 optimizations
* Everything described here is about the same for GCC 6.3 and 7 - whatever version of it GodBolt uses.
* The entire bug is demonstrated here: https://godbolt.org/g/lDJSRm plus here https://godbolt.org/g/9Y2ebd


Consider the task of copying 3-byte values from one place to another. If both those places are in memory, it seems reasonable to do four moves, and indeed GCC compiles this:

  #include <string.h>

  typedef struct { unsigned char data[3]; } uint24_t;

  void f(uint24_t* __restrict__ dest, uint24_t* __restrict__ src) { memcpy(dest,src,3); }

into this (clipping the instructions for the return value): 

  f(uint24_t*, uint24_t*):
          movzx   eax, WORD PTR [rsi]
          mov     WORD PTR [rdi], ax
          movzx   eax, BYTE PTR [rsi+2]
          mov     BYTE PTR [rdi+2], al

If the source or the destination is a register, two mov's should suffice - either the first two or the second two of the above. However, if I write this (perhaps contrived, but likely demonstrative of what could happen with larger programs, especially with multi-translation units, or when the OS gives you a pointer to work with etc):

  #include <string.h>
  
  typedef struct { unsigned char data[3]; } uint24_t;
  
  void f(uint24_t* __restrict__ dest, uint24_t* __restrict__ src) { memcpy(dest,src,3); }
  
  int main() {
    uint24_t* p = (uint24_t*) 48;
    unsigned x;
    f((uint24_t*) &x,p);
    x += 1;
    f(p,(uint24_t*) &x);
    return 0;
  }

The 3-byte value is "constructed" on the stack rather than in a register (first four mov's), and then one cannot avoid using four more mov's to copy it to the destination:

        movzx   eax, WORD PTR ds:48
        mov     WORD PTR [rsp-4], ax
        movzx   eax, BYTE PTR ds:50
        mov     BYTE PTR [rsp-2], al
        add     DWORD PTR [rsp-4], 1
        movzx   eax, WORD PTR [rsp-4]
        mov     WORD PTR ds:48, ax
        movzx   eax, BYTE PTR [rsp-2]
        mov     BYTE PTR ds:50, al


If we do this with 4-byte values, i.e. replace uint24_t with uint32_t, it's a single mov both ways, and in fact it gets further optimized, so that this:

  #include <string.h>
  #include <stdint.h> 

  void f(uint32_t* __restrict__ dest, uint32_t* __restrict__ src)
  {
    memcpy(dest,src,4);
  }

 int main() {
    uint32_t* p = (uint32_t*) 48;
    uint32_t x;
    f(&x,p);
    x += 1;
    f(p,&x);
    return 0;
  }


is compiled into just this

        add     DWORD PTR ds:48, 1

Now obviously you can't expect to optimize-out _that_ much with a 3-byte value, but 2 mov's in and 2 mov's out should be enough. Indeed, clang (since at least 3.4.1 or so) emits this for the uint24_t code:

        movzx   eax, byte ptr [50]
        shl     eax, 16
        movzx   ecx, word ptr [48]
        lea     eax, [rcx + rax + 1]
        mov     word ptr [48], ax
        shr     eax, 16
        mov     byte ptr [50], al

which has just four mov's.


---


### compiler : `gcc`
### title : `bogus snprintf truncation warning due to missing range info`
### open_at : `2017-01-02T18:55:44Z`
### last_modified_date : `2021-12-15T15:45:33Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=78969
### status : `RESOLVED`
### tags : `diagnostic, missed-optimization`
### component : `tree-optimization`
### version : `7.0`
### severity : `normal`
### contents :
In both functions in the following test case the %3u argument to snprintf is in the range [0, 999] and so the directive writes exactly 3 bytes into the destination buffer of size 4.  As the VRP dump shows, GCC exposes that range to the -Wformat-length checker via the get_range_info() function in the call in function f() allowing it to avoid a warning.  But in the call in function g(), even though the same range is also known, it's not made available for the argument to the directive, resulting in a false positive.

$ cat t.c && gcc -O2 -S -Wall -Wformat-length=2 -fdump-tree-vrp=/dev/stdout t.c 
void f (unsigned j, char *p)
{
  if (j > 999)
    j = 0;

  __builtin_snprintf (p, 4, "%3u", j);
}

void g (unsigned j, char *p)
{
  if (j > 999)
    return;

  __builtin_snprintf (p, 4, "%3u", j);
}




;; Function f (f, funcdef_no=0, decl_uid=1796, cgraph_uid=0, symbol_order=0)

;; 1 loops found
;;
;; Loop 0
;;  header 0, latch 1
;;  depth 0, outer -1
;;  nodes: 0 1 2 3 4
;; 2 succs { 3 4 }
;; 3 succs { 4 }
;; 4 succs { 1 }

SSA replacement table
N_i -> { O_1 ... O_j } means that N_i replaces O_1, ..., O_j

j_6 -> { j_2(D) }
j_7 -> { j_2(D) }
Incremental SSA update started at block: 2
Number of blocks in CFG: 6
Number of blocks to update: 4 ( 67%)



Value ranges after VRP:

j_1: [0, 999]  EQUIVALENCES: { } (0 elements)
j_2(D): VARYING
j_6: [1000, +INF]  EQUIVALENCES: { j_2(D) } (1 elements)
j_7: [0, 999]  EQUIVALENCES: { j_2(D) } (1 elements)


Removing basic block 3
f (unsigned int j, char * p)
{
  <bb 2> [100.00%]:
  if (j_2(D) > 999)
    goto <bb 4>; [54.00%]
  else
    goto <bb 3>; [46.00%]

  <bb 3> [46.00%]:

  <bb 4> [100.00%]:
  # j_1 = PHI <j_2(D)(3), 0(2)>
  __builtin_snprintf (p_4(D), 4, "%3u", j_1);
  return;

}



;; Function f (f, funcdef_no=0, decl_uid=1796, cgraph_uid=0, symbol_order=0)

;; 1 loops found
;;
;; Loop 0
;;  header 0, latch 1
;;  depth 0, outer -1
;;  nodes: 0 1 2 3 4
;; 2 succs { 3 4 }
;; 3 succs { 4 }
;; 4 succs { 1 }

SSA replacement table
N_i -> { O_1 ... O_j } means that N_i replaces O_1, ..., O_j

j_6 -> { j_2(D) }
j_7 -> { j_2(D) }
Incremental SSA update started at block: 2
Number of blocks in CFG: 6
Number of blocks to update: 4 ( 67%)



Value ranges after VRP:

j_1: [0, 999]  EQUIVALENCES: { } (0 elements)
j_2(D): VARYING
j_6: [1000, +INF]  EQUIVALENCES: { j_2(D) } (1 elements)
j_7: [0, 999]  EQUIVALENCES: { j_2(D) } (1 elements)


Removing basic block 3
f (unsigned int j, char * p)
{
  <bb 2> [100.00%]:
  if (j_2(D) > 999)
    goto <bb 4>; [54.00%]
  else
    goto <bb 3>; [46.00%]

  <bb 3> [46.00%]:

  <bb 4> [100.00%]:
  # j_1 = PHI <j_2(D)(3), 0(2)>
  __builtin_snprintf (p_4(D), 4, "%3u", j_1);
  return;

}



;; Function g (g, funcdef_no=1, decl_uid=1800, cgraph_uid=1, symbol_order=1)

;; 1 loops found
;;
;; Loop 0
;;  header 0, latch 1
;;  depth 0, outer -1
;;  nodes: 0 1 2 3 4
;; 2 succs { 4 3 }
;; 3 succs { 4 }
;; 4 succs { 1 }

SSA replacement table
N_i -> { O_1 ... O_j } means that N_i replaces O_1, ..., O_j

j_6 -> { j_2(D) }
Incremental SSA update started at block: 2
Number of blocks in CFG: 5
Number of blocks to update: 2 ( 40%)



Value ranges after VRP:

.MEM_1: VARYING
j_2(D): VARYING
j_6: [0, 999]  EQUIVALENCES: { j_2(D) } (1 elements)


g (unsigned int j, char * p)
{
  <bb 2> [100.00%]:
  if (j_2(D) > 999)
    goto <bb 4>; [51.01%]
  else
    goto <bb 3>; [48.99%]

  <bb 3> [48.99%]:
  __builtin_snprintf (p_4(D), 4, "%3u", j_2(D));

  <bb 4> [100.00%]:
  return;

}


t.c: In function ‘g’:
t.c:14:30: warning: ‘%3u’ directive output may be truncated writing between 3 and 10 bytes into a region of size 4 [-Wformat-length=]
   __builtin_snprintf (p, 4, "%3u", j);
                              ^~~
t.c:14:29: note: using the range [1, 4294967295] for directive argument
   __builtin_snprintf (p, 4, "%3u", j);
                             ^~~~~
t.c:14:3: note: format output between 4 and 11 bytes into a destination of size 4
   __builtin_snprintf (p, 4, "%3u", j);
   ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

;; Function g (g, funcdef_no=1, decl_uid=1800, cgraph_uid=1, symbol_order=1)

;; 1 loops found
;;
;; Loop 0
;;  header 0, latch 1
;;  depth 0, outer -1
;;  nodes: 0 1 2 3 4
;; 2 succs { 4 3 }
;; 3 succs { 4 }
;; 4 succs { 1 }

SSA replacement table
N_i -> { O_1 ... O_j } means that N_i replaces O_1, ..., O_j

j_6 -> { j_2(D) }
Incremental SSA update started at block: 2
Number of blocks in CFG: 5
Number of blocks to update: 2 ( 40%)



Value ranges after VRP:

.MEM_1: VARYING
j_2(D): VARYING
j_6: [0, 999]  EQUIVALENCES: { j_2(D) } (1 elements)


g (unsigned int j, char * p)
{
  <bb 2> [100.00%]:
  if (j_2(D) > 999)
    goto <bb 4>; [51.01%]
  else
    goto <bb 3>; [48.99%]

  <bb 3> [48.99%]:
  __builtin_snprintf (p_4(D), 4, "%3u", j_2(D));

  <bb 4> [100.00%]:
  return;

}


---


### compiler : `gcc`
### title : `-Ofast makes aarch64 C++ benchmark slower for A53`
### open_at : `2017-01-04T22:32:14Z`
### last_modified_date : `2021-05-04T12:32:10Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=78994
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `target`
### version : `5.4.0`
### severity : `normal`
### contents :
Created attachment 40463
Preprocessed source + assembly files

After make && ./build/dsp-bench, the results look as follows

@ -O3 -mcpu=cortex-a53 -ftree-vectorize

iir:    67945 ns per loop
iir_2:  67952 ns per loop

@ -Ofast -mcpu=cortex-a53 -ftree-vectorize

iir:    73367 ns per loop
iir_2:  73349 ns per loop


---


### compiler : `gcc`
### title : `Weird c++ assembly code generated for tail call`
### open_at : `2017-01-05T12:23:05Z`
### last_modified_date : `2021-07-28T05:37:56Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=79002
### status : `NEW`
### tags : `EH, missed-optimization`
### component : `tree-optimization`
### version : `unknown`
### severity : `normal`
### contents :
G++ (r244001) generates some pretty weird assembly code on s390x for this test case.  (Note that j is not initialised and I couldn't find a variant of this test case where it is).

-- test.C --
int g;
unsigned char *p;
void r1()
{
  int i;
  int j;
  i = *p;
  if (j <= g || (i) != 1) // <---- note: parentheses around (i)
    r1();
}
------------

$ gcc -O3 -march=z10 -mzarch -m64 -S test.C
$ cat test.s

--
_Z2r1v:
        lgrl    %r2,p      <-- r2 := &p
        lrl     %r1,g      <-- r1 := &g
        llc     %r2,0(%r2) <-- r2 := *r2
.L5:
        cijlh   %r2,1,.L2  <-- compare with immediate and jump if !=
.L4:
        cijhe   %r1,0,.L11 <-- ... if >=
.L1:
        br      %r14
.L11:
        cijl    %r1,0,.L1  <-- ... if <
        cijl    %r1,0,.L1
        cijhe   %r1,0,.L4
        br      %r14
.L2:
        cijl    %r1,0,.L5
        cijl    %r1,0,.L5
        j       .L2
--

If the parentheses are removed from "(i)", the result is sane:

  ...
  if (j <= g || i != 1) // <---- note: no parentheses around i
  ...

--
_Z2r1v:
        lgrl    %r2,p
        lrl     %r1,g
        llc     %r2,0(%r2)
.L2:
        cijhe   %r1,0,.L2
        cijlh   %r2,1,.L2
        br      %r14
--

Not tested on other targets, but to me it looks like a general C++ problem (does not happen with the C compiler, at least not with this test case).  While the generated code is valid, this effect makes reducing test cases from the Spec2006 suite harder (there are variants of the code that result in even more unnecessary labels and assembly code).  It might be possible to trigger this without relying on undefined variables.


---


### compiler : `gcc`
### title : `Un-optimal/ incorrect forward propagation`
### open_at : `2017-01-09T07:49:23Z`
### last_modified_date : `2023-08-22T04:45:33Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=79028
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `7.0`
### severity : `normal`
### contents :
test case: (options: -Os)
typedef unsigned int uint8_t __attribute__((__mode__(__QI__)));                                                                      
typedef unsigned int uint32_t __attribute__ ((__mode__ (__SI__)));
typedef struct rpl_instance rpl_instance_t;
struct rpl_instance {
  uint8_t dio_intcurrent;
  uint32_t dio_next_delay;
};
unsigned short random_rand(void);

void
new_dio_interval(rpl_instance_t *instance)
{
  uint32_t time;
  uint32_t ticks;
  time = 1UL << instance->dio_intcurrent;
  ticks = (time * 128) / 1000;
  instance->dio_next_delay = ticks;
  ticks = ticks / 2 + (ticks / 2 * (uint32_t)random_rand()) / 65535U;
  instance->dio_next_delay -= ticks;
}

tree dump before and after optimizations
(snip from ssa dump)
 _1 = instance_14(D)->dio_intcurrent;
 _2 = (int) _1;
 _3 = 1 << _2;
 time_15 = (uint32_t) _3;
 _4 = time_15 * 128;
 ticks_16 = _4 / 1000;
 instance_14(D)->dio_next_delay = ticks_16;
 _5 = ticks_16 / 2;
 _6 = ticks_16 / 2;
 _7 = random_rand ();
 _8 = (unsigned int) _7;
 _9 = _6 * _8;
 _10 = _9 / 65535;
 ticks_19 = _5 + _10;
 _11 = instance_14(D)->dio_next_delay;
 _12 = _11 - ticks_19;
 instance_14(D)->dio_next_delay = _12;
 return;
(snip)

gcc-7 propagates ticks_16 to definitions of _5 and _6 as part of forwprop1 pass. It contradicts the  descriptions "substituting variables that are used once into the expression".

(snip from optimized dump)
  <bb 2> [100.00%]:
  _1 = instance_13(D)->dio_intcurrent;
  _2 = (int) _1;
  _3 = 1 << _2;
  time_14 = (uint32_t) _3;
  _4 = time_14 * 128;
  ticks_15 = _4 / 1000;
  instance_13(D)->dio_next_delay = ticks_15;
  _5 = _4 / 2000;
  _6 = random_rand ();
  _7 = (unsigned int) _6;
  _8 = _5 * _7;
  _9 = _8 / 65535;
  _10 = instance_13(D)->dio_next_delay;
  _23 = _10 - _5;
  _11 = _23 - _9;
  instance_13(D)->dio_next_delay = _11;
  return;
(snip)

Without that forward propagation, _5 would be _5 = ticks_15 >> 1, that is optimal than the current code.
Till gcc-4 it was optimal for this case, got changed gcc-5 onwards.


---


### compiler : `gcc`
### title : `bool&bool expanded as 2 jumps`
### open_at : `2017-01-10T14:56:18Z`
### last_modified_date : `2023-09-24T22:05:21Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=79045
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `7.0`
### severity : `enhancement`
### contents :
From http://stackoverflow.com/q/41508563/1918193

extern void g();
void f1(char a,char b){ if(a&b)g(); }
void f2(bool a,bool b){ if(a&b)g(); }

f1 gives the nice

	testb	%dil, %sil
	jne	.L4
	rep ret
.L4:
	jmp	_Z1gv

while f2 gives the uglier

	testb	%dil, %dil
	je	.L5
	testb	%sil, %sil
	je	.L5
	jmp	_Z1gv
.L5:
	rep ret

From my understanding of the ABI, the same code generated for f1 would also be valid for f2.


---


### compiler : `gcc`
### title : `loop annotation ignored in templated function`
### open_at : `2017-01-10T18:13:36Z`
### last_modified_date : `2021-07-31T22:07:46Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=79047
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `c++`
### version : `5.4.0`
### severity : `normal`
### contents :
Created attachment 40496
exploit

#pragma GCC ivdep
is ignored in a templated function:

simple.cc: In member function ‘void VectorT<T>::add(const VectorT<T>&) [with T = float]’:
simple.cc:37:20: warning: ignoring loop annotation
     for( int x = 0 ; x < r.count() ; x++ ) {


simple.cc:37:20: note: loop vectorized
simple.cc:37:20: note: loop versioned for vectorization because of possible aliasing
simple.cc:37:20: note: loop peeled for vectorization to enhance alignment


I attach an example that demonstrates this behavior. Compiled with

g++ -O3  -fopt-info-vec simple.cc

g++ (Ubuntu 5.4.0-6ubuntu1~16.04.4) 5.4.0 20160609

The examples also shows that vectorization works for the same function if we remove the template. Thus, the problem is that the loop annotation is not passed down to the template instantiation of the function. (Otherwise I cannot explain the behavior as the functions are identical.)


---


### compiler : `gcc`
### title : `Unnecessary reload for flags setting insn when operands die`
### open_at : `2017-01-10T19:04:13Z`
### last_modified_date : `2021-11-25T22:19:54Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=79048
### status : `RESOLVED`
### tags : `missed-optimization, ra`
### component : `rtl-optimization`
### version : `7.0`
### severity : `normal`
### contents :
Following testcase:

extern void g();
void f1(char a,char b){ if(a|b)g(); }

compiles to (-O2):

f1:
        movl    %esi, %eax
        orb     %dil, %al
        jne     .L4

Note that reload fails to figure out that both registers die in (insn 10):

(insn 10 9 11 2 (parallel [
            (set (reg:CCZ 17 flags)
                (compare:CCZ (ior:QI (subreg:QI (reg:SI 91 [ b ]) 0)
                        (subreg:QI (reg:SI 89 [ a ]) 0))
                    (const_int 0 [0])))
            (clobber (scratch:QI))
        ]) "pr79045.c":2 437 {*iorqi_3}
     (expr_list:REG_DEAD (reg:SI 91 [ b ])
        (expr_list:REG_DEAD (reg:SI 89 [ a ])
            (nil))))

RA could allocate %esi (or even %edi, iorqi_3 has commutative operands)
as a matched output scratch, but instead generates an unnecessary reload with additional temporary register, bloating the code and increasing register pressure:

(insn 21 9 10 2 (set (reg:QI 0 ax [93])
        (reg:QI 4 si [orig:91 b ] [91])) "pr79045.c":2 84 {*movqi_internal}
     (nil))
(insn 10 21 11 2 (parallel [
            (set (reg:CCZ 17 flags)
                (compare:CCZ (ior:QI (reg:QI 0 ax [93])
                        (reg:QI 5 di [orig:89 a ] [89]))
                    (const_int 0 [0])))
            (clobber (reg:QI 0 ax [93]))
        ]) "pr79045.c":2 437 {*iorqi_3}
     (nil))

Ideally, RA should use dead input reg to allocate as matched scratch, possibly also exploiting "%" operand modifier.


---


### compiler : `gcc`
### title : `missing range information with INT_MAX`
### open_at : `2017-01-11T02:38:53Z`
### last_modified_date : `2021-08-16T08:04:46Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=79054
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `7.0`
### severity : `normal`
### contents :
This is a test case reduced from bug 79051 showing that GCC seems to "lose" range information for expressions in functions that contain other expressions involving limits such as INT_MAX in unrelated statement.  In the test program, function foobar() contains the two statements from functions foo() and bar().  In each of foo() and bar(), GCC correctly represents the range of the argument in the call to the function alloc().  But in foobar(), unlike in foo(), the range of the argument in the first call to alloc() is lost (it's VR_VARYING).  This can be seen in both the VRP dumps and by the absence of the -Walloc-size-larger-than warning for that call in foobar().

$ cat t.c && gcc -O2 -S -Wall -Walloc-size-larger-than=1234 -fdump-tree-vrp=/dev/stdout t.c
#define INT_MAX   __INT_MAX__
#define INT_MIN   (-INT_MAX - 1)

void sink (void*);
void* alloc (int) __attribute__ ((alloc_size (1)));

int anti_range (int min, int max)
{
  extern int value (void);
  int val = value ();
  if (min <= val && val <= max)
    val = min - 1;
  return val;
}

void foo (int n)
{
  sink (alloc (anti_range (INT_MIN + 2, 1235)));
}

void bar (int n)
{
  sink (alloc (anti_range (0, INT_MAX)));
}

void foobar (int n)
{
  sink (alloc (anti_range (INT_MIN + 2, 1235)));
  sink (alloc (anti_range (0, INT_MAX)));
}

;; Function anti_range (anti_range, funcdef_no=0, decl_uid=2522, cgraph_uid=0, symbol_order=0)

;; 1 loops found
;;
;; Loop 0
;;  header 0, latch 1
;;  depth 0, outer -1
;;  nodes: 0 1 2 3 4 5
;; 2 succs { 3 5 }
;; 3 succs { 4 5 }
;; 4 succs { 5 }
;; 5 succs { 1 }

SSA replacement table
N_i -> { O_1 ... O_j } means that N_i replaces O_1, ..., O_j

val_8 -> { val_4 }
val_9 -> { val_4 }
val_10 -> { val_4 }
val_11 -> { val_4 }
min_12 -> { min_5(D) }
Incremental SSA update started at block: 2
Number of blocks in CFG: 8
Number of blocks to update: 6 ( 75%)



Value ranges after VRP:

val_1: VARYING
val_4: VARYING
min_5(D): VARYING
max_6(D): VARYING
val_7: VARYING
val_8: [-INF, max_6(D)]  EQUIVALENCES: { val_4 val_10 } (2 elements)
val_9: [max_6(D) + 1, +INF]  EQUIVALENCES: { val_4 val_10 } (2 elements)
val_10: [min_5(D), +INF]  EQUIVALENCES: { val_4 } (1 elements)
val_11: [-INF, min_5(D) + -1]  EQUIVALENCES: { val_4 } (1 elements)
min_12: [-INF, val_10]  EQUIVALENCES: { min_5(D) } (1 elements)


Removing basic block 6
Removing basic block 7
anti_range (int min, int max)
{
  int val;

  <bb 2> [100.00%]:
  val_4 = value ();
  if (val_4 >= min_5(D))
    goto <bb 3>; [54.00%]
  else
    goto <bb 5>; [46.00%]

  <bb 3> [54.00%]:
  if (val_4 <= max_6(D))
    goto <bb 4>; [54.00%]
  else
    goto <bb 5>; [46.00%]

  <bb 4> [29.16%]:
  val_7 = min_5(D) + -1;

  <bb 5> [100.00%]:
  # val_1 = PHI <val_4(2), val_4(3), val_7(4)>
  return val_1;

}



;; Function anti_range (anti_range, funcdef_no=0, decl_uid=2522, cgraph_uid=0, symbol_order=0)

;; 1 loops found
;;
;; Loop 0
;;  header 0, latch 1
;;  depth 0, outer -1
;;  nodes: 0 1 2 3 4 5
;; 2 succs { 3 5 }
;; 3 succs { 4 5 }
;; 4 succs { 5 }
;; 5 succs { 1 }

SSA replacement table
N_i -> { O_1 ... O_j } means that N_i replaces O_1, ..., O_j

val_8 -> { val_4 }
val_9 -> { val_4 }
val_10 -> { val_4 }
min_11 -> { min_5(D) }
val_12 -> { val_4 }
Incremental SSA update started at block: 2
Number of blocks in CFG: 8
Number of blocks to update: 6 ( 75%)



Value ranges after VRP:

val_1: VARYING
val_4: VARYING
min_5(D): VARYING
max_6(D): VARYING
val_7: VARYING
val_8: [-INF, max_6(D)]  EQUIVALENCES: { val_4 val_12 } (2 elements)
val_9: [max_6(D) + 1, +INF]  EQUIVALENCES: { val_4 val_12 } (2 elements)
val_10: [-INF, min_5(D) + -1]  EQUIVALENCES: { val_4 } (1 elements)
min_11: [-INF, val_12]  EQUIVALENCES: { min_5(D) } (1 elements)
val_12: [min_5(D), +INF]  EQUIVALENCES: { val_4 } (1 elements)


Removing basic block 6
Removing basic block 7
anti_range (int min, int max)
{
  int val;

  <bb 2> [100.00%]:
  val_4 = value ();
  if (val_4 >= min_5(D))
    goto <bb 3>; [54.00%]
  else
    goto <bb 5>; [46.00%]

  <bb 3> [54.00%]:
  if (val_4 <= max_6(D))
    goto <bb 4>; [54.00%]
  else
    goto <bb 5>; [46.00%]

  <bb 4> [29.16%]:
  val_7 = min_5(D) + -1;

  <bb 5> [100.00%]:
  # val_1 = PHI <val_4(2), val_4(3), val_7(4)>
  return val_1;

}



;; Function foo (foo, funcdef_no=1, decl_uid=2529, cgraph_uid=1, symbol_order=1)

;; 1 loops found
;;
;; Loop 0
;;  header 0, latch 1
;;  depth 0, outer -1
;;  nodes: 0 1 2 3 4 5
;; 2 succs { 3 5 }
;; 3 succs { 4 5 }
;; 4 succs { 5 }
;; 5 succs { 1 }

SSA replacement table
N_i -> { O_1 ... O_j } means that N_i replaces O_1, ..., O_j

val_8 -> { val_5 }
val_9 -> { val_5 }
val_10 -> { val_5 }
val_11 -> { val_5 }
Incremental SSA update started at block: 2
Number of blocks in CFG: 8
Number of blocks to update: 6 ( 75%)



Value ranges after VRP:

_1: VARYING
val_5: VARYING
val_6: ~[-2147483646, 1235]  EQUIVALENCES: { } (0 elements)
val_8: [-2147483646, 1235]  EQUIVALENCES: { val_5 val_10 } (2 elements)
val_9: [1236, +INF]  EQUIVALENCES: { val_5 val_10 } (2 elements)
val_10: [-2147483646, +INF]  EQUIVALENCES: { val_5 } (1 elements)
val_11: [-INF, -2147483647]  EQUIVALENCES: { val_5 } (1 elements)


Removing basic block 4
Removing basic block 6
foo (int n)
{
  int val;
  void * _1;

  <bb 2> [100.00%]:
  val_5 = value ();
  if (val_5 >= -2147483646)
    goto <bb 3>; [54.00%]
  else
    goto <bb 5>; [46.00%]

  <bb 3> [54.00%]:
  if (val_5 <= 1235)
    goto <bb 5>; [54.00%]
  else
    goto <bb 4>; [46.00%]

  <bb 4> [24.84%]:

  <bb 5> [100.00%]:
  # val_6 = PHI <val_5(2), val_5(4), -2147483647(3)>
  _1 = alloc (val_6);
  sink (_1);
  return;

}



;; Function foo (foo, funcdef_no=1, decl_uid=2529, cgraph_uid=1, symbol_order=1)

;; 1 loops found
;;
;; Loop 0
;;  header 0, latch 1
;;  depth 0, outer -1
;;  nodes: 0 1 2 3 4
;; 2 succs { 3 4 }
;; 3 succs { 4 }
;; 4 succs { 1 }

Value ranges after VRP:

_1: VARYING
val_5: VARYING
val_6: ~[-2147483646, 1235]
_8: [0, +INF]
_9: [0, +INF]
_10: [0, +INF]


foo (int n)
{
  int val;
  void * _1;
  unsigned int _8;
  unsigned int _9;
  _Bool _10;

  <bb 2> [100.00%]:
  val_5 = value ();
  _8 = (unsigned int) val_5;
  _9 = _8 + 2147483646;
  _10 = _9 <= 2147484881;
  if (_10 != 0)
    goto <bb 3>; [54.00%]
  else
    goto <bb 4>; [46.00%]

  <bb 3> [29.16%]:

  <bb 4> [100.00%]:
  # val_6 = PHI <-2147483647(3), val_5(2)>
  _1 = alloc (val_6);
  sink (_1);
  return;

}


t.c: In function ‘foo’:
t.c:18:3: warning: argument 1 range [1236, 2147483647] exceeds maximum object size 1234 [-Walloc-size-larger-than=]
   sink (alloc (anti_range (INT_MIN + 2, 1235)));
   ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
t.c:5:7: note: in a call to allocation function ‘alloc’ declared here
 void* alloc (int) __attribute__ ((alloc_size (1)));
       ^~~~~

;; Function bar (bar, funcdef_no=2, decl_uid=2532, cgraph_uid=2, symbol_order=2)

;; 1 loops found
;;
;; Loop 0
;;  header 0, latch 1
;;  depth 0, outer -1
;;  nodes: 0 1 2 3 4
;; 2 succs { 3 4 }
;; 3 succs { 4 }
;; 4 succs { 1 }

SSA replacement table
N_i -> { O_1 ... O_j } means that N_i replaces O_1, ..., O_j

val_8 -> { val_5 }
val_9 -> { val_5 }
Incremental SSA update started at block: 2
Number of blocks in CFG: 6
Number of blocks to update: 4 ( 67%)



Value ranges after VRP:

_1: VARYING
val_5: VARYING
val_6: [-INF, -1]  EQUIVALENCES: { } (0 elements)
val_8: [0, +INF]  EQUIVALENCES: { val_5 } (1 elements)
val_9: [-INF, -1]  EQUIVALENCES: { val_5 } (1 elements)


Removing basic block 3
bar (int n)
{
  int val;
  void * _1;

  <bb 2> [100.00%]:
  val_5 = value ();
  if (val_5 >= 0)
    goto <bb 4>; [67.61%]
  else
    goto <bb 3>; [32.39%]

  <bb 3> [32.39%]:

  <bb 4> [100.00%]:
  # val_6 = PHI <val_5(3), -1(2)>
  _1 = alloc (val_6);
  sink (_1);
  return;

}



;; Function bar (bar, funcdef_no=2, decl_uid=2532, cgraph_uid=2, symbol_order=2)

;; 1 loops found
;;
;; Loop 0
;;  header 0, latch 1
;;  depth 0, outer -1
;;  nodes: 0 1 2
;; 2 succs { 1 }

Value ranges after VRP:

_1: VARYING
val_5: VARYING
val_8: [-INF, -1]


bar (int n)
{
  int val;
  void * _1;

  <bb 2> [100.00%]:
  val_5 = value ();
  val_8 = MIN_EXPR <val_5, -1>;
  _1 = alloc (val_8);
  sink (_1);
  return;

}


t.c: In function ‘bar’:
t.c:23:3: warning: argument 1 range [-2147483648, -1] is negative [-Walloc-size-larger-than=]
   sink (alloc (anti_range (0, INT_MAX)));
   ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
t.c:5:7: note: in a call to allocation function ‘alloc’ declared here
 void* alloc (int) __attribute__ ((alloc_size (1)));
       ^~~~~

;; Function foobar (foobar, funcdef_no=3, decl_uid=2535, cgraph_uid=3, symbol_order=3)

;; 1 loops found
;;
;; Loop 0
;;  header 0, latch 1
;;  depth 0, outer -1
;;  nodes: 0 1 2 3 4 5 6 7
;; 2 succs { 3 5 }
;; 3 succs { 4 5 }
;; 4 succs { 5 }
;; 5 succs { 6 7 }
;; 6 succs { 7 }
;; 7 succs { 1 }

SSA replacement table
N_i -> { O_1 ... O_j } means that N_i replaces O_1, ..., O_j

val_14 -> { val_8 }
val_15 -> { val_8 }
val_16 -> { val_10 }
val_17 -> { val_10 }
val_18 -> { val_10 }
val_19 -> { val_10 }
Incremental SSA update started at block: 2
Number of blocks in CFG: 11
Number of blocks to update: 9 ( 82%)



Value ranges after VRP:

_1: VARYING
_2: VARYING
val_8: VARYING
val_9: [-INF, -1]  EQUIVALENCES: { } (0 elements)
val_10: VARYING
val_11: ~[-2147483646, 1235]  EQUIVALENCES: { } (0 elements)
val_14: [0, +INF]  EQUIVALENCES: { val_8 } (1 elements)
val_15: [-INF, -1]  EQUIVALENCES: { val_8 } (1 elements)
val_16: [-2147483646, 1235]  EQUIVALENCES: { val_10 val_18 } (2 elements)
val_17: [1236, +INF]  EQUIVALENCES: { val_10 val_18 } (2 elements)
val_18: [-2147483646, +INF]  EQUIVALENCES: { val_10 } (1 elements)
val_19: [-INF, -2147483647]  EQUIVALENCES: { val_10 } (1 elements)


Removing basic block 4
Removing basic block 6
Removing basic block 8
foobar (int n)
{
  int val;
  int val;
  void * _1;
  void * _2;

  <bb 2> [100.00%]:
  val_10 = value ();
  if (val_10 >= -2147483646)
    goto <bb 3>; [50.00%]
  else
    goto <bb 5>; [50.00%]

  <bb 3> [50.00%]:
  if (val_10 <= 1235)
    goto <bb 5>; [50.00%]
  else
    goto <bb 4>; [50.00%]

  <bb 4> [25.00%]:

  <bb 5> [100.00%]:
  # val_11 = PHI <val_10(2), val_10(4), -2147483647(3)>
  _1 = alloc (val_11);
  sink (_1);
  val_8 = value ();
  if (val_8 >= 0)
    goto <bb 7>; [67.61%]
  else
    goto <bb 6>; [32.39%]

  <bb 6> [32.39%]:

  <bb 7> [100.00%]:
  # val_9 = PHI <val_8(6), -1(5)>
  _2 = alloc (val_9);
  sink (_2);
  return;

}



;; Function foobar (foobar, funcdef_no=3, decl_uid=2535, cgraph_uid=3, symbol_order=3)

;; 1 loops found
;;
;; Loop 0
;;  header 0, latch 1
;;  depth 0, outer -1
;;  nodes: 0 1 2 3 4
;; 2 succs { 3 4 }
;; 3 succs { 4 }
;; 4 succs { 1 }

Value ranges after VRP:

_1: VARYING
_2: VARYING
val_8: VARYING
_9: [0, +INF]
val_10: VARYING
val_11: VARYING
val_14: [-INF, -1]
_15: [0, +INF]
_16: [0, +INF]


foobar (int n)
{
  int val;
  int val;
  void * _1;
  void * _2;
  unsigned int _9;
  unsigned int _15;
  _Bool _16;

  <bb 2> [100.00%]:
  val_10 = value ();
  _9 = (unsigned int) val_10;
  _15 = _9 + 2147483646;
  _16 = _15 <= 2147484881;
  if (_16 != 0)
    goto <bb 3>; [50.00%]
  else
    goto <bb 4>; [50.00%]

  <bb 3> [25.00%]:

  <bb 4> [100.00%]:
  # val_11 = PHI <-2147483647(3), val_10(2)>
  _1 = alloc (val_11);
  sink (_1);
  val_8 = value ();
  val_14 = MIN_EXPR <val_8, -1>;
  _2 = alloc (val_14);
  sink (_2);
  return;

}


t.c: In function ‘foobar’:
t.c:29:3: warning: argument 1 range [-2147483648, -1] is negative [-Walloc-size-larger-than=]
   sink (alloc (anti_range (0, INT_MAX)));
   ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
t.c:5:7: note: in a call to allocation function ‘alloc’ declared here
 void* alloc (int) __attribute__ ((alloc_size (1)));
       ^~~~~


---


### compiler : `gcc`
### title : `Information from CCmode is not propagated across basic blocks`
### open_at : `2017-01-11T13:07:38Z`
### last_modified_date : `2021-10-09T09:02:04Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=79059
### status : `UNCONFIRMED`
### tags : `internal-improvement, missed-optimization`
### component : `rtl-optimization`
### version : `unknown`
### severity : `enhancement`
### contents :
This bug report is motivated by a performance regression [1] in 429.mcf on AArch64, but is relevant to all targets that use CCmode and rely on combine optimization.  Below description assumes AArch64 ISA.

Sample code:
===========
<BB1>:
...
add w1, w1, w2
cmp w1, #0
b.nz BB1

<BB2>:
ccmp ..., eq	// Some instruction that needs only NZ bits of CC register
cmp w2, w3	// Set CC to something new
b.eq BB1
===========

The high-level issue is that "add" and "cmp" instructions can't be combined into "adds" in BB1 because reg liveness info at the top of BB2 advertises that it needs "CC" register [1].  While BB2 really needs only part of CC register valid (NZ flags), liveness info cannot relate that.  Therefore liveness info marks all of CC as used thus preventing combining optimization.

I've considered several ways to improve on the situation, but none of them seem particularly appealing.  I would appreciate improvements and suggestions on these or other approaches.

#1 Make register liveness info include mode information.

The current state can be viewed as all registers listing their widest mode.  We can [incrementally] set more precise modes on registers (e.g., CC_REGNUM) when cases like the above present themselves.  This would be a substantial overall project, with several milestones each of which is worthy in itself.  I.e.,
phase_1: add mode field, set it conservatively, and verify it is propagated correctly through dataflow;
phase_2: improve handling of CC modes for the above motivating example;
phase_3: improve handling of modes for non-CC registers when examples present themselves.

The main advantage of this approach is that it will benefit many architectures and will improve liveness information for all registers, not just CC_REGNUM.  The main disadvantage -- it is a big project.

#2 Split CC_REGNUM into separate registers: CC_NZ_REGNUM, CC_CV_REGNUM.

This would require substantial rework of aarch64 backend.  All patterns needs to audited, some patterns will need to be duplicated.  It might be possible to reduce pattern duplication by inventing additional iterators in MD files, or otherwise automating conversion.

This work needs to be done entirely in aarch64 backend, which, IMO, is bad since other targets do not benefit.

#3 <Something else>

Suggestions and comments are welcome.

[1] The regression occurred after a legitimate patch (IIRC, rev. 232442 by Kyrill Tkachov) made GCC generate "ccmp" instruction in BB2 instead of starting BB2 with "cmp w1, #0".

[2] "adds" instruction sets NZ flags just like "cmp" instruction would, but CV flags are set differently.  Therefore "cmp" can be substituted with "adds" only when CV flags are unused.


---


### compiler : `gcc`
### title : `gcc fails to auto-vectorise the multiplicative reduction of an array of complex floats`
### open_at : `2017-01-16T14:10:44Z`
### last_modified_date : `2023-07-27T13:48:53Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=79102
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `7.0`
### severity : `normal`
### contents :
Consider this simple piece of code.

#include <complex.h>
complex float f(complex float x[]) {
  complex float p = 1.0;
  for (int i = 0; i < 128; i++)
    p *= x[i];
  return p;
}

If I compile it with -O3 -march=bdver2 -ffast-math  I get

f:
        vmovss  xmm2, DWORD PTR .LC1[rip]
        vxorps  xmm1, xmm1, xmm1
        lea     rax, [rdi+256]
.L2:
        vmovss  xmm0, DWORD PTR [rdi+4]
        add     rdi, 8
        vmulss  xmm3, xmm0, xmm2
        vmulss  xmm0, xmm0, xmm1
        vfmadd132ss     xmm1, xmm3, DWORD PTR [rdi-8]
        vfmsub132ss     xmm2, xmm0, DWORD PTR [rdi-8]
        cmp     rax, rdi
        jne     .L2
        vmovss  DWORD PTR [rsp-8], xmm2
        vmovss  DWORD PTR [rsp-4], xmm1
        vmovq   xmm0, QWORD PTR [rsp-8]
        ret
.LC1:
        .long   1065353216


This is unvectorised code. However if I do the same using float instead, that is with:

float f(float x[], int n ) {
  float p = 1.0;
  for (int i = 0; i < 32; i++)
    p *= x[i];
  return p;
}

I get

        vmovups xmm2, XMMWORD PTR [rdi]
        vmulps  xmm0, xmm2, XMMWORD PTR [rdi+16]
        vmulps  xmm0, xmm0, XMMWORD PTR [rdi+32]
        vmulps  xmm0, xmm0, XMMWORD PTR [rdi+48]
        vmulps  xmm0, xmm0, XMMWORD PTR [rdi+64]
        vmulps  xmm0, xmm0, XMMWORD PTR [rdi+80]
        vmulps  xmm0, xmm0, XMMWORD PTR [rdi+96]
        vmulps  xmm0, xmm0, XMMWORD PTR [rdi+112]
        vpsrldq xmm1, xmm0, 8
        vmulps  xmm0, xmm0, xmm1
        vpsrldq xmm1, xmm0, 4
        vmulps  xmm0, xmm0, xmm1
        ret

This is vectorised.

As a test I also the Intel C compiler version 17. In this case the assembly you get using complex float is however vectorised giving:

f:
        mov       rdx, rdi                                      #4.3
        and       rdx, 15                                       #4.3
        movsd     xmm0, QWORD PTR p.152.0.0.1[rip]              #3.19
        test      dl, dl                                        #4.3
        je        ..B1.4        # Prob 50%                      #4.3
        test      dl, 7                                         #4.3
        jne       ..B1.12       # Prob 10%                      #4.3
        movsd     xmm0, QWORD PTR [rdi]                         #5.10
        mov       dl, 1                                         #4.3
..B1.4:                         # Preds ..B1.3 ..B1.1
        movzx     eax, dl                                       #4.3
        neg       dl                                            #4.3
        and       dl, 3                                         #4.3
        movzx     edx, dl                                       #4.3
        movss     xmm1, DWORD PTR .L_2il0floatpacket.0[rip]     #3.19
        neg       rdx                                           #4.3
        movlhps   xmm0, xmm1                                    #3.19
        add       rdx, 128                                      #4.3
..B1.5:                         # Preds ..B1.5 ..B1.4
        movaps    xmm2, xmm0                                    #5.5
        movups    xmm1, XMMWORD PTR [rdi+rax*8]                 #5.10
        shufps    xmm2, xmm0, 160                               #5.5
        mulps     xmm2, xmm1                                    #5.5
        xorps     xmm1, XMMWORD PTR .L_2il0floatpacket.1[rip]   #5.5
        shufps    xmm1, xmm1, 177                               #5.5
        shufps    xmm0, xmm0, 245                               #5.5
        mulps     xmm1, xmm0                                    #5.5
        movups    xmm3, XMMWORD PTR [16+rdi+rax*8]              #5.10
        add       rax, 4                                        #4.3
        addps     xmm2, xmm1                                    #5.5
        movaps    xmm0, xmm2                                    #5.5
        shufps    xmm0, xmm2, 160                               #5.5
        mulps     xmm0, xmm3                                    #5.5
        xorps     xmm3, XMMWORD PTR .L_2il0floatpacket.1[rip]   #5.5
        shufps    xmm3, xmm3, 177                               #5.5
        shufps    xmm2, xmm2, 245                               #5.5
        mulps     xmm3, xmm2                                    #5.5
        addps     xmm0, xmm3                                    #5.5
        cmp       rax, rdx                                      #4.3
        jb        ..B1.5        # Prob 99%                      #4.3
        movaps    xmm1, xmm0                                    #3.19
        movhlps   xmm1, xmm0                                    #3.19
        movaps    xmm2, xmm1                                    #3.19
        shufps    xmm2, xmm1, 160                               #3.19
        mulps     xmm2, xmm0                                    #3.19
        xorps     xmm0, XMMWORD PTR .L_2il0floatpacket.1[rip]   #3.19
        shufps    xmm0, xmm0, 177                               #3.19
        shufps    xmm1, xmm1, 245                               #3.19
        mulps     xmm0, xmm1                                    #3.19
        addps     xmm0, xmm2                                    #3.19
..B1.7:                         # Preds ..B1.6 ..B1.12
        cmp       rdx, 128                                      #4.3
        jae       ..B1.11       # Prob 0%                       #4.3
..B1.9:                         # Preds ..B1.7 ..B1.9
        movsd     xmm1, QWORD PTR [rdi+rdx*8]                   #5.10
        inc       rdx                                           #4.3
        movaps    xmm2, xmm1                                    #5.5
        shufps    xmm2, xmm1, 160                               #5.5
        mulps     xmm2, xmm0                                    #5.5
        xorps     xmm0, XMMWORD PTR .L_2il0floatpacket.1[rip]   #5.5
        shufps    xmm0, xmm0, 177                               #5.5
        shufps    xmm1, xmm1, 245                               #5.5
        mulps     xmm0, xmm1                                    #5.5
        addps     xmm0, xmm2                                    #5.5
        cmp       rdx, 128                                      #4.3
        jb        ..B1.9        # Prob 99%                      #4.3
..B1.11:                        # Preds ..B1.9 ..B1.7
        ret                                                     #6.10
..B1.12:                        # Preds ..B1.2
        xor       edx, edx                                      #4.3
        jmp       ..B1.7        # Prob 100%                     #4.3
p.152.0.0.1:
        .long   0x3f800000,0x00000000
.L_2il0floatpacket.1:
        .long   0x00000000,0x80000000,0x00000000,0x80000000
.L_2il0floatpacket.0:
        .long   0x3f800000


---


### compiler : `gcc`
### title : `absolute value of a pointer difference can be assumed to be less than or equal to PTRDIFF_MAX`
### open_at : `2017-01-17T18:53:00Z`
### last_modified_date : `2023-05-06T20:20:35Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=79119
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `7.0`
### severity : `enhancement`
### contents :
C and C++ guarantee that the difference between two pointers into the same array must be representable in ptrdiff_t.  In addition, the absolute value of the difference must be less than or equal to PTRDIFF_MAX / sizeof (T) where T is the type of the array element.  The test case below shows that GCC doesn't make use of the guarantee.  If it did, it should be able to determine that the condition guarding the abort() statement in each of the functions below can never evaluate to true.

$ cat t.c && gcc -O2 -S -fdump-tree-optimized=/dev/stdout t.c
void f (int *a, __SIZE_TYPE__ i, __SIZE_TYPE__ j)
{
  int *p = a + i;
  int *q = a + j;

  __SIZE_TYPE__ n = p < q ? q - p : p - q;

  if (n > __PTRDIFF_MAX__ / sizeof (int))
    __builtin_abort ();
}

void g (int *a, __SIZE_TYPE__ i, __SIZE_TYPE__ j)
{
  int *p = a + i;
  int *q = a + j;

  __SIZE_TYPE__ n = p < q ? q - p : p - q;

  if (n > __PTRDIFF_MAX__)
    __builtin_abort ();
}


;; Function f (f, funcdef_no=0, decl_uid=1445, cgraph_uid=0, symbol_order=0)

f (int * a, long unsigned int i, long unsigned int j)
{
  int * q;
  int * p;
  long unsigned int _1;
  long unsigned int _2;
  long int _3;
  long int _4;
  long int _5;
  long int _6;
  long unsigned int iftmp.0_7;
  long unsigned int iftmp.0_13;
  long unsigned int iftmp.0_14;
  long int _21;
  long int _22;

  <bb 2> [100.00%]:
  _1 = i_8(D) * 4;
  p_10 = a_9(D) + _1;
  _2 = j_11(D) * 4;
  q_12 = a_9(D) + _2;
  _21 = (long int) _1;
  _22 = (long int) _2;
  if (p_10 < q_12)
    goto <bb 3>; [50.00%]
  else
    goto <bb 4>; [50.00%]

  <bb 3> [50.00%]:
  _3 = _22 - _21;
  _4 = _3 /[ex] 4;
  iftmp.0_14 = (long unsigned int) _4;
  goto <bb 5>; [100.00%]

  <bb 4> [50.00%]:
  _5 = _21 - _22;
  _6 = _5 /[ex] 4;
  iftmp.0_13 = (long unsigned int) _6;

  <bb 5> [100.00%]:
  # iftmp.0_7 = PHI <iftmp.0_14(3), iftmp.0_13(4)>
  if (iftmp.0_7 > 536870911)
    goto <bb 6>; [0.04%]
  else
    goto <bb 7>; [99.96%]

  <bb 6> [0.04%]:
  __builtin_abort ();

  <bb 7> [99.96%]:
  return;

}



;; Function g (g, funcdef_no=1, decl_uid=1453, cgraph_uid=1, symbol_order=1)

g (int * a, long unsigned int i, long unsigned int j)
{
  int * q;
  int * p;
  long unsigned int _1;
  long unsigned int _2;
  long int _3;
  long int _4;
  long int _5;
  long int _6;
  signed int n.10_7;
  long unsigned int iftmp.5_8;
  long unsigned int iftmp.5_14;
  long unsigned int iftmp.5_15;
  long int _22;
  long int _23;

  <bb 2> [100.00%]:
  _1 = i_9(D) * 4;
  p_11 = a_10(D) + _1;
  _2 = j_12(D) * 4;
  q_13 = a_10(D) + _2;
  _22 = (long int) _1;
  _23 = (long int) _2;
  if (p_11 < q_13)
    goto <bb 3>; [50.00%]
  else
    goto <bb 4>; [50.00%]

  <bb 3> [50.00%]:
  _3 = _23 - _22;
  _4 = _3 /[ex] 4;
  iftmp.5_15 = (long unsigned int) _4;
  goto <bb 5>; [100.00%]

  <bb 4> [50.00%]:
  _5 = _22 - _23;
  _6 = _5 /[ex] 4;
  iftmp.5_14 = (long unsigned int) _6;

  <bb 5> [100.00%]:
  # iftmp.5_8 = PHI <iftmp.5_15(3), iftmp.5_14(4)>
  n.10_7 = (signed int) iftmp.5_8;
  if (n.10_7 < 0)
    goto <bb 6>; [0.04%]
  else
    goto <bb 7>; [99.96%]

  <bb 6> [0.04%]:
  __builtin_abort ();

  <bb 7> [99.96%]:
  return;

}


---


### compiler : `gcc`
### title : `stack addresses are spilled to stack slots on x86-64 at -Os instead of rematerializing the addresses`
### open_at : `2017-01-19T15:24:36Z`
### last_modified_date : `2023-05-16T23:04:07Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=79148
### status : `WAITING`
### tags : `missed-optimization, ra`
### component : `rtl-optimization`
### version : `6.3.0`
### severity : `normal`
### contents :
Noticed this while browsing around Firefox source code compiled with GCC 5.4; a colleague confirms that this happens with 6.3 as well.  Compiling:

https://people.mozilla.org/~nfroyd/Unified_cpp_widget0.ii.gz

(Tried to get it under the attachment limit with xz, didn't happen)

with options:

-mtune=generic -march=x86-64 -g -Os -std=gnu++11 -fPIC -fno-strict-aliasing -fno-rtti -ffunction-sections -fdata-sections -fno-exceptions -fno-math-errno -freorder-blocks -fno-omit-frame-pointer -fstack-protector-strong

gives, for the function _ZN7mozilla6widget11GfxInfoBase20GetFeatureStatusImplEiPiR18nsAString_internalRK8nsTArrayINS0_13GfxDriverInfoEER19nsACString_internalPNS0_15OperatingSystemE a bit of code that looks like:

.LVL3402:
	leaq	-784(%rbp), %rax      [1a]
.LVL3403:
	movq	%rax, %rdi
.LVL3404:
	movq	%rax, -816(%rbp)      [1b]
	call	_ZN12nsAutoStringC1Ev
.LVL3405:
	.loc 14 887 0
	leaq	-624(%rbp), %rax      [2a]
	movq	%rax, %rdi
	movq	%rax, -824(%rbp)      [2b]
	call	_ZN12nsAutoStringC1Ev
.LVL3406:
	.loc 14 888 0
	leaq	-464(%rbp), %rax      [3a]
	movq	%rax, %rdi
	movq	%rax, -800(%rbp)      [3b]
	call	_ZN12nsAutoStringC1Ev
.LVL3407:
	.loc 14 889 0
	movq	(%r12), %rax
	movq	-816(%rbp), %rsi      [1c]
	movq	%r12, %rdi
	call	*104(%rax)
.LVL3408:
	.loc 14 890 0
	testl	%eax, %eax
	js	.L2479
	movq	(%r12), %rax
	movq	-824(%rbp), %rsi      [2c]
	movq	%r12, %rdi
	call	*120(%rax)
.LVL3409:
	.loc 14 889 0
	testl	%eax, %eax
	js	.L2479
	.loc 14 891 0
	movq	(%r12), %rax
	movq	-800(%rbp), %rsi      [3c]
	movq	%r12, %rdi
	call	*168(%rax)

The problem here, for each of the trio of instructions marked [1], [2], and [3], is that the instructions [1b], [2b], and [3b] that store the stack addresses are really unnecessary; replacing [1c], [2c], and [3c] with the `lea` instructions from [1a], [2a], and [3a] is the same size and doesn't require the stack slot storage, so we could eliminate those instructions ([1b], [2b], and [3b]) and (possibly) make the stack frame smaller as well.

I think rematerializing the stack addresses on x86/x86-64 ought always to be a win in terms of size (I don't know whether you'd want to make the same choices when compiling for speed); I think it'd be a similar win for RISC-y chips, at least so long as the stack frame sizes are reasonably small.


---


### compiler : `gcc`
### title : `bad optimization on MIPS and ARM leading to excessive stack usage in some cases`
### open_at : `2017-01-19T15:38:07Z`
### last_modified_date : `2022-01-20T11:32:00Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=79149
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `7.0`
### severity : `normal`
### contents :
Created attachment 40546
compressed preprocessed source for wp512 crypto from linux kernel

Build-testing the Linux kernel on MIPS shows warnings about possible kernel stack overflow in the kernel's crypto libraries, in particular the wp512 algorithm, as the stack frame grows beyond the normal per-function limit of 1024 bytes we use in the kernel.

I have been able to avoid the problem by turning off two specific optimizations,
and I have reproduced the same thing with both gcc-4.9 and gcc-7.0:

$ /home/arnd/cross-gcc/bin/mips-linux-gcc-7.0.0 -fno-strict-aliasing -O2 -c -Wall -Wframe-larger-than=100 -Wno-pointer-sign  wp512.i  
../../crypto/wp512.c: In function 'wp512_process_buffer':
../../crypto/wp512.c:987:1: warning: the frame size of 1128 bytes is larger than 100 bytes [-Wframe-larger-than=]

$ /home/arnd/cross-gcc/bin/mips-linux-gcc-7.0.0 -fno-strict-aliasing -O2 -c -Wall -Wframe-larger-than=100 -Wno-pointer-sign  wp512.i  -fno-sched-critical-path-heuristic -fno-sched-dep-count-heuristic
../../crypto/wp512.c: In function 'wp512_process_buffer':
../../crypto/wp512.c:987:1: warning: the frame size of 304 bytes is larger than 100 bytes [-Wframe-larger-than=]

$ /home/arnd/cross-gcc/bin/mips-linux-gcc-4.9.3 -fno-strict-aliasing -O2 -c -Wall -Wframe-larger-than=100 -Wno-pointer-sign  wp512.i  
../../crypto/wp512.c: In function 'wp512_process_buffer':
../../crypto/wp512.c:987:1: warning: the frame size of 1096 bytes is larger than 100 bytes [-Wframe-larger-than=]

$ /home/arnd/cross-gcc/bin/mips-linux-gcc-4.9.3 -fno-strict-aliasing -O2 -c -Wall -Wframe-larger-than=100 -Wno-pointer-sign  wp512.i  -fno-sched-critical-path-heuristic -fno-sched-dep-count-heuristic 
../../crypto/wp512.c: In function 'wp512_process_buffer':
../../crypto/wp512.c:987:1: warning: the frame size of 272 bytes is larger than 100 bytes [-Wframe-larger-than=]

To cross-check the problem, I have tried compiling the same file on ARM, which shows similar results but stays below the warning limit:

/home/arnd/cross-gcc/bin/arm-linux-gnueabi-gcc-7.0.0 -fno-strict-aliasing -O2 -c -Wall -Wframe-larger-than=100 -Wno-pointer-sign  wp512.i  
../../crypto/wp512.c: In function 'wp512_process_buffer':
../../crypto/wp512.c:987:1: warning: the frame size of 816 bytes is larger than 100 bytes [-Wframe-larger-than=]

$ /home/arnd/cross-gcc/bin/arm-linux-gnueabi-gcc-7.0.0 -fno-strict-aliasing -O2 -c -Wall -Wframe-larger-than=100 -Wno-pointer-sign  wp512.i  -fno-sched-critical-path-heuristic -fno-sched-dep-count-heuristic
../../crypto/wp512.c: In function 'wp512_process_buffer':
../../crypto/wp512.c:987:1: warning: the frame size of 344 bytes is larger than 100 bytes [-Wframe-larger-than=]

$ /home/arnd/cross-gcc/bin/arm-linux-gnueabi-gcc-4.9.3 -fno-strict-aliasing -O2 -c -Wall -Wframe-larger-than=100 -Wno-pointer-sign  wp512.i  
../../crypto/wp512.c: In function 'wp512_process_buffer':
../../crypto/wp512.c:987:1: warning: the frame size of 840 bytes is larger than 100 bytes [-Wframe-larger-than=]

$ /home/arnd/cross-gcc/bin/arm-linux-gnueabi-gcc-4.9.3 -fno-strict-aliasing -O2 -c -Wall -Wframe-larger-than=100 -Wno-pointer-sign  wp512.i   -fno-sched-critical-path-heuristic -fno-sched-dep-count-heuristic
../../crypto/wp512.c: In function 'wp512_process_buffer':
../../crypto/wp512.c:987:1: warning: the frame size of 376 bytes is larger than 100 bytes [-Wframe-larger-than=]

However, using an x86 compiler, the frame for the same source is always under 300 bytes, and the options have no effect.


---


### compiler : `gcc`
### title : `Missed BB vectorization with strided/scalar stores`
### open_at : `2017-01-19T18:16:11Z`
### last_modified_date : `2021-08-15T23:31:32Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=79151
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `7.0`
### severity : `enhancement`
### contents :
Consider the following code. The function "scalar" contains two formulas in a
function which are identical, except for the coefficients which
differ.

This could be vectorized.  As an example of how this could be done,
see the function "vector" where vectorization intrinsics are used.

You will see that "vector" is much shorter; all the operations are
done using vector intrinsics.

This is for x86_64-pc-linux-gnu.

#include <stdio.h>
 
void scalar(const double *restrict a, const double *restrict b,
        double x, double *ar, double *br)
{
  double ra, rb;
  int i;
 
  ra = a[0] + a[1]/x - 1.0/(a[0]-a[1]);
  rb = b[0] + b[1]/x - 1.0/(b[0]-b[1]);
 
  *ar = ra;
  *br = rb;
}
 
void vector(const double *restrict a, const double *restrict b,
        double x, double *ar, double *br)
{
  typedef double v2do __attribute__((vector_size (16)));
  v2do c0, c1, r;
 
  c0[0] = a[0];
  c0[1] = b[0];
  c1[0] = a[1];
  c1[1] = b[1];
 
  r = c0 + c1/x - 1.0/(c0-c1);
  *ar = r[0];
  *br = r[1];
}
 
double a[] = {1.0, -1.5};
double b[] = {1.3, -1.2};
 
int main()
{
  double x = 1.24;
  double ar, br;
 
  scalar(a, b, x, &ar, &br);
  printf("%f %f\n", ar, br);
  vector(a, b, x, &ar, &br);
  printf("%f %f\n", ar, br);
 
  return 0;
}

Assembly for the function "scalar":

scalar:
.LFB11:
        .cfi_startproc
        movsd   8(%rdi), %xmm4
        movsd   8(%rsi), %xmm5
        movapd  %xmm4, %xmm1
        movsd   (%rdi), %xmm2
        movapd  %xmm5, %xmm7
        divsd   %xmm0, %xmm1
        divsd   %xmm0, %xmm7
        addsd   %xmm2, %xmm1
        subsd   %xmm4, %xmm2
        movapd  %xmm2, %xmm4
        movsd   (%rsi), %xmm3
        movsd   .LC0(%rip), %xmm2
        movapd  %xmm7, %xmm0
        movapd  %xmm2, %xmm6
        addsd   %xmm3, %xmm0
        subsd   %xmm5, %xmm3
        divsd   %xmm4, %xmm6
        divsd   %xmm3, %xmm2
        subsd   %xmm6, %xmm1
        movsd   %xmm1, (%rdx)
        subsd   %xmm2, %xmm0
        movsd   %xmm0, (%rcx)
        ret

Assembly for the function "vector":

vector:
.LFB12:
        .cfi_startproc
        movsd   8(%rsi), %xmm2
        movsd   8(%rdi), %xmm3
        unpcklpd        %xmm0, %xmm0
        unpcklpd        %xmm2, %xmm3
        movapd  .LC1(%rip), %xmm2
        movsd   (%rdi), %xmm1
        movapd  %xmm3, %xmm4
        movhpd  (%rsi), %xmm1
        divpd   %xmm0, %xmm4
        movapd  %xmm4, %xmm0
        addpd   %xmm1, %xmm0
        subpd   %xmm3, %xmm1
        divpd   %xmm1, %xmm2
        addpd   %xmm2, %xmm0
        movlpd  %xmm0, (%rdx)
        movhpd  %xmm0, (%rcx)
        ret


---


### compiler : `gcc`
### title : `possibly lost DCE / invariant motion optimization`
### open_at : `2017-01-20T11:17:01Z`
### last_modified_date : `2023-06-21T06:20:31Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=79161
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `6.3.0`
### severity : `normal`
### contents :
Created attachment 40553
a.c

Consider the following example (a.c in attach):

static void f(const char *s)
{
    for (; *s++ == '0'; );
}
int main(int argc, char **argv)
{
    const char *s0 = argv[1];
    for (int x = 0; x < 1000000000; ++x) f(s0);
    return 0;
}

Clang thinks this can be optimized to just 'return 0':

$ clang++-3.9 -c -O2 a.c -oa.o && objdump -d a.o
clang-3.9: warning: treating 'c' input as 'c++' when in C++ mode, this behavior is deprecated

a.o:     file format elf64-x86-64


Disassembly of section .text:

0000000000000000 <main>:
   0:   31 c0                   xor    %eax,%eax
   2:   c3                      retq

While GCC doesn't:

$ g++ -c -O2 a.c -oa.o && objdump -d a.o

a.o:     file format elf64-x86-64


Disassembly of section .text.startup:

0000000000000000 <main>:
   0:   48 8b 4e 08             mov    0x8(%rsi),%rcx
   4:   ba 00 ca 9a 3b          mov    $0x3b9aca00,%edx
   9:   0f 1f 80 00 00 00 00    nopl   0x0(%rax)
  10:   48 89 c8                mov    %rcx,%rax
  13:   0f 1f 44 00 00          nopl   0x0(%rax,%rax,1)
  18:   48 83 c0 01             add    $0x1,%rax
  1c:   80 78 ff 30             cmpb   $0x30,-0x1(%rax)
  20:   74 f6                   je     18 <main+0x18>
  22:   83 ea 01                sub    $0x1,%edx
  25:   75 e9                   jne    10 <main+0x10>
  27:   31 c0                   xor    %eax,%eax
  29:   c3                      retq

I'm not sure if optimization is rightful but it looks correct to me. I don't see any side effects in 'f' function.


---


### compiler : `gcc`
### title : `[ARM] Implement neon_valid_immediate tricks for BYTES_BIG_ENDIAN`
### open_at : `2017-01-20T14:39:21Z`
### last_modified_date : `2021-05-17T08:08:55Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=79166
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `7.0`
### severity : `enhancement`
### contents :
As a result of the fix for PR 71270 the various tricks that neon_valid_immediate can do to splat a constant across a vector have been restricted to all but the most basic ones on BYTES_BIG_ENDIAN.

This is a PR to track implementing them properly on big-endian targets.
See also https://gcc.gnu.org/ml/gcc-patches/2017-01/msg00381.html


---


### compiler : `gcc`
### title : `add-with-carry and subtract-with-borrow support (x86_64 and others)`
### open_at : `2017-01-21T00:51:53Z`
### last_modified_date : `2023-08-29T08:47:27Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=79173
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `7.0`
### severity : `enhancement`
### contents :
There should be a way to support full add-with-carry and subtract-with-borrow by generating adc / sbb instructions on x86_64 (and similar instructions on other targets).

GCC could add builtins, such as __builtin_addc* and __builtin_subc* (two arguments, carry in, carry out, and the result), similar to Clang:
http://clang.llvm.org/docs/LanguageExtensions.html#multiprecision-arithmetic-builtins
as suggested in PR 60206 comment 3.

Detection of special constructs in standard C/... code would be useful too. Here are some examples from https://gcc.gnu.org/ml/gcc-help/2017-01/msg00067.html for subtraction:

typedef unsigned long T;

void sub1 (T *p, T u0, T u1, T u2, T v0, T v1, T v2)
{
  T t1;
  int b0, b1;

  p[0] = u0 - v0;
  b0 = u0 < v0;
  t1 = u1 - v1;
  b1 = u1 < v1;
  p[1] = t1 - b0;
  b1 |= p[1] > t1;
  p[2] = u2 - v2 - b1;
}

void sub2 (T *p, T u0, T u1, T u2, T v0, T v1, T v2)
{
  int b0, b1;

  p[0] = u0 - v0;
  b0 = u0 < v0;
  p[1] = u1 - v1 - b0;
  b1 = u1 < v1 || (u1 == v1 && b0 != 0);
  p[2] = u2 - v2 - b1;
}

In the second example, the b1 line could also be replaced by:

  b1 = u1 < v1 + b0 || v1 + b0 < v1;

For the subtractions, optimal code would contain 1 sub and 2 sbb's.


---


### compiler : `gcc`
### title : `[8 Regression] register allocation in the addition of two 128/9 bit ints`
### open_at : `2017-01-22T17:30:41Z`
### last_modified_date : `2022-05-27T09:57:26Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=79185
### status : `RESOLVED`
### tags : `missed-optimization, ra`
### component : `target`
### version : `7.0`
### severity : `normal`
### contents :
Consider this code:

__int128_t ai (__int128_t x, __int128_t y) {
  return x + y;
}

In gcc 4.8.5, clang and icc using -O2 this gives code that is more or less exactly:

ai:
        mov     rax, rdx
        mov     rdx, rcx
        add     rax, rdi
        adc     rdx, rsi
        ret


However in gcc 4.9 and later you get

ai:
        mov     r9, rdi
        mov     r10, rsi
        add     r9, rdx
        adc     r10, rcx
        mov     rax, r9
        mov     rdx, r10
        ret

Interestingly, that is also the code you get in gcc 4.8.5 if you use -O instead of -O2.

Is this addition of two extra mov's a regression?


---


### compiler : `gcc`
### title : `Poor code generation when using stateless lambda instead of normal function`
### open_at : `2017-01-22T19:49:00Z`
### last_modified_date : `2021-07-23T23:40:19Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=79189
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `c++`
### version : `7.0`
### severity : `normal`
### contents :
When doing an indirect call (through a function pointer), GCC generates different code depending on whether the function pointer was obtained by converting a stateless lambda or a normal function. The code generated for a normal function is vastly superior, and in fact the call can sometimes be elided.

Code:

  #if 1
    template <typename T>
    static auto const increment = [](void* self) { ++*static_cast<T*>(self); };
  #else
    template <typename T>
    void increment(void* self) { ++*static_cast<T*>(self); }
  #endif

  struct VTable { void (*increment)(void*); };
  template <typename T> static VTable const vtable{increment<T>};

  struct any_iterator {
    template <typename Iterator>
    explicit any_iterator(Iterator it)
      : vptr_{&vtable<Iterator>}, self_{new Iterator(it)}
    { }
    VTable const* vptr_;
    void* self_;
  };

  int main() {
    int input[100] = {0};
    any_iterator first{&input[0]};
    first.vptr_->increment(first.self_);
  }


Codegen with the lambda:

  increment<int*>::{lambda(void*)#1}::_FUN(void*):
          add     QWORD PTR [rdi], 4
          ret
  main:
          sub     rsp, 408
          xor     eax, eax
          mov     ecx, 50
          mov     rdi, rsp
          rep stosq
          mov     edi, 8
          call    operator new(unsigned long)
          mov     QWORD PTR [rax], rsp
          mov     rdi, rax
          call    [QWORD PTR vtable<int*>[rip]]
          xor     eax, eax
          add     rsp, 408
          ret
  _GLOBAL__sub_I_main:
          mov     QWORD PTR vtable<int*>[rip], OFFSET FLAT:increment<int*>::{lambda(void*)#1}::_FUN(void*)
          ret


Codegen with the function:

  main:
          sub     rsp, 8
          mov     edi, 8
          call    operator new(unsigned long)
          xor     eax, eax
          add     rsp, 8
          ret


Note that Clang (trunk) makes a much better job at optimizing this. Also see [1] for this example on compiler explorer. See [2] for a larger example that exhibits the same behavior, and where this results in a ~10x speed difference because the call is done in a loop.

[1]: https://godbolt.org/g/HQb5Y5
[2]: http://melpon.org/wandbox/permlink/Gs3njR3STPLk2Ecr


---


### compiler : `gcc`
### title : `potentially truncating unsigned conversion defeats range propagation`
### open_at : `2017-01-23T00:42:28Z`
### last_modified_date : `2023-05-12T05:00:23Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=79191
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `7.0`
### severity : `normal`
### contents :
As mentioned in a recent discussion (https://gcc.gnu.org/ml/gcc-patches/2017-01/msg01617.html), a truncating unsigned conversion such as from unsigned long to unsigned in LP64 appears to defeat VRP and prevent GCC from emitting optimal code.

In the test case below, the indirect call to abort() in g() is optimized away because n is known to be less than 3.  However, the same indirect call to abort() is not optimized away in h().

$ cat t.c && gcc -O2 -S -Wall -fdump-tree-optimized=/dev/stdout t.c
void f (unsigned long n)
{
  if (n > 3)
    __builtin_abort ();
}

void g (unsigned n)
{
  if (n < 3)
    f (n);
}

void h (unsigned long m)
{
  unsigned n = m;

  if (n < 3)
    f (n);
}

;; Function f (f, funcdef_no=0, decl_uid=1795, cgraph_uid=0, symbol_order=0)

f (long unsigned int n)
{
  <bb 2> [100.00%]:
  if (n_1(D) > 3)
    goto <bb 3>; [0.04%]
  else
    goto <bb 4>; [99.96%]

  <bb 3> [0.04%]:
  __builtin_abort ();

  <bb 4> [99.96%]:
  return;

}



;; Function g (g, funcdef_no=1, decl_uid=1798, cgraph_uid=1, symbol_order=1)

g (unsigned int n)
{
  <bb 2> [100.00%]:
  return;

}



;; Function h (h, funcdef_no=2, decl_uid=1801, cgraph_uid=2, symbol_order=2)

Removing basic block 6
Removing basic block 7
h (long unsigned int m)
{
  unsigned int n;
  long unsigned int _5;

  <bb 2> [100.00%]:
  n_2 = (unsigned int) m_1(D);
  if (n_2 <= 2)
    goto <bb 3>; [54.00%]
  else
    goto <bb 5>; [46.00%]

  <bb 3> [54.00%]:
  _5 = m_1(D) & 4294967295;
  if (_5 > 3)
    goto <bb 4>; [0.04%]
  else
    goto <bb 5>; [99.96%]

  <bb 4> [0.02%]:
  __builtin_abort ();

  <bb 5> [99.98%]:
  return;

}


---


### compiler : `gcc`
### title : `missed optimization: sinking doesn't handle calls, swap PRE and sinking`
### open_at : `2017-01-23T17:27:51Z`
### last_modified_date : `2021-11-06T14:05:57Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=79201
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `7.0`
### severity : `enhancement`
### contents :
Consider this code:

int f(int n) {
  int i,j=0;
  for (i = 0; i < 32; i++) {
    j = __builtin_ffs(i);
  }
  return j;
}

With gcc -O3 you get

f:
        xor     eax, eax
        xor     edx, edx
        mov     ecx, -1
        jmp     .L3
.L5:
        bsf     eax, edx
        cmove   eax, ecx
        add     eax, 1
.L3:
        add     edx, 1
        cmp     edx, 32
        jne     .L5
        rep ret


However with clang you get

f:                                      # @f
        mov     eax, 1
        ret


A similar difference occurs if you replace the limit 32 with the variable n.

gcc is unable to detect that the loop can be omitted.


---


### compiler : `gcc`
### title : `Missed swap optimization on powerpc64le simple test case`
### open_at : `2017-01-24T21:08:09Z`
### last_modified_date : `2022-03-08T16:20:54Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=79218
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `target`
### version : `7.0`
### severity : `normal`
### contents :
The following test case has some unnecessary swaps:

bergner@genoa:~/gcc/BUGS$ cat ptr5.i 
void
ptr5 (__int128_t *dst, __int128_t *src)
{
  *dst = ~*src;
}
bergner@genoa:~/gcc/BUGS$ gcc7 -O2 -mcpu=power8 -S ptr5.i 
bergner@genoa:~/gcc/BUGS$ cat ptr5.s 
ptr5:
	lxvd2x 0,0,4
	xxpermdi 0,0,0,2
	xxlnor 0,0,0
	xxpermdi 0,0,0,2
	stxvd2x 0,0,3
	blr

This is still better than what GCC6 which produces:

bergner@genoa:~/gcc/BUGS$ gcc6 -O2 -mcpu=power8 -S ptr5.i 
bergner@genoa:~/gcc/BUGS$ cat ptr5.s 
ptr5:
	ld 10,0(4)
	ld 11,8(4)
	not 10,10
	not 11,11
	std 10,0(3)
	std 11,8(3)
	blr

I'll note that GCC7 using -mcpu=power9 does not have any swaps due to the new endian friendly dform load/stores:

bergner@genoa:~/gcc/BUGS$ gcc7 -O2 -mcpu=power9 -S ptr5.i 
bergner@genoa:~/gcc/BUGS$ cat ptr5.s 
ptr5:
	lxv 0,0(4)
	xxlnor 0,0,0
	stxv 0,0(3)
	blr


---


### compiler : `gcc`
### title : `[7 Regression] Large C-Ray slowdown`
### open_at : `2017-01-25T08:37:07Z`
### last_modified_date : `2021-11-16T13:04:01Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=79224
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `7.0`
### severity : `normal`
### contents :
http://gcc.opensuse.org/c++bench-czerny/c-ray/ shows regressions at revision ranges r239336-r239387 and r243991-r243996 (on x86_64, -O3 -ffast-math -funroll-loops -march=core-avx2)

And it was good again for a short time, improving between r244241:244289
and regressing again r244382:244454.  The former adjusts PRED_CALL the latter
has the partial DSE adjustments.

See also PR77468 where I split this out from or its dup, PR68664


---


### compiler : `gcc`
### title : `[8/9/10 Regression] load gap with store gap causing performance regression in 462.libquantum`
### open_at : `2017-01-28T08:33:09Z`
### last_modified_date : `2019-11-19T17:12:47Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=79262
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `7.0`
### severity : `normal`
### contents :
As reported at https://gcc.gnu.org/bugzilla/show_bug.cgi?id=18438#c9 but what is not mentioned is that this is a regression from GCC 5.  I noticed this again when I was working on improving ThunderX 2 CN99xx performance difference between -O2 and -Ofast and GCC 5.4.0 and the trunk.

Take:
struct node_struct
{
  float _Complex gap;
  unsigned long long state;
};

struct reg_struct
{
  int size;
  struct node_struct *node;
};

void
func(int target, struct reg_struct *reg)
{
  int i;

  for(i=0; i<reg->size; i++)
    reg->node[i].state ^= ((unsigned long long) 1 << target);
}
---- CUT ---
Currently this is vectorized on the trunk using load gaps but then the store is using scalars.  This is much slower and also it is only doing 2 at a time.  There are some cost model issues in the aarch64 backend dealing with scalar for int vs floating point too.  I might just go fix those first.


---


### compiler : `gcc`
### title : `FRE/PRE do not allow folding to look at SSA defs during elimination`
### open_at : `2017-02-02T08:51:45Z`
### last_modified_date : `2021-05-07T15:55:13Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=79333
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `7.0.1`
### severity : `enhancement`
### contents :
This for example shows as not folding memory builtins or not doing any complex
match.pd replacements for gcc.dg/tree-ssa/pr71078-3.c when match.h provides
for example

extern __inline __attribute__ ((__always_inline__)) __attribute__ ((__gnu_inline__)) double __attribute__ ((__nothrow__ , __leaf__)) fabs (double __x) { return __builtin_fabs (__x); }

as opposed to just a prototype.  This results in

  <bb 2> [100.00%]:
  _1 = (double) f_3(D);
  _8 = ABS_EXPR <_1>;
  _2 = (double) f_3(D);
  t2_5 = _2 / _8;
  return t2_5;

which is not matched by the x / abs(x) -> copysign (1.0, x) pattern.  You'd
expect FRE1 to do the CSE (it does) and elimination folding of the stmt
to turn op the __builtin_copysign but that doesn't happen because the fold_stmt
done by elimination doesn't allow SSA name following.


---


### compiler : `gcc`
### title : `Poor vectorisation of additive reduction of complex array, final SLP reduction step inefficient`
### open_at : `2017-02-02T10:44:18Z`
### last_modified_date : `2021-06-08T14:06:19Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=79336
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `7.0`
### severity : `normal`
### contents :
Consider this code:

#include <complex.h>
complex float f(complex float x[]) {
  complex float p = 1.0;
  for (int i = 0; i < 32; i++)
    p += x[i];
  return p;
}

gcc 7 with -march=core-avx2 -ffast-math gives

f:
        lea     r10, [rsp+8]
        and     rsp, -32
        push    QWORD PTR [r10-8]
        push    rbp
        mov     rbp, rsp
        push    r10
        vmovups ymm0, YMMWORD PTR [rdi+64]
        vmovaps ymm1, YMMWORD PTR .LC0[rip]
        vaddps  ymm0, ymm0, YMMWORD PTR [rdi+32]
        vaddps  ymm1, ymm1, YMMWORD PTR [rdi]
        vaddps  ymm0, ymm0, ymm1
        vmovups ymm1, YMMWORD PTR [rdi+128]
        vaddps  ymm1, ymm1, YMMWORD PTR [rdi+96]
        vaddps  ymm0, ymm0, ymm1
        vmovups ymm1, YMMWORD PTR [rdi+192]
        vaddps  ymm1, ymm1, YMMWORD PTR [rdi+160]
        vaddps  ymm0, ymm0, ymm1
        vaddps  ymm0, ymm0, YMMWORD PTR [rdi+224]
        vunpckhps       xmm3, xmm0, xmm0
        vshufps xmm2, xmm0, xmm0, 255
        vshufps xmm1, xmm0, xmm0, 85
        vaddss  xmm1, xmm2, xmm1
        vaddss  xmm3, xmm3, xmm0
        vextractf128    xmm0, ymm0, 0x1
        vunpckhps       xmm4, xmm0, xmm0
        vshufps xmm2, xmm0, xmm0, 85
        vaddss  xmm4, xmm4, xmm0
        vshufps xmm0, xmm0, xmm0, 255
        vaddss  xmm0, xmm2, xmm0
        vaddss  xmm3, xmm3, xmm4
        vaddss  xmm1, xmm1, xmm0
        vmovss  DWORD PTR [rbp-24], xmm3
        vmovss  DWORD PTR [rbp-20], xmm1
        vzeroupper
        vmovq   xmm0, QWORD PTR [rbp-24]
        pop     r10
        pop     rbp
        lea     rsp, [r10-8]
        ret

This is vectorised but appears to perform a number of unnecessary instructions.

By contrast, icc using the same options gives:


f:
        vmovups   ymm1, YMMWORD PTR [rdi]                       #5.10
        vmovups   ymm2, YMMWORD PTR [64+rdi]                    #5.10
        vmovups   ymm5, YMMWORD PTR [128+rdi]                   #5.10
        vmovups   ymm6, YMMWORD PTR [192+rdi]                   #5.10
        vmovsd    xmm0, QWORD PTR p.152.0.0.1[rip]              #3.19
        vaddps    ymm3, ymm1, YMMWORD PTR [32+rdi]              #3.19
        vaddps    ymm4, ymm2, YMMWORD PTR [96+rdi]              #3.19
        vaddps    ymm7, ymm5, YMMWORD PTR [160+rdi]             #3.19
        vaddps    ymm8, ymm6, YMMWORD PTR [224+rdi]             #3.19
        vaddps    ymm9, ymm3, ymm4                              #3.19
        vaddps    ymm10, ymm7, ymm8                             #3.19
        vaddps    ymm11, ymm9, ymm10                            #3.19
        vextractf128 xmm12, ymm11, 1                            #3.19
        vaddps    xmm13, xmm11, xmm12                           #3.19
        vmovhlps  xmm14, xmm13, xmm13                           #3.19
        vaddps    xmm15, xmm13, xmm14                           #3.19
        vaddps    xmm0, xmm15, xmm0                             #3.19
        vzeroupper                                              #6.10
        ret


---


### compiler : `gcc`
### title : `unused std::string is not optimized away in presense of a call`
### open_at : `2017-02-02T22:51:51Z`
### last_modified_date : `2022-03-18T08:06:37Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=79349
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `7.0`
### severity : `enhancement`
### contents :
g++ version (GCC) 7.0.0 20170118 (experimental)

$ cat t.cpp

#include<string>
void foo();

int main() {
  std::string s("abc");
  foo ();
  return 0;
}

$ install/bin/g++ -O3 t.cpp -S -o t.s
$ cat t.s

main:
.LFB995:
        .cfi_startproc
        .cfi_personality 0x3,__gxx_personality_v0
        .cfi_lsda 0x3,.LLSDA995
        pushq   %rbx
        .cfi_def_cfa_offset 16
        .cfi_offset 3, -16
        subq    $32, %rsp
        .cfi_def_cfa_offset 48
        leaq    16(%rsp), %rax
        movb    $99, 18(%rsp)
        movq    $3, 8(%rsp)
        movb    $0, 19(%rsp)
        movq    %rax, (%rsp)
        movl    $25185, %eax
        movw    %ax, 16(%rsp)
.LEHB0:
        call    _Z3foov
.LEHE0:
        movq    (%rsp), %rdi
        leaq    16(%rsp), %rax
        cmpq    %rax, %rdi
        je      .L6
        call    _ZdlPv
.L6:
        addq    $32, %rsp
        .cfi_remember_state
        .cfi_def_cfa_offset 16
        xorl    %eax, %eax
        popq    %rbx
        .cfi_def_cfa_offset 8
        ret
.L5:
        .cfi_restore_state
        movq    (%rsp), %rdi
        leaq    16(%rsp), %rdx
        movq    %rax, %rbx
        cmpq    %rdx, %rdi
        je      .L4
        call    _ZdlPv
.L4:
        movq    %rbx, %rdi
.LEHB1:
        call    _Unwind_Resume
.LEHE1:
        .cfi_endproc
.LFE995:
        .globl  __gxx_personality_v0
        .section        .gcc_except_table,"a",@progbits


While clang++ optimizes it away: clang version 5.0.0 (llvm-project SHA: 28b7c19c2379e17b26571260933467b9f98b449c)


$ ./bin/clang++ -O3 t.cpp -S -o t.s -stdlib=libc++
$ cat t.s

main:                                   # @main
        .cfi_startproc
# BB#0:                                 # %entry
        pushq   %rax
.Lcfi0:
        .cfi_def_cfa_offset 16
        callq   _Z3foov
        xorl    %eax, %eax
        popq    %rcx
        retq
.Lfunc_end0:
        .size   main, .Lfunc_end0-main
        .cfi_endproc


        .ident  "clang version 5.0.0 "
        .section        ".note.GNU-stack","",@progbits


---


### compiler : `gcc`
### title : `poor code for AVX vector compare`
### open_at : `2017-02-03T11:14:58Z`
### last_modified_date : `2021-08-01T15:52:46Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=79355
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `6.3.0`
### severity : `enhancement`
### contents :
gcc-6.2 (and previous versions) generates a very inefficient code for AVX when comparing 32-byte vectors:

$ cat a.c
#include <x86intrin.h>

__v8su eq2(__v8su a, __v8su b)
{
        return a == b;
}

$ gcc -S -Ofast -mavx a.c -o -
        .file   "a.c"
        .text   
        .p2align 4,,15
        .globl  eq2
        .type   eq2, @function
eq2:
.LFB4856:
        .cfi_startproc
        vmovd   %xmm0, %edx
        vmovd   %xmm1, %eax
        leaq    8(%rsp), %r10
        .cfi_def_cfa 10, 0
        vpextrd $1, %xmm0, %ecx
        andq    $-32, %rsp
        cmpl    %eax, %edx
[... extracting and comparing every element here ...]
        vpinsrd $1, %r11d, %xmm5, %xmm1
        vpinsrd $1, %r9d, %xmm7, %xmm0
        popq    %r10
        .cfi_def_cfa 10, 0
        vpunpcklqdq     %xmm3, %xmm0, %xmm0
        vpunpcklqdq     %xmm2, %xmm1, %xmm1
        popq    %rbp
        leaq    -8(%r10), %rsp
        .cfi_def_cfa 7, 8
        vinsertf128     $0x1, %xmm1, %ymm0, %ymm0
        ret

When it could instead generate (i.e. split vector in half and combine afterwards):

        vextractf128    $0x1, %ymm0, %xmm2
        vextractf128    $0x1, %ymm1, %xmm3
        vpcmpeqd        %xmm1, %xmm0, %xmm0
        vpcmpeqd        %xmm3, %xmm2, %xmm2
        vinsertf128     $0x1, %xmm2, %ymm0, %ymm0
        ret

$ gcc -v
Using built-in specs.
COLLECT_GCC=gcc
COLLECT_LTO_WRAPPER=/usr/lib/gcc/x86_64-linux-gnu/6/lto-wrapper
Target: x86_64-linux-gnu
Configured with: ../src/configure -v --with-pkgversion='Debian 6.3.0-5' --with-bugurl=file:///usr/share/doc/gcc-6/README.Bugs --enable-languages=c,ada,c++,java
,go,d,fortran,objc,obj-c++ --prefix=/usr --program-suffix=-6 --program-prefix=x86_64-linux-gnu- --enable-shared --enable-linker-build-id --libexecdir=/usr/lib --without-included-gettext --enable-threads=posix --libdir=/usr/lib --enable-nls --with-sysroot=/ --enable-clocale=gnu --enable-libstdcxx-debug --enable-libstdcxx-time=yes --with-default-libstdcxx-abi=new --enable-gnu-unique-object --disable-vtable-verify --enable-libmpx --enable-plugin --enable-default-pie --with-system-zlib --disable-browser-plugin --enable-java-awt=gtk --enable-gtk-cairo --with-java-home=/usr/lib/jvm/java-1.5.0-gcj-6-amd64/jre --enable-java-home --with-jvm-root-dir=/usr/lib/jvm/java-1.5.0-gcj-6-amd64 --with-jvm-jar-dir=/usr/lib/jvm-exports/java-1.5.0-gcj-6-amd64 --with-arch-directory=amd64 --with-ecj-jar=/usr/share/java/eclipse-ecj.jar --with-target-system-zlib --enable-objc-gc=auto --enable-multiarch --with-arch-32=i686 --with-abi=m64 --with-multilib-list=m32,m64,mx32 --enable-multilib --with-tune=generic --enable-checking=release --build=x86_64-linux-gnu --host=x86_64-linux-gnu --target=x86_64-linux-gnu                Thread model: posix
gcc version 6.3.0 20170124 (Debian 6.3.0-5)


---


### compiler : `gcc`
### title : `Doubling a single complex float  gives inefficient code`
### open_at : `2017-02-03T13:54:50Z`
### last_modified_date : `2021-09-01T03:05:54Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=79357
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `7.0`
### severity : `normal`
### contents :
Consider the following code:

#include <complex.h>
complex float f(complex float x) {
  return 2*x;
}

gcc with -O3  -march=core-avx2  gives:

f:
        vmovq   QWORD PTR [rsp-8], xmm0
        vmovss  xmm1, DWORD PTR [rsp-8]
        vmovss  xmm0, DWORD PTR [rsp-4]
        vaddss  xmm1, xmm1, xmm1
        vaddss  xmm0, xmm0, xmm0
        vmovss  DWORD PTR [rsp-16], xmm1
        vmovss  DWORD PTR [rsp-12], xmm0
        vmovq   xmm0, QWORD PTR [rsp-16]
        ret

Better and still suitable without -ffast-math would be:

f:
        vmulps    xmm0, xmm0, XMMWORD PTR .L_2il0floatpacket.1[rip] #3.12
        ret


---


### compiler : `gcc`
### title : `Squaring a complex float gives inefficient code`
### open_at : `2017-02-03T15:18:51Z`
### last_modified_date : `2023-05-15T07:22:30Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=79359
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `7.0`
### severity : `normal`
### contents :
Consider:

#include <complex.h>
complex float f(complex float x) {
  return x*x;
}


This PR has two parts.

Part 1.

In gcc 7 with -Ofast  -march=core-avx2  gives

f:
        vmovq   QWORD PTR [rsp-8], xmm0
        vmovss  xmm2, DWORD PTR [rsp-4]
        vmovss  xmm0, DWORD PTR [rsp-8]
        vmulss  xmm1, xmm2, xmm2
        vfmsub231ss     xmm1, xmm0, xmm0
        vmulss  xmm0, xmm0, xmm2
        vmovss  DWORD PTR [rsp-16], xmm1
        vaddss  xmm0, xmm0, xmm0
        vmovss  DWORD PTR [rsp-12], xmm0
        vmovq   xmm0, QWORD PTR [rsp-16]
        ret


Using the Intel C Compiler with -O3 -march=core-avx2 we get:

f:
        vmovshdup xmm1, xmm0                                    #3.12
        vshufps   xmm2, xmm0, xmm0, 177                         #3.12
        vmulps    xmm4, xmm1, xmm2                              #3.12
        vmovsldup xmm3, xmm0                                    #3.12
        vfmaddsub213ps xmm0, xmm3, xmm4                         #3.12
        ret  

which is somewhat better.


Part 2.

If we instead use -O3 alone for gcc we get:

f:
        vmovq   QWORD PTR [rsp-16], xmm0
        vmovss  xmm3, DWORD PTR [rsp-12]
        vmovss  xmm2, DWORD PTR [rsp-16]
        vmovaps xmm1, xmm3
        vmovaps xmm0, xmm2
        jmp     __mulsc3

which is much slower potentially.

In ICC if we use -fp-model precise we get:


f:
        vmovshdup xmm1, xmm0                                    #3.12
        vshufps   xmm2, xmm0, xmm0, 177                         #3.12
        vmulps    xmm4, xmm1, xmm2                              #3.12
        vmovsldup xmm3, xmm0                                    #3.12
        vfmaddsub213ps xmm0, xmm3, xmm4                         #3.12
        ret   

which is the same as above and if we use -fp-model strict we get:


f:
        vmovsldup xmm1, xmm0                                    #3.12
        vmovshdup xmm2, xmm0                                    #3.12
        vshufps   xmm3, xmm0, xmm0, 177                         #3.12
        vmulps    xmm4, xmm1, xmm0                              #3.12
        vmulps    xmm5, xmm2, xmm3                              #3.12
        vaddsubps xmm0, xmm4, xmm5                              #3.12
        ret 


The Intel docs claim that -fp-model strict is value safe (as is the "precise" option), turns on floating point exception semantics and turns off fuse add multiply.

jakub on IRC asked if it was really true that the icc code handles all the corner cases (NaNs etc.) correctly and suggested going through all the corner cases in mulsc3 and seeing what the ICC code emits.


---


### compiler : `gcc`
### title : `[7 Regression] 10% performance drop in SciMark2 LU after r242550`
### open_at : `2017-02-06T13:18:23Z`
### last_modified_date : `2023-05-06T19:02:19Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=79390
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `7.0`
### severity : `normal`
### contents :
Created attachment 40677
The relevant source code and generated asm before/after this change

The dense LU matrix factorization test from the old SciMark2 (http://math.nist.gov/scimark) used in the Phoronix compiler test suite has regressed 10% compared to the November trunk when run on Intel i7 6800K Broadwell (compiled with "-O3 -march=native"). GCC 6 generated much slower code, so this is not a regression compared to released versions of the compiler.

The regression was introduced in r242550:
------------------------------------------------------------------------
r242550 | wschmidt | 2016-11-17 15:22:17 +0100 (tor, 17 nov 2016) | 18 lines

[gcc]

2016-11-17  Bill Schmidt  <wschmidt@linux.vnet.ibm.com>
            Richard Biener  <rguenther@suse.de>

        PR tree-optimization/77848
	* tree-if-conv.c (tree_if_conversion): Always version loops unless
	the user specified -ftree-loop-if-convert.

[gcc/testsuite]

2016-11-17  Bill Schmidt  <wschmidt@linux.vnet.ibm.com>
            Richard Biener  <rguenther@suse.de>

        PR tree-optimization/77848
	* gfortran.dg/vect/pr77848.f: New test.
------------------------------------------------------------------------
and has the effect that the pivot-finding loop

    int LU_factor(int M, int N, double **A,  int *pivot)
    {
      int minMN =  M < N ? M : N;
      int j=0;

      for (j=0; j<minMN; j++)
      {
        /* find pivot in column j and  test for singularity. */

        int jp=j;
        int i;

        double t = fabs(A[j][j]);
        for (i=j+1; i<M; i++)
        {
          double ab = fabs(A[i][j]);
          if ( ab > t)
          {
            jp = i;
	    t = ab;
          }
        }

        pivot[j] = jp;
        ...

is transformed. The perf output seems to say that this is due to bad branch prediction, but I do not understand x86 assembler enough to be able to determine its cause (or to say if it really is a bug or just some random thing the compiler cannot know about...)


---


### compiler : `gcc`
### title : `Redundant move instruction when getting sign bit of double on 32-bit architecture`
### open_at : `2017-02-09T00:56:03Z`
### last_modified_date : `2021-01-19T03:05:38Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=79437
### status : `UNCONFIRMED`
### tags : `missed-optimization, ra`
### component : `target`
### version : `6.3.1`
### severity : `normal`
### contents :
Testing this simple example:

#ifdef DO_BOOL
bool
#else
int
#endif
sign(double a) noexcept {
    __UINT64_TYPE__ r;
    __builtin_memcpy(&r, &a, sizeof(r));
    return r >> 63 & 1;
}

Compiling with: -march=i686 -m32 -Os -fomit-frame-pointer

With DO_BOOL defined (bool sign(double)), this is the code generated:

sign(double):
        mov     eax, DWORD PTR [esp+8]
        shr     eax, 31
        ret

Without DO_BOOL (int sign(double)), this is the code generated instead:

sign(double):
        mov     edx, DWORD PTR [esp+8]
        mov     eax, edx
        shr     eax, 31
        ret

Notice the redundant moving around, from edx to eax instead of straight to eax.

These are my findings so far when investigating this:

* There is no difference between punning with memcpy or with union.

* Problem only happens when punning from floating point to integer.
Variants of the sign function that accept a void* or an uint64 directly are not affected (ie either retuning bool or int result in the same optimal code).

* Problem only happens when punning to uint64. When punning to uint32[2], ie:

sign(double a) noexcept {
    __UINT32_TYPE__ r[2];
    __builtin_memcpy(&r, &a, sizeof(r));
    return r[1] >> 31 & 1;
}

then again optimal code generation is performed in both cases.

* Inspecting the results of -fdump-tree-all reveals the following transformation happens early on (on -tree-original already)

--- build_bool/test.cc.003t.original    2017-02-08 22:07:22.749603900 -0200
+++ build_int/test.cc.003t.original     2017-02-08 22:07:11.675433300 -0200
@@ -1,5 +1,5 @@

-;; Function bool sign_mcpy1(double) (null)
+;; Function int sign_mcpy1(double) (null)
 ;; enabled by -tree-original


@@ -10,7 +10,7 @@
         long long unsigned int r;
     <<cleanup_point <<< Unknown tree: expr_stmt
   (void) __builtin_memcpy ((void *) &r, (const void *) &a, 8) >>>>>;
-    return <retval> = (signed long long) r < 0;
+    return <retval> = (int) (r >> 63);
   }
    >>>;

This basic structure persists until past .211t.optimized:

--- build_bool/test.cc.211t.optimized   2017-02-08 22:07:22.743595700 -0200
+++ build_int/test.cc.211t.optimized    2017-02-08 22:07:11.670441000 -0200
@@ -1,16 +1,16 @@

-;; Function bool sign_mcpy1(double) (_Z10sign_mcpy1d, funcdef_no=0, decl_uid=1665, cgraph_uid=0, symbol_order=0)
+;; Function int sign_mcpy1(double) (_Z10sign_mcpy1d, funcdef_no=0, decl_uid=1665, cgraph_uid=0, symbol_order=0)

-bool sign_mcpy1(double) (double a)
+int sign_mcpy1(double) (double a)
 {
   long long unsigned int _2;
-  signed long long r.1_3;
-  bool _4;
+  long long unsigned int _3;
+  int _4;

   <bb 2>:
   _2 = VIEW_CONVERT_EXPR<long long unsigned int>(a_5(D));
-  r.1_3 = (signed long long) _2;
-  _4 = r.1_3 < 0;
+  _3 = _2 >> 63;
+  _4 = (int) _3;
   return _4;

 }

So, the return bool case gets a different optimization early (at the front-end?), and later stages can't fix it.


---


### compiler : `gcc`
### title : `Possibly inefficient code for the inner product of two vectors`
### open_at : `2017-02-13T16:41:37Z`
### last_modified_date : `2021-08-03T02:28:02Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=79491
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `7.0`
### severity : `normal`
### contents :
Consider:

float f(float x[], float y[]) {
  float p = 0;
  for (int i = 0; i <64; i++)
    p += x[i] * y[i];
  return p;
}

Using gcc 7 (snapshot) and  -Ofast -march=core-avx2  you get:

f:
        mov     rax, rdi
        shr     rax, 2
        neg     rax
        and     eax, 7
        je      .L6
        vmovss  xmm0, DWORD PTR [rdi]
        vmulss  xmm1, xmm0, DWORD PTR [rsi]
        cmp     eax, 1
        je      .L7
        vmovss  xmm4, DWORD PTR [rdi+4]
        vfmadd231ss     xmm1, xmm4, DWORD PTR [rsi+4]
        cmp     eax, 2
        je      .L8
        vmovss  xmm3, DWORD PTR [rdi+8]
        vfmadd231ss     xmm1, xmm3, DWORD PTR [rsi+8]
        cmp     eax, 3
        je      .L9
        vmovss  xmm2, DWORD PTR [rdi+12]
        vfmadd231ss     xmm1, xmm2, DWORD PTR [rsi+12]
        cmp     eax, 4
        je      .L10
        vmovss  xmm3, DWORD PTR [rdi+16]
        vfmadd231ss     xmm1, xmm3, DWORD PTR [rsi+16]
        cmp     eax, 5
        je      .L11
        vmovss  xmm7, DWORD PTR [rdi+20]
        vfmadd231ss     xmm1, xmm7, DWORD PTR [rsi+20]
        cmp     eax, 7
        jne     .L12
        vmovss  xmm4, DWORD PTR [rsi+24]
        vfmadd231ss     xmm1, xmm4, DWORD PTR [rdi+24]
        mov     r9d, 57
        mov     r10d, 7
.L2:
        mov     ecx, 64
        sub     ecx, eax
        mov     eax, eax
        sal     rax, 2
        mov     r8d, ecx
        lea     rdx, [rdi+rax]
        add     rax, rsi
        shr     r8d, 3
        vmovups ymm0, YMMWORD PTR [rax+32]
        vmulps  ymm0, ymm0, YMMWORD PTR [rdx+32]
        vmovaps ymm3, YMMWORD PTR [rdx]
        vfmadd231ps     ymm0, ymm3, YMMWORD PTR [rax]
        vmovaps ymm4, YMMWORD PTR [rdx+64]
        vfmadd231ps     ymm0, ymm4, YMMWORD PTR [rax+64]
        vmovaps ymm5, YMMWORD PTR [rdx+96]
        vfmadd231ps     ymm0, ymm5, YMMWORD PTR [rax+96]
        vmovaps ymm6, YMMWORD PTR [rdx+128]
        vmovaps ymm7, YMMWORD PTR [rdx+160]
        vfmadd231ps     ymm0, ymm6, YMMWORD PTR [rax+128]
        vmovaps ymm3, YMMWORD PTR [rdx+192]
        vfmadd231ps     ymm0, ymm7, YMMWORD PTR [rax+160]
        vfmadd231ps     ymm0, ymm3, YMMWORD PTR [rax+192]
        cmp     r8d, 8
        jne     .L4
        vmovaps ymm4, YMMWORD PTR [rdx+224]
        vfmadd231ps     ymm0, ymm4, YMMWORD PTR [rax+224]
.L4:
        vhaddps ymm0, ymm0, ymm0
        mov     r8d, ecx
        mov     edx, r9d
        and     r8d, -8
        lea     eax, [r8+r10]
        sub     edx, r8d
        vhaddps ymm2, ymm0, ymm0
        vperm2f128      ymm0, ymm2, ymm2, 1
        vaddps  ymm0, ymm0, ymm2
        vaddss  xmm0, xmm0, xmm1
        cmp     ecx, r8d
        je      .L31
        movsx   rcx, eax
        vmovss  xmm5, DWORD PTR [rdi+rcx*4]
        vfmadd231ss     xmm0, xmm5, DWORD PTR [rsi+rcx*4]
        lea     ecx, [rax+1]
        cmp     edx, 1
        je      .L31
        movsx   rcx, ecx
        vmovss  xmm6, DWORD PTR [rdi+rcx*4]
        vfmadd231ss     xmm0, xmm6, DWORD PTR [rsi+rcx*4]
        lea     ecx, [rax+2]
        cmp     edx, 2
        je      .L31
        movsx   rcx, ecx
        vmovss  xmm7, DWORD PTR [rdi+rcx*4]
        vfmadd231ss     xmm0, xmm7, DWORD PTR [rsi+rcx*4]
        lea     ecx, [rax+3]
        cmp     edx, 3
        je      .L31
        movsx   rcx, ecx
        vmovss  xmm2, DWORD PTR [rdi+rcx*4]
        vfmadd231ss     xmm0, xmm2, DWORD PTR [rsi+rcx*4]
        lea     ecx, [rax+4]
        cmp     edx, 4
        je      .L31
        movsx   rcx, ecx
        vmovss  xmm7, DWORD PTR [rdi+rcx*4]
        vfmadd231ss     xmm0, xmm7, DWORD PTR [rsi+rcx*4]
        lea     ecx, [rax+5]
        cmp     edx, 5
        je      .L31
        movsx   rcx, ecx
        add     eax, 6
        vmovss  xmm5, DWORD PTR [rdi+rcx*4]
        vfmadd231ss     xmm0, xmm5, DWORD PTR [rsi+rcx*4]
        cmp     edx, 6
        je      .L31
        cdqe
        vmovss  xmm6, DWORD PTR [rdi+rax*4]
        vfmadd231ss     xmm0, xmm6, DWORD PTR [rsi+rax*4]
.L31:
        vzeroupper
        ret
.L10:
        mov     r9d, 60
        mov     r10d, 4
        jmp     .L2
.L7:
        mov     r9d, 63
        mov     r10d, 1
        jmp     .L2
.L6:
        mov     r9d, 64
        xor     r10d, r10d
        vxorps  xmm1, xmm1, xmm1
        jmp     .L2
.L8:
        mov     r9d, 62
        mov     r10d, 2
        jmp     .L2
.L9:
        mov     r9d, 61
        mov     r10d, 3
        jmp     .L2
.L11:
        mov     r9d, 59
        mov     r10d, 5
        jmp     .L2
.L12:
        mov     r9d, 58
        mov     r10d, 6
        jmp     .L2

However this seems more efficient from clang trunk:

f:                                      # @f
        vmovups ymm0, ymmword ptr [rsi]
        vmovups ymm1, ymmword ptr [rsi + 32]
        vmovups ymm2, ymmword ptr [rsi + 64]
        vmovups ymm3, ymmword ptr [rsi + 96]
        vmulps  ymm0, ymm0, ymmword ptr [rdi]
        vfmadd231ps     ymm0, ymm1, ymmword ptr [rdi + 32]
        vfmadd231ps     ymm0, ymm2, ymmword ptr [rdi + 64]
        vfmadd231ps     ymm0, ymm3, ymmword ptr [rdi + 96]
        vmovups ymm1, ymmword ptr [rsi + 128]
        vfmadd132ps     ymm1, ymm0, ymmword ptr [rdi + 128]
        vmovups ymm0, ymmword ptr [rsi + 160]
        vfmadd132ps     ymm0, ymm1, ymmword ptr [rdi + 160]
        vmovups ymm1, ymmword ptr [rsi + 192]
        vfmadd132ps     ymm1, ymm0, ymmword ptr [rdi + 192]
        vmovups ymm0, ymmword ptr [rsi + 224]
        vfmadd132ps     ymm0, ymm1, ymmword ptr [rdi + 224]
        vextractf128    xmm1, ymm0, 1
        vaddps  ymm0, ymm0, ymm1
        vpermilpd       xmm1, xmm0, 1   # xmm1 = xmm0[1,0]
        vaddps  ymm0, ymm0, ymm1
        vhaddps ymm0, ymm0, ymm0
        vzeroupper
        ret


It seems that gcc is going to some lengths to align the data which may not be worth the cost.


---


### compiler : `gcc`
### title : `[11/12/13/14 Regression] tree-ifcombine aarch64 performance regression with trunk@245151`
### open_at : `2017-02-15T17:18:55Z`
### last_modified_date : `2023-08-03T21:29:45Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=79534
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `7.0`
### severity : `normal`
### contents :
Created attachment 40752
Reduced test-case. Larger scores are better.

I am seeing about a 6-10% performance regression on a proprietary benchmark on AArch64, depending on the target micro-architecture.

# SHA d2c3261, trunk@245149, patch immediately preceding regression
/gcc/2017-02-03-12-17-59-d2c3261-master/bin/aarch64-sarc-linux-gnu-g++ -O3 -mcpu=cortex-a57 -std=c++11 -c a.cpp -o a.o
/gcc/2017-02-03-12-17-59-d2c3261-master/bin/aarch64-sarc-linux-gnu-g++  -o a a.o
(best of 3 runs)
  SCORE_DIRECTION ==> larger is better
  SCORE ==> 1619.832509

# SHA f56c861, trunk@245151, regressing patch
/gcc/2017-02-03-14-03-35-f56c861-master/bin/aarch64-sarc-linux-gnu-g++ -O3 -mcpu=cortex-a57 -std=c++11 -c a.cpp -o a.o
/gcc/2017-02-03-14-03-35-f56c861-master/bin/aarch64-sarc-linux-gnu-g++  -o a a.o
(best of 3 runs)
  SCORE_DIRECTION ==> larger is better
  SCORE ==> 1468.440527

# SHA e502db7, a recent 2/14/2017 tip build
/gcc/2017-02-14-23-11-19-e502db7-master/bin/aarch64-sarc-linux-gnu-g++ -O3 -mcpu=cortex-a57 -std=c++11 -c a.cpp -o a.o
/gcc/2017-02-14-23-11-19-e502db7-master/bin/aarch64-sarc-linux-gnu-g++  -o a a.o
  SCORE_DIRECTION ==> larger is better
  SCORE ==> 1483.952217


I do not see the slowdown when testing on x86_64.


---


### compiler : `gcc`
### title : `Missed optimization: useless guards for zero-initialized POD statics with =default default ctor at function scope`
### open_at : `2017-02-16T20:03:45Z`
### last_modified_date : `2021-08-30T02:23:00Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=79561
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `c++`
### version : `7.0.1`
### severity : `normal`
### contents :
Example code:

====BEGIN====
#include <atomic>
#include <type_traits>

template <typename T>
class BasicAtomic
{
public:
	std::atomic<T> v;

	BasicAtomic() = default;
	constexpr BasicAtomic(T t) noexcept : v(t) {}
	BasicAtomic(const BasicAtomic&) = delete;
	BasicAtomic &operator=(const BasicAtomic &) = delete;
	BasicAtomic &operator=(const BasicAtomic &) volatile = delete;
};

static_assert(std::is_pod<BasicAtomic<int>>::value, "oops");

static BasicAtomic<int> s_dyn;

int f(const char *str) {
	while (*str++)
    	++s_dyn.v;
  	return s_dyn.v;
}

int f_dynamic_init(const char *str) {
	static BasicAtomic<int> counter;
	while (*str++)
    	++counter.v;
  	return counter.v;
}

int f_static_init(const char *str) {
	static BasicAtomic<int> counter = {0};
	while (*str++)
    	++counter.v;
  	return counter.v;
}

====END====

GCC (all the way up to 7.0.1) adds a guard for f_dynamic_init(const char*)::counter (but not for the other two).

Clang 3.9.1 doesn't.

See the difference here: https://godbolt.org/g/erFlRq


---


### compiler : `gcc`
### title : `[8 Regression] Poor/Worse code generation for FPU on versions after 6`
### open_at : `2017-02-18T23:37:05Z`
### last_modified_date : `2021-05-14T10:10:52Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=79593
### status : `RESOLVED`
### tags : `missed-optimization, ra`
### component : `rtl-optimization`
### version : `6.0`
### severity : `normal`
### contents :
First of all sorry if the "Component" is set wrong, I didn't know what to pick (in respect to worse code generation than former versions) :)

Newer GCC versions seem to have regressed in their x87 code generation and do it extremely poor mistakes. This is about a regression in code generation for x87 code, not a "wishlist" of better code (i.e. it's about the possibility of having it reverted back to v5, at least in respect to x87 code gen). Sometimes I want to use it for various reasons, for example for "long double" high intermediate precision.

So technically this is a "performance bug" regression: In fact GCC version 5 generates quite good x87 code! So I'd simply want that generation reverted as a goal with this report (if the culprit is found of course), so don't misunderstand my intention please.

For example, since GCC 6, when you "convert" from say a "float" to a "long double", it generates spurious instructions like this sequence:

        fld     st(0)
        fcomip  st, st(2)

Instead of just:

        fcomip  st, st(1)

Which is IMHO killing one of the few nice features of x87 that it has automatic conversions to 80-bit all the time at no extra cost.

Bear in mind, GCC 5 is just fine and does the latter which is optimal. My C++ code actually does all calculations in "long double" on purpose, but it has to interface with data found in a "float" on a constant basis (reading it), and also returning some of it as float or double. The problem is, as you can see, newer versions of GCC do pointless "conversions" or something like that (I'm not sure myself why it does those pointless loads) when you load a "float" into a "long double" or something similar to that effect.

This is a two-fold problem: not only there's extra instructions, but it also requires one more "space" in the register stack resulting in more pointless spills (of long doubles!).


Now to illustrate what I mean so you can verify yourself, I've included a stupid little testcase that doesn't do much of anything, but it seems to exhibit this "poor code" generation, here's the code:



#include <stdint.h>

#undef MIN
#undef MAX
template<typename T> T inline MIN(T a, T b) { return a < b ? a : b; }
template<typename T> T inline MAX(T a, T b) { return a > b ? a : b; }

struct foo
{
  uint32_t num;
  union { uint32_t i; float f; };
};

extern float global_data[1024];

float bar(foo* __restrict__ e, uint32_t id)
{
  if(id >= e->num) return 0.0f;
  long double delta = (global_data[0]), min = (global_data[1]);
  delta = ((delta < 0.0l) ? (min-((long double)e->i)) : ((e->f)-min)) / delta;
  return (MIN(MAX(delta, 0.0l), 1.0l));
}



I compiled with e.g. -m32 -Ofast -mfpmath=387    (to have the return value in st(0) to show this issue better)

Here's the outputs for GCC versions 5, 6 and 7, with comments from me showing obvious poor code:


GCC 5:
   sub     esp, 12
   fldz
   mov     eax, DWORD PTR [esp+16]
   mov     ecx, DWORD PTR [esp+20]
   cmp     DWORD PTR [eax], ecx
   jbe     .L2
   fld     DWORD PTR global_data
   fld     DWORD PTR global_data+4
   fxch    st(2)
   fcomip  st, st(1)
   ja      .L12
   fxch    st(1)
   fsubr   DWORD PTR [eax+4]
 .L5:
   fdivrp  st(1), st
   fldz
   fxch    st(1)
   fcomi   st, st(1)
   fcmovb  st, st(1)
   fstp    st(1)
   fld1
   fcomi   st, st(1)
   fcmovnb st, st(1)
   fstp    st(1)
 .L2:
   add     esp, 12
   ret
 .L12:
   mov     eax, DWORD PTR [eax+4] # here the only issue I have with GCC 5
   xor     edx, edx
   mov     DWORD PTR [esp+4], edx # I don't understand what's this spill for?
   mov     DWORD PTR [esp], eax   # can't it load directly from [eax+4]?
   fild    QWORD PTR [esp]        # fild DWORD PTR [eax+4] or am I wrong?
   fsubp   st(2), st
   fxch    st(1)
   jmp     .L5



GCC 6:
   sub     esp, 12
   fldz
   mov     eax, DWORD PTR [esp+16]
   mov     ecx, DWORD PTR [esp+20]
   cmp     DWORD PTR [eax], ecx
   jbe     .L1
   fld     DWORD PTR global_data
   fld     st(0)                    # this is the poor "conversion" mentioned
   fld     DWORD PTR global_data+4
   fxch    st(3)
   fcomip  st, st(2)                # here's its "pop" (unneeded otherwise)
   fstp    st(1)
   ja      .L12
   fxch    st(1)
   fsubr   DWORD PTR [eax+4]
 .L5:
   fdivrp  st(1), st
   fldz
   fxch    st(1)
   fcomi   st, st(1)
   fcmovb  st, st(1)
   fstp    st(1)
   fld1
   fcomi   st, st(1)
   fcmovnb st, st(1)
   fstp    st(1)
 .L1:
   add     esp, 12
   ret
 .L12:
   mov     eax, DWORD PTR [eax+4]
   xor     edx, edx
   mov     DWORD PTR [esp+4], edx
   mov     DWORD PTR [esp], eax
   fild    QWORD PTR [esp]
   fsubp   st(2), st
   fxch    st(1)
   jmp     .L5



GCC 7:
   sub     esp, 12
   fldz
   mov     eax, DWORD PTR [esp+16]
   mov     edx, DWORD PTR [esp+20]
   cmp     DWORD PTR [eax], edx
   jbe     .L1
   fld     DWORD PTR global_data
   mov     eax, DWORD PTR [eax+4]
   fld     st(0)                    # same pointless instruction as v6
   fld     DWORD PTR global_data+4
   fxch    st(3)
   fcomip  st, st(2)
   fstp    st(1)
   ja      .L12
   mov     DWORD PTR [esp], eax     # worse than v6: spills to stack!
   fld     DWORD PTR [esp]          # instead of 'fsubr DWORD PTR [eax+4]'
   fsubrp  st(2), st
 .L5:
   fdivp   st(1), st
   fldz
   fxch    st(1)
   fcomi   st, st(1)
   fcmovb  st, st(1)
   fstp    st(1)
   fld1
   fld     st(0)                    # here it "converts" the constant 1.0l?
   fcomip  st, st(2)
   jnb     .L13
   fstp    st(1)
   jmp     .L6
 .L13:
   fstp    st(0)
 .L6:
 .L1:
   add     esp, 12
   ret
 .L12:
   mov     DWORD PTR [esp], eax
   mov     DWORD PTR [esp+4], 0
   fild    QWORD PTR [esp]
   fsubp   st(2), st
   jmp     .L5



As you can see, each new version made it even worse than it was. GCC 7 is especially bad, it even refuses to do "fsubr DWORD PTR [eax+4]" directly, and opts for a spill and a load. Furthermore, it loads a constant twice for no reason, even when I explicitly declared the constant literal as "long double". Am I missing something obvious?

Can this behavior be reverted? Version 5 obviously produces much better x87 code. Please note that I don't know anything about GCC's internals, but IMO code gen of version 5 is "quite good" and should be kept instead of breaking it like now...

Alternatively, I'd love to hear if this is a new behavior consequence of a command line setting that is now enabled by default on optimizing, so I can unset it myself. Am I missing some command line setting here?

Let me know if you need more info so I can see what to provide.


---
