### Total Bugs Detected: 101
### Current Chunk: 1 of 1
### Bugs in this Chunk: 101 (From bug 1 to 101)
---


### compiler : `llvm`
### title : `[JIT] Programs cannot resolve the fstat function`
### open_at : `2004-03-09T03:23:16Z`
### last_modified_date : `2020-07-01T18:23:24Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=274
### status : `RESOLVED`
### tags : `miscompilation`
### component : `MCJIT`
### version : `1.0`
### severity : `normal`
### contents :
Programs that use the 'fstat' function (such as GNU m4) are failing to work with
the JIT, because dlsym is apparently failing on it or something.

Here's a small testcase:

#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
int main() {
       struct stat SB;
       return fstat(1, &SB);
}

$ llvmgcc test.c -c -o - | lli
WARNING: Cannot resolve fn '__main' using a dummy noop function instead!
WARNING: Cannot resolve fn 'fstat' using a dummy noop function instead!

Note that the __main warning is expected, but the fstat one is not.

-Chris


---


### compiler : `llvm`
### title : `[livevar] Live variables missed physical register use of aliased definition`
### open_at : `2004-05-10T01:08:53Z`
### last_modified_date : `2018-11-07T08:17:41Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=337
### status : `RESOLVED`
### tags : `miscompilation`
### component : `Common Code Generator Code`
### version : `1.0`
### severity : `normal`
### contents :
The attached test case loads two longs from global constants (7 and 49),
compares them with SetLE, casts them to int, and returns the value from main.
This should give a program with a result value of 0 or 1. However, it always
returns 0. It should return 1 because 7 <= 49.

Here's the test case:

%global_long_1 = linkonce global long 7
%global_long_2 = linkonce global long 49
                                                                               
                                                            
implementation   ; Functions:
                                                                               
                                                            
declare void %exit(int)
                                                                               
                                                            
int %main() {
        %long_1 = getelementptr long* %global_long_1, long 0
        %long_2 = getelementptr long* %global_long_2, long 0
                                                                               
                                                            
        %l1 = load long* %long_1
        %l2 = load long* %long_2
                                                                               
                                                            
        %cond = setle long %l1, %l2
        %cast2 = cast bool %cond to int
        ret int %cast2
}


---


### compiler : `llvm`
### title : `"rem double x, y" always returns 0.0`
### open_at : `2005-08-03T17:24:43Z`
### last_modified_date : `2018-11-07T08:17:42Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=611
### status : `RESOLVED`
### tags : `miscompilation`
### component : `Common Code Generator Code`
### version : `1.4`
### severity : `normal`
### contents :
According to fmod(3), the remainder of dividing x by y (both FP) is "x - n * y"
where "n is the quotient of x / y, rounded towards zero to an integer.

In the x86 backend, we are not doing that rounding to an integer, but just
multiplying the result of x/y (as a floating-point value) back by y, and then
subtracing, leading to always returning 0.0 .

LLVM:

fastcc double %float_mod(double %x_2, double %y_3) {
 block0:
  ;; ** v12 = float_mod(x_2, y_3) **
  %v12 = rem double %x_2, %y_3
  br label %block1
 block1:
  %v4 = phi double [%v12, %block0]
  ret double %v4
}

X86 asm:

 float_mod:
   fldl 12(%esp)
   fldl 4(%esp)
   fld %st(0)
   fdiv %st(2)
   # MISSING rounding to integer!
   fmulp %st(2)
   fsubp %st(1)

Bug found by Eric van Riet Paap.  Thanks!


---


### compiler : `llvm`
### title : `instcombine misoptimizes shr+and to setgt`
### open_at : `2006-09-16T03:00:46Z`
### last_modified_date : `2018-11-07T08:17:43Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=913
### status : `RESOLVED`
### tags : `miscompilation`
### component : `Scalar Optimizations`
### version : `1.7`
### severity : `normal`
### contents :
The instruction combiner is making the following transformation:

        %tmp = load int* %tmp1          ; <int> [#uses=1]
        %tmp = cast int %tmp to uint            ; <uint> [#uses=1]
-       %tmp2 = shr uint %tmp, ubyte 5          ; <uint> [#uses=1]
-       %tmp2 = cast uint %tmp2 to int          ; <int> [#uses=1]
-       %tmp3 = and int %tmp2, 1                ; <int> [#uses=1]
-       %tmp3 = cast int %tmp3 to bool          ; <bool> [#uses=1]
-       %tmp34 = cast bool %tmp3 to int         ; <int> [#uses=1]
+       %tmp3 = setgt uint %tmp, 31             ; <bool> [#uses=1]
+       %tmp34 = cast bool %tmp3 to int         ; <int> [#uses=2]

simplifying "(x >> 5) & 1 != 0" into "x > 31". They are not the same; consider
64: 64 >> 5 = 2, 2 & 1 = 0. But 64 > 31.


---


### compiler : `llvm`
### title : `Infinite loops are optimized out in languages without forward progress guarantees (C, Rust)`
### open_at : `2006-10-23T02:33:40Z`
### last_modified_date : `2021-01-24T22:54:27Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=965
### status : `RESOLVED`
### tags : `miscompilation`
### component : `Interprocedural Analyses`
### version : `trunk`
### severity : `normal`
### contents :
Hi,

I have been playing with functions marked __attribute__((noreturn));
Specifically consider a following code:

void f(void) __attribute__((noreturn));

int call_f()
{
    f();
}

void f()
{
    while(1)
        ;
}

With "opt -globalsmodref-aa -adce" this gets compiled to:

int %call_f() {
entry:
    %retval = alloca int, align 4           ; <int*> [#uses=1]
    unreachable ; **** WRONG!!
    
return:         ; No predecessors!
    %retval = load int* %retval             ; <int> [#uses=1]
    ret int %retval
    
void %f() {
entry:
    br label %bb
    
bb:             ; preds = %bb, %entry
    br label %bb
    
return:         ; No predecessors!
    ret void    
}


---


### compiler : `llvm`
### title : `llvm.memcpy.i64 miscompiled on 32-bit target`
### open_at : `2006-11-07T03:56:50Z`
### last_modified_date : `2018-11-07T08:17:30Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=987
### status : `RESOLVED`
### tags : `miscompilation`
### component : `Common Code Generator Code`
### version : `trunk`
### severity : `normal`
### contents :
I'm encountering a lot of nightly testcase failures and am bugpointing them.
I'll attach examples of .ll and matching .s for testcases that I think are all
the same bug.

I have no idea what the bug is yet.


---


### compiler : `llvm`
### title : `codegen problem with 'complex' type on x86/linux`
### open_at : `2006-11-08T02:29:33Z`
### last_modified_date : `2018-11-07T08:17:29Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=990
### status : `RESOLVED`
### tags : `miscompilation`
### component : `Backend: X86`
### version : `1.9`
### severity : `normal`
### contents :
I've noticed a pattern in my testcase failures involving "csretcc". The bug
occurs with a simple testcase from the "cexp" man page:

// RUN: %llvmgcc -O2 -lm %s -o %s.exe
// RUN: ./%s.exe | grep "-1.000000+0.000000*i"
#include <stdio.h>

/* check that exp(i*pi) == -1 */
#include <math.h>   /* for atan */
#include <complex.h>
int main(void) {
  double pi = 4*atan(1);
  complex z = cexp(I*pi);
  printf("%f+%f*i\n", creal(z), cimag(z));
}

With LLVM, this produces:

$ llvm-gcc -O0 csretcc.c -lm -o csretcc
$ ./csretcc
0.000000+0.000000*i
Segmentation fault

while with GCC, it works:

$ gcc -O0 csretcc.c -lm -o csretcc
$ ./csretcc
-1.000000+0.000000*i

In the bytecode, the call to "cexp" is called with "csretcc" calling convention.


---


### compiler : `llvm`
### title : `MultiSource/Benchmarks/Prolangs-C/allroots broken on x86`
### open_at : `2006-11-10T20:12:37Z`
### last_modified_date : `2018-11-07T08:17:28Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=996
### status : `RESOLVED`
### tags : `miscompilation`
### component : `Backend: X86`
### version : `trunk`
### severity : `normal`
### contents :
This test is definitely broken. Please find attached LLVM bytecode & generated
assembler code.

Generated code segfaults at first "movaps" instruction in newton function. llc
-march=pentium3 generates working code.


---


### compiler : `llvm`
### title : `instcombine + dagcombine miscompilation`
### open_at : `2006-11-27T18:31:38Z`
### last_modified_date : `2018-11-07T08:17:41Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=1014
### status : `RESOLVED`
### tags : `miscompilation`
### component : `Scalar Optimizations`
### version : `trunk`
### severity : `normal`
### contents :
Consider the attached .ll file.

It will ask a number as input. Input "32".
Correct answer is "41". It can be obtained via cbackend. Both llc and lli
generate code, which produces "186".


---


### compiler : `llvm`
### title : `-instcombine miscompilation of MiBench/consumer-typeset`
### open_at : `2007-01-12T08:55:23Z`
### last_modified_date : `2018-11-07T08:17:44Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=1107
### status : `RESOLVED`
### tags : `miscompilation`
### component : `Scalar Optimizations`
### version : `trunk`
### severity : `normal`
### contents :
I have been trying to solve a little mystery. After resolving various issues
with the test case itsellf (MultisSource/Benchmarks/MiBench/consumer-typeset), I
have determined that there is a codegen bug that this test triggers when
-instcombine is run. Here's how I know this:

1. If you run the Output/consumer-typeset.linked.rbc file through lli in JIT 
   mode it works fine.

2. All three backends (llc,jit,cbe) fail in the same way. They all produce the
   same incorrect output. This indicates a misoptimization rather than a code
   gen bug.

3. I used findmisopt to find the first optimization that caused the output to 
   differ. It reported this sequence of optimizations as the first set that
   produces a difference in the output:
      -lowersetjmp -funcresolve -raiseallocs -simplifycfg -mem2reg -globalopt
      -globaldce -ipconstprop -deadargelim -instcombine
4. bugpoint produces a non-sensical reduction (two branches and a return) 

I'm wondernig if someone can bugpoint this on Darwin because I'm starting to
think that bugpoint doesn't work so well on Linux. In the last month, a Darwin
run of bugpoint was able to reduce a test case that a run on Linux, with the
same inputs, could not reduce. If you can reduce this on Darwin, I'll file a bug
against bugpoint.


---


### compiler : `llvm`
### title : `Bug in LoopSimplfy pass`
### open_at : `2007-03-09T15:07:12Z`
### last_modified_date : `2018-11-07T08:17:29Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=1246
### status : `RESOLVED`
### tags : `miscompilation`
### component : `Loop Optimizer`
### version : `trunk`
### severity : `normal`
### contents :
Consider the attached bytecode. Be careful with re-assembling - you can hit PR1245.

Everything is ok with "llc -fast" or with disabled LoopStrengthReduce pass (or
cbe), but segfault with enabled.

Segfault occurs in bb43 BB. The variable %i1.0_cc becames uninitialized.
Initialization occurs in the meshBB BB, but it seems, that LSR incorrectly moves
it somewhere. 

Target triple is, unfortunately, set to mingw32, but bytecode should run ok any
ia32 platform, it doesn't contain any target-specific code. Unfortunately, until
PR1245 is fixed, I cannot change it :(

Please also note, that "opt -std-compile-opts" is buggy on this bytecode, but
it's subject for future investigation (maybe due to PR1245).


---


### compiler : `llvm`
### title : `Miscompilation passing struct by value to varargs function`
### open_at : `2007-03-10T20:53:04Z`
### last_modified_date : `2018-11-07T08:17:36Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=1249
### status : `RESOLVED`
### tags : `miscompilation`
### component : `llvm-gcc`
### version : `trunk`
### severity : `normal`
### contents :
Consider the attached C source (from gcc testsuite).

The call to function f is converted to LLVM IR incorrectly: i8/16 args will be
extended to 32 bits, but args handling logic in f() itself assumes, that they
are all in place.


---


### compiler : `llvm`
### title : `Instcombine broken after APIntification`
### open_at : `2007-03-25T20:59:59Z`
### last_modified_date : `2018-11-07T08:17:31Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=1271
### status : `RESOLVED`
### tags : `miscompilation`
### component : `Scalar Optimizations`
### version : `trunk`
### severity : `normal`
### contents :
instcombine is broken now.

This leads to big miscompilations here and there.
The smallest testcase is:
Regression/C/2003-05-21-UnionBitfields.c


---


### compiler : `llvm`
### title : `-O2/-O3 breaks reverse iterators`
### open_at : `2013-06-22T21:15:11Z`
### last_modified_date : `2019-10-29T08:24:13Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=16421
### status : `RESOLVED`
### tags : `miscompilation`
### component : `Global Analyses`
### version : `trunk`
### severity : `normal`
### contents :
#include <cstddef>
#include <iostream>
#include <vector>
#include <numeric>
int main()
{
    std::vector<double> wd(5);
    std::iota(wd.rbegin(), wd.rend(), 1.0);
    for (std::size_t i = 0; i < wd.size(); ++i)
        std::cout << wd[i] << ", ";
    for (std::ptrdiff_t i = wd.size() - 1; i >= 0; --i)
        std::cout << wd[i] << ", ";
}

This code yields the expected result when compiled with -O1:
5, 4, 3, 2, 1, 1, 2, 3, 4, 5, 
When compiling with -O2 or -O3, it breaks, however:
0, 4, 3, 2, 1, 1, 2, 3, 4, 5, 

That's a pretty heavy bug if you ask me. It has affected me in a real application.
Interestingly, if the two loops are interchanged, the bug disappears. The sample is compiled correctly when using gcc 4.6, 4.7, 4.8 as well as Intel C++ 13.1. It is also broken in Clang 3.2

Possible duplicate is http://llvm.org/bugs/show_bug.cgi?id=12531


---


### compiler : `llvm`
### title : `Improper decaying of pointers to arrays as template parameters`
### open_at : `2014-07-24T06:18:25Z`
### last_modified_date : `2020-04-23T20:43:33Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=20430
### status : `RESOLVED`
### tags : `miscompilation`
### component : `C++`
### version : `trunk`
### severity : `normal`
### contents :
The following code outputs 1 instead of 5, as if the template parameter were decaying to "const char *" instead of being the proper "const char (*)[5]":

#include <cstdio>

template <const char (*STR)[5]>
unsigned TestBug()
{
	return sizeof(*STR);
}

extern const char g_meow[5] = "meow";

int main()
{
	std::printf("%u\n", TestBug<&g_meow>());
	return 0;
}

This works correctly if TestBug were to take STR as a runtime parameter, including constexpr functions evaluated at compile time.  For example, the following code prints 5:

#include <cstdio>

constexpr unsigned TestBug(const char (*STR)[5])
{
    return sizeof(*STR);
}

extern const char g_meow[5] = "meow";

template <unsigned N>
struct Number
{
    enum ValueType : unsigned { Value = N };
};

int main()
{
	std::printf("%u\n", static_cast<unsigned>(Number<TestBug(&g_meow)>::Value));
	return 0;
}

This is all possibly related to bug 6226 or its fix, from the description of that bug.


---


### compiler : `llvm`
### title : `mcount inlining bug when -pg and -O2 enabled`
### open_at : `2016-07-22T08:11:03Z`
### last_modified_date : `2020-10-12T20:05:58Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=28660
### status : `RESOLVED`
### tags : `miscompilation`
### component : `LLVM Codegen`
### version : `trunk`
### severity : `normal`
### contents :
See the simple example below.

$ cat mcount-test.c
int bar()
{
  return 0;
}

int foo()
{
  return bar();
}

int main()
{
  return foo();
}

If the example is compiled with -pg and -O2 options. It generates the code as below:

$ clang -pg -O2 -S mcount-test.c
$ cat mcount-test.s
(shows assembly code only ...)
bar:
        pushq   %rbp
        movq    %rsp, %rbp
        callq   mcount
        xorl    %eax, %eax
        popq    %rbp
        retq

foo:
        pushq   %rbp
        movq    %rsp, %rbp
        callq   mcount
        callq   mcount       @ (1) calling bar is inlined with mcount
        xorl    %eax, %eax
        popq    %rbp
        retq

main:
        pushq   %rbp
        movq    %rsp, %rbp
        callq   mcount
        callq   mcount       @ (2) calling foo is inlined with mcount
        callq   mcount       @ (3) calling bar is inlined with mcount
        xorl    %eax, %eax
        popq    %rbp
        retq

As I put some comments, the problem is that function inlining is done with mcount call.
bar() has a single mcount at the entry of function, but foo() has two mcount calls. It's because bar is inlined with its mcount call into foo's body.  And also main() has three mcount calls because the foo() is inlined its own mcount and its body that has two mcount calls inside.

This is tested on the current trunk.


---


### compiler : `llvm`
### title : `Invalid subexpression in sizeof fails to remove candidate`
### open_at : `2016-07-22T18:44:46Z`
### last_modified_date : `2021-10-15T22:49:54Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=28667
### status : `RESOLVED`
### tags : `accepts-invalid, compile-fail, miscompilation`
### component : `C++11`
### version : `trunk`
### severity : `normal`
### contents :
In the following case, Clang fails to detect an error in the subexpression of
the sizeof during substitution of the template arguments into the signature of
the function in question.

Online compiler: http://melpon.org/wandbox/permlink/by24bjnKIvVPecSH

### SOURCE (<stdin>):
struct A { A(int); };

template <typename T> void foo(void *, char (*)[sizeof(0, A(T()))]) { }
template <typename T> void foo(int, ...);

int main(void) { foo<decltype(nullptr)>(0, 0); }


### COMPILER INVOCATION:
clang++ -cc1 -fsyntax-only -x c++ -std=c++11 -


### EXPECTED OUTPUT:
(clean compile)


### ACTUAL OUTPUT:
<stdin>:6:18: error: call to 'foo' is ambiguous
int main(void) { foo<decltype(nullptr)>(0, 0); }
                 ^~~~~~~~~~~~~~~~~~~~~~
<stdin>:3:28: note: candidate function [with T = nullptr_t]
template <typename T> void foo(void *, char (*)[sizeof(0, A(T()))]) { }
                           ^
<stdin>:4:28: note: candidate function [with T = nullptr_t]
template <typename T> void foo(int, ...);
                           ^
1 error generated.


### COMPILER VERSION INFO (clang++ -v):
clang version 4.0.0 (trunk 276290)
Target: x86_64-unknown-linux-gnu
Thread model: posix
InstalledDir: /usr/local/llvm-head/bin
Found candidate GCC installation: /usr/lib/gcc/x86_64-linux-gnu/4.6
Found candidate GCC installation: /usr/lib/gcc/x86_64-linux-gnu/4.6.3
Selected GCC installation: /usr/lib/gcc/x86_64-linux-gnu/4.6
Candidate multilib: .;@m64
Candidate multilib: 32;@m32
Selected multilib: .;@m64


---


### compiler : `llvm`
### title : `InstCombine can't fold "select %c, undef, %foo" to %foo  (miscompile)`
### open_at : `2017-01-13T19:25:33Z`
### last_modified_date : `2021-03-22T08:48:28Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=31633
### status : `RESOLVED`
### tags : `miscompilation`
### component : `Scalar Optimizations`
### version : `trunk`
### severity : `normal`
### contents :
InstCombine currently folds  "select %c, undef, %foo" into %foo, because it assumes that undef can take any value that %foo may take.
This is not correct since %foo may be poison.
This problem has long been know, but I'm adding now an end-to-end miscompilation example triggered by this bug.

$ cat select-undef.ll
define i1 @f(i1 %c, i32 %y) {
  %y2 = add nsw i32 %y, 1
  %s = select i1 %c, i32 undef, i32 %y2
  %r = icmp sgt i32 %s, %y
  ret i1 %r
}

$ opt -S select-undef.ll -instcombine
define i1 @f(i1 %c, i32 %y) {
  ret i1 true
}

Which is wrong for the case %y=0x7FFFFFFF and %c=true. %y2 overflows and becomes poison, but the select should return undef only, not poison.
Alive report: http://rise4fun.com/Alive/XGW

Related with PR31632.


---


### compiler : `llvm`
### title : `Loop unswitch and GVN interact badly and miscompile`
### open_at : `2017-01-16T13:19:41Z`
### last_modified_date : `2021-07-14T12:48:57Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=31652
### status : `NEW`
### tags : `miscompilation`
### component : `Scalar Optimizations`
### version : `trunk`
### severity : `normal`
### contents :
Created attachment 17845
Reduced IR test case

Loop unswitch and GVN when taken together can miscompile code due to disagreeing semantics of branch on undef.
In our opinion it's loop unswitch that is incorrect.

Test case in C:
static volatile int always_false = 0;

void maybe_init(int *p) {}

int f(int limit0) {
  int maybe_undef_loc;
  maybe_init(&maybe_undef_loc);

  int limit = limit0;
  int total = 0;
  for (int i = 0; i < limit; i++) {
    total++;
    if (always_false) {
      if (maybe_undef_loc != (limit0 + 10)) {
        total++;
      }
    }
    limit = limit0 + 10;
  }
  return total;
}

int printf(const char *, ...);

int main(int argc, char **argv) {
  printf("f(10) = %d\n", f(10));
  return 0;
}


I believe this test case has no UB even at C level. It should print "f(10) = 20".

I've attached a reduced IR test case.


Running LICM, the comparison of maybe_undef_loc gets hoisted:

$ opt -S bug.ll -loop-rotate -licm
...
loop.body.lr.ph:
  %undef_loc = load i32, i32* %maybe_undef_loc, align 4
  %add = add nsw i32 %limit0, 10
  %cmp3 = icmp ne i32 %undef_loc, %add
  %limit2 = add nsw i32 %limit0, 10
  br label %loop.body
...


This is still ok. But then adding loop unswitch:

$ opt -S bug.ll -loop-rotate -licm -loop-unswitch
...
loop.body.lr.ph:
  %undef_loc = load i32, i32* %maybe_undef_loc, align 4
  %add = add nsw i32 %limit0, 10
  %cmp3 = icmp ne i32 %undef_loc, %add
  %limit2 = add nsw i32 %limit0, 10
  br i1 %cmp3, label %loop.body.lr.ph.split.us, label %loop.body.lr.ph.loop.body.lr.ph.split_crit_edge
...

Loop unswitch introduce a branch on %cmp3, which will be undef once we inline maybe_init(). Hence loop unswitch assumes branch on undef is a non-deterministic jump (so not UB).
By running GVN after loop unswitch, we clearly see that GVN has a different perspective on the semantics of branch on undef. It produces this diff:
-  %limit2 = add nsw i32 %limit0, 10
...
-  %cmp = icmp slt i32 %i2, %limit2
+  %cmp = icmp slt i32 %i2, %undef_loc

I'm not including the context here, but to be able to justify this transformation, branch on undef has to be UB, not a non-deterministic jump as assumed by loop unswitch above.

Putting all things together:
$ opt -S bug.ll -loop-rotate -licm -loop-unswitch -gvn | opt -S -O2 | llc -o x.S && clang x.S -o x && ./x
f(10) = 1

This is wrong. Should be 20, not 1.

This example shows how Loop unswitch and GVN can produce a miscompilation end-to-end. The bug can be fixed by using the proposed freeze instruction in loop unswitch.

(Example by Sanjoy)


---


### compiler : `llvm`
### title : `Simpify* cannot distribute instructions for simplification due to undef`
### open_at : `2017-05-25T09:13:43Z`
### last_modified_date : `2020-10-22T16:51:58Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=33165
### status : `RESOLVED`
### tags : `miscompilation`
### component : `Scalar Optimizations`
### version : `trunk`
### severity : `normal`
### contents :
$ cat a.ll
define i2 @f(i2, i1) {
  %a = xor i2 %0, -1
  %b = select i1 %1, i2 %a, i2 undef
  %c = and i2 %a, %b
  ret i2 %c
}

$ opt -S a.ll -newgvn
define i2 @f(i2, i1) {
  %a = xor i2 %0, -1
  %b = select i1 %1, i2 %a, i2 undef
  ret i2 %b
}

This is incorrect. Alive report:

ERROR: Mismatch in values of i2 ret_

Example:
%0 i2 = 0x2 (2, -2)
%1 i1 = 0x0 (0)
%a i2 = 0x1 (1)
%b i2 = 0x0 (0)
%c i2 = 0x0 (0)
Source value: 0x0 (0)
Target value: 0x2 (2, -2)

http://rise4fun.com/Alive/dKH


GVN gets this right (http://rise4fun.com/Alive/n6D):
$ opt -S a.ll -gvn
define i2 @f(i2, i1) {
  %a = xor i2 %0, -1
  ret i2 %a
}


---


### compiler : `llvm`
### title : `Assertion failure/bad codegen: too many args w/inherited constructor from virtual base in ctor-initializer`
### open_at : `2017-09-01T05:11:58Z`
### last_modified_date : `2021-11-03T11:14:56Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=34401
### status : `CONFIRMED`
### tags : `miscompilation`
### component : `C++17`
### version : `trunk`
### severity : `normal`
### contents :
When a mem-initializer selects an inherited constructor from a virtual base and the object it constructs is not a complete object, Clang tries to pass more arguments than it should.

### SOURCE (<stdin>):
struct V { V() = default; V(int); };
struct A : virtual V {
  using V::V;
  A() : A(19) { }
};
struct B : A { } b;


### COMPILER INVOCATION:
clang++ -cc1 -xc++ -std=c++1z -emit-llvm -


### EXPECTED OUTPUT:
(Clean compile)


### ACTUAL OUTPUT:
clang++: /llvm_trunk/llvm/tools/clang/lib/CodeGen/CGCall.cpp:4112: clang::CodeGen::RValue clang::CodeGen::CodeGenFunction::EmitCall(const clang::CodeGen::CGFunctionInfo&, const clang::CodeGen::CGCallee&, clang::CodeGen::ReturnValueSlot, const clang::CodeGen::CallArgList&, llvm::Instruction**): Assertion `IRCallArgs.size() == IRFuncTy->getNumParams() || IRFuncTy->isVarArg()' failed.
#0 0x000000001481a998 llvm::sys::PrintStackTrace(llvm::raw_ostream&) /llvm_trunk/llvm/lib/Support/Unix/Signals.inc:398:0
#1 0x000000001481aa9c PrintStackTraceSignalHandler(void*) /llvm_trunk/llvm/lib/Support/Unix/Signals.inc:461:0
#2 0x000000001481877c llvm::sys::RunSignalHandlers() /llvm_trunk/llvm/lib/Support/Signals.cpp:50:0
#3 0x0000000014819f40 SignalHandler(int) /llvm_trunk/llvm/lib/Support/Unix/Signals.inc:242:0
#4 0x00003fff840e0478  0x478 __GI_abort
#5 0x00003fff840e0478
#6 0x00003fff840e0478 __assert_fail_base (+0x478)
#7 0x00003fff83b30d70 __GI___assert_fail (/lib64/libc.so.6+0x40d70)
#8 0x00003fff83b248a4 clang::CodeGen::CodeGenFunction::EmitCall(clang::CodeGen::CGFunctionInfo const&, clang::CodeGen::CGCallee const&, clang::CodeGen::ReturnValueSlot, clang::CodeGen::CallArgList const&, llvm::Instruction**) /llvm_trunk/llvm/tools/clang/lib/CodeGen/CGCall.cpp:4112:0
#9 0x00003fff83b24994 clang::CodeGen::CodeGenFunction::EmitCXXConstructorCall(clang::CXXConstructorDecl const*, clang::CXXCtorType, bool, bool, clang::CodeGen::Address, clang::CodeGen::CallArgList&) /llvm_trunk/llvm/tools/clang/lib/CodeGen/CGClass.cpp:2061:0
#10 0x0000000015057448 clang::CodeGen::CodeGenFunction::EmitCXXConstructorCall(clang::CXXConstructorDecl const*, clang::CXXCtorType, bool, bool, clang::CodeGen::Address, clang::CXXConstructExpr const*) /llvm_trunk/llvm/tools/clang/lib/CodeGen/CGClass.cpp:1979:0
#11 0x0000000015080cd4 clang::CodeGen::CodeGenFunction::EmitCXXConstructExpr(clang::CXXConstructExpr const*, clang::CodeGen::AggValueSlot) /llvm_trunk/llvm/tools/clang/lib/CodeGen/CGExprCXX.cpp:622:0
#12 0x0000000015080518 (anonymous namespace)::AggExprEmitter::VisitCXXConstructExpr(clang::CXXConstructExpr const*) /llvm_trunk/llvm/tools/clang/lib/CodeGen/CGExprAgg.cpp:1001:0
#13 0x000000001511be9c clang::StmtVisitorBase<clang::make_ptr, (anonymous namespace)::AggExprEmitter, void>::Visit(clang::Stmt*) /tools/clang/include/clang/AST/StmtNodes.inc:213:0
#14 0x000000001510c0a8 (anonymous namespace)::AggExprEmitter::Visit(clang::Expr*) /llvm_trunk/llvm/tools/clang/lib/CodeGen/CGExprAgg.cpp:104:0
#15 0x00000000151103d0 clang::CodeGen::CodeGenFunction::EmitAggExpr(clang::Expr const*, clang::CodeGen::AggValueSlot) /llvm_trunk/llvm/tools/clang/lib/CodeGen/CGExprAgg.cpp:1532:0
#16 0x000000001510791c clang::CodeGen::CodeGenFunction::EmitDelegatingCXXConstructorCall(clang::CXXConstructorDecl const*, clang::CodeGen::FunctionArgList const&) /llvm_trunk/llvm/tools/clang/lib/CodeGen/CGClass.cpp:2289:0
#17 0x000000001510efb8 clang::CodeGen::CodeGenFunction::EmitCtorPrologue(clang::CXXConstructorDecl const*, clang::CXXCtorType, clang::CodeGen::FunctionArgList&) /llvm_trunk/llvm/tools/clang/lib/CodeGen/CGClass.cpp:1243:0
#18 0x000000001508242c clang::CodeGen::CodeGenFunction::EmitConstructorBody(clang::CodeGen::FunctionArgList&) /llvm_trunk/llvm/tools/clang/lib/CodeGen/CGClass.cpp:839:0
#19 0x000000001507d230 clang::CodeGen::CodeGenFunction::GenerateCode(clang::GlobalDecl, llvm::Function*, clang::CodeGen::CGFunctionInfo const&) /llvm_trunk/llvm/tools/clang/lib/CodeGen/CodeGenFunction.cpp:1218:0
#20 0x000000001507aef0 clang::CodeGen::CodeGenModule::codegenCXXStructor(clang::CXXMethodDecl const*, clang::CodeGen::StructorType) /llvm_trunk/llvm/tools/clang/lib/CodeGen/CGCXX.cpp:234:0
#21 0x0000000014d88f18 (anonymous namespace)::ItaniumCXXABI::emitCXXStructor(clang::CXXMethodDecl const*, clang::CodeGen::StructorType) /llvm_trunk/llvm/tools/clang/lib/CodeGen/ItaniumCXXABI.cpp:3668:0
#22 0x000000001503bcf8 clang::CodeGen::CodeGenModule::EmitGlobalDefinition(clang::GlobalDecl, llvm::GlobalValue*) /llvm_trunk/llvm/tools/clang/lib/CodeGen/CodeGenModule.cpp:2011:0
#23 0x0000000014f92b50 clang::CodeGen::CodeGenModule::EmitDeferred() /llvm_trunk/llvm/tools/clang/lib/CodeGen/CodeGenModule.cpp:1440:0
#24 0x0000000014daf498 clang::CodeGen::CodeGenModule::EmitDeferred() /llvm_trunk/llvm/tools/clang/lib/CodeGen/CodeGenModule.cpp:1447:0
#25 0x0000000014dabff8 clang::CodeGen::CodeGenModule::Release() /llvm_trunk/llvm/tools/clang/lib/CodeGen/CodeGenModule.cpp:385:0
#26 0x0000000014dac068 (anonymous namespace)::CodeGeneratorImpl::HandleTranslationUnit(clang::ASTContext&) /llvm_trunk/llvm/tools/clang/lib/CodeGen/ModuleBuilder.cpp:265:0
#27 0x0000000014da5ea0 clang::BackendConsumer::HandleTranslationUnit(clang::ASTContext&) /llvm_trunk/llvm/tools/clang/lib/CodeGen/CodeGenAction.cpp:204:0
#28 0x0000000015b478a0 clang::ParseAST(clang::Sema&, bool, bool) /llvm_trunk/llvm/tools/clang/lib/Parse/ParseAST.cpp:159:0
#29 0x0000000015b3bf14 clang::ASTFrontendAction::ExecuteAction() /llvm_trunk/llvm/tools/clang/lib/Frontend/FrontendAction.cpp:1004:0
#30 0x0000000016d027d8 clang::CodeGenAction::ExecuteAction() /llvm_trunk/llvm/tools/clang/lib/CodeGen/CodeGenAction.cpp:992:0
#31 0x0000000015482c6c clang::FrontendAction::Execute() /llvm_trunk/llvm/tools/clang/lib/Frontend/FrontendAction.cpp:902:0
#32 0x0000000015b3936c clang::CompilerInstance::ExecuteAction(clang::FrontendAction&) /llvm_trunk/llvm/tools/clang/lib/Frontend/CompilerInstance.cpp:986:0
#33 0x00000000154824d4 clang::ExecuteCompilerInvocation(clang::CompilerInstance*) /llvm_trunk/llvm/tools/clang/lib/FrontendTool/ExecuteCompilerInvocation.cpp:252:0
#34 0x00000000153fb814 cc1_main(llvm::ArrayRef<char const*>, char const*, void*) /llvm_trunk/llvm/tools/clang/tools/driver/cc1_main.cpp:221:0
#35 0x0000000015657598 ExecuteCC1Tool(llvm::ArrayRef<char const*>, llvm::StringRef) /llvm_trunk/llvm/tools/clang/tools/driver/driver.cpp:302:0
#36 0x0000000011bd2e04 main /llvm_trunk/llvm/tools/clang/tools/driver/driver.cpp:381:0
#37 0x0000000011bc137c generic_start_main.isra.0 (/bin/clang+++0x11bc137c)
#38 0x0000000011bc1fb8 __libc_start_main (/bin/clang+++0x11bc1fb8)
/bin/clang++(_ZN4llvm3sys15PrintStackTraceERNS_11raw_ostreamE+0x58)[0x1481a998]
/bin/clang++[0x1481aa9c]
/bin/clang++(_ZN4llvm3sys17RunSignalHandlersEv+0xb4)[0x1481877c]
/bin/clang++[0x14819f40]
[0x3fff840e0478]
/lib64/libc.so.6(abort+0x280)[0x3fff83b30d70]
/lib64/libc.so.6(+0x348a4)[0x3fff83b248a4]
/lib64/libc.so.6(__assert_fail+0x64)[0x3fff83b24994]
/bin/clang++(_ZN5clang7CodeGen15CodeGenFunction8EmitCallERKNS0_14CGFunctionInfoERKNS0_8CGCalleeENS0_15ReturnValueSlotERKNS0_11CallArgListEPPN4llvm11InstructionE+0x2738)[0x15057448]
/bin/clang++(_ZN5clang7CodeGen15CodeGenFunction22EmitCXXConstructorCallEPKNS_18CXXConstructorDeclENS_11CXXCtorTypeEbbNS0_7AddressERNS0_11CallArgListE+0x5ac)[0x15080cd4]
/bin/clang++(_ZN5clang7CodeGen15CodeGenFunction22EmitCXXConstructorCallEPKNS_18CXXConstructorDeclENS_11CXXCtorTypeEbbNS0_7AddressEPKNS_16CXXConstructExprE+0x2b4)[0x15080518]
/bin/clang++(_ZN5clang7CodeGen15CodeGenFunction20EmitCXXConstructExprEPKNS_16CXXConstructExprENS0_12AggValueSlotE+0x454)[0x1511be9c]
/bin/clang++[0x1510c0a8]
/bin/clang++[0x151103d0]
/bin/clang++[0x1510791c]
/bin/clang++(_ZN5clang7CodeGen15CodeGenFunction11EmitAggExprEPKNS_4ExprENS0_12AggValueSlotE+0x164)[0x1510efb8]
/bin/clang++(_ZN5clang7CodeGen15CodeGenFunction32EmitDelegatingCXXConstructorCallEPKNS_18CXXConstructorDeclERKNS0_15FunctionArgListE+0xf4)[0x1508242c]
/bin/clang++(_ZN5clang7CodeGen15CodeGenFunction16EmitCtorPrologueEPKNS_18CXXConstructorDeclENS_11CXXCtorTypeERNS0_15FunctionArgListE+0x58)[0x1507d230]
/bin/clang++(_ZN5clang7CodeGen15CodeGenFunction19EmitConstructorBodyERNS0_15FunctionArgListE+0x294)[0x1507aef0]
/bin/clang++(_ZN5clang7CodeGen15CodeGenFunction12GenerateCodeENS_10GlobalDeclEPN4llvm8FunctionERKNS0_14CGFunctionInfoE+0x2d4)[0x14d88f18]
/bin/clang++(_ZN5clang7CodeGen13CodeGenModule18codegenCXXStructorEPKNS_13CXXMethodDeclENS0_12StructorTypeE+0x17c)[0x1503bcf8]
/bin/clang++[0x14f92b50]
/bin/clang++(_ZN5clang7CodeGen13CodeGenModule20EmitGlobalDefinitionENS_10GlobalDeclEPN4llvm11GlobalValueE+0x168)[0x14daf498]
/bin/clang++(_ZN5clang7CodeGen13CodeGenModule12EmitDeferredEv+0x1fc)[0x14dabff8]
/bin/clang++(_ZN5clang7CodeGen13CodeGenModule12EmitDeferredEv+0x26c)[0x14dac068]
/bin/clang++(_ZN5clang7CodeGen13CodeGenModule7ReleaseEv+0x30)[0x14da5ea0]
/bin/clang++[0x15b478a0]
/bin/clang++[0x15b3bf14]
/bin/clang++(_ZN5clang8ParseASTERNS_4SemaEbb+0x364)[0x16d027d8]
/bin/clang++(_ZN5clang17ASTFrontendAction13ExecuteActionEv+0x1d4)[0x15482c6c]
/bin/clang++(_ZN5clang13CodeGenAction13ExecuteActionEv+0x4a4)[0x15b3936c]
/bin/clang++(_ZN5clang14FrontendAction7ExecuteEv+0xbc)[0x154824d4]
/bin/clang++(_ZN5clang16CompilerInstance13ExecuteActionERNS_14FrontendActionE+0x5f0)[0x153fb814]
/bin/clang++(_ZN5clang25ExecuteCompilerInvocationEPNS_16CompilerInstanceE+0x7b8)[0x15657598]
/bin/clang++(_Z8cc1_mainN4llvm8ArrayRefIPKcEES2_Pv+0x4a8)[0x11bd2e04]
/bin/clang++[0x11bc137c]
/bin/clang++(main+0x9b8)[0x11bc1fb8]
/lib64/libc.so.6(+0x24700)[0x3fff83b14700]
/lib64/libc.so.6(__libc_start_main+0xc4)[0x3fff83b148f4]
Stack dump:
0.      Program arguments: /bin/clang++ -cc1 -xc++ -std=c++1z -emit-llvm -
1.      <eof> parser at end of file
2.      Per-file LLVM IR generation
3.      <stdin>:4:3: Generating code for declaration 'A::A'


### COMPILER VERSION INFO (clang++ -v):
clang version 6.0.0 (trunk)
Target: powerpc64le-unknown-linux-gnu
Thread model: posix
InstalledDir: /bin
Found candidate GCC installation: /usr/lib/gcc/ppc64le-redhat-linux/4.8.2
Found candidate GCC installation: /usr/lib/gcc/ppc64le-redhat-linux/4.8.5
Selected GCC installation: /usr/lib/gcc/ppc64le-redhat-linux/4.8.5
Candidate multilib: .;@m64
Selected multilib: .;@m64


---


### compiler : `llvm`
### title : `InstCombine cannot blindly assume that inttoptr(ptrtoint x) -> x`
### open_at : `2017-09-11T10:08:39Z`
### last_modified_date : `2021-07-28T15:37:14Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=34548
### status : `NEW`
### tags : `miscompilation`
### component : `Scalar Optimizations`
### version : `trunk`
### severity : `normal`
### contents :
Example of an end-to-end miscompilation by clang of the following code involving ptrtoint:

$ cat c.c
#include <stdio.h>

void f(int*, int*);

int main()
{
  int a=0, y[1], x = 0;
  uintptr_t pi = (uintptr_t) &x;
  uintptr_t yi = (uintptr_t) (y+1);
  uintptr_t n = pi != yi;

  if (n) {
    a = 100;
    pi = yi;
  }

  if (n) {
    a = 100;
    pi = (uintptr_t) y;
  }

  *(int *)pi = 15;

  printf("a=%d x=%d\n", a, x);

  f(&x,y);

  return 0;
}


$ cat b.c
void f(int*x, int*y) {}


$ clang -O2 c.c b.c -o foo

$ ./foo
a=0 x=0

This result is wrong.  The two possible outcomes are: a=0 x=15, and a=100 x=0.

The bug is in Instcombine that treats inttoptr(ptrtoint(x)) == x, which is incorrect.  This transformation can only be done if x is dereferenceable for the accesses through inttoptr.
Compare the following:
clang -O0 -S -emit-llvm -o - c.c | opt -S -sroa
clang -O0 -S -emit-llvm -o - c.c | opt -S -sroa -instcombine

Integer compares are replaces with pointer compares (wrong) and load/stores are changed from inttoptr to pointers directly (also wrong).

Test case by Gil Hur.


---


### compiler : `llvm`
### title : `[miscompilation] set to 0 on __m128d ignored: garbage in high element on compare and movemask`
### open_at : `2017-09-11T11:09:09Z`
### last_modified_date : `2019-09-08T13:12:27Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=34549
### status : `NEW`
### tags : `miscompilation`
### component : `Backend: X86`
### version : `5.0`
### severity : `normal`
### contents :
reduced testcase:

#include <x86intrin.h>
#include <iostream>

std::ostream &operator<<(std::ostream &s, __m128d v)
{
    return s << '{' << v[0] << ", " << v[1] << '}';
}

int main()
{
    for (double lo_ : {1., 1.}) {
        for (double hi_ : {1., 1.}) {
            for (std::size_t pos = 0; pos < 2; ++pos) {
                __m128d lo = _mm_set1_pd(lo_);
                __m128d hi = _mm_set1_pd(hi_);
                if (0 != _mm_movemask_pd(hi < lo)) {
                    std::cerr << hi << ", lo: " << lo;
                    if (3 != _mm_movemask_pd(hi >= hi)) {
                        std::cerr << hi << ", lo: " << lo;
                    }
                }
            }
        }
    }

    __m128d x = _mm_set1_pd(1.);
    for (std::size_t i = 0; i < 2; ++i) {
        asm("ror $64,%%rax" ::"m"(x));
        x[i] = 0;  // #1
    }
    asm("ror $64,%%rax" :"+m"(x));
    if (3 != _mm_movemask_pd(x == _mm_setzero_pd())) {
        std::cerr << "!!!FAILED!!!\n";
        return 1;
    }
    return 0;
}

Compile with `clang++-5.0 -std=c++14 -O2 -msse2`. clang 4.0 does not fail.

The assignment at line #1 is skipped for i = 1. However, minimal changes to unrelated code lead to the use of a `movsd` from memory, thus zeroing the upper 64 bits, as requested.

The above code is a reduced testcase from a unit test in https://github.com/VcDevel/Vc.


---


### compiler : `llvm`
### title : `Strict-aliasing not noticing valid aliasing of two unions with active members`
### open_at : `2017-09-15T20:25:10Z`
### last_modified_date : `2021-06-21T05:30:37Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=34632
### status : `NEW`
### tags : `miscompilation`
### component : `C++`
### version : `trunk`
### severity : `normal`
### contents :
Consider the following C/C++ code with -O3 -fstrict-aliasing:

struct s1 {unsigned short x;};
struct s2 {unsigned short x;};
union s1s2 { struct s1 v1; struct s2 v2; };

static int read_s1x(struct s1 *p) { return p->x; }
static void write_s2x(struct s2 *p, int v) { p->x=v;}

int test(union s1s2 *p1, union s1s2 *p2, union s1s2 *p3)
{
  if (read_s1x(&p1->v1))
  {
    unsigned short temp;
    temp = p3->v1.x;
    p3->v2.x = temp;
    write_s2x(&p2->v2,1234);
    temp = p3->v2.x;
    p3->v1.x = temp;
  }
  return read_s1x(&p1->v1);
}
int test2(int x)
{
  union s1s2 q[2];
  q->v1.x = 4321;
  return test(q,q+x,q+x);
}
#include <stdio.h>
int main(void)
{
  printf("%d\n",test2(0));
}

Clang (and GCC) generate code that outputs 4321 instead of the expected 1234.

I don't really understand things in terms of the C standard, but in terms of the C++ standard, it seems as if Clang and GCC are incorrect, and this code is well-defined.  (The output is 4321 in both C and C++ mode.)

According to [class.union]/5 in the C++17 draft N4659, the assignment expression "p3->v2.x = temp;" changes the active member of the union.  It's done through a union member access expression.  Thus the pointer &p2->v2 is valid here.

Even if I switch this to "p3->v2 = { x };", avoiding the nested case, the problem still happens.

Even if I explicitly change the active member of the union with placement new as "new(&p3.v2) s2;", the problem still happens.

Is it possible that Clang doesn't see the possibility that p2 and p3 point to the same object?


---


### compiler : `llvm`
### title : `Clang miscompiles with -O0.`
### open_at : `2018-03-07T13:02:30Z`
### last_modified_date : `2020-06-21T11:12:38Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=36629
### status : `RESOLVED`
### tags : `miscompilation`
### component : `new bugs`
### version : `trunk`
### severity : `normal`
### contents :
Created attachment 20013
Reproducer.

Reduced reproducer (see full in attachment):
>$ cat repr.cpp
#include <stdio.h>
#include <vector>

struct struct_1 {
  signed char member_1_0 : 23;
  unsigned char : 16;
  unsigned char member_1_1 : 25;
};

const unsigned char aa = 60;
const unsigned char bb = 246;
signed char cc = 36;
signed char dd = 97;
unsigned char ee = 178;
struct_1 struct_obj_1;
short a = 42;

void tf_0_foo() {
  ee = a % (unsigned char)((bb && aa ? ~0 : 0) % struct_obj_1.member_1_0 ^ cc);
  dd = struct_obj_1.member_1_1;
}

int main() {
  struct_obj_1.member_1_0 = -122;
  struct_obj_1.member_1_1 = 98;
  tf_0_foo();
  printf("%d\n", (int)ee);
}

Error:
>$ clang++ -fsanitize=undefined -fno-sanitize-recover=undefined -Werror=uninitialized -Werror=implicitly-unsigned-literal -O0 -w repr.cpp ; ./a.out
42
>$  clang++ -w -O0 repr.cpp ; ./a.out
5

LLVM version:
>$ clang++ -v
clang version 7.0.0 (trunk 326547)
Target: x86_64-unknown-linux-gnu
Thread model: posix
InstalledDir: /llvm/bin-trunk/bin
Found candidate GCC installation: /usr/lib/gcc/i686-redhat-linux/4.8.2
Found candidate GCC installation: /usr/lib/gcc/i686-redhat-linux/4.8.5
Found candidate GCC installation: /usr/lib/gcc/x86_64-redhat-linux/4.8.2
Found candidate GCC installation: /usr/lib/gcc/x86_64-redhat-linux/4.8.5
Selected GCC installation: /usr/lib/gcc/x86_64-redhat-linux/4.8.5
Candidate multilib: .;@m64
Candidate multilib: 32;@m32
Selected multilib: .;@m64


---


### compiler : `llvm`
### title : `Mac OS X cmake scripts don’t test for necessary code-signing capacity before attempting to build`
### open_at : `2018-03-19T17:42:03Z`
### last_modified_date : `2019-05-21T07:09:33Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=36803
### status : `NEW`
### tags : `build-problem, miscompilation`
### component : `cmake`
### version : `trunk`
### severity : `enhancement`
### contents :
If you are building LLVM using `cmake` on a Macintosh and you wish to include any of the components that require code-signed binaries, you will need to have already gone through the (perhaps infamous) manual process of creating a self-signed code-signing certificate in your System Keychain:

    https://llvm.org/svn/llvm-project/lldb/trunk/docs/code-signing.txt

… if you haven’t already performed everything listed therein, or if this procedure is somehow alien or off-putting to you, you may be stranded somewhat: your `cmake` configure step will have successfully executed, but your build phase will have choked out with a fatal error – likely with one whose orthogonal nature to the problem will fail to lead to a solution.

A `cmake` function that tests for proper code-signing capacity (by building a hello-world-ish program, and subsequently invoking `/usr/bin/codesign` on the programs’ output binary) would surely be a valuable addition to this project, no?

I, myself, had generated the certificate some time ago, and was happily building LLVM with all available options – until today, when I was met with the same sort of cryptically un-Googleable build-time errors. I eventually realized that my certificate had past its “use-by” date, of two years’ past the generation date, and had finally expired.


---


### compiler : `llvm`
### title : `A miscompilation bug with unsigned char`
### open_at : `2018-05-15T13:53:36Z`
### last_modified_date : `2021-06-11T13:50:51Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=37469
### status : `NEW`
### tags : `miscompilation`
### component : `Transformation Utilities`
### version : `trunk`
### severity : `normal`
### contents :
Created attachment 20304
A source file that raises the bug.

```
$ cat test-main.c
#include <string.h>
#include <stdio.h>
#include <stdint.h>

// If f(A, B + 4) is given, and integer representation of A and B + 4
// are the same, c1 == c2 in the loop becomes true,
// so arr3 = arr1. Hence r = A, and *A should be 10.
// However, if compiled with -O3, *A is still 1.
void store_10_to_p(int *p, int *q) {
  unsigned char arr1[8];
  unsigned char arr2[8];
  unsigned char arr3[8];
  // Type punning with char* is allowed.
  memcpy((unsigned char*)arr1, (unsigned char *)&p, sizeof(p));
  memcpy((unsigned char*)arr2, (unsigned char *)&q, sizeof(q));
  // Now arr1 is p, arr2 is q.

  for (int i = 0; i < sizeof(q); i++) {
    int c1 = (int)arr1[i], c2 = (int)arr2[i];
    // Note that c1 == c2 is a comparison between _integers_ (not pointers).
    if (c1 == c2)
      // Always true if p and q have same integer representation.
      arr3[i] = arr1[i];
    else
      arr3[i] = arr2[i];
  }
  // Now arr3 is equivalent to arr1, which is p.
  int *r;
  memcpy(&r, (unsigned char *)arr3, sizeof(r));
  // Now r is p.
  *p = 1;
  *r = 10;
}

int main() {
  int A[4], B[4];
  printf("%p %p\n", A, &B[4]);
  if ((uintptr_t)A == (uintptr_t)&B[4]) {
    store_10_to_p(A, &B[4]);
    printf("%d\n", A[0]);
  }
  return 0;
}

$ clang -O3 -o test-main test-main.c
$ ./test-main
0x7fffffffe580 0x7fffffffe580
1
$ clang -O0 -o test-main test-main.c
$ ./test-main
0x7fffffffe580 0x7fffffffe580
10
```

This is what is happening inside LLVM:
(1) Instcombine changes the loop body to "arr3[i] = arr2[i];"
(2) Loop idiom recognizer replaces the loop with a "memcpy(arr3, arr2, 8)"
(3) Instcombine does the store forwarding from the memcpy to the load


I think this is related with lowering 'unsigned char' in C into 'i8' in LLVM.

There are two choices:
(1) Lowering 'unsigned char' into 'i8' is correct.
(2) Lowering 'unsigned char' into 'i8' is incorrect.

If (1) is right, then one of the optimizations happening in this example should be disabled, to stop the miscompilation.
If (2) is right, then it is clang which miscompiles this example. 'unsigned char' should be lowered into something else.


---


### compiler : `llvm`
### title : `opt miscompiles with "opt -O3 -flattencfg"`
### open_at : `2018-06-02T15:54:20Z`
### last_modified_date : `2020-05-21T11:22:18Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=37662
### status : `RESOLVED`
### tags : `miscompilation`
### component : `-New Bugs`
### version : `trunk`
### severity : `enhancement`
### contents :
Created attachment 20384
Reproducer.

Opt produces incorrect code with opt -O3 -o func.ll func.bc -flattencfg
opt-bisect-limit points to Simplify the CFG on function

Reproducer:
>$ cat func.cpp
extern unsigned short a, c;
extern short *d;
extern unsigned short *e;
extern short b;
void foo() {
  e = &a;
  c = 0;
  if (*d)
    e = &c;
  if (b)
    e = &c;
}

>$ cat driver.cpp
#include <stdio.h>

short a = 6, b = 6;
unsigned short c;
unsigned short *d = &c;
short *e;

void foo();

int main() {
  foo();
  printf("%hd\n", *(e));
}

Error:
>$ clang++ driver.cpp func.cpp
>$ ./a.out
0
>$ clang++ -O3 -Xclang -disable-llvm-optzns -emit-llvm -c -o func.bc func.cpp
>$ opt -O3 -o func.ll func.bc -flattencfg
>$ clang++ -c -o func.o func.ll
>$ clang++ driver.cpp func.o
>$ ./a.out
6

LLVM version:
>$ clang++ -v
clang version 7.0.0 (trunk 333377)
Target: x86_64-unknown-linux-gnu
Thread model: posix
InstalledDir: /llvm/bin-trunk/bin
Found candidate GCC installation: /usr/lib/gcc/x86_64-redhat-linux/4.4.7
Found candidate GCC installation: /usr/lib/gcc/x86_64-redhat-linux/4.8.2
Found candidate GCC installation: /usr/lib/gcc/x86_64-redhat-linux/4.8.5
Selected GCC installation: /usr/lib/gcc/x86_64-redhat-linux/4.8.5
Candidate multilib: .;@m64
Candidate multilib: 32;@m32
Selected multilib: .;@m64


---


### compiler : `llvm`
### title : `opt miscompiles with "opt -O3 -newgvn -structurizecfg"`
### open_at : `2018-06-02T20:31:08Z`
### last_modified_date : `2020-04-29T20:31:29Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=37664
### status : `RESOLVED`
### tags : `miscompilation`
### component : `-New Bugs`
### version : `trunk`
### severity : `enhancement`
### contents :
Created attachment 20385
Reproducer.

Opt produces incorrect code with -O3 -newgvn -structurizecfg
opt-bisect-limit points to Machine Common Subexpression Elimination on function
Testcase looks weird, but I can't reduce it further.

Reproducer:
>$ cat func.cpp
#include "init.h"
void tf_3_foo() {
  bool a(var_3);
  var_2 = (tf_3_var_38 && struct_obj.member_1_3) ||
                  (a && arr_3[0]) || !a || !ptr;
}
>$ cat driver.cpp
#include "init.h"
#include <vector>
void a(long) {}
std::vector<int> b;
struct_1 struct_2::member_2;
bool var_1, var_2;
const bool tf_3_var_38 = false;
unsigned short var_3 = 3;
tf_3_struct_1 struct_obj;
std::array<unsigned short, 10> arr_2;
std::valarray<bool> arr_3{false};
unsigned short *ptr = &arr_2[0];
void tf_3_foo();
int main() {
  a(1038);
  a(var_1);
  a(struct_2::member_2.member_1);
  b[2];
  b[3];
  tf_3_foo();
  printf("%d\n", (int)var_2);
}
>$ cat init.h
#include <valarray>
struct struct_1 {
  int member_1 : 13;
};
struct struct_2 {
  static struct_1 member_2;
};
extern const bool tf_3_var_38;
extern unsigned short var_3;
struct tf_3_struct_1 {
  bool member_1_3 : 3;
} extern struct_obj;
extern std::valarray<bool> arr_3;
extern bool var_2;
extern unsigned short *ptr;

Error:
>$ clang++ driver.cpp func.cpp
>$ ./a.out
0
>$ clang++ -O3 -Xclang -disable-llvm-optzns -emit-llvm -c -o func.bc func.cpp
>$ opt -O3 -o func.ll func.bc -newgvn -structurizecfg
>$ clang++ -O3 -c -o func.o func.ll
>$ clang++ driver.cpp func.o
>$ ./a.out
1

LLVM version:
clang version 7.0.0 (trunk 333377)
Target: x86_64-unknown-linux-gnu
Thread model: posix
InstalledDir: /llvm/bin-trunk/bin
Found candidate GCC installation: /usr/lib/gcc/x86_64-redhat-linux/4.4.7
Found candidate GCC installation: /usr/lib/gcc/x86_64-redhat-linux/4.8.2
Found candidate GCC installation: /usr/lib/gcc/x86_64-redhat-linux/4.8.5
Selected GCC installation: /usr/lib/gcc/x86_64-redhat-linux/4.8.5
Candidate multilib: .;@m64
Candidate multilib: 32;@m32
Selected multilib: .;@m64


---


### compiler : `llvm`
### title : `Intermittent bug in opt with -O3 -newgvn`
### open_at : `2018-06-04T11:29:37Z`
### last_modified_date : `2019-07-22T19:22:54Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=37676
### status : `RESOLVED`
### tags : `miscompilation`
### component : `-New Bugs`
### version : `trunk`
### severity : `enhancement`
### contents :
Created attachment 20388
Reproducer.

Intermittent bug in opt with -O3 -newgvn. 
It gives 2 variants of assembler for different compilations.
opt-bisect-limit points to "Global Value Numbering on function"
Reproducer:
>$ cat func.c
extern unsigned long long b, e, g;
extern const signed char a;
extern const unsigned c;
extern unsigned d, h;
extern signed char f, i;
extern unsigned *j;
extern unsigned long long *k;
extern signed char *l;
void foo() {
  if (*k <= (8 & -b * ((1 - 8ULL) * c) ?: ~i))
    f = 8 & -(b * ((1 - 8ULL) * c)) ?: i * d;
  e = g ? -(8 & -b * ((1 - 8ULL) * c) ?: i * d) : 0;
  if (!a) {
    *l = ~0 ? 8 & -(b * ((1 - 8ULL) * c)) ?: i * d : 2022409665839104;
    h = 8 & -(b * ((1ULL - 8) * c)) ? b * ((1 - 8ULL) * c) : 0;
  }
  if (8 & -(b * ((1ULL - 8) * c)) ? 0 : ~0)
    *j = b * ((1 - 8ULL) * c);
}
>$ cat driver.c
#include <stdio.h>
unsigned long long b, e, g;
const signed char a = 8;
const unsigned c = 92620;
unsigned d, h, m;
signed char f, i;
unsigned *j = &m;
unsigned long long *k = &e;
signed char *l;
void foo();
int main() {
  *j = 42;
  foo();
  printf("%u\n", *j);
}

Error:
>$ clang driver.c func.c
>$ ./a.out
0
>$ clang -O3 -Xclang -disable-llvm-optzns -emit-llvm -c -o func.bc func.c
>$ opt -O3 -o func.ll func.bc -newgvn
>$ clang -O3 -c -o func.o func.ll
>$ clang -O3 driver.c func.o
>$ ./a.out
42

LLVM version:
clang version 7.0.0 (trunk 333836)
Target: x86_64-unknown-linux-gnu
Thread model: posix
InstalledDir: /users/vlivinsk/llvm/bin-trunk/bin
Found candidate GCC installation: /usr/lib/gcc/x86_64-redhat-linux/4.4.7
Found candidate GCC installation: /usr/lib/gcc/x86_64-redhat-linux/4.8.2
Found candidate GCC installation: /usr/lib/gcc/x86_64-redhat-linux/4.8.5
Selected GCC installation: /usr/lib/gcc/x86_64-redhat-linux/4.8.5
Candidate multilib: .;@m64
Candidate multilib: 32;@m32
Selected multilib: .;@m64


---


### compiler : `llvm`
### title : `LLVM miscompiles long double to unsigned long long conversion`
### open_at : `2018-07-24T17:54:18Z`
### last_modified_date : `2019-04-03T10:34:58Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=38289
### status : `RESOLVED`
### tags : `miscompilation`
### component : `Backend: X86`
### version : `trunk`
### severity : `normal`
### contents :
$ cat fp.c
long double l = 10240000000000000256.000000L;

int main() {
  __builtin_printf("%llu\n", (unsigned long long)l);
}

$ clang -O0 fp.c && ./a.out
10240000000000000256
$ clang -O1 fp.c && ./a.out
10239999935508381696

This only happens when no ssse3 is available. This started failing with r329339,
but the bug is probably older. What happens is that instructions get scheduled
over a x87 control word store.


---


### compiler : `llvm`
### title : `Incorrect fold of 'x & (-1 >> y) s>= x'`
### open_at : `2018-12-02T22:47:39Z`
### last_modified_date : `2019-06-09T05:07:30Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=39861
### status : `RESOLVED`
### tags : `miscompilation`
### component : `Scalar Optimizations`
### version : `trunk`
### severity : `normal`
### contents :
This is a bug in test/Transforms/InstCombine/canonicalize-constant-low-bit-mask-and-icmp-sge-to-icmp-sle.ll

Output of Alive2:
declare i1 @pv(i8 %x, i8 %y) {
  %tmp0 = lshr i8 255, %y
  %tmp1 = and i8 %tmp0, %x
  %ret = icmp sge i8 %tmp1, %x
  ret i1 %ret
}
=>
declare i1 @pv(i8 %x, i8 %y) {
  %tmp0 = lshr i8 255, %y
  %1 = icmp sge i8 %tmp0, %x
  ret i1 %1
}
Transformation doesn't verify!
ERROR: Value mismatch

Example:
i8 %x = 0x7e (126)
i8 %y = 0x0 (0)

Source:
i8 %tmp0 = 0xff (255, -1)
i8 %tmp1 = 0x7e (126)
i1 %ret = 0x1 (1, -1)

Target:
i8 %tmp0 = 0xff (255, -1)
i1 %1 = 0x0 (0)
Source value: 0x1 (1, -1)
Target value: 0x0 (0)


---


### compiler : `llvm`
### title : `Constant folding incorrectly folds modifiable compound literal`
### open_at : `2018-12-12T16:54:11Z`
### last_modified_date : `2018-12-14T22:16:30Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=39977
### status : `NEW`
### tags : `miscompilation`
### component : `C++`
### version : `trunk`
### severity : `normal`
### contents :
In the following, Clang appears to ignore the modification of the array element; this, in turn, leads to a call to `abort()`. The GCC-built executable returns 0 as expected.


### SOURCE (<stdin>):
extern "C" void abort(void);
constexpr int *p0 = (int []){ 13 };
int main(void) {
  *p0 = 42;
  int x[*p0];
  if ((sizeof x)/sizeof(int) == 42) return 0;
  abort();
}


### COMPILER INVOCATION:
clang++ -xc++ -std=gnu++11 -o testit -


### INVOCATION OF RESULTING EXECUTABLE:
./testit


### ACTUAL EXECUTION OUTPUT:
Aborted
Return:  0x86:134


### EXPECTED EXECUTION OUTPUT:
Return:  0x00:0


### COMPILER VERSION INFO (clang++ -v):
clang version 8.0.0 (trunk)
Target: powerpc64le-unknown-linux-gnu
Thread model: posix
InstalledDir: /gsa/tlbgsa/projects/x/xlcmpbld/run/clang/main_trunk/linux_leppc/daily/latest/bin
Found candidate GCC installation: /usr/lib/gcc/ppc64le-redhat-linux/4.8.2
Found candidate GCC installation: /usr/lib/gcc/ppc64le-redhat-linux/4.8.5
Selected GCC installation: /usr/lib/gcc/ppc64le-redhat-linux/4.8.5
Candidate multilib: .;@m64
Selected multilib: .;@m64


---


### compiler : `llvm`
### title : `[PowerPC64] [ELFv2] wrong .init section for large binaries (long branch thunk)`
### open_at : `2019-02-15T15:23:38Z`
### last_modified_date : `2019-05-10T06:06:09Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=40740
### status : `RESOLVED`
### tags : `miscompilation`
### component : `ELF`
### version : `unspecified`
### severity : `normal`
### contents :
A large powerpc64 ELFv2 executable linked with lld (i.e. clang) may have an incorrect .init section and it will crash with SIGTRAP.

In the example bellow, where I'd expect "bl  nnnnn <frame_dummy+0x8>", there's a "trap" instruction instead, followed by function "<__long_branch_frame_dummy>":


[root@alfredo-1 /home/alfredo.junior/tmp]# /usr/local/bin/objdump clang -d -j .init
 
clang:     file format elf64-powerpc-freebsd
 
 
Disassembly of section .init:
 
0000000013ca9f10 <_init>:
    13ca9f10:   3c 4c 00 1d     addis   r2,r12,29
    13ca9f14:   38 42 76 38     addi    r2,r2,30264
    13ca9f18:   f8 21 ff d1     stdu    r1,-48(r1)
    13ca9f1c:   7c 08 02 a6     mflr    r0
    13ca9f20:   f8 01 00 40     std     r0,64(r1)
    13ca9f24:   7f e0 00 08     trap
 
0000000013ca9f28 <__long_branch_frame_dummy>:
    13ca9f28:   3d 82 ff e4     addis   r12,r2,-28
    13ca9f2c:   e9 8c bf 00     ld      r12,-16640(r12)
    13ca9f30:   7d 89 03 a6     mtctr   r12
    13ca9f34:   4e 80 04 20     bctr
    13ca9f38:   4b ff ff f1     bl      13ca9f28 <__long_branch_frame_dummy>
    13ca9f3c:   60 00 00 00     nop
    13ca9f40:   4b ff ff 59     bl      13ca9e98 <__do_global_ctors_aux+0x8>
    13ca9f44:   60 00 00 00     nop
    13ca9f48:   e8 21 00 00     ld      r1,0(r1)
    13ca9f4c:   e8 01 00 10     ld      r0,16(r1)
    13ca9f50:   7c 08 03 a6     mtlr    r0
    13ca9f54:   4e 80 00 20     blr



Looks like long-branch-thunk code need to handle .init section as an special case when the second part of init lands in a higher address.


---


### compiler : `llvm`
### title : `[coverage] linker failure with dead code stripping`
### open_at : `2019-02-27T14:14:11Z`
### last_modified_date : `2019-03-01T09:02:49Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=40884
### status : `NEW`
### tags : `compile-fail, miscompilation`
### component : `Tooling`
### version : `trunk`
### severity : `normal`
### contents :
This is related to Bug 37561. The bug is fixed now, but I get linker errors (lld-link) when building teh project with optimizer (for release).

lld-link reports about an error with relocation against "symbol" in discarded section. This was triggered by a global function calling sprintf(), which was not referenced. After I removed the function or replaced sprintf() with snprintf(), linker did not complain, but the unit test was failing.

When building for Debug, the linker also did not complain, the unit test was passing and I was able to create the coverage report.

Looks to me like dead code stripping is leading to dangling references and also the Optimizer may cause code corruptions.

I hope Marius can reproduce the issue with his project, as I can hardly share mine and it comes with a lot of references in our repository.

SSB


---


### compiler : `llvm`
### title : `ELF st_other field is not being set on versioned symbol`
### open_at : `2019-03-12T19:27:06Z`
### last_modified_date : `2019-05-21T15:56:00Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=41048
### status : `RESOLVED`
### tags : `miscompilation`
### component : `libclang`
### version : `trunk`
### severity : `enhancement`
### contents :
Using clang on PowerPC64 ELFv2 ABI for FreeBSD I found that the versioned symbols containing a localEntryPoint are missing st_other flags (see missing 0x60 flag in front of symbol openattt@FBSD_1.1 bellow):

root@FreeBSD-ELFv2:~/tmp/symerror # objdump -t test.o

test.o:     file format elf64-powerpc-freebsd

SYMBOL TABLE:
0000000000000000 l    df *ABS*	0000000000000000 test.c
0000000000000000 l    d  .toc	0000000000000000 .toc
0000000000000000         *UND*	0000000000000000 .TOC.
0000000000000000  w    F .text	000000000000002c 0x60 __impl_openattt
0000000000000000 g     O .bss	0000000000000004 a
0000000000000000 g     F .text	000000000000002c 0x60 openattt
0000000000000000  w    F .text	000000000000002c openattt@FBSD_1.1


---


### compiler : `llvm`
### title : `Wrong alignment of pointer argument when typedef enforced`
### open_at : `2019-06-06T11:50:06Z`
### last_modified_date : `2020-02-11T15:43:36Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=42154
### status : `REOPENED`
### tags : `miscompilation`
### component : `-New Bugs`
### version : `trunk`
### severity : `normal`
### contents :
Given the input cpp code:
===
#include <arm_neon.h>

struct S4 {
  long long M2;
  S4(signed int &&P5) {}
};

typedef struct S5 {
  float32x2_t M0;
  float16x4_t M1;
  int M5;
  S5(float32x2_t &&P0, float16x4_t &&P1) : M0(P0), M1(P1) {}
} S5 __attribute((aligned(4))); //<<== In a typedef, it reduces the alignment.

struct S2 :  public S4, public S5 {
public:
  S2(S4 &&P1, S5 &&P2) : S4(P1), S5(P2) {}
};

int main() {
  S2 a(S4(2049077767), S5(vdup_n_f32(0), vdup_n_f16(0)));
  return 0;
}
===
The typedef enforces S5 to be 4 bytes aligned.
S5 constructor should write to M0 and M1 using a 4 byte alignment, but clang emits 8 bytes alignment for these writes.
===
compiling with the command:

clang --target=arm-arm-none-eabi -mcpu=cortex-a15 -S -o - -emit-llvm -O1 test.cpp

In the IR, the important bits are:
==
Allocating the S5 structure:

` %ref.tmp2 = alloca %struct.S5, align 4`
==
In the S5 constructor, function simd64_float32_tO18__simd64_float16_t:

Writing to the first element:
`
 %M0 = getelementptr inbounds %struct.S5, %struct.S5* %this, i32 0, i32 0
 store <2 x float> %0, <2 x float>* %M0, align 8   <<==== WRONG align!
`

Writing to the second element:
`
   %M1 = getelementptr inbounds %struct.S5, %struct.S5* %this, i32 0, i32 1
   store <4 x half> %1, <4 x half>* %M1, align 8 <<==== WRONG align!
`
--


This causes llc to generate the instruction:
`vst1.32 {d16}, [r1:64]!`
instead of
`vst1.32 {d16}, [r1]!`
Which enforces a 64 bit alignment, but the r1 pointer is 32 bit aligned.

Changing these aligns to 4 gives the correct result. So clang should be able to detect that alignment = min (8, 4) here.


---


### compiler : `llvm`
### title : `Passing long double args on 32-bit SPARC violates ABI`
### open_at : `2019-07-03T08:28:12Z`
### last_modified_date : `2020-10-09T14:07:38Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=42493
### status : `NEW`
### tags : `ABI, miscompilation`
### component : `Backend: Sparc`
### version : `trunk`
### severity : `normal`
### contents :
I'm current working to fix the remaining compiler-rt testsuite bugs on SPARC
(https://reviews.llvm.org/D40900).  One of the failures is

    Builtins-sparc-sunos :: divtc3_test.c
    Builtins-sparcv9-sunos :: divtc3_test.c

While the sparcv9 failure is different, the sparc one boils down to incorrectly
passing long double arguments.  Consider the following testcase:

$ cat caller.c
extern void callee (long double);

int
main (void)
{
  long double ld = 1.0;

  callee (ld);
  return 0;
}
$ cat callee.c
extern void abort (void);

void
callee (long double ld)
{
  if (ld != 1.0)
    abort ();
}
$ clang -m32 -c caller.c -o caller.clang.o
$ clang -m32 -c callee.c -o callee.clang.o
$ gcc -m32 -c caller.c -o caller.gcc.o
$ gcc -m32 -c callee.c -o callee.gcc.o
$ gcc -m32 -o clang-gcc caller.clang.o callee.gcc.o 
$ ./clang-gcc 
Segmentation Fault (core dumped)
$ gcc -m32 -o gcc-clang caller.gcc.o callee.clang.o 
$ ./gcc-clang 
Abort (core dumped)

The SPARC psABI, p.3-15 (Structure, Union, and Quad-Precision Arguments)
requires long double args to be passed by reference, while clang passes
them by value (as is correct for SPARCv9).


---


### compiler : `llvm`
### title : `NaN compares equal for SPARC V9`
### open_at : `2019-07-03T14:01:12Z`
### last_modified_date : `2019-07-03T14:01:12Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=42496
### status : `NEW`
### tags : `miscompilation`
### component : `Backend: Sparc`
### version : `trunk`
### severity : `enhancement`
### contents :
When investigating the last test failures on SPARC (for https://reviews.llvm.org/D40900),
I found two failures that boil down to long double NaN comparing equal to itself
on 64-bit SPARC:

    Builtins-sparcv9-sunos :: compiler_rt_logbl_test.c
    Builtins-sparcv9-sunos :: divtc3_test.c

They seem to boil down to the following testcase:

$ cat nancmp.c
#include <math.h>
#include <stdio.h>

int
main (void)
{
  long double lnan = NAN;
  long double mlnan = -NAN;

  if (lnan != lnan)
    printf ("nan neq\n");
  else
    printf ("nan eq\n");

  if (mlnan != mlnan)
    printf ("-nan neq\n");
  else
    printf ("-nan eq\n");

  return 0;
}
$ gcc -m32 -o nancmp nancmp.c && ./nancmp
nan neq
-nan neq
gcc -m64 -o nancmp nancmp.c && ./nancmp
nan neq
-nan neq
$ clang -m32 -o nancmp nancmp.c && ./nancmp
nan neq
-nan neq
$ clang -m64 -o nancmp nancmp.c && ./nancmp
nan eq
-nan eq

This may be due to the fact that clang calls _Qp_cmp for the comparison, which
returns unordered (3) in this case, while gcc uses _Qp_feq, which just returns
unequal (0) instead.


---


### compiler : `llvm`
### title : `Clang generates overaligned load of thrown object`
### open_at : `2019-07-18T13:15:57Z`
### last_modified_date : `2020-02-11T15:37:08Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=42668
### status : `RESOLVED`
### tags : `ABI, miscompilation`
### component : `C++`
### version : `trunk`
### severity : `normal`
### contents :
For the C++ code:
===
#include <arm_neon.h>

int main(void) {
  try {
    throw vld1q_u64(((const uint64_t[2]){1, 2}));
  } catch (uint64x2_t exc) {
    return 0;
  }
  return 1;
}

====
and command:
clang --target=arm-arm-none-eabi -march=armv8-a -c test_upstream.cpp -o - -Os -o - -S -emit-llvm
====
we obtain this:
entry:
  %exception = tail call i8* @__cxa_allocate_exception(i32 16) #2
  %0 = bitcast i8* %exception to <2 x i64>*
  store <2 x i64> <i64 1, i64 2>, <2 x i64>* %0, align 16, !tbaa !5
========
Which, passing to llc will generate:
   vld1.64 {d16, d17}, [r1]
   vst1.64 {d16, d17}, [r0:128]  << Not 128, but 64!!!
========

The store assumes an alignment of 16. However, %exception has alignment 64 as defined in
https://github.com/llvm-mirror/libunwind/blob/master/include/unwind.h
where we have:
struct _Unwind_Exception {
 ...
} __attribute__((__aligned__)); //<< For the ARM ABI the largest alignment is 8 (64 bits).

I do believe that the missing "align 8" in %exception should be the root of the error, as that should be passed further to %0 and, finally, to the store.

I also believe that clang should not assume data-width alignment when the pointer is a bitcast from a smaller data-type.


---


### compiler : `llvm`
### title : `ICE: "Cannot select: X86ISD::SUBV_BROADCAST" with -O3 -march=skx`
### open_at : `2019-07-30T00:53:50Z`
### last_modified_date : `2019-08-06T08:08:36Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=42819
### status : `RESOLVED`
### tags : `miscompilation`
### component : `Backend: X86`
### version : `trunk`
### severity : `enhancement`
### contents :
Clang fails with ICE.

Reproducer:
extern int a[], b[];
void c() {
  for (int d = 32; d <= 57; d++)
    b[d] = a[d] + a[d - 3];
}

Error:
>$ clang -c -O3 -march=skx small.c
fatal error: error in backend: Cannot select: t116: v2i64 = X86ISD::SUBV_BROADCAST t113
  t113: v4i64 = bitcast t9
    t9: v8i32,ch = load<(load 32 from `<8 x i32>* bitcast (i32* getelementptr inbounds ([0 x i32], [0 x i32]* @a, i64 0, i64 45) to <8 x i32>*)`, align 4, !tbaa !2)> t0, t156, undef:i64
      t156: i64 = X86ISD::Wrapper TargetGlobalAddress:i64<[0 x i32]* @a> + 180
        t155: i64 = TargetGlobalAddress<[0 x i32]* @a> + 180
      t5: i64 = undef
In function: c
clang-10: error: clang frontend command failed with exit code 70 (use -v to see invocation)
clang version 10.0.0 (trunk 367162)
Target: x86_64-unknown-linux-gnu
Thread model: posix

LLVM version:
clang version 10.0.0 (trunk 367162)


---


### compiler : `llvm`
### title : `Incorrect result with -O3 -march=skx`
### open_at : `2019-07-30T20:23:50Z`
### last_modified_date : `2019-08-20T10:10:22Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=42833
### status : `RESOLVED`
### tags : `miscompilation`
### component : `Backend: X86`
### version : `trunk`
### severity : `enhancement`
### contents :
Clang produces incorrect result with -O3 -march=skx

Reproducer:
#include <stdio.h>

int b;
unsigned c[49];
int d[49];

void i() {
  for (int g = 32; g <= 48; g++) {
    d[g] -= c[g] + b;
    c[g] += c[g] + b;
    b -= b;
  }
}

int main() {
  for (int g = 0; g < 49; ++g)
    c[g] = 3;
  i();
  printf("%d\n", d[36]);
}

Error:
>$ clang -O3 -march=skx small.c ; ./a.out
0
>$ clang -O0 -march=skx small.c ; ./a.out
-3

LLVM version:
clang version 10.0.0 (trunk 367162)
Target: x86_64-unknown-linux-gnu
Thread model: posix


---


### compiler : `llvm`
### title : `Incorrect fold of uadd.with.overflow with undef`
### open_at : `2019-09-01T11:09:33Z`
### last_modified_date : `2021-01-03T18:01:31Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=43188
### status : `RESOLVED`
### tags : `miscompilation`
### component : `Scalar Optimizations`
### version : `trunk`
### severity : `normal`
### contents :
Alive2 complains about a transformation in Transforms/ConstProp/overflow-ops.ll:

define {i8, i1} @uadd_undef() {
%0:
  %t = uadd_overflow i8 142, undef
  ret {i8, i1} %t
}
=>
define {i8, i1} @uadd_undef() {
%0:
  ret {i8, i1} undef
}
Transformation doesn't verify!
ERROR: Value mismatch

Example:

Source:
{i8, i1} %t = { #x8e (142, -114), #x0 (0) }     [based on undef value]

Target:
Source value: { #x8e (142, -114), #x0 (0) }     [based on undef value]
Target value: { #x00 (0), #x0 (0) }


In summary, there's no value in the source that the undef can take that allows uadd to return {0, 0}. To return 0, it has to overflow (unsigned), and hence the 2nd value would be 1.
Two valid return values I can think off: {%a, 0}; {undef, 1}.


---


### compiler : `llvm`
### title : `Incorrect fold of ashr+xor -> lshr w/ vectors`
### open_at : `2019-10-13T21:51:08Z`
### last_modified_date : `2020-03-26T18:13:04Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=43665
### status : `RESOLVED`
### tags : `miscompilation`
### component : `Scalar Optimizations`
### version : `trunk`
### severity : `normal`
### contents :
The following test in Transforms/InstCombine/vector-xor.ll shows an incorrect transformation. I reproduce it here with a smaller vector size & bitwidth to make it easier to understand.
The issue is that "undef >> 4" is "ssss.sxyz" (s = sign bit), while "undef u>> 4" is "0000.xyzw", so it can produce the value "0000.1000", while ashr cannot. See details below:


define <2 x i8> @test_v4i32_not_ashr_negative_const_undef(<2 x i8> %a0) {
  %1 = ashr <2 x i8> { 251, undef }, %a0
  %2 = xor <2 x i8> { 255, 255 }, %1
  ret <2 x i8> %2
}
=>
define <2 x i8> @test_v4i32_not_ashr_negative_const_undef(<2 x i8> %a0) {
  %1 = lshr <2 x i8> { 4, undef }, %a0
  ret <2 x i8> %1
}
Transformation doesn't verify!
ERROR: Value mismatch

Example:
<2 x i8> %a0 = < #x00 (0), #x04 (4) >

Source:
<2 x i8> %1 = < #xfb (251, -5), #x00 (0)        [based on undef value] >
<2 x i8> %2 = < #x04 (4), #xff (255, -1) >

Target:
<2 x i8> %1 = < #x04 (4), #x08 (8) >
Source value: < #x04 (4), #xff (255, -1) >
Target value: < #x04 (4), #x08 (8) >


---


### compiler : `llvm`
### title : `Incorrect 'icmp sle' -> 'icmp slt' w/ vectors`
### open_at : `2019-10-20T11:30:02Z`
### last_modified_date : `2019-10-29T15:14:08Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=43730
### status : `RESOLVED`
### tags : `miscompilation`
### component : `Scalar Optimizations`
### version : `trunk`
### severity : `normal`
### contents :
This transformation exposed in Transforms/InstCombine/icmp-vec.ll is incorrect. The issue is that "INT_MIN <= undef" is not the same as "INT_MIN < undef".

define <2 x i1> @PR27756_2(<2 x i8> %a) {
  %cmp = icmp sle <2 x i8> %a, { undef, 0 }
  ret <2 x i1> %cmp
}
=>
define <2 x i1> @PR27756_2(<2 x i8> %a) {
  %cmp = icmp slt <2 x i8> %a, { undef, 1 }
  ret <2 x i1> %cmp
}
Transformation doesn't verify!
ERROR: Value mismatch

Example:
<2 x i8> %a = < #x80 (128, -128), #x80 (128, -128) >

Source:
<2 x i1> %cmp = < #x1 (1), #x1 (1) >

Target:
<2 x i1> %cmp = < #x0 (0), #x1 (1) >
Source value: < #x1 (1), #x1 (1) >
Target value: < #x0 (0), #x1 (1) >


---


### compiler : `llvm`
### title : `Incorrect instcombine 'and + icmp eq' -> 'icmp ult' fold`
### open_at : `2019-10-20T11:36:56Z`
### last_modified_date : `2019-10-29T15:14:08Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=43731
### status : `RESOLVED`
### tags : `miscompilation`
### component : `Scalar Optimizations`
### version : `trunk`
### severity : `normal`
### contents :
The 2nd element of the result of this test case is incorrect (InstCombine/canonicalize-constant-low-bit-mask-and-icmp-eq-to-icmp-ule.ll):

define <3 x i1> @p3_vec_splat_undef(<3 x i8> %x) {
  %tmp0 = and <3 x i8> %x, { 3, undef, 3 }
  %ret = icmp eq <3 x i8> %tmp0, %x
  ret <3 x i1> %ret
}
=>
define <3 x i1> @p3_vec_splat_undef(<3 x i8> %x) {
  %1 = icmp ult <3 x i8> %x, { 4, undef, 4 }
  ret <3 x i1> %1
}
Transformation doesn't verify!
ERROR: Value mismatch

Example:
<3 x i8> %x = < #x00 (0), #x00 (0), #x00 (0) >

Source:
<3 x i8> %tmp0 = < #x00 (0), #x00 (0), #x00 (0) >
<3 x i1> %ret = < #x1 (1), #x1 (1), #x1 (1) >

Target:
<3 x i1> %1 = < #x1 (1), #x0 (0), #x1 (1) >
Source value: < #x1 (1), #x1 (1), #x1 (1) >
Target value: < #x1 (1), #x0 (0), #x1 (1) >


---


### compiler : `llvm`
### title : `[X86] Invalid code generated for shufflevector + extractelement`
### open_at : `2019-11-11T20:04:49Z`
### last_modified_date : `2019-11-11T22:07:21Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=43968
### status : `RESOLVED`
### tags : `miscompilation`
### component : `Backend: X86`
### version : `trunk`
### severity : `normal`
### contents :
define float @foo(i32 %a, float %in) {
  %1 = insertelement <4 x float> undef, float %in, i32 0
  %t6.i = shufflevector <4 x float> %1, <4 x float> undef, <4 x i32> <i32 undef, i32 0, i32 0, i32 0>
  %val = extractelement <4 x float> %t6.i, i32 1
  ret float %val
}


llc gives:
foo:                                    # @foo
        ret


It should return %in.

https://godbolt.org/z/Ej_CKQ


---


### compiler : `llvm`
### title : `Alignment specifier not applied to anonymous structure or union`
### open_at : `2019-11-12T21:20:45Z`
### last_modified_date : `2019-12-21T02:18:19Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=43983
### status : `RESOLVED`
### tags : `miscompilation`
### component : `C`
### version : `9.0`
### severity : `normal`
### contents :
Created attachment 22802
minimal example

The _Alignas specifier is not being applied to anonymous structures or unions. If the structure or union is given a declarator then the alignment specifier is correctly applied. This is a useful construct in that it allows for alignment of portions of a structure.

#include <stdio.h>

struct A {              struct { int a; };   };
struct B { _Alignas(64) struct { int b; };   };
struct C { _Alignas(64) struct { int c; } x; };

int main(int argc, char *argv[])
{
	printf("%zu %zu %zu\n",
	       sizeof(struct A), sizeof(struct B), sizeof(struct C));
	return 0;
}

Should output "4 64 64" on an LP64 platform; instead outputs "4 4 64". GCC 9 compiles correctly. I haven't yet tested on platforms other than macOS.


---


### compiler : `llvm`
### title : `Can't remove shufflevector if input might be poison`
### open_at : `2019-11-30T15:20:30Z`
### last_modified_date : `2021-09-27T10:24:11Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=44185
### status : `NEW`
### tags : `miscompilation`
### component : `Scalar Optimizations`
### version : `trunk`
### severity : `normal`
### contents :
Test case from Transforms/InstCombine/insert-extract-shuffle.ll:

define <4 x float> @insert_not_undef_shuffle_translate_commute(float %x, <4 x float> %y, <4 x float> %q) {
  %xv = insertelement <4 x float> %q, float %x, i32 2
  %r = shufflevector <4 x float> %y, <4 x float> %xv, <4 x i32> { 0, 6, 2, undef }
  ret <4 x float> %r
}
=>
define <4 x float> @insert_not_undef_shuffle_translate_commute(float %x, <4 x float> %y, <4 x float> %q) {
  %r = insertelement <4 x float> %y, float %x, i32 1
  ret <4 x float> %r
}
Transformation doesn't verify!
ERROR: Target is more poisonous than source

Example:
float %x = poison
<4 x float> %y = < poison, poison, poison, poison >
<4 x float> %q = < poison, poison, poison, poison >

Source:
<4 x float> %xv = < poison, poison, poison, poison >
<4 x float> %r = < poison, poison, poison, undef >

Target:
<4 x float> %r = < poison, poison, poison, poison >
Source value: < poison, poison, poison, undef >
Target value: < poison, poison, poison, poison >


This is with the semantics of LangRef, where an undef mask stops propagation of poison. This implies this kind of shufflevectors can't be removed.


---


### compiler : `llvm`
### title : `Incorrect instcombine transform urem -> icmp+zext with vectors`
### open_at : `2019-11-30T15:28:15Z`
### last_modified_date : `2019-12-20T19:25:19Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=44186
### status : `RESOLVED`
### tags : `miscompilation`
### component : `Scalar Optimizations`
### version : `trunk`
### severity : `normal`
### contents :
Testcase from Transforms/InstCombine/vector-urem.ll:

define <4 x i32> @test_v4i32_one_undef(<4 x i32> %a0) {
  %1 = urem <4 x i32> { 1, 1, 1, undef }, %a0
  ret <4 x i32> %1
}
=>
define <4 x i32> @test_v4i32_one_undef(<4 x i32> %a0) {
  %1 = icmp ne <4 x i32> %a0, { 1, 1, 1, undef }
  %2 = zext <4 x i1> %1 to <4 x i32>
  ret <4 x i32> %2
}
Transformation doesn't verify!
ERROR: Value mismatch

Example:
<4 x i32> %a0 = < #x00000010 (16), #x00000001 (1), #x00000400 (1024), #x00000001 (1) >

Source:
<4 x i32> %1 = < #x00000001 (1), #x00000000 (0), #x00000001 (1), #x00000000 (0) >

Target:
<4 x i1> %1 = < #x1 (1), #x0 (0), #x1 (1), #x1 (1) >
<4 x i32> %2 = < #x00000001 (1), #x00000000 (0), #x00000001 (1), #x00000001 (1) >
Source value: < #x00000001 (1), #x00000000 (0), #x00000001 (1), #x00000000 (0) >
Target value: < #x00000001 (1), #x00000000 (0), #x00000001 (1), #x00000001 (1) >


Essentially, "x urem 1" is 0 for any 'x'. However, the optimized code can produce 0 or 1.
I guess the easiest fix is to change undef to 1 in the icmp.


---


### compiler : `llvm`
### title : `[CLANG-CL] 64x inline assembler function call/jump miscompiled`
### open_at : `2019-12-11T10:38:00Z`
### last_modified_date : `2020-01-11T21:42:10Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=44272
### status : `RESOLVED`
### tags : `miscompilation`
### component : `new bugs`
### version : `9.0`
### severity : `normal`
### contents :
I've recently starting using Clang-CL in Visual Studio 2019 and I've discovered a fatal bug within the compiler, when attempting to call a function within inline assembly the function pointer is dereferenced, causing to crash due to memory access violation, the same issue exists by attempting to "jmp" to a function directly, I've tried to fix this in various ways, but I only found a way to get around the problem, this happens only with 64bit inline assembler and the fatal bug is clearly visible within assembly output.

The problem is replicated by doing something like this:

int main() {
      __asm {
           xor rcx, rcx
           call exit
      }
      printf("The application didn't quit!");
      return 0;
}

The generated inline assembly looks like this:

xor rcx, rcx
call qword ptr [exit]

The way I get around the problem is by using "lea" instruction to retrieve the function pointer, which looks like this:

__asm {
     xor rcx, rcx
     lea rax, exit
     call rax 
}

Results in generated inline assembly that looks like this:

xor rcx, rcx
lea rax, [exit]
call rax

This no longer results in a crash.

My Clang-CL installation (--version):

CLang Version: 9.0.0 (release-final)
Target: x86_64-pc-windows-msvc
InstalledDir: C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Tools\Llvm\bin

The Clang-CL compiler is downloaded via visual studio 2019 installer, selecting the "C++ Clang tools for Windows (9.0.0 - x64/x86)"

I hope this problem can be addressed soon, this is my first time reporting a bug. Thank you.


---


### compiler : `llvm`
### title : `Instcombine: incorrect transformation 'x > (x & undef)' -> 'x > undef'`
### open_at : `2019-12-26T19:39:34Z`
### last_modified_date : `2020-10-24T01:33:04Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=44383
### status : `RESOLVED`
### tags : `miscompilation`
### component : `Scalar Optimizations`
### version : `trunk`
### severity : `normal`
### contents :
The following transformation in Transforms/InstCombine/canonicalize-constant-low-bit-mask-and-icmp-sgt-to-icmp-sgt.ll is incorrect:

define <3 x i1> @p3_vec_splat_undef() {
  %x = call <3 x i8> @gen3x8()
  %tmp0 = and <3 x i8> %x, { 3, undef, 3 }
  %ret = icmp sgt <3 x i8> %x, %tmp0
  ret <3 x i1> %ret
}
=>
define <3 x i1> @p3_vec_splat_undef() {

  %x = call <3 x i8> @gen3x8()
  %1 = icmp sgt <3 x i8> %x, { 3, undef, 3 }
  ret <3 x i1> %1
}

Transformation doesn't verify!
ERROR: Value mismatch

Example:

Source:
<3 x i8> %x = < poison, #x00 (0), poison >
<3 x i8> %tmp0 = < poison, #x00 (0), poison >
<3 x i1> %ret = < poison, #x0 (0), poison >

Target:
<3 x i8> %x = < poison, #x00 (0), poison >
<3 x i1> %1 = < poison, #x1 (1), poison >
Source value: < poison, #x0 (0), poison >
Target value: < poison, #x1 (1), poison >


The transformation does 'x > (x & undef)' -> 'x > undef'.
Take x=0, undef=-1, and we get '0 > 0' -> '0 > -1'.


---


### compiler : `llvm`
### title : `Instcombine incorrectly transforms store i64 -> store double`
### open_at : `2020-03-09T15:33:20Z`
### last_modified_date : `2021-03-20T17:14:27Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=45152
### status : `NEW`
### tags : `miscompilation`
### component : `Scalar Optimizations`
### version : `trunk`
### severity : `normal`
### contents :
The unit test "test/Transforms/InstCombine/bitcast-phi-uselistorder.ll" shows an incorrect transformation from load+store i64 into load/store double. These are not equivalent because NaN values can be canonicalized by the CPU so the store double can write a different bit-pattern than store i64.

Alive2's counterexample:
@Q = global 8 bytes, align 8

define double @test(i1 %c, * %p) {
%entry:
  br i1 %c, label %if, label %end

%if:
  %__constexpr_0 = bitcast * @Q to *
  %load = load i64, * %__constexpr_0, align 8
  br label %end

%end:
  %phi = phi i64 [ 0, %entry ], [ %load, %if ]
  store i64 %phi, * %p, align 8
  %cast = bitcast i64 %phi to double
  ret double %cast
}
=>
@Q = global 8 bytes, align 8

define double @test(i1 %c, * %p) {
%entry:
  br i1 %c, label %if, label %end

%if:
  %load1 = load double, * @Q, align 8
  br label %end

%end:
  %0 = phi double [ 0.000000, %entry ], [ %load1, %if ]
  %1 = bitcast * %p to *
  store double %0, * %1, align 8
  ret double %0
}
Transformation doesn't verify!
ERROR: Mismatch in memory

Example:
i1 %c = #x1 (1)
* %p = pointer(non-local, block_id=2, offset=64)

Source:
* %__constexpr_0 = pointer(non-local, block_id=1, offset=0)
i64 %load = #x7ff0000001000000 (9218868437244182528)
i64 %phi = #x7ff0000001000000 (9218868437244182528)
double %cast = NaN

Target:
double %load1 = NaN
double %0 = NaN
* %1 = pointer(non-local, block_id=2, offset=64)

Mismatch in pointer(non-local, block_id=2, offset=64)
Source value: #x7ff0000001000000
Target value: #x7ff0000000020000


---


### compiler : `llvm`
### title : `[inline assembly] "p" constraint is not always a valid address`
### open_at : `2020-03-10T18:06:43Z`
### last_modified_date : `2020-03-10T18:06:43Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=45168
### status : `NEW`
### tags : `compile-fail, miscompilation`
### component : `Frontend`
### version : `trunk`
### severity : `normal`
### contents :
Consider the following (useless) code:

int * f (int *p)
{
    __asm__ ("leal %a1, %0" : "=r" (p) : "p" (p));
    return p;
}

Which produces the following IR:

define dso_local i32* @f(i32* readnone) local_unnamed_addr #0 !dbg !8 {
  call void @llvm.dbg.value(metadata i32* %0, metadata !15, metadata !DIExpression()), !dbg !16
  %2 = tail call i32* asm "leal ${1:a}, $0", "=r,im,~{dirflag},~{fpsr},~{flags}"(i32* %0) #2, !dbg !17, !srcloc !18
  call void @llvm.dbg.value(metadata i32* %2, metadata !15, metadata !DIExpression()), !dbg !16
  ret i32* %2, !dbg !19
}

We can see that "p" has been translated to "im". It is true from at least clang 3.0 to at least 9.0 (tested on https://godbolt.org/).
But "p" definition is "An operand that is a valid memory address is allowed.".
Correct me, but "m" is not a valid memory address as it is already a memory access.
I think a non-optimal way to encode "p" would rather be "ir" as both constant and register can be part of an address, but it would miss complex addresses like "%ebp + 4 * %eax - 8".


---


### compiler : `llvm`
### title : `Incorrect optimization of gep without inbounds + load -> icmp eq`
### open_at : `2020-03-15T11:31:29Z`
### last_modified_date : `2021-05-31T17:24:49Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=45210
### status : `RESOLVED`
### tags : `miscompilation`
### component : `Scalar Optimizations`
### version : `trunk`
### severity : `normal`
### contents :
The following unit test in "Transforms/InstCombine/load-cmp.ll" exposes an incorrect optimization:

define i1 @test1_noinbounds(i32 %X) {
; CHECK-LABEL: @test1_noinbounds(
; CHECK-NEXT:    [[R:%.*]] = icmp eq i32 [[X:%.*]], 9
; CHECK-NEXT:    ret i1 [[R]]
;
  %P = getelementptr [10 x i16], [10 x i16]* @G16, i32 0, i32 %X
  %Q = load i16, i16* %P
  %R = icmp eq i16 %Q, 0
  ret i1 %R
}


Output of Alive2. TL;DR: the optimization is only correct with gep inbounds, otherwise the transformation to "icmp eq" misses the overflow case.

@G16 = constant 20 bytes, align 16

define i1 @test1_noinbounds(i32 %X) {
#init:
  store [10 x i16] { 35, 82, 69, 81, 85, 73, 82, 69, 68, 0 }, * @G16, align 16
  br label %0

%0:
  %P = gep * @G16, 20 x i32 0, 2 x i32 %X
  %Q = load i16, * %P, align 2
  %R = icmp eq i16 %Q, 0
  ret i1 %R
}
=>
@G16 = constant 20 bytes, align 16

define i1 @test1_noinbounds(i32 %X) {
#init:
  store [10 x i16] { 35, 82, 69, 81, 85, 73, 82, 69, 68, 0 }, * @G16, align 16
  br label %0

%0:
  %R = icmp eq i32 %X, 9
  ret i1 %R
}


Transformation doesn't verify!
ERROR: Value mismatch

Example:
i32 %X = #x80000009 (2147483657, -2147483639)

Source:
* %P = pointer(non-local, block_id=1, offset=18)
i16 %Q = #x0000 (0)
i1 %R = #x1 (1)

Target:
i1 %R = #x0 (0)
Source value: #x1 (1)
Target value: #x0 (0)


---


### compiler : `llvm`
### title : `Invalid transform: gep p, (q-p) -> q`
### open_at : `2020-04-06T13:18:49Z`
### last_modified_date : `2020-04-06T15:30:42Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=45444
### status : `RESOLVED`
### tags : `miscompilation`
### component : `Scalar Optimizations`
### version : `trunk`
### severity : `normal`
### contents :
Unit test: Transforms/InstCombine/getelementptr.ll
Summary: just because 2 pointers have the same integer value it doesn't mean they are the same pointer. While %gep is in bounds, %c2 may refer to another object with an OOB pointer.

define * @test45(* %c1, * %c2) {
%0:
  %ptrtoint1 = ptrtoint * %c1 to i64
  %ptrtoint2 = ptrtoint * %c2 to i64
  %sub = sub i64 %ptrtoint2, %ptrtoint1
  %shr = sdiv i64 %sub, 7
  %gep = gep inbounds * %c1, 7 x i64 %shr
  ret * %gep
}
=>
define * @test45(* %c1, * %c2) {
%0:
  %gep = bitcast * %c2 to *
  ret * %gep
}
Transformation doesn't verify!
ERROR: Value mismatch

Example:
* %c1 = pointer(non-local, block_id=1, offset=7790792235569643584)
* %c2 = pointer(non-local, block_id=0, offset=8251192938491543615)

Source:
i64 %ptrtoint1 = #x72907442c8000040 (8255225947142225984)
i64 %ptrtoint2 = #x72822042c800003f (8251192938491543615)
i64 %sub = #xfff1abffffffffff (18442711065058869247, -4033008650682369)
i64 %shr = #xfffdf40000000000 (18446167929616596992, -576144092954624)
* %gep = pointer(non-local, block_id=1, offset=7786759226918961216)

Target:
* %gep = pointer(non-local, block_id=0, offset=8251192938491543615)
Source value: pointer(non-local, block_id=1, offset=7786759226918961216)
Target value: pointer(non-local, block_id=0, offset=8251192938491543615)


https://web.ist.utl.pt/nuno.lopes/alive2/index.php?hash=2009353267698970&test=Transforms%2FInstCombine%2Fgetelementptr.ll


---


### compiler : `llvm`
### title : `gep(ptr, undef) isn't undef`
### open_at : `2020-04-06T13:33:17Z`
### last_modified_date : `2020-10-22T16:46:05Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=45445
### status : `NEW`
### tags : `miscompilation`
### component : `Scalar Optimizations`
### version : `trunk`
### severity : `normal`
### contents :
Test: Transforms/InstCombine/vec_demanded_elts.ll
Summary: gep(ptr, undef) isn't undef. It's a pointer based on ptr with an undef offset (a multiple of 4 in this case). A way to make this correct is to return <%base, %base>.


define <2 x *> @gep_all_lanes_undef(* %base, i64 %idx) {
  %basevec = insertelement <2 x *> undef, * %base, i32 0
  %idxvec = insertelement <2 x i64> undef, i64 %idx, i32 1
  %gep = gep <2 x *> %basevec, 4 x <2 x i64> %idxvec
  ret <2 x *> %gep
}
=>
define <2 x *> @gep_all_lanes_undef(* %base, i64 %idx) {
  ret <2 x *> undef
}

Transformation doesn't verify!
ERROR: Value mismatch

Example:
* %base = pointer(non-local, block_id=1, offset=0)
i64 %idx = #x0000000000080000 (524288)

Source:
<2 x *> %basevec = < pointer(non-local, block_id=1, offset=0), null >
<2 x i64> %idxvec = < undef, #x0000000000080000 (524288) >
<2 x *> %gep = < pointer(non-local, block_id=1, offset=0), pointer(non-local, block_id=0, offset=2097152) >

Target:
Source value: < pointer(non-local, block_id=1, offset=0), pointer(non-local, block_id=0, offset=2097152) >
Target value: < pointer(non-local, block_id=0, offset=16), null >


https://web.ist.utl.pt/nuno.lopes/alive2/index.php?hash=2009353267698970&test=Transforms%2FInstCombine%2Fvec_demanded_elts.ll


---


### compiler : `llvm`
### title : `Incorrect transformation: (undef u>> a) ^ -1  ->  undef >> a, when a != 0`
### open_at : `2020-04-06T14:05:52Z`
### last_modified_date : `2020-10-24T01:33:04Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=45447
### status : `RESOLVED`
### tags : `miscompilation`
### component : `Scalar Optimizations`
### version : `trunk`
### severity : `enhancement`
### contents :
Test: Transforms/InstCombine/vector-xor.ll
Summary: (undef u>> a) ^ -1 always leaves top bits as 1 when a > 0. However 'undef >> a' can leave top bits as 0 or 1, depending on the sign bit of undef.


define <4 x i32> @test_v4i32_not_lshr_nonnegative_const_undef(<4 x i32> %a0) {
  %1 = lshr <4 x i32> { 3, 5, undef, 9 }, %a0
  %2 = xor <4 x i32> { 4294967295, 4294967295, 4294967295, undef }, %1
  ret <4 x i32> %2
}
=>
define <4 x i32> @test_v4i32_not_lshr_nonnegative_const_undef(<4 x i32> %a0) {
  %1 = ashr <4 x i32> { 4294967292, 4294967290, undef, 4294967286 }, %a0
  ret <4 x i32> %1
}
Transformation doesn't verify!
ERROR: Value mismatch

Example:
<4 x i32> %a0 = < #x00000000 (0), #xfffffffe (4294967294, -2), #x0000001f (31), #xfffffffe (4294967294, -2) >

Source:
<4 x i32> %1 = < #x00000003 (3), poison, #x00000000 (0)	[based on undef value], poison >
<4 x i32> %2 = < #xfffffffc (4294967292, -4), poison, #xffffffff (4294967295, -1), poison >

Target:
<4 x i32> %1 = < #xfffffffc (4294967292, -4), poison, #x00000000 (0), poison >
Source value: < #xfffffffc (4294967292, -4), poison, #xffffffff (4294967295, -1), poison >
Target value: < #xfffffffc (4294967292, -4), poison, #x00000000 (0), poison >


https://web.ist.utl.pt/nuno.lopes/alive2/index.php?hash=2009353267698970&test=Transforms%2FInstCombine%2Fvector-xor.ll


---


### compiler : `llvm`
### title : `Invalid undef splat in instcombine`
### open_at : `2020-04-07T08:29:38Z`
### last_modified_date : `2020-05-20T14:26:56Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=45455
### status : `RESOLVED`
### tags : `miscompilation`
### component : `Scalar Optimizations`
### version : `trunk`
### severity : `normal`
### contents :
Test: Transforms/InstCombine/unfold-masked-merge-with-const-mask-vector.ll

define <3 x i4> @splat_undef(<3 x i4> %x, <3 x i4> %y) {
  %n0 = xor <3 x i4> %x, %y
  %n1 = and <3 x i4> %n0, { 14, undef, 14 }
  %r = xor <3 x i4> %n1, %y
  ret <3 x i4> %r
}
=>
define <3 x i4> @splat_undef(<3 x i4> %x, <3 x i4> %y) {
  %1 = and <3 x i4> %x, { 14, undef, 14 }
  %2 = and <3 x i4> %y, { 1, undef, 1 }
  %r = or <3 x i4> %1, %2
  ret <3 x i4> %r
}
Transformation doesn't verify!
ERROR: Value mismatch

Example:
<3 x i4> %x = < #x0 (0), #xd (13, -3), #x0 (0) >
<3 x i4> %y = < undef, #x8 (8, -8), #x0 (0) >

Source:
<3 x i4> %n0 = < #x0 (0), #x5 (5), #x0 (0) >
<3 x i4> %n1 = < #x0 (0), #x0 (0)	[based on undef value], #x0 (0) >
<3 x i4> %r = < #x0 (0), #x8 (8, -8), #x0 (0) >

Target:
<3 x i4> %1 = < #x0 (0), #x1 (1), #x0 (0) >
<3 x i4> %2 = < #x0 (0), #x0 (0), #x0 (0) >
<3 x i4> %r = < #x0 (0), #x1 (1), #x0 (0) >
Source value: < #x0 (0), #x8 (8, -8), #x0 (0) >
Target value: < #x0 (0), #x1 (1), #x0 (0) >


https://web.ist.utl.pt/nuno.lopes/alive2/index.php?hash=2009353267698970&test=Transforms%2FInstCombine%2Funfold-masked-merge-with-const-mask-vector.ll


---


### compiler : `llvm`
### title : `Can't remove insertelement undef`
### open_at : `2020-04-09T09:03:34Z`
### last_modified_date : `2020-12-02T14:43:30Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=45481
### status : `RESOLVED`
### tags : `miscompilation`
### component : `Scalar Optimizations`
### version : `trunk`
### severity : `normal`
### contents :
Test: Transforms/InstSimplify/insertelement.ll
Summary: We can't remove insertelement undef to a vector, since it may be replacing a poison value.

define <4 x i32> @PR1286(<4 x i32> %A) {
  %B = insertelement <4 x i32> %A, i32 undef, i32 1
  ret <4 x i32> %B
}
=>
define <4 x i32> @PR1286(<4 x i32> %A) {
  ret <4 x i32> %A
}
Transformation doesn't verify!
ERROR: Target is more poisonous than source

Example:
<4 x i32> %A = < poison, poison, poison, poison >

Source:
<4 x i32> %B = < poison, undef, poison, poison >

Target:
Source value: < poison, undef, poison, poison >
Target value: < poison, poison, poison, poison >


Report: https://web.ist.utl.pt/nuno.lopes/alive2/index.php?hash=ed3ac07d4817b221&test=Transforms%2FInstSimplify%2Finsertelement.ll


---


### compiler : `llvm`
### title : `InstSimplify: fadd (nsz op), +0 incorrectly removed`
### open_at : `2020-05-02T11:08:15Z`
### last_modified_date : `2020-05-05T22:39:51Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=45778
### status : `RESOLVED`
### tags : `miscompilation`
### component : `Scalar Optimizations`
### version : `trunk`
### severity : `normal`
### contents :
Test: Transforms/InstSimplify/fast-math.ll
Summary: +0 + +0 == +0 and -0 + +0 == +0 in default rounding mode. Hence below when %nsz is +/-0 the function returns +0 only, while the optimized function returns +/-0.

define float @fold_fadd_cannot_be_neg0_nsz_src_x_0(float %a, float %b) {
  %nsz = fmul nsz float %a, %b
  %add = fadd float %nsz, 0.000000
  ret float %add
}
=>
define float @fold_fadd_cannot_be_neg0_nsz_src_x_0(float %a, float %b) {
  %nsz = fmul nsz float %a, %b
  ret float %nsz
}
Transformation doesn't verify!
ERROR: Value mismatch

Example:
float %a = #x01e21080 (0.000000000000?)
float %b = #x00225d01 (0.000000000000?)

Source:
float %nsz = #x80000000 (-0.0)
float %add = #x00000000 (+0.0)

Target:
float %nsz = #x80000000 (-0.0)
Source value: #x00000000 (+0.0)
Target value: #x80000000 (-0.0)

https://web.ist.utl.pt/nuno.lopes/alive2/index.php?hash=1ede71ade7988ad1&test=Transforms%2FInstSimplify%2Ffast-math.ll


---


### compiler : `llvm`
### title : `The using declaration doesn't work for parent class' constructors.`
### open_at : `2020-05-05T04:30:27Z`
### last_modified_date : `2020-05-05T19:09:04Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=45801
### status : `RESOLVED`
### tags : `miscompilation`
### component : `C++14`
### version : `10.0`
### severity : `normal`
### contents :
The following code works in GCC 9.3 and MSVC v19.24, but fails in Clang 10.0.0 (adding the typename keyword resolves that issue, but Clang has other problems that GCC does not).
 
==================
template<typename>
struct A
{
    int n;

    A(bool)
    {}
};

template<typename>
struct B
{
    struct C : A<B>
    {
        using Base = A<B>;

        using A<B>::A; // ok
        using Base::n; // ok

        // error: dependent using declaration resolved to type without 'typename'
        using Base::A;
    };

    C get() const
    {
        return C(true);
    }
};

int main()
{
    auto b = B<int>();
    b.get();
}


---


### compiler : `llvm`
### title : `Incorrect instcombine fold of control-flow to umul.with.overflow`
### open_at : `2020-05-16T22:24:26Z`
### last_modified_date : `2020-06-01T10:25:32Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=45952
### status : `NEW`
### tags : `miscompilation`
### component : `Scalar Optimizations`
### version : `trunk`
### severity : `normal`
### contents :
Test: Transforms/PhaseOrdering/unsigned-multiply-overflow-check.ll
Summary: the original code below has a fast-path for %arg1=0 and returns 0 in that case. The optimized code has no fast-path and so the result is tainted if %arg=poison.


define i1 @will_not_overflow(i64 %arg, i64 %arg1) {
  %t0 = icmp eq i64 %arg, 0
  br i1 %t0, label %bb5, label %bb2

%bb2:
  %t3 = udiv i64 -1, %arg
  %t4 = icmp ult i64 %t3, %arg1
  br label %bb5

%bb5:
  %t6 = phi i1 [ 0, %bb ], [ %t4, %bb2 ]
  ret i1 %t6
}
=>
define i1 @will_not_overflow(i64 %arg, i64 %arg1) {
  %umul = umul_overflow {i64, i1, i56} %arg, %arg1
  %umul.ov = extractvalue {i64, i1, i56} %umul, 1
  ret i1 %umul.ov
}
Transformation doesn't verify!
ERROR: Target is more poisonous than source

Example:
i64 %arg = #x0000000000000000 (0)
i64 %arg1 = poison

Source:
i1 %t0 = #x1 (1)
i64 %t3 = #xffffffffffffffff (18446744073709551615, -1)
i1 %t4 = poison
i1 %t6 = #x0 (0)

Target:
{i64, i1, i56} %umul = { poison, poison, poison }
i1 %umul.ov = poison
Source value: #x0 (0)
Target value: poison

https://web.ist.utl.pt/nuno.lopes/alive2/index.php?hash=72296a443c683892&test=Transforms%2FPhaseOrdering%2Funsigned-multiply-overflow-check.ll


---


### compiler : `llvm`
### title : `Incorrect instcombine fold of vector ult -> sgt`
### open_at : `2020-05-17T11:53:52Z`
### last_modified_date : `2020-09-03T19:57:48Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=45954
### status : `NEW`
### tags : `miscompilation`
### component : `Scalar Optimizations`
### version : `trunk`
### severity : `normal`
### contents :
Test: Transforms/InstCombine/canonicalize-clamp-like-pattern-between-zero-and-positive-threshold.ll
Summary: There's a off-by-one in the transformation below that makes the optimize code return the wrong value.
The original code can return either %x or %replacement_low, while the optimized code returns %replacement_high for %x[1] == 65536.

define <3 x i32> @t20_ult_slt_vec_undef1(<3 x i32> %x, <3 x i32> %replacement_low, <3 x i32> %replacement_high) {
  %t0 = icmp slt <3 x i32> %x, { 65536, 65537, 65536 }
  %t1 = select <3 x i1> %t0, <3 x i32> %replacement_low, <3 x i32> %replacement_high
  %t2 = icmp ult <3 x i32> %x, { 65536, undef, 65536 }
  %r = select <3 x i1> %t2, <3 x i32> %x, <3 x i32> %t1
  ret <3 x i32> %r
}
=>
define <3 x i32> @t20_ult_slt_vec_undef1(<3 x i32> %x, <3 x i32> %replacement_low, <3 x i32> %replacement_high) {
  %1 = icmp slt <3 x i32> %x, { 0, 0, 0 }
  %2 = icmp sgt <3 x i32> %x, { 65535, 65535, 65535 }
  %3 = select <3 x i1> %1, <3 x i32> %replacement_low, <3 x i32> %x
  %r = select <3 x i1> %2, <3 x i32> %replacement_high, <3 x i32> %3
  ret <3 x i32> %r
}
Transformation doesn't verify!
ERROR: Value mismatch

Example:
<3 x i32> %x = < #x0000ffff (65535), #x00010000 (65536), #x08000000 (134217728) >
<3 x i32> %replacement_low = < *, #x00000000 (0), * >
<3 x i32> %replacement_high = < *, #x00001000 (4096), #x0000ffff (65535) >

Source:
<3 x i1> %t0 = < #x1 (1), #x1 (1), #x0 (0) >
<3 x i32> %t1 = < *, #x00000000 (0), #x0000ffff (65535) >
<3 x i1> %t2 = < #x1 (1), undef, #x0 (0) >
<3 x i32> %r = < #x0000ffff (65535), #x00000000 (0)     [based on undef value], #x0000ffff (65535) >

Target:
<3 x i1> %1 = < #x0 (0), #x0 (0), #x0 (0) >
<3 x i1> %2 = < #x0 (0), #x1 (1), #x1 (1) >
<3 x i32> %3 = < #x0000ffff (65535), #x00010000 (65536), #x08000000 (134217728) >
<3 x i32> %r = < #x0000ffff (65535), #x00001000 (4096), #x0000ffff (65535) >
Source value: < #x0000ffff (65535), #x00000000 (0), #x0000ffff (65535) >
Target value: < #x0000ffff (65535), #x00001000 (4096), #x0000ffff (65535) >


https://web.ist.utl.pt/nuno.lopes/alive2/index.php?hash=72296a443c683892&test=Transforms%2FInstCombine%2Fcanonicalize-clamp-like-pattern-between-zero-and-positive-threshold.ll


---


### compiler : `llvm`
### title : `Incorrect instcombine fold of vector bitwise of ((x ^ y) & const) ^ y`
### open_at : `2020-05-17T12:07:51Z`
### last_modified_date : `2020-05-20T14:26:56Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=45955
### status : `RESOLVED`
### tags : `miscompilation`
### component : `Scalar Optimizations`
### version : `trunk`
### severity : `normal`
### contents :
Test: Transforms/InstCombine/unfold-masked-merge-with-const-mask-vector.ll
TL;DR: the transformation below needs to fix the newly introduced undef constants

define <3 x i4> @splat_undef(<3 x i4> %x, <3 x i4> %y) {
  %n0 = xor <3 x i4> %x, %y
  %n1 = and <3 x i4> %n0, { 14, undef, 14 }
  %r = xor <3 x i4> %n1, %y
  ret <3 x i4> %r
}
=>
define <3 x i4> @splat_undef(<3 x i4> %x, <3 x i4> %y) {
  %1 = and <3 x i4> %x, { 14, undef, 14 }
  %2 = and <3 x i4> %y, { 1, undef, 1 }
  %r = or <3 x i4> %1, %2
  ret <3 x i4> %r
}
Transformation doesn't verify!
ERROR: Value mismatch

Example:
<3 x i4> %x = < #x0 (0), #xd (13, -3), #x0 (0) >
<3 x i4> %y = < undef, #x8 (8, -8), #x0 (0) >

Source:
<3 x i4> %n0 = < #x0 (0), #x5 (5), #x0 (0) >
<3 x i4> %n1 = < #x0 (0), #x0 (0)	[based on undef value], #x0 (0) >
<3 x i4> %r = < #x0 (0), #x8 (8, -8), #x0 (0) >

Target:
<3 x i4> %1 = < #x0 (0), #x1 (1), #x0 (0) >
<3 x i4> %2 = < #x0 (0), #x0 (0), #x0 (0) >
<3 x i4> %r = < #x0 (0), #x1 (1), #x0 (0) >
Source value: < #x0 (0), #x8 (8, -8), #x0 (0) >
Target value: < #x0 (0), #x1 (1), #x0 (0) >


https://web.ist.utl.pt/nuno.lopes/alive2/index.php?hash=72296a443c683892&test=Transforms%2FInstCombine%2Funfold-masked-merge-with-const-mask-vector.ll


---


### compiler : `llvm`
### title : `Jumpthreading introduces jump on poison`
### open_at : `2020-05-17T12:30:55Z`
### last_modified_date : `2020-07-26T10:44:48Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=45956
### status : `NEW`
### tags : `miscompilation`
### component : `Scalar Optimizations`
### version : `trunk`
### severity : `normal`
### contents :
Test: Transforms/JumpThreading/select.ll
Summary: the optimized code has a new jump on `%phitmp`, which is UB if either %y or %z are poison. The original code doesn't have any jump depending on either of these values. A correct version requires introducing of freeze.


define i32 @unfold3(i32 %u, i32 %v, i32 %w, i32 %x, i32 %y, i32 %z, i32 %j) {
%entry:
  %add3 = add nsw i32 %j, 2
  %cmp.i = icmp slt i32 %u, %v
  br i1 %cmp.i, label %.exit, label %cond.false.i

%cond.false.i:
  %cmp4.i = icmp sgt i32 %u, %v
  br i1 %cmp4.i, label %.exit, label %cond.false.6.i

%cond.false.6.i:
  %cmp8.i = icmp slt i32 %w, %x
  br i1 %cmp8.i, label %.exit, label %cond.false.10.i

%cond.false.10.i:
  %cmp13.i = icmp sgt i32 %w, %x
  br i1 %cmp13.i, label %.exit, label %cond.false.15.i

%cond.false.15.i:
  %phitmp = icmp sge i32 %y, %z
  br label %.exit

%.exit:
  %cond23.i = phi i1 [ 0, %entry ], [ 1, %cond.false.i ], [ 0, %cond.false.6.i ], [ %phitmp, %cond.false.15.i ], [ 1, %cond.false.10.i ]
  %j.add3 = select i1 %cond23.i, i32 %j, i32 %add3
  ret i32 %j.add3
}
=>
define i32 @unfold3(i32 %u, i32 %v, i32 %w, i32 %x, i32 %y, i32 %z, i32 %j) {
%entry:
  %add3 = add nsw i32 %j, 2
  %cmp.i = icmp slt i32 %u, %v
  br i1 %cmp.i, label %.exit.thread3, label %cond.false.i

%cond.false.i:
  %cmp4.i = icmp sgt i32 %u, %v
  br i1 %cmp4.i, label %.exit.thread, label %cond.false.6.i

%cond.false.6.i:
  %cmp8.i = icmp slt i32 %w, %x
  br i1 %cmp8.i, label %.exit.thread3, label %cond.false.10.i

%cond.false.10.i:
  %cmp13.i = icmp sgt i32 %w, %x
  br i1 %cmp13.i, label %.exit.thread, label %.exit

%.exit:
  %phitmp = icmp sge i32 %y, %z
  br i1 %phitmp, label %.exit.thread, label %.exit.thread3

%.exit.thread:
  br label %.exit.thread3

%.exit.thread3:
  %0 = phi i32 [ %j, %.exit.thread ], [ %add3, %.exit ], [ %add3, %entry ], [ %add3, %cond.false.6.i ]
  ret i32 %0
}
Transformation doesn't verify!
ERROR: Source is more defined than target

Example:
i32 %u = #x2ba5afc9 (732278729)
i32 %v = #x2ba5afc9 (732278729)
i32 %w = #x400000c1 (1073742017)
i32 %x = #x400000c1 (1073742017)
i32 %y = poison
i32 %z = poison
i32 %j = poison

Source:
i32 %add3 = poison
i1 %cmp.i = #x0 (0)
i1 %cmp4.i = #x0 (0)
i1 %cmp8.i = #x0 (0)
i1 %cmp13.i = #x0 (0)
i1 %phitmp = poison
i1 %cond23.i = poison
i32 %j.add3 = poison

Target:
i32 %add3 = poison
i1 %cmp.i = #x0 (0)
i1 %cmp4.i = #x0 (0)
i1 %cmp8.i = #x0 (0)
i1 %cmp13.i = #x0 (0)
i1 %phitmp = poison
i32 %0 = poison


---


### compiler : `llvm`
### title : `X86InterleavedAccess introduces misaligned loads`
### open_at : `2020-05-17T15:00:31Z`
### last_modified_date : `2020-05-27T12:30:32Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=45957
### status : `RESOLVED`
### tags : `miscompilation`
### component : `Backend: X86`
### version : `trunk`
### severity : `normal`
### contents :
See here: https://github.com/llvm/llvm-project/blob/master/llvm/lib/Target/X86/X86InterleavedAccess.cpp#L219

    Value *NewBasePtr =
        Builder.CreateGEP(VecBaseTy, VecBasePtr, Builder.getInt32(i));
    Instruction *NewLoad =
        Builder.CreateAlignedLoad(VecBaseTy, NewBasePtr, LI->getAlign());

Newly created loads inherit the original load's alignment. This is not correct, as the original load may have a larger alignment than the GEP done above.

A concrete failure we see is in: Transforms/InterleavedAccess/X86/interleavedLoad.ll

define <32 x i8> @interleaved_load_vf32_i8_stride3(* %ptr) {
  %wide.vec = load <96 x i8>, * %ptr, align 128
...
}
=>
define <32 x i8> @interleaved_load_vf32_i8_stride3(* %ptr) {
  %1 = bitcast * %ptr to *
  %2 = gep * %1, 16 x i32 0
  %3 = load <16 x i8>, * %2, align 128  ; <-- this is not 128-byte aligned
  %4 = gep * %1, 16 x i32 1
  %5 = load <16 x i8>, * %4, align 128
  %6 = gep * %1, 16 x i32 2
  %7 = load <16 x i8>, * %6, align 128
...
}


Report: https://web.ist.utl.pt/nuno.lopes/alive2/index.php?hash=72296a443c683892&test=Transforms%2FInterleavedAccess%2FX86%2FinterleavedLoad.ll


---


### compiler : `llvm`
### title : `[AVR] Implement a subclass of clang::ABIInfo that is binary-compatible with AVR-GCC`
### open_at : `2020-05-30T05:09:21Z`
### last_modified_date : `2021-03-26T15:35:20Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=46140
### status : `CONFIRMED`
### tags : `ABI, accepts-invalid, miscompilation`
### component : `LLVM Codegen`
### version : `unspecified`
### severity : `normal`
### contents :
Currently, AVR under Clang uses the default ABI implementation - clang::DefaultABIInfo.

There will be cases where the default ABI implementation is binary-incompatible with AVR-GCC. A new AVR-specific calling convention ABIInfo subclass should be written.


---


### compiler : `llvm`
### title : `__int128 not aligned to 16-byte boundary`
### open_at : `2020-06-14T22:37:20Z`
### last_modified_date : `2020-06-16T02:39:55Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=46320
### status : `NEW`
### tags : `miscompilation`
### component : `Backend: X86`
### version : `10.0`
### severity : `normal`
### contents :
Consider this program:

int main(void) {
    __int128 x = 0;
    __asm__ __volatile__(
        "movdqa  %%xmm3, %0"
        : 
        : "xm"(x)
        : "xmm3"
    );
}

When I compile it with "clang -O3" on x86-64 and run it, it segfaults. The problem is that it put x at address 0x402008, which is only 8-byte aligned, even though the System V ABI requires that __int128's be 16-byte aligned, which "movdqa" depends on.

https://godbolt.org/z/kMJnSd


---


### compiler : `llvm`
### title : `ICE: Assertion `!verifyFunction(*L->getHeader()->getParent())' failed`
### open_at : `2020-06-30T20:07:18Z`
### last_modified_date : `2020-07-10T18:55:28Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=46525
### status : `RESOLVED`
### tags : `miscompilation`
### component : `new bugs`
### version : `trunk`
### severity : `enhancement`
### contents :
Error:
>$ clang++ -c -O3 func.cpp
clang++: llvm/llvm-trunk/llvm/lib/Transforms/Vectorize/LoopVectorize.cpp:7993: bool llvm::LoopVectorizePass::processLoop(llvm::Loop*): Assertion `!verifyFunction(*L->getHeader()->getParent())' failed.
PLEASE submit a bug report to https://bugs.llvm.org/ and include the crash backtrace, preprocessed source, and associated run script.
Stack dump:
0.	Program arguments: clang++ -c -O3 func.cpp 
1.	<eof> parser at end of file
2.	Per-module optimization passes
3.	Running pass 'Function Pass Manager' on module 'func.cpp'.
4.	Running pass 'Loop Vectorization' on function '@_Z4testv'
 #0 0x000055f2ca9fce3e llvm::sys::PrintStackTrace(llvm::raw_ostream&) (llvm/bin-trunk/bin/clang-11+0x238ee3e)
 #1 0x000055f2ca9fac14 llvm::sys::RunSignalHandlers() (llvm/bin-trunk/bin/clang-11+0x238cc14)
 #2 0x000055f2ca9fae91 llvm::sys::CleanupOnSignal(unsigned long) (llvm/bin-trunk/bin/clang-11+0x238ce91)
 #3 0x000055f2ca968ee8 CrashRecoverySignalHandler(int) (llvm/bin-trunk/bin/clang-11+0x22faee8)
 #4 0x00007ff9528db540 __restore_rt (/lib/x86_64-linux-gnu/libpthread.so.0+0x15540)
 #5 0x00007ff9523703eb raise /build/glibc-t7JzpG/glibc-2.30/signal/../sysdeps/unix/sysv/linux/raise.c:51:1
 #6 0x00007ff95234f899 abort /build/glibc-t7JzpG/glibc-2.30/stdlib/abort.c:81:7
 #7 0x00007ff95234f769 get_sysdep_segment_value /build/glibc-t7JzpG/glibc-2.30/intl/loadmsgcat.c:509:8
 #8 0x00007ff95234f769 _nl_load_domain /build/glibc-t7JzpG/glibc-2.30/intl/loadmsgcat.c:970:34
 #9 0x00007ff952361006 (/lib/x86_64-linux-gnu/libc.so.6+0x37006)
#10 0x000055f2cabc9a47 llvm::LoopVectorizePass::processLoop(llvm::Loop*) (llvm/bin-trunk/bin/clang-11+0x255ba47)
#11 0x000055f2cabcb710 llvm::LoopVectorizePass::runImpl(llvm::Function&, llvm::ScalarEvolution&, llvm::LoopInfo&, llvm::TargetTransformInfo&, llvm::DominatorTree&, llvm::BlockFrequencyInfo&, llvm::TargetLibraryInfo*, llvm::DemandedBits&, llvm::AAResults&, llvm::AssumptionCache&, std::function<llvm::LoopAccessInfo const& (llvm::Loop&)>&, llvm::OptimizationRemarkEmitter&, llvm::ProfileSummaryInfo*) (llvm/bin-trunk/bin/clang-11+0x255d710)
#12 0x000055f2cabcbba7 (anonymous namespace)::LoopVectorize::runOnFunction(llvm::Function&) (llvm/bin-trunk/bin/clang-11+0x255dba7)
#13 0x000055f2ca334f0c llvm::FPPassManager::runOnFunction(llvm::Function&) (llvm/bin-trunk/bin/clang-11+0x1cc6f0c)
#14 0x000055f2ca3355d9 llvm::FPPassManager::runOnModule(llvm::Module&) (llvm/bin-trunk/bin/clang-11+0x1cc75d9)
#15 0x000055f2ca335987 llvm::legacy::PassManagerImpl::run(llvm::Module&) (llvm/bin-trunk/bin/clang-11+0x1cc7987)
#16 0x000055f2cacaac06 clang::EmitBackendOutput(clang::DiagnosticsEngine&, clang::HeaderSearchOptions const&, clang::CodeGenOptions const&, clang::TargetOptions const&, clang::LangOptions const&, llvm::DataLayout const&, llvm::Module*, clang::BackendAction, std::unique_ptr<llvm::raw_pwrite_stream, std::default_delete<llvm::raw_pwrite_stream> >) (llvm/bin-trunk/bin/clang-11+0x263cc06)
#17 0x000055f2cb991591 clang::BackendConsumer::HandleTranslationUnit(clang::ASTContext&) (llvm/bin-trunk/bin/clang-11+0x3323591)
#18 0x000055f2cc70d2e9 clang::ParseAST(clang::Sema&, bool, bool) (llvm/bin-trunk/bin/clang-11+0x409f2e9)
#19 0x000055f2cb990098 clang::CodeGenAction::ExecuteAction() (llvm/bin-trunk/bin/clang-11+0x3322098)
#20 0x000055f2cb2d3f69 clang::FrontendAction::Execute() (llvm/bin-trunk/bin/clang-11+0x2c65f69)
#21 0x000055f2cb28afde clang::CompilerInstance::ExecuteAction(clang::FrontendAction&) (llvm/bin-trunk/bin/clang-11+0x2c1cfde)
#22 0x000055f2cb3a8d80 clang::ExecuteCompilerInvocation(clang::CompilerInstance*) (llvm/bin-trunk/bin/clang-11+0x2d3ad80)
#23 0x000055f2c9299269 cc1_main(llvm::ArrayRef<char const*>, char const*, void*) (llvm/bin-trunk/bin/clang-11+0xc2b269)
#24 0x000055f2c9296618 ExecuteCC1Tool(llvm::SmallVectorImpl<char const*>&) (llvm/bin-trunk/bin/clang-11+0xc28618)
#25 0x000055f2cb14d699 void llvm::function_ref<void ()>::callback_fn<clang::driver::CC1Command::Execute(llvm::ArrayRef<llvm::Optional<llvm::StringRef> >, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >*, bool*) const::'lambda'()>(long) (llvm/bin-trunk/bin/clang-11+0x2adf699)
#26 0x000055f2ca96906c llvm::CrashRecoveryContext::RunSafely(llvm::function_ref<void ()>) (llvm/bin-trunk/bin/clang-11+0x22fb06c)
#27 0x000055f2cb14dfc6 clang::driver::CC1Command::Execute(llvm::ArrayRef<llvm::Optional<llvm::StringRef> >, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >*, bool*) const (.part.0) (llvm/bin-trunk/bin/clang-11+0x2adffc6)
#28 0x000055f2cb1256cc clang::driver::Compilation::ExecuteCommand(clang::driver::Command const&, clang::driver::Command const*&) const (llvm/bin-trunk/bin/clang-11+0x2ab76cc)
#29 0x000055f2cb126006 clang::driver::Compilation::ExecuteJobs(clang::driver::JobList const&, llvm::SmallVectorImpl<std::pair<int, clang::driver::Command const*> >&) const (llvm/bin-trunk/bin/clang-11+0x2ab8006)
#30 0x000055f2cb12f3a9 clang::driver::Driver::ExecuteCompilation(clang::driver::Compilation&, llvm::SmallVectorImpl<std::pair<int, clang::driver::Command const*> >&) (llvm/bin-trunk/bin/clang-11+0x2ac13a9)
#31 0x000055f2c9219109 main (llvm/bin-trunk/bin/clang-11+0xbab109)
#32 0x00007ff9523511e3 __libc_start_main /build/glibc-t7JzpG/glibc-2.30/csu/../csu/libc-start.c:342:3
#33 0x000055f2c929616e _start (llvm/bin-trunk/bin/clang-11+0xc2816e)
clang-11: error: clang frontend command failed due to signal (use -v to see invocation)
clang version 11.0.0 (https://github.com/llvm/llvm-project.git 5cba1c6336c790877b631e4fcd3cb6e49452a00c)
Target: x86_64-unknown-linux-gnu
Thread model: posix

Reproducer:
extern int var_1, var_3;
extern short var_7, var_11;
extern char var_8;
extern unsigned long var_10;
extern int arr_148[];

long long int max(long long int a, long long int b) {
    return a > b ? a : b;
}

void test() {
  for (long a = 0; a < var_1; a++)
    for (char b = 0; b < 6; b += 2)
      for (char c = 0; c < (char)var_11; c = 1)
        #pragma clang loop vectorize_predicate(enable)
        for (char d(var_8); d < 5;
             d += var_10 / (max(492802768830814067LL, (long long)var_3) + var_7) + 1)
          arr_148[d] = 0;
}

Clang version:
clang version 11.0.0 (https://github.com/llvm/llvm-project.git 5cba1c6336c790877b631e4fcd3cb6e49452a00c)


---


### compiler : `llvm`
### title : `Clang produces wrong code with -O1 (Combine redundant instructions on function)`
### open_at : `2020-07-02T19:17:14Z`
### last_modified_date : `2020-07-04T15:25:09Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=46561
### status : `RESOLVED`
### tags : `miscompilation`
### component : `new bugs`
### version : `trunk`
### severity : `enhancement`
### contents :
opt-bisect limit points to Combine redundant instructions on function

>$ clang++ -w -O1 driver.cpp func.cpp && ./a.out 
42
>$ clang++ -w -O0 driver.cpp func.cpp && ./a.out 
0

Reproducer:
Func.cpp 
extern const bool tf_4_var_4;
extern const int tf_4_var_72;
extern unsigned long long int tf_4_var_124;
extern bool tf_4_array_3;
extern const bool tf_4_ptr_1;

void tf_4_foo() {
    if (~(tf_4_var_72 ? tf_4_ptr_1 * tf_4_array_3 ^ ~tf_4_var_4 : 0))
        tf_4_var_124 = 0;
}

Driver.cpp 
#include <stdio.h>
#include "init.h"

const bool tf_4_var_4 = true;
const int tf_4_var_72 = 2085646722;
unsigned long long int tf_4_var_124 = 42;
bool tf_4_array_3 = false;
const bool tf_4_ptr_1 = true;

extern void tf_4_foo();

int main() {
    tf_4_foo();
    printf("%llu\n", tf_4_var_124);
    return 0;
}

Init.h 
extern const bool tf_4_var_4;
extern const int tf_4_var_72;
extern unsigned long long int tf_4_var_124;
extern bool tf_4_array_3;
extern const bool tf_4_ptr_1;

Clang version:
clang version 11.0.0 (https://github.com/llvm/llvm-project.git 565e37c7702d181804c12d36b6010c513c9b3417)


---


### compiler : `llvm`
### title : `win32 std::current_exception miscompilation`
### open_at : `2020-07-04T18:23:04Z`
### last_modified_date : `2020-07-06T12:27:17Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=46584
### status : `NEW`
### tags : `miscompilation`
### component : `Backend: X86`
### version : `trunk`
### severity : `normal`
### contents :
This is probably oversimplified reproducer of Boost crash:  https://github.com/boostorg/thread/pull/320#issuecomment-653677766

#include <exception>

template <class T>
inline std::exception_ptr make_exception_ptr(T e)
{
    try {
        throw e;
    }
    catch(...) {
        return std::current_exception();
    }
}

struct X {};

int main()
{
    try
    {
        std::rethrow_exception(make_exception_ptr(X{}));
    }
    catch(X const&)
    {
    }
}

clang-cl /O2 /EHsc /DNDEBUG -m32 z.cpp


---


### compiler : `llvm`
### title : `[x86] Clang produces wrong code with -O1`
### open_at : `2020-07-04T19:45:19Z`
### last_modified_date : `2020-07-07T17:27:05Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=46586
### status : `RESOLVED`
### tags : `miscompilation`
### component : `Backend: X86`
### version : `trunk`
### severity : `enhancement`
### contents :
>$ clang++ -O1 func.cpp driver.cpp && ./a.out 
277562856
>$ clang++ -O0 func.cpp driver.cpp && ./a.out 
0
Reproducer:

//func.cpp
extern int var_22;
void test(unsigned a, unsigned short b, unsigned short c, signed char d,
          short e, unsigned char f, long long g,
          unsigned char h[2][20][22][21][15]) {
  for (bool i = 0; i < 1; i = f)
    for (char j = 0; j < 9; j = 75)
      for (bool k = 0; k < (bool)d /*1*/; k = 1)
        for (int l = 0; l < c /*45282*/; l = g /*1453005525*/)
#pragma clang loop interleave(enable)
          for (int m = 0; m < e + 31262 /*14*/; m += b - 55386 /*4*/)
            var_22 = h[i][j][7][l][m] % a;
}

//driver.cpp 
#include <stdio.h>

unsigned int var_0 = 1369684504U;
unsigned short var_2 = (unsigned short)55390;
unsigned short var_3 = (unsigned short)45282;
signed char var_4 = (signed char)115;
short var_5 = (short)-31248;
unsigned char var_7 = (unsigned char)161;
long long int var_9 = 7910119181202954965LL;
unsigned int var_22 = 3518480962U;
unsigned char arr_11 [2] [20] [22] [21] [15] ;

void test(unsigned int var_0, unsigned short var_2, unsigned short var_3, signed char var_4, short var_5, unsigned char var_7, long long int var_9, unsigned char arr_11 [2] [20] [22] [21] [15]);

int main() {
    test(var_0, var_2, var_3, var_4, var_5, var_7, var_9, arr_11);
    printf("%u\n", var_22);
}

Clang version:
clang version 11.0.0 (https://github.com/llvm/llvm-project.git 120c5f1057dc50229f73bc75bbabf4df6ee50fef)


---


### compiler : `llvm`
### title : `Incorrect mul foo, undef -> shl foo, undef`
### open_at : `2020-08-12T11:35:38Z`
### last_modified_date : `2020-10-24T01:33:04Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=47133
### status : `RESOLVED`
### tags : `miscompilation`
### component : `Scalar Optimizations`
### version : `trunk`
### severity : `normal`
### contents :
This is a recent regression in Transforms/InstCombine/mul.ll.
shl foo, undef is poison, so we can't introduce that.


define <2 x i32> @mulsub1_vec_nonuniform_undef(<2 x i32> %a0, <2 x i32> %a1) {
  %sub = sub <2 x i32> %a1, %a0
  %mul = mul <2 x i32> %sub, { 4294967292, undef }
  ret <2 x i32> %mul
}
=>
define <2 x i32> @mulsub1_vec_nonuniform_undef(<2 x i32> %a0, <2 x i32> %a1) {
  %sub.neg = sub <2 x i32> %a0, %a1
  %mul = shl <2 x i32> %sub.neg, { 2, undef }
  ret <2 x i32> %mul
}
Transformation doesn't verify!
ERROR: Target is more poisonous than source

Example:
<2 x i32> %a0 = < undef, undef >
<2 x i32> %a1 = < undef, undef >

Source:
<2 x i32> %sub = < undef, undef >
<2 x i32> %mul = < #x00000000 (0), #x00000000 (0) >

Target:
<2 x i32> %sub.neg = < #x00000000 (0), #x00000000 (0) >
<2 x i32> %mul = < #x00000000 (0), poison >
Source value: < #x00000000 (0), #x00000000 (0) >
Target value: < #x00000000 (0), poison >


Probably caused by https://github.com/llvm/llvm-project/commit/0c1c756a31536666a7b6f5bdb744dbce923a0c9e


https://web.ist.utl.pt/nuno.lopes/alive2/index.php?hash=b697cc49b7cc411c&test=Transforms%2FInstCombine%2Fmul.ll


---


### compiler : `llvm`
### title : `InstCombine: incorrect select operand simplification with undef`
### open_at : `2020-09-30T17:49:42Z`
### last_modified_date : `2020-10-24T01:33:04Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=47696
### status : `RESOLVED`
### tags : `miscompilation`
### component : `Scalar Optimizations`
### version : `trunk`
### severity : `normal`
### contents :
Test: Transforms/InstCombine/select-binop-cmp.ll

Seems to be a regression from https://reviews.llvm.org/D87480
The undef operand in the icmp needs to be fixed to 0 for the transformation to be correct. See here: https://alive2.llvm.org/ce/z/YYhL33


define <2 x i8> @select_xor_icmp_vec_undef(<2 x i8> %x, <2 x i8> %y, <2 x i8> %z) {
  %A = icmp eq <2 x i8> %x, { 0, undef }
  %B = xor <2 x i8> %x, %z
  %C = select <2 x i1> %A, <2 x i8> %B, <2 x i8> %y
  ret <2 x i8> %C
}
=>
define <2 x i8> @select_xor_icmp_vec_undef(<2 x i8> %x, <2 x i8> %y, <2 x i8> %z) {
  %A = icmp eq <2 x i8> %x, { 0, undef }
  %C = select <2 x i1> %A, <2 x i8> %z, <2 x i8> %y
  ret <2 x i8> %C
}
Transformation doesn't verify!
ERROR: Target's return value is more undefined

Example:
<2 x i8> %x = < poison, #x01 (1) >
<2 x i8> %y = < poison, #x00 (0) >
<2 x i8> %z = < poison, #x01 (1) >

Source:
<2 x i1> %A = < poison, any >
<2 x i8> %B = < poison, #x00 (0) >
<2 x i8> %C = < poison, #x00 (0) >

Target:
<2 x i1> %A = < poison, #x1 (1) >
<2 x i8> %C = < poison, #x01 (1) >
Source value: < poison, #x00 (0) >
Target value: < poison, #x01 (1) >


https://web.ist.utl.pt/nuno.lopes/alive2/index.php?hash=1546033e6d866cfc&test=Transforms%2FInstCombine%2Fselect-binop-cmp.ll


---


### compiler : `llvm`
### title : `MemCpyOpt: uses sext instead of zext for memcpy/memset size subtraction`
### open_at : `2020-09-30T18:43:39Z`
### last_modified_date : `2020-09-30T21:12:16Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=47697
### status : `NEW`
### tags : `miscompilation`
### component : `Scalar Optimizations`
### version : `trunk`
### severity : `normal`
### contents :
Test: Transforms/MemCpyOpt/memset-memcpy-redundant-memset.ll

MemCpyOpt sign-extends the difference between memcpy/memset sizes instead of zero-extending them.

https://alive2.llvm.org/ce/z/RgKeyt

----------------------------------------
define void @src(* %dst, * %src, i8 %dst_size, i8 %src_size, i8 %c) {
  memset * %dst align 1, i8 %c, i8 %dst_size
  memcpy * %dst align 1, * %src align 1, i8 %src_size
  ret void
}
=>
define void @src(* %dst, * %src, i8 %dst_size, i8 %src_size, i8 %c) {
  %1 = usub_sat i8 %dst_size, %src_size
  %2 = sext i8 %src_size to i64
  %3 = gep * %dst, 1 x i64 %2
  memset * %3 align 1, i8 %c, i8 %1
  memcpy * %dst align 1, * %src align 1, i8 %src_size
  ret void
}
Transformation doesn't verify!
ERROR: Source is more defined than target

Example:
* %dst = pointer(non-local, block_id=1, offset=96)
* %src = pointer(non-local, block_id=1, offset=9007199254741152)
i8 %dst_size = #x83 (131, -125)
i8 %src_size = #x82 (130, -126)
i8 %c = any

Source:

SOURCE MEMORY STATE
===================
NON-LOCAL BLOCKS:
Block 0 >	size: 0	align: 1	alloc type: 0
Block 1 >	size: 2305843009213693952	align: 2	alloc type: 0
Block 2 >	align: 2	alloc type: 0

Target:
i8 %1 = #x01 (1)
i64 %2 = #xffffffffffffff82 (18446744073709551490, -126)
* %3 = pointer(non-local, block_id=1, offset=-30)


Summary:
  0 correct transformations
  1 incorrect transformations
  0 Alive2 errors

https://web.ist.utl.pt/nuno.lopes/alive2/index.php?hash=1546033e6d866cfc&test=Transforms%2FMemCpyOpt%2Fmemset-memcpy-redundant-memset.ll


---


### compiler : `llvm`
### title : `Clang :: Sema/offsetof-64.c FAILs on 64-bit Sparc`
### open_at : `2020-10-02T12:25:49Z`
### last_modified_date : `2020-10-09T11:55:00Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=47710
### status : `NEW`
### tags : `miscompilation, regression`
### component : `Backend: Sparc`
### version : `trunk`
### severity : `normal`
### contents :
The Clang :: Sema/offsetof-64.c test FAILs on 64-bit Sparc (seen on both
sparcv9-sun-solaris2.11 and sparc64-unknown-linux-gnu):

Assertion failed: (Size == 0 || EltInfo.Width <= (uint64_t)(-1) / Size) && "Overflow in array type bit size evaluation", file /vol/llvm/src/llvm-project/dist/clang/lib/AST/ASTContext.cpp, line 1914

However, the same problem can be seen in a much reduced testcase (attached).

Compile with

$ clang -m64 -O3 -o o64 o64.c o64d.c && ./o64
Assertion failed: Width <= (uint64_t)(-1) / Size, file o64.c, line 7, function main
Abort (core dumped)

The test works with gcc and clang-9, while clang-10 and 11 show the same error.


---


### compiler : `llvm`
### title : `Miscompile with opt -loop-vectorize`
### open_at : `2020-10-07T00:36:56Z`
### last_modified_date : `2020-10-07T18:00:12Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=47751
### status : `RESOLVED`
### tags : `miscompilation`
### component : `Loop Optimizer`
### version : `trunk`
### severity : `normal`
### contents :
Created attachment 24028
Testcase

opt -loop-vectorize makes the attached testcase behave incorrectly.

The IR testcase is runnable: compile with llc, then run.  If it's built correctly, it should produce "3 1 2 4 5 6".  After vectorization, it instead produces "2 1 2 4 5 6".

I think the memcheck is getting emitted incorrectly?  It looks like the vectorized loop assumes the memory operations don't overlap.  There is in fact overlap at runtime; I guess the memcheck is supposed to detect that, but it looks like that detection is failing somehow.  At first glance, the check looks like it's in the right form, but maybe something is going wrong in SCEV.

Not sure when this regressed, but it looks like it's been this way for at least a year.

Not sure who to CC; has anyone looked at runtime checks recently?


---


### compiler : `llvm`
### title : `a bug report happenning in clang in loop vectorize(enable)`
### open_at : `2020-11-12T11:46:12Z`
### last_modified_date : `2020-11-12T12:01:55Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=48160
### status : `NEW`
### tags : `miscompilation`
### component : `C++2a`
### version : `10.0`
### severity : `enhancement`
### contents :
discription:
Two version of code should both use loop vectorize(enable), the result comes out that the first does while the second not.
They are compiled under the same environment and CXX_FLAG

version:
clang version:Apple clang version 12.0.0 (clang-1200.0.32.27)
Target: x86_64-apple-darwin19.6.0
Thread model: posix

compiler flag: 
-O2 -DNDEBUG -g -Xclang -fopenmp -std=gnu++2a -march=native 
-Rpass-missed=loop-vectorized(important to show the bug)

source code:
(There is a comparison, the first version produce wrong assembly, the second do not)
(The main function is at the end)

first version:
(T = float, matrix<T> = vector<vector<T>>)
template<typename T>
vector<T> operator*(const matrix<T> &left, const vector<T> &right) {
    vector<T> out(left.size());
    for (size_t i = 0; i < left.size(); i++) {
        T s(0);
#pragma clang loop vectorize(enable)
        for (size_t j = 0; j < right.size(); j++)
            s += left[i][j] * right[j];
        out[i] = s;
    }
    return out;
}

second version:(T and matrix<T> are the same)
template<typename T>
vector<T> operator*(const matrix<T> &left, const vector<T> &right) {
    vector<T> out(left.size());
    for (size_t i = 0; i < left.size(); i++)
#pragma clang loop vectorize(enable)
        for (size_t j = 0; j < right.size(); j++)
            out[i] += left[i][j] * right[j];
    return out;
}

error:

second version compiler waring:
warning: loop not vectorized: the optimizer was unable to perform the requested transformation; the transformation might be disabled or specified as part of an unsupported transformation ordering [-Wpass-failed=transform-warning]
        for (size_t j = 0; j < right.size(); j++)
        ^
now look at assembly, the first version's assembly is write with enough SIMD, the second do not!

test`operator+<float>:
    0x10eaa6010 <+0>:   pushq  %rbp
    0x10eaa6011 <+1>:   movq   %rsp, %rbp
    0x10eaa6014 <+4>:   pushq  %r15
    0x10eaa6016 <+6>:   pushq  %r14
    0x10eaa6018 <+8>:   pushq  %r13
    0x10eaa601a <+10>:  pushq  %r12
    0x10eaa601c <+12>:  pushq  %rbx
    0x10eaa601d <+13>:  subq   $0x18, %rsp
    0x10eaa6021 <+17>:  movq   (%rsi), %rcx
    0x10eaa6024 <+20>:  movq   0x8(%rsi), %rax
    0x10eaa6028 <+24>:  vxorps %xmm0, %xmm0, %xmm0
    0x10eaa602c <+28>:  vmovups %xmm0, (%rdi)
    0x10eaa6030 <+32>:  movq   %rdi, -0x30(%rbp)
    0x10eaa6034 <+36>:  movq   $0x0, 0x10(%rdi)
    0x10eaa603c <+44>:  movq   %rcx, -0x40(%rbp)
    0x10eaa6040 <+48>:  subq   %rcx, %rax
    0x10eaa6043 <+51>:  je     0x10eaa628b               ; <+635> at test.cpp
    0x10eaa6049 <+57>:  sarq   $0x3, %rax
    0x10eaa604d <+61>:  movabsq $-0x5555555555555555, %r14 ; imm = 0xAAAAAAAAAAAAAAAB 
    0x10eaa6057 <+71>:  imulq  %rax, %r14
    0x10eaa605b <+75>:  movq   %r14, %rax
    0x10eaa605e <+78>:  shrq   $0x3e, %rax
    0x10eaa6062 <+82>:  jne    0x10eaa62a1               ; <+657> at test.cpp
    0x10eaa6068 <+88>:  movq   %rdx, -0x38(%rbp)
    0x10eaa606c <+92>:  leaq   (,%r14,4), %r12
    0x10eaa6074 <+100>: movq   %r12, %rdi
    0x10eaa6077 <+103>: callq  0x10eaa6b14               ; symbol stub for: operator new(unsigned long)
    0x10eaa607c <+108>: movq   %rax, %r13
    0x10eaa607f <+111>: movq   -0x30(%rbp), %r15
    0x10eaa6083 <+115>: movq   %rax, (%r15)
    0x10eaa6086 <+118>: leaq   (%rax,%r14,4), %rbx
    0x10eaa608a <+122>: movq   %rbx, 0x10(%r15)
    0x10eaa608e <+126>: movq   %rax, %rdi
    0x10eaa6091 <+129>: movq   %r12, %rsi
    0x10eaa6094 <+132>: callq  0x10eaa6b1a               ; symbol stub for: __bzero
    0x10eaa6099 <+137>: movq   %rbx, 0x8(%r15)
    0x10eaa609d <+141>: movq   -0x38(%rbp), %rcx
    0x10eaa60a1 <+145>: movq   (%rcx), %rax
    0x10eaa60a4 <+148>: movq   0x8(%rcx), %r12
    0x10eaa60a8 <+152>: movq   %r12, %rdx
    0x10eaa60ab <+155>: subq   %rax, %rdx
    0x10eaa60ae <+158>: sarq   $0x2, %rdx
    0x10eaa60b2 <+162>: cmpq   $0x1, %rdx
    0x10eaa60b6 <+166>: movl   $0x1, %r15d
    0x10eaa60bc <+172>: cmovaq %rdx, %r15
    0x10eaa60c0 <+176>: leaq   -0x20(%r15), %r9
    0x10eaa60c4 <+180>: shrq   $0x5, %r9
    0x10eaa60c8 <+184>: leaq   0x1(%r9), %r8
    0x10eaa60cc <+188>: movq   %r15, %r11
    0x10eaa60cf <+191>: andq   $-0x20, %r11
    0x10eaa60d3 <+195>: movl   %r8d, %r10d
    0x10eaa60d6 <+198>: andl   $0x1, %r10d
    0x10eaa60da <+202>: andq   $-0x2, %r8
    0x10eaa60de <+206>: xorl   %edi, %edi
    0x10eaa60e0 <+208>: jmp    0x10eaa6103               ; <+243> at test.cpp
    0x10eaa60e2 <+210>: nopw   %cs:(%rax,%rax)
    0x10eaa60ec <+220>: nopl   (%rax)
    0x10eaa60f0 <+224>: vmovss %xmm0, (%r13,%rdi,4)
    0x10eaa60f7 <+231>: incq   %rdi
    0x10eaa60fa <+234>: cmpq   %r14, %rdi
    0x10eaa60fd <+237>: jae    0x10eaa628b               ; <+635> at test.cpp
    0x10eaa6103 <+243>: vxorps %xmm0, %xmm0, %xmm0
    0x10eaa6107 <+247>: cmpq   %rax, %r12
    0x10eaa610a <+250>: je     0x10eaa60f0               ; <+224> at test.cpp:19:16
    0x10eaa610c <+252>: leaq   (%rdi,%rdi,2), %rcx
    0x10eaa6110 <+256>: movq   -0x40(%rbp), %rsi
    0x10eaa6114 <+260>: movq   (%rsi,%rcx,8), %rsi
    0x10eaa6118 <+264>: cmpq   $0x1f, %r15
    0x10eaa611c <+268>: ja     0x10eaa6130               ; <+288> at test.cpp
    0x10eaa611e <+270>: vxorps %xmm0, %xmm0, %xmm0
    0x10eaa6122 <+274>: xorl   %ecx, %ecx
    0x10eaa6124 <+276>: jmp    0x10eaa6270               ; <+608> at test.cpp:18:18
    0x10eaa6129 <+281>: nopl   (%rax)
    0x10eaa6130 <+288>: vxorps %xmm0, %xmm0, %xmm0
    0x10eaa6134 <+292>: xorl   %ebx, %ebx
    0x10eaa6136 <+294>: vxorps %xmm1, %xmm1, %xmm1
    0x10eaa613a <+298>: vxorps %xmm2, %xmm2, %xmm2
    0x10eaa613e <+302>: vxorps %xmm3, %xmm3, %xmm3
    0x10eaa6142 <+306>: testq  %r9, %r9
    0x10eaa6145 <+309>: je     0x10eaa61f4               ; <+484> at test.cpp
    0x10eaa614b <+315>: movq   %r8, %rcx
    0x10eaa614e <+318>: nop    
->  0x10eaa6150 <+320>: vmovups (%rsi,%rbx,4), %ymm4
    0x10eaa6155 <+325>: vmovups 0x20(%rsi,%rbx,4), %ymm5
    0x10eaa615b <+331>: vmovups 0x40(%rsi,%rbx,4), %ymm6
    0x10eaa6161 <+337>: vmovups 0x60(%rsi,%rbx,4), %ymm7
    0x10eaa6167 <+343>: vmulps (%rax,%rbx,4), %ymm4, %ymm4
    0x10eaa616c <+348>: vaddps %ymm4, %ymm0, %ymm0
    0x10eaa6170 <+352>: vmulps 0x20(%rax,%rbx,4), %ymm5, %ymm4
    0x10eaa6176 <+358>: vaddps %ymm4, %ymm1, %ymm1
    0x10eaa617a <+362>: vmulps 0x40(%rax,%rbx,4), %ymm6, %ymm4
    0x10eaa6180 <+368>: vaddps %ymm4, %ymm2, %ymm2
    0x10eaa6184 <+372>: vmulps 0x60(%rax,%rbx,4), %ymm7, %ymm4
    0x10eaa618a <+378>: vaddps %ymm4, %ymm3, %ymm3
    0x10eaa618e <+382>: vmovups 0x80(%rsi,%rbx,4), %ymm4
    0x10eaa6197 <+391>: vmovups 0xa0(%rsi,%rbx,4), %ymm5
    0x10eaa61a0 <+400>: vmovups 0xc0(%rsi,%rbx,4), %ymm6
    0x10eaa61a9 <+409>: vmovups 0xe0(%rsi,%rbx,4), %ymm7
    0x10eaa61b2 <+418>: vmulps 0x80(%rax,%rbx,4), %ymm4, %ymm4
    0x10eaa61bb <+427>: vaddps %ymm4, %ymm0, %ymm0
    0x10eaa61bf <+431>: vmulps 0xa0(%rax,%rbx,4), %ymm5, %ymm4
    0x10eaa61c8 <+440>: vaddps %ymm4, %ymm1, %ymm1
    0x10eaa61cc <+444>: vmulps 0xc0(%rax,%rbx,4), %ymm6, %ymm4
    0x10eaa61d5 <+453>: vaddps %ymm4, %ymm2, %ymm2
    0x10eaa61d9 <+457>: vmulps 0xe0(%rax,%rbx,4), %ymm7, %ymm4
    0x10eaa61e2 <+466>: vaddps %ymm4, %ymm3, %ymm3
    0x10eaa61e6 <+470>: addq   $0x40, %rbx
    0x10eaa61ea <+474>: addq   $-0x2, %rcx
    0x10eaa61ee <+478>: jne    0x10eaa6150               ; <+320> at test.cpp:18:18
    0x10eaa61f4 <+484>: testq  %r10, %r10
    0x10eaa61f7 <+487>: je     0x10eaa6237               ; <+551> at test.cpp:17:9
    0x10eaa61f9 <+489>: vmovups (%rsi,%rbx,4), %ymm4
    0x10eaa61fe <+494>: vmovups 0x20(%rsi,%rbx,4), %ymm5
    0x10eaa6204 <+500>: vmovups 0x40(%rsi,%rbx,4), %ymm6
    0x10eaa620a <+506>: vmovups 0x60(%rsi,%rbx,4), %ymm7
    0x10eaa6210 <+512>: vmulps 0x60(%rax,%rbx,4), %ymm7, %ymm7
    0x10eaa6216 <+518>: vaddps %ymm7, %ymm3, %ymm3
    0x10eaa621a <+522>: vmulps 0x40(%rax,%rbx,4), %ymm6, %ymm6
    0x10eaa6220 <+528>: vaddps %ymm6, %ymm2, %ymm2
    0x10eaa6224 <+532>: vmulps 0x20(%rax,%rbx,4), %ymm5, %ymm5
    0x10eaa622a <+538>: vaddps %ymm5, %ymm1, %ymm1
    0x10eaa622e <+542>: vmulps (%rax,%rbx,4), %ymm4, %ymm4
    0x10eaa6233 <+547>: vaddps %ymm4, %ymm0, %ymm0
    0x10eaa6237 <+551>: vaddps %ymm0, %ymm1, %ymm0
    0x10eaa623b <+555>: vaddps %ymm0, %ymm2, %ymm0
    0x10eaa623f <+559>: vaddps %ymm0, %ymm3, %ymm0
    0x10eaa6243 <+563>: vextractf128 $0x1, %ymm0, %xmm1
    0x10eaa6249 <+569>: vaddps %xmm1, %xmm0, %xmm0
    0x10eaa624d <+573>: vpermilpd $0x1, %xmm0, %xmm1        ; xmm1 = xmm0[1,0] 
    0x10eaa6253 <+579>: vaddps %xmm1, %xmm0, %xmm0
    0x10eaa6257 <+583>: vmovshdup %xmm0, %xmm1              ; xmm1 = xmm0[1,1,3,3] 
    0x10eaa625b <+587>: vaddss %xmm1, %xmm0, %xmm0
    0x10eaa625f <+591>: movq   %r11, %rcx
    0x10eaa6262 <+594>: cmpq   %r11, %r15
    0x10eaa6265 <+597>: je     0x10eaa60f0               ; <+224> at test.cpp:19:16
    0x10eaa626b <+603>: nopl   (%rax,%rax)
    0x10eaa6270 <+608>: vmovss (%rsi,%rcx,4), %xmm1      ; xmm1 = mem[0],zero,zero,zero 
    0x10eaa6275 <+613>: vmulss (%rax,%rcx,4), %xmm1, %xmm1
    0x10eaa627a <+618>: vaddss %xmm1, %xmm0, %xmm0
    0x10eaa627e <+622>: incq   %rcx
    0x10eaa6281 <+625>: cmpq   %rdx, %rcx
    0x10eaa6284 <+628>: jb     0x10eaa6270               ; <+608> at test.cpp:18:18
    0x10eaa6286 <+630>: jmp    0x10eaa60f0               ; <+224> at test.cpp:19:16
    0x10eaa628b <+635>: movq   -0x30(%rbp), %rax
    0x10eaa628f <+639>: addq   $0x18, %rsp
    0x10eaa6293 <+643>: popq   %rbx
    0x10eaa6294 <+644>: popq   %r12
    0x10eaa6296 <+646>: popq   %r13
    0x10eaa6298 <+648>: popq   %r14
    0x10eaa629a <+650>: popq   %r15
    0x10eaa629c <+652>: popq   %rbp
    0x10eaa629d <+653>: vzeroupper 
    0x10eaa62a0 <+656>: retq   
    0x10eaa62a1 <+657>: movq   -0x30(%rbp), %rdi
    0x10eaa62a5 <+661>: callq  0x10eaa6aa8               ; symbol stub for: std::__1::__vector_base_common<true>::__throw_length_error() const
    0x10eaa62aa <+666>: ud2    
    0x10eaa62ac <+668>: movq   %rax, %rbx
    0x10eaa62af <+671>: movq   -0x30(%rbp), %rax
    0x10eaa62b3 <+675>: movq   (%rax), %rdi
    0x10eaa62b6 <+678>: testq  %rdi, %rdi
    0x10eaa62b9 <+681>: je     0x10eaa62c8               ; <+696> at new
    0x10eaa62bb <+683>: movq   -0x30(%rbp), %rax
    0x10eaa62bf <+687>: movq   %rdi, 0x8(%rax)
    0x10eaa62c3 <+691>: callq  0x10eaa6b0e               ; symbol stub for: operator delete(void*)
    0x10eaa62c8 <+696>: movq   %rbx, %rdi
    0x10eaa62cb <+699>: callq  0x10eaa6aa2               ; symbol stub for: _Unwind_Resume
    0x10eaa62d0 <+704>: ud2    
    0x10eaa62d2 <+706>: nopw   %cs:(%rax,%rax)
    0x10eaa62dc <+716>: nopl   (%rax)


test`operator+<float>:
    0x10de2f1c0 <+0>:   pushq  %rbp
    0x10de2f1c1 <+1>:   movq   %rsp, %rbp
    0x10de2f1c4 <+4>:   pushq  %r15
    0x10de2f1c6 <+6>:   pushq  %r14
    0x10de2f1c8 <+8>:   pushq  %r13
    0x10de2f1ca <+10>:  pushq  %r12
    0x10de2f1cc <+12>:  pushq  %rbx
    0x10de2f1cd <+13>:  subq   $0x18, %rsp
    0x10de2f1d1 <+17>:  movq   %rdi, %r14
    0x10de2f1d4 <+20>:  movq   (%rsi), %r13
    0x10de2f1d7 <+23>:  movq   0x8(%rsi), %rax
    0x10de2f1db <+27>:  vxorps %xmm0, %xmm0, %xmm0
    0x10de2f1df <+31>:  vmovups %xmm0, (%rdi)
    0x10de2f1e3 <+35>:  movq   $0x0, 0x10(%rdi)
    0x10de2f1eb <+43>:  subq   %r13, %rax
    0x10de2f1ee <+46>:  je     0x10de2f29d               ; <+221> at test.cpp:20:1
    0x10de2f1f4 <+52>:  sarq   $0x3, %rax
    0x10de2f1f8 <+56>:  movabsq $-0x5555555555555555, %r15 ; imm = 0xAAAAAAAAAAAAAAAB 
    0x10de2f202 <+66>:  imulq  %rax, %r15
    0x10de2f206 <+70>:  movq   %r15, %rax
    0x10de2f209 <+73>:  shrq   $0x3e, %rax
    0x10de2f20d <+77>:  jne    0x10de2f2af               ; <+239> [inlined] std::__1::vector<float, std::__1::allocator<float> >::__vallocate(unsigned long) at vector:1125
    0x10de2f213 <+83>:  movq   %rdx, -0x38(%rbp)
    0x10de2f217 <+87>:  leaq   (,%r15,4), %rdi
    0x10de2f21f <+95>:  movq   %rdi, -0x30(%rbp)
    0x10de2f223 <+99>:  callq  0x10de2fb14               ; symbol stub for: operator new(unsigned long)
    0x10de2f228 <+104>: movq   %rax, %rbx
    0x10de2f22b <+107>: movq   %rax, (%r14)
    0x10de2f22e <+110>: leaq   (%rax,%r15,4), %r12
    0x10de2f232 <+114>: movq   %r12, 0x10(%r14)
    0x10de2f236 <+118>: movq   %rax, %rdi
    0x10de2f239 <+121>: movq   -0x30(%rbp), %rsi
    0x10de2f23d <+125>: callq  0x10de2fb1a               ; symbol stub for: __bzero
    0x10de2f242 <+130>: movq   %r12, 0x8(%r14)
    0x10de2f246 <+134>: movq   -0x38(%rbp), %rcx
    0x10de2f24a <+138>: movq   (%rcx), %rax
    0x10de2f24d <+141>: movq   0x8(%rcx), %r8
    0x10de2f251 <+145>: movq   %r8, %rdx
    0x10de2f254 <+148>: subq   %rax, %rdx
    0x10de2f257 <+151>: sarq   $0x2, %rdx
    0x10de2f25b <+155>: xorl   %esi, %esi
    0x10de2f25d <+157>: jmp    0x10de2f268               ; <+168> at test.cpp
    0x10de2f25f <+159>: nop    
    0x10de2f260 <+160>: incq   %rsi
    0x10de2f263 <+163>: cmpq   %r15, %rsi
    0x10de2f266 <+166>: jae    0x10de2f29d               ; <+221> at test.cpp:20:1
    0x10de2f268 <+168>: cmpq   %rax, %r8
    0x10de2f26b <+171>: je     0x10de2f260               ; <+160> at test.cpp:14:42
    0x10de2f26d <+173>: leaq   (%rsi,%rsi,2), %rcx
    0x10de2f271 <+177>: movq   (%r13,%rcx,8), %rdi
->  0x10de2f276 <+182>: vmovss (%rbx,%rsi,4), %xmm0      ; xmm0 = mem[0],zero,zero,zero 
    0x10de2f27b <+187>: xorl   %ecx, %ecx
    0x10de2f27d <+189>: nopl   (%rax)
    0x10de2f280 <+192>: vmovss (%rdi,%rcx,4), %xmm1      ; xmm1 = mem[0],zero,zero,zero 
    0x10de2f285 <+197>: vmulss (%rax,%rcx,4), %xmm1, %xmm1
    0x10de2f28a <+202>: vaddss %xmm0, %xmm1, %xmm0
    0x10de2f28e <+206>: vmovss %xmm0, (%rbx,%rsi,4)
    0x10de2f293 <+211>: incq   %rcx
    0x10de2f296 <+214>: cmpq   %rdx, %rcx
    0x10de2f299 <+217>: jb     0x10de2f280               ; <+192> at test.cpp:17:23
    0x10de2f29b <+219>: jmp    0x10de2f260               ; <+160> at test.cpp:14:42
    0x10de2f29d <+221>: movq   %r14, %rax
    0x10de2f2a0 <+224>: addq   $0x18, %rsp
    0x10de2f2a4 <+228>: popq   %rbx
    0x10de2f2a5 <+229>: popq   %r12
    0x10de2f2a7 <+231>: popq   %r13
    0x10de2f2a9 <+233>: popq   %r14
    0x10de2f2ab <+235>: popq   %r15
    0x10de2f2ad <+237>: popq   %rbp
    0x10de2f2ae <+238>: retq   
    0x10de2f2af <+239>: movq   %r14, %rdi
    0x10de2f2b2 <+242>: callq  0x10de2faa8               ; symbol stub for: std::__1::__vector_base_common<true>::__throw_length_error() const
    0x10de2f2b7 <+247>: ud2    
    0x10de2f2b9 <+249>: movq   %rax, %rbx
    0x10de2f2bc <+252>: movq   (%r14), %rdi
    0x10de2f2bf <+255>: testq  %rdi, %rdi
    0x10de2f2c2 <+258>: je     0x10de2f2cd               ; <+269> at new
    0x10de2f2c4 <+260>: movq   %rdi, 0x8(%r14)
    0x10de2f2c8 <+264>: callq  0x10de2fb0e               ; symbol stub for: operator delete(void*)
    0x10de2f2cd <+269>: movq   %rbx, %rdi
    0x10de2f2d0 <+272>: callq  0x10de2faa2               ; symbol stub for: _Unwind_Resume
    0x10de2f2d5 <+277>: ud2    
    0x10de2f2d7 <+279>: nopw   (%rax,%rax)

main:
int main(){
    using T = float;
    constexpr size_t size = 1000;
    matrix<T> to_decompose(size, vector<T>(size));
    vector<T> to_solve(size);
    /*use random to generate to_solve, uncomment this if you want to
    std::random_device rd;  //Will be used to obtain a seed for the random number engine
    std::mt19937 gen(rd()); //Standard mersenne_twister_engine seeded with rd()
    std::uniform_real_distribution<> dis(-1.0, 1.0);

    for (size_t i = 0; i < size; ++i){
        if (i != 0)
            to_decompose[i][i - 1] = to_decompose[i - 1][i]= 1;
        to_decompose[i][i] = 10;
    }

    for (size_t i = 0; i < size; ++i) {
        // Use dis to transform the random unsigned int generated by gen into a
        // T in [-1, 1). Each call to dis(gen) generates a new random T
        to_solve[i] = dis(gen);
    }
    */
    solved = to_decompose * to_solve;
    cout << solved[0] << endl;
}


---


### compiler : `llvm`
### title : `DSE incorrectly removes store in function that only triggers UB in one branch`
### open_at : `2020-12-15T19:33:03Z`
### last_modified_date : `2020-12-15T23:22:20Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=48521
### status : `RESOLVED`
### tags : `miscompilation`
### component : `Scalar Optimizations`
### version : `trunk`
### severity : `normal`
### contents :
Test: Transforms/DeadStoreElimination/MSSA/out-of-bounds-stores.ll
Summary: Once DSE finds a store that is OOB, and therefore the function triggers UB, it removes all stores. However, in the program below OOB only happens if %c = true.
When %c=false there's no UB and therefore the store cannot be removed.


define i32 @test_out_of_bounds_store_nonlocal(i1 %c) {
%0:
  %d = alloca i64 4, align 4
  br label %for.body

%for.body:
  %arrayidx = gep inbounds * %d, 4 x i64 0, 4 x i64 0
  store i32 10, * %arrayidx, align 4
  br label %for.inc

%for.inc:
  br i1 %c, label %for.body.1, label %for.end

%for.body.1:
  %arrayidx.1 = gep inbounds * %d, 4 x i64 0, 4 x i64 1
  store i32 20, * %arrayidx.1, align 4
  ret i32 1

%for.end:
  %arrayidx1 = gep inbounds * %d, 4 x i64 0, 4 x i64 0
  %lv1 = load i32, * %arrayidx1, align 4
  call void @use(i32 %lv1)
  ret i32 0
}
=>
define i32 @test_out_of_bounds_store_nonlocal(i1 %c) {
%0:
  %d = alloca i64 4, align 4
  br label %for.body

%for.body:
  br label %for.inc

%for.inc:
  br i1 %c, label %for.body.1, label %for.end

%for.body.1:
  ret i32 1

%for.end:
  %arrayidx1 = gep inbounds * %d, 4 x i64 0, 4 x i64 0
  %lv1 = load i32, * %arrayidx1, align 4
  call void @use(i32 %lv1)
  ret i32 0
}
Transformation doesn't verify!
ERROR: Source is more defined than target

Example:
i1 %c = #x0 (0)

Source:
* %d = pointer(local, block_id=2, offset=0)
* %arrayidx = pointer(local, block_id=2, offset=0)
* %arrayidx.1 = pointer(local, block_id=2, offset=4)
* %arrayidx1 = pointer(local, block_id=2, offset=0)
i32 %lv1 = #x0000000a (10)

Target:
* %d = pointer(local, block_id=2, offset=0)
* %arrayidx1 = pointer(local, block_id=2, offset=0)
i32 %lv1 = poison


https://web.ist.utl.pt/nuno.lopes/alive2/index.php?hash=4b7777d913fed80c&test=Transforms%2FDeadStoreElimination%2FMSSA%2Fout-of-bounds-stores.ll


---


### compiler : `llvm`
### title : `Miscompilation of va_start on Windows MSYS2`
### open_at : `2020-12-29T19:51:38Z`
### last_modified_date : `2021-01-05T18:42:41Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=48624
### status : `NEW`
### tags : `miscompilation`
### component : `C`
### version : `11.0`
### severity : `release blocker`
### contents :
Not sure if this is a Clang bug or a MSYS2 bug, so I am filing it here.


However, since the problem doesn't affect GCC which links to the same libc, I am assuming it is something fishy with clang.

Compile this rather simple C program on MSYS2:


#include <stdarg.h>
#include <stdio.h>

void my_printf(const char *fmt, ...)
{
    va_list ap;
    va_start(ap, fmt);
    vprintf(fmt, ap);
    va_end(ap);
}

int main(void)
{
    my_printf("%s\n", "Hello, world!");
}

***@**** MSYS2 ~
$ clang --version
clang version 11.0.0 (https://github.com/msys2/MSYS2-packages a5a028a0811f03c8f9697bf80c2e28111628ffff)
Target: x86_64-pc-windows-msys
Thread model: posix
InstalledDir: /usr/bin

***@**** MSYS2 ~
$ clang test.c; ./a.exe
0@

***@**** MSYS2 ~
$./a.exe | hexdump -C
00000000  04 30 40 0a                                       |.0@.|
00000004

In case you are wondering, GCC correctly compiles this; my libc isn't broken.

***@**** MSYS2 ~
$ gcc --version
gcc (GCC) 10.2.0
Copyright (C) 2020 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

***@**** MSYS2 ~
$ gcc test.c; ./a.exe
Hello, world!

It doesn't matter if optimizations are on or off, it still prints 0x04 0x30 0x40.

mingw-w64 clang compiles it fine, though. 

Doing some more investigation now, although I am not familiar with the calling convention.


---


### compiler : `llvm`
### title : `Inline assembly allocated register clash with multi-register constraints`
### open_at : `2021-01-24T09:56:46Z`
### last_modified_date : `2021-01-24T22:00:46Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=48862
### status : `NEW`
### tags : `miscompilation`
### component : `Register Allocator`
### version : `trunk`
### severity : `enhancement`
### contents :
Consider the following sample program (targeting Linux/x86-64):

#include <stdio.h>
#include <stdlib.h>
int main(int argc, char *argv[])
{
  unsigned arg1 = strtoul(argv[1], NULL, 0);
  unsigned arg2 = strtoul(argv[2], NULL, 0);
  asm(
    "mov %[arg1], %%ecx\n\t"
    "add %[arg2], %[arg1]\n\t"
    "add %[arg2], %%ecx\n\t"
    "xchg %%ecx, %[arg2]"
    : [arg1] "+&abdSD" (arg1), [arg2] "+&abdSD" (arg2)
    :
    : "cc", "ecx");
  printf("%u %u\n", arg1, arg2);
}

(xchg is used just for easy grepping of compiled instructions in listing. This is just an example crafted to reproduce the issue, far from real code, but clear enough.)

With GCC, it works as expected - different registers are assigned to arg1 and arg2, for example:

    11bf:       e8 cc fe ff ff          callq  1090 <strtoul@plt>
    11c4:       89 da                   mov    %ebx,%edx
    11c6:       89 d1                   mov    %edx,%ecx
    11c8:       01 c2                   add    %eax,%edx
    11ca:       01 c1                   add    %eax,%ecx
    11cc:       91                      xchg   %eax,%ecx

(so, arg1 in edx, arg2 in eax)

But, compiling with Clang (confirmed on all from 6.0 to trunk) results in assigning the same register for arg1 and arg2:

  401174:       e8 d7 fe ff ff          callq  401050 <strtoul@plt>
  401179:       44 89 f0                mov    %r14d,%eax ; <--
  40117c:       89 c1                   mov    %eax,%ecx
  40117e:       01 c0                   add    %eax,%eax ; <-- so, arg1 and arg2 both in eax
  401180:       01 c1                   add    %eax,%ecx
  401182:       91                      xchg   %eax,%ecx

The issue remains with multiple variations as e.g.: + instead of +& in constraint strings; numeric forms like %0 to address operands; replacing xchg with another rare instruction; and so on.

The issue is of importance on x86 because a lots of its instructions are allowing only fixed registers, but a desire to alleviate allocation causes constraint suggestion as explicit list except 1-2 reserved ones.

A workaround is accessible to use generic constraints like 'r' while marking all disallowed registers as clobbered, but Iʼm uncertain whether it wonʼt explode with "rm" or analogs.

Discussed also at https://stackoverflow.com/q/65644864 (with an explicit suggestion this is really a bug).


---


### compiler : `llvm`
### title : `Incorrect swap of fptrunc with fast-math instructions`
### open_at : `2021-02-07T20:30:30Z`
### last_modified_date : `2021-05-31T11:20:30Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=49080
### status : `NEW`
### tags : `miscompilation`
### component : `Scalar Optimizations`
### version : `trunk`
### severity : `normal`
### contents :
See the example below where fptrunc & fabs are swapped. The issue is that fabs has the nninf tag, which becomes poison because its input is inf.

Two solutions come to mind: drop nninf from fabs in the solution, or add fast-math flags to fptrunc.


define half @test_shrink_intrin_fabs_fast_double_src(float %D) {
  %E = fabs fast float %D
  %F = fptrunc float %E to half
  ret half %F
}
=>
define half @test_shrink_intrin_fabs_fast_double_src(float %D) {
  %1 = fptrunc float %D to half
  %F = fabs fast half %1
  ret half %F
}
Transformation doesn't verify!
ERROR: Target is more poisonous than source

Example:
float %D = #x477ff080 (65520.5)

Source:
float %E = #x477ff080 (65520.5)
half %F = #x7c00 (+oo)

Target:
half %1 = #x7c00 (+oo)
half %F = poison
Source value: #x7c00 (+oo)
Target value: poison


File: llvm/test/Transforms/InstCombine/double-float-shrink-2.ll
A similar test also fails in Transforms/InstCombine/fpcast.ll (test4-fast)


---


### compiler : `llvm`
### title : `[InstCombine] Incorrect propagation of nsz from fneg to fdiv`
### open_at : `2021-03-19T18:05:31Z`
### last_modified_date : `2021-06-10T18:26:13Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=49654
### status : `RESOLVED`
### tags : `miscompilation`
### component : `Scalar Optimizations`
### version : `trunk`
### severity : `normal`
### contents :
This is from Transforms/InstCombine/fneg.ll, reduced from fast to just nsz.
The issue is that the original fdiv has no nsz but the optimized one has. In this case, nsz can be propagated, but not added (even if fneg is nsz).


define float @fdiv_op0_constant_fneg_fmf(float %x) {
  %d = fdiv float 42.000000, %x
  %r = fneg nsz float %d
  ret float %r
}
=>
define float @fdiv_op0_constant_fneg_fmf(float %x) {
  %r = fdiv nsz float -42.000000, %x
  ret float %r
}
Transformation doesn't verify!
ERROR: Value mismatch

Example:
float %x = #x80000000 (-0.0)

Source:
float %d = #xff800000 (-oo)
float %r = #x7f800000 (+oo)

Target:
float %r = #xff800000 (-oo)
Source value: #x7f800000 (+oo)
Target value: #xff800000 (-oo)


---


### compiler : `llvm`
### title : `InstSimplify: incorrect fold of pointer comparison between globals`
### open_at : `2021-05-03T17:41:55Z`
### last_modified_date : `2021-05-09T12:18:15Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=50208
### status : `NEW`
### tags : `miscompilation`
### component : `Scalar Optimizations`
### version : `trunk`
### severity : `normal`
### contents :
test: Transforms/InstSimplify/ConstProp/icmp-null.ll
The transformation below is only correct if the gep is over i8*, and not with non-byte-sized types. This is correct: https://alive2.llvm.org/ce/z/S_TsHW

----------------------------------------
@g2 = global 4 bytes, align 4
@g = global 8 bytes, align 4

define i1 @null_gep_ne_global() {
  %__constexpr_0 = ptrtoint * @g2 to i64
  %gep = gep * null, 8 x i64 %__constexpr_0  ; <-- notice the 8 x
  %cmp = icmp ne * %gep, @g
  ret i1 %cmp
}
=>
@g2 = global 4 bytes, align 4
@g = global 8 bytes, align 4

define i1 @null_gep_ne_global() {
  ret i1 1
}
Transformation doesn't verify!

ERROR: Value mismatch

Example:

Source:
i64 %__constexpr_0 = #x924925b6db6f5564 (10540997870133138788, -7905746203576412828)
* %gep = pointer(non-local, block_id=0, offset=-7905737407482647776)
i1 %cmp = #x0 (0)

SOURCE MEMORY STATE
===================
NON-LOCAL BLOCKS:
Block 0 >       size: 0 align: 1        alloc type: 0   address: 0
Block 1 >       size: 4 align: 4        alloc type: 0   address: 10540997870133138788
Block 2 >       size: 8 align: 4        alloc type: 0   address: 10541006666226903840

Target:
Source value: #x0 (0)
Target value: #x1 (1)


---


### compiler : `llvm`
### title : `ConstraintElimination: incorrect fold of pointer comparison`
### open_at : `2021-05-09T11:55:07Z`
### last_modified_date : `2021-05-09T13:28:41Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=50280
### status : `NEW`
### tags : `miscompilation`
### component : `Scalar Optimizations`
### version : `trunk`
### severity : `normal`
### contents :
Test: Transforms/ConstraintElimination/gep-arithmetic.ll

The optimization below is incorrect as it misses one case:
lower < src.end < src < upper < src.step


define i4 @ptr_N_signed_positive_assume(* %src, * %lower, * %upper, i16 %N, i16 %step) {
%entry:
  %src.end = gep inbounds * %src, 1 x i16 %N
  %cmp.src.start = icmp ult * %src, %lower
  %cmp.src.end = icmp uge * %src.end, %upper
  %N.neg = icmp slt i16 %N, 0
  assume i1 %N.neg
  %or.precond.0 = or i1 %cmp.src.start, %cmp.src.end
  br i1 %or.precond.0, label %trap.bb, label %step.check

%step.check:
  %step.pos = icmp uge i16 %step, 0
  %step.ult.N = icmp ult i16 %step, %N
  %and.step = and i1 %step.pos, %step.ult.N
  br i1 %and.step, label %ptr.check, label %exit

%ptr.check:
  %src.step = gep inbounds * %src, 1 x i16 %step
  %cmp.step.start = icmp ult * %src.step, %lower
  %cmp.step.end = icmp uge * %src.step, %upper
  %or.check = or i1 %cmp.step.start, %cmp.step.end
  br i1 %or.check, label %trap.bb, label %exit

%exit:
  ret i4 3

%trap.bb:
  ret i4 2
}
=>
define i4 @ptr_N_signed_positive_assume(* %src, * %lower, * %upper, i16 %N, i16 %step) {
%entry:
  %src.end = gep inbounds * %src, 1 x i16 %N
  %cmp.src.start = icmp ult * %src, %lower
  %cmp.src.end = icmp uge * %src.end, %upper
  %N.neg = icmp slt i16 %N, 0
  assume i1 %N.neg
  %or.precond.0 = or i1 %cmp.src.start, %cmp.src.end
  br i1 %or.precond.0, label %trap.bb, label %step.check

%step.check:
  %step.pos = icmp uge i16 %step, 0
  %step.ult.N = icmp ult i16 %step, %N
  %and.step = and i1 %step.pos, %step.ult.N
  br i1 %and.step, label %ptr.check, label %exit

%ptr.check:
  %src.step = gep inbounds * %src, 1 x i16 %step
  %cmp.step.start = icmp ult * %src.step, %lower
  %cmp.step.end = icmp uge * %src.step, %upper
  %or.check = or i1 0, 0
  br i1 %or.check, label %trap.bb, label %exit

%exit:
  ret i4 3

%trap.bb:
  ret i4 2
}
Transformation doesn't verify!
ERROR: Value mismatch

Example:
* %src = pointer(non-local, block_id=1, offset=229377)
* %lower = pointer(non-local, block_id=0, offset=-393217)
* %upper = pointer(non-local, block_id=0, offset=-419450)
i16 %N = #x9014 (36884, -28652)
i16 %step = #x100d (4109)

Source:
* %src.end = pointer(non-local, block_id=1, offset=200725)
i1 %cmp.src.start = #x0 (0)
i1 %cmp.src.end = #x0 (0)
i1 %N.neg = #x1 (1)
i1 %or.precond.0 = #x0 (0)
i1 %step.pos = #x1 (1)
i1 %step.ult.N = #x1 (1)
i1 %and.step = #x1 (1)
* %src.step = pointer(non-local, block_id=1, offset=233486)
i1 %cmp.step.start = #x0 (0)
i1 %cmp.step.end = #x1 (1)
i1 %or.check = #x1 (1)

SOURCE MEMORY STATE
===================
NON-LOCAL BLOCKS:
Block 0 >	size: 0	align: 1	alloc type: 0	address: 0
Block 1 >	size: 524288	align: 4	alloc type: 0	address: 425988
Block 2 >	size: 100654	align: 8589934592	alloc type: 0	address: 263504
Block 3 >	size: 230832	align: 8589934592	alloc type: 0	address: 29184

Target:
* %src.end = pointer(non-local, block_id=1, offset=200725)
i1 %cmp.src.start = #x0 (0)
i1 %cmp.src.end = #x0 (0)
i1 %N.neg = #x1 (1)
i1 %or.precond.0 = #x0 (0)
i1 %step.pos = #x1 (1)
i1 %step.ult.N = #x1 (1)
i1 %and.step = #x1 (1)
* %src.step = pointer(non-local, block_id=1, offset=233486)
i1 %cmp.step.start = #x0 (0)
i1 %cmp.step.end = #x1 (1)
i1 %or.check = #x0 (0)
Source value: #x2 (2)
Target value: #x3 (3)


---


### compiler : `llvm`
### title : `InstCombine: incorrect select fast-math folds`
### open_at : `2021-05-09T12:32:01Z`
### last_modified_date : `2021-05-09T15:41:32Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=50281
### status : `NEW`
### tags : `miscompilation`
### component : `Scalar Optimizations`
### version : `trunk`
### severity : `normal`
### contents :
Alive2 reports a few incorrect optimizations around select w/ fast-math in Transforms/InstCombine/minmax-fp.ll:

-----------------------------------------

nsz allows the output to be +0/-0 non-deterministically. In this example, the source always returns +0 and the target may return +0 or -0. The select in src would need nsz as well:

define <2 x float> @fsub_fmax(<2 x float> %x, <2 x float> %y) {
  %n1 = fsub <2 x float> { -0.000000, -0.000000 }, %x
  %n2 = fsub <2 x float> { -0.000000, -0.000000 }, %y
  %cond = fcmp nnan nsz uge <2 x float> %n1, %n2
  %max = select <2 x i1> %cond, <2 x float> %n1, <2 x float> %n2
  ret <2 x float> %max
}
=>
define <2 x float> @fsub_fmax(<2 x float> %x, <2 x float> %y) {
  %cond.inv = fcmp nnan nsz ogt <2 x float> %x, %y
  %1 = select nnan nsz <2 x i1> %cond.inv, <2 x float> %y, <2 x float> %x
  %max = fneg <2 x float> %1
  ret <2 x float> %max
}
Transformation doesn't verify!

ERROR: Value mismatch

Example:
<2 x float> %x = < poison, #x80000000 (-0.0) >
<2 x float> %y = < poison, #x00800001 (0.000000000000?) >

Source:
<2 x float> %n1 = < poison, #x00000000 (+0.0) >
<2 x float> %n2 = < poison, #x80800001 (-0.000000000000?) >
<2 x i1> %cond = < poison, #x1 (1) >
<2 x float> %max = < poison, #x00000000 (+0.0) >

Target:
<2 x i1> %cond.inv = < poison, #x0 (0) >
<2 x float> %1 = < poison, #x00000000 (+0.0) >
<2 x float> %max = < poison, #x80000000 (-0.0) >
Source value: < poison, #x00000000 (+0.0) >
Target value: < poison, #x80000000 (-0.0) >


-----------------------------

select nnan only applies to the chosen operand (?). If that's the case then the optimization below isn't correct for a NaN input. If nnan applies to both select operands, then fptrunc_select_true_val_extra_use in fptrunc.ll is incorrect.

define float @maxnum_ogt_fmf_on_select(float %a, float %b) {
  %cond = fcmp ogt float %a, %b
  %f = select nnan nsz i1 %cond, float %a, float %b
  ret float %f
}
=>
define float @maxnum_ogt_fmf_on_select(float %a, float %b) {
  %1 = fmax nnan nsz float %a, %b
  ret float %1
}
Transformation doesn't verify!

ERROR: Target is more poisonous than source

Example:
float %a = NaN
float %b = #x20008b45 (0.000000000000?)

Source:
i1 %cond = #x0 (0)
float %f = #x20008b45 (0.000000000000?)

Target:
float %1 = poison
Source value: #x20008b45 (0.000000000000?)
Target value: poison


---


### compiler : `llvm`
### title : `wrong code for -O of attribute(const or pure) for overriden virtual base class method`
### open_at : `2021-06-25T15:24:40Z`
### last_modified_date : `2021-06-25T17:03:49Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=50866
### status : `NEW`
### tags : `miscompilation`
### component : `new bugs`
### version : `trunk`
### severity : `normal`
### contents :
#include <iostream>
struct A {
  virtual int c() __attribute__ ((const));
  virtual int p() __attribute__ ((pure ));
};
struct B : public A {
  virtual int c() override;
  virtual int p() override;
};
int A::c() { std::cout << "A::c()\n"; return 0x01; }
int A::p() { std::cout << "A::p()\n"; return 0x04; }
int B::c() { std::cout << "B::c()\n"; return 0x10; }
int B::p() { std::cout << "B::p()\n"; return 0x40; }
int main() {
  B b;
  A &a(b);
  return a.c() + a.c() + a.p() + a.p(); // 160==0xa0==0x10+0x10+0x40+0x40
}
-------------------------------------------------------------------------
for i in g++ clang++;do $i -o virtone virtone.C -Wall -g -O;./virtone;echo $?;done
-------------------------------------------------------------------------
PASS: gcc-11.1.1-3.fc34.x86_64
B::c()
B::c()
B::p()
B::p()
160
-------------------------------------------------------------------------
FAIL: clang-12.0.0-2.fc34.x86_64
FAIL: clang version 13.0.0 91053e327ccd27cb1ee66a7d4954d456ceeed5f6
      Target: x86_64-unknown-linux-gnu
B::c()
B::p()
160
-------------------------------------------------------------------------
It is discussed here but I see no conclusion there:
  https://stackoverflow.com/a/18394716/2995591
The GCC behavior looks more useful to me.
The clang behavior is dangerous. One must make any 'const' or 'pure' virtual methods also 'final' to be safe for future. If they cannot be 'final' one must not use 'const'/'pure' for the base class method even despite it could be useful.


---


### compiler : `llvm`
### title : `ICE on valid, templated friend injection cause ICE, invalid template parameters, true and false at the same time assert condition`
### open_at : `2021-07-06T00:48:04Z`
### last_modified_date : `2021-07-06T01:02:51Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=50989
### status : `NEW`
### tags : `compile-fail, miscompilation`
### component : `C++`
### version : `8.0`
### severity : `normal`
### contents :
Hi,

I've stumbled upon a really weird bug with how friends are handled by clang.
The following causes invalid template parameters to be introduced and an ICE.

It's present since clang 8.0 and is still present in trunk.
Befoer clang 8, the friend was just never instantiated, which was also invalid.

Here a compiler-explorer link to the issue: https://godbolt.org/z/qzM41rrKG

Or here, the a minimal example:
```
#include <type_traits>

template<class...> struct type_t {};

struct A {};

template<class... Args>
void fn(A, type_t<Args...>);

template<int N>
void nothing() {}

struct fn_arg {};
struct class_arg {};

template<class T>
struct B
{
    template<class... Args>
    friend void fn(A, type_t<Args...>) {
        static_assert(std::is_same<T, fn_arg>::value, "Should be class_arg!");

        static_assert(sizeof...(Args) != 0, "ok");
        static_assert(sizeof...(Args) == 0, "What?");
        constexpr auto n = sizeof...(Args);
        nothing<n>(); //ICE!
    }
};

void func(B<class_arg> = {}) {}

int main()
{
    fn(A{}, type_t<fn_arg>{});
}

```

Thanks in advance


---


### compiler : `llvm`
### title : `Wrong code with throwing const function`
### open_at : `2021-07-08T11:29:34Z`
### last_modified_date : `2021-07-08T18:51:28Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=51021
### status : `NEW`
### tags : `miscompilation`
### component : `C++`
### version : `trunk`
### severity : `normal`
### contents :
The GCC developers have clarified that the function attributes const and pure do not imply that the functions do not throw. clang does assume that and as such miscompiles the following program:

  __attribute__((const)) void f() {
    throw 0;
  }

  int main() {
    try {
      f();
    } catch(int i) {
      return 0;
    }

    return 1;
  }

This program should return 0, not 1.

Godbolt link: https://godbolt.org/z/jj1PG7o78

(Please ignore the warning emitted by GCC, 'const' attribute on function returning 'void'; I have reported that as part of https://gcc.gnu.org/bugzilla/show_bug.cgi?id=101376.)


---


### compiler : `llvm`
### title : `constinit thread_local not destroyed when type incomplete at odr-use`
### open_at : `2021-07-13T16:55:38Z`
### last_modified_date : `2021-10-09T01:47:05Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=51079
### status : `RESOLVED`
### tags : `miscompilation`
### component : `C++2a`
### version : `trunk`
### severity : `normal`
### contents :
When an odr-use of a constinit thread_local variable of incomplete class type occurs, Clang does not make any attempt to register the odr-use (and thus the initialization and any associated destructor calls). The case where the variable is a (possibly multi-dimensional) array of an incomplete class type is similarly affected.

### SOURCE (<stdin>):
struct A;
extern constinit thread_local A a;
A &foo() { return a; }


### COMPILER INVOCATION:
clang -cc1 -emit-llvm -Wall -Wextra -Werror -pedantic-errors -std=c++20 -xc++ -std=c++20 -


### ACTUAL OUTPUT (IR snippet):
define dso_local nonnull align 1 %struct.A* @_Z3foov() #0 {
entry:
  ret %struct.A* @a
}


### EXPECTED OUTPUT (IR snippet):
define dso_local nonnull align 1 dereferenceable(1) %struct.A* @_Z3foov() #0 {
entry:
  %0 = call %struct.A* @_ZTW1a()
  ret %struct.A* %0
}


### COMPILER VERSION INFO (clang++ -v):
clang version 13.0.0 (https://github.com/llvm/llvm-project.git c4ed142e695f14ba5675ec6d12226ee706329a0f)
Target: x86_64-unknown-linux-gnu
Thread model: posix
InstalledDir: /opt/wandbox/clang-head/bin
Found candidate GCC installation: /usr/lib/gcc/x86_64-linux-gnu/5
Found candidate GCC installation: /usr/lib/gcc/x86_64-linux-gnu/5.5.0
Found candidate GCC installation: /usr/lib/gcc/x86_64-linux-gnu/6
Found candidate GCC installation: /usr/lib/gcc/x86_64-linux-gnu/6.5.0
Found candidate GCC installation: /usr/lib/gcc/x86_64-linux-gnu/7
Found candidate GCC installation: /usr/lib/gcc/x86_64-linux-gnu/7.5.0
Selected GCC installation: /usr/lib/gcc/x86_64-linux-gnu/5.5.0
Candidate multilib: .;@m64
Candidate multilib: 32;@m32
Candidate multilib: x32;@mx32
Selected multilib: .;@m64


---


### compiler : `llvm`
### title : `Multiple immediate invocation expression-statements of lambda expressions should be constant expressions`
### open_at : `2021-07-15T23:08:30Z`
### last_modified_date : `2021-07-15T23:08:30Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=51111
### status : `NEW`
### tags : `miscompilation`
### component : `C++2a`
### version : `trunk`
### severity : `enhancement`
### contents :
See https://godbolt.org/z/YqG7P977v.
```C++
void f() {
  []() consteval { int i{}; }();
  []() consteval { int i{}; ++i; }();
}
void g() {
  (void)[](int i) consteval { return i; }(0);
  (void)[](int i) consteval { return i; }(0);
}
```


---


### compiler : `llvm`
### title : `EarlyCSE incorrectly assumes that readonly functions return`
### open_at : `2021-08-30T09:48:21Z`
### last_modified_date : `2021-08-30T14:37:51Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=51668
### status : `NEW`
### tags : `miscompilation`
### component : `Scalar Optimizations`
### version : `trunk`
### severity : `normal`
### contents :
Test: Transforms/EarlyCSE/globalsaa-memoryssa.ll

define void @f3() {
  %call1 = call i16 @f1() nowrite nofree
  call void @f2()
  %call2 = call i16 @f1() nowrite nofree
  ret void
}
=>
define void @f3() {
  %call1 = call i16 @f1() nowrite nofree
  call void @f2()
  ret void
}

The second call to @f1() is incorrectly removed. We don't know if it exits, for example. Function @f2 may change the state read by @f1 and thus the first call may return and the second exit.
The optimization should be restricted to functions with the 'willreturn' attribute.


---


### compiler : `llvm`
### title : `LoopIdiomRecognize: Overflow in ctlz shifting loop`
### open_at : `2021-08-30T10:21:22Z`
### last_modified_date : `2021-08-30T10:42:15Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=51669
### status : `NEW`
### tags : `miscompilation`
### component : `Loop Optimizer`
### version : `trunk`
### severity : `enhancement`
### contents :
Test: Transforms/LoopIdiom/X86/arithmetic-right-shift-until-zero.ll

LoopIdiom creates expressions that overflow and produce incorrect result.
e.g. this instruction:
add nsw i8 %val.numactivebits, %0

overflows and yields poison. Even removing nsw doesn't fix the issue; see counterexample below.


----------------------------------------
define i8 @p0(i8 %val, i8 %start, i8 %extraoffset) {
%entry:
  br label %loop

%loop:
  %iv = phi i8 [ %start, %entry ], [ %iv.next, %loop ]
  %nbits = add nsw i8 %iv, %extraoffset
  %val.shifted = ashr i8 %val, %nbits
  %val.shifted.iszero = icmp eq i8 %val.shifted, 0
  %iv.next = add i8 %iv, 1
  call void @escape_inner(i8 %iv, i8 %nbits, i8 %val.shifted, i1 %val.shifted.iszero, i8 %iv.next)
  br i1 %val.shifted.iszero, label %end, label %loop

%end:
  %iv.res = phi i8 [ %iv, %loop ]
  %nbits.res = phi i8 [ %nbits, %loop ]
  %val.shifted.res = phi i8 [ %val.shifted, %loop ]
  %val.shifted.iszero.res = phi i1 [ %val.shifted.iszero, %loop ]
  %iv.next.res = phi i8 [ %iv.next, %loop ]
  call void @escape_outer(i8 %iv.res, i8 %nbits.res, i8 %val.shifted.res, i1 %val.shifted.iszero.res, i8 %iv.next.res)
  ret i8 %iv.res
}
=>
define i8 @p0(i8 %val, i8 %start, i8 %extraoffset) {
%entry:
  %val.numleadingzeros = ctlz i8 %val, 0
  %val.numactivebits = sub nsw nuw i8 8, %val.numleadingzeros
  %0 = sub i8 0, %extraoffset
  %val.numactivebits.offset = add i8 %val.numactivebits, %0
  %iv.final = smax i8 %val.numactivebits.offset, %start
  %loop.backedgetakencount = sub nsw i8 %iv.final, %start
  %loop.tripcount = add nsw nuw i8 %loop.backedgetakencount, 1
  br label %loop

%loop:
  %loop.iv = phi i8 [ 0, %entry ], [ %loop.iv.next, %loop ]
  %loop.iv.next = add nsw nuw i8 %loop.iv, 1
  %loop.ivcheck = icmp eq i8 %loop.iv.next, %loop.tripcount
  %iv = add nsw i8 %loop.iv, %start
  %nbits = add nsw i8 %iv, %extraoffset
  %val.shifted = ashr i8 %val, %nbits
  %iv.next = add i8 %iv, 1
  call void @escape_inner(i8 %iv, i8 %nbits, i8 %val.shifted, i1 %loop.ivcheck, i8 %iv.next)
  br i1 %loop.ivcheck, label %end, label %loop

%end:
  %iv.res = phi i8 [ %iv.final, %loop ]
  %nbits.res = phi i8 [ %nbits, %loop ]
  %val.shifted.res = phi i8 [ %val.shifted, %loop ]
  %val.shifted.iszero.res = phi i1 [ %loop.ivcheck, %loop ]
  %iv.next.res = phi i8 [ %iv.next, %loop ]
  call void @escape_outer(i8 %iv.res, i8 %nbits.res, i8 %val.shifted.res, i1 %val.shifted.iszero.res, i8 %iv.next.res)
  ret i8 %iv.res
}
Transformation doesn't verify!

ERROR: Source is more defined than target

Example:
i8 %val = #x80 (128, -128)
i8 %start = #x78 (120)
i8 %extraoffset = #x88 (136, -120)

Source:
i8 %iv = #x78 (120)
i8 %nbits = #x00 (0)
i8 %val.shifted = #x80 (128, -128)
i1 %val.shifted.iszero = #x0 (0)
i8 %iv.next = #x79 (121)

SOURCE MEMORY STATE
===================
NON-LOCAL BLOCKS:
Block 0 >       size: 0 align: 1        alloc type: 0
Block 1 >       size: 0 align: 1

Target:
i8 %val.numleadingzeros = #x00 (0)
i8 %val.numactivebits = #x08 (8)
i8 %0 = #x78 (120)
i8 %val.numactivebits.offset = #x80 (128, -128)
i8 %iv.final = #x78 (120)
i8 %loop.backedgetakencount = #x00 (0)
i8 %loop.tripcount = #x01 (1)
i8 %loop.iv = #x00 (0)
i8 %loop.iv.next = #x01 (1)
i1 %loop.ivcheck = #x1 (1)
i8 %iv = #x78 (120)
i8 %nbits = #x00 (0)
i8 %val.shifted = #x80 (128, -128)
i8 %iv.next = #x79 (121)
i8 %iv.res = #x78 (120)
i8 %nbits.res = #x00 (0)
i8 %val.shifted.res = #x80 (128, -128)
i1 %val.shifted.iszero.res = #x1 (1)
i8 %iv.next.res = #x79 (121)


---


### compiler : `llvm`
### title : `LoopUnroll: runtime check introduces branch on poison if fn call doesn't return`
### open_at : `2021-08-30T10:35:57Z`
### last_modified_date : `2021-08-30T10:35:57Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=51670
### status : `NEW`
### tags : `miscompilation`
### component : `Loop Optimizer`
### version : `trunk`
### severity : `normal`
### contents :
Test: Transforms/LoopUnroll/loop-remarks.ll

In the test below, @baz may not return. In that case, the source function will not branch on the possibly poison %exitcond (poison if %n poison).
The target function always branches on %n regardless of whether @baz returns or not.
The fix is to freeze %n if the code doesn't provably reach the branch.


define i32 @runtime(i32 %n) {
%entry:
  br label %for.body

%for.body:
  %s.06 = phi i32 [ 0, %entry ], [ %add1, %for.body ]
  %i.05 = phi i32 [ 0, %entry ], [ %inc, %for.body ]
  %add = add nsw i32 %i.05, 4
  %call = call i32 @baz(i32 %add)
  %add1 = add nsw i32 %call, %s.06
  %inc = add nsw i32 %i.05, 1
  %exitcond = icmp eq i32 %inc, %n
  br i1 %exitcond, label %for.end, label %for.body

%for.end:
  ret i32 %add1
}
=>
define i32 @runtime(i32 %n) {
%entry:
  %0 = add i32 %n, 4294967295
  %xtraiter = and i32 %n, 3
  %1 = icmp ult i32 %0, 3
  br i1 %1, label %for.end.unr-lcssa, label %entry.new

%entry.new:
  %unroll_iter = sub i32 %n, %xtraiter
  br label %for.body

%for.body:
  %s.06 = phi i32 [ 0, %entry.new ], [ %add1.3, %for.body ]
  %i.05 = phi i32 [ 0, %entry.new ], [ %inc.3, %for.body ]
  %niter = phi i32 [ %unroll_iter, %entry.new ], [ %niter.nsub.3, %for.body ]
  %add = add nsw i32 %i.05, 4
  %call = call i32 @baz(i32 %add)
  %add1 = add nsw i32 %call, %s.06
  %inc = add nsw nuw i32 %i.05, 1
  %niter.nsub = sub i32 %niter, 1
  %add.1 = add nsw i32 %inc, 4
  %call.1 = call i32 @baz(i32 %add.1)
  %add1.1 = add nsw i32 %call.1, %add1
  %inc.1 = add nsw nuw i32 %inc, 1
  %niter.nsub.1 = sub i32 %niter.nsub, 1
  %add.2 = add nsw i32 %inc.1, 4
  %call.2 = call i32 @baz(i32 %add.2)
  %add1.2 = add nsw i32 %call.2, %add1.1
  %inc.2 = add nsw nuw i32 %inc.1, 1
  %niter.nsub.2 = sub i32 %niter.nsub.1, 1
  %add.3 = add nsw i32 %inc.2, 4
  %call.3 = call i32 @baz(i32 %add.3)
  %add1.3 = add nsw i32 %call.3, %add1.2
  %inc.3 = add nsw i32 %inc.2, 1
  %niter.nsub.3 = sub i32 %niter.nsub.2, 1
  %niter.ncmp.3 = icmp eq i32 %niter.nsub.3, 0
  br i1 %niter.ncmp.3, label %for.end.unr-lcssa.loopexit, label %for.body

%for.end.unr-lcssa.loopexit:
  %add1.lcssa.ph.ph = phi i32 [ %add1.3, %for.body ]
  %s.06.unr.ph = phi i32 [ %add1.3, %for.body ]
  %i.05.unr.ph = phi i32 [ %inc.3, %for.body ]
  br label %for.end.unr-lcssa

%for.end.unr-lcssa:
  %add1.lcssa.ph = phi i32 [ undef, %entry ], [ %add1.lcssa.ph.ph, %for.end.unr-lcssa.loopexit ]
  %s.06.unr = phi i32 [ 0, %entry ], [ %s.06.unr.ph, %for.end.unr-lcssa.loopexit ]
  %i.05.unr = phi i32 [ 0, %entry ], [ %i.05.unr.ph, %for.end.unr-lcssa.loopexit ]
  %lcmp.mod = icmp ne i32 %xtraiter, 0
  br i1 %lcmp.mod, label %for.body.epil.preheader, label %for.end

%for.body.epil.preheader:
  br label %for.body.epil

%for.body.epil:
  %add.epil = add nsw i32 %i.05.unr, 4
  %call.epil = call i32 @baz(i32 %add.epil)
  %add1.epil = add nsw i32 %call.epil, %s.06.unr
  %inc.epil = add nsw i32 %i.05.unr, 1
  %epil.iter.sub = sub i32 %xtraiter, 1
  %epil.iter.cmp = icmp ne i32 %epil.iter.sub, 0
  br i1 %epil.iter.cmp, label %for.body.epil.1, label %for.end.epilog-lcssa

%for.body.epil.1:
  %add.epil.1 = add nsw i32 %inc.epil, 4
  %call.epil.1 = call i32 @baz(i32 %add.epil.1)
  %add1.epil.1 = add nsw i32 %call.epil.1, %add1.epil
  %inc.epil.1 = add nsw i32 %inc.epil, 1
  %epil.iter.sub.1 = sub i32 %epil.iter.sub, 1
  %epil.iter.cmp.1 = icmp ne i32 %epil.iter.sub.1, 0
  br i1 %epil.iter.cmp.1, label %for.body.epil.2, label %for.end.epilog-lcssa

%for.body.epil.2:
  %add.epil.2 = add nsw i32 %inc.epil.1, 4
  %call.epil.2 = call i32 @baz(i32 %add.epil.2)
  %add1.epil.2 = add nsw i32 %call.epil.2, %add1.epil.1
  br label %for.end.epilog-lcssa

%for.end.epilog-lcssa:
  %add1.lcssa.ph1 = phi i32 [ %add1.epil, %for.body.epil ], [ %add1.epil.1, %for.body.epil.1 ], [ %add1.epil.2, %for.body.epil.2 ]
  br label %for.end

%for.end:
  %add1.lcssa = phi i32 [ %add1.lcssa.ph, %for.end.unr-lcssa ], [ %add1.lcssa.ph1, %for.end.epilog-lcssa ]
  ret i32 %add1.lcssa
}
Transformation doesn't verify!
ERROR: Source is more defined than target

Example:
i32 %n = poison

Source:
i32 %s.06 = #x00000000 (0)
i32 %i.05 = #x00000000 (0)
i32 %add = #x00000004 (4)
i32 %call = poison
i32 %add1 = poison
i32 %inc = #x00000001 (1)
i1 %exitcond = poison

Target:
i32 %0 = poison
i32 %xtraiter = poison
i1 %1 = poison


---


### compiler : `llvm`
### title : `(Simple)LoopUnswitch introduces branch on poison if call doesn't return`
### open_at : `2021-08-30T10:46:31Z`
### last_modified_date : `2021-08-30T18:21:25Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=51671
### status : `RESOLVED`
### tags : `miscompilation`
### component : `Loop Optimizer`
### version : `trunk`
### severity : `normal`
### contents :
Tests:
 - Transforms/LoopUnswitch/preserve-analyses.ll
 - Transforms/SimpleLoopUnswitch/delete-dead-blocks.ll
 - Transforms/SimpleLoopUnswitch/nontrivial-unswitch-cost.ll


In the test below, @pci_get_device may not return. In that case, the source function will not branch on the undef %conv56.
The target function always branches on %conv56 regardless of whether @pci_get_device returns or not.
The fix is to freeze the condition if the code doesn't provably reach the branch.


define void @pnp_check_irq() {
%entry:
  %conv56 = trunc i64 undef to i32
  br label %while.cond.i

%while.cond.i:
  %call.i25 = call * @pci_get_device()
  br i1 undef, label %if.then65, label %while.body.i

%if.then65:
  assume i1 0

%while.body.i:
  br i1 undef, label %if.then31.i.i, label %while.cond.i.backedge

%if.then31.i.i:
  switch i32 %conv56, label %while.cond.i.backedge [
    i32 14, label %if.then42.i.i
    i32 15, label %if.then42.i.i
  ]

%if.then42.i.i:
  %call.i25.lcssa48 = phi * [ %call.i25, %if.then31.i.i ], [ %call.i25, %if.then31.i.i ]
  assume i1 0

%while.cond.i.backedge:
  br label %while.cond.i
}
=>
define void @pnp_check_irq() {
%entry:
  %conv56 = trunc i64 undef to i32
  %0 = icmp eq i32 %conv56, 14
  br i1 %0, label %entry.split.us, label %entry.entry.split_crit_edge

%entry.entry.split_crit_edge:
  br label %entry.split

%entry.split:
  %1 = icmp eq i32 %conv56, 15
  br i1 %1, label %entry.split.split.us, label %entry.split.entry.split.split_crit_edge

%entry.split.split.us:
  br label %while.cond.i.us1

%while.cond.i.us1:
  %call.i25.us2 = call * @pci_get_device()
  br i1 1, label %if.then65.us-lcssa.us-lcssa.us, label %while.body.i.us3

%if.then65.us-lcssa.us-lcssa.us:
  br label %if.then65.us-lcssa

%while.body.i.us3:
  br i1 undef, label %if.then31.i.i.us4, label %while.cond.i.backedge.us5

%if.then31.i.i.us4:
  switch i32 15, label %while.cond.i.backedge.us5 [
    i32 14, label %if.then42.i.i.us-lcssa.us-lcssa.us
    i32 15, label %if.then42.i.i.us-lcssa.us-lcssa.us
  ]

%if.then42.i.i.us-lcssa.us-lcssa.us:
  %call.i25.lcssa48.ph.ph.us = phi * [ %call.i25.us2, %if.then31.i.i.us4 ], [ %call.i25.us2, %if.then31.i.i.us4 ]
  br label %if.then42.i.i.us-lcssa

%while.cond.i.backedge.us5:
  br label %while.cond.i.us1

%entry.split.entry.split.split_crit_edge:
  br label %entry.split.split

%entry.split.split:
  br label %while.cond.i

%while.cond.i:
  %call.i25 = call * @pci_get_device()
  br i1 1, label %if.then65.us-lcssa.us-lcssa, label %while.body.i

%if.then65.us-lcssa.us-lcssa:
  br label %if.then65.us-lcssa

%if.then65.us-lcssa:
  br label %if.then65

%while.body.i:
  br i1 undef, label %if.then31.i.i, label %while.cond.i.backedge

%if.then31.i.i:
  switch i32 %conv56, label %while.cond.i.backedge [
    i32 14, label %if.then42.i.i.us-lcssa.us-lcssa
    i32 15, label %if.then42.i.i.us-lcssa.us-lcssa
  ]

%if.then42.i.i.us-lcssa.us-lcssa:
  %call.i25.lcssa48.ph.ph = phi * [ %call.i25, %if.then31.i.i ], [ %call.i25, %if.then31.i.i ]
  br label %if.then42.i.i.us-lcssa

%if.then42.i.i.us-lcssa:
  %call.i25.lcssa48.ph = phi * [ %call.i25.lcssa48.ph.ph, %if.then42.i.i.us-lcssa.us-lcssa ], [ %call.i25.lcssa48.ph.ph.us, %if.then42.i.i.us-lcssa.us-lcssa.us ]
  br label %if.then42.i.i

%while.cond.i.backedge:
  br label %while.cond.i

%entry.split.us:
  br label %while.cond.i.us

%while.cond.i.us:
  %call.i25.us = call * @pci_get_device()
  br i1 1, label %if.then65.us-lcssa.us, label %while.body.i.us

%if.then65.us-lcssa.us:
  br label %if.then65

%if.then65:
  assume i1 0

%while.body.i.us:
  br i1 undef, label %if.then31.i.i.us, label %while.cond.i.backedge.us

%if.then31.i.i.us:
  switch i32 14, label %while.cond.i.backedge.us [
    i32 14, label %if.then42.i.i.us-lcssa.us
    i32 15, label %if.then42.i.i.us-lcssa.us
  ]

%if.then42.i.i.us-lcssa.us:
  %call.i25.lcssa48.ph.us = phi * [ %call.i25.us, %if.then31.i.i.us ], [ %call.i25.us, %if.then31.i.i.us ]
  br label %if.then42.i.i

%if.then42.i.i:
  %call.i25.lcssa48 = phi * [ %call.i25.lcssa48.ph, %if.then42.i.i.us-lcssa ], [ %call.i25.lcssa48.ph.us, %if.then42.i.i.us-lcssa.us ]
  assume i1 0

%while.cond.i.backedge.us:
  br label %while.cond.i.us
}
Transformation doesn't verify!
ERROR: Source is more defined than target

Example:

Source:
i32 %conv56 = any
* %call.i25 = poison

SOURCE MEMORY STATE
===================
NON-LOCAL BLOCKS:
Block 0 >       size: 0 align: 1        alloc type: 0
Block 1 >       size: 0 align: 1

Target:
i32 %conv56 = #xfffffff1 (4294967281, -15)
i1 %0 = #x0 (0)
i1 %1 = #x0 (0)
* %call.i25.us2 = poison
* %call.i25 = poison
* %call.i25.us = poison


---


### compiler : `llvm`
### title : `MergeICmps reorders comparisons and introduces UB`
### open_at : `2021-09-14T09:51:55Z`
### last_modified_date : `2021-09-21T19:26:03Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=51845
### status : `NEW`
### tags : `miscompilation`
### component : `Scalar Optimizations`
### version : `trunk`
### severity : `normal`
### contents :
test: Transforms/MergeICmps/X86/entry-block-shuffled.ll

src: compares 12/8, br, 0/0, br, 4/4, br, 12/12
tgt: compares 0/0, 4/4, br, 12/8, br, 12/12

The issue is that tgt branches on 0-8 values, which can be poison, while src wouldn't branch on those if e.g. 12/8 offsets are different.
Needs a freeze.


define i1 @opeq1(* nocapture nowrite dereferenceable(16) %a, * nocapture nowrite dereferenceable(16) %b) nofree {
%entry:
  %first.i = gep inbounds * nocapture nowrite dereferenceable(16) %a, 16 x i64 0, 1 x i64 12
  %0 = load i32, * %first.i, align 4
  %first1.i = gep inbounds * nocapture nowrite dereferenceable(16) %b, 16 x i64 0, 1 x i64 8
  %1 = load i32, * %first1.i, align 4
  %cmp.i = icmp eq i32 %0, %1
  br i1 %cmp.i, label %land.rhs.i, label %opeq1.exit

%land.rhs.i:
  %second.i = gep inbounds * nocapture nowrite dereferenceable(16) %a, 16 x i64 0, 1 x i64 0
  %2 = load i32, * %second.i, align 4
  %second2.i = gep inbounds * nocapture nowrite dereferenceable(16) %b, 16 x i64 0, 1 x i64 0
  %3 = load i32, * %second2.i, align 4
  %cmp3.i = icmp eq i32 %2, %3
  br i1 %cmp3.i, label %land.rhs.i.2, label %opeq1.exit

%land.rhs.i.2:
  %third.i = gep inbounds * nocapture nowrite dereferenceable(16) %a, 16 x i64 0, 1 x i64 4
  %4 = load i32, * %third.i, align 4
  %third2.i = gep inbounds * nocapture nowrite dereferenceable(16) %b, 16 x i64 0, 1 x i64 4
  %5 = load i32, * %third2.i, align 4
  %cmp4.i = icmp eq i32 %4, %5
  br i1 %cmp4.i, label %land.rhs.i.3, label %opeq1.exit

%land.rhs.i.3:
  %fourth.i = gep inbounds * nocapture nowrite dereferenceable(16) %a, 16 x i64 0, 1 x i64 12
  %6 = load i32, * %fourth.i, align 4
  %fourth2.i = gep inbounds * nocapture nowrite dereferenceable(16) %b, 16 x i64 0, 1 x i64 12
  %7 = load i32, * %fourth2.i, align 4
  %cmp5.i = icmp eq i32 %6, %7
  br label %opeq1.exit

%opeq1.exit:
  %8 = phi i1 [ 0, %entry ], [ 0, %land.rhs.i ], [ 0, %land.rhs.i.2 ], [ %cmp5.i, %land.rhs.i.3 ]
  ret i1 %8
}
=>
define i1 @opeq1(* nocapture nowrite dereferenceable(16) %a, * nocapture nowrite dereferenceable(16) %b) nofree {
%land.rhs.i+land.rhs.i.2:
  %0 = gep inbounds * nocapture nowrite dereferenceable(16) %a, 16 x i64 0, 1 x i64 0
  %1 = gep inbounds * nocapture nowrite dereferenceable(16) %b, 16 x i64 0, 1 x i64 0
  %cstr = bitcast * %0 to *
  %cstr3 = bitcast * %1 to *
  %memcmp = memcmp * %cstr, * %cstr3, i64 8
  %2 = icmp eq i32 %memcmp, 0
  br i1 %2, label %entry2, label %opeq1.exit

%entry2:
  %3 = gep inbounds * nocapture nowrite dereferenceable(16) %a, 16 x i64 0, 1 x i64 12
  %4 = gep inbounds * nocapture nowrite dereferenceable(16) %b, 16 x i64 0, 1 x i64 8
  %5 = load i32, * %3, align 4
  %6 = load i32, * %4, align 4
  %7 = icmp eq i32 %5, %6
  br i1 %7, label %land.rhs.i.31, label %opeq1.exit

%land.rhs.i.31:
  %8 = gep inbounds * nocapture nowrite dereferenceable(16) %a, 16 x i64 0, 1 x i64 12
  %9 = gep inbounds * nocapture nowrite dereferenceable(16) %b, 16 x i64 0, 1 x i64 12
  %10 = load i32, * %8, align 4
  %11 = load i32, * %9, align 4
  %12 = icmp eq i32 %10, %11
  br label %opeq1.exit

%opeq1.exit:
  %13 = phi i1 [ %12, %land.rhs.i.31 ], [ 0, %entry2 ], [ 0, %land.rhs.i+land.rhs.i.2 ]
  ret i1 %13
}
Transformation doesn't verify!
ERROR: Source is more defined than target

Example:
* nocapture nowrite dereferenceable(16) %a = pointer(non-local, block_id=1, offset=10, attrs=3)
* nocapture nowrite dereferenceable(16) %b = pointer(non-local, block_id=2, offset=88, attrs=3)

Source:
* %first.i = pointer(non-local, block_id=1, offset=22, attrs=3)
i32 %0 = #x80000002 (2147483650, -2147483646)
* %first1.i = pointer(non-local, block_id=2, offset=96, attrs=3)
i32 %1 = #x00010100 (65792)
i1 %cmp.i = #x0 (0)
  >> Jump to %opeq1.exit
i1 %8 = #x0 (0)

SOURCE MEMORY STATE
===================
NON-LOCAL BLOCKS:
Block 0 >	size: 0	align: 1	alloc type: 0	address: 0
Block 1 >	size: 129	align: 2	alloc type: 0	address: 122
Block 2 >	size: 105	align: 2	alloc type: 0	address: 16

Target:
* %0 = pointer(non-local, block_id=1, offset=10, attrs=3)
* %1 = pointer(non-local, block_id=2, offset=88, attrs=3)
* %cstr = pointer(non-local, block_id=1, offset=10, attrs=3)
* %cstr3 = pointer(non-local, block_id=2, offset=88, attrs=3)
i32 %memcmp = poison
i1 %2 = poison
UB triggered on br


---


### compiler : `llvm`
### title : `Sink: moves calls that may not return`
### open_at : `2021-09-14T09:56:12Z`
### last_modified_date : `2021-09-14T09:56:12Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=51846
### status : `NEW`
### tags : `miscompilation`
### component : `Scalar Optimizations`
### version : `trunk`
### severity : `normal`
### contents :
Test: Transforms/Sink/call.ll

Transformation only valid if willreturn & nounwind attributes are present.


define i32 @test_sink_no_stores(i1 %z) {
%0:
  %l = call i32 @f_load_global() nowrite nofree
  br i1 %z, label %true, label %false

%false:
  ret i32 0

%true:
  ret i32 %l
}
=>
define i32 @test_sink_no_stores(i1 %z) {
%0:
  br i1 %z, label %true, label %false

%false:
  ret i32 0

%true:
  %l = call i32 @f_load_global() nowrite nofree
  ret i32 %l
}
Transformation doesn't verify!
ERROR: Source is more defined than target

Example:
i1 %z = undef

Source:
i32 %l = UB triggered!

SOURCE MEMORY STATE
===================
NON-LOCAL BLOCKS:
Block 0 >	size: 0	align: 1	alloc type: 0
Block 1 >	size: 0	align: 1

Target:
UB triggered on br


---


### compiler : `llvm`
### title : `LICM introduces load in writeonly function (UB)`
### open_at : `2021-09-19T10:53:43Z`
### last_modified_date : `2021-09-19T17:05:11Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=51906
### status : `NEW`
### tags : `miscompilation`
### component : `Loop Optimizer`
### version : `trunk`
### severity : `normal`
### contents :
LICM transforms this:
for (i=0; i < 4; i += 4)
  store @glb, some-expr
=>
tmp = load @lgb
compute some-expr
for (i=0; i < 4; i += 4)
  tmp = expr
store @glb, tmp


For functions that are writeonly this introduces UB as the original function had no load and the optimized now has a load from global memory.
The second issue is the store introduction. I didn't check if the store is introduced for loops that are not guaranteed to execute, but if that's the case that may violate C++'s memory model (where I believe you cannot introduce stores).


@glb = external global i8, align 1

define void @test(i8 %var) writeonly {
entry:
  br label %for.cond

for.cond:
  %i = phi i64 [ 0, %entry ], [ %add, %cond.end ]
  %cmp = icmp ult i64 %i, 4
  br i1 %cmp, label %for.body39, label %for.end

for.body39:
  %div = sdiv i8 %var, 3
  %cmp2 = icmp slt i8 %div, 0
  br i1 %cmp2, label %cond.true, label %cond.false

cond.true:
  br label %cond.end

cond.false:
  br label %cond.end

cond.end:
  %merge = phi i8 [ %div, %cond.true ], [ 0, %cond.false ]
  store i8 %merge, i8* @glb, align 1
  %add = add i64 %i, 4
  br label %for.cond

for.end:
  ret void
}


After LICM:
define void @test(i8 %var) #0 {
entry:
  %div = sdiv i8 %var, 3
  %cmp2 = icmp slt i8 %div, 0
  %glb.promoted = load i8, i8* @glb, align 1
  br label %for.cond

for.cond:                                         ; preds = %cond.end, %entry
  %merge1 = phi i8 [ %glb.promoted, %entry ], [ %merge, %cond.end ]
  %i = phi i64 [ 0, %entry ], [ %add, %cond.end ]
  %cmp = icmp ult i64 %i, 4
  br i1 %cmp, label %for.body39, label %for.end

for.body39:                                       ; preds = %for.cond
  br i1 %cmp2, label %cond.true, label %cond.false

cond.true:                                        ; preds = %for.body39
  br label %cond.end

cond.false:                                       ; preds = %for.body39
  br label %cond.end

cond.end:                                         ; preds = %cond.false, %cond.true
  %merge = phi i8 [ %div, %cond.true ], [ 0, %cond.false ]
  %add = add i64 %i, 4
  br label %for.cond

for.end:                                          ; preds = %for.cond
  %merge1.lcssa = phi i8 [ %merge1, %for.cond ]
  store i8 %merge1.lcssa, i8* @glb, align 1
  ret void
}


Reduced test case from John Regehr & Vsevolod Livinskii.


---


### compiler : `llvm`
### title : `Incorrect result with -O1 -march=skx`
### open_at : `2021-10-28T19:19:38Z`
### last_modified_date : `2021-11-01T23:45:10Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=52335
### status : `NEW`
### tags : `miscompilation`
### component : `Backend: X86`
### version : `trunk`
### severity : `enhancement`
### contents :
It looks like LoopVectorizePass introduces changes that uncover a bug in the backend. The transformation was verified with alive2. I've attached C++ and LLVM IR reproducers.

C++ reproducer:
// func.cpp
extern int var_3;
extern bool var_23;
extern int arr_12[];
extern short arr_13[];
void test() {
#pragma clang loop vectorize_predicate(enable)
  for (char a = 4; a < var_3; a++) {
    arr_13[a] = arr_12[a - 3];
    var_23 = arr_12[a - 1];
  }
}

// driver.cpp 
#include <stdio.h>

int var_3 = 24;
bool var_23 = 1;
int arr_12 [25];
unsigned short arr_13 [25];

void test();

int main() {
    for (size_t i_0 = 0; i_0 < 25; ++i_0)
        arr_12 [i_0] = 1;
    test();
    printf("%d\n", (int)var_23);
}

>$ clang++ -O0 -march=skx func.cpp driver.cpp && sde -skx -- ./a.out 
1
>$ clang++ -O1 -march=skx func.cpp driver.cpp && sde -skx -- ./a.out 
0

LLVM IR Reproducer:
; ModuleID = 'func.cpp'
source_filename = "func.cpp"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

@var_3 = external dso_local local_unnamed_addr global i32, align 4
@arr_12 = external dso_local local_unnamed_addr global [0 x i32], align 4
@arr_13 = external dso_local local_unnamed_addr global [0 x i16], align 2
@var_23 = external dso_local local_unnamed_addr global i8, align 1

; Function Attrs: mustprogress nofree norecurse nosync nounwind uwtable
define dso_local void @_Z4testv() local_unnamed_addr #0 {
entry:
  %0 = load i32, i32* @var_3, align 4, !tbaa !3
  %cmp13 = icmp sgt i32 %0, 4
  br i1 %cmp13, label %for.body.preheader, label %for.cond.cleanup

for.body.preheader:                               ; preds = %entry
  br label %for.body

for.cond.for.cond.cleanup_crit_edge:              ; preds = %for.body
  %conv15.lcssa = phi i32 [ %conv15, %for.body ]
  %sub6 = add nsw i32 %conv15.lcssa, -1
  %idxprom7 = sext i32 %sub6 to i64
  %arrayidx8 = getelementptr inbounds [0 x i32], [0 x i32]* @arr_12, i64 0, i64 %idxprom7
  %1 = load i32, i32* %arrayidx8, align 4, !tbaa !3
  %tobool = icmp ne i32 %1, 0
  %frombool = zext i1 %tobool to i8
  store i8 %frombool, i8* @var_23, align 1, !tbaa !7
  br label %for.cond.cleanup

for.cond.cleanup:                                 ; preds = %for.cond.for.cond.cleanup_crit_edge, %entry
  ret void

for.body:                                         ; preds = %for.body.preheader, %for.body
  %conv15 = phi i32 [ %conv, %for.body ], [ 4, %for.body.preheader ]
  %a.014 = phi i8 [ %inc, %for.body ], [ 4, %for.body.preheader ]
  %sub = add nsw i32 %conv15, -3
  %idxprom = sext i32 %sub to i64
  %arrayidx = getelementptr inbounds [0 x i32], [0 x i32]* @arr_12, i64 0, i64 %idxprom
  %2 = load i32, i32* %arrayidx, align 4, !tbaa !3
  %conv2 = trunc i32 %2 to i16
  %idxprom3 = sext i8 %a.014 to i64
  %arrayidx4 = getelementptr inbounds [0 x i16], [0 x i16]* @arr_13, i64 0, i64 %idxprom3
  store i16 %conv2, i16* %arrayidx4, align 2, !tbaa !9
  %inc = add i8 %a.014, 1
  %conv = sext i8 %inc to i32
  %cmp = icmp sgt i32 %0, %conv
  br i1 %cmp, label %for.body, label %for.cond.for.cond.cleanup_crit_edge, !llvm.loop !11
}

attributes #0 = { mustprogress nofree norecurse nosync nounwind uwtable "frame-pointer"="none" "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="skx" "target-features"="+adx,+aes,+avx,+avx2,+avx512bw,+avx512cd,+avx512dq,+avx512f,+avx512vl,+bmi,+bmi2,+clflushopt,+clwb,+crc32,+cx16,+cx8,+f16c,+fma,+fsgsbase,+fxsr,+invpcid,+lzcnt,+mmx,+movbe,+pclmul,+pku,+popcnt,+prfchw,+rdrnd,+rdseed,+sahf,+sse,+sse2,+sse3,+sse4.1,+sse4.2,+ssse3,+x87,+xsave,+xsavec,+xsaveopt,+xsaves" }

!llvm.module.flags = !{!0, !1}
!llvm.ident = !{!2}

!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{i32 7, !"uwtable", i32 1}
!2 = !{!"clang version 14.0.0 (https://github.com/llvm/llvm-project.git 2d77b272a8f9b5b89b022628ca30b6b896a8f725)"}
!3 = !{!4, !4, i64 0}
!4 = !{!"int", !5, i64 0}
!5 = !{!"omnipotent char", !6, i64 0}
!6 = !{!"Simple C++ TBAA"}
!7 = !{!8, !8, i64 0}
!8 = !{!"bool", !5, i64 0}
!9 = !{!10, !10, i64 0}
!10 = !{!"short", !5, i64 0}
!11 = distinct !{!11, !12, !13, !14, !15}
!12 = !{!"llvm.loop.mustprogress"}
!13 = !{!"llvm.loop.unroll.disable"}
!14 = !{!"llvm.loop.vectorize.predicate.enable", i1 true}
!15 = !{!"llvm.loop.vectorize.enable", i1 true}

>$ clang++ -O0 ok.ll driver.cpp && sde -skx -- ./a.out 
1
>$ opt -loop-vectorize ok.ll > opt.ll && clang++ -O0 opt.ll driver.cpp && sde -skx -- ./a.out 
0

LLVM version:
clang version 14.0.0 (https://github.com/llvm/llvm-project.git 2d77b272a8f9b5b89b022628ca30b6b896a8f725)


---


### compiler : `llvm`
### title : `InstSimplify incorrectly folds signed comparisons of 'gep inbounds'`
### open_at : `2021-11-05T23:14:58Z`
### last_modified_date : `2021-11-07T03:12:09Z`
### link : https://bugs.llvm.org/show_bug.cgi?id=52429
### status : `RESOLVED`
### tags : `miscompilation`
### component : `Scalar Optimizations`
### version : `trunk`
### severity : `normal`
### contents :
File: Transforms/InstSimplify/compare.ll

define i1 @gep_same_base_constant_indices(i8* %a) {
; CHECK-NEXT:    ret i1 true
;
  %arrayidx1 = getelementptr inbounds i8, i8* %a, i64 1
  %arrayidx2 = getelementptr inbounds i8, i8* %a, i64 10
  %cmp = icmp slt i8* %arrayidx1, %arrayidx2
  ret i1 %cmp
}

Folding such unsigned comparisons is correct, but not for signed as an object may cross the unsigned/signed line, e.g:
ptr = malloc(42) // 0x7fff..ff0
ptr + 42  // 0x8....


---
