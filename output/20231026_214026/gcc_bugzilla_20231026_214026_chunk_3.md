### Total Bugs Detected: 4649
### Current Chunk: 3 of 30
### Bugs in this Chunk: 160 (From bug 321 to 480)
---


### compiler : `gcc`
### title : `Missing expression simplication for conditional OR`
### open_at : `2008-02-23T05:15:53Z`
### last_modified_date : `2021-06-03T02:59:51Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=35306
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.3.0`
### severity : `enhancement`
### contents :
The following rule is not handled by GCC


(a & x) || (a & y) ===>  a & (x | y)


---


### compiler : `gcc`
### title : `Late struct expansion leads to missing PRE`
### open_at : `2008-02-23T05:25:14Z`
### last_modified_date : `2021-07-26T04:10:26Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=35309
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.3.0`
### severity : `enhancement`
### contents :
// Example: the load of structs at return is partially redundant

struct A {
  int a;
  int b;
  int c;
  int d;
} ag, ag2,ag3;


struct A foo(int n)
{
   if (n)
   {
     ag2 = ag;
   }

   return ag;
}

// Gcc generated assembly code:

foo:
.LFB2:
        testl   %edi, %edi
        je      .L2
        movq    ag(%rip), %rax
        movq    %rax, ag2(%rip)
        movq    ag+8(%rip), %rax
        movq    %rax, ag2+8(%rip)
.L2:
        movq    ag+8(%rip), %rdx
        movq    ag(%rip), %rax
        ret
.LFE2:


---


### compiler : `gcc`
### title : `Late struct expansion -- missing PRE (2)`
### open_at : `2008-02-23T05:27:00Z`
### last_modified_date : `2021-12-27T03:45:59Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=35310
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.3.0`
### severity : `enhancement`
### contents :
union U {
   struct A {
     int a;
     int b;
  }aa;
  long long ll;
};

struct B{
   union U u1;
   union U u2;
} bg;
struct B bg;

struct B bar();
int foo (int n)
{
     if (n)
     {
        bg = bar();
     }

     return bg.u1.ll + bg.u2.ll;
};

// Two union fields loads are partially redundant.

gcc genearted code at -O2:

foo:
.LFB2:
        subq    $24, %rsp
.LCFI0:
        testl   %edi, %edi
        je      .L2
        xorl    %eax, %eax
        call    bar
        movq    %rax, bg(%rip)
        movq    %rdx, bg+8(%rip)
.L2:
        movq    bg(%rip), %rax
        addl    bg+8(%rip), %eax
        addq    $24, %rsp
        ret


---


### compiler : `gcc`
### title : `Early exit loop with short known trip count not unrolled`
### open_at : `2008-02-24T04:20:54Z`
### last_modified_date : `2022-01-10T11:06:24Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=35341
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.3.0`
### severity : `enhancement`
### contents :
Gcc fully unrolls short trip counted (known) loop if the unrolled loop body size d oes not exceed a threshold. However, if  the loop has early exit, this is not done -- leading to missing scalar opt later on.

Example:

int a[100];
int b[100];
int foo(void)
{
     int i, j;

     for (i = 0; i < 5; i ++)
     {
          a[2*i] += a[i];
          if (a[2*i] == 10) break;
     }

     return 0;
}


---


### compiler : `gcc`
### title : `Sum-reduction loop not recognized (enable -fvariable-expansion-in-unroller by default)`
### open_at : `2008-02-24T04:28:01Z`
### last_modified_date : `2021-07-26T03:54:06Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=35343
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.3.0`
### severity : `enhancement`
### contents :
It is beneficial to unroll reduction loop (and split the reduction target) to reduce dependence height due to recurrence, but GCC does not perform such optimization (-O3 -fno-tree-vectorize)


int a[1000];
int b[1000];
int foo(int n)
{

   int s = 0;
   int i = 0;
   for (i = 0; i < 1000 ; i++)
   {
       s += a[i] + b[2*i];
   }
   return s;
}


---


### compiler : `gcc`
### title : `Loop unswitching to produce perfect loop nest`
### open_at : `2008-02-24T04:33:05Z`
### last_modified_date : `2021-07-26T03:36:03Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=35344
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.3.0`
### severity : `enhancement`
### contents :
GCC loop unswitching is very good -- handles most of the cases I tried. The only only thing I notice is that the nested for loops in C in the example below is not converted into a perfect loop nest:

int** p;

int** q;

void foo(int m, int n)
{
   int i, j;

   for (i = 0;  i < m; i++)
   {
      for (j = 0; j < n ; j++)
     {
        p[i][j] += q[i][j];
        q[i][j] ++;
     }
   }

}

It is generated into (roughly) the following code by gcc (-O3 -fno-tree-vectorize)

 if (m > 0)
 {
      do
      {
          if (n > 0 )
          {
              do
              {
                 p[i][j] += q[i][j];
                 q[i][j] += 1;
                 j += 1;
              } while ( j < n);
          }
          i+=1;
     } while (i < m);
 }

Ideally-- it should be:

 if (m > 0)
 {
    if (n >0)
    {
        do
        {
            do
            {
              ....
              j++;
            } while(...);
            i++;
        }while (...);
     }
    // empty loop deleted
}


---


### compiler : `gcc`
### title : `Scalar replacement to handle output dependence`
### open_at : `2008-02-24T04:40:22Z`
### last_modified_date : `2021-06-08T09:30:38Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=35345
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.3.0`
### severity : `enhancement`
### contents :
// David Li
Gcc's scalar replacement and predictive commoning implementation is very good. There are some missing cases. Handling output dependence is one of them.

Handling of output dependence. In this case, the store at (1) is dead except for the last iteration -- it should be sinked out of the loop. (-O3 -fno-tree-vectorize)

int a[1000];
int b[1000];

void foo(int n)
{
   int i = 1;
   for(; i < n; i++)
   {
        a[i+1] =i;     // (1) 
        a[i] = i+1;
   }
}


---


### compiler : `gcc`
### title : `Missing Index splitting support in  gcc`
### open_at : `2008-02-25T04:55:05Z`
### last_modified_date : `2020-01-28T06:56:47Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=35356
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.3.0`
### severity : `enhancement`
### contents :
The following cases are not handled by gcc:

case 1:
Example 28:  search loop -- yes it is silly, but exists in real program:

  for (i = 0; i < n; i++)
  {
      if ( i == k)
          a[i] = ...
  }

Should eliminate the loop and generate:

if (k >= 0 && k < n)
    a[k] = ....


case 2:

  for (i = 0; i < n; i++)
  {
       if (i == k)
          a[i] = 1;
       else 
          a[i] = i;
  }

Should be converted into:
  for (i = 0; i < min (n, k); i++)
     a[i] = i;
  if (k >= 0 && k < n)
     a[k] = 1;
  for (i = max(k+1,0); i < n; i++)
     a[i] = i;


case 3 (similar to case 1): (from art)

int winner,numf1s,numf2s, resonant,cp,numpatterns;
double **tds;
double d, tsum;
typedef struct {
      double y;
      int   reset;
      } xyz;

xyz *Y;
int ti;

void match()
{
  int tj,tresult;
  for (tj=0;tj<numf2s;tj++)
    {
      if ((tj == winner) &&(Y[tj].y > 0))
        tsum += tds[ti][tj] * d;
    }
}


---


### compiler : `gcc`
### title : `Loop peeling not happening`
### open_at : `2008-02-25T05:01:20Z`
### last_modified_date : `2022-12-19T21:06:40Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=35357
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.3.0`
### severity : `enhancement`
### contents :
//David Li

Loop peeling is special case of index splitting. Gcc has support for this (under -O3 -funrool_loops, also -fno-tree-vectorize for the simple case), but it does not happen for the following cases:

int a[100];
int b[1000];
void foo(int n)
{
      int i;
      for ( i = 0; i <= n; i++)
      {

           b[i*2] = a[3*i+1];
           if (i < n)
              b[i*2] +=1;
      }
}


---------------------

int a[100];
int b[1000];
void foo(int n)
{
      int i;
      for ( i = 0; i < n; i++)
      {
          if (i==0) b[i*2] +=1;
           b[i*2] = a[3*i+1];
      }
}


---


### compiler : `gcc`
### title : `Static (base/offset/size rule) should be extended to handle array elements`
### open_at : `2008-02-25T05:19:38Z`
### last_modified_date : `2021-07-26T09:02:35Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=35360
### status : `RESOLVED`
### tags : `alias, missed-optimization`
### component : `middle-end`
### version : `4.3.0`
### severity : `enhancement`
### contents :
// David Li
the two references in the loop are not aliased. Not optimized by gcc

struct A{
 int a;
 int b;
};

struct A aa[100];


void foo(int n, int i, int j)
{
  int k = 0;
  for (k = 0; k < n; k++)
  {
      aa[i].a += aa[j].b;
  }
}


---


### compiler : `gcc`
### title : `Splitting up a switch table into smaller ones (where there a huge gaps between the clusters)`
### open_at : `2008-02-25T05:37:42Z`
### last_modified_date : `2019-03-01T14:57:30Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=35362
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.3.0`
### severity : `enhancement`
### contents :
// David Li

For switch statement with very large case value range, but the number of actual cases are not large, gcc generated code seems suboptimal: in some cases, huge jump table is generated (with lots of duplicated entries), while in other cases, huge concatenated ifs are generated (the number of compares for a hit may be more than 3 even with binary search scheme). For those cases, mixed mode expansion may be preferred -- where both compares and jump tables are used.

// Example 1: huge jump  table (> 300 entries)

int g;
int foo(int k)
{

   switch (k)
  {

    case 20: g += 10; break;
    case 18: g += 11; break;
    case 16: g += 12; break;
    case 14: g += 13; break;
    case 12: g += 14; break;
    case 10: g += 15; break;
    case 8: g += 3; break;
    case 4: g += 2; break;
    case 2: g -= 1; break;
    case 0: g += 1; break;

    case 120: g += 10; break;
    case 118: g += 11; break;
    case 116: g += 12; break;
    case 114: g += 13; break;
    case 112: g += 14; break;
    case 110: g += 15; break;
    case 119: g += 3; break;
    case 121: g += 2; break;
    case 122: g -= 1; break;
    case 123: g += 1; break;

    case 220: g += 10; break;
    case 218: g += 11; break;
    case 216: g += 12; break;
    case 214: g += 13; break;
    case 212: g += 14; break;
    case 210: g += 15; break;

    case 324: g += 10; break;
    case 323: g += 10; break;
    case 322: g += 10; break;
    case 321: g += 10; break;
    case 320: g += 10; break;
    case 318: g += 11; break;
    case 316: g += 12; break;
    case 314: g += 13; break;
    case 312: g += 14; break;
    case 310: g += 15; break;

    default: break;
 }
 return g;
}

Example 2: No jump table used:

int g;
int foo(int k)
{
   switch (k)
  {

    case 20: g += 10; break;
    case 18: g += 11; break;
    case 16: g += 12; break;
    case 14: g += 13; break;
    case 12: g += 14; break;
    case 10: g += 15; break;
    case 8: g += 3; break;
    case 4: g += 2; break;
    case 2: g -= 1; break;
    case 0: g += 1; break;

    case 120: g += 10; break;
    case 118: g += 11; break;
    case 116: g += 12; break;
    case 114: g += 13; break;
    case 112: g += 14; break;
    case 110: g += 15; break;
    case 119: g += 3; break;
    case 121: g += 2; break;
    case 122: g -= 1; break;
    case 123: g += 1; break;

    case 220: g += 10; break;
    case 218: g += 11; break;
    case 216: g += 12; break;
    case 214: g += 13; break;
    case 212: g += 14; break;
    case 210: g += 15; break;

    case 324: g += 10; break;
    case 323: g += 10; break;
    case 322: g += 10; break;
    case 321: g += 10; break;
    case 320: g += 10; break;
    case 318: g += 11; break;
    case 316: g += 12; break;
    case 314: g += 13; break;
    case 312: g += 14; break;
    case 310: g += 15; break;

    case 1324: g += 10; break;
    case 1323: g += 10; break;
    case 1322: g += 10; break;
    case 1321: g += 10; break;
    case 1320: g += 10; break;
    case 1318: g += 11; break;

    default: break;
 }
 return g;
}


---


### compiler : `gcc`
### title : `Missing bit field coalescing optimization`
### open_at : `2008-02-25T05:38:52Z`
### last_modified_date : `2021-11-28T07:20:25Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=35363
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.6.0`
### severity : `enhancement`
### contents :
// David Li

struct A{
  int b1: 3;
  int b2: 3;
  int b3: 2;
  int b4: 17;
}a;
void foo()
{
    a.b1 = 2;
    a.b2 = 3;
    a.b4 = 8;
}

This requires one LOAD + one OR + one STORE, but the generate code looks like:

foo:
.LFB2:
        movzbl  a(%rip), %eax
        andl    $-64, %eax
        orl     $26, %eax
        movb    %al, a(%rip)
        movl    a(%rip), %eax
        andl    $-33554177, %eax
        orb     $8, %ah
        movl    %eax, a(%rip)
        ret


---


### compiler : `gcc`
### title : `Improve targetm.binds_local_p`
### open_at : `2008-03-09T15:06:36Z`
### last_modified_date : `2022-03-01T15:45:48Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=35513
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.4.0`
### severity : `normal`
### contents :
Compiler wants to know:

1. If a symbol will be referenced locally within the file. If a readonly
symbol with initializer is referenced with the file, compiler may
replace symbol read with its initializer. PRs 35402/35494/35501.
2. If a symbol will be referenced locally within the module, an optimized
relocation may be used, depend on symbol types. But for weak, undefined,
hidden function symbol, it is necessary to treat it as global for read.
PR 32219.
3. If a function will be called with in the module, an optimized
relocation may be used.

However, the current targetm.binds_local_p doesn't distinguish those
different usages. As the result, gcc makes wrong conclusions in some
cases, PR 32219.

I think targetm.binds_local_p should take a parameter to indicate
its usage.


---


### compiler : `gcc`
### title : `tracer pass is run too late`
### open_at : `2008-03-12T05:55:26Z`
### last_modified_date : `2019-03-06T10:22:18Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=35545
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.4.0`
### severity : `enhancement`
### contents :
In the following example, virtual calls via ap should be speciallized -- there is one dominatating call target, but compiling the program at -O3 with -fprofile-use, it does not happen.

g++ -O1 -fprofile-generate devirt.cc
./a.out
g++ -fprofile-use -O3 -fdump-tree-optimized devirt.cc


// devirt.cc

class A {
public:
  virtual int foo() {
     return 1;
  }

int i;
};

class B : public A
{
public:
  virtual int foo() {
     return 2;
  }

 int b;
} ;


int main()
{
 int i;

  A* ap = 0;

  for (i = 0; i < 10000; i++)
  {

     if (i%7==0)
     {
        ap = new A();
     }
     else
        ap = new B();

    ap->foo();

    delete ap;

  }

  return 0;

}


---


### compiler : `gcc`
### title : `Missing CSE/PRE for memory operations involved in virtual call.`
### open_at : `2008-03-12T20:43:53Z`
### last_modified_date : `2023-01-09T14:30:31Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=35560
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.4.0`
### severity : `enhancement`
### contents :
In the following example, three loads to the vtable pointer value can be CSEed, so are two accesses to the same vtable entry (for foo), but final assembly dumping indicate otherwise.  It is true that the object pointed to by ap may be modified by the calls, but this does not apply to the vptr field.

class A {

public:

virtual int foo(int i);
virtual int bar(int i);

private:
int a;
};

int test(A* ap, int i)
{

   int r1 = ap->foo(i);
   int r2 = ap->bar(i);

   return r1+r2 + ap->foo(i);
}
     ...
.LCFI4:
        movq    (%rdi), %rax
        movl    %esi, %r12d
        call    *(%rax)
        movl    %eax, %r13d
        movq    (%rbx), %rax   <----- redundant
        movl    %r12d, %esi
        movq    %rbx, %rdi
        call    *8(%rax)
        movl    %eax, %ebp
        movq    (%rbx), %rax   <---- redundant
        movl    %r12d, %esi
        movq    %rbx, %rdi
        call    *(%rax)             <-- *(%rax) is redundant
        leal    (%rbp,%r13), %edx
        movq    8(%rsp), %rbx
        movq    16(%rsp), %rbp
        movq    24(%rsp), %r12
        movq    32(%rsp), %r13
        addq    $40, %rsp
        leal    (%rdx,%rax), %eax
        ret


---


### compiler : `gcc`
### title : `Promote written once local aggregates to static`
### open_at : `2008-03-12T20:59:16Z`
### last_modified_date : `2023-06-02T00:13:32Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=35561
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.4.0`
### severity : `enhancement`
### contents :
// David Li

In some programs (not so rare), local arrays/aggregates are used to hold some program parameters that never change. Such local arrays are candidates for being promoted into readonly static data, in order to 1) reducing stack size; 2) avoid paying the overhead of the initializing the array each time the routine is entered.

Such optimization can be extended to cases when the local array is defined once on entry of a single entry routine, read within the region, but not live out of it (such cases can be created due to inlining).

Example:

int foo(...)
{
   int coeff_array[30] = {1,2,3.......};

   ..... = coeff_array[i];
   ..
}


---


### compiler : `gcc`
### title : `gcc.dg/tree-ssa/loop-25.c scan-tree-dump-times profile fails`
### open_at : `2008-03-18T21:02:42Z`
### last_modified_date : `2021-09-14T07:04:42Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=35629
### status : `NEW`
### tags : `missed-optimization, xfail`
### component : `tree-optimization`
### version : `4.4.0`
### severity : `normal`
### contents :
Revision 133318 failed:

Native configuration is i686-pc-linux-gnu

		=== gcc tests ===


Running target unix
XPASS: gcc.dg/cpp/cmdlne-dI-M.c scan-file (^|\\\\n)cmdlne-dI-M.*:[^\\\\n]*cmdlne-dI-M.c
XPASS: gcc.dg/cpp/cmdlne-dM-M.c scan-file (^|\\\\n)cmdlne-dM-M[^\\\\n]*:[^\\\\n]*cmdlne-dM-M.c
FAIL: gcc.dg/tree-ssa/loop-25.c scan-tree-dump-times profile "Found latch edge" 5
FAIL: gcc.dg/tree-ssa/loop-25.c scan-tree-dump-times profile "Merged latch edges" 2
FAIL: gcc.dg/tree-ssa/loop-25.c scan-tree-dump-times profile "4 loops found" 2
FAIL: gcc.dg/tree-ssa/loop-25.c scan-tree-dump-times profile "3 loops found" 2
FAIL: gcc.dg/tree-ssa/loop-25.c scan-tree-dump-times profile "2 loops found" 1

		=== gcc Summary ===

# of expected passes		49134
# of unexpected failures	5
# of unexpected successes	2
# of expected failures		166
# of untested testcases		35
# of unsupported tests		269
/home/jrp/build/gcc/xgcc  version 4.4.0 20080318 (experimental) (GCC) 



Using built-in specs.
Target: i686-pc-linux-gnu
Configured with: ../gcc/configure -v --enable-languages=c,c++,fortran --enable-shared --with-system-zlib --without-included-gettext --enable-threads=posix --enable-nls --enable-__cxa_atexit --enable-clocale=gnu --enable-libstdcxx-debug --enable-mpfr --enable-checking=release --with-arch=core2
Thread model: posix
gcc version 4.4.0 20080317 (experimental) (GCC)


---


### compiler : `gcc`
### title : `gcc is not using the overflow flag`
### open_at : `2008-03-20T01:20:15Z`
### last_modified_date : `2021-06-03T01:30:10Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=35646
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.3.0`
### severity : `enhancement`
### contents :
Two simple examples:

unsigned int add(unsigned int a,unsigned int b) {
  if (a+b<a) exit(0);
  return a+b;
}

This produces code without an extra cmp, as expected.

void addto(unsigned int* a,unsigned int b) {
  if ((*a+=b)<b) exit(0);
}

This generates this code:

        movl    %esi, %eax
        addl    (%rdi), %eax
        cmpl    %eax, %esi
        movl    %eax, (%rdi)
        ja      .L5

I would have expected something like:

        addl    %esi, (%rdi)
        jo      .L5

Can we please fix this?  It is a common case for integer overflow checking, and if we could get programmers to see that checking for integer overflows is not inefficient and you don't need some inline assembly code to get it to be efficient, that would help a lot.


---


### compiler : `gcc`
### title : `Missed (a == 0) && (b == 0) into (a|(typeof(a)(b)) == 0 when the types don't match`
### open_at : `2008-03-25T04:31:50Z`
### last_modified_date : `2018-11-19T12:42:05Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=35691
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.4.0`
### severity : `enhancement`
### contents :
While looking into PR 35429, I noticed this small missed optimization.
If we have:
typedef unsigned int1;

int foo(int z0, int1 z1)
{
  return z0 != 0 || z1 != 0;
}

int foo1(int z0, int1 z1)
{
  return z0 == 0 && z1 == 0;
}
--- CUT ---
Both of those should optimize as int is the same size as unsigned and we are comparing against 0.  The same thing should happen with int and long on a ILP32 target.


---


### compiler : `gcc`
### title : `collapsing popping args for tail calls at -Os`
### open_at : `2008-03-31T15:12:27Z`
### last_modified_date : `2019-04-14T19:34:16Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=35775
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.4.0`
### severity : `enhancement`
### contents :
At "-Os", the two "popl %ebp" instructions
in the alternate branches could have been collapsed.

$ cat tailcall.c 
void foo(int a)
{
  if (a)
    bar();
  else
    baz();
}
$ gcc -Os -S tailcall.c 
$ cat tailcall.s 
	.file	"tailcall.c"
	.text
.globl foo
	.type	foo, @function
foo:
	pushl	%ebp
	movl	%esp, %ebp
	cmpl	$0, 8(%ebp)
	je	.L2
	popl	%ebp
	jmp	bar
.L2:
	popl	%ebp
	jmp	baz
	.size	foo, .-foo
	.ident	"GCC: (GNU) 4.4.0 20080330 (experimental)"
	.section	.note.GNU-stack,"",@progbits


---


### compiler : `gcc`
### title : `Object code is bigger at -Os than at -O2`
### open_at : `2008-04-02T17:48:10Z`
### last_modified_date : `2022-01-05T10:44:38Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=35806
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `target`
### version : `4.4.0`
### severity : `enhancement`
### contents :
Hi,
the code below compiles to 60 byte when using -Os
and 4 byte when using -O2.

This is just one example of many from the test suite: 

extern void f(char *const *);
void g (char **o)
{
  static const char *const multilib_exclusions_raw[] = { 0 };
  const char *const *q = multilib_exclusions_raw;

  f (o);
  while (*q++)
    f (o);
}


---


### compiler : `gcc`
### title : `Pushing / Poping ebx without using it.`
### open_at : `2008-04-13T17:48:42Z`
### last_modified_date : `2021-12-25T07:07:32Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=35926
### status : `RESOLVED`
### tags : `missed-optimization, ra`
### component : `target`
### version : `4.3.0`
### severity : `enhancement`
### contents :
The following code produces a push and pop of ebx without using it inside:

typedef struct toto_s *toto_t;
toto_t add (toto_t a, toto_t b) {
  int64_t tmp = (int64_t)(intptr_t)a + ((int64_t)(intptr_t)b&~1L);
  return (toto_t)(intptr_t) tmp;
}

Here is the output of the compiler:
gcc version 4.3.0 (GCC) 
COLLECT_GCC_OPTIONS='-v' '-O3' '-S' '-fomit-frame-pointer' '-save-temps' '-mtune=generic'
 /usr/local/libexec/gcc/i686-pc-linux-gnu/4.3.0/cc1 -E -quiet -v immediate.c -mtune=generic -fomit-frame-pointer -O3 -fpch-preprocess -o immediate.i
ignoring nonexistent directory "/usr/local/lib/gcc/i686-pc-linux-gnu/4.3.0/../../../../i686-pc-linux-gnu/include"
#include "..." search starts here:
#include <...> search starts here:
 /usr/local/include
 /usr/local/lib/gcc/i686-pc-linux-gnu/4.3.0/include
 /usr/local/lib/gcc/i686-pc-linux-gnu/4.3.0/include-fixed
 /usr/include
End of search list.
COLLECT_GCC_OPTIONS='-v' '-O3' '-S' '-fomit-frame-pointer' '-save-temps' '-mtune=generic'
 /usr/local/libexec/gcc/i686-pc-linux-gnu/4.3.0/cc1 -fpreprocessed immediate.i -quiet -dumpbase immediate.c -mtune=generic -auxbase immediate -O3 -version -fomit-frame-pointer -o immediate.s
GNU C (GCC) version 4.3.0 (i686-pc-linux-gnu)
        compiled by GNU C version 4.3.0, GMP version 4.2.2, MPFR version 2.3.1.
warning: GMP header version 4.2.2 differs from library version 4.1.4.
GGC heuristics: --param ggc-min-expand=98 --param ggc-min-heapsize=128998
Compiler executable checksum: 6f004a95f08b214d06bfab9d0128e657
COMPILER_PATH=/usr/local/libexec/gcc/i686-pc-linux-gnu/4.3.0/:/usr/local/libexec/gcc/i686-pc-linux-gnu/4.3.0/:/usr/local/libexec/gcc/i686-pc-linux-gnu/:/usr/local/lib/gcc/i686-pc-linux-gnu/4.3.0/:/usr/local/lib/gcc/i686-pc-linux-gnu/
LIBRARY_PATH=/usr/local/lib/gcc/i686-pc-linux-gnu/4.3.0/:/usr/local/lib/gcc/i686-pc-linux-gnu/4.3.0/../../../:/lib/:/usr/lib/
COLLECT_GCC_OPTIONS='-v' '-O3' '-S' '-fomit-frame-pointer' '-save-temps' '-mtune=generic'
[pphd@localhost to-do]$ cat immediate.s 
        .file   "immediate.c"
        .text
        .p2align 4,,15
.globl add
        .type   add, @function
add:
        pushl   %ebx
        movl    12(%esp), %eax
        movl    8(%esp), %ecx
        popl    %ebx
        andl    $-2, %eax
        addl    %ecx, %eax
        ret
        .size   add, .-add
        .ident  "GCC: (GNU) 4.3.0"
        .section        .note.GNU-stack,"",@progbits

I can reproduce this problem for GCC 4.1.2 and GCC 4.2.2 too.


---


### compiler : `gcc`
### title : `Loop interchange not performed`
### open_at : `2008-04-22T14:55:35Z`
### last_modified_date : `2023-10-17T20:56:45Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=36010
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.4.0`
### severity : `enhancement`
### contents :
For the testcase

double a[16][64], y[64], x[16];
void foo(void)
{
  int i, j;
  for (j = 0; j < 64; ++j)
    for (i = 0; i < 16; ++i)
      y[j] = y[j] + a[i][j] * x[i];
}

with -O2 -fno-tree-pre -fno-tree-loop-im -ftree-loop-linear loop interchange
is performed but with PRE or lim moving the load (and the store) from/to
y[j] out of the innermost loop the interchange is no longer performed because

      before = gcc_loopnest_to_lambda_loopnest (loop_nest, &oldivs,
                                                &invariants, &lambda_obstack);

returns NULL.


---


### compiler : `gcc`
### title : `Loop interchange not performed, data dependence analysis defect`
### open_at : `2008-04-22T15:01:52Z`
### last_modified_date : `2021-12-25T11:16:47Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=36011
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.4.0`
### severity : `enhancement`
### contents :
For the testcase

double a[16][16][64], y[16][64], x[16][16];

void foo(void)
{
  int i, j, k;
  for (k = 0; k < 16; ++k)
    for (j = 0; j < 64; ++j)
      for (i = 0; i < 16; ++i)
        {
          y[k][j] = y[k][j] + a[k][i][j] * x[k][i];
        }
}

loop interchange is performed with -O2 -fno-tree-pre -fno-tree-loop-im -ftree-loop-linear but not with PRE or lim moving the store/load to/from
y[k][j].  The interchange fails because

            /* Validate the resulting matrix.  When the transformation
               is not valid, reverse to the previous transformation.  */
            if (!lambda_transform_legal_p (trans, depth, dependence_relations))

returns false which is because constants or SSA names from final values
leak into the access fns like

(compute_affine_dependence
  (stmt_a =
pretmp.11_3 = y[k_41][j_40])
  (stmt_b =
y[k_41][j_40] = D.1578_20)
(subscript_dependence_tester
(analyze_overlapping_iterations
  (chrec_a = {0, +, 1}_2)
  (chrec_b = 63)
(analyze_siv_subscript
)
  (overlap_iterations_a = [63]
)
  (overlap_iterations_b = [0]
)

which confuses dependency analysis here:

      else if (!operand_equal_p (access_fn_a, access_fn_b, 0))
        {
          /* This can be for example an affine vs. constant dependence
             (T[i] vs. T[3]) that is not an affine dependence and is
             not representable as a distance vector.  */
          non_affine_dependence_relation (ddr);
          return false;


---


### compiler : `gcc`
### title : `shift operator strength reduction in loops not done.`
### open_at : `2008-04-22T22:26:58Z`
### last_modified_date : `2021-08-28T23:36:34Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=36020
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.3.0`
### severity : `enhancement`
### contents :
Consider this simple loop:

int shift_integer (int value, unsigned int amount)
{
  unsigned int i;

  for (i=0; i<amount; i++)
   value<<=1;

  return value;
}

The compiler generates aloop to evalue the result and does not strength-reduce the calculation.

A slightly different version of that loop gets strength-reduced. I just replaced the shift with an add.

int inc_integer (int value, unsigned int amount)
{
  unsigned int i;

  for (i=0; i<amount; i++)
   value+=1;

  return value;
}

Tested with gcc 4.3.0 i686-pc-cygwin. 

Assembly-Output with -O3 -fomit-frame-pointer:

        .file   "test.c"
        .text
        .p2align 4,,15
.globl _shift_integer
        .def    _shift_integer; .scl    2;      .type   32;     .endef
_shift_integer:
        movl    8(%esp), %ecx
        movl    4(%esp), %eax
        testl   %ecx, %ecx
        je      L2
        xorl    %edx, %edx
        .p2align 4,,7
L3:
        addl    $1, %edx
        addl    %eax, %eax
        cmpl    %edx, %ecx
        ja      L3
L2:
        rep
        ret
        .p2align 4,,15
.globl _inc_integer
        .def    _inc_integer;   .scl    2;      .type   32;     .endef
_inc_integer:
        movl    8(%esp), %edx
        movl    4(%esp), %eax
        testl   %edx, %edx      
        je      L8             
        addl    %edx, %eax
L8:
        rep
        ret


---


### compiler : `gcc`
### title : `Speed up builtin_popcountll`
### open_at : `2008-04-25T00:34:18Z`
### last_modified_date : `2021-11-28T00:18:14Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=36041
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.2.0`
### severity : `enhancement`
### contents :
The current __builtin_popcountll (and likely __builtin_popcount) are fairly slow as compared to a simple, short C version derived from what can be found in Knuth's recent publications.  The following short function is about 3x as fast as the __builtin version, which runs counter to the idea that __builtin_XXX provides access to implementations that are exemplars for a given platform.

unsigned int popcount64(unsigned long long x)
{
    x = (x & 0x5555555555555555ULL) + ((x >> 1) & 0x5555555555555555ULL);
    x = (x & 0x3333333333333333ULL) + ((x >> 2) & 0x3333333333333333ULL);
    x = (x & 0x0F0F0F0F0F0F0F0FULL) + ((x >> 4) & 0x0F0F0F0F0F0F0F0FULL);
    return (x * 0x0101010101010101ULL) >> 56;
}

This version has the additional benefit that it omits the lookup table that the current "builtin" version uses.

I measured the above function vs. __builtin_popcountll with a loop like the following:

    t1 = clock();
    for (j = 0; j < 1000000; j++)
        for (i = 0; i < 1024; i++)
            pt = popcount64(data[i]);
    t2 = clock();

    printf("popcount64 = %d clocks\n", t2 - t1);

...where data[] is a u64 that's preinitialized.

I'll attach the exact source I used, which also includes two other possible implementations of popcountll.


---


### compiler : `gcc`
### title : `bad code generation with -ftree-vectorize`
### open_at : `2008-04-26T16:25:59Z`
### last_modified_date : `2021-08-23T23:09:05Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=36054
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.3.1`
### severity : `normal`
### contents :
hi all,

(first of all, sorry for this unprofessional bug report)

compiling my application with gcc-4.3 with -O2 -ftree-vectorize, it segfaults. i haven't been able to write a stripped-down test case, but here are the information, that i gathered:

the constructor of the main data structure of my application contains:
0xb5eb02bd <Environment+205>:	movdqa %xmm0,0x1990(%edi)
0xb5eb02c5 <Environment+213>:	movdqa %xmm0,0x19a0(%edi)
0xb5eb02cd <Environment+221>:	movdqa %xmm0,0x19b0(%edi)
0xb5eb02d5 <Environment+229>:	movdqa %xmm0,0x19c0(%edi)
0xb5eb02dd <Environment+237>:	movdqa %xmm0,0x19d0(%edi)
0xb5eb02e5 <Environment+245>:	movdqa %xmm0,0x19e0(%edi)
0xb5eb02ed <Environment+253>:	movdqa %xmm0,0x19f0(%edi)
0xb5eb02f5 <Environment+261>:	movdqa %xmm0,0x1a00(%edi)

where %edi contains the this pointer to the class. the problem is, that the address, that Environment+205 tries to load seems not to be guarrantied to be aligned to a 16 byte boundary. 

in my debugging session, it pointed to 0x8369f58, 0x8369f58+0x1990 is not aligned as required by the movdqa instruction, though ...

i am using gcc-4.3:
Using built-in specs.
Target: i486-linux-gnu
Configured with: ../src/configure linux gnu
Thread model: posix
gcc version 4.3.1 20080401 (prerelease) (Debian 4.3.0-3) 

the command line options are: -g -O3 -march=core2 -mfpmath=sse -msse -ftemplate-depth-4096 -Wnon-virtual-dtor -fPIC 

unfortunately i haven't been able to construct a smaller test-case ... gcc-4.2 works fine for me ...

the preprocessed source file is attached


---


### compiler : `gcc`
### title : `bad choice of loop IVs above -Os on x86`
### open_at : `2008-05-05T02:11:26Z`
### last_modified_date : `2023-06-21T08:05:30Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=36127
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.4.0`
### severity : `enhancement`
### contents :
> /usr/local/gcc44/bin/gcc -v
[..]
gcc version 4.4.0 20080503 (experimental) (GCC)
> gcc -O3 -mfpmath=sse -fno-pic -fno-tree-vectorize -S himenoBMTxps.c

With -O2/-O3, the inner loop in jacobi() in this program ends containing a lot of this:
	movss	_p-4(%edi,%edx,4), %xmm0
	movl	-96(%ebp), %edi
	subss	_p-4(%edi,%edx,4), %xmm0
	movl	-108(%ebp), %edi
	subss	_p-4(%edi,%edx,4), %xmm0
	movl	-92(%ebp), %edi
	addss	_p-4(%edi,%edx,4), %xmm0
	movl	-124(%ebp), %edi

At -O1 or -Os, it instead produces:
	movss	34056(%eax), %xmm0
	subss	33024(%eax), %xmm0
	subss	-33024(%eax), %xmm0
	addss	-34056(%eax), %xmm0

which is much better. On core 2 it claims to be 40% faster at -Os.

IIRC this isn't a problem on x86-64, but IRA+-O3 was much worse again.


---


### compiler : `gcc`
### title : `missed optimistic value-numbering on global vars`
### open_at : `2008-05-09T15:32:07Z`
### last_modified_date : `2021-09-12T12:44:15Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=36188
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.4.0`
### severity : `enhancement`
### contents :
int f(int lay)
{
  static int syncsize, init;
  if (init == 0)
     syncsize = 1344, init = 1;
  return syncsize;
}


store-ccp should handle that.


---


### compiler : `gcc`
### title : `Investigate which tests need -fno-trapping-math`
### open_at : `2008-05-09T16:49:39Z`
### last_modified_date : `2023-08-09T09:47:41Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=36190
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.4.0`
### severity : `enhancement`
### contents :
In a recent change gcc became more strict on where trapping instructions can be placed. They are no longer valid on condexprs. This introduced some regressions. The tests have been changed to use -fno-trapping-math. We should investigate if we could optimize them even with trapping math.

The tests are:
gcc.dg/vect/vect-111.c
gcc.dg/vect/vect-ifcvt-11.c
gcc.dg/vect/vect-ifcvt-12.c
gcc.dg/vect/vect-ifcvt-13.c
gcc.dg/vect/vect-ifcvt-14.c
gcc.dg/vect/vect-ifcvt-15.c


---


### compiler : `gcc`
### title : `vector code is not parallelized`
### open_at : `2008-05-20T19:25:52Z`
### last_modified_date : `2021-11-29T00:06:04Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=36281
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.4.0`
### severity : `enhancement`
### contents :
The testcase of PR36181 should be parallelized after being vectorized.

/* { dg-do compile } */
/* { dg-options "-O3 -ftree-parallelize-loops=2" } */

int foo ()
{
  int i, sum = 0, data[1024];

  for(i = 0; i<1024; i++)
    sum += data[i];

  return sum;
}

The fix for PR36181 was to disable the parallelization of a loop when
one of the phi nodes had a vector type.  This testcase should also be
parallelized.  See also the comments from the fix for PR36181:
http://gcc.gnu.org/ml/gcc-patches/2008-05/msg01217.html


---


### compiler : `gcc`
### title : `missed "inlining" of static untouched variable in linked once function`
### open_at : `2008-05-28T07:41:57Z`
### last_modified_date : `2021-09-12T12:44:54Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=36352
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.3.0`
### severity : `enhancement`
### contents :
While looking into PR 36297, I found this interesting missed optimization, it only happens with linked once functions.  Testcase:
template <int a> int f(void)
{
  static int t = a;
  return t;
}

int g(void)
{
  return f<1>();
}

We should produce return 1 for both functions but currently we reference f<1>::t .


---


### compiler : `gcc`
### title : `folding of conversion for BOOLEAN_TYPE or ENUMERAL_TYPE`
### open_at : `2008-05-30T07:50:15Z`
### last_modified_date : `2021-06-03T02:06:45Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=36384
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.4.0`
### severity : `enhancement`
### contents :
In fold_unary, CASE_CONVERT, the folding of the conversion into a bitwise AND
is performed only for INTEGER_TYPE, while it could very likely be performed
for BOOLEAN_TYPE and ENUMERAL_TYPE as well:

      /* Convert (T)(x & c) into (T)x & (T)c, if c is an integer
	 constants (if x has signed type, the sign bit cannot be set
	 in c).  This folds extension into the BIT_AND_EXPR.
	 ??? We don't do it for BOOLEAN_TYPE or ENUMERAL_TYPE because they
	 very likely don't have maximal range for their precision and this
	 transformation effectively doesn't preserve non-maximal ranges.  */
      if (TREE_CODE (type) == INTEGER_TYPE
	  && TREE_CODE (op0) == BIT_AND_EXPR
	  && TREE_CODE (TREE_OPERAND (op0, 1)) == INTEGER_CST)

The problem is that the transformation doesn't preserve non-maximal ranges for
a given precision and, as a consequence, VRP can draw different conclusions
on each side.

See gnat.dg/bit_packed_array3.adb.


---


### compiler : `gcc`
### title : `Additional instructions in prologue and epilogue.`
### open_at : `2008-06-01T10:46:19Z`
### last_modified_date : `2021-12-20T11:18:06Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=36409
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.3.1`
### severity : `normal`
### contents :
Stack space creation instructions in prologue and epilogue don't get deleted. 

foo:
        sub     sp, sp, #8 --> Unnecessary 
        mov     r3, #0
        add     sp, sp, #8 --> Unnecessary
        str     r3, [r0]


struct Foo {
  int *p;
  int *q;
};

void __attribute__((noinline))
     foo(struct Foo f)
{
  *f.p = 0;
}


This appears to be due to get_frame_size returning the size of the incoming parameters being 8 bytes in the backend .


---


### compiler : `gcc`
### title : `x86 can use x >> -y for x >> 32-y`
### open_at : `2008-06-11T22:52:28Z`
### last_modified_date : `2021-09-20T02:57:49Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=36503
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.4.0`
### severity : `enhancement`
### contents :
> gcc -v
Using built-in specs.
Target: i386-apple-darwin9.2.2
Configured with: ../gcc/configure --prefix=/usr/local/gcc44
--enable-threads=posix --with-arch=core2 --with-tune=core2 --with-gmp=/sw
--with-mpfr=/sw --disable-nls --disable-bootstrap --enable-checking=yes,rtl
--enable-languages=c,c++,objc
Thread model: posix
gcc version 4.4.0 20080611 (experimental) (GCC) 

gcc compiles

int shift32(int i, int n)
{
	return i >> (32 - n);
}

to

_shift32:
        subl    $12, %esp
        movl    $32, %ecx
        subl    20(%esp), %ecx
        movl    16(%esp), %eax
        sarl    %cl, %eax
        addl    $12, %esp
        ret

Since all 286-and-up CPUs only use the low 5 bits of ecx when shifting, this can be:

_shift32:
        movl    8(%esp), %ecx
        movl    4(%esp), %eax
        negl   %ecx
        sarl    %cl, %eax
        ret

This is very common in bitstream readers, where it's used to read the top N bits from a word. ffmpeg already has an inline asm to do it, which I'd like to get rid of.

I'd guess this applies to some other architectures; it probably works on x86-64, but doesn't on PPC.


---


### compiler : `gcc`
### title : `Poor register allocation from IRA`
### open_at : `2008-06-14T06:47:33Z`
### last_modified_date : `2023-05-15T04:47:33Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=36539
### status : `RESOLVED`
### tags : `missed-optimization, ra`
### component : `target`
### version : `4.4.0`
### severity : `enhancement`
### contents :
Using today's IRA branch (r136683), on the attached file.

> gcc -O3 -fno-pic -fomit-frame-pointer -m64 -S cabac-ret.i -fira
_get_cabac:
LFB2:
	pushq	%rbx
LCFI0:
	movl	(%rdi), %eax
	movl	4(%rdi), %r8d
# 16 "cabac-ret.i" 1
	#%ebx %r8d %ax 24(%rdi) %rsi
# 0 "" 2
	movl	%eax, (%rdi)
	movl	%r8d, 4(%rdi)
	movl	%ebx, %eax
	popq	%rbx
	andl	$1, %eax
	ret

with an unnecessary mov %ebx, %eax. Without -fira:
	movl	(%rdi), %r8d
	movl	4(%rdi), %r9d
# 16 "cabac-ret.i" 1
	#%eax %r9d %r8w 24(%rdi) %rsi
# 0 "" 2
	movl	%r8d, (%rdi)
	movl	%r9d, 4(%rdi)
	andl	$1, %eax
	ret

Both allocators don't allocate bit to eax in 32-bit mode, though all other compilers with inline asm support I tried did. gcc 3.3 does, as well, but no other version seemed to.

In this case it's not a problem, since changing the class to "=&a" fixes it, but the function will be inlined a lot and I don't want to put unnecessary constraints on it.


---


### compiler : `gcc`
### title : `store using long array  index not hoisted out of loop`
### open_at : `2008-06-18T00:36:57Z`
### last_modified_date : `2021-12-25T22:24:59Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=36561
### status : `NEW`
### tags : `alias, missed-optimization, testsuite-fail`
### component : `tree-optimization`
### version : `4.4.0`
### severity : `enhancement`
### contents :
Testsuite test  gcc.dg/tree-ssa/loop35.c fails for avr target for test3().

This test uses long array index. Tests with int or char index get hoisted as expected.

void test3(unsigned long b)
{
  unsigned i;

  /* And here.  */
  for (i = 0; i < 100; i++)
    {
      arr[b+8].X += i;
      arr[b+9].X += i;
    }
}

Richard Guenther indicates:
> This is because the alias-oracle for store-motion doesn't handle conversions
> to sizetype well in the offset disambiguation.


---


### compiler : `gcc`
### title : `memset should be optimized into an empty CONSTRUCTOR`
### open_at : `2008-06-22T21:06:12Z`
### last_modified_date : `2021-08-22T00:07:42Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=36602
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.4.0`
### severity : `enhancement`
### contents :
I noticed this while looking into tree-ssa-sccvn.c sources (though I doubt it helps in general really).  But anyways we should optimize the following code into just a "return 0;":
struct f
{
  int t, k;
  int g[1024];
};


int g(void)
{
  struct f a;
  __builtin_memset(&a, 0, sizeof(a));
  return a.t;
}

-- CUT ---
You can see that with the above code we get a zeroing for the struct still.


---


### compiler : `gcc`
### title : `Vectorizer doesn't support  INT<->FP conversions with different size`
### open_at : `2008-07-15T21:41:55Z`
### last_modified_date : `2021-08-16T21:43:04Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=36844
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.4.0`
### severity : `enhancement`
### contents :
Intel AVX has variable vector lengths of 128bit and 256bit.
There are 128bit INT and 256bit FP vector arithmetic operations
as well as asymmetric vector conversion operations:
 
256bit vector (V4DF/V4DI) <-> 256bit vector (D4SI/V4SF)
256bit vector (V8SI) <-> 256bit vecor (V8SF)

The current vectorizer only supports different vector
size based on scalar type. But it doesn't support asymmetric
vector conversion nor different vector size based on
operation. The current AVX branch limits vector size
to 128bit for vectorizer:

/* ??? No autovectorization into MMX or 3DNOW until we can reliably
   place emms and femms instructions.
   FIXME: AVX has 32byte floating point vector operations and 16byte
   integer vector operations.  But vectorizer doesn't support
   different sizes for integer and floating point vectors.  We limit
   vector size to 16byte.  */
#define UNITS_PER_SIMD_WORD(MODE)                                       \
  (TARGET_AVX ? (((MODE) == DFmode || (MODE) == SFmode) ? 16 : 16)      \
              : (TARGET_SSE ? 16 : UNITS_PER_WORD))


---


### compiler : `gcc`
### title : `[4.4 Regression] Creating runtime relocations for code which does not need it`
### open_at : `2008-07-20T18:41:41Z`
### last_modified_date : `2021-09-05T00:29:34Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=36881
### status : `RESOLVED`
### tags : `missed-optimization, rejects-valid`
### component : `tree-optimization`
### version : `4.4.0`
### severity : `normal`
### contents :
Compile gcc.c-torture/execute/20080719-1.c with -O2 -fPIC and you will get:
gcc/gcc/testsuite/gcc.c-torture/execute/20080719-1.c: In function ‘xxx’:
gcc/gcc/testsuite/gcc.c-torture/execute/20080719-1.c:65: error: creating run-time relocation for ‘cfb_tab8_be’
gcc/gcc/testsuite/gcc.c-torture/execute/20080719-1.c:65: error: creating run-time relocation for ‘cfb_tab32’
gcc/gcc/testsuite/gcc.c-torture/execute/20080719-1.c:65: error: creating run-time relocation for ‘cfb_tab32’

This is because of the switch conversion pass which should be disabled for -fPIC on spu-elf.  The runtime loader for spu does not currently support runtime relocations.

If we compile with -O1 -fPIC, these runtime relocations are not created.


---


### compiler : `gcc`
### title : `ifcvt poor optimization`
### open_at : `2008-07-20T19:44:48Z`
### last_modified_date : `2023-05-26T01:18:38Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=36884
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.3.0`
### severity : `normal`
### contents :
If conversion is causing extraordinary bad code for AVR.
This occurs on 4.3 4.4 is no better.

Testcase:

int z;

int foo2(void)
{
  return ( ++z >= 0);
}

Conversion replaces if using store flag. However, there appears to be no account of relative costs and rather bad interactions with mode narrowing and widening

After conversion we have:

z++
Extract upper byte of 'z'
Sign extend
One complement
Shift right 15


RTL prior to ce1 pass:

;; Pred edge  ENTRY [100.0%]  (fallthru)
(note 3 0 2 2 [bb 2] NOTE_INSN_BASIC_BLOCK)

(note 2 3 5 2 NOTE_INSN_FUNCTION_BEG)

(insn 5 2 6 2 test1.c:15 (set (reg:HI 43 [ z ])
        (mem/c/i:HI (symbol_ref:HI ("z") <var_decl 0x7fe000b0 z>) [3 z+0 S2 A8])) 10 {*movhi} (nil))

(insn 6 5 7 2 test1.c:15 (set (reg:HI 41 [ z.5 ])
        (plus:HI (reg:HI 43 [ z ])
            (const_int 1 [0x1]))) 25 {addhi3} (expr_list:REG_DEAD (reg:HI 43 [ z ])
        (nil)))

(insn 7 6 8 2 test1.c:15 (set (mem/c/i:HI (symbol_ref:HI ("z") <var_decl 0x7fe000b0 z>) [3 z+0 S2 A8])
        (reg:HI 41 [ z.5 ])) 10 {*movhi} (nil))

(insn 8 7 9 2 test1.c:15 (set (reg:HI 44)
        (const_int 0 [0x0])) 10 {*movhi} (nil))

(insn 9 8 10 2 test1.c:15 (set (cc0)
        (reg:HI 41 [ z.5 ])) 95 {tsthi} (expr_list:REG_DEAD (reg:HI 41 [ z.5 ])
        (nil)))

(jump_insn 10 9 25 2 test1.c:15 (set (pc)
        (if_then_else (lt (cc0)
                (const_int 0 [0x0]))
            (label_ref 12)
            (pc))) 109 {branch} (expr_list:REG_BR_PROB (const_int 2100 [0x834])
        (nil)))
;; End of basic block 2 -> ( 4 3)
;; lr  out 	 28 [r28] 32 [__SP_L__] 34 [argL] 44
;; live  out 	 28 [r28] 32 [__SP_L__] 34 [argL] 44





RTL after ce1:

(note 2 3 5 2 NOTE_INSN_FUNCTION_BEG)

(insn 5 2 6 2 test1.c:15 (set (reg:HI 43 [ z ])
        (mem/c/i:HI (symbol_ref:HI ("z") <var_decl 0x7fe000b0 z>) [3 z+0 S2 A8])) 10 {*movhi} (nil))

(insn 6 5 7 2 test1.c:15 (set (reg:HI 41 [ z.5 ])
        (plus:HI (reg:HI 43 [ z ])
            (const_int 1 [0x1]))) 25 {addhi3} (expr_list:REG_DEAD (reg:HI 43 [ z ])
        (nil)))

(insn 7 6 8 2 test1.c:15 (set (mem/c/i:HI (symbol_ref:HI ("z") <var_decl 0x7fe000b0 z>) [3 z+0 S2 A8])
        (reg:HI 41 [ z.5 ])) 10 {*movhi} (nil))

(insn 8 7 9 2 test1.c:15 (set (reg:HI 44)
        (const_int 0 [0x0])) 10 {*movhi} (nil))

(insn 9 8 35 2 test1.c:15 (set (cc0)
        (reg:HI 41 [ z.5 ])) 95 {tsthi} (expr_list:REG_DEAD (reg:HI 41 [ z.5 ])
        (nil)))

(insn 35 9 36 2 test1.c:15 (set (reg:QI 49)
        (subreg:QI (reg:HI 41 [ z.5 ]) 1)) 4 {*movqi} (nil))

(insn 36 35 37 2 test1.c:15 (set (reg:HI 48)
        (sign_extend:HI (reg:QI 49))) 84 {extendqihi2} (nil))

(insn 37 36 38 2 test1.c:15 (set (reg:HI 50)
        (not:HI (reg:HI 48))) 82 {one_cmplhi2} (nil))

(insn 38 37 32 2 test1.c:15 (set (reg:HI 44)
        (lshiftrt:HI (reg:HI 50)
            (const_int 15 [0xf]))) 71 {lshrhi3} (nil))

(insn 32 38 33 2 test1.c:16 (set (reg:QI 24 r24)
        (subreg:QI (reg:HI 44) 0)) 4 {*movqi} (nil))

(insn 33 32 23 2 test1.c:16 (set (reg:QI 25 r25 [+1 ])
        (subreg:QI (reg:HI 44) 1)) 4 {*movqi} (expr_list:REG_DEAD (reg:HI 44)
        (nil)))



Final (annotated) code:


  22               	/* prologue: frame size=0 */
  23               	/* prologue end (size=0) */
  24               	.LM2:
  25 0000 8091 0000 		lds r24,z
  26 0004 9091 0000 		lds r25,(z)+1
  27 0008 0196      		adiw r24,1
  28 000a 9093 0000 		sts (z)+1,r25
  29 000e 8093 0000 		sts z,r24
  30 0012 892F      		mov r24,r25
  31 0014 9927      		clr r25  ;SIGN EXTEND
  32 0016 87FD      		sbrc r24,7 ;ditto
  33 0018 9095      		com r25 ; ditto
  34 001a 8095      		com r24 ; ONE'SCOMPLEMENT
  35 001c 9095      		com r25 ; ditto
  36               	.LM3:
  37 001e 8827      		clr r24 ;LSHIFT 15
  38 0020 990F      		lsl r25 ; ditto
  39 0022 881F      		rol r24 ; ditto
  40 0024 9927      		clr r25 ; ditto
  41               	/* epilogue: frame size=0 */
  42 0026 0895      		ret


---


### compiler : `gcc`
### title : `Redundant creation of stack frame on spu-gcc`
### open_at : `2008-07-30T12:17:06Z`
### last_modified_date : `2020-01-18T03:11:29Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=36972
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.4.0`
### severity : `enhancement`
### contents :
Running the testcase from PR33927 on spu-gcc 4.4.0 2008062 generates the following code which contains a redundant creation of stack frame:

test1:
        fa      $3,$3,$4
        stqd    $sp,-48($sp)
        ai      $sp,$sp,-48
        lnop
        ai      $sp,$sp,48
        bi      $lr
        .size   test1, .-test1
        .align  3
        .global test2
        .type   test2, @function
test2:
        fa      $4,$4,$4
        stqd    $sp,-128($sp)
        fa      $3,$3,$3
        ai      $sp,$sp,-128
        ai      $sp,$sp,128
        bi      $lr
        .size   test2, .-test2
        .ident  "GCC: (GNU) 4.4.0 20080629 (experimental)"


Here is again the testcase from PR33297:

#define vector __attribute__((__vector_size__(16) ))

typedef vector float vec_float4;
typedef struct {
        vec_float4 data;
} VecFloat4;

typedef struct {
        vec_float4 a;
        vec_float4 b;
} VecFloat4x2;


VecFloat4 test1(VecFloat4 a, VecFloat4 b)
{
        a.data = a.data+b.data;
        return a;
}


VecFloat4x2 test2(VecFloat4x2 data)
{
        data.a = data.a+data.a;
        data.b = data.b+data.b;
        return data;
}


---


### compiler : `gcc`
### title : `basic-block vectorization misses some unrolled loops`
### open_at : `2008-08-18T15:33:27Z`
### last_modified_date : `2021-02-11T11:10:34Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=37150
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.4.0`
### severity : `enhancement`
### contents :
As pointed out :

http://gcc.gnu.org/ml/gcc/2008-08/msg00290.html

The attached testcase yields (on a core2 duo, gcc trunk):

    gfortran -O3 -ftree-vectorize -ffast-math -march=native test.f90
    time ./a.out

real 0m3.414s

    ifort -xT -O3  test.f90
    time ./a.out

real 0m1.556s

The assembly contains:

        ifort   gfortran
mulpd     140          0
mulsd       0        280


so the reason seems that ifort vectorizes the attached testcase


---


### compiler : `gcc`
### title : `peeling last iteration of a <= loop`
### open_at : `2008-08-26T11:34:06Z`
### last_modified_date : `2021-10-27T04:58:57Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=37239
### status : `ASSIGNED`
### tags : `missed-optimization, patch`
### component : `tree-optimization`
### version : `4.3.2`
### severity : `enhancement`
### contents :
If the condition of the loop is tested within the loop with == or !=, it may be beneficial to peel off the final iteration of the loop by changing the condition to <.

This happens in the attached benchmark's heapsort function where

    while ((maxIdx += maxIdx) <= last) { 
        if (maxIdx != last && numbers[maxIdx] < numbers[maxIdx + 1]) maxIdx++;
        if (tmp >= numbers[maxIdx]) break;
        numbers[top] = numbers[maxIdx];
        top = maxIdx;
    }

can become

    while ((maxIdx += maxIdx) <= last) { 
        if (numbers[maxIdx] < numbers[maxIdx + 1]) maxIdx++;
        if (tmp >= numbers[maxIdx]) break;
        numbers[top] = numbers[maxIdx];
        top = maxIdx;
    }
    if (maxIdx == last && tmp < numbers[maxIdx]) {
        numbers[top] = numbers[maxIdx];
        top = maxIdx;
    }

enabling in turn if-conversion of the first branch.

Performance of the benchmark is (-O3)

    basic               2.990
    peeling only        2.730
    if-conversion only  2.290
    peel+if-convert     2.010   (faster than quicksort!!)

ICC does this optimization.


---


### compiler : `gcc`
### title : `missed FRE opportunity because of signedness of addition`
### open_at : `2008-08-26T11:54:16Z`
### last_modified_date : `2019-08-20T12:03:27Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=37242
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.4.0`
### severity : `enhancement`
### contents :
In the attached code, the if-conversion opportunity in PR37240 does not benefit a Pentium 4.  However, there is another optimization possible on both systems, namely changing

    while ((maxIdx += maxIdx) < last) {
        if (numbers[maxIdx] < numbers[maxIdx + 1]) maxIdx++;
        if (tmp >= numbers[maxIdx]) break;
        numbers[top] = numbers[maxIdx];
        top = maxIdx;
    }

to

    while ((maxIdx += maxIdx) < last) {
        int a = numbers[maxIdx], b = numbers[maxIdx + 1];
        if (a < b) maxIdx++, a = b;
        if (tmp >= a) break;
        numbers[top] = a;
        top = maxIdx;
    }

It seems to me that numbers[maxIdx] is partially redundant (it is available if maxIdx++ is not executed).  If an additional load of numbers[maxIdx + 1] is inserted in the "then" branch, it can also be found to be fully redundant so that copy propagation generates the optimized code.

This gives a ~3% performance increase on i686-pc-linux-gnu for this benchmark.


---


### compiler : `gcc`
### title : `-Os significantly faster than -O2 on test case wiht -funroll-all-loops`
### open_at : `2008-09-01T11:21:32Z`
### last_modified_date : `2021-09-16T22:17:56Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=37312
### status : `UNCONFIRMED`
### tags : `inline-asm, missed-optimization, ra`
### component : `rtl-optimization`
### version : `4.4.0`
### severity : `normal`
### contents :
[component might be wrong]

The appended test case is significantly faster with -Os -funroll-all-loops (~5%) versus -O2 -funroll-all-loops in gcc 4.4 ( gcc version 4.4.0 20080829; that
is shortly after the IRA merge) on a Core2 (Merom) 

In earlier gcc versions they are about the same performance. The -Os improvement
is against all earlier versions (good!) but it should be in -O2 too.

I tried -fno-tree-pre as it was suggested and it didn't make a difference.


---


### compiler : `gcc`
### title : `fast 64-bit divide by constant on 32-bit platform`
### open_at : `2008-09-09T13:57:38Z`
### last_modified_date : `2021-08-15T11:28:58Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=37443
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.2.3`
### severity : `enhancement`
### contents :
consider the code fragment:

uint64_t slow(uint64_t x) {
  return x / 1220703125u;
}

This can be replaced by:

uint64_t fast(uint64_t x) {
  uint32_t a = ((x >> 32) * 1270091284u) >> 32;
  uint32_t b = ((x & 0xffffffffu) * 3777893186u) >> 32;
  return ((x >> 32) * 3777893186ull + a + b) >> 30;
}

The 'fast' code runs 50% faster than 'slow'. However, removing the redundant multiplies (see my earlier bug - fixed in 4.4 trunk) and tidying up storage, I can use the following assembler to run nearly 100% faster than 'slow':

        .p2align 4,,15
.globl _fast
        .def    _fast;  .scl    2;      .type   32;     .endef
_fast:
        pushl   %ebx
        movl    $1270091284, %eax
        mull    12(%esp)
        movl    $-517074110, %eax
        movl    %edx, %ebx
        mull    8(%esp)
        movl    $-517074110, %eax
        movl    %edx, %ecx
        mull    12(%esp)
        addl    %ebx, %ecx
        popl    %ebx
        adcl    $0, %edx
        addl    %ecx, %eax
        adcl    $0, %edx
        shrdl   $30, %edx, %eax
        shrl    $30, %edx
        ret

NOTE: the 2 multipliers are derived using 96-bit arithmetic:

d = 1220703125u

-517074110 = 0xffe12e1342u = (((1u << 94) + d - 1) / d) >> 32

1270091284 = (((1u << 94) + d - 1) / d) & 0xffffffffu


---


### compiler : `gcc`
### title : `Extra addition for doloop in some cases`
### open_at : `2008-09-09T22:03:12Z`
### last_modified_date : `2023-02-13T20:27:00Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=37451
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.4.0`
### severity : `enhancement`
### contents :
Simple testcase:
/* { dg-do compile } */
/* { dg-options "-O2" } */

int f(int l, int *a)
{
  int i;
  for(i = 0;i < l; i++)
    a[i] = i;
  return l;
}

/* We should be able to do this loop without adding -1 to the l
   to get the number of iterations with this loop still doing a do-loop. */
/* The place where we were getting an extra -1 is when converting from 32bits
   to 64bits as the ctr register is used as 64bits on powerpc64. */
/* { dg-final { scan-assembler-not "-1" } } */
/* { dg-final { scan-assembler "bdnz" } } */
/* { dg-final { scan-assembler-times "mtctr" 1 } } */

---- CUT ---
The issue is that we zero extend before correcting the count of the iterations.


---


### compiler : `gcc`
### title : `Move invariant pulls too many cmps out of a loop`
### open_at : `2008-09-10T22:56:49Z`
### last_modified_date : `2023-01-16T02:43:47Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=37471
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.4.0`
### severity : `enhancement`
### contents :
I was looking at some code generation for an internal benchmark when I noticed this.  With the current trunk on powerpc, we get a mfcr which is slow for the cell (and most likely other PPCs too) as we pulled too many cmps with some loops.
A simple example:
int f(int b, int l, int d, int c, int e)
{
  int i = 0;

  for(i = 0;i< l;i ++)
  {
    if (b)
      g();
    if (c)
      g();
    if (d)
      g();
    if (e)
      g();
  }
}


---


### compiler : `gcc`
### title : `~(-2 - a) is not being optimized into a + 1`
### open_at : `2008-09-14T03:35:58Z`
### last_modified_date : `2021-08-03T23:03:50Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=37516
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.4.0`
### severity : `enhancement`
### contents :
I noticed this when looking into PR 34087 with connection of a patch I wrote for loop-doloop.c which is supposed to reduce the number of instructions.
Anyways the following two functions are equivalent but are not optimized that way:
int f(int a)
{
  a = -2 - a;
  return -(a+1);
}

int f1(int a)
{
  return a + 1;
}


---


### compiler : `gcc`
### title : `mfcr is produced when a branch should be done`
### open_at : `2008-09-16T01:43:56Z`
### last_modified_date : `2021-08-22T01:30:11Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=37537
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.4.0`
### severity : `enhancement`
### contents :
Reduced from PR 37536, but this is actually what the user did:

int f(int a, int b, int c)
{
if (a > 0 ? b < c: b > c)
  return a;
else
  return b;
}

This should be able to rewritten as:
int f(int a, int b, int c)
{
  if (a > 0)
  {
    if (b < c)
      return a;
  } else if (b > c)
      return a;

  return b;
}


---


### compiler : `gcc`
### title : `When peeling an ordinary label off a case-table and making it a default label, strip from the end with identical labels.`
### open_at : `2008-10-02T00:30:17Z`
### last_modified_date : `2021-08-29T03:30:00Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=37710
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.4.0`
### severity : `enhancement`
### contents :
See PR 35809, comment #3 <http://gcc.gnu.org/bugzilla/show_bug.cgi?id=35809#c3>:
Looking at assembly-code for
gcc.c-torture/execute/pr35800.c at r140821 reveals that the first case is still
arbitrarily taken as the default, where the last one would have been better as
it's repeated 32 times.

So, when a new default-label is to be picked, use the end with identical labels, and peel all of them off.  If there are no identical labels, use the end which results in the smallest lower end of the case range. (Usually the beginning needs to be added or subtracted in the back-end, so a smaller constant (hopefully zero) usually means a lower cost.


---


### compiler : `gcc`
### title : `Bad store sinking job`
### open_at : `2008-10-12T15:13:31Z`
### last_modified_date : `2023-05-15T04:05:44Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=37810
### status : `NEW`
### tags : `alias, missed-optimization`
### component : `tree-optimization`
### version : `4.4.0`
### severity : `enhancement`
### contents :
The following code snippet:

void g();

struct A {
  int n;
  int m;

  A& operator++(void)
  {
    if (__builtin_expect(n == m, false))
      g();
    else
      ++n;
    return *this;
  }

  A() : n(0), m(0) { }

  friend bool operator!=(A const& a1, A const& a2) { return a1.n != a2.n; }
};

void testfunction(A& iter)
{
  A const end;
  while (iter != end)
    ++iter;
}

Results in the following assembly code, using maximum optimization:

        movl    (%rdi), %eax
        jmp     .L6

.L4:
        cmpl    %eax, 4(%rdi)     // n == m ?
        je      .L8               // unlikely jump
        addl    $1, %eax          // ++n
        movl    %eax, (%rdi)      // *** store result to memory ***
.L6:
        testl   %eax, %eax        // iter != end ?
        jne     .L4               // continue while loop


The storing (back) of %eax to (%rdi) remains inside the inner
loop no matter what I try. It could/should be moved outside
the loop, since nothing inside the L4 loop is accessing (%rdi)
or could possibly be accessing that memory.

This loop has two exits: below the last jne .L4, and the
jump to .L8. The store could be sinked to both exits.
This grows the code, but it seems reasonable to do for
a loop with a very small body, especially if one of the
exits is marked as unlikely :p.


---


### compiler : `gcc`
### title : `[11/12/13/14 Regression] SSA names causing register pressure; unnecessarily many simultaneously "live" names.`
### open_at : `2008-10-25T20:06:32Z`
### last_modified_date : `2023-07-07T10:29:02Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=37916
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.3.3`
### severity : `normal`
### contents :
The attached preprocessed code in the first attachment is that of the adler32 function in zlib-1.1.3.  It comes highest in the profile of a zlib-based performance regression test (the "example" program with no parameters).
I'm attaching the assembly code corresponding to gcc-3.2.1 for cris-axis-elf with -O2 -march=v10 -fno-gcse -fno-reorder-blocks (the latter options being the default in our local distribution) as well as the versions for the 4.3 branch at 141344 and trunk at 141361 with the same options.  Note the larger stack frames for the newer versions, as well as larger code that uses all available registers and then some stack slots for the additive sums, where two registers would have been enough.

While SSA generates lots of "names", IIUC they should have been collapsed before outof-ssa.  It does to some extent, if the uses and the definitions are close enough.  Looking at the tree-dumps, it's one pass that moved all the uses away from the definitions, tree-reassoc, and no pass later that moved them "back"; in particular TER (part of outof-ssa) did not.  Adding the option -fno-tree-reassoc gets rid of most of the regression for this code (and others).

Having TER changed to, or adding a subpass of outof-ssa, that moves each use back to its definition, would seem like a better solution than shutting off tree-reassoc.

This is also a good example of missed post-increment opportunities (all versions); instead of increasing offsets from a base, there should have been a single post-incremented register.


---


### compiler : `gcc`
### title : `static initialisation through pointer deferred until run time`
### open_at : `2008-10-29T10:25:41Z`
### last_modified_date : `2021-02-26T04:27:17Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=37949
### status : `SUSPENDED`
### tags : `missed-optimization`
### component : `c++`
### version : `4.2.4`
### severity : `enhancement`
### contents :
Given various methods for determining byte order on different platforms, the following can be used in C++ to find the byte order across platforms.

  static const uint32_t bytes = 0x03020100ul;
  static const unsigned lo = *(const unsigned char*)&bytes;

Unfortunately, the value of 'lo' is determined at pre-run rather than at compile time.

It would be useful if the compiler could determine the value of 'lo' so as to eliminate constant logical tests and jumps.


---


### compiler : `gcc`
### title : `GCC Overlooks Logical Operation Optimizations ?`
### open_at : `2008-10-31T12:02:35Z`
### last_modified_date : `2021-11-28T05:06:13Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=37979
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.2.3`
### severity : `enhancement`
### contents :
gcc looks like it's omitting a simple optimization which can be done on logical operations.

/* Command line and output on a linux host */
engin@engin-desktop:~$ gcc -o test test.c -Os && ls -l test
-rwxr-xr-x 1 engin engin 6461 2008-10-31 12:26 test
 
engin@engin-desktop:~$ gcc -o test test.c -Os -DHAND_OPTIMIZED && ls -l test
-rwxr-xr-x 1 engin engin 6365 2008-10-31 12:26 test
 
engin@engin-desktop:~$ gcc -v
Using built-in specs.
Target: i486-linux-gnu
Configured with: ../src/configure -v --enable-languages=c,c++,fortran,objc,obj-c++,treelang --prefix=/usr --enable-shared --with-system-zlib --libexecdir=/usr/lib --without-included-gettext --enable-threads=posix --enable-nls --with-gxx-include-dir=/usr/include/c++/4.2 --program-suffix=-4.2 --enable-clocale=gnu --enable-libstdcxx-debug --enable-objc-gc --enable-mpfr --enable-targets=all --enable-checking=release --build=i486-linux-gnu --host=i486-linux-gnu --target=i486-linux-gnu
Thread model: posix
gcc version 4.2.3 (Ubuntu 4.2.3-2ubuntu7

/* Command line and ouput on cygwin */

Engin@Engin-Dell /cygdrive/c/Users/Engin/Code/mmc
$ gcc -o test test.c -Os && ls -l test
-rwxr-xr-x 1 Engin None 9068 Oct 31 13:42 test
 
Engin@Engin-Dell /cygdrive/c/Users/Engin/Code/mmc
$ gcc -o test test.c -Os -DHAND_OPTIMIZED&& ls -l test
-rwxr-xr-x 1 Engin None 8556 Oct 31 13:43 test
 
Engin@Engin-Dell /cygdrive/c/Users/Engin/Code/mmc
$ gcc -v
Reading specs from /usr/lib/gcc/i686-pc-cygwin/3.4.4/specs
Configured with: /usr/build/package/orig/test.respin/gcc-3.4.4-3/configure --verbose --prefix=/usr --exec-pref
ix=/usr --sysconfdir=/etc --libdir=/usr/lib --libexecdir=/usr/lib --mandir=/usr/share/man --infodir=/usr/share
/info --enable-languages=c,ada,c++,d,f77,pascal,java,objc --enable-nls --without-included-gettext --enable-ver
sion-specific-runtime-libs --without-x --enable-libgcj --disable-java-awt --with-system-zlib --enable-interpre
ter --disable-libgcj-debug --enable-threads=posix --enable-java-gc=boehm --disable-win32-registry --enable-sjl
j-exceptions --enable-hash-synchronization --enable-libstdcxx-debug
Thread model: posix
gcc version 3.4.4 (cygming special, gdc 0.12, using dmd 0.125)


/************* CODE ******************/
volatile int* foo = (volatile int*)0x23232322;
 
 
int
main(void)
{
	int a, b, c, d, e, f, g, h, z = 0;
	a = *foo;
	b = *foo;
	c = *foo;
	d = *foo;
	e = *foo;
	f = *foo;
	g = *foo;
	h = *foo;
 
#ifndef HAND_OPTIMIZED
 
	if ( 
		(f && c && b && a) || 
		(f && e && d && a) || 
		(f && e && h && a) || 
		(g && c && b && a) || 
		(g && e && d && a) || 
		(g && e && h && a) 
	   )
#else
	if ((f||g) && a && ( (b&&c) || ((d||h)&& e)))
#endif
	{
		z= a + b + c;
		h=12;  
		d= h + b + c;
		e=45;  
	}
 
 
	e=z*2+d+a;
	*foo = e;
 
	while(1)
	{
		*foo = e;
	}
 
}


---


### compiler : `gcc`
### title : `suboptimal code for (a && b || !a && !b)`
### open_at : `2008-11-15T00:06:31Z`
### last_modified_date : `2022-12-19T20:57:21Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=38126
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.3.0`
### severity : `enhancement`
### contents :
I would expect gcc to generate comparable code for both functions below, or perhaps even better code for foo() than for bar() since the code in foo() is likely to be more common than the equivalent code in bar(). However, the code produced for foo() is suboptimal in comparison to the code for bar(). In my timings on x86 with gcc 4.3.0 at -O2, foo() appears to run about 5% slower than bar().

$ cat t.c && gcc -S -O2 t.c && cat t.s
int foo (int *a, int *b) { return a && b || !a && !b; }
int bar (int *a, int *b) { return !!a == !!b; }
        .file   "t.c"
        .text
        .p2align 4,,15
.globl foo
        .type   foo, @function
foo:
.LFB2:
        testq   %rdi, %rdi
        je      .L2
        testq   %rsi, %rsi
        movl    $1, %eax
        je      .L2
        rep
        ret
        .p2align 4,,10
        .p2align 3
.L2:
        testq   %rdi, %rdi
        sete    %al
        testq   %rsi, %rsi
        sete    %dl
        andl    %edx, %eax
        movzbl  %al, %eax
        ret
.LFE2:
        .size   foo, .-foo
        .p2align 4,,15
.globl bar
        .type   bar, @function
bar:
.LFB3:
        testq   %rdi, %rdi
        sete    %al
        testq   %rsi, %rsi
        setne   %dl
        xorl    %edx, %eax
        movzbl  %al, %eax
        ret
.LFE3:
        .size   bar, .-bar
        .section        .eh_frame,"a",@progbits
.Lframe1:
        .long   .LECIE1-.LSCIE1
.LSCIE1:
        .long   0x0
        .byte   0x1
        .string "zR"
        .uleb128 0x1
        .sleb128 -8
        .byte   0x10
        .uleb128 0x1
        .byte   0x3
        .byte   0xc
        .uleb128 0x7
        .uleb128 0x8
        .byte   0x90
        .uleb128 0x1
        .align 8
.LECIE1:
.LSFDE1:
        .long   .LEFDE1-.LASFDE1
.LASFDE1:
        .long   .LASFDE1-.Lframe1
        .long   .LFB2
        .long   .LFE2-.LFB2
        .uleb128 0x0
        .align 8
.LEFDE1:
.LSFDE3:
        .long   .LEFDE3-.LASFDE3
.LASFDE3:
        .long   .LASFDE3-.Lframe1
        .long   .LFB3
        .long   .LFE3-.LFB3
        .uleb128 0x0
        .align 8
.LEFDE3:
        .ident  "GCC: (GNU) 4.3.0 20080428 (Red Hat 4.3.0-8)"
        .section        .note.GNU-stack,"",@progbits


---


### compiler : `gcc`
### title : `[11/12/13/14 Regression] speed regression with many loop invariants`
### open_at : `2008-11-15T15:54:51Z`
### last_modified_date : `2023-07-07T10:29:06Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=38134
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.4.0`
### severity : `normal`
### contents :
the attached program, a simdfied version of the tanf function, shows a 20% performance regression from gcc-4.3 to gcc-4.4:

the compared compilers are
g++-4.3
Using built-in specs.
Target: x86_64-linux-gnu
Configured with: ../src/configure -v --with-pkgversion='Ubuntu 4.3.2-1ubuntu11' --with-bugurl=file:///usr/share/doc/gcc-4.3/README.Bugs --enable-languages=c,c++,fortran,objc,obj-c++ --prefix=/usr --enable-shared --with-system-zlib --libexecdir=/usr/lib --without-included-gettext --enable-threads=posix --enable-nls --with-gxx-include-dir=/usr/include/c++/4.3 --program-suffix=-4.3 --enable-clocale=gnu --enable-libstdcxx-debug --enable-objc-gc --enable-mpfr --enable-checking=release --build=x86_64-linux-gnu --host=x86_64-linux-gnu --target=x86_64-linux-gnu
Thread model: posix
gcc version 4.3.2 (Ubuntu 4.3.2-1ubuntu11) 

and

Using built-in specs.
Target: x86_64-linux-gnu
Configured with: ../src/configure -v --with-pkgversion='Ubuntu 20081024-0ubuntu1' --with-bugurl=file:///usr/share/doc/gcc-snapshot/README.Bugs --enable-languages=c,c++,java,fortran,objc,obj-c++,ada --prefix=/usr/lib/gcc-snapshot --enable-shared --with-system-zlib --disable-nls --enable-clocale=gnu --enable-libstdcxx-debug --enable-java-awt=gtk --enable-gtk-cairo --disable-plugin --with-java-home=/usr/lib/gcc-snapshot --enable-java-home --with-jvm-root-dir=/usr/lib/gcc-snapshot/jvm --with-jvm-jar-dir=/usr/lib/gcc-snapshot/jvm-exports --with-ecj-jar=/usr/share/java/eclipse-ecj.jar --enable-objc-gc --enable-mpfr --disable-werror --build=x86_64-linux-gnu --host=x86_64-linux-gnu --target=x86_64-linux-gnu
Thread model: posix
gcc version 4.4.0 20081024 (experimental) [trunk revision 141342] (Ubuntu 20081024-0ubuntu1) 

the interesting part is the inner loop of the bench_1_simd function. 
gcc-4.4 generates:

.L54:
	movaps	in(%rax), %xmm0
	movdqa	%xmm14, %xmm3
	addl	$4, %edx
	pand	%xmm0, %xmm3
#APP
# 325 "benchmarks/../source/dsp/../../libs/libsimdmath/lib/sincosf4.h" 1
	xorps %xmm3, %xmm0
# 0 "" 2
#NO_APP
	movaps	%xmm0, %xmm4
	movaps	%xmm0, %xmm15
	mulps	%xmm13, %xmm4
#APP
# 328 "benchmarks/../source/dsp/../../libs/libsimdmath/lib/sincosf4.h" 1
	cvttps2dq %xmm4, %xmm4
# 0 "" 2
#NO_APP
	movdqa	%xmm4, %xmm1
	pand	%xmm12, %xmm1
	paddd	%xmm1, %xmm4
#APP
# 331 "benchmarks/../source/dsp/../../libs/libsimdmath/lib/sincosf4.h" 1
	cvtdq2ps  %xmm4, %xmm1
# 0 "" 2
#NO_APP
	pand	.LC15(%rip), %xmm4
	movaps	%xmm1, %xmm2
	psrld	$1, %xmm4
	mulps	%xmm11, %xmm2
	subps	%xmm2, %xmm15
	movaps	%xmm15, %xmm2
	movaps	%xmm1, %xmm15
	mulps	%xmm9, %xmm1
	mulps	%xmm10, %xmm15
	subps	%xmm15, %xmm2
	movaps	%xmm8, %xmm15
	subps	%xmm1, %xmm2
	cmpltps	%xmm0, %xmm15
	movaps	%xmm2, %xmm1
	mulps	%xmm2, %xmm1
	movaps	%xmm1, %xmm0
	mulps	%xmm7, %xmm0
	addps	.LC10(%rip), %xmm0
	mulps	%xmm1, %xmm0
	addps	.LC11(%rip), %xmm0
	mulps	%xmm1, %xmm0
	addps	.LC12(%rip), %xmm0
	mulps	%xmm1, %xmm0
	addps	.LC13(%rip), %xmm0
	mulps	%xmm1, %xmm0
	addps	.LC14(%rip), %xmm0
	mulps	%xmm1, %xmm0
	movdqa	%xmm5, %xmm1
	mulps	%xmm2, %xmm0
	psubd	%xmm4, %xmm1
	addps	%xmm2, %xmm0
	movdqa	%xmm1, %xmm4
#APP
# 342 "benchmarks/../source/dsp/../../libs/libsimdmath/lib/sincosf4.h" 1
	andps %xmm15, %xmm0
# 0 "" 2
#NO_APP
	movaps	.LC16(%rip), %xmm1
#APP
# 343 "benchmarks/../source/dsp/../../libs/libsimdmath/lib/sincosf4.h" 1
	andnps %xmm2, %xmm15
# 0 "" 2
#NO_APP
	movaps	%xmm6, %xmm2
#APP
# 344 "benchmarks/../source/dsp/../../libs/libsimdmath/lib/sincosf4.h" 1
	orps  %xmm15, %xmm0
# 0 "" 2
#NO_APP
	addps	%xmm0, %xmm1
	divps	%xmm1, %xmm2
	movaps	%xmm2, %xmm1
#APP
# 145 "benchmarks/../source/dsp/../../libs/libsimdmath/lib/simdconst.h" 1
	andps %xmm4, %xmm1
# 0 "" 2
# 146 "benchmarks/../source/dsp/../../libs/libsimdmath/lib/simdconst.h" 1
	andnps %xmm0, %xmm4
# 0 "" 2
#NO_APP
	movaps	%xmm1, %xmm0
#APP
# 147 "benchmarks/../source/dsp/../../libs/libsimdmath/lib/simdconst.h" 1
	orps  %xmm4, %xmm0
# 0 "" 2
# 349 "benchmarks/../source/dsp/../../libs/libsimdmath/lib/sincosf4.h" 1
	xorps %xmm3, %xmm0
# 0 "" 2
#NO_APP
	movaps	%xmm0, out(%rax)
	addq	$16, %rax
	cmpl	%edi, %edx
	jne	.L54

while gcc-4.3 generates:
.L48:
	movaps	in(%rax), %xmm2
	movdqa	.LC2(%rip), %xmm5
	movaps	.LC3(%rip), %xmm0
	pand	%xmm2, %xmm5
	movdqa	.LC4(%rip), %xmm4
	movaps	.LC5(%rip), %xmm1
	addl	$4, %edx
#APP
# 325 "benchmarks/../source/dsp/../../libs/libsimdmath/lib/sincosf4.h" 1
	xorps %xmm5, %xmm2
# 0 "" 2
#NO_APP
	mulps	%xmm2, %xmm0
	movaps	%xmm2, %xmm3
#APP
# 328 "benchmarks/../source/dsp/../../libs/libsimdmath/lib/sincosf4.h" 1
	cvttps2dq %xmm0, %xmm0
# 0 "" 2
#NO_APP
	pand	%xmm0, %xmm4
	paddd	%xmm0, %xmm4
#APP
# 331 "benchmarks/../source/dsp/../../libs/libsimdmath/lib/sincosf4.h" 1
	cvtdq2ps  %xmm4, %xmm0
# 0 "" 2
#NO_APP
	pand	%xmm9, %xmm4
	mulps	%xmm0, %xmm1
	psrld	$1, %xmm4
	subps	%xmm1, %xmm3
	movaps	.LC6(%rip), %xmm1
	mulps	%xmm0, %xmm1
	mulps	.LC7(%rip), %xmm0
	subps	%xmm1, %xmm3
	subps	%xmm0, %xmm3
	movaps	.LC8(%rip), %xmm0
	movaps	%xmm3, %xmm1
	cmpltps	%xmm2, %xmm0
	mulps	%xmm3, %xmm1
	movaps	%xmm0, %xmm2
	movaps	%xmm1, %xmm0
	mulps	%xmm15, %xmm0
	addps	%xmm14, %xmm0
	mulps	%xmm1, %xmm0
	addps	%xmm13, %xmm0
	mulps	%xmm1, %xmm0
	addps	%xmm12, %xmm0
	mulps	%xmm1, %xmm0
	addps	%xmm11, %xmm0
	mulps	%xmm1, %xmm0
	addps	%xmm10, %xmm0
	mulps	%xmm1, %xmm0
	mulps	%xmm3, %xmm0
	addps	%xmm3, %xmm0
#APP
# 342 "benchmarks/../source/dsp/../../libs/libsimdmath/lib/sincosf4.h" 1
	andps %xmm2, %xmm0
# 0 "" 2
# 343 "benchmarks/../source/dsp/../../libs/libsimdmath/lib/sincosf4.h" 1
	andnps %xmm3, %xmm2
# 0 "" 2
#NO_APP
	movaps	%xmm7, %xmm3
#APP
# 344 "benchmarks/../source/dsp/../../libs/libsimdmath/lib/sincosf4.h" 1
	orps  %xmm2, %xmm0
# 0 "" 2
#NO_APP
	movdqa	%xmm6, %xmm2
	movaps	%xmm0, %xmm1
	psubd	%xmm4, %xmm2
	addps	%xmm8, %xmm1
	divps	%xmm1, %xmm3
	movaps	%xmm3, %xmm1
#APP
# 145 "benchmarks/../source/dsp/../../libs/libsimdmath/lib/simdconst.h" 1
	andps %xmm2, %xmm1
# 0 "" 2
# 146 "benchmarks/../source/dsp/../../libs/libsimdmath/lib/simdconst.h" 1
	andnps %xmm0, %xmm2
# 0 "" 2
# 147 "benchmarks/../source/dsp/../../libs/libsimdmath/lib/simdconst.h" 1
	orps  %xmm2, %xmm1
# 0 "" 2
# 349 "benchmarks/../source/dsp/../../libs/libsimdmath/lib/sincosf4.h" 1
	xorps %xmm5, %xmm1
# 0 "" 2
#NO_APP
	movaps	%xmm1, out(%rax)
	addq	$16, %rax
	cmpl	%edi, %edx
	jne	.L48

the code generated by gcc-4.4 requires more memory access. the code was generated with the flags -O3 -march=core2. while the assembly code is generated for the x86_64 architecture, similar results can be seen with x86 code (4.4 is about 14% slower than 4.3)


---


### compiler : `gcc`
### title : `branch optimisation generates worse code`
### open_at : `2008-11-21T06:04:33Z`
### last_modified_date : `2022-11-19T22:44:33Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=38209
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.3.1`
### severity : `enhancement`
### contents :
Test code:

register unsigned char val asm("r4");

void negate(void)
{
    if (val)
        val = ~val;
    else
        val = ~val;
}

Code generated with -Os

.global negate
        .type   negate, @function
negate:
/* prologue: function */
/* frame size = 0 */
        tst r4
        breq .L2
        com r4
        ret
.L2:
        clr r4
        dec r4
        ret
        .size   negate, .-negate

In the "else" branch gcc knows that r4 is zero, and that it should change to 0xff - taking this approach generates longer code than in the first branch.

The same applies when operations like !, ++, -- are used.


---


### compiler : `gcc`
### title : `gcc.dg/tree-ssa/vrp47.c fails on m68k`
### open_at : `2008-11-21T17:15:13Z`
### last_modified_date : `2021-07-29T01:06:23Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=38219
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.4.0`
### severity : `normal`
### contents :
The gcc.dg/tree-ssa/vrp47.c test case fails on powerpc apple darwin as follows...

Executing on host: /sw/src/fink.build/gcc44-4.3.999-20081120/darwin_objdir/gcc/xgcc -B/sw/src/fink.build/gcc44-4.3.999-20081120/darwin_objdir/gcc/ /sw/src/fink.build/gcc44-4.3.999-20081120/gcc-4.4-20081120/gcc/testsuite/gcc.dg/tree-ssa/vrp47.c   -O2 -fdump-tree-vrp -fdump-tree-dom -S  -o vrp47.s    (timeout = 300)
PASS: gcc.dg/tree-ssa/vrp47.c (test for excess errors)
FAIL: gcc.dg/tree-ssa/vrp47.c scan-tree-dump-times vrp1 "[xy][^ ]* !=" 0
FAIL: gcc.dg/tree-ssa/vrp47.c scan-tree-dump-times dom1 "x[^ ]* & y" 1
XFAIL: gcc.dg/tree-ssa/vrp47.c scan-tree-dump-times vrp1 "x[^ ]* & y" 1
PASS: gcc.dg/tree-ssa/vrp47.c scan-tree-dump-times vrp1 "x[^ ]* [|] y" 1
PASS: gcc.dg/tree-ssa/vrp47.c scan-tree-dump-times vrp1 "x[^ ]* \^ 1" 1


---


### compiler : `gcc`
### title : `tree_forwarder_block_p says no to first basic block`
### open_at : `2008-11-25T19:10:45Z`
### last_modified_date : `2023-08-27T04:55:52Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=38264
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.4.0`
### severity : `enhancement`
### contents :
tree_forwarder_block_p has

  if (find_edge (ENTRY_BLOCK_PTR, bb))
    return false;

without explanation.  This test was added by you, Jeff - do you remember why?

Removing this check triggers some ICEs in the testsuite because remove_bb
(called from remove_forwarder_block) unconditionally moves labels from the
removed block to prev_bb (yuck!) - which is of course invalid if that happens
to be the entry bb.  Luckily remove_forwarder_block already contains code
to do the label-move job itself - it is just conditional on seen abnormal
incoming edges.  Enabling this code to run by default causes a bootstrap
comparison failure though.


---


### compiler : `gcc`
### title : `rtl epilogues worse than non-rtl epilogues for dbr scheduling`
### open_at : `2008-11-25T19:32:37Z`
### last_modified_date : `2021-09-12T04:33:45Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=38267
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.2.1`
### severity : `normal`
### contents :
The rtl epilogues are inserted after the USE which indicates where
the return value is.  As a result, an instruction that calculates the
return value cannot be placed in the delay slot of the return
instruction.  That is something that we did get right when we
had non-rtl epilogues - the epilogue_delay could well contain an insn to calculate
the function result.


---


### compiler : `gcc`
### title : `moving the allocation of temps out of loops.`
### open_at : `2008-11-29T16:15:35Z`
### last_modified_date : `2023-07-22T03:06:23Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=38318
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.4.0`
### severity : `enhancement`
### contents :
consider the following source and timings, were a natural form of a subroutine S1, and two hand optimized forms are timed:

> cat test.f90
SUBROUTINE S1(N,A)
 REAL :: A(3)
 DO I=1,N
   CALL S2(-A)
 ENDDO
END SUBROUTINE

SUBROUTINE S1_opt1(N,A)
 REAL :: A(3)
 REAL, ALLOCATABLE :: B(:)
 ALLOCATE(B(SIZE(A,1)))
 DO I=1,N
   B=-A
   CALL S2(B)
 ENDDO
END SUBROUTINE


SUBROUTINE S1_opt2(N,A)
 REAL :: A(3),B(3)
 DO I=1,N
   B=-A
   CALL S2(B)
 ENDDO
END SUBROUTINE

> cat main.f90

SUBROUTINE S2(A)
 REAL :: A(*),D
 COMMON /F/D
 D=D+A(1)+A(2)+A(3)
END SUBROUTINE

INTEGER, PARAMETER :: N=100000
REAL :: A(3),T1,T2,T3,T4,D
COMMON /F/D
D=0.0
A=0.0
CALL CPU_TIME(T1)
DO I=1,10000
  CALL S1(N,A)
ENDDO
CALL CPU_TIME(T2)
DO I=1,10000
  CALL S1_opt1(N,A)
ENDDO
CALL CPU_TIME(T3)
DO I=1,10000
  CALL S1_opt2(N,A)
ENDDO
CALL CPU_TIME(T4)

write(6,*) "Default [s]:",T2-T1
write(6,*) "OPT1 [s]:",T3-T2
write(6,*) "OPT2 [s]:",T4-T3
write(6,*) D
END

gfortran-4.4 -O3 test.f90 main.f90
 Default [s]:   18.293142
 OPT1 [s]:   6.2603912
 OPT2 [s]:   6.2563915

ifort -O3 test.f90 main.f90
 Default [s]:   6.256391
 OPT1 [s]:   6.252390
 OPT2 [s]:   6.256390

so, gfortran by default is about 3x slower than ifort, which by default moves the generation of the temporaries out of the loop. 

FYI, allowing for multi file IPO, I hope LTO gets that far...

ifort -O3 -fast test.f90 main.f90 (includes ipo)
 Default [s]:   3.752234
 OPT1 [s]:   1.276080
 OPT2 [s]:   3.752234


---


### compiler : `gcc`
### title : `PRE missing a load PRE which causes a loop to have two BBs`
### open_at : `2008-12-11T23:21:11Z`
### last_modified_date : `2021-08-22T04:04:32Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=38497
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.2.0`
### severity : `enhancement`
### contents :
Testcase:
void DoHuffIteration(int);
int f(int *a)
{
  int i;
  int plaintextlen=*a;
  for(i = 0; i< 10000; i++)
     DoHuffIteration(*a);
return *a - plaintextlen;
}

--- CUT ---
There is a load of *a after that loop even though we could have placed the load inside the loop after the call.


---


### compiler : `gcc`
### title : `missed opportunity to use adc (conditional store)`
### open_at : `2008-12-16T21:55:01Z`
### last_modified_date : `2021-08-05T23:49:02Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=38544
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.4.0`
### severity : `enhancement`
### contents :
The optimizer at -O3 for x86_64 finds opportunities to generate the "adc" (add with carry) instruction to avoid a conditional branch.  However, the dst of the adc can only be in a register.  The optimizer misses a chance to use "adc" with the destination in memory, and will instead use a conditional branch in a straightforward manner.  The following program shows that foo1 uses adc, but foo0 does not.

Although I haven't tested this, I'm sure that the other 3 possibilities in this family (involving sbb and/or different literal values to add/subtract) will also not find the opportunity to do a memory update with adc.

extern void consumep(int *);
extern void consume(int);
void foo0(unsigned a, unsigned b, int *victim)
{
  if (a > b) { (*victim)++; }
  consumep(victim);
}
void foo1(unsigned a, unsigned b, int victim)
{
  if (a > b) { victim++; }
  consume(victim);
}


---


### compiler : `gcc`
### title : `[arm] -mthumb generates sub-optimal prolog/epilog`
### open_at : `2008-12-18T17:19:50Z`
### last_modified_date : `2019-05-17T22:24:03Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=38570
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `unknown`
### severity : `enhancement`
### contents :
When generating relatively trivial leaf-functions that contains local branch instructions (not calling sub functions), the compiler generates unnecessary PUSH/POP instructions to store the LR on the stack.

Richard Earnshaw [Richard.Earnshaw@arm.com] has confirmed that this is a bug and requested that I raise it in bugzilla.

In the attached example (test.c), it can be seen in the generated assembly file (test-prologue-thumb.s) that all of the wcstrlenN() functions have unnecessary 'push{lr}/pop{pc}' which could be replaced by just doing 'bx lr' in the epilog.

Command line was:

arm-none-eabi-gcc -mthumb -mno-thumb-interwork test.c -Os -S -o test-prologue-thumb.s


---


### compiler : `gcc`
### title : `Optimize memmove / memcmp combination`
### open_at : `2008-12-21T10:46:10Z`
### last_modified_date : `2020-11-11T09:41:05Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=38592
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.4.0`
### severity : `enhancement`
### contents :
$ cat foo.f90
program main
  character(len=3) :: a
  a = 'yes'
  print *,'yes' == a
end program main
$ gfortran -fdump-tree-optimized -O3 -S foo.f90
$ grep compare_string foo.s
        call    _gfortran_compare_string


---


### compiler : `gcc`
### title : `gcc.target/mips/mips16e-extends.c fails for -mlong64`
### open_at : `2008-12-21T13:48:20Z`
### last_modified_date : `2020-02-25T10:12:59Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=38595
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.4.0`
### severity : `normal`
### contents :
mipsisa64-elf-gcc -O2 -S gcc.target/mips/mips16e-extends.c -DMIPS16='__attribute__((mips16))' -msoftf-float

The output code does not contain the expected ZEB and ZEH instructions.  (The options here select EABI64, but the same problem occurs with other -mlong64 ABIs.)

The problem is that we don't have MIPS16e equivalents of the non-MIPS16 extend-truncate combiner patterns.

I'm filing this for 4.5 or later; it isn't something we'd fix in 4,4 or earlier.


---


### compiler : `gcc`
### title : `trivial try/catch statement not eliminated`
### open_at : `2008-12-29T00:47:30Z`
### last_modified_date : `2021-07-23T00:12:12Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=38658
### status : `NEW`
### tags : `missed-optimization`
### component : `c++`
### version : `4.3.1`
### severity : `enhancement`
### contents :
I would expect a C++ compiler to generate optimal and equivalently efficient
code for both of the functions below. gcc 4.3 generates much worse code for
bar() than for foo() even at -O3.

int foo () { return 1; }
int bar () { try { throw 1; } catch (int i) { return i; } }


---


### compiler : `gcc`
### title : `[11/12/13/14 Regression] huge performance regression on EEMBC bitmnp01`
### open_at : `2009-01-09T15:45:48Z`
### last_modified_date : `2023-07-07T10:29:08Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=38785
### status : `ASSIGNED`
### tags : `missed-optimization, patch`
### component : `tree-optimization`
### version : `4.4.0`
### severity : `normal`
### contents :
After merging ARCompact support into gcc 4.4.0 20081210, we noticed that
cycle count is up by 155% compared to gcc 4.2.1 for ARC700 on the eembc bitmnp01
benchmark.  There are long sequences of putting integer constants on the stack,
and shufflink stack locations / registers around in the inner loop.
The *084t.pre dump shows that partial redundancy elimination / constant
propagation has gone berserk, calculating combined ORed values through
all the paths of the sequence of ifs in the main loop.

I've built an i686-pc-linux-gnu compiler from the same sources and
verified that the 084t.pre dump and the .s file show the same bogosity.
(Using options -O3 -fomit-frame-pointer -gstabs -fdump-tree-all. )
I've confirmed the same findings for i686-pc-linux-gnu with a pristine
svn snapshot from today, Revision: 143207.


---


### compiler : `gcc`
### title : `loop iv detection failure`
### open_at : `2009-01-15T18:24:13Z`
### last_modified_date : `2021-11-28T04:31:48Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=38856
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.3.2`
### severity : `normal`
### contents :
I apologize if it is a well disguised feature, but I am forced to consider this being a performance regression/bug. 

In the following trivial example:
void
VecADD(
    long long *In1,
    long long *In2,
    long long *Out,
    unsigned int samples
){
  int i;
  for (i = 0; i < samples; i++) {
    Out[i] = In1[i] + In2[i];
  }
}

there is an implicit imprecision in the way C is used - type of 'samples' is unsigned, while type of 'i' is signed. 

The problem on the high level - induction variable analysis fails for this loop, which impairs further tree level loop optimizations from functioning properly (including autoincrement). In my port performance is off by 50% for this loop. GCC 3.4.6 was able to handle this situation fine. 

What I believe to be the problem at the lowest level is a non-minimal (or overly restrictive) SSA representation right before the iv detection:

VecADD (In1, In2, Out, samples)
{
  int i;
  long long int D.1857;
  long long int D.1856;
  long long int * D.1855;
  long long int D.1854;
  long long int * D.1853;
  long long int * D.1852;
  unsigned int D.1851;
  unsigned int i.0;

<bb 2>:

<bb 6>:
  # i_10 = PHI <0(2)>
  i.0_5 = (unsigned int) i_10;
  if (i.0_5 < samples_4(D))
    goto <bb 3>;
  else
    goto <bb 5>;

<bb 3>:
  # i.0_9 = PHI <i.0_3(4), i.0_5(6)>
  # i_14 = PHI <i_1(4), i_10(6)>
  D.1851_6 = i.0_9 * 8;
  D.1852_8 = Out_7(D) + D.1851_6;
  D.1853_12 = In1_11(D) + D.1851_6;
  D.1854_13 = *D.1853_12;
  D.1855_17 = In2_16(D) + D.1851_6;
  D.1856_18 = *D.1855_17;
  D.1857_19 = D.1854_13 + D.1856_18;
  *D.1852_8 = D.1857_19;
  i_20 = i_14 + 1;

<bb 4>:
  # i_1 = PHI <i_20(3)>
  i.0_3 = (unsigned int) i_1;
  if (i.0_3 < samples_4(D))
    goto <bb 3>;
  else
    goto <bb 5>;

<bb 5>:
  return;
}

The two PHI nodes in the beginning of BB3 break the iv detection. Same example when types of ‘i’ and ‘samples’ would match will be analyzed perfectly fine with the SSA at the same point looking like this:

VecADD (In1, In2, Out, samples)
{
  int i;
  long long int D.1857;
  long long int D.1856;
  long long int * D.1855;
  long long int D.1854;
  long long int * D.1853;
  long long int * D.1852;
  unsigned int D.1851;
  unsigned int i.0;

<bb 2>:

<bb 6>:
  # i_9 = PHI <0(2)>
  if (i_9 < samples_3(D))
    goto <bb 3>;
  else
    goto <bb 5>;

<bb 3>:
  # i_13 = PHI <i_1(4), i_9(6)>
  i.0_4 = (unsigned int) i_13;
  D.1851_5 = i.0_4 * 8;
  D.1852_7 = Out_6(D) + D.1851_5;
  D.1853_11 = In1_10(D) + D.1851_5;
  D.1854_12 = *D.1853_11;
  D.1855_16 = In2_15(D) + D.1851_5;
  D.1856_17 = *D.1855_16;
  D.1857_18 = D.1854_12 + D.1856_17;
  *D.1852_7 = D.1857_18;
  i_19 = i_13 + 1;

<bb 4>:
  # i_1 = PHI <i_19(3)>
  if (i_1 < samples_3(D))
    goto <bb 3>;
  else
    goto <bb 5>;

<bb 5>:
  return;
}

On one hand I seem to understand that a danger of signed/unsigned overflow at increment can force this kind of conservatism, but on the high level this situation was handled fine by gcc 3.4.6 and is handled with no issues by another SSA based compiler. If there is a way to relax this strict interpretation of C rules by GCC 4.3.2, I would gladly learn about it, but my brief flag mining exercise yielded no results. Thank you.


---


### compiler : `gcc`
### title : `Missed full redundancies during PRE`
### open_at : `2009-01-28T10:06:23Z`
### last_modified_date : `2021-12-27T05:44:14Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=38998
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.4.0`
### severity : `enhancement`
### contents :
extern double cos(double);
void test2(double x, double y)
{
 if (cos(y<10 ? x : -y) != cos(y<10 ? x : y))
     link_error ();
}

PRE figures out new full redundancies because it phi-translates.  This leads
to missed optimizations wrt the SCCVN value-numbers because we do not iterate
with the new redundancy.  The immediate effect is that PRE inserts a
duplicate PHI:

<bb 4>:
  # x_2 = PHI <x_5(D)(3), y_3(D)(7)>
  # D.1601_16 = PHI <D.1601_8(3), D.1601_9(7)>
  # prephitmp.13_15 = PHI <D.1601_8(3), D.1601_9(7)>

which only DOM removes later.  The second-order missed optimization is
that elimination does not optimize the following predicate

  D.1606_12 = prephitmp.13_15;
  if (D.1601_16 != D.1606_12)

See also

http://gcc.gnu.org/ml/gcc-patches/2008-08/msg01545.html

which added a broken patch that caused PR38926.


---


### compiler : `gcc`
### title : `C++ compiler doesn't optimize inlined function call for PIE`
### open_at : `2009-01-30T16:41:12Z`
### last_modified_date : `2021-07-22T18:33:57Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=39043
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `c++`
### version : `4.4.0`
### severity : `normal`
### contents :
[hjl@gnu-6 gcc]$ cat /tmp/i.ii 
inline void foo () {}

int
main ()
{
  foo ();
  return 0;
}
[hjl@gnu-6 gcc]$ ./xgcc -B./ -fpie /tmp/i.ii -S
[hjl@gnu-6 gcc]$ grep call i.s | grep foo
	call	_Z3foov@PLT
[hjl@gnu-6 gcc]$ 

Do we need @PLT for PIE?


---


### compiler : `gcc`
### title : `writing arrays twice not optimized`
### open_at : `2009-02-01T00:32:36Z`
### last_modified_date : `2023-05-15T04:35:15Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=39052
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.4.0`
### severity : `enhancement`
### contents :
In the test case below, both stores are done.

The compiler chould eliminate the first loop completely.

$ cat a.c
void foo(int *a, int n)
{
   int i;

   for (i=0; i<n; i++)
      a[i] = 0;

   for (i=0; i<n; i++)
      a[i] = 1;
}
$ gcc -O3 -S a.c
$ cat a.s
        .file   "a.c"
        .text
        .p2align 4,,15
.globl foo
        .type   foo, @function
foo:
        pushl   %ebp
        movl    %esp, %ebp
        movl    12(%ebp), %edx
        movl    8(%ebp), %ecx
        testl   %edx, %edx
        jle     .L5
        xorl    %eax, %eax
        .p2align 4,,7
        .p2align 3
.L3:
        movl    $0, (%ecx,%eax,4)
        addl    $1, %eax
        cmpl    %edx, %eax
        jne     .L3
        xorl    %eax, %eax
        .p2align 4,,7
        .p2align 3
.L4:
        movl    $1, (%ecx,%eax,4)
        addl    $1, %eax
        cmpl    %edx, %eax
        jne     .L4
.L5:
        popl    %ebp
        ret
        .size   foo, .-foo
        .ident  "GCC: (GNU) 4.4.0 20090124 (experimental)"
        .section        .note.GNU-stack,"",@progbits


---


### compiler : `gcc`
### title : `alignment for "unsigned short a[10000]" vs "extern unsigned short a[10000]"`
### open_at : `2009-02-02T14:39:52Z`
### last_modified_date : `2022-01-05T10:00:45Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=39075
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.4.0`
### severity : `enhancement`
### contents :
 


---


### compiler : `gcc`
### title : `loop_niter_by_eval should deal with &a[i_1]`
### open_at : `2009-02-04T10:34:31Z`
### last_modified_date : `2022-01-03T11:05:05Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=39094
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.4.0`
### severity : `enhancement`
### contents :
Brute force evaluation of niters does not deal with

<bb 5>:
  i_10 = i_1 + 1;

<bb 6>:
  # i_1 = PHI <0(2), i_10(5)>
  # .MEM_11 = PHI <.MEM_17(2), .MEM_11(5)>
  if (i_1 <= 4)
    goto <bb 3>;
  else
    goto <bb 7>;

<bb 3>:
  D.5476_6 = &a._M_instance[i_1];
  D.5457_8 = i_1 * 4;
  D.5458_9 = &a._M_instance[0] + D.5457_8;
  if (D.5476_6 != D.5458_9)
    goto <bb 4>;
  else
    goto <bb 5>;

where get_val_for cannot handle &a._M_instance[i_1].


---


### compiler : `gcc`
### title : `gcc generating multiple stack stores in optimised code`
### open_at : `2009-02-05T08:34:23Z`
### last_modified_date : `2021-08-16T01:08:04Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=39102
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.3.3`
### severity : `enhancement`
### contents :
Test code:

#include <stdint.h>

struct u64x2_t {
  uint64_t u64a;
  uint64_t u64b;
};

union u64_u {
  uint64_t u64;
  uint64_t *ptr_u64;
};

struct u64x2_t multiple_stack_stores(struct u64x2_t in) {
  struct u64x2_t out;
  out.u64a=in.u64a+1;
  out.u64b=in.u64b;
  if ((out.u64a & 63)==0) {
    union u64_u u;
    u.u64=(out.u64a >> 6) << 3;
    out.u64b=u.ptr_u64[0];
  }
  return out;
}

struct u64x2_t no_stack_stores(uint64_t u64a, uint64_t u64b) {
  struct u64x2_t out;
  out.u64a=u64a+1;
  out.u64b=u64b;
  if ((out.u64a & 63)==0) {
    union u64_u u;
    u.u64=(out.u64a >> 6) << 3;
    out.u64b=u.ptr_u64[0];
  }
  return out;
}

int main() {
  return 0;
}


$ gcc-4.3 -O3 gcc-stack-stores-bug.c && objdump -d -m i386:x86-64:intel a.out
generates in part:

0000000000400480 <multiple_stack_stores>:
  400480:       48 8d 4f 01             lea    rcx,[rdi+0x1]
  400484:       48 89 7c 24 d8          mov    QWORD PTR [rsp-0x28],rdi
  400489:       48 89 74 24 e0          mov    QWORD PTR [rsp-0x20],rsi
  40048e:       f6 c1 3f                test   cl,0x3f
  400491:       75 0f                   jne    4004a2 <multiple_stack_stores+0x22>
  400493:       48 89 c8                mov    rax,rcx
  400496:       48 c1 e8 06             shr    rax,0x6
  40049a:       48 8b 34 c5 00 00 00    mov    rsi,QWORD PTR [rax*8+0x0]
  4004a1:       00 
  4004a2:       48 89 f2                mov    rdx,rsi
  4004a5:       48 89 c8                mov    rax,rcx
  4004a8:       c3                      ret    
  4004a9:       0f 1f 80 00 00 00 00    nop    DWORD PTR [rax+0x0]

00000000004004b0 <no_stack_stores>:
  4004b0:       48 8d 4f 01             lea    rcx,[rdi+0x1]
  4004b4:       f6 c1 3f                test   cl,0x3f
  4004b7:       75 0f                   jne    4004c8 <no_stack_stores+0x18>
  4004b9:       48 89 c8                mov    rax,rcx
  4004bc:       48 c1 e8 06             shr    rax,0x6
  4004c0:       48 8b 34 c5 00 00 00    mov    rsi,QWORD PTR [rax*8+0x0]
  4004c7:       00 
  4004c8:       48 89 f2                mov    rdx,rsi
  4004cb:       48 89 c8                mov    rax,rcx
  4004ce:       c3                      ret    
  4004cf:       90                      nop    


With the better-designed x86-64 ABI this struct is passed and returned in registers. So why is gcc generating this code:

  400484:       48 89 7c 24 d8          mov    QWORD PTR [rsp-0x28],rdi
  400489:       48 89 74 24 e0          mov    QWORD PTR [rsp-0x20],rsi

Similar output is observed with gcc-4.1, gcc-4.2 and gcc-snapshot (Debian 20090129-1) 4.4.0 20090129 (experimental) [trunk revision 143770]


---


### compiler : `gcc`
### title : `[meta-bug] ivopts metabug`
### open_at : `2009-02-16T09:06:46Z`
### last_modified_date : `2019-03-05T16:33:59Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=39201
### status : `RESOLVED`
### tags : `meta-bug, missed-optimization`
### component : `tree-optimization`
### version : `4.4.0`
### severity : `normal`
### contents :
Metabug for ivopts issues


---


### compiler : `gcc`
### title : `FAIL: g++.dg/tree-ssa/new1.C scan-tree-dump-not forwprop1 "= .* \+ -"`
### open_at : `2009-02-19T18:22:30Z`
### last_modified_date : `2021-12-12T09:32:52Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=39251
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.4.0`
### severity : `normal`
### contents :
Executing on host: /home/dave/gnu/gcc/objdir/gcc/testsuite/g++/../../g++ -B/home
/dave/gnu/gcc/objdir/gcc/testsuite/g++/../../ /home/dave/gnu/gcc/gcc/gcc/testsui
te/g++.dg/tree-ssa/new1.C  -nostdinc++ -I/home/dave/gnu/gcc/objdir/arm-none-linu
x-gnueabi/libstdc++-v3/include/arm-none-linux-gnueabi -I/home/dave/gnu/gcc/objdi
r/arm-none-linux-gnueabi/libstdc++-v3/include -I/home/dave/gnu/gcc/gcc/libstdc++
-v3/libsupc++ -I/home/dave/gnu/gcc/gcc/libstdc++-v3/include/backward -I/home/dav
e/gnu/gcc/gcc/libstdc++-v3/testsuite/util -fmessage-length=0  -O2 -Wall -fdump-t
ree-forwprop1  -S  -o new1.s    (timeout = 300)
PASS: g++.dg/tree-ssa/new1.C (test for excess errors)
FAIL: g++.dg/tree-ssa/new1.C scan-tree-dump-not forwprop1 "= .* \+ -"


---


### compiler : `gcc`
### title : `x86 -Os could use mulw for (uint16 * uint16)>>16`
### open_at : `2009-03-01T02:42:30Z`
### last_modified_date : `2021-07-21T05:01:44Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=39329
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.4.0`
### severity : `enhancement`
### contents :
Using 'gcc -Os -fomit-frame-pointer -march=core2 -mtune=core2' for

unsigned short mul_high_c(unsigned short a, unsigned short b)
{
    return (unsigned)(a * b) >> 16;
}

unsigned short mul_high_asm(unsigned short a, unsigned short b)
{
    unsigned short res;
    asm("mulw %w2" : "=d"(res),"+a"(a) : "rm"(b));
    return res;
}

I get

_mul_high_c:
	subl	$12, %esp
	movzwl	20(%esp), %eax
	movzwl	16(%esp), %edx
	addl	$12, %esp
	imull	%edx, %eax
	shrl	$16, %eax
	ret
_mul_high_asm:
	subl	$12, %esp
	movl	16(%esp), %eax
	mulw 20(%esp)
	addl	$12, %esp
	movl	%edx, %eax
	ret

mulw puts its outputs in dx:ax, and dx contains (dx:ax)>>16, so the shift is avoided.

Ignoring the weird Darwin stack adjustment code, the version with mulw is somewhat shorter and avoids a movzwl. I'm not sure what the performance difference is; mulw is listed in Agner's tables as fairly low latency, but requires a length changing prefix for memory.

This type of operation is useful in fixed-point math, such as embedded audio codecs or arithmetic coders.


---


### compiler : `gcc`
### title : `reload is too earer to re-use reload registers`
### open_at : `2009-03-05T02:41:28Z`
### last_modified_date : `2021-07-19T17:14:14Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=39374
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.4.0`
### severity : `normal`
### contents :
reload is too eager to re-use reload registers, which means that
reloads that should be available for inheritance by later insn do not
even live past the end of the current insn.
There should be a target hook to identify input reloads that
should be kept.


---


### compiler : `gcc`
### title : `Calculated values replaced with constants even if the constants cost more than the calculations`
### open_at : `2009-03-15T22:49:44Z`
### last_modified_date : `2019-03-06T08:53:55Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=39469
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.4.0`
### severity : `normal`
### contents :
On ARM target when the compiler can deduce that the result of a calculation is a constant, it always substitutes the calculation with the constant, even if loading the constant is more expensive (both in code size and execution time) than the actual calculation. 

I attach a file that contains two short C functions. They do exactly the same, but foo() processes a constant while bar() processes its argument. Compiling the code with -Os, -O2 or -O3 results in code where processing the argument is much shorter and faster than processing the constant. 

In particular, processing the variable argument generates code (the same assembly is generated for -Os and -O3) that is 7 words long and executes in 14 clocks. Using -Os, the function processing a constant generates a 10 word, 25 clock assembly while -O2 or -O3 creates a 17 words, 24 clock code.

That is, when a constant is given instead of a variable parameter, the generated code is 40% longer and 79% slower for -Os and 143% longer and 71% slower with -O3.

Adding the load of the constant to the beginning of the variable argument version of the code would cost 1 word, 1 clock if the peephole optimiser was clever enough and 2 words, 3 clocks in the worst case. Nowhere near the 3 words, 11 clocks (-Os) or 10 words, 10 clocks (-O2,-O3) cost the compiler generated.


The command line used was:

arm-aebi-gcc-4.4.0 -S -O[s23] constant.c


---


### compiler : `gcc`
### title : `Nonoptimal byte load. mov (%rdi),%al better then movzbl (%rdi),%eax`
### open_at : `2009-03-24T18:59:36Z`
### last_modified_date : `2021-09-09T22:26:29Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=39549
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.3.2`
### severity : `enhancement`
### contents :
> gcc --version
gcc (SUSE Linux) 4.3.2 [gcc-4_3-branch revision 141291]

> cat test.c
// file test.c One byte transfer

void f(char *a,char *b){
*b=*a;
}

void F(char *a,char *b){
asm volatile("mov (%rdi),%al\nmov %al,(%rsi)");
}
...

> gcc -g -otest test.c -O2 -mtune=core2
> objdump -d test
....
00000000004004f0 <f>:
  4004f0:	0f b6 07             	movzbl (%rdi),%eax
  4004f3:	88 06                	mov    %al,(%rsi)
  4004f5:	c3                   	retq   
  4004f6:	66 2e 0f 1f 84 00 00 	nopw   %cs:0x0(%rax,%rax,1)
  4004fd:	00 00 00 

0000000000400500 <F>:
  400500:	8a 07                	mov    (%rdi),%al
  400502:	88 06                	mov    %al,(%rsi)
  400504:	c3                   	retq   
  
GCC use movzbl (%rdi),%eax, but better to use mov (%rdi),%al, because last instruction 1 byte shorter. Execution time the same (at least on Core 2 Duo and Core 2 Solo).

Probably it is result of Intel recomendations to use movz to avoid a partial register stall. But smaller instruction reduce fetch bandwidth... and

Qwote from: Intel® 64 and IA-32 Architectures Optimization Reference Manual 248966. 3.5.2.3 Partial Register Stalls
"The delay of a partial register stall is small in processors based on Intel Core and
NetBurst microarchitectures, and in Pentium M processor (with CPUID signature
family 6, model 13), Intel Core Solo, and Intel Core Duo processors. Pentium M
processors (CPUID signature with family 6, model 9) and the P6 family incur a large
penalty."


---


### compiler : `gcc`
### title : `Unnecessary stack usage with flexible array member`
### open_at : `2009-03-25T00:54:39Z`
### last_modified_date : `2022-01-06T03:33:35Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=39552
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.4.0`
### severity : `enhancement`
### contents :
After fixing PR 39545, I got

[hjl@gnu-34 pr39545]$ cat f-1.i
struct line {
int length;
char contents[];
};

void foo (struct line);

struct line
bar ()
{
 struct line x;
 x.length = sizeof (struct line);
 foo (x);
 return x;
}
[hjl@gnu-34 pr39545]$ make f-1.s
/export/build/gnu/gcc-avx/build-x86_64-linux/stage1-gcc/xgcc -B/export/build/gnu/gcc-avx/build-x86_64-linux/stage1-gcc/ -O2 -fno-asynchronous-unwind-tables -S -o f-1.s f-1.i
f-1.i: In function ‘bar’:
f-1.i:10: note: The ABI of passing struct with a flexible array member has changed in GCC 4.4
[hjl@gnu-34 pr39545]$ cat f-1.s
	.file	"f-1.i"
	.text
	.p2align 4,,15
.globl bar
	.type	bar, @function
bar:
	subq	$40, %rsp
	movl	$4, 16(%rsp)
	movq	16(%rsp), %rdi
	call	foo
	movl	$4, %eax
	addq	$40, %rsp
	ret
	.size	bar, .-bar
[hjl@gnu-34 pr39545]$ cat f-3.i
struct line {
int length;
char contents[0];
};

void foo (struct line);

struct line
bar ()
{
 struct line x;
 x.length = sizeof (struct line);
 foo (x);
 return x;
}
[hjl@gnu-34 pr39545]$ make f-3.s
/export/build/gnu/gcc-avx/build-x86_64-linux/stage1-gcc/xgcc -B/export/build/gnu/gcc-avx/build-x86_64-linux/stage1-gcc/ -O2 -fno-asynchronous-unwind-tables -S -o f-3.s f-3.i
[hjl@gnu-34 pr39545]$ cat f-3.s
	.file	"f-3.i"
	.text
	.p2align 4,,15
.globl bar
	.type	bar, @function
bar:
	subq	$8, %rsp
	movl	$4, %edi
	call	foo
	movl	$4, %eax
	addq	$8, %rsp
	ret
	.size	bar, .-bar
[hjl@gnu-34 pr39545]$ 

With char contents[0], gcc doesn't touch stack. With char contents[],
we put value on stack even if it is passed in register.


---


### compiler : `gcc`
### title : `[8/9/10 Regression] LIM inserts loads from uninitialized local memory`
### open_at : `2009-04-02T04:31:47Z`
### last_modified_date : `2022-04-22T06:29:13Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=39612
### status : `RESOLVED`
### tags : `deferred, missed-optimization`
### component : `tree-optimization`
### version : `4.4.0`
### severity : `normal`
### contents :
GCC Version: gcc (gcc version 4.4.0 20090307 (Red Hat 4.4.0-0.23) (GCC)
Distribution: Fedora Rawhide.

The attached pre-processed code generates:
f.i: In function ‘f2’:
f.i:19: warning: ‘inter’ is used uninitialized in this function

I believe that this warning is incorrect.


---


### compiler : `gcc`
### title : `-fstrict-overflow misses multiply in comparison`
### open_at : `2009-04-07T20:06:59Z`
### last_modified_date : `2023-06-18T18:53:56Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=39683
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.4.0`
### severity : `enhancement`
### contents :
The shift isn't necessary.  This could have
been re-coded as

    return (a-b)<2;

with -fstrict-overflow.

$ cat ga.c
int foo(int a, int b)
{
    return (a-b)*4 < 8;
}
$ gcc -S -O2 -fstrict-overflow ga.c
$ cat ga.s
        .file   "ga.c"
        .text
        .p2align 4,,15
.globl foo
        .type   foo, @function
foo:
        pushl   %ebp
        movl    %esp, %ebp
        movl    8(%ebp), %eax
        subl    12(%ebp), %eax
        popl    %ebp
        sall    $2, %eax
        cmpl    $7, %eax
        setle   %al
        movzbl  %al, %eax
        ret
        .size   foo, .-foo
        .ident  "GCC: (GNU) 4.4.0 20090221 (experimental)"
        .section        .note.GNU-stack,"",@progbits


---


### compiler : `gcc`
### title : `[11/12/13/14 Regression][cond-optab] MIPS pessimizations on floating-point`
### open_at : `2009-04-10T14:20:09Z`
### last_modified_date : `2023-07-07T10:29:11Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=39725
### status : `WAITING`
### tags : `missed-optimization`
### component : `target`
### version : `4.5.0`
### severity : `normal`
### contents :
MIPS floating-point comparisons are sometimes improved, sometimes pessimized.  Here are the tests that are pessimized more:

gcc.c-torture/execute/ieee/compare-fp-1.c
gcc.c-torture/execute/ieee/compare-fp-4.c (-fno-trapping-math)
gcc.c-torture/unsorted/DFcmp.c

(not for all versions, but for example at -O1 -mfp32 -mgp32 they are affected).

Just removing these three is enough to change from a depressing

 513 files changed, 24582 insertions(+), 20790 deletions(-)

to a decent

 467 files changed, 15738 insertions(+), 15818 deletions(-)


---


### compiler : `gcc`
### title : `component references with VIEW_CONVERT_EXPR should be canonicalized`
### open_at : `2009-04-12T18:35:39Z`
### last_modified_date : `2021-07-26T20:19:14Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=39744
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.5.0`
### severity : `enhancement`
### contents :
VIEW_CONVERT_EXPR <T>(a.b.c.d).e.f.g.h

should be canonicalized to strip zero-offset and same size as T component
references off the VIEW_CONVERT_EXPR argument.  The same should be applied
to component references of the VIEW_CONVERT_EXPR result by adjusting the
type T the VIEW_CONVERT_EXPR converts to.

This missed canonicalization will help folding and value numbering.


---


### compiler : `gcc`
### title : `data-flow analysis does not discover constant real/imaginary parts`
### open_at : `2009-04-14T08:54:46Z`
### last_modified_date : `2021-07-26T04:56:00Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=39761
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.4.0`
### severity : `normal`
### contents :
From this testcase:

void bar();
void foo(int i)
{
  __complex__ int k = 0;
  if (i)
    k = 1;
  if (k)
    bar();
}

(cfr. gcc.c-torture/compile/pr35431.c) we get after cddce1:

  # k_1 = PHI <__complex__ (0, 0)(2), __complex__ (1, 0)(3)>
  D.1198_6 = REALPART_EXPR <k_1>;
  if (D.1198_6 != 0)
    goto <bb 6>;
  else
    goto <bb 5>;

<bb 5>:
  D.1200_7 = IMAGPART_EXPR <k_1>;
  if (D.1200_7 != 0)
    goto <bb 6>;
  else
    goto <bb 7>;

and the IMAGPART_EXPR could be CCP'd or FRE'd to zero.  Likewise the REALPART_EXPR could be FRE'd to PHI <0(2), 1(3)>.


---


### compiler : `gcc`
### title : `120% slowdown with vectorizer`
### open_at : `2009-04-20T00:23:00Z`
### last_modified_date : `2021-09-03T02:41:11Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=39821
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.4.0`
### severity : `normal`
### contents :
The vectorizer produces horrible code with this testcase:

$ cat dotproduct.c 
#include "inttypes.h"

int64_t dotproduct(int32_t *v1, int32_t *v2, int order)
{
    int64_t accum = 0;
    while (order--)
        accum += (int64_t) *v1++ * *v2++;
    return accum;
}

int64_t dotproduct_order4(int32_t *v1, int32_t *v2, int order)
{
    return dotproduct(v1, v2, 4);
}
$ gcc-4.4rc1 -o dotproduct.o -c dotproduct.c -O3
$ gcc-4.4rc1 -o dotproduct-no-vectorize.o -c dotproduct.c -O3 -fno-tree-vectorize
$ objdump -d dotproduct.o

dotproduct.o:     file format elf64-x86-64


Disassembly of section .text:

0000000000000000 <dotproduct>:
   0:   31 c0                   xor    %eax,%eax
   2:   85 d2                   test   %edx,%edx
   4:   0f 84 4e 01 00 00       je     158 <dotproduct+0x158>
   a:   41 89 d0                mov    %edx,%r8d
   d:   44 8d 52 ff             lea    -0x1(%rdx),%r10d
  11:   41 c1 e8 02             shr    $0x2,%r8d
  15:   83 fa 03                cmp    $0x3,%edx
  18:   46 8d 0c 85 00 00 00    lea    0x0(,%r8,4),%r9d
  1f:   00 
  20:   76 05                   jbe    27 <dotproduct+0x27>
  22:   45 85 c9                test   %r9d,%r9d
  25:   75 09                   jne    30 <dotproduct+0x30>
  27:   31 c0                   xor    %eax,%eax
  29:   e9 fc 00 00 00          jmpq   12a <dotproduct+0x12a>
  2e:   66 90                   xchg   %ax,%ax
  30:   66 0f ef c0             pxor   %xmm0,%xmm0
  34:   31 c0                   xor    %eax,%eax
  36:   66 45 0f ef c9          pxor   %xmm9,%xmm9
  3b:   31 c9                   xor    %ecx,%ecx
  3d:   0f 1f 00                nopl   (%rax)
  40:   f3 0f 6f 14 07          movdqu (%rdi,%rax,1),%xmm2
  45:   83 c1 01                add    $0x1,%ecx
  48:   66 41 0f 6f d9          movdqa %xmm9,%xmm3
  4d:   f3 0f 6f 24 06          movdqu (%rsi,%rax,1),%xmm4
  52:   66 45 0f 6f c1          movdqa %xmm9,%xmm8
  57:   66 0f 6f ea             movdqa %xmm2,%xmm5
  5b:   48 83 c0 10             add    $0x10,%rax
  5f:   66 0f 66 dc             pcmpgtd %xmm4,%xmm3
  63:   66 0f 6f fc             movdqa %xmm4,%xmm7
  67:   66 44 0f 66 c2          pcmpgtd %xmm2,%xmm8
  6c:   41 39 c8                cmp    %ecx,%r8d
  6f:   66 0f 62 fb             punpckldq %xmm3,%xmm7
  73:   66 41 0f 62 e8          punpckldq %xmm8,%xmm5
  78:   66 0f 6a e3             punpckhdq %xmm3,%xmm4
  7c:   66 41 0f 6a d0          punpckhdq %xmm8,%xmm2
  81:   66 0f 6f cf             movdqa %xmm7,%xmm1
  85:   66 0f 6f f5             movdqa %xmm5,%xmm6
  89:   66 44 0f 6f d7          movdqa %xmm7,%xmm10
  8e:   66 0f f4 cd             pmuludq %xmm5,%xmm1
  92:   66 0f 6f da             movdqa %xmm2,%xmm3
  96:   66 0f 73 d6 20          psrlq  $0x20,%xmm6
  9b:   66 0f f4 f7             pmuludq %xmm7,%xmm6
  9f:   66 41 0f 73 d2 20       psrlq  $0x20,%xmm10
  a5:   66 0f 73 f6 20          psllq  $0x20,%xmm6
  aa:   66 41 0f f4 ea          pmuludq %xmm10,%xmm5
  af:   66 0f d4 ce             paddq  %xmm6,%xmm1
  b3:   66 0f 73 f5 20          psllq  $0x20,%xmm5
  b8:   66 0f d4 cd             paddq  %xmm5,%xmm1
  bc:   66 0f 6f ec             movdqa %xmm4,%xmm5
  c0:   66 0f d4 c8             paddq  %xmm0,%xmm1
  c4:   66 0f 73 d3 20          psrlq  $0x20,%xmm3
  c9:   66 0f 6f c4             movdqa %xmm4,%xmm0
  cd:   66 0f f4 dc             pmuludq %xmm4,%xmm3
  d1:   66 0f 73 f3 20          psllq  $0x20,%xmm3
  d6:   66 0f 73 d5 20          psrlq  $0x20,%xmm5
  db:   66 0f f4 c2             pmuludq %xmm2,%xmm0
  df:   66 0f f4 d5             pmuludq %xmm5,%xmm2
  e3:   66 0f d4 c3             paddq  %xmm3,%xmm0
  e7:   66 0f 73 f2 20          psllq  $0x20,%xmm2
  ec:   66 0f d4 c2             paddq  %xmm2,%xmm0
  f0:   66 0f d4 c1             paddq  %xmm1,%xmm0
  f4:   0f 87 46 ff ff ff       ja     40 <dotproduct+0x40>
  fa:   42 8d 0c 8d 00 00 00    lea    0x0(,%r9,4),%ecx
 101:   00 
 102:   66 0f 6f c8             movdqa %xmm0,%xmm1
 106:   45 29 ca                sub    %r9d,%r10d
 109:   89 c9                   mov    %ecx,%ecx
 10b:   66 0f 73 d9 08          psrldq $0x8,%xmm1
 110:   66 0f d4 c1             paddq  %xmm1,%xmm0
 114:   48 01 cf                add    %rcx,%rdi
 117:   48 01 ce                add    %rcx,%rsi
 11a:   44 39 ca                cmp    %r9d,%edx
 11d:   66 0f d6 44 24 f8       movq   %xmm0,-0x8(%rsp)
 123:   48 8b 44 24 f8          mov    -0x8(%rsp),%rax
 128:   74 2e                   je     158 <dotproduct+0x158>
 12a:   45 89 d2                mov    %r10d,%r10d
 12d:   31 d2                   xor    %edx,%edx
 12f:   4e 8d 0c 95 04 00 00    lea    0x4(,%r10,4),%r9
 136:   00 
 137:   66 0f 1f 84 00 00 00    nopw   0x0(%rax,%rax,1)
 13e:   00 00 
 140:   48 63 0c 16             movslq (%rsi,%rdx,1),%rcx
 144:   4c 63 04 17             movslq (%rdi,%rdx,1),%r8
 148:   48 83 c2 04             add    $0x4,%rdx
 14c:   49 0f af c8             imul   %r8,%rcx
 150:   48 01 c8                add    %rcx,%rax
 153:   4c 39 ca                cmp    %r9,%rdx
 156:   75 e8                   jne    140 <dotproduct+0x140>
 158:   f3 c3                   repz retq 
 15a:   66 0f 1f 44 00 00       nopw   0x0(%rax,%rax,1)

0000000000000160 <dotproduct_order4>:
 160:   66 0f ef c0             pxor   %xmm0,%xmm0
 164:   f3 0f 6f 0f             movdqu (%rdi),%xmm1
 168:   f3 0f 6f 1e             movdqu (%rsi),%xmm3
 16c:   66 0f 6f d0             movdqa %xmm0,%xmm2
 170:   66 0f 6f f1             movdqa %xmm1,%xmm6
 174:   66 0f 66 c1             pcmpgtd %xmm1,%xmm0
 178:   66 0f 6f fb             movdqa %xmm3,%xmm7
 17c:   66 0f 66 d3             pcmpgtd %xmm3,%xmm2
 180:   66 0f 62 f0             punpckldq %xmm0,%xmm6
 184:   66 0f 62 fa             punpckldq %xmm2,%xmm7
 188:   66 0f 6a da             punpckhdq %xmm2,%xmm3
 18c:   66 0f 6a c8             punpckhdq %xmm0,%xmm1
 190:   66 0f 6f ee             movdqa %xmm6,%xmm5
 194:   66 44 0f 6f c7          movdqa %xmm7,%xmm8
 199:   66 0f 6f e7             movdqa %xmm7,%xmm4
 19d:   66 0f 6f c3             movdqa %xmm3,%xmm0
 1a1:   66 0f 73 d5 20          psrlq  $0x20,%xmm5
 1a6:   66 44 0f f4 c6          pmuludq %xmm6,%xmm8
 1ab:   66 0f f4 ef             pmuludq %xmm7,%xmm5
 1af:   66 0f 6f d1             movdqa %xmm1,%xmm2
 1b3:   66 0f 73 d4 20          psrlq  $0x20,%xmm4
 1b8:   66 0f 73 f5 20          psllq  $0x20,%xmm5
 1bd:   66 0f f4 e6             pmuludq %xmm6,%xmm4
 1c1:   66 41 0f d4 e8          paddq  %xmm8,%xmm5
 1c6:   66 0f 73 f4 20          psllq  $0x20,%xmm4
 1cb:   66 0f d4 e5             paddq  %xmm5,%xmm4
 1cf:   66 0f 6f eb             movdqa %xmm3,%xmm5
 1d3:   66 0f f4 c1             pmuludq %xmm1,%xmm0
 1d7:   66 0f 73 d2 20          psrlq  $0x20,%xmm2
 1dc:   66 0f f4 d3             pmuludq %xmm3,%xmm2
 1e0:   66 0f 73 f2 20          psllq  $0x20,%xmm2
 1e5:   66 0f d4 c2             paddq  %xmm2,%xmm0
 1e9:   66 0f 73 d5 20          psrlq  $0x20,%xmm5
 1ee:   66 0f f4 cd             pmuludq %xmm5,%xmm1
 1f2:   66 0f 73 f1 20          psllq  $0x20,%xmm1
 1f7:   66 0f d4 c1             paddq  %xmm1,%xmm0
 1fb:   66 0f d4 c4             paddq  %xmm4,%xmm0
 1ff:   66 0f 6f c8             movdqa %xmm0,%xmm1
 203:   66 0f 73 d9 08          psrldq $0x8,%xmm1
 208:   66 0f d4 c1             paddq  %xmm1,%xmm0
 20c:   66 0f d6 44 24 f8       movq   %xmm0,-0x8(%rsp)
 212:   48 8b 44 24 f8          mov    -0x8(%rsp),%rax
 217:   c3                      retq   
$ objdump -d dotproduct-no-vectorize.o

dotproduct-no-vectorize.o:     file format elf64-x86-64


Disassembly of section .text:

0000000000000000 <dotproduct>:
   0:   31 c0                   xor    %eax,%eax
   2:   85 d2                   test   %edx,%edx
   4:   74 2a                   je     30 <dotproduct+0x30>
   6:   83 ea 01                sub    $0x1,%edx
   9:   4c 8d 0c 95 04 00 00    lea    0x4(,%rdx,4),%r9
  10:   00 
  11:   31 d2                   xor    %edx,%edx
  13:   0f 1f 44 00 00          nopl   0x0(%rax,%rax,1)
  18:   48 63 0c 16             movslq (%rsi,%rdx,1),%rcx
  1c:   4c 63 04 17             movslq (%rdi,%rdx,1),%r8
  20:   48 83 c2 04             add    $0x4,%rdx
  24:   49 0f af c8             imul   %r8,%rcx
  28:   48 01 c8                add    %rcx,%rax
  2b:   4c 39 ca                cmp    %r9,%rdx
  2e:   75 e8                   jne    18 <dotproduct+0x18>
  30:   f3 c3                   repz retq 
  32:   66 66 66 66 66 2e 0f    nopw   %cs:0x0(%rax,%rax,1)
  39:   1f 84 00 00 00 00 00 

0000000000000040 <dotproduct_order4>:
  40:   48 63 07                movslq (%rdi),%rax
  43:   48 63 16                movslq (%rsi),%rdx
  46:   48 63 4f 04             movslq 0x4(%rdi),%rcx
  4a:   48 0f af d0             imul   %rax,%rdx
  4e:   48 63 46 04             movslq 0x4(%rsi),%rax
  52:   48 0f af c1             imul   %rcx,%rax
  56:   48 63 4f 08             movslq 0x8(%rdi),%rcx
  5a:   48 01 c2                add    %rax,%rdx
  5d:   48 63 46 08             movslq 0x8(%rsi),%rax
  61:   48 0f af c1             imul   %rcx,%rax
  65:   48 63 4f 0c             movslq 0xc(%rdi),%rcx
  69:   48 01 c2                add    %rax,%rdx
  6c:   48 63 46 0c             movslq 0xc(%rsi),%rax
  70:   48 0f af c1             imul   %rcx,%rax
  74:   48 01 d0                add    %rdx,%rax
  77:   c3                      retq


---


### compiler : `gcc`
### title : `VRP can't see through cast to unsigned`
### open_at : `2009-04-23T15:44:07Z`
### last_modified_date : `2023-06-09T15:31:26Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=39870
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.4.0`
### severity : `enhancement`
### contents :
A common way to do array bounds checking is to cast the index i to unsigned and then check

  if ((unsigned)i > (unsigned)length)
    abort();

instead of

  if (i >= length || i < 0)
    abort();

The phrases are equivalent, but VRP doesn't know that so the bounds check is not eliminated.

The problem is that this is such a common idiom that it will affect many programs.


---


### compiler : `gcc`
### title : `Nonoptimal code - leaveq; xchg   %ax,%ax; retq`
### open_at : `2009-04-28T12:20:33Z`
### last_modified_date : `2020-04-14T21:20:03Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=39942
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `target`
### version : `4.3.2`
### severity : `minor`
### contents :
Sometimes we can see 2 bytes nop (xchg %ax,%ax) between leaveq and retq.
IMHO, better to remove xchg %ax,%ax

Examples from Kernel 2.6.29.1:

> gcc --version
gcc (SUSE Linux) 4.3.2 [gcc-4_3-branch revision 141291]
> objdump vmlinux
...
ffffffff804262e0 <set_blitting_type>:
ffffffff804262e0:	55                   	push   %rbp
ffffffff804262e1:	0f b7 07             	movzwl (%rdi),%eax
ffffffff804262e4:	4c 8b 86 d0 03 00 00 	mov    0x3d0(%rsi),%r8
ffffffff804262eb:	48 c1 e0 07          	shl    $0x7,%rax
ffffffff804262ef:	48 89 e5             	mov    %rsp,%rbp
ffffffff804262f2:	48 05 40 1f 9c 80    	add    $0xffffffff809c1f40,%rax
ffffffff804262f8:	49 89 80 90 01 00 00 	mov    %rax,0x190(%r8)
ffffffff804262ff:	8b 46 04             	mov    0x4(%rsi),%eax
ffffffff80426302:	89 c1                	mov    %eax,%ecx
ffffffff80426304:	81 e1 00 00 02 00    	and    $0x20000,%ecx
ffffffff8042630a:	75 2c                	jne    ffffffff80426338 <set_blitting_type+0x58>
ffffffff8042630c:	48 8b 86 d0 03 00 00 	mov    0x3d0(%rsi),%rax
ffffffff80426313:	4c 89 c7             	mov    %r8,%rdi
ffffffff80426316:	48 8b 90 90 01 00 00 	mov    0x190(%rax),%rdx
ffffffff8042631d:	8b 52 1c             	mov    0x1c(%rdx),%edx
ffffffff80426320:	83 fa 03             	cmp    $0x3,%edx
ffffffff80426323:	0f 4e ca             	cmovle %edx,%ecx
ffffffff80426326:	89 88 b0 01 00 00    	mov    %ecx,0x1b0(%rax)
ffffffff8042632c:	e8 2f 4d 00 00       	callq  ffffffff8042b060 <fbcon_set_bitops>
ffffffff80426331:	c9                   	leaveq 
ffffffff80426332:	c3                   	retq   
ffffffff80426333:	0f 1f 44 00 00       	nopl   0x0(%rax,%rax,1)
ffffffff80426338:	e8 23 61 00 00       	callq  ffffffff8042c460 <fbcon_set_tileops>
ffffffff8042633d:	c9                   	leaveq 
ffffffff8042633e:	66 90                	xchg   %ax,%ax
ffffffff80426340:	c3                   	retq   

...
...

ffffffff8042b060 <fbcon_set_bitops>:
ffffffff8042b060:	55                   	push   %rbp
ffffffff8042b061:	48 c7 07 d0 ad 42 80 	movq   $0xffffffff8042add0,(%rdi)
ffffffff8042b068:	8b 87 b0 01 00 00    	mov    0x1b0(%rdi),%eax
ffffffff8042b06e:	48 89 e5             	mov    %rsp,%rbp
ffffffff8042b071:	48 c7 47 08 30 ae 42 	movq   $0xffffffff8042ae30,0x8(%rdi)
ffffffff8042b078:	80 
ffffffff8042b079:	48 c7 47 10 c0 b7 42 	movq   $0xffffffff8042b7c0,0x10(%rdi)
ffffffff8042b080:	80 
ffffffff8042b081:	48 c7 47 18 10 af 42 	movq   $0xffffffff8042af10,0x18(%rdi)
ffffffff8042b088:	80 
ffffffff8042b089:	48 c7 47 20 10 b1 42 	movq   $0xffffffff8042b110,0x20(%rdi)
ffffffff8042b090:	80 
ffffffff8042b091:	48 c7 47 28 c0 b0 42 	movq   $0xffffffff8042b0c0,0x28(%rdi)
ffffffff8042b098:	80 
ffffffff8042b099:	48 c7 47 30 00 00 00 	movq   $0x0,0x30(%rdi)
ffffffff8042b0a0:	00 
ffffffff8042b0a1:	85 c0                	test   %eax,%eax
ffffffff8042b0a3:	75 0b                	jne    ffffffff8042b0b0 <fbcon_set_bitops+0x50>
ffffffff8042b0a5:	c9                   	leaveq 
ffffffff8042b0a6:	c3                   	retq   
ffffffff8042b0a7:	66 0f 1f 84 00 00 00 	nopw   0x0(%rax,%rax,1)
ffffffff8042b0ae:	00 00 
ffffffff8042b0b0:	e8 4b 15 00 00       	callq  ffffffff8042c600 <fbcon_set_rotate>
ffffffff8042b0b5:	c9                   	leaveq 
ffffffff8042b0b6:	66 90                	xchg   %ax,%ax
ffffffff8042b0b8:	c3                   	retq


---


### compiler : `gcc`
### title : `use brz instead of cmp/be with 32-bit values`
### open_at : `2009-05-08T09:36:12Z`
### last_modified_date : `2021-09-09T09:28:27Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=40067
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.4.0`
### severity : `enhancement`
### contents :
Compiling the following function with -O3 gives the following assembly output:

void spin(int volatile* ptr) {
    while(*ptr);
    return;
}

spin:
.LLFB1:
        .register       %g2, #scratch
        lduw    [%o0], %g1      ! 8     *zero_extendsidi2_insn_sp64/2   [length = 1]
        cmp     %g1, 0  ! 9     *cmpsi_insn     [length = 1]
        be,pn   %icc, .LL3      ! 10    *normal_branch  [length = 1]
         mov    0, %g1  ! 17    *movdi_insn_sp64/1      [length = 1]
.LL6:   
        lduw    [%o0], %g2      ! 20    *zero_extendsidi2_insn_sp64/2   [length = 1]
        cmp     %g2, 0  ! 22    *cmpsi_insn     [length = 1]
        bne,pt  %icc, .LL6      ! 23    *normal_branch  [length = 1]
         add    %g1, 1, %g1     ! 19    *adddi3_sp64/1  [length = 1]
.LL3:   
        jmp     %o7+8   ! 55    *return_internal        [length = 1]
         mov    %g1, %o0        ! 30    *movdi_insn_sp64/1      [length = 1]

Manually replacing the cmp/b* pairs with br* instructions gives 10-11% more iterations/sec on my machine:

        .global spin_brz
spin_brz:
        .register %g2, #scratch
        ld        [%o0], %g1
        brz,pn    %g1, spin_brz_done
        clr       %g1
spin_brz_again:
        ld        [%o0], %g2
        brnz,pt   %g2, spin_brz_again
        add       %g1, 0x1, %g1
spin_brz_done:
        retl
        mov       %g1, %o0
        .size   spin_brz, .- spin_brz


---


### compiler : `gcc`
### title : `Nonoptimal code -  CMOVxx %eax,%edi; mov    %edi,%eax; retq`
### open_at : `2009-05-08T16:04:10Z`
### last_modified_date : `2023-08-08T01:26:13Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=40072
### status : `NEW`
### tags : `missed-optimization, ra`
### component : `target`
### version : `4.4.0`
### severity : `enhancement`
### contents :
Sometimes GCC generate code at end of function:

 cmovge %eax,%edi
 mov    %edi,%eax
 retq   

but faster:

 cmovl %edi,%eax
 retq   
  
Example:

# cat test.c

#define MX 0
#define LIM 7

char char_char(char m)
{if(m>LIM) return(MX); return(m);}

char char_int(int m)
{if(m>LIM) return(MX); return(m);}

char char_uint(unsigned int m)
{if(m>LIM) return(MX); return(m);}

char char_long(long m)
{if(m>LIM) return(MX); return(m);}

char char_ulong(unsigned long m)
{if(m>LIM) return(MX); return(m);}


int int_char(char m)
{if(m>LIM) return(MX); return(m);}

int int_int(int m)
{if(m>LIM) return(MX); return(m);}	// Nonoptimal 
int int_uint(unsigned int m)
{if(m>LIM) return(MX); return(m);}

int int_long(long m)
{if(m>LIM) return(MX); return(m);}

int int_ulong(unsigned long m)
{if(m>LIM) return(MX); return(m);}



unsigned int uint_char(char m)
{if(m>LIM) return(MX); return(m);}

unsigned int uint_int(int m)
{if(m>LIM) return(MX); return(m);}

unsigned int uint_uint(unsigned int m)	//Nonoptimal
{if(m>LIM) return(MX); return(m);}

unsigned int uint_long(long m)
{if(m>LIM) return(MX); return(m);}

unsigned int uint_ulong(unsigned long m)
{if(m>LIM) return(MX); return(m);}



long long_char(char m)
{if(m>LIM) return(MX); return(m);}

long long_int(int m)
{if(m>LIM) return(MX); return(m);}

long long_uint(unsigned int m)
{if(m>LIM) return(MX); return(m);}

long long_long(long m)			//Nonoptimal
{if(m>LIM) return(MX); return(m);}

long long_ulong(unsigned long m)
{if(m>LIM) return(MX); return(m);}




unsigned long ulong_char(char m)
{if(m>LIM) return(MX); return(m);}

unsigned long ulong_int(int m)
{if(m>LIM) return(MX); return(m);}

unsigned long ulong_uint(unsigned int m)
{if(m>LIM) return(MX); return(m);}

unsigned long ulong_long(long m)
{if(m>LIM) return(MX); return(m);}

unsigned long ulong_ulong(unsigned long m)	//Nonoptimal
{if(m>LIM) return(MX); return(m);}

# gcc -o t test.c -O2 -c
# objdump -d t

t:     file format elf64-x86-64


Disassembly of section .text:

0000000000000000 <char_char>:
   0:	89 f8                	mov    %edi,%eax
   2:	40 80 ff 08          	cmp    $0x8,%dil
   6:	ba 00 00 00 00       	mov    $0x0,%edx
   b:	0f 4d c2             	cmovge %edx,%eax    <--- It's ok! Optimal
   e:	c3                   	retq   
   f:	90                   	nop    

<skip...>

0000000000000060 <int_int>:
  60:	83 ff 08             	cmp    $0x8,%edi
  63:	b8 00 00 00 00       	mov    $0x0,%eax
  68:	0f 4d f8             	cmovge %eax,%edi    <--- Nonoptimal
  6b:	89 f8                	mov    %edi,%eax    <--- Nonoptimal
  6d:	c3                   	retq   
  6e:	66 90                	xchg   %ax,%ax

<skip...>

00000000000000c0 <uint_uint>:
  c0:	83 ff 08             	cmp    $0x8,%edi
  c3:	b8 00 00 00 00       	mov    $0x0,%eax
  c8:	0f 43 f8             	cmovae %eax,%edi    <--- Nonoptimal
  cb:	89 f8                	mov    %edi,%eax    <--- Nonoptimal
  cd:	c3                   	retq   
  ce:	66 90                	xchg   %ax,%ax

<skip...>

0000000000000120 <long_long>:
 120:	48 83 ff 08          	cmp    $0x8,%rdi
 124:	b8 00 00 00 00       	mov    $0x0,%eax
 129:	48 0f 4d f8          	cmovge %rax,%rdi    <--- Nonoptimal
 12d:	48 89 f8             	mov    %rdi,%rax    <--- Nonoptimal
 130:	c3                   	retq   
 
<skip...>

0000000000000190 <ulong_ulong>:
 190:	48 83 ff 08          	cmp    $0x8,%rdi
 194:	b8 00 00 00 00       	mov    $0x0,%eax
 199:	48 0f 43 f8          	cmovae %rax,%rdi    <--- Nonoptimal
 19d:	48 89 f8             	mov    %rdi,%rax    <--- Nonoptimal
 1a0:	c3                   	retq


---


### compiler : `gcc`
### title : `Vector short/char shifts generate sub-optimal code`
### open_at : `2009-05-08T16:57:20Z`
### last_modified_date : `2022-03-08T17:25:08Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=40073
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `6.0`
### severity : `enhancement`
### contents :
On machines like the x86_64/i386 with -msse2 option or powerpc with the -maltivec option that support vector 8-bit/16-bit shift instructions, GCC generates suboptimal code for variable shifts.  Rather than generate the native instruction, the compiler converts the vector to V4SI vector, does the shift, and then converts the vector back to V16QI/V8HI mode.  I speculate that this is due to the normal binary operator rules being done to bring both sides to the same type.  Shifts and rotates are different in that the right hand side is an int type.


---


### compiler : `gcc`
### title : `Optimization by functios reordering.`
### open_at : `2009-05-10T16:38:56Z`
### last_modified_date : `2021-08-29T22:41:10Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=40093
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.4.0`
### severity : `enhancement`
### contents :
Because memory controller prefetch memory blocks, execution time of functions calls sequence depend on order this functions in memory. For example:
4 calls:

call func1
call func2
call func3
call func4

faster in case of direct functions order in memmory:
.p2align 4
func1:
      ret
.p2align 4
func2:
      ret
.p2align 4
func3:
      ret
.p2align 4
func4:
      ret

and slow in case inverse order:
.p2align 4
func4:
      ret
.p2align 4
func3:
      ret
.p2align 4
func2:
      ret
.p2align 4
func1:
      ret

Unfortunately, inverse order is typical for C/C++.
what do you think about this kind optimization?


---


### compiler : `gcc`
### title : `using alias-set zero for union accesses necessary because of RTL alias oracle`
### open_at : `2009-05-13T20:30:43Z`
### last_modified_date : `2019-10-23T12:35:31Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=40135
### status : `RESOLVED`
### tags : `alias, missed-optimization`
### component : `middle-end`
### version : `4.5.0`
### severity : `enhancement`
### contents :
The RTL alias oracle does defer to TBAA even for the case of disambiguating
two accesses based on decls.  This makes

  /* Permit type-punning when accessing a union, provided the access
     is directly through the union.  For example, this code does not
     permit taking the address of a union member and then storing
     through it.  Even the type-punning allowed here is a GCC
     extension, albeit a common and useful one; the C standard says
     that such accesses have implementation-defined behavior.  */
  for (u = t;
       TREE_CODE (u) == COMPONENT_REF || TREE_CODE (u) == ARRAY_REF;
       u = TREE_OPERAND (u, 0))
    if (TREE_CODE (u) == COMPONENT_REF
        && TREE_CODE (TREE_TYPE (TREE_OPERAND (u, 0))) == UNION_TYPE)
      return 0;

in c-common.c necessary which needlessly pessimizes TBAA in the face
of union accesses.


---


### compiler : `gcc`
### title : `finding common subexpressions`
### open_at : `2009-05-16T09:35:29Z`
### last_modified_date : `2021-12-25T07:01:19Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=40168
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.5.0`
### severity : `enhancement`
### contents :
The testcase to be attached can be compiled with

gfortran -O3 -march=native -ffast-math -funroll-loops -ffree-line-length-200 test.f90 

and as discussed in 
http://gcc.gnu.org/ml/gcc/2009-05/msg00416.html
shows some limitations in optimization of gcc 4.3 4.4 and 4.5


---


### compiler : `gcc`
### title : `redundant zero extensions`
### open_at : `2009-05-16T14:14:01Z`
### last_modified_date : `2021-07-26T05:58:29Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=40170
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.4.1`
### severity : `normal`
### contents :
#include <stdint.h>
#include <stdio.h>

uint8_t nibble(size_t addr) {
  size_t byte_addr;
  uint8_t bit;
  __asm__("shr $1, %[addr]; setc %[bit]\n"
	  : [addr] "=rm" (byte_addr), [bit] "=rm" (bit)
	  : "[addr]" (addr)
	  : "cc");
  uint8_t byte=((uint8_t *) byte_addr)[0];
  byte >>= bit;
  byte >>= bit;
  byte >>= bit;
  byte >>= bit;
  return byte & 15;
}

int main() {
  return 0;
}


Generated code for nibble() at -O3 (Intel syntax):

  400480:       48 d1 ef                shr    rdi,1
  400483:       0f 92 c1                setb   cl
  400486:       0f b6 07                movzx  eax,BYTE PTR [rdi]
  400489:       0f b6 c9                movzx  ecx,cl
  40048c:       d3 f8                   sar    eax,cl
  40048e:       0f b6 c0                movzx  eax,al
  400491:       d3 f8                   sar    eax,cl
  400493:       0f b6 c0                movzx  eax,al
  400496:       d3 f8                   sar    eax,cl
  400498:       0f b6 c0                movzx  eax,al
  40049b:       d3 f8                   sar    eax,cl
  40049d:       83 e0 0f                and    eax,0xf
  4004a0:       c3                      ret


Suggested code:

  400480:       48 d1 ef                shr    rdi,1
  400483:       0f 92 c1                setb   cl
  400486:       0f b6 07                movzx  eax,BYTE PTR [rdi]
  4004xx:       d3 f8                   sar    eax,cl
  4004xx:       d3 f8                   sar    eax,cl
  4004xx:       d3 f8                   sar    eax,cl
  4004xx:       d3 f8                   sar    eax,cl
  4004xx:       83 e0 0f                and    eax,0xf
  4004xx:       c3                      ret

[Alternatively multiply CL by 4 and perform one right shift by CL]

I do not see a partial register stall in the suggested code that the additional movzx instructions address.


---


### compiler : `gcc`
### title : `request for enhancement: delay argument loading until needed`
### open_at : `2009-05-20T15:15:37Z`
### last_modified_date : `2021-08-08T20:08:55Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=40207
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.3.0`
### severity : `enhancement`
### contents :
While working on some Linux kernel code, I've found that functions that
are declared as 'static inline' are having their arguments evaluated
well before they are used. For example I have a function:

static inline void trace(arg1, arg2)
{
    if (unlikely(enabled)) {
        <use the arguments>
    }
}

To make this more concrete here is a simple .c program:


#include <stdio.h>

# define unlikely(x)    __builtin_expect(!!(x), 0)

int enabled = 0;

struct foo {
        int value;
};

struct foo a = {
        .value = 10
};

static inline evaluate(int value) {
        if (unlikely(enabled)) {
                printf("value is: %d\n", value);
        }
}


/*

#define evaluate(val) \
do { \
        if (unlikely(enabled)) { \
                printf("value is: %d\n", val); \
        } \
} while (0)

*/

int main() {

        evaluate((&a)->value);
}


With the macro commented out I get:
00000000004004cc <main>:
  4004cc:       55                      push   %rbp
  4004cd:       48 89 e5                mov    %rsp,%rbp
  4004d0:       48 83 ec 10             sub    $0x10,%rsp
  4004d4:       8b 3d 22 04 20 00       mov    0x200422(%rip),%edi        # 6008fc <a>
  4004da:       e8 02 00 00 00          callq  4004e1 <evaluate>

Thus, a is loaded before the call to 'evaluate'

However, if i compile the macro version of 'evaluate' i get:

00000000004004cc <main>:
  4004cc:       55                      push   %rbp
  4004cd:       48 89 e5                mov    %rsp,%rbp
  4004d0:       48 83 ec 10             sub    $0x10,%rsp
  4004d4:       8b 05 ee 03 20 00       mov    0x2003ee(%rip),%eax        # 6008c8 <enabled>
  4004da:       85 c0                   test   %eax,%eax
  4004dc:       0f 95 c0                setne  %al
  4004df:       0f b6 c0                movzbl %al,%eax
  4004e2:       48 85 c0                test   %rax,%rax
  4004e5:       74 15                   je     4004fc <main+0x30>
  4004e7:       8b 35 c7 03 20 00       mov    0x2003c7(%rip),%esi        # 6008b4 <a>
  4004ed:       bf f8 05 40 00          mov    $0x4005f8,%edi
  4004f2:       b8 00 00 00 00          mov    $0x0,%eax
  4004f7:       e8 bc fe ff ff          callq  4003b8 <printf@plt>


Thus, the load of 'a' happens after the 'unlikely' test as I would like it. It would be nice if gcc could optimize the 'unlikely' case in the 'static inline' function case.

thanks.


---


### compiler : `gcc`
### title : `Conditional return not always profitable with -Os`
### open_at : `2009-06-06T14:43:36Z`
### last_modified_date : `2022-04-26T19:19:05Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=40361
### status : `RESOLVED`
### tags : `missed-optimization, patch`
### component : `rtl-optimization`
### version : `4.5.0`
### severity : `enhancement`
### contents :
Consider this test case:

extern void bar1 (void);
extern void bar2 (void);

int a;
int b;

int foo (void)
{
  if (a < 0)
    {
      bar1 ();
      if (b < 0)
	b = 0;
    }
  else
    {
      bar2 ();
      if (b < 0)
	b = 0;
    }
}


Compiling x86_64-unknown-linux X arm-elf "xgcc (GCC) 4.5.0 20090606 (experimental) [trunk revision 148236]", with options -march=armv7-r -Os -dAP" without patches results in this code:


	.file	"t.c"
	.text
	.align	2
	.global	foo
	.type	foo, %function
foo:
	@ args = 0, pretend = 0, frame = 0
	@ frame_needed = 0, uses_anonymous_args = 0
	@ basic block 2
	ldr	r3, .L6	@ 67	*arm_movsi_insn/5	[length = 4]
	stmfd	sp!, {r4, lr}	@ 69	*push_multi	[length = 4]
	ldr	r3, [r3, #0]	@ 6	*arm_movsi_insn/5	[length = 4]
	ldr	r4, .L6+4	@ 62	*arm_movsi_insn/5	[length = 4]
	cmp	r3, #0	@ 7	*arm_cmpsi_insn/1	[length = 4]
	bge	.L2	@ 8	*arm_cond_branch	[length = 4]
	@ basic block 3
	bl	bar1	@ 10	*call_symbol	[length = 4]
	ldr	r3, [r4, #0]	@ 12	*arm_movsi_insn/5	[length = 4]
	cmp	r3, #0	@ 13	*arm_cmpsi_insn/1	[length = 4]
	movlt	r3, #0	@ 17	neon_vornv2di+78/2	[length = 4]
	strlt	r3, [r4, #0]	@ 18	neon_vornv2di+78/6	[length = 4]
	ldmfd	sp!, {r4, pc}	@ 71	return	[length = 12]
.L2:
	@ basic block 4
	bl	bar2	@ 23	*call_symbol	[length = 4]
	ldr	r3, [r4, #0]	@ 25	*arm_movsi_insn/5	[length = 4]
	cmp	r3, #0	@ 26	*arm_cmpsi_insn/1	[length = 4]
	ldmgefd	sp!, {r4, pc}	@ 27	*cond_return	[length = 12]
	@ basic block 5
	mov	r3, #0	@ 30	*arm_movsi_insn/2	[length = 4]
	str	r3, [r4, #0]	@ 31	*arm_movsi_insn/6	[length = 4]
	ldmfd	sp!, {r4, pc}	@ 73	return	[length = 12]
.L7:
	.align	2
.L6:
	.word	a
	.word	b
	.size	foo, .-foo
	.comm	a,4,4
	.comm	b,4,4
	.ident	"GCC: (GNU) 4.5.0 20090606 (experimental) [trunk revision 148236]"



Note the conditional return at the end of basic block 3.  It voids a crossjumping opportunity and results in bigger code compared with a direct branch to a shared return instruction.  This comes from threading the return instruction in prologue/epilogue threading.  With a patch to disable this transformation when optimizing for size, I get this code:

	.file	"t.c"
	.text
	.align	2
	.global	foo
	.type	foo, %function
foo:
	@ args = 0, pretend = 0, frame = 0
	@ frame_needed = 0, uses_anonymous_args = 0
	@ basic block 2
	ldr	r3, .L9	@ 67	*arm_movsi_insn/5	[length = 4]
	stmfd	sp!, {r4, lr}	@ 69	*push_multi	[length = 4]
	ldr	r3, [r3, #0]	@ 6	*arm_movsi_insn/5	[length = 4]
	ldr	r4, .L9+4	@ 62	*arm_movsi_insn/5	[length = 4]
	cmp	r3, #0	@ 7	*arm_cmpsi_insn/1	[length = 4]
	bge	.L2	@ 8	*arm_cond_branch	[length = 4]
	@ basic block 3
	bl	bar1	@ 10	*call_symbol	[length = 4]
	b	.L7	@ 87	*arm_jump	[length = 4]
.L2:
	@ basic block 4
	bl	bar2	@ 23	*call_symbol	[length = 4]
.L7:
	@ basic block 5
	ldr	r3, [r4, #0]	@ 25	*arm_movsi_insn/5	[length = 4]
	cmp	r3, #0	@ 26	*arm_cmpsi_insn/1	[length = 4]
	movlt	r3, #0	@ 30	neon_vornv2di+78/2	[length = 4]
	strlt	r3, [r4, #0]	@ 31	neon_vornv2di+78/6	[length = 4]
	ldmfd	sp!, {r4, pc}	@ 72	return	[length = 12]
.L10:
	.align	2
.L9:
	.word	a
	.word	b
	.size	foo, .-foo
	.comm	a,4,4
	.comm	b,4,4
	.ident	"GCC: (GNU) 4.5.0 20090606 (experimental) [trunk revision 148236]"


Basic block 3 now ends in a direct jump and the similar code is cross-jumped.  

The size of the unpatched code (sum of the reported insn lengths) is 100 for the unpatched code, and 64 bytes for the patched code.

This is the patch:

Index: ../../trunk/gcc/function.c
===================================================================
--- ../../trunk/gcc/function.c	(revision 148236)
+++ ../../trunk/gcc/function.c	(working copy)
@@ -5022,13 +5022,18 @@
 
   rtl_profile_for_bb (EXIT_BLOCK_PTR);
 #ifdef HAVE_return
-  if (optimize && HAVE_return)
+  if (HAVE_return && optimize_function_for_speed_p (cfun))
     {
       /* If we're allowed to generate a simple return instruction,
 	 then by definition we don't need a full epilogue.  Examine
 	 the block that falls through to EXIT.   If it does not
-	 contain any code, examine its predecessors and try to
-	 emit (conditional) return instructions.  */
+	 contain any code, and we are optimizing for speed, then
+	 examine its predecessors and try to emit (conditional)
+	 return instructions.  If optimizing for size, conditional
+	 returns are usually not a win, because they can interfere
+	 with crossjumping opportunities, and because there may be
+	 registers to restore from the stack in the return insns
+	 itself (such as the ARM return instruction).  */
 
       basic_block last;
       rtx label;


---


### compiler : `gcc`
### title : `Nonoptimal save/restore registers`
### open_at : `2009-06-06T21:09:23Z`
### last_modified_date : `2021-09-09T00:45:00Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=40363
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.5.0`
### severity : `enhancement`
### contents :
IMHO, current save/restore registers strategy is not optimal. Look:

# cat test.c

#include <stdio.h>
void print(char *mess, char *format, int text)
{
	printf(mess);
	printf(format,text);
}
void main()
{
	print("X=","%d\n",1);
}

# gcc --version
gcc (GCC) 4.5.0 20090601 (experimental)
# gcc -o test test.c -O2
# objdump -d test

00000000004004d0 <print>:
  4004d0:	48 89 5c 24 f0       	mov    %rbx,-0x10(%rsp)    <----
  4004d5:	48 89 6c 24 f8       	mov    %rbp,-0x8(%rsp)    <----
  4004da:	48 89 f3             	mov    %rsi,%rbx
  4004dd:	48 83 ec 18          	sub    $0x18,%rsp    <----
  4004e1:	89 d5                	mov    %edx,%ebp
  4004e3:	31 c0                	xor    %eax,%eax
  4004e5:	e8 ce fe ff ff       	callq  4003b8 <printf@plt>
  4004ea:	89 ee                	mov    %ebp,%esi
  4004ec:	48 89 df             	mov    %rbx,%rdi
  4004ef:	48 8b 6c 24 10       	mov    0x10(%rsp),%rbp    <----
  4004f4:	48 8b 5c 24 08       	mov    0x8(%rsp),%rbx    <----
  4004f9:	31 c0                	xor    %eax,%eax
  4004fb:	48 83 c4 18          	add    $0x18,%rsp    <----
  4004ff:	e9 b4 fe ff ff       	jmpq   4003b8 <printf@plt>

=========

Let's replace current save/restore:

48 89 5c 24 f0       	mov    %rbx,-0x10(%rsp)
48 89 6c 24 f8       	mov    %rbp,-0x8(%rsp)
48 83 ec 18          	sub    $0x18,%rsp
...
48 8b 6c 24 10       	mov    0x10(%rsp),%rbp
48 8b 5c 24 08       	mov    0x8(%rsp),%rbx
48 83 c4 18          	add    $0x18,%rsp

to faster and short new save/restore:

55                   	push   %rbp
53                   	push   %rbx
53                   	push   %rbx	; dummy push
...
5b                   	pop    %rbx	; dummy pop
5b                   	pop    %rbx
5d                   	pop    %rbp
 
IMPOTANT note: For faster execution, "dummy push" have to use same register as previous push!

Measurement results on Core2: new save/restore 5 ticks faster then carrent one.

Regards,
 Vladimir Volynsky


---


### compiler : `gcc`
### title : `use stm and ldm to access consecutive memory words`
### open_at : `2009-06-16T09:06:49Z`
### last_modified_date : `2023-01-14T00:16:44Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=40457
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.5.0`
### severity : `enhancement`
### contents :
Current gcc can't make use of stm and ldm to reduce code size.


---


### compiler : `gcc`
### title : `Inefficient code on insn with fixed hard register`
### open_at : `2009-06-17T18:38:18Z`
### last_modified_date : `2021-08-08T05:40:15Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=40480
### status : `RESOLVED`
### tags : `missed-optimization, ra`
### component : `rtl-optimization`
### version : `4.5.0`
### severity : `normal`
### contents :
Gcc 4.5.0 revision 148602 generates:

[hjl@gnu-6 intrin-1]$ cat y.c
#include <x86intrin.h>

unsigned long long
foo1 (int x)
{
  return _rdpmc (x);
}
[hjl@gnu-6 intrin-1]$ /export/build/gnu/gcc-intrin/build-x86_64-linux/gcc/xgcc -B/export/build/gnu/gcc-intrin/build-x86_64-linux/gcc/  -O2 -S y.c -m32
[hjl@gnu-6 intrin-1]$ cat y.s
	.file	"y.c"
	.text
	.p2align 4,,15
.globl foo1
	.type	foo1, @function
foo1:
	pushl	%ebp
	movl	%esp, %ebp
	movl	8(%ebp), %ecx
	rdpmc
	popl	%ebp
	ret
	.size	foo1, .-foo1

when we use ECX during expand. If I let RA to allocate
register with

Index: i386.md
===================================================================
--- i386.md	(revision 6164)
+++ i386.md	(working copy)
@@ -22681,11 +22681,17 @@
   rtx reg = gen_reg_rtx (DImode);
   rtx si;
 
+#if 0
   /* Force operand 1 into ECX.  */
   rtx ecx = gen_rtx_REG (SImode, CX_REG);
   emit_insn (gen_rtx_SET (VOIDmode, ecx, operands[1]));
   si = gen_rtx_UNSPEC_VOLATILE (DImode, gen_rtvec (1, ecx),
 				UNSPECV_RDPMC);
+#else
+  rtx op1 = force_reg (SImode, operands[1]);
+  si = gen_rtx_UNSPEC_VOLATILE (DImode, gen_rtvec (1, op1),
+				UNSPECV_RDPMC);
+#endif
 
   if (TARGET_64BIT)
     {

I got

---
[hjl@gnu-6 intrin-1]$ /export/build/gnu/gcc-intrin/build-x86_64-linux/gcc/xgcc -B/export/build/gnu/gcc-intrin/build-x86_64-linux/gcc/  -O2 -S y.c -m32
[hjl@gnu-6 intrin-1]$ more y.s
	.file	"y.c"
	.text
	.p2align 4,,15
.globl foo1
	.type	foo1, @function
foo1:
	pushl	%ebp
	movl	%esp, %ebp
	movl	8(%ebp), %eax <<------ extra insn
	movl	%eax, %ecx
	rdpmc
	popl	%ebp
	ret
	.size	foo1, .-foo1
---

It seems that RA/reload handle insns with hard register
poorly if we don't assign hard register before hand.


---


### compiler : `gcc`
### title : `[missed optimization] branch to return not threaded on thumb`
### open_at : `2009-06-20T03:52:02Z`
### last_modified_date : `2023-09-25T06:43:20Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=40499
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.5.0`
### severity : `enhancement`
### contents :
If the function epilogue has only one return instruction, then the branch to return can be replaced by the return instruction directly.


---


### compiler : `gcc`
### title : `efficiency problem with V2HI add`
### open_at : `2009-06-29T15:06:09Z`
### last_modified_date : `2021-08-29T22:49:27Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=40589
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.3.0`
### severity : `enhancement`
### contents :
I am working on a port for the TriMedia processor family, and I was playing around with the following example (extracted from gcc.c-torture/execute/simd-2.c) to see how well our port takes advantage of the addv2hi3 operator of our tm3271 processor.

test.c:
...
typedef short __attribute__((vector_size (N))) vecint;
vecint i, j, k;
void f () {  k = i + j; }
...

test.c.016veclower, N=4. This looks good, the addv2hi3 has been used once.
...
  vector short int k.2;
  vector short int j.1;
  vector short int i.0;
  i.0 = i;
  j.1 = j;
  k.2 = i.0 + j.1;
  k = k.2;
}
...

test.c.016veclower, N=32. This also looks good, the addv2hi3 has been used 8x.
...
  vector short unsigned int D.1445;
  vector short unsigned int D.1444;
  vector short unsigned int D.1443;
  vector short unsigned int D.1442;
  vector short unsigned int D.1441;
  vector short unsigned int D.1440;
  vector short unsigned int D.1439;
  vector short unsigned int D.1438;
  vector short unsigned int D.1437;
  vector short unsigned int D.1436;
  vector short unsigned int D.1435;
  vector short unsigned int D.1434;
  vector short unsigned int D.1433;
  vector short unsigned int D.1432;
  vector short unsigned int D.1431;
  vector short unsigned int D.1430;
  vector short unsigned int D.1429;
  vector short unsigned int D.1428;
  vector short unsigned int D.1427;
  vector short unsigned int D.1426;
  vector short unsigned int D.1425;
  vector short unsigned int D.1424;
  vector short unsigned int D.1423;
  vector short unsigned int D.1422;
  vector short int k.2;
  vector short int j.1;
  vector short int i.0;
  i.0 = i;
  j.1 = j;
  D.1422 = BIT_FIELD_REF <i.0, 32, 0>;
  D.1423 = BIT_FIELD_REF <j.1, 32, 0>;
  D.1424 = D.1422 + D.1423;
  D.1425 = BIT_FIELD_REF <i.0, 32, 32>;
  D.1426 = BIT_FIELD_REF <j.1, 32, 32>;
  D.1427 = D.1425 + D.1426;
  D.1428 = BIT_FIELD_REF <i.0, 32, 64>;
  D.1429 = BIT_FIELD_REF <j.1, 32, 64>;
  D.1430 = D.1428 + D.1429;
  D.1431 = BIT_FIELD_REF <i.0, 32, 96>;
  D.1432 = BIT_FIELD_REF <j.1, 32, 96>;
  D.1433 = D.1431 + D.1432;
  D.1434 = BIT_FIELD_REF <i.0, 32, 128>;
  D.1435 = BIT_FIELD_REF <j.1, 32, 128>;
  D.1436 = D.1434 + D.1435;
  D.1437 = BIT_FIELD_REF <i.0, 32, 160>;
  D.1438 = BIT_FIELD_REF <j.1, 32, 160>;
  D.1439 = D.1437 + D.1438;
  D.1440 = BIT_FIELD_REF <i.0, 32, 192>;
  D.1441 = BIT_FIELD_REF <j.1, 32, 192>;
  D.1442 = D.1440 + D.1441;
  D.1443 = BIT_FIELD_REF <i.0, 32, 224>;
  D.1444 = BIT_FIELD_REF <j.1, 32, 224>;
  D.1445 = D.1443 + D.1444;
  k.2 = {D.1424, D.1427, D.1430, D.1433, D.1436, D.1439, D.1442, D.1445};
  k = k.2;
...

test.c.016veclower, N=8. This does not look good. The addv2hi3 has not been used. The addsi3 has been used 4 times, while the addv2hi3 could have been used only 2 times.
...
  short int D.1431;
  short int D.1430;
  short int D.1429;
  short int D.1428;
  short int D.1427;
  short int D.1426;
  short int D.1425;
  short int D.1424;
  short int D.1423;
  short int D.1422;
  short int D.1421;
  short int D.1420;
  vector short int k.2;
  vector short int j.1;
  vector short int i.0;
  i.0 = i;
  j.1 = j;
  D.1420 = BIT_FIELD_REF <i.0, 16, 0>;
  D.1421 = BIT_FIELD_REF <j.1, 16, 0>;
  D.1422 = D.1420 + D.1421;
  D.1423 = BIT_FIELD_REF <i.0, 16, 16>;
  D.1424 = BIT_FIELD_REF <j.1, 16, 16>;
  D.1425 = D.1423 + D.1424;
  D.1426 = BIT_FIELD_REF <i.0, 16, 32>;
  D.1427 = BIT_FIELD_REF <j.1, 16, 32>;
  D.1428 = D.1426 + D.1427;
  D.1429 = BIT_FIELD_REF <i.0, 16, 48>;
  D.1430 = BIT_FIELD_REF <j.1, 16, 48>;
  D.1431 = D.1429 + D.1430;
  k.2 = {D.1422, D.1425, D.1428, D.1431};
  k = k.2;
...

This grep illustrates that the problem only occurs for N=8/16:
...
$ for N in 4 8 16 32 64; do \
  rm -f *.c.* ; \
  cc1 test.c -quiet -march=tm3271 -O2 -DN=${N} \
      -fdump-rtl-all -fdump-tree-all \
  && grep -c '+' test.c.016t.veclower ; \
done
1
4
8
8
16
...

So why does the problem occur? Lets look at the TYPE_MODE (type) in expand_vector_operations_1() for different values of N:
...
N=4  V2HI
N=8  DImode
N=16 TImode
N=32 BLKmode
N=64 BLKmode
...

For the DImode and TImode, we don't generate efficient code, due to the test on BLKmode:
...
  /* For very wide vectors, try using a smaller vector mode.  */
  compute_type = type;
  if (TYPE_MODE (type) == BLKmode && op)
...
in expand_vector_operations_1(). For my target, which has a native addv2hi3 operator, also DImode/TImode can be considered a 'wide vector'.

Using this patch, I also generate addv2hi3 for N=8/N=16: 
...
Index: tree-vect-generic.c
===================================================================
--- tree-vect-generic.c (revision 14)
+++ tree-vect-generic.c (working copy)
@@ -462,7 +462,7 @@
 
   /* For very wide vectors, try using a smaller vector mode.  */
   compute_type = type;
-  if (TYPE_MODE (type) == BLKmode && op)
+  if (op)
     {
       tree vector_compute_type
         = type_for_widest_vector_mode (TYPE_MODE (TREE_TYPE (type)), op,
...


Furthermore, I think this patch (in the style of expmed.c:extract_bit_field_1()) could be useful:
...
Index: tree-vect-generic.c
===================================================================
--- tree-vect-generic.c (revision 14)
+++ tree-vect-generic.c (working copy)
@@ -35,6 +35,7 @@
 #include "tree-pass.h"
 #include "flags.h"
 #include "ggc.h"
+#include "target.h"
 
 
 /* Build a constant of type TYPE, made of VALUE's bits replicated
@@ -369,6 +370,7 @@
   for (; mode != VOIDmode; mode = GET_MODE_WIDER_MODE (mode))
     if (GET_MODE_INNER (mode) == inner_mode
         && GET_MODE_NUNITS (mode) > best_nunits
+       && targetm.vector_mode_supported_p(mode)
        && optab_handler (op, mode)->insn_code != CODE_FOR_nothing)
       best_mode = mode, best_nunits = GET_MODE_NUNITS (mode);
...
It automatically disables a addv4hi3 if v4hi is disabled in TARGET_VECTOR_MODE_SUPPORTED_P.


---


### compiler : `gcc`
### title : `Optimizing for pentium-m gives worse code than optimizing for i486`
### open_at : `2009-07-03T18:27:47Z`
### last_modified_date : `2021-08-29T22:50:09Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=40644
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `target`
### version : `4.5.0`
### severity : `normal`
### contents :
Try compiling the attached program with the following options (they differ only in -march specification)

1. gcc -std=c99 -march=i486 -funroll-loops -fprefetch-loop-arrays -ftree-vectorize -O3 -o gen_weyl_group gen_weyl_group.c
2. gcc -std=c99 -march=i686 -funroll-loops -fprefetch-loop-arrays -ftree-vectorize -O3 -o gen_weyl_group gen_weyl_group.c
3. gcc -std=c99 -march=pentium-m -funroll-loops -fprefetch-loop-arrays -ftree-vectorize -O3 -o gen_weyl_group gen_weyl_group.c

 With my notebook (CPU core is Dothan) I get the following execution times:
i486  37.510
i686  37.534
p-m   53.959

Results for i486 and i686 are roughly the same, but compiling for pentium-m results in a seriously degraded performance.

I first noted this behaviour with gcc 4.3.3 that is my system's stock compiler; the abovementioned times were measured for 4.5.0-svn149207, so, probably, all versions from 4.3 to 4.5 are affected by this bug.

GCC 4.5.0, used to compile the tests, was configured with the following options:

--prefix=/home/artem/testing/gcc45 --enable-shared --enable-bootstrap --enable-languages=c --enable-threads=posix --enable-checking=release --with-system-zlib --with-gnu-ld --verbose --with-arch=i686


---


### compiler : `gcc`
### title : `extra register move`
### open_at : `2009-07-08T09:36:27Z`
### last_modified_date : `2021-09-27T00:24:01Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=40680
### status : `NEW`
### tags : `missed-optimization, ra`
### component : `target`
### version : `4.5.0`
### severity : `normal`
### contents :
Compile the attached source code with options -Os -mthumb -march=armv5te, gcc generates:

        push    {r3, r4, r5, lr}
.LCFI0:
        mov     r4, r0
        ldr     r0, [r0]
        bl      _Z3foof
        ldr     r1, [r4, #4]
        @ sp needed for prologue
        add     r5, r0, #0
        bl      _Z3barfi
        mov     r0, r5           // *
        bl      _Z3fffi          // *
        mov     r4, r5           // *
        mov     r5, r0           // *
        mov     r0, r4           // *
        bl      _Z3fffi          // *
        mov     r1, r0           // *
        mov     r0, r5           // *
        bl      _Z3setii
        pop     {r3, r4, r5, pc}

There is an obvious extra register move (mov r4, r5) in the marked section, a better code sequence of the marked section could be:

        mov     r0, r5
        bl      _Z3fffi
        mov     r4, r0
        mov     r0, r5
        bl      _Z3fffi
        mov     r1, r0
        mov     r0, r4

The marked code sequence before scheduler is:

        mov     r4, r5
        mov     r0, r5
        bl      _Z3fffi
        mov     r5, r0
        mov     r0, r4
        bl      _Z3fffi
        mov     r1, r0
        mov     r0, r5

The instruction (mov r4, r5 ) is generated by register allocator. I don't know why RA generates this instruction.


---


### compiler : `gcc`
### title : `redundant memory load`
### open_at : `2009-07-13T08:57:35Z`
### last_modified_date : `2023-05-15T00:24:06Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=40730
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.5.0`
### severity : `normal`
### contents :
Compile the attached source code with options -Os -mthumb -march=armv5te -fno-strict-aliasing, Gcc generates:

iterate:
        push    {lr}
        ldr     r3, [r1]        // C
        b       .L5
.L4:
        ldr     r3, [r3, #8]    // D
.L5:
        str     r3, [r0]        //  A
        ldr     r3, [r0]        //  B
        cmp     r3, #0
        beq     .L3
        ldr     r2, [r3, #4]
        cmp     r2, #0
        beq     .L4
.L3:
        str     r3, [r0, #12]
        @ sp needed for prologue
        pop     {pc}

Pay attention to instructions marked as A and B. Instruction A store r3 to [r0] but insn B load it back to r3.

The instruction A was originally put after instruction C and D. After register allocation, they were allocated to the same registers and looks exactly same. In pass csa, cleanup_cfg was called and it found the same instructions and moved them before instruction B. Now instruction B is obviously redundant.

Is it OK to remove this kind of redundant code in pass dce?


---


### compiler : `gcc`
### title : `simple switch/case, if/else and arithmetics result in different code`
### open_at : `2009-07-14T17:09:16Z`
### last_modified_date : `2021-10-25T12:42:21Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=40748
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.5.0`
### severity : `enhancement`
### contents :
Tested r149624, 4.4.0 and 4.3.3

# ./gcc -v
Using built-in specs.
Target: x86_64-unknown-linux-gnu
Configured with: ../configure --enable-languages=c,c++ --prefix=/mnt/svn/gcc-trunk/build/
Thread model: posix
gcc version 4.5.0 20090714 (experimental) (GCC)

4.4.0 and 4.5 have better behaviour in the case of "switch"

The following code:
-------------------------------
unsigned f1(unsigned i)
{
	switch (i) {
		case 0: return 0;
		case 1: return 1;
		case 2: return 2;
		case 3: return 3;
		default: return 4;
	}
}

unsigned f2(unsigned i)
{
	if (i == 0) return 0;
	if (i == 1) return 1;
	if (i == 2) return 2;
	if (i == 3) return 3;
	return 4;
}

unsigned f3(unsigned i)
{
	return i < 4 ? i : 4;
}
-------------------------------

f1(), f2() and f3() do the same, but the resulting code differs a lot.


---


### compiler : `gcc`
### title : `Vectorization of complex types, vectorization of sincos missing`
### open_at : `2009-07-16T09:42:04Z`
### last_modified_date : `2020-09-22T11:31:00Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=40770
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.5.0`
### severity : `enhancement`
### contents :
The following should be vectorized with proper -mveclib:

float xf[1024];
float sf[1024];
float cf[1024];
void foo (void)
{
  int i;
  for (i = 0; i < 1024; ++i)
    {
      sf[i] = __builtin_sinf (xf[i]);
      cf[i] = __builtin_cosf (xf[i]);
    }
}

double xd[1024];
double sd[1024];
double cd[1024];
void bar (void)
{
  int i;
  for (i = 0; i < 1024; ++i)
    {
      sd[i] = __builtin_sin (xd[i]);
      cd[i] = __builtin_cos (xd[i]);
    }
}


---


### compiler : `gcc`
### title : `inefficient code to accumulate function return values`
### open_at : `2009-07-17T06:56:17Z`
### last_modified_date : `2021-07-26T08:07:21Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=40783
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.5.0`
### severity : `enhancement`
### contents :
Compile the following code with options -Os -mthumb -march=armv5te

union FloatIntUnion {
        float  fFloat;
        int fSignBitInt;
};

static inline float fast_inc(float x) {
      union FloatIntUnion data;
      data.fFloat = x;
      data.fSignBitInt += 1;
      return data.fFloat;
}

extern int MyConvert(float);
extern float dumm();
int time_math() {
      int i;
      int sum = 0;
      const int repeat = 100;
      float f;

      f = dumm();
      for (i = repeat - 1; i >= 0; --i) {
          sum += (int)f; f = fast_inc(f);
          sum += (int)f; f = fast_inc(f);
          sum += (int)f; f = fast_inc(f);
          sum += (int)f; f = fast_inc(f);
      }

      f = dumm();
      for (i = repeat - 1; i >= 0; --i) {
        sum += MyConvert(f); f = fast_inc(f);
        sum += MyConvert(f); f = fast_inc(f);
        sum += MyConvert(f); f = fast_inc(f);
      }
      return sum;
}

Gcc generates:

        push    {r4, r5, r6, r7, lr}
        sub     sp, sp, #12
        bl      dumm
        mov     r4, #0
        mov     r6, #99
        add     r5, r0, #0
.L2:
        add     r0, r5, #0
        bl      __aeabi_f2iz
        add     r5, r5, #1
        add     r4, r0, r4
        add     r0, r5, #0
        bl      __aeabi_f2iz
        add     r5, r5, #1
        add     r4, r4, r0
        add     r0, r5, #0
        bl      __aeabi_f2iz
        add     r5, r5, #1
        add     r4, r4, r0
        add     r0, r5, #0
        bl      __aeabi_f2iz
        add     r5, r5, #1
        add     r4, r4, r0
        sub     r6, r6, #1
        bcs     .L2
        bl      dumm
        mov     r6, #99
        add     r5, r0, #0
.L3:
        add     r0, r5, #0
        bl      MyConvert
        add     r5, r5, #1
        str     r0, [sp, #4]
        add     r0, r5, #0
        bl      MyConvert
        add     r5, r5, #1
        mov     r7, r0
        add     r0, r5, #0
        bl      MyConvert
        ldr     r3, [sp, #4]
        add     r5, r5, #1
        add     r7, r7, r3
        add     r7, r7, r0
        add     r4, r4, r7
        sub     r6, r6, #1
        bcs     .L3
        add     sp, sp, #12
        mov     r0, r4
        @ sp needed for prologue
        pop     {r4, r5, r6, r7, pc}

The source code contains 2 similar loops. But the generated code are quite different. The code for first loop is as expected. After evaluating each function, accumulates the returned value immediately. The code for second loop is much worse. After evaluating each function, it saves the returned value to a different place. After calling all functions in the same round of loop, it accumulates all the saved results together. The code for second loop is larger and slower, and even caused a register spilling.

The intermediate representation patterns for the two loops started to diverge from pass float2int.c.078t.reassoc1. I don't know why gcc performs different transforms on the two loops in this pass.


---


### compiler : `gcc`
### title : `Poor register class choice in IRA`
### open_at : `2009-07-23T21:31:59Z`
### last_modified_date : `2022-03-08T16:20:41Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=40842
### status : `UNCONFIRMED`
### tags : `missed-optimization, ra`
### component : `rtl-optimization`
### version : `4.5.0`
### severity : `normal`
### contents :
Moving this issue from bz 39976 since it is a separate problem than the original documented there.

Verified the behavior still exists using current trunk revision (150020).  The testcase comes from cpu2000 sixtrack benchmark. Following is original comment I posted:

=======
The attatched testcase exhibits the problem with the load-hit-store. It's
resulting from choosing a bad register class (GENERAL_REGS) for a pseudo that
should get assigned to FLOAT_REGS. Since there is no FPR -> GPR move for
-mcpu=power6 the copy must go through memory.  I compiled the testcase with
-m64 -O3 -mcpu=power6 using trunk revision 149376.  The pseudo in question is
361.

Following are the 3 insns referencing reg 361 in the sched1 dump (before ira):

(insn 51 238 241 8 thin6d_reduced.f:178 (set (reg:DF 361 [ prephitmp.35 ])
        (reg:DF 358 [ prephitmp.35 ])) 351 {*movdf_hardfloat64} (nil))
...
(insn 47 46 231 9 thin6d_reduced.f:178 (set (reg:DF 361 [ prephitmp.35 ])
        (reg:DF 179 [ prephitmp.35 ])) 351 {*movdf_hardfloat64} (nil))
...
(insn 196 194 198 11 thin6d_reduced.f:169 (set (mem/c/i:DF (plus:DI (reg/f:DI
477)
                (const_int 56 [0x38])) [2 crkve+0 S8 A64])
        (reg:DF 361 [ prephitmp.35 ])) 351 {*movdf_hardfloat64}
(expr_list:REG_DEAD (reg:DF 361 [ prephitmp.35 ])
        (nil)))


And from the ira dump:

Pass1 cost computation:
    a71 (r361,l1) best GENERAL_REGS, cover GENERAL_REGS
    a3 (r361,l0) best GENERAL_REGS, cover GENERAL_REGS
  a3(r361,l0) costs: BASE_REGS:0,0 GENERAL_REGS:0,0 FLOAT_REGS:0,0
LINK_REGS:156,1836 CTR_REGS:156,1836 SPECIAL_REGS:156,1836 MEM:156
  a71(r361,l1) costs: BASE_REGS:0,0 GENERAL_REGS:0,0 FLOAT_REGS:0,0
LINK_REGS:1680,1680 CTR_REGS:1680,1680 SPECIAL_REGS:1680,1680 MEM:1120


Pass 2 cost computation:
    r361: preferred GENERAL_REGS, alternative NO_REGS
  a3(r361,l0) costs: BASE_REGS:0,2240 GENERAL_REGS:0,2240 FLOAT_REGS:312,2552
LINK_REGS:234,4154 CTR_REGS:234,4154 SPECIAL_REGS:234,4154 MEM:156
  a71(r361,l1) costs: BASE_REGS:2240,2240 GENERAL_REGS:2240,2240
FLOAT_REGS:2240,2240 LINK_REGS:3920,3920 CTR_REGS:3920,3920
SPECIAL_REGS:3920,3920 MEM:3360


---


### compiler : `gcc`
### title : `ARM and PPC truncate intermediate operations unnecessarily`
### open_at : `2009-07-28T16:28:10Z`
### last_modified_date : `2021-12-13T08:55:22Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=40893
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.4.0`
### severity : `enhancement`
### contents :
Consider the following C code:

#include <inttypes.h>

void dct2x2dc_dconly( int16_t d[2][2] )
{
    int d0 = d[0][0] + d[0][1];
    int d1 = d[1][0] + d[1][1];
    d[0][0] = d0 + d1;
    d[0][1] = d0 - d1;
}

The following is generated with arm-none-linux-gnueabi-gcc-4.4.0 -O3 -mcpu=cortex-a8 -S
dct2x2dc_dconly:
	ldrsh	ip, [r0, #2]
	ldrsh	r3, [r0, #0]
	ldrsh	r1, [r0, #6]
	ldrsh	r2, [r0, #4]
	add	r3, ip, r3
	add	r2, r1, r2
	uxth	r3, r3
	uxth	r2, r2
	rsb	r1, r2, r3
	add	r3, r2, r3
	strh	r1, [r0, #2]	@ movhi
	strh	r3, [r0, #0]	@ movhi
	bx	lr
(with pre-armv6 targets the two uxth are replaced by asl #16, lsr #16 pairs.)

The following is generated with powerpc-unknown-linux-gnu-gcc-4.4.0 -O3 -mcpu=G4 -S
dct2x2dc_dconly:
	lha 10,2(3)
	lha 0,0(3)
	lha 11,6(3)
	lha 9,4(3)
	add 0,10,0
	rlwinm 0,0,0,0xffff
	add 9,11,9
	rlwinm 9,9,0,0xffff
	subf 11,9,0
	add 0,9,0
	sth 11,2(3)
	sth 0,0(3)
	blr

The two uxth in the ARM version, and the two rlwinm in the PPC version are completely unnecessary, as letting strh/sth truncate will give equivalent results. x86 does not exhibit this behaviour, and removing either d0 + d1 or d0 - d1 will not cause d0 and d1 be truncated to to 16 bits on both ARM and PPC.

powerpc-unknown-linux-gnu-gcc-4.4.0 -v
Using built-in specs.
Target: powerpc-unknown-linux-gnu
Configured with: /var/tmp/portage/sys-devel/gcc-4.4.0/work/gcc-4.4.0/configure --prefix=/usr --bindir=/usr/powerpc-unknown-linux-gnu/gcc-bin/4.4.0 --includedir=/usr/lib/gcc/powerpc-unknown-linux-gnu/4.4.0/include --datadir=/usr/share/gcc-data/powerpc-unknown-linux-gnu/4.4.0 --mandir=/usr/share/gcc-data/powerpc-unknown-linux-gnu/4.4.0/man --infodir=/usr/share/gcc-data/powerpc-unknown-linux-gnu/4.4.0/info --with-gxx-include-dir=/usr/lib/gcc/powerpc-unknown-linux-gnu/4.4.0/include/g++-v4 --host=powerpc-unknown-linux-gnu --build=powerpc-unknown-linux-gnu --enable-altivec --disable-fixed-point --without-ppl --without-cloog --disable-nls --with-system-zlib --disable-checking --disable-werror --enable-secureplt --disable-multilib --disable-libmudflap --disable-libssp --enable-libgomp --enable-cld --disable-libgcj --enable-languages=c,c++,fortran --enable-shared --enable-threads=posix --enable-__cxa_atexit --enable-clocale=gnu --with-bugurl=http://bugs.gentoo.org/ --with-pkgversion='Gentoo 4.4.0 p1.1'
Thread model: posix
gcc version 4.4.0 (Gentoo 4.4.0 p1.1) 

arm-none-linux-gnueabi-gcc-4.4.0 -v
Using built-in specs.
Target: arm-none-linux-gnueabi
Configured with: ../gcc-4.4.0/configure --target=arm-none-linux-gnueabi --prefix=/usr/local/arm --enable-threads --with-sysroot=/usr/local/arm/arm-none-linux-gnueabi/libc
Thread model: posix
gcc version 4.4.0 (GCC)


---


### compiler : `gcc`
### title : `missed merge of basic blocks`
### open_at : `2009-08-08T00:09:51Z`
### last_modified_date : `2019-09-05T04:29:45Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=41004
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.5.0`
### severity : `normal`
### contents :
Compile the attached source code with options -Os -march=armv5te -mthumb
Gcc generates following code snippet:

      ...
       cmp     r0, r2
       bne     .L5
       b       .L15                            <--- A
.L9:
       ldr     r3, [r1]
       cmp     r3, #0
       beq     .L7
       str     r0, [r1, #8]
       b       .L8
.L7:
       str     r3, [r1, #8]
.L8:
       ldr     r1, [r1, #4]
       b       .L12                          <---- C
.L15:
       mov     r0, #1                       <--- B
.L12:
       cmp     r1, r2                       <---- D
       bne     .L9
       ...

inst A jump to B then fall through to D
inst C jump to D

there is no other instructions jump to instruction B, so we can put inst B just before A, then A jump to D, and C can be removed.

There are two possible functions can potentially do this optimization. They are merge_blocks_move and try_forward_edges. 

Function try_forward_edges can only redirect a series of forwarder blocks. It can't move the target blocks before the forwarder blocks.

In function merge_blocks_move only when both block b and c aren't forwarder blocks then can they be merged. In this case block A is a forwarder block, so they are not merged.


---


### compiler : `gcc`
### title : `invariant address load inside loop with -Os.`
### open_at : `2009-08-10T13:08:46Z`
### last_modified_date : `2022-01-05T10:24:33Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=41026
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.4.1`
### severity : `enhancement`
### contents :
gcc --version
gcc (GCC) 4.4.1 20090507 (prerelease)

The following test compiled with
gcc -S -Os

struct struct_t {
  int* data;
};

void testAddr (struct struct_t* sp, int len)
{
    int i;
    for (i = 0; i < len; i++)
      {
        sp->data[i] = 0;
      }
}

generates the following code for x86

testAddr :
	pushl	%ebp
	xorl	%eax, %eax
	movl	%esp, %ebp
	movl	8(%ebp), %ecx
	pushl	%ebx
	movl	12(%ebp), %edx
	jmp	.L2
.L3:
	movl	(%ecx), %ebx          <-- invariant address load
	movl	$0, (%ebx,%eax,4)
	incl	%eax
.L2:
	cmpl	%edx, %eax
	jl	.L3
	popl	%ebx
	popl	%ebp
	ret

Whereas making the intent explicit like so

void testAddr (struct struct_t* sp, int len)
{
    int i;
    int *p = sp->data;
    for (i = 0; i < len; i++)
      {
        p[i] = 0;
      }
}

generates

testAddr :
	pushl	%ebp
	movl	%esp, %ebp
	movl	8(%ebp), %eax
	movl	12(%ebp), %ecx
	movl	(%eax), %edx          <-- now outside the loop
	xorl	%eax, %eax
	jmp	.L2
.L3:
	movl	$0, (%edx,%eax,4)
	incl	%eax
.L2:
	cmpl	%ecx, %eax
	jl	.L3
	popl	%ebp
	ret

Why can't we move the address load outside the loop in the first case?


---


### compiler : `gcc`
### title : `4x bigger object when compiled with -O3 option`
### open_at : `2009-08-17T19:52:40Z`
### last_modified_date : `2023-07-22T02:46:35Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=41095
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `target`
### version : `4.4.1`
### severity : `normal`
### contents :
Hi,

When I compile "libavcodec/dsputil.c" file from FFmpeg package with these options (-O2 -fipa-cp-clone -finline-functions -fgcse-after-reload -ftree-vectorize -fpredictive-commoning -funswitch-loops):

OPTFLAGS= -mnobitfield -m68060 -std=c99  -Wdeclaration-after-statement -Wdisabled-optimization -fno-math-errno -D_ISOC99_SOURCE -D_POSIX_C_SOURCE=200112 -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -fno-common -fomit-frame-pointer -Wall -Wno-switch -Wpointer-arith -Wredundant-decls -Wcast-qual -Wwrite-strings -Wundef -O2 -fipa-cp-clone -finline-functions -fgcse-after-reload -ftree-vectorize -fpredictive-commoning -funswitch-loops

I get "dsputil.o" with size of 306kb.

When I compile "dsputil.c" with -O3 option:

OPTFLAGS= -mnobitfield -m68060 -std=c99  -Wdeclaration-after-statement -Wdisabled-optimization -fno-math-errno -D_ISOC99_SOURCE -D_POSIX_C_SOURCE=200112 -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -fno-common -fomit-frame-pointer -Wall -Wno-switch -Wpointer-arith -Wredundant-decls -Wcast-qual -Wwrite-strings -Wundef -O3

I get "dsputil.o" with size of 1,18mb.


---


### compiler : `gcc`
### title : `We should be better in folding pow with integer powers`
### open_at : `2009-08-18T09:51:15Z`
### last_modified_date : `2021-09-14T07:02:13Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=41098
### status : `NEW`
### tags : `missed-optimization, xfail`
### component : `middle-end`
### version : `4.5.0`
### severity : `enhancement`
### contents :
There are a bunch of missed-optimizations in fold_builtin_pow where we restrict
foldings to cases of non-negative base even when the power is an integer.

One source of easy missed optimizations is that fold folds x * x to pow (x, 2.0)
instead of powi (x, 2) which would make further analysis easier.


---


### compiler : `gcc`
### title : `Tree-vectorizer: VecCost tuning for X2: Without vectorization 30% faster`
### open_at : `2009-08-19T07:46:53Z`
### last_modified_date : `2022-01-10T10:02:58Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=41115
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.5.0`
### severity : `normal`
### contents :
This is on an AMD Athlon(tm) 64 X2 Dual Core Processor 4800+  (using openSUSE Factory in x86-64 mode).

When compiling the Polyhedron "induct.f90" test case with and without vectorization, the run time with vectorization is 30% longer. I think the vectorization cost model needs to be tuned for this processor. (By comparison, with a Core2Duo, the run time doubles without vectorization.)

gfortran -march=native -ffast-math -O3 -ftree-vectorize -fvect-cost-model induct.f90
user    0m35.626s

gfortran -march=opteron -ffast-math -funroll-loops -ftree-vectorize -ftree-loop-linear -msse3 -O3 induct.f90; time ./a.out
real    0m36.676s, user    0m36.390s

gfortran -march=opteron -ffast-math -funroll-loops -fno-tree-vectorize -ftree-loop-linear -msse3 -O3 induct.f90; time ./a.out
real    0m28.000s, user    0m27.830s

(If you don't have the benchmark, it is available from http://www.polyhedron.co.uk/MFL6VW74649 )


The problem was detected when applying the patch http://gcc.gnu.org/ml/fortran/2009-08/msg00208.html. With that patch one has

induct.f90:5062: note: LOOP VECTORIZED.
induct.f90:5061: note: LOOP VECTORIZED.
induct.f90:5060: note: LOOP VECTORIZED.
induct.f90:5059: note: LOOP VECTORIZED.
induct.f90:5058: note: LOOP VECTORIZED.
induct.f90:5057: note: LOOP VECTORIZED.
induct.f90:4893: note: LOOP VECTORIZED.

and without the patch (and 30% slower):

induct.f90:1772: note: LOOP VECTORIZED.
induct.f90:1660: note: LOOP VECTORIZED.
induct.f90:2220: note: LOOP VECTORIZED.
induct.f90:2077: note: LOOP VECTORIZED.
induct.f90:3060: note: LOOP VECTORIZED.
induct.f90:2918: note: LOOP VECTORIZED.
induct.f90:2724: note: LOOP VECTORIZED.
induct.f90:2582: note: LOOP VECTORIZED.
induct.f90:5062: note: LOOP VECTORIZED.
induct.f90:5061: note: LOOP VECTORIZED.
induct.f90:5060: note: LOOP VECTORIZED.
induct.f90:5059: note: LOOP VECTORIZED.
induct.f90:5058: note: LOOP VECTORIZED.
induct.f90:5057: note: LOOP VECTORIZED.
induct.f90:4893: note: LOOP VECTORIZED.


---


### compiler : `gcc`
### title : `inefficient zeroing of an array`
### open_at : `2009-08-21T06:14:49Z`
### last_modified_date : `2021-12-26T05:51:45Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=41137
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.5.0`
### severity : `enhancement`
### contents :
triggered by some discussion in PR41113

SUBROUTINE S(a,n)
INTEGER :: n
REAL :: a(n,n,n,n)
a(:,:,:,:)=0.0
END SUBROUTINE

generates a four-fold look to do the zeroing, while it would be more efficient to zero n**4 elements starting from a(1,1,1,1). I.e. since a is contiguous in memory a memset or similar can be done (properly guarded for zero-sized arrays).

Note that the case with compile time constant bounds is already captured i.e. 

.LFB2:
        movl    $40000, %edx
        xorl    %esi, %esi
        jmp     memset
.LFE2:

is generated for 

SUBROUTINE S(a)
REAL :: a(10,10,10,10)
a(:,:,:,:)=0.0
END SUBROUTINE


---


### compiler : `gcc`
### title : `register allocator undoing optimal schedule`
### open_at : `2009-08-25T21:48:47Z`
### last_modified_date : `2021-12-19T00:03:15Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=41171
### status : `NEW`
### tags : `missed-optimization, ra`
### component : `rtl-optimization`
### version : `4.4.0`
### severity : `normal`
### contents :
When I compile the following code

void f(int *x, int *y){
  *x = 7;
  *y = 4;
}

at -O2 for Itanium, I get the following assembly:

f:
        .prologue
        .body
        .mmi
        addl r14 = 7, r0
        ;;
        st4 [r32] = r14
        addl r14 = 4, r0
        ;;
        .mib
        st4 [r33] = r14
        nop 0
        br.ret.sptk.many b0
        .endp f#

The expected output is

f:
        .prologue
        .body
        .mii
        addl r14 = 7, r0
        addl r15 = 4, r0
        ;;
        nop 0
        .mmb
        st4 [r32] = r14
        st4 [r33] = r15
        br.ret.sptk.many b0
        .endp f#

In the .sched1 dump, I see the expected schedule:

;;        0-->     7 r341=0x7                          :2_A
;;        0-->     9 r342=0x4                          :2_A
;;        1-->     8 [in0]=r341                        :2_M_only_um23
;;        1-->    10 [in1]=r342                        :2_M_only_um23
;;   total time = 1

but in the .ira dump, the RTL has reverted back to the serial code.  Because of the anti-dependency introduced by register allocation, the .mach dump shows an inferior schedule:

;;        0-->     7 r14=0x7                           :2_A
;;        1-->     8 [r32]=r14                         :2_M_only_um23
;;        1-->    21 r14=0x4                           :2_A
;;        2-->    10 [r33]=r14                         :2_M_only_um23
;;        2-->    25 {return;use b0;}                  :2_B
;;   total time = 2

In GCC 4.3.2 and 3.4.6, I see the lreg pass likewise creating an inferior schedule.  However, for PowerPC, MIPS, ARM, and FR-V, GCC 4.3.2 leaves the initial schedule intact, whereas GCC 4.4.0 changes the order of insns in the IRA pass for all targets.

For targets other than Itanium, I'm not sure this transformation in IRA degrades performance, and it reduces register pressure, so it seems like a positive change.  For Itanium, this degrades performance.  What's odd is that the Itanium port had this behavior prior to GCC 4.4.0, while other ports did not.  Is there some set of machine-specific parameters that the Itanium port could tune to prevent this transformation in IRA (hopefully without degrading performance elsewhere)?


---


### compiler : `gcc`
### title : `"&data[i] - data" isn't converted to "i"`
### open_at : `2009-09-03T13:49:16Z`
### last_modified_date : `2023-06-12T02:12:01Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=41244
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.5.0`
### severity : `enhancement`
### contents :
In attached code:
in find(), generated code computes offset using multiplication/division.
in set(), generated code computes &data[10] and compares &data[i] with that (to verify find() fails to be optimised because of overflow rules)

tested gcc: 4.3.4, 4.4.1, 4.5.0-alpha20090827

command line:
gcc main.c -o main.o -c -O3
-f(no-)strict-overflow or -m32 doesn't have any effect on that behaviour

---------------------------------
static struct {
	int a, b, c;
	char pad[200]; /* padding so offset computation has to use expensive div/mul */
} data[1000]; /* 1000 so loop isn't unrolled */

int find(int val)
{
	int i;
	for (i = 0; i < 1000; i++) {
		if (data[i].a == val) return &data[i] - data; /* does *212, /212 */
	}
	return -1;
}

void set(int val)
{
	int i;
	for (i = 0; i < 1000; i++) {
		data[i].b = &data[i] - data < 10 || data[i].a == val; /* compares with &data[10] */
	}
}
---------------------------------

Relevant generated ASM:
(eax is "i", sar+imul is converted division by 212)
---------------------------------
	cdqe
	imul	rax, rax, 212
	sar	rax, 2
	imul	eax, eax, -1944890851
	ret
---------------------------------


---


### compiler : `gcc`
### title : `XFAIL gcc.dg/tree-ssa/forwprop-12.c`
### open_at : `2009-09-09T14:58:24Z`
### last_modified_date : `2023-07-21T11:58:54Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=41320
### status : `RESOLVED`
### tags : `missed-optimization, testsuite-fail, xfail`
### component : `tree-optimization`
### version : `4.5.0`
### severity : `normal`
### contents :
We no longer propagate &(*a)[0] into the dereference in

int f(int *p, int n)
{
  int (*a)[n] = (int (*)[n])p;
  int *q = &(*a)[0];
  return q[1];
}

because 1) the C frontend decomposes &(*a)[0] into address arithmetic and
2) because of the fix for PR41317 we no longer fold (int *)a to &(*a)[0].


---


### compiler : `gcc`
### title : `missed space optimization related to basic block reorder`
### open_at : `2009-09-18T07:56:08Z`
### last_modified_date : `2019-09-09T08:01:33Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=41396
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.5.0`
### severity : `enhancement`
### contents :
Compile the attached source code with options -march=armv5te -mthumb -Os, I got

        push    {r4, lr}
        ldr     r4, [r0, #8]
        ldr     r3, [r0, #4]
        b       .L2
.L7:
        ldr     r2, [r3, #8]
        ldr     r1, [r2]
        ldr     r2, [r3]
        add     r2, r1, r2
        ldr     r1, [r3, #4]
        ldr     r1, [r1]
        sub     r2, r2, r1
        ldr     r1, [r3, #12]
        cmp     r1, #1
        beq     .L4
        cmp     r1, #2
        bne     .L3
        b       .L12       // C
.L4:                       // ---------BEGIN BLOCK B
        ldr     r1, [r0]
        neg     r1, r1
        cmp     r2, r1
        bge     .L3
        b       .L9        // ----------END BLOCK B
.L12:                      // ---------------BEGIN BLOCK A-------
        ldr     r1, [r0]
        cmp     r2, r1
        bgt     .L9
.L3:
        add     r3, r3, #16
.L2:
        cmp     r3, r4
        bcc     .L7
        mov     r0, #0
        b       .L6      // -----------------END BLOCK A---------
.L9:
        mov     r0, #1
.L6:
        @ sp needed for prologue
        pop     {r4, pc}


If we change the order of block A and block B, we can remove 2 branch instructions, inst C and another inst at the end of block B.

Need new basic block reorder algorithm for code size optimization?


---


### compiler : `gcc`
### title : `Inefficient write of 32 bit value to 16 bit volatile on ARM`
### open_at : `2009-09-24T09:20:44Z`
### last_modified_date : `2022-09-27T23:38:24Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=41458
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.4.1`
### severity : `normal`
### contents :
GCC from at least 4.1.1, up to and including 4.4.1 generates two redundant bit shift operations when writing a 32 bit value to a 16 bit variable. Example:

  volatile unsigned short v1;
  void test1(unsigned x) { v1 = x; }

This code generates the following when compiled with "arm-elf-gcc -O2 -S -o- tmp.c":

	mov	r0, r0, asl #16
	ldr	r3, .L3
	mov	r0, r0, lsr #16
	strh	r0, [r3, #0]	@ movhi

If compiled with GCC 3.4.4, or if the volatile is removed, the expected code is generated:

	ldr	r3, .L7
	strh	r0, [r3, #0]	@ movhi

This also does not happen with GCC 4.4.1 for i586-redhat-linux.  It generates identical code whether the volatile is there or not.


---


### compiler : `gcc`
### title : `vector loads are unnecessarily split into high and low loads`
### open_at : `2009-09-24T23:14:26Z`
### last_modified_date : `2021-12-13T00:09:05Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=41464
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.4.1`
### severity : `normal`
### contents :
gcc (GCC) 4.4.1 20090725 (Red Hat 4.4.1-2)

The testcase (built with -Wall -O3):

#include <math.h>

void MulPi(float * __attribute__((aligned(16))) i, float * __attribute__((aligned(16))) f, int n)
{
        for (int j = 0; j < n; j++)
                f[j] = (float) M_PI * i[j];
}

produces the following for the vectorized version of the loop:

.L7:
	movaps	%xmm1, %xmm0		# zero XMM0
	incl	%ecx			
	movlps	(%rdi,%rax), %xmm0	# load the low half into XMM0
	movhps	8(%rdi,%rax), %xmm0	# load the high half into XMM0
	mulps	%xmm2, %xmm0		# multiply by pi
	movaps	%xmm0, (%rsi,%rax)	# store to memory
	addq	$16, %rax
	cmpl	%r8d, %ecx
	jb	.L7


---


### compiler : `gcc`
### title : `missed optimization in cse`
### open_at : `2009-09-27T09:13:06Z`
### last_modified_date : `2021-08-29T22:52:10Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=41481
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.5.0`
### severity : `enhancement`
### contents :
Compile following code with options -Os -march=armv5te -mthumb,

class A
{
 public:
  int ah;
  unsigned field : 2;
};

void foo(A* p)
{
  p->ah = 1;
  p->field = 1;
}

We can get:

        mov     r3, #1             // A
        str     r3, [r0]
        ldrb    r3, [r0, #4]
        mov     r2, #3
        bic     r3, r3, r2
        mov     r2, #1             // B
        orr     r3, r3, r2
        strb    r3, [r0, #4]
        @ sp needed for prologue
        bx      lr

Both instruction A and B load a constant 1 into register. We can load 1 into r1 in instruction A and use r1 when constant 1 is required. So instruction B can be removed.

cse pass doesn't find this opportunity is because it needs all expressions to be of the same mode. But in rtl level the first 1 is in mode SI and the second 1 is in mode QI. Arm doesn't has any physical register of QI mode, so all of them are put into 32 bit physical register and causes redundant load of constant 1.


---


### compiler : `gcc`
### title : `cselim is not dse aware`
### open_at : `2009-09-28T10:51:59Z`
### last_modified_date : `2022-01-05T10:17:07Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=41486
### status : `RESOLVED`
### tags : `missed-optimization, wrong-code`
### component : `tree-optimization`
### version : `4.5.0`
### severity : `normal`
### contents :
The cs elim pass introduces a conditional store, but does not remove the original one. If the former is not removed by DSE, this results in worse code.

original thread: http://gcc.gnu.org/ml/gcc-patches/2009-09/msg01955.html.

on machines with no predicated stores, disabling this optimization is generally a win, but only as a workaround.


---


### compiler : `gcc`
### title : `GCC choosing poor code sequence for certain stores (x86)`
### open_at : `2009-09-29T15:53:04Z`
### last_modified_date : `2021-07-26T18:57:33Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=41505
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `unknown`
### severity : `normal`
### contents :
Consider:

foo(int *x)
{
  *x = 0;
}

Compile with -Os -fomit-frame-pointer and you'll get something like this:

	movl	4(%esp), %eax
	movl	$0, (%eax)

It would be 2 bytes shorter to instead load the constant 0 via an xor instruction into a scratch register, then store the scratch register into the memory location.  Something like this:

	movl	4(%esp), %eax
	xor	%edx, %edx
	movl	%edx, (%eax)


ISTM this could easily be implemented with a peep2.

I'm not well versed enough in x86 instruction timings to know if the xor sequence is going to generally be faster.


---


### compiler : `gcc`
### title : `Unnecessary zero-extension at -O2 but not -O1`
### open_at : `2009-10-18T13:56:15Z`
### last_modified_date : `2023-04-11T17:07:07Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=41742
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.5.0`
### severity : `enhancement`
### contents :
Take the following example:

void *memset(void *b, int c, unsigned long len)
{
        unsigned long i;

        for (i = 0; i < len; i++)
                ((unsigned char *)b)[i] = c;

        return b;
}

-O2 generates:

memset:
        cmpwi 0,5,0
        beqlr 0
        mtctr 5
        rlwinm 4,4,0,0xff
        li 9,0
        .p2align 4,,15
.L3:
        stbx 4,3,9
        addi 9,9,1
        bdnz .L3
        blr

The zero-extension of GPR4 isn't needed, and in fact, -O1 doesn't
generate it:

memset:
        cmpwi 0,5,0
        beqlr 0
        li 9,0
        subf 5,9,5
        mtctr 5
.L3:
        stbx 4,3,9
        addi 9,9,1
        bdnz .L3
        blr

(the subf here is superfluous though).


---


### compiler : `gcc`
### title : `GCC ignores restrict on array`
### open_at : `2009-11-01T20:25:38Z`
### last_modified_date : `2021-03-25T13:48:09Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=41898
### status : `ASSIGNED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.5.0`
### severity : `normal`
### contents :
Adding a pointless array qualifier to the restrict-1.c test makes it not work with gcc -O2; we fail to optimize away the call to link_error.

int * __restrict__ a[1];
int * __restrict__ b[1];

extern void link_error (void);

int main()
{
  a[0][0] = 1;
  b[0][0] = 1;
  if (a[0][0] != 1)
    link_error ();
  return 0;
}


---


### compiler : `gcc`
### title : `[4.9 Regression] 50% performance regression`
### open_at : `2009-11-19T16:00:55Z`
### last_modified_date : `2022-02-02T00:23:15Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=42108
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.5.0`
### severity : `normal`
### contents :
With the attached sample code I get a substantial performance drop from 4.3.1 to either 4.4.1 or 4.5.0, same compiler option, same machine. To reproduce, feed a size to the program (in the case below, 40000) and time the executable. 

[sfilippo@donald fgp_fmm_20091112]$ gfortran -v  
Using built-in specs.
Target: x86_64-unknown-linux-gnu
Configured with: ../gcc-4.3.1/configure --prefix=/usr/local/gcc43 --with-mpfr=/u
sr/local/mpfr --with-gmp=/usr/local/gmp
Thread model: posix
gcc version 4.3.1 (GCC) 
[sfilippo@donald fgp_fmm_20091112]$ gfortran -O3 -o try_eval eval.f90
[sfilippo@donald fgp_fmm_20091112]$ time ./try_eval <<EOF
40000
EOF

real    0m10.871s
user    0m10.825s
sys     0m0.011s
[sfilippo@donald fgp_fmm_20091112]$ module unload gnu43
[sfilippo@donald fgp_fmm_20091112]$ module load gnu45 
        gnu45 - loads the GNU 4.5.0-pre compilers suite

        Version 1.0

[sfilippo@donald fgp_fmm_20091112]$ gfortran -v 
Using built-in specs.
COLLECT_GCC=gfortran
COLLECT_LTO_WRAPPER=/usr/local/gnu45/libexec/gcc/x86_64-unknown-linux-gnu/4.5.0/
lto-wrapper
Target: x86_64-unknown-linux-gnu
Configured with: ../gcc/configure --prefix=/usr/local/gnu45 --enable-languages=c
,c++,fortran : (reconfigured) ../gcc/configure --prefix=/usr/local/gnu45 --enabl
e-languages=c,c++,fortran : (reconfigured) ../gcc/configure --prefix=/usr/local/
gnu45 --enable-languages=c,c++,fortran,lto --no-create --no-recursion : (reconfi
gured) ../gcc/configure --prefix=/usr/local/gnu45 --enable-languages=c,c++,fortr
an,lto --no-create --no-recursion
Thread model: posix
gcc version 4.5.0 20091119 (experimental) (GCC) 
[sfilippo@donald fgp_fmm_20091112]$ gfortran -O3 -o try_eval eval.f90
[sfilippo@donald fgp_fmm_20091112]$ time ./try_eval <<EOF
40000
EOF

real    0m23.935s
user    0m23.862s
sys     0m0.011s
[sfilippo@donald fgp_fmm_20091112]$ cat /proc/cpuinfo
processor       : 0
vendor_id       : AuthenticAMD
cpu family      : 16
model           : 2
model name      : AMD Athlon(tm) 7750 Dual-Core Processor
stepping        : 3
cpu MHz         : 2700.000
cache size      : 512 KB
physical id     : 0
siblings        : 2
core id         : 0
cpu cores       : 2
apicid          : 0
initial apicid  : 0
fpu             : yes
fpu_exception   : yes
cpuid level     : 5
wp              : yes
flags           : fpu vme de pse tsc msr pae mce cx8 apic mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ht syscall nx mmxext fxsr_opt pdpe1gb rdtscp lm 3dnowext 3dnow constant_tsc rep_good nonstop_tsc extd_apicid pni monitor cx16 lahf_lm cmp_legacy svm extapic cr8_legacy abm sse4a misalignsse 3dnowprefetch osvw ibs
bogomips        : 5424.74
TLB size        : 1024 4K pages
clflush size    : 64
cache_alignment : 64
address sizes   : 48 bits physical, 48 bits virtual
power management: ts ttp tm stc 100mhzsteps hwpstate


---


### compiler : `gcc`
### title : `VRP should do if-conversion`
### open_at : `2009-11-20T12:49:19Z`
### last_modified_date : `2023-08-10T00:00:05Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=42117
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.5.0`
### severity : `enhancement`
### contents :
The vrp47 testcase currently fails on i386 and S/390.  The ssa code before vrp
looks different for both compared to x86_64 due to a different value
returned by BRANCH_COST. (Branches on S/390 are relatively cheap due
to a sophisticated branch prediction unit.)  Therefore during
gimplification fold_truthop (line 5866) uses more branches for
function h in vrp47.c than the x86_64 variant.
The problem can also be reproduced on x86 when compiling for a cpu with low branch costs defined in i386.c as e.g. -march=i386.

int h(int x, int y)
{
  if ((x >= 0 && x <= 1) && (y >= 0 && y <= 1))
    return x && y;
  else
    return -1;
}

Compile the testcase above with:
cc1 -m32 -O2 vrp47.c -fdump-tree-vrp -march=i386

The vrp pass is not able to get rid of the comparisons in this case
(069t.vrp1 from i386):

h (int x, int y)
{
  int D.2021;
  unsigned int y.1;
  unsigned int x.0;

<bb 2>:
  x.0_4 = (unsigned int) x_3(D);
  if (x.0_4 <= 1)
    goto <bb 3>;
  else
    goto <bb 7>;

<bb 3>:
  y.1_6 = (unsigned int) y_5(D);
  if (y.1_6 <= 1)
    goto <bb 4>;
  else
    goto <bb 7>;

<bb 4>:
  if (x_3(D) != 0)
    goto <bb 5>;
  else
    goto <bb 6>;

<bb 5>:
  if (y_5(D) != 0)
    goto <bb 7>;
  else
    goto <bb 6>;

<bb 6>:

<bb 7>:
  # D.2021_1 = PHI <0(6), -1(3), -1(2), 1(5)>
  return D.2021_1;

}


---


### compiler : `gcc`
### title : `use __cxa_vec_dtor instead of loop to reduce code size`
### open_at : `2009-11-24T08:51:33Z`
### last_modified_date : `2023-03-21T09:56:41Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=42161
### status : `NEW`
### tags : `missed-optimization`
### component : `c++`
### version : `4.5.0`
### severity : `enhancement`
### contents :
Compile the attached test case with options -Os -mthumb, gcc generates following code to destruct the array of objects:

__tcf_0:
        .fnstart
.LFB1:
        .save   {r3, r4, r5, lr}
        push    {r3, r4, r5, lr}
.LCFI0:
        ldr     r5, .L5
        mov     r4, r5
        add     r4, r4, #36
        sub     r5, r5, #12
.L2:
        mov     r0, r4
        sub     r4, r4, #12
        bl      _ZN1AD1Ev
        cmp     r4, r5
        bne     .L2
        @ sp needed for prologue
        pop     {r3, r4, r5, pc}
.L6:
        .align  2
.L5:
        .word   .LANCHOR0
 
It uses a loop to call the destructor of each element of the array. Actually we can call function __cxa_vec_dtor to destruct the array of objects. So we can reduce several instructions and the result will be:

        push    {r3, r4, r5, lr}
        ldr     r0, .L5
        mov     r1, 4
        mov     r2, #12
        ldr     r3, .L5+4
        bl      __cxa_vec_dtor
        @ sp needed for prologue
        pop     {r3, r4, r5, pc}
.L6:
        .align  2
.L5:
        .word   .LANCHOR0
        .word   ZN1AD1Ev


---


### compiler : `gcc`
### title : `inefficient bit fields assignments`
### open_at : `2009-11-25T09:15:55Z`
### last_modified_date : `2021-07-21T03:18:16Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=42172
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.5.0`
### severity : `enhancement`
### contents :
The attached test case contains several continuous bit fields assignment, compile it with options -mthumb -Os, gcc generates

        .fnstart
.LFB1:
        ldrb    r3, [r0]
        mov     r2, #7
        bic     r3, r3, r2
        strb    r3, [r0]
        ldrb    r3, [r0]
        mov     r2, #56
        bic     r3, r3, r2
        mov     r2, #8
        orr     r3, r3, r2
        strb    r3, [r0]
        ldrb    r3, [r0]
        mov     r2, #64
        bic     r3, r3, r2
        strb    r3, [r0]
        ldrb    r2, [r0]
        mov     r3, #127
        and     r3, r3, r2
        strb    r3, [r0]
        @ sp needed for prologue
        bx      lr

The 4 fields are contained in one word, for each field assignment the code loads the word, changes the field, then write the word back. A better code sequence should load the word once, change all 4 fields, then write back the changed word.

        ldrb    r3, [r0]
        mov     r2, #255             // bit mask
        bic     r3, r3, r2
        mov     r2, #8               // the new value of all 4 fields
        orr     r3, r3, r2
        strb    r3, [r0]
        @ sp needed for prologue
        bx      lr

or more aggressively if the word contains only these four fields

        mov     r3, #8
        strb    r3, [r0]
        @ sp needed for prologue
        bx      lr


---


### compiler : `gcc`
### title : `missed xnor optimization.`
### open_at : `2009-11-27T13:25:08Z`
### last_modified_date : `2023-10-25T22:43:04Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=42195
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.4.3`
### severity : `enhancement`
### contents :
bool xnor_1( bool x, bool y ) { return !( x ^ y ); }
bool xnor_2( bool x, bool y ) { return ( x && y ) || ( !x && !y ); }

both functions should emit (x==y) code, but _2 isn't optimized.

bool xnor_1(bool, bool) (x, y)
{
  int D.2085;
<bb 0>:
  return x == y;
}

bool xnor_2(bool, bool) (x, y)
{
  bool D.2181;
  int prephitmp.51;
  bool D.2098;
  bool D.2097;
  bool D.2096;
  bool iftmp.0;
  int D.2090;
<bb 0>:
  if (x == 0) goto <L2>; else goto <L0>;
<L0>:;
  (void) 0;
  prephitmp.51 = (int) y;
  goto <bb 3> (<L5>);
<L2>:;
  (void) 0;
  prephitmp.51 = (int) (y == 0);
<L5>:;
  return prephitmp.51;
}


---


### compiler : `gcc`
### title : `Suboptimal optimization: after x / 2 carry flag == x & 1`
### open_at : `2009-11-27T21:18:36Z`
### last_modified_date : `2021-09-13T00:25:58Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=42200
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.4.1`
### severity : `enhancement`
### contents :
In the example below f1 and f2 are equivalent functions differing only by the order of conditions in if(): y && !(x & 1) versus !(x & 1) && y.
There are two lost optimization opportunities here: gcc does not try to pick an order of conditions which is better, and in both cases it does not use the fact that (x & 1) at this point is available as a carry bit.

void a(unsigned);

void f1(unsigned x)
{
        unsigned y = x / 2;
        if (y && !(x & 1))
                a(y);
}
/* compiled with -Os -fomit-frame-pointer on x86_64: 20 bytes
f1:     movl    %edi, %eax
        shrl    %eax
        je      .L7
        andb    $1, %dil
        jne     .L7
        movl    %eax, %edi
        jmp     a
.L7:    ret
*/

void f2(unsigned x)
{
        unsigned y = x / 2;
        if (!(x & 1) && y)
                a(y);
}
/* 18 bytes
f2:     movl    %edi, %eax
        shrl    %edi
        testb   $1, %al
        jne     .L3
        testl   %edi, %edi
        je      .L3
        jmp     a
.L3:    ret
*/

/* Handwritten assembly: 12 bytes
f3:     shrl    %edi
        jc      .L77
        jz      .L77
        jmp     a
.L77:   ret
*/


---


### compiler : `gcc`
### title : `[missed optimization]  inefficient byte access when -Os is specified`
### open_at : `2009-11-30T08:55:52Z`
### last_modified_date : `2021-07-26T08:09:34Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=42226
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.5.0`
### severity : `enhancement`
### contents :
Compile the attached test case with options -Os -mthumb, gcc generates:

        add     r1, r1, #40
        mov     r3, r0
        ldrb    r2, [r1]
        add     r3, r3, #40
        strb    r2, [r3]
        @ sp needed for prologue
        bx      lr

When change the options to -O2 -mthumb, gcc generates:

        mov     r3, #40
        ldrb    r2, [r1, r3]
        strb    r2, [r0, r3]
        @ sp needed for prologue
        bx      lr

It is both smaller and faster.

Compare the dumped IL with different options, all TREE expressions are identical. The first difference occurs after rtl expanding.


---


### compiler : `gcc`
### title : `[4.4/4.5 Regression] Extra sign extension instructions generated`
### open_at : `2009-12-04T00:49:25Z`
### last_modified_date : `2019-06-14T19:28:03Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=42269
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.5.0`
### severity : `normal`
### contents :
In reference to http://gcc.gnu.org/bugzilla/show_bug.cgi?id=27469#c3

This bug to track the regression since 4.2,
not the enhancement in the original PR.


---


### compiler : `gcc`
### title : `long vector operation causes gcc to copy arguments`
### open_at : `2009-12-14T13:32:17Z`
### last_modified_date : `2021-05-31T01:20:48Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=42367
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.1.2`
### severity : `enhancement`
### contents :
Why GCC copies vectorized buffers to and from stack ?
Am I doing something wrong ?

===
Compiler:
===
gcc -v
Using built-in specs.
Target: x86_64-redhat-linux
Configured with: ../configure --prefix=/usr --mandir=/usr/share/man --infodir=/usr/share/info --enable-shared --enable-threads=posix --enable-checking=release --with-system-zlib --enable-__cxa_atexit --disable-libunwind-exceptions --enable-libgcj-multifile --enable-languages=c,c++,objc,obj-c++,java,fortran,ada --enable-java-awt=gtk --disable-dssi --enable-plugin --with-java-home=/usr/lib/jvm/java-1.4.2-gcj-1.4.2.0/jre --with-cpu=generic --host=x86_64-redhat-linux
Thread model: posix
gcc version 4.1.2 20080704 (Red Hat 4.1.2-46)



===
Source a.c:
===
typedef int BLOCK512 __attribute__((__vector_size__(512)));

void f (BLOCK512 *d, const BLOCK512 *s0, const BLOCK512 *s1) {
    *d = *s0 ^ *s1;
}



===
Command:
===
gcc -O3 a.c -c -o a.o


===
Result (note 3 calls to memcpy):
===
Disassembly of section .text:

0000000000000000 <f>:
   0:   41 54                   push   %r12
   2:   49 89 fc                mov    %rdi,%r12
   5:   53                      push   %rbx
   6:   48 89 d3                mov    %rdx,%rbx
   9:   ba 00 02 00 00          mov    $0x200,%edx
   e:   48 81 ec 08 06 00 00    sub    $0x608,%rsp
  15:   48 8d bc 24 00 02 00    lea    0x200(%rsp),%rdi
  1c:   00 
  1d:   e8 00 00 00 00          callq  22 <f+0x22>
                        1e: R_X86_64_PC32       memcpy+0xfffffffffffffffc
  22:   48 8d bc 24 00 04 00    lea    0x400(%rsp),%rdi
  29:   00 
  2a:   48 89 de                mov    %rbx,%rsi
  2d:   ba 00 02 00 00          mov    $0x200,%edx
  32:   e8 00 00 00 00          callq  37 <f+0x37>
                        33: R_X86_64_PC32       memcpy+0xfffffffffffffffc
  37:   66 0f 6f 84 24 00 04    movdqa 0x400(%rsp),%xmm0
  3e:   00 00 
  40:   48 89 e6                mov    %rsp,%rsi
  43:   4c 89 e7                mov    %r12,%rdi
  46:   ba 00 02 00 00          mov    $0x200,%edx
  4b:   66 0f ef 84 24 00 02    pxor   0x200(%rsp),%xmm0
  52:   00 00 
  54:   66 0f 7f 04 24          movdqa %xmm0,(%rsp)
  59:   66 0f 6f 84 24 10 04    movdqa 0x410(%rsp),%xmm0
  60:   00 00 
  62:   66 0f ef 84 24 10 02    pxor   0x210(%rsp),%xmm0
  69:   00 00 
  6b:   66 0f 7f 44 24 10       movdqa %xmm0,0x10(%rsp)
  71:   66 0f 6f 84 24 20 04    movdqa 0x420(%rsp),%xmm0
  78:   00 00 
  7a:   66 0f ef 84 24 20 02    pxor   0x220(%rsp),%xmm0
  81:   00 00 
  83:   66 0f 7f 44 24 20       movdqa %xmm0,0x20(%rsp)
  89:   66 0f 6f 84 24 30 04    movdqa 0x430(%rsp),%xmm0
  90:   00 00 
  92:   66 0f ef 84 24 30 02    pxor   0x230(%rsp),%xmm0
  99:   00 00 
  9b:   66 0f 7f 44 24 30       movdqa %xmm0,0x30(%rsp)
  a1:   66 0f 6f 84 24 40 04    movdqa 0x440(%rsp),%xmm0
  a8:   00 00 
  aa:   66 0f ef 84 24 40 02    pxor   0x240(%rsp),%xmm0
  b1:   00 00 
  b3:   66 0f 7f 44 24 40       movdqa %xmm0,0x40(%rsp)
  b9:   66 0f 6f 84 24 50 04    movdqa 0x450(%rsp),%xmm0
  c0:   00 00 
  c2:   66 0f ef 84 24 50 02    pxor   0x250(%rsp),%xmm0
  c9:   00 00 
  cb:   66 0f 7f 44 24 50       movdqa %xmm0,0x50(%rsp)
  d1:   66 0f 6f 84 24 60 04    movdqa 0x460(%rsp),%xmm0
  d8:   00 00 
  da:   66 0f ef 84 24 60 02    pxor   0x260(%rsp),%xmm0
  e1:   00 00 
  e3:   66 0f 7f 44 24 60       movdqa %xmm0,0x60(%rsp)
  e9:   66 0f 6f 84 24 70 04    movdqa 0x470(%rsp),%xmm0
  f0:   00 00 
  f2:   66 0f ef 84 24 70 02    pxor   0x270(%rsp),%xmm0
  f9:   00 00 
  fb:   66 0f 7f 44 24 70       movdqa %xmm0,0x70(%rsp)
 101:   66 0f 6f 84 24 80 04    movdqa 0x480(%rsp),%xmm0
 108:   00 00 
 10a:   66 0f ef 84 24 80 02    pxor   0x280(%rsp),%xmm0
 111:   00 00 
 113:   66 0f 7f 84 24 80 00    movdqa %xmm0,0x80(%rsp)
 11a:   00 00 
 11c:   66 0f 6f 84 24 90 04    movdqa 0x490(%rsp),%xmm0
 123:   00 00 
 125:   66 0f ef 84 24 90 02    pxor   0x290(%rsp),%xmm0
 12c:   00 00 
 12e:   66 0f 7f 84 24 90 00    movdqa %xmm0,0x90(%rsp)
 135:   00 00 
 137:   66 0f 6f 84 24 a0 04    movdqa 0x4a0(%rsp),%xmm0
 13e:   00 00 
 140:   66 0f ef 84 24 a0 02    pxor   0x2a0(%rsp),%xmm0
 147:   00 00 
 149:   66 0f 7f 84 24 a0 00    movdqa %xmm0,0xa0(%rsp)
 150:   00 00 
 152:   66 0f 6f 84 24 b0 04    movdqa 0x4b0(%rsp),%xmm0
 159:   00 00 
 15b:   66 0f ef 84 24 b0 02    pxor   0x2b0(%rsp),%xmm0
 162:   00 00 
 164:   66 0f 7f 84 24 b0 00    movdqa %xmm0,0xb0(%rsp)
 16b:   00 00 
 16d:   66 0f 6f 84 24 c0 04    movdqa 0x4c0(%rsp),%xmm0
 174:   00 00 
 176:   66 0f ef 84 24 c0 02    pxor   0x2c0(%rsp),%xmm0
 17d:   00 00 
 17f:   66 0f 7f 84 24 c0 00    movdqa %xmm0,0xc0(%rsp)
 186:   00 00 
 188:   66 0f 6f 84 24 d0 04    movdqa 0x4d0(%rsp),%xmm0
 18f:   00 00 
 191:   66 0f ef 84 24 d0 02    pxor   0x2d0(%rsp),%xmm0
 198:   00 00 
 19a:   66 0f 7f 84 24 d0 00    movdqa %xmm0,0xd0(%rsp)
 1a1:   00 00 
 1a3:   66 0f 6f 84 24 e0 04    movdqa 0x4e0(%rsp),%xmm0
 1aa:   00 00 
 1ac:   66 0f ef 84 24 e0 02    pxor   0x2e0(%rsp),%xmm0
 1b3:   00 00 
 1b5:   66 0f 7f 84 24 e0 00    movdqa %xmm0,0xe0(%rsp)
 1bc:   00 00 
 1be:   66 0f 6f 84 24 f0 04    movdqa 0x4f0(%rsp),%xmm0
 1c5:   00 00 
 1c7:   66 0f ef 84 24 f0 02    pxor   0x2f0(%rsp),%xmm0
 1ce:   00 00 
 1d0:   66 0f 7f 84 24 f0 00    movdqa %xmm0,0xf0(%rsp)
 1d7:   00 00 
 1d9:   66 0f 6f 84 24 00 05    movdqa 0x500(%rsp),%xmm0
 1e0:   00 00 
 1e2:   66 0f ef 84 24 00 03    pxor   0x300(%rsp),%xmm0
 1e9:   00 00 
 1eb:   66 0f 7f 84 24 00 01    movdqa %xmm0,0x100(%rsp)
 1f2:   00 00 
 1f4:   66 0f 6f 84 24 10 05    movdqa 0x510(%rsp),%xmm0
 1fb:   00 00 
 1fd:   66 0f ef 84 24 10 03    pxor   0x310(%rsp),%xmm0
 204:   00 00 
 206:   66 0f 7f 84 24 10 01    movdqa %xmm0,0x110(%rsp)
 20d:   00 00 
 20f:   66 0f 6f 84 24 20 05    movdqa 0x520(%rsp),%xmm0
 216:   00 00 
 218:   66 0f ef 84 24 20 03    pxor   0x320(%rsp),%xmm0
 21f:   00 00 
 221:   66 0f 7f 84 24 20 01    movdqa %xmm0,0x120(%rsp)
 228:   00 00 
 22a:   66 0f 6f 84 24 30 05    movdqa 0x530(%rsp),%xmm0
 231:   00 00 
 233:   66 0f ef 84 24 30 03    pxor   0x330(%rsp),%xmm0
 23a:   00 00 
 23c:   66 0f 7f 84 24 30 01    movdqa %xmm0,0x130(%rsp)
 243:   00 00 
 245:   66 0f 6f 84 24 40 05    movdqa 0x540(%rsp),%xmm0
 24c:   00 00 
 24e:   66 0f ef 84 24 40 03    pxor   0x340(%rsp),%xmm0
 255:   00 00 
 257:   66 0f 7f 84 24 40 01    movdqa %xmm0,0x140(%rsp)
 25e:   00 00 
 260:   66 0f 6f 84 24 50 05    movdqa 0x550(%rsp),%xmm0
 267:   00 00 
 269:   66 0f ef 84 24 50 03    pxor   0x350(%rsp),%xmm0
 270:   00 00 
 272:   66 0f 7f 84 24 50 01    movdqa %xmm0,0x150(%rsp)
 279:   00 00 
 27b:   66 0f 6f 84 24 60 05    movdqa 0x560(%rsp),%xmm0
 282:   00 00 
 284:   66 0f ef 84 24 60 03    pxor   0x360(%rsp),%xmm0
 28b:   00 00 
 28d:   66 0f 7f 84 24 60 01    movdqa %xmm0,0x160(%rsp)
 294:   00 00 
 296:   66 0f 6f 84 24 70 05    movdqa 0x570(%rsp),%xmm0
 29d:   00 00 
 29f:   66 0f ef 84 24 70 03    pxor   0x370(%rsp),%xmm0
 2a6:   00 00 
 2a8:   66 0f 7f 84 24 70 01    movdqa %xmm0,0x170(%rsp)
 2af:   00 00 
 2b1:   66 0f 6f 84 24 80 05    movdqa 0x580(%rsp),%xmm0
 2b8:   00 00 
 2ba:   66 0f ef 84 24 80 03    pxor   0x380(%rsp),%xmm0
 2c1:   00 00 
 2c3:   66 0f 7f 84 24 80 01    movdqa %xmm0,0x180(%rsp)
 2ca:   00 00 
 2cc:   66 0f 6f 84 24 90 05    movdqa 0x590(%rsp),%xmm0
 2d3:   00 00 
 2d5:   66 0f ef 84 24 90 03    pxor   0x390(%rsp),%xmm0
 2dc:   00 00 
 2de:   66 0f 7f 84 24 90 01    movdqa %xmm0,0x190(%rsp)
 2e5:   00 00 
 2e7:   66 0f 6f 84 24 a0 05    movdqa 0x5a0(%rsp),%xmm0
 2ee:   00 00 
 2f0:   66 0f ef 84 24 a0 03    pxor   0x3a0(%rsp),%xmm0
 2f7:   00 00 
 2f9:   66 0f 7f 84 24 a0 01    movdqa %xmm0,0x1a0(%rsp)
 300:   00 00 
 302:   66 0f 6f 84 24 b0 05    movdqa 0x5b0(%rsp),%xmm0
 309:   00 00 
 30b:   66 0f ef 84 24 b0 03    pxor   0x3b0(%rsp),%xmm0
 312:   00 00 
 314:   66 0f 7f 84 24 b0 01    movdqa %xmm0,0x1b0(%rsp)
 31b:   00 00 
 31d:   66 0f 6f 84 24 c0 05    movdqa 0x5c0(%rsp),%xmm0
 324:   00 00 
 326:   66 0f ef 84 24 c0 03    pxor   0x3c0(%rsp),%xmm0
 32d:   00 00 
 32f:   66 0f 7f 84 24 c0 01    movdqa %xmm0,0x1c0(%rsp)
 336:   00 00 
 338:   66 0f 6f 84 24 d0 05    movdqa 0x5d0(%rsp),%xmm0
 33f:   00 00 
 341:   66 0f ef 84 24 d0 03    pxor   0x3d0(%rsp),%xmm0
 348:   00 00 
 34a:   66 0f 7f 84 24 d0 01    movdqa %xmm0,0x1d0(%rsp)
 351:   00 00 
 353:   66 0f 6f 84 24 e0 05    movdqa 0x5e0(%rsp),%xmm0
 35a:   00 00 
 35c:   66 0f ef 84 24 e0 03    pxor   0x3e0(%rsp),%xmm0
 363:   00 00 
 365:   66 0f 7f 84 24 e0 01    movdqa %xmm0,0x1e0(%rsp)
 36c:   00 00 
 36e:   66 0f 6f 84 24 f0 05    movdqa 0x5f0(%rsp),%xmm0
 375:   00 00 
 377:   66 0f ef 84 24 f0 03    pxor   0x3f0(%rsp),%xmm0
 37e:   00 00 
 380:   66 0f 7f 84 24 f0 01    movdqa %xmm0,0x1f0(%rsp)
 387:   00 00 
 389:   e8 00 00 00 00          callq  38e <f+0x38e>
                        38a: R_X86_64_PC32      memcpy+0xfffffffffffffffc
 38e:   48 81 c4 08 06 00 00    add    $0x608,%rsp
 395:   5b                      pop    %rbx
 396:   41 5c                   pop    %r12
 398:   c3


---


### compiler : `gcc`
### title : `VRP should mark non-trapping integer divisions`
### open_at : `2009-12-19T19:40:43Z`
### last_modified_date : `2022-01-13T07:13:02Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=42436
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.5.0`
### severity : `enhancement`
### contents :
In PR42108 a division is found to be non-trapping by VRP but neither PRE nor
LIM can make use of that information (well, because VRP doesn't mark the
divisions in any meaningful way).


---


### compiler : `gcc`
### title : `arm-eabi-gcc 64-bit multiply weirdness`
### open_at : `2010-01-01T17:33:01Z`
### last_modified_date : `2019-10-11T14:49:30Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=42575
### status : `RESOLVED`
### tags : `missed-optimization, ra`
### component : `rtl-optimization`
### version : `5.0`
### severity : `normal`
### contents :
Given the following complete source file:

long long longfunc(long long x, long long y)
{
      return x * y;
}

Compile with ARM EABI gcc 4.2.1:
% arm-eabi-gcc -c -O2 -save-temps mul64.c


This yields mul64.i:

# 1 "mul64.c"
# 1 "<built-in>"
# 1 "<command-line>"
# 1 "mul64.c"
long long longfunc(long long x, long long y)
{
      return x * y;
}

And mul64.s:

       .file   "mul64.c"
       .text
       .align  2
       .global longfunc
       .type   longfunc, %function
longfunc:
       @ args = 0, pretend = 0, frame = 0
       @ frame_needed = 0, uses_anonymous_args = 0
       stmfd   sp!, {r4, r5, lr}
       mul     lr, r2, r1
       mov     r4, r0
       mov     r5, r1
       umull   r0, r1, r2, r4
       mla     ip, r4, r3, lr
       add     r1, ip, r1
       ldmfd   sp!, {r4, r5, pc}
       .size   longfunc, .-longfunc
       .ident  "GCC: (GNU) 4.2.1"

Note the use of register r5.  It's saved, restored, and used to hold a copy of r1, but it's never used in the computation.


---


### compiler : `gcc`
### title : `load-modify-store on x86 should be a single instruction`
### open_at : `2010-01-03T06:04:25Z`
### last_modified_date : `2023-09-21T14:02:25Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=42586
### status : `NEW`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.5.0`
### severity : `enhancement`
### contents :
Continuation from 42585

From one of the examples of http://embed.cs.utah.edu/embarrassing/dec_09/harvest/gcc-head_llvm-gcc-head/

struct _fat_ptr
{
  unsigned char *curr;
  unsigned char *base;
  unsigned char *last_plus_one;
};
int Cyc_string_ungetc (int ignore, struct _fat_ptr *sptr);
int
Cyc_string_ungetc (int ignore, struct _fat_ptr *sptr)
{
  struct _fat_ptr *_T0;
  struct _fat_ptr *_T1;
  struct _fat_ptr _T2;
  int _T3;
  struct _fat_ptr _ans;
  int _change;

  {
    _T0 = sptr;
    _T1 = sptr;
    _T2 = *sptr;
    _T3 = -1;
    _ans = _T2;
    _change = -1;
    _ans.curr += 4294967295U;
    *sptr = _ans;
    return (0);
  }
}

when compiled with -O2 -m32 on 4.5.0 20091219 generates

Cyc_string_ungetc:
        subl    $32, %esp
        movl    40(%esp), %eax
        movl    (%eax), %edx
        subl    $1, %edx
        movl    %edx, (%eax)
        xorl    %eax, %eax
        addl    $32, %esp
        ret

Apart from the useless stack frame manipulation it should use

       subl $1,(%eax) 

not load-modify-store as recommended in the Intel/AMD optimization
manuals for any modern CPU.

I experimented with different -mtune=s
(thinking it was maybe optimizing for Pentium5 where this made sense), but that didn't help (apart from turning the subl into a decl). The code snippet
above is for -mtune=generic -m32


---


### compiler : `gcc`
### title : `bswap not recognized for memory`
### open_at : `2010-01-03T06:15:03Z`
### last_modified_date : `2021-05-10T12:22:33Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=42587
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `unknown`
### severity : `enhancement`
### contents :
From http://embed.cs.utah.edu/embarrassing/dec_09/harvest/gcc-head_llvm-gcc-head/

typedef unsigned char u8;
typedef unsigned int u32;
#pragma pack(1)
#pragma pack()
#pragma pack(1)
#pragma pack()
#pragma pack(1)
#pragma pack()
#pragma pack(4)
#pragma pack()
union __anonunion_out_195
{
  u32 value;
  u8 bytes[4];
};
union __anonunion_in_196
{
  u32 value;
  u8 bytes[4];
};
extern void acpi_ut_track_stack_ptr (void);
u32 acpi_ut_dword_byte_swap (u32 value);
u32
acpi_ut_dword_byte_swap (u32 value)
{
  union __anonunion_out_195 out;
  union __anonunion_in_196 in;

  {
    acpi_ut_track_stack_ptr ();
    in.value = value;
    out.bytes[0] = in.bytes[3];
    out.bytes[1] = in.bytes[2];
    out.bytes[2] = in.bytes[1];
    out.bytes[3] = in.bytes[0];
    return (out.value);
  }
}

/* Checksum = 1251E213 */


does not turn into bswap, while llvm does that.

There's bswap detection code in tree-ssa-math-ops.c, but it doesn't
seem to work for this union pattern. Perhaps it should?


---


### compiler : `gcc`
### title : `unnecessary move through x87 stack/local frame for union`
### open_at : `2010-01-03T06:22:52Z`
### last_modified_date : `2021-07-26T07:03:40Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=42588
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `unknown`
### severity : `enhancement`
### contents :
from http://embed.cs.utah.edu/embarrassing/dec_09/harvest/gcc-head_llvm-gcc-head/

union __anonunion___u_19
{
  double __d;
  int __i[2];
};
extern __attribute__ ((__nothrow__))
     int __signbit (double __x) __attribute__ ((__const__));
     extern __attribute__ ((__nothrow__))
     int __signbit (double __x) __attribute__ ((__const__));
     extern int __signbit (double __x)
{
  union __anonunion___u_19 __u;

  {
    __u.__d = __x;
    return (__u.__i[1] < 0);
  }
}

/* Checksum = AEFB9790 */

generates with -O2 -m32 -fomit-frame-pointer

 subl    $12, %esp
        fldl    16(%esp)
        fstpl   (%esp)
        movl    4(%esp), %eax
        addl    $12, %esp
        shrl    $31, %eax
        ret

the move through the x87 stack and the local frame is totally unnecessary;
the shr could be just done on the input stack value

in comparison llvm generates the much neater:

   0:	0f b7 44 24 0c       	movzwl 0xc(%esp),%eax
   5:	c1 e8 0f             	shr    $0xf,%eax
   8:	c3                   	ret


---


### compiler : `gcc`
### title : `post-increment addressing not used`
### open_at : `2010-01-04T16:02:10Z`
### last_modified_date : `2022-07-12T05:39:59Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=42612
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `7.1.0`
### severity : `enhancement`
### contents :
It seems post-increment addressing is not used as often as it could be, resulting in sub-optimal code. Take this trivial test case:

char * func(char *p)
{
  *p++=0;
  *p++=0;
  *p++=0;
  return p;
}

On ARM, we end up with:

        mov     r2, #0  @ 6
        mov     r3, r0  @ 28
        strb    r2, [r3], #1
        strb    r2, [r0, #1]
        add     r0, r3, #2         
        strb    r2, [r3, #1]
        bx      lr      

The add instruction could be removed if all of the strb instructions used post-increment addressing.

Problem seems to occur in both 4.4.0 and 4.5.0 latest svn. Also seems to effect other targets that have post-increment addressing, not just ARM.


---


### compiler : `gcc`
### title : `Jump threading breaks canonical loop forms`
### open_at : `2010-01-07T14:26:55Z`
### last_modified_date : `2021-12-13T13:57:14Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=42646
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.5.0`
### severity : `normal`
### contents :
pass_dominator tries to thread jumps.But sometimes this will cause that the loop's exit bb does not dominator its latch bb again. 

-------------------------------------
void
foo (int x)
{
 int i;

 for (i=0; i < 10 ; i++)
   if (x)
     {
       if (i == 0)
         fun_1 ();
       else
         fun_2 ();
     }
}
---------------------------------------
$ gcc -O3 -S foo.c
$ cat foo.s

       .file   "foo.c"
       .text
       .p2align 4,,15
.globl foo
       .type   foo, @function
foo:
       pushl   %ebp
       movl    %esp, %ebp
       pushl   %ebx
       movl    $1, %ebx
       subl    $4, %esp
       movl    8(%ebp), %eax
       testl   %eax, %eax
       jne     .L3
       addl    $4, %esp
       popl    %ebx
       popl    %ebp
       ret
       .p2align 4,,7
       .p2align 3
.L7:
       call    fun_1
.L5:
       addl    $1, %ebx
.L3:
       cmpl    $1, %ebx
       je      .L7
       call    fun_2
       cmpl    $9, %ebx
       jle     .L5
       addl    $4, %esp
       popl    %ebx
       popl    %ebp
       ret
       .size   foo, .-foo
       .ident  "GCC: (GNU) 4.5.0 20100107 (experimental)"
       .section        .note.GNU-stack,"",@progbits
-------------------------------------------
$ gcc -O3 -fno-tree-dominator-opts -S foo.c
$ cat foo.s

       .file   "foo.c"
       .text
       .p2align 4,,15
.globl foo
       .type   foo, @function
foo:
       pushl   %ebp
       movl    %esp, %ebp
       subl    $8, %esp
       movl    8(%ebp), %eax
       testl   %eax, %eax
       je      .L1
       call    fun_1
       call    fun_2
       .p2align 4,,5
       call    fun_2
       .p2align 4,,5
       call    fun_2
       .p2align 4,,5
       call    fun_2
       .p2align 4,,5
       call    fun_2
       .p2align 4,,5
       call    fun_2
       .p2align 4,,5
       call    fun_2
       .p2align 4,,5
       call    fun_2
       leave
       jmp     fun_2
       .p2align 4,,7
       .p2align 3
.L1:
       leave
       ret
       .size   foo, .-foo
       .ident  "GCC: (GNU) 4.5.0 20100107 (experimental)"
       .section        .note.GNU-stack,"",@progbits
-------------------------------------------
$ gcc -v
Using built-in specs.
COLLECT_GCC=gcc
COLLECT_LTO_WRAPPER=/home/eric/install/trunk/libexec/gcc/i686-pc-linux-gnu/4.5.0/lto-wrapper
Target: i686-pc-linux-gnu
Configured with: ../trunk/configure --prefix=/home/eric/install/trunk
--with-gmp=/home/eric/install/generic
--with-mpfr=/home/eric/install/generic
--with-mpc=/home/eric/install/generic/ --enable-languages=c
Thread model: posix
gcc version 4.5.0 20100107 (experimental) (GCC)


---


### compiler : `gcc`
### title : `move_by_pieces() incorrectly pushes structures to stack`
### open_at : `2010-01-13T09:43:47Z`
### last_modified_date : `2021-08-16T22:29:49Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=42722
### status : `UNCONFIRMED`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.4.2`
### severity : `enhancement`
### contents :
The move_by_pieces() function incorrectly works on targets with enabled PUSH_ARGS that support post-increment loads. To reproduce the bug, the following code should be compiled:

struct test { int a, b, c, d, e, f; } //Enough fields to pass structure in stack
void func2(test copy);
void func1(test copy) {func2(copy);}

Every time a copy of our big structure is pushed to stack, its fields will go in reverse order. This happens due to a bug in move_by_pieces() function from expr.c that generates code for pushing a memory block in stack. 
This happens because if the target supports post-increment addressing, the USE_LOAD_POST_INCREMENT() condition is met and the memory block to be pushed is parsed from start to end using autoincrement addressing. The "reverse" flag specifying that the push statements should traverse the block from end to start is then ignored.
The proposed fix explicitly disables using post-increment mode if the "reverse" flag is set.

The following patch fixes the problem:
---------------------------------------------
--- expr.old	Thu Aug 20 00:52:11 2009
+++ expr.new	Tue Jan 12 23:32:05 2010
@@ -952,13 +952,13 @@
       if (USE_LOAD_PRE_DECREMENT (mode) && data.reverse && ! data.autinc_from)
 	{
 	  data.from_addr = copy_addr_to_reg (plus_constant (from_addr, len));
 	  data.autinc_from = 1;
 	  data.explicit_inc_from = -1;
 	}
-      if (USE_LOAD_POST_INCREMENT (mode) && ! data.autinc_from)
+      if (USE_LOAD_POST_INCREMENT (mode) && !data.reverse && ! data.autinc_from)
 	{
 	  data.from_addr = copy_addr_to_reg (from_addr);
 	  data.autinc_from = 1;
 	  data.explicit_inc_from = 1;
 	}
       if (!data.autinc_from && CONSTANT_P (from_addr))


---


### compiler : `gcc`
### title : `Superfluous stack management code is generated`
### open_at : `2010-01-17T20:05:54Z`
### last_modified_date : `2018-12-13T17:57:46Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=42778
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.5.0`
### severity : `normal`
### contents :
#include <x86intrin.h>

int test1(__m128i v) {

   return _mm_cvtsi128_si32(v);
}

compiled with

g++ -std=gnu++0x -O2 -m32 -march=native -msse -msse2 -msse3 -Wall
-Werror -Wno-unused -Wno-strict-aliasing -march=native
-fomit-frame-pointer -Wno-pmf-conversions -g main.cpp

emits:

004012e0 <__Z5test1U8__vectorx>:
 4012e0:       83 ec 0c                sub    $0xc,%esp
 4012e3:       66 0f 7e c0             movd   %xmm0,%eax
 4012e7:       83 c4 0c                add    $0xc,%esp
 4012ea:       c3                      ret

which shows that the stack pointer is being updated
without any purpose.


---


### compiler : `gcc`
### title : `inefficient code for trivial tail-call with large struct parameter`
### open_at : `2010-01-30T22:48:31Z`
### last_modified_date : `2021-09-23T01:21:19Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=42909
### status : `NEW`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `4.5.0`
### severity : `normal`
### contents :
While looking at PR42722 I noticed that gcc generates awful code for a tail-call involving a trivial pass-through of a large struct parameter.

> cat bug1.c
struct s1 { int x[16]; };
extern void g1(struct s1);
void f1(struct s1 s1) { g1(s1); }

struct s2 { int x[17]; };
extern void g2(struct s2);
void f2(struct s2 s2) { g2(s2); }
> gcc -O2 -fomit-frame-pointer -S bug1.c
> cat bug1.s
        .file   "bug1.c"
        .text
        .p2align 4,,15
.globl f1
        .type   f1, @function
f1:
        subl    $12, %esp
        addl    $12, %esp
        jmp     g1
        .size   f1, .-f1
        .p2align 4,,15
.globl f2
        .type   f2, @function
f2:
        subl    $12, %esp
        movl    $17, %ecx
        movl    %edi, 8(%esp)
        leal    16(%esp), %edi
        movl    %esi, 4(%esp)
        movl    %edi, %esi
        rep movsl
        movl    4(%esp), %esi
        movl    8(%esp), %edi
        addl    $12, %esp
        jmp     g2
        .size   f2, .-f2
        .ident  "GCC: (GNU) 4.5.0 20100128 (experimental)"
        .section        .note.GNU-stack,"",@progbits

There are two problems with this code:
1. For the larger struct gcc generates a block copy with identical source and destination addresses, which amounts to a very slow NOP.
2. For the smaller struct gcc manages to eliminate the block copy, but it leaves pointless stack manipulation behind in the function (f1). However, gcc-4.3 generates no pointless stack manipulation:

.globl f1
        .type   f1, @function
f1:
        jmp     g1
        .size   f1, .-f1
        .ident  "GCC: (GNU) 4.3.5 20100103 (prerelease)"

so there's a code size and performance regression in 4.5/4.4.


---


### compiler : `gcc`
### title : `Argument unnecessarily spilled`
### open_at : `2010-01-31T22:54:01Z`
### last_modified_date : `2023-05-15T04:50:43Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=42919
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.5.0`
### severity : `enhancement`
### contents :
void foo(unsigned long long *x);
void testfunc2(unsigned long long a) { foo (&a); }

generates

testfunc2:
        pushl   %ebp
        movl    %esp, %ebp
        subl    $40, %esp
        movl    8(%ebp), %eax
        movl    %eax, -16(%ebp)
        movl    12(%ebp), %eax
        movl    %eax, -12(%ebp)
        leal    -16(%ebp), %eax
        movl    %eax, (%esp)
        call    foo
        leave
        ret

which is a lot worse to what compared to what 3.4 produced:

testfunc2:
        pushl   %ebp
        movl    %esp, %ebp
        leal    8(%ebp), %eax
        subl    $8, %esp
        movl    %eax, (%esp)
        call    foo
        leave
        ret


---


### compiler : `gcc`
### title : `Missed unused function return value elimination`
### open_at : `2010-02-05T11:03:39Z`
### last_modified_date : `2021-10-27T05:05:27Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=42970
### status : `ASSIGNED`
### tags : `missed-optimization, patch`
### component : `tree-optimization`
### version : `4.5.0`
### severity : `enhancement`
### contents :
IPA-SRA can do unused function parameter removal but misses unused return
value elimination.  This can be useful for a function like

int
quantum_gate_counter(int inc)
{
  static int counter = 0;

  if(inc > 0)
    counter += inc;
  else if(inc < 0)
    counter = 0;

  return counter;
}

which is only used in places that do not use the returned value in which
case the function should be optimized away completely, eliminating
the counter updates.  Note that this has to be done before inlining
into the callers to be effective.

The above missed-optimization blocks partial inlining of a function like

int flag;
int foo (void)
{
  quantum_gate_counter (1);
  if (!flag)
    return 0;

  ...
}


---


### compiler : `gcc`
### title : `Very bad bit field code`
### open_at : `2010-02-05T11:12:50Z`
### last_modified_date : `2021-07-20T23:59:37Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=42972
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.5.0`
### severity : `enhancement`
### contents :
Taken from http://hardwarebug.org/2010/01/30/bit-field-badness/

-----------------------------------
struct bf1_31 {
    unsigned a:1;
    unsigned b:31;
};

void func(struct bf1_31 *p, int n, int a)
{
    int i = 0;
    do {
        if (p[i].a)
            p[i].b += a;
    } while (++i < n);
}
-----------------------------------

GCC produces this dreadful code for arm-elf with options -march=armv5te -O3:

        .file   "t.c"
        .text
        .align  2
        .global func
        .type   func, %function
func:
        @ args = 0, pretend = 0, frame = 0
        @ frame_needed = 0, uses_anonymous_args = 0
        @ link register save eliminated.
        mov     r3, #0
        str     r4, [sp, #-4]!
.L3:
        ldrb    ip, [r0, #0]    @ zero_extendqisi2
        add     r3, r3, #1
        tst     ip, #1
        ldrne   ip, [r0, #0]
        addne   r4, r2, ip, lsr #1
        andne   ip, ip, #1
        orrne   ip, ip, r4, asl #1
        strne   ip, [r0, #0]
        cmp     r3, r1
        add     r0, r0, #4
        blt     .L3
        ldmfd   sp!, {r4}
        bx      lr
        .size   func, .-func
        .ident  "GCC: (GNU) 4.5.0 20100204 (experimental) [trunk revision 156492]"


What is wrong with this code:
1) The same value is loaded from memory twice (from [r0, #0])
2) Mask/shift/or operations are used where a simple shifted add would suffice
3) Write-back addressing is not used
4) The loop control counts up and compares instead of counting down

(Re. 4: The loop is clearly invertible. Does GCC fail to see this? Or is this optimization just not implemented?)


Hand-optimized assembly would look like this according to Hardwarebug:
func:
        ldr     r3,  [r0], #4
        tst     r3,  #1
        add     r3,  r3,  r2,  lsl #1
        strne   r3,  [r0, #-4]
        subs    r1,  r1,  #1
        bgt     func
        bx      lr

Best compiler available produces this:
func:
        mov     r3, #0
        push    {r4, lr}
loop:
        ldr     ip, [r0, r3, lsl #2]
        tst     ip, #1
        addne   ip, ip, r2, lsl #1
        strne   ip, [r0, r3, lsl #2]
        add     r3, r3, #1
        cmp     r3, r1
        blt     loop
        pop     {r4, pc}


Part of the problem seems to be that the redundant load is not exposed in GIMPLE (altough the RTL optimizers should also be able to see it). The .139t.optimized dump looks like this:

     1  ;; Function func (func)
     2
     3  func (struct bf1_31 * p, int n, int a)
     4  {
     5    long unsigned int ivtmp.16;
     6    int i;
     7    <unnamed-unsigned:31> D.1973;
     8    unsigned int D.1972;
     9    int D.1971;
    10    int D.1970;
    11    <unnamed-unsigned:31> D.1969;
    12    unsigned char D.1966;
    13    unsigned char D.1965;
    14    struct bf1_31 * D.1964;
    15
    16  <bb 2>:
    17    ivtmp.16_30 = (long unsigned int) p_5(D);
    18
    19  <bb 3>:
    20    # i_1 = PHI <0(2), i_21(5)>
    21    # ivtmp.16_32 = PHI <ivtmp.16_30(2), ivtmp.16_31(5)>
    22    D.1964_38 = (struct bf1_31 *) ivtmp.16_32;
    23    D.1965_7 = BIT_FIELD_REF <*D.1964_38, 8, 0>;
    24    D.1966_8 = D.1965_7 & 1;
    25    if (D.1966_8 != 0)
    26      goto <bb 4>;
    27    else
    28      goto <bb 5>;
    29
    30  <bb 4>:
    31    D.1969_15 = D.1964_38->b;
    32    D.1970_16 = (int) D.1969_15;
    33    D.1971_18 = a_17(D) + D.1970_16;
    34    D.1972_19 = (unsigned int) D.1971_18;
    35    D.1973_20 = (<unnamed-unsigned:31>) D.1972_19;
    36    D.1964_38->b = D.1973_20;
    37
    38  <bb 5>:
    39    i_21 = i_1 + 1;
    40    ivtmp.16_31 = ivtmp.16_32 + 4;
    41    if (i_21 < n_22(D))
    42      goto <bb 3>;
    43    else
    44      goto <bb 6>;
    45
    46  <bb 6>:
    47    return;
    48
    49  }



There are two loads from *D.1964_38 at line 23 and line 31, but one is a BIT_FIELD_REF and the other is an INDIRECT_REF, so the redundant load is not noticed.


RTL PRE fails to kill the redundant load because the expressions for the loads are not the same:

Index 0 (hash value 10)
  (zero_extend:SI (mem/s:QI (reg:SI 158 [ ivtmp.16 ]) [0+0 S1 A32]))
Index 3 (hash value 7)
  (mem/s:SI (reg:SI 158 [ ivtmp.16 ]) [0+0 S4 A32])


CSE also does not see the redundant load although it could notice it:

* It sees the path:
;; Following path with 17 sets: 3 4

* It sees the first load:
(insn 23 22 24 3 t.c:10 (set (reg:SI 169)
        (zero_extend:SI (mem/s:QI (reg:SI 158 [ ivtmp.16 ]) [0+0 S1 A32]))) 148 {*arm_zero_extendqisi2} (nil))

* It sees the second load:
(insn 31 30 32 4 t.c:11 (set (reg:SI 174)
        (mem/s:SI (reg:SI 158 [ ivtmp.16 ]) [0+0 S4 A32])) 166 {*arm_movsi_insn} (nil))

The problem here probably is the same as for RTL PRE, that the zero_extend hides the redundancy.


---


### compiler : `gcc`
### title : `-O2 doesn't use movl (A,B,4),C to its full extent to access an array`
### open_at : `2010-02-11T15:06:36Z`
### last_modified_date : `2021-08-09T06:01:05Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=43035
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.4.1`
### severity : `normal`
### contents :
The following code:

    typedef struct node { struct node **next; } node_t;
    __attribute__((fastcall)) void *f(node_t *n, int i) {
        return n->next[i];
    }

compiled with -O2 generates the following assembly (generated esp/ebp dead code removed for readability):

    f:
        movl    (%ecx), %eax
        movl    (%eax,%edx,4), %eax
        ret

which seems optimal. However, simply storing the return value in a variable damages the generated code:

    typedef struct node { struct node **next; } node_t;
    __attribute__((fastcall)) void *f(node_t *n, int i) {
        n = n->next[i];
        return n;
    }

generates:
    f:
        sall    $2, %edx
        addl    (%ecx), %edx
        movl    (%edx), %eax
        ret

which is less optimal than the previous version, for no reason.


---


### compiler : `gcc`
### title : `re-association doesn't handle multiple uses with constant operands`
### open_at : `2010-02-11T15:55:59Z`
### last_modified_date : `2021-07-26T07:34:58Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=43037
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `tree-optimization`
### version : `4.5.0`
### severity : `enhancement`
### contents :
int a, b;
void foo (int i, int x)
{
  int j, k, l;
  j = i * x;
  j = j * 5;
  k = j * 3;
  l = j * 4;
  a = k;
  b = l;
}

  j_3 = i_1(D) * 5;
  j_4 = j_3 * x_2(D);
  k_5 = j_4 * 3;
  l_6 = j_4 * 4;

should be re-associated and simplified to

  D.1_3 = i_1(D) * x_2(D);
  k_5 = D.1_3 * 15;
  l_6 = D.1_3 * 20;

note that this requires a value that is not computed previously and thus
is only profitable if all uses of j_4 will be dead after the transformation
unless it is possible to compute j_4 in terms of the new value with the
same number of operations.


---


### compiler : `gcc`
### title : `SSE shuffle merge`
### open_at : `2010-02-23T01:27:31Z`
### last_modified_date : `2023-08-22T04:32:24Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=43147
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `rtl-optimization`
### version : `12.0`
### severity : `enhancement`
### contents :
I've noticed that GCC (my current version is 4.4.1) doesn't fully optimize SSE shuffle merges, as seen in this example: 

#include <xmmintrin.h>
 
extern void printv(__m128 m);
 
int main()
{
	m = _mm_shuffle_ps(m, m, 0xC9); // Those two shuffles together swap pairs
	m = _mm_shuffle_ps(m, m, 0x2D); // And could be optimized to 0x4E
	printv(m);
 
	return 0;
}

This code generates the following assembly:

	movaps	.LC1, %xmm1
	shufps	$201, %xmm1, %xmm1
	shufps	$45, %xmm1, %xmm1    ; <-- Both should merge to 78
	movaps	%xmm1, %xmm0
	movaps	%xmm1, -24(%ebp)

	.LC0:
		.long	1065353216 ; 1.0f
		.long	1073741824 ; 2.0f
		.long	1077936128 ; 3.0f
		.long	1082130432 ; 4.0f

Would be nice to see it as an enhancement!


---


### compiler : `gcc`
### title : `GCC does not pull out a[0] from loop that changes a[i] for i:[1,n]`
### open_at : `2010-02-25T23:37:34Z`
### last_modified_date : `2021-07-26T07:45:40Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=43182
### status : `NEW`
### tags : `alias, missed-optimization`
### component : `middle-end`
### version : `4.5.0`
### severity : `enhancement`
### contents :
gcc 4.5 can not vectorize this simple loop:

void foo(int a[], int n) {
 int i;
 for(i=1; i< n; i++)
  a[i] = a[0];
}

"gcc -O3 -fdump-tree-vect-all -c foo.c" shows:
foo.c:3: note: not vectorized: unhandled data-ref 
foo.c:3: note: bad data references.
foo.c:1: note: vectorized 0 loops in function.

It seems gcc gets confused at a[0] and gives up vectorization. There
is no dependence in this loop, and we should teach gcc to handle a[0]
to vectorize it.


---


### compiler : `gcc`
### title : `Structure copies not vectorized`
### open_at : `2010-03-02T04:23:54Z`
### last_modified_date : `2021-08-05T22:21:48Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=43225
### status : `RESOLVED`
### tags : `missed-optimization`
### component : `target`
### version : `4.5.0`
### severity : `enhancement`
### contents :
Source:

#include <emmintrin.h>

struct a1 { char l[16];};
struct a2 { __m128i l; };

void f1(struct a1 *a, struct a1 *b)
{
    *a = *b;
}

void f2(struct a2 *a, struct a2 *b)
{
    *a = *b;
}

> /usr/local/gcc45/bin/gcc -O3 -fomit-frame-pointer -S copy_gcc.c
_f1:
        movq    (%rsi), %rax
        movq    %rax, (%rdi)
        movq    8(%rsi), %rax
        movq    %rax, 8(%rdi)
        ret

_f2:
        movdqa  (%rsi), %xmm0
        movdqa  %xmm0, (%rdi)
        ret

Both are appropriately aligned and should use movdqa. This might not show up in generic code, but I could have used it in an ffmpeg optimization.


---


### compiler : `gcc`
### title : `x86 flags not combined across blocks`
### open_at : `2010-03-02T19:17:06Z`
### last_modified_date : `2021-07-26T08:29:34Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=43233
### status : `NEW`
### tags : `missed-optimization`
### component : `middle-end`
### version : `4.5.0`
### severity : `enhancement`
### contents :
Source:
int g1,g2,g3;

int f1(int a, int b)
{
    a &= 1;
    
    if (a) return g1;
    return g2;
}

int f2(int a, int b)
{
    a &= 1;
    
    if (b)
        g3++;
    
    if (a) return g1;
    return g2;
}

Compiled with:
> gcc -O3 -fomit-frame-pointer -S and_flags.c

f1 is ok but f2 generates this:
_f2:
	andl	$1, %edi <-- #1
	testl	%esi, %esi
	je	L7
	movq	_g3@GOTPCREL(%rip), %rax
	incl	(%rax)
L7:
	testl	%edi, %edi <-- #2
	jne	L10
	movq	_g2@GOTPCREL(%rip), %rax
	movl	(%rax), %eax
	ret
	.align 4,0x90
L10:
	movq	_g1@GOTPCREL(%rip), %rax
	movl	(%rax), %eax
	ret

The andl and testl should be folded into one andl.

Code is reduced from ffmpeg h264 decoder. It's easy to work around by reordering source lines, so not too important.


---


### compiler : `gcc`
### title : `missed 'movw' optimization.`
### open_at : `2010-03-09T19:06:39Z`
### last_modified_date : `2022-01-05T23:28:05Z`
### link : https://gcc.gnu.org/bugzilla/show_bug.cgi?id=43311
### status : `NEW`
### tags : `missed-optimization`
### component : `target`
### version : `4.4.3`
### severity : `enhancement`
### contents :
reduced testcase:

typedef struct { unsigned char b1, b2; } __attribute__((aligned(8))) S;
void f( S const* s, unsigned char* b1, unsigned char* b2 )
{
        *b1 = s->b1;
        *b2 = s->b2;
}

generates at -Os and -O3:

f:
        movb    (%rdi), %al     # <variable>.b1, <variable>.b1
        movb    %al, (%rsi)     # <variable>.b1,* b1
        movb    1(%rdi), %al    # <variable>.b2, <variable>.b2
        movb    %al, (%rdx)     # <variable>.b2,* b2
        ret

gcc could (at least at -Os) reduce code size and memory accesses to:

        movw    (%rdi), %ax
        movb    %al, (%rsi)     # <variable>.b1,* b1
        movb    %ah, (%rdx)     # <variable>.b2,* b2
        ret


---
