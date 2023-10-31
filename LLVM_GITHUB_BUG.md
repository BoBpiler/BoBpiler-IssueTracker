## LLVM 목차
## 컴파일러 버그
1. [wrong code at -O1 and above on x86_64-linux-gnu (컴파일러 버그)](#1)
2. [LoopVectorize Miscompilation with Aliases in clang 15+ (컴파일러 버그)](#2)
3. [Failure to remove mask from shift amounts in unrolled loop (컴파일러 버그)](#3)
4. [Bug in mips64el: Varied Output by Clang Optimization Levels (컴파일러 버그)](#4)
5. [Wrong code at -O1/2/s on x86_64-linux_gnu since 669ddd1 (컴파일러 버그)](#5)
6. [wrong code at -O1 and above on x86_64-linux-gnu (컴파일러 버그)](#6)
7. [Wrong code at -O2 on x86_64-linux_gnu since ca18e21 (컴파일러 버그)](#7)
8. [Wrong code at -O2/3/s on x86_64-linux_gnu since 45ecfed (컴파일러 버그)](#8)
9. [Wrong code at -Os on x86_64-linux_gnu since 5dde9c1 (컴파일러 버그)](#9)
10. [Clang's Optimization Introduces Unexpected Sign Extension in RISC-V Bit-Field Operations (컴파일러 버그)](#10)
11. [Missed optimization: Reorder deallocations before allocations of unrelated memory (버그는 아니지만 꽤 흥미로운 논의)](#11)
12. [Conversion of _Float16 for variadic functions doesn't seem to work (컴파일러 버그)](#12)
13. [Clang fails to remove unnecessary loop (컴파일러 버그)](#13)
14. [Wrong code at -O2 on x86_64-linux_gnu since 3ddd1ff (컴파일러 버그)](#14)
15. [Too aggresive C++23 static call operator optimization (컴파일러 버그)](#15)
16. [abs from cmath is not constexpr when it should be [C++23] (컴파일러 버그)](#18)
17. [Wrong code at -O2 on x86_64-linux_gnu since ddfee6d (recent regression) (컴파일러 버그)](#25)
18. [[X86] Musttail calls involving unions with long double members are miscompiled at -O2 (컴파일러 버그)(이거 뭔가 취약점으로 잘 쓸수 있을지도 !)](#26)
19. [[WinEH] Model catch object write in MIR (컴파일러 버그)(익셉션 랜덤 메모리 읽기)](#27)
20. [Wrong code under '-mcmodel=large -O1' (컴파일러 버그)](#28)
21. [miscompile of store to element of <i1 x N> (컴파일러 버그)](#29)
22. [Compare operator not defined for recursive data types on C++20 (컴파일러 버그)](#31)
23. [-frounding-math is buggy at -O1 and above (컴파일러 버그)](#32)
24. [Wrong code at -O3  on x86_64 [14 regression since 0d95b20] (컴파일러 버그)](#33)
25. [avx register spill generates 20 extra instructions (컴파일러 버그)](#34)
26. [Clang ssp-buffer-size misinterprets some IR-level padding as arrays (컴파일러 버그) (스택 카나리 사라짐)](#35)
27. [Behavior of overflowing floating-point to integer conversions (컴파일러 버그)](#40)
28. [wrong type of ternary expression involving composite pointer type with array of unknown bound (컴파일러 버그)](#41)
42. [Complex division doesn't respect pragma float_control (컴파일러 버그)](#42)
43. [Sanitizer `pointer-overflow` does not appear to function (컴파일러 버그)](#43)
44. [[Bug][AArch64] Ensure SVE function operands passed via memory are initialised.](#44)
45. [[AArch64] Miscompilation when stack tagging is enabled in AArch64 (컴파일러 버그)](#45)
46. [[clang] Main Function Missing Due to Incorrect Infinite Loop Optimization (컴파일러 버그)](#46)
47. [`SSP Strong with `-fexceptions` causing code-gen change on a C compilation with a `noreturn` attribute` (컴파일러 버그)](#47)
48. [SLPVectorizer incorrectly reorders select operands (컴파일러 버그)](#50)
49. [[clang][vectorize] -O2 vectorize will get wrong result (컴파일러 버그)](#51)
50. [The combination of -fno-rtti -fexceptions is very brittle (컴파일러 버그)](#52)
51. [Wrong code at -Os on x86_64 (recent regression since 6ed152a) (컴파일러 버그)](#53)
52. [[Inliner] Should we inline callee containing llvm.frameaddress? (컴파일러 버그), 인라인 함수의 주소 등과 연관](#54)
53. [[AArch64] neon big endian miscompiled (컴파일러 버그)](#56)
54. [Incorrect value of requires expression involving discarded value (컴파일러 버그)](#57)
55. [Assumptions not working with complex conditionals (컴파일러 버그)](#61)
56. [Possible incorrect code generation when using variable templates (컴파일러 버그)](#62)
58. [Missed function specialization (Clang vs GCC) (컴파일러 버그)](#63)
58. [if-conversion creating dead references to removed MachineBasicBlocks in INLINEASM_BR (컴파일러 버그)](#64)
58. [[Clang] [Concepts] Regression between 15.x and trunk: satisfaction of constraint depends on itself (컴파일러 버그)](#65)
48. [machine-cse pass breaks __builtin_setjmp on powerpc (컴파일러 버그)](#66)
48. [clang c++20: Associated constraints added to a default constructor are excessively checked(컴파일러 버그)](#67)
48. [[clang] Multiple destructor calls emitted with consteval usage in switch statement (이거 소멸자 두번 호출되는 쌉버그 !)](#68)
48. [comparison with short (< 16 chars) local `const std::string` is slower when it is `static` (성능이 더 느려지는 컴파일러 버그)](#69)
48. [Terminate handler generated for noexcept method using try/catch(...) (try catch에서 프로그램 종료 코드 컴파일되는 컴파일러 버그)](#70)
48. [[clang] Miscompiled atomic ordering at -O1 (clang-14 onwards) (원자 변수에 대한 컴파일러 버그)](#71)
48. [Wrongful cleanup for `trivial_abi` parameter after passing it to callee (이중 소멸자 호출 버그)](#72)
48. [Constant propagation makes a register value forgotten (이중 으로 값을 할당 이거 뭔가 문제가 될수있을지도?)](#73)
48. [Thrown exception in `nothrow` function not detected (컴파일러 경고 누락 ?)](#74)
48. [[Clang]: Incorrect inheritance of protected (default) constructor (컴파일러 버그)](#75)
48. [wrong type for `auto&` parameter when deducing a class template partial specialization (auto에 대한 타입 추론 버그)](#76)
48. [A miscompile in instcombine, opt pass. (컴파일러 버그)(재현이 안됨..)](#79)
48. [clang 15 built kernel crashes w. "BUG: kernel NULL pointer dereference, address: 00000000", gcc 12 built kernel with same config boots fine (6.1-rc7, x86_32) (커널에서 발생한 컴파일러 관련 버그인듯? 분석 더 필요)](#80)
48. [clang-15: May produce invalid code when -O1 (or higher) is used with -fzero-call-used-regs=all (openssh에서 발생한 컴파일러 버그)](#81)
48. [[clang] incorrect code generation when building gawk 5.2.1 using -O2/-O3 (컴파일러 쌉버그)](#82)
48. [Clang mistakenly elides coroutine allocation resulting in a segfault and `stack-use-after-return` from `AddressSanitizer` (컴파일러 버그)](#83)
48. [NTTP of structural class types pass values literally when used directly (should: invoke copy constructors) in Clang 15 (C++) (컴파일러 버그)](#84)
48. [Miscompilation with noalias and pointer equality (컴파일러 버그)](#85)
48. [[LoopVectorizePass] Miscompilation of default vectorization vs no vectorization (컴파일러 버그)](#86)
48. [Incorrect sign-extension of load's index generated on armv8 under UBSAN (컴파일러 버그)](#87)
48. [miscompilation? with 3010f60381bcd828d1b409cfaa576328bcd05bbc on RISCV (컴파일러 버그)](#88)
48. [clang-cl 32 bit vectorcall doesn't match msvc 32 bit vectorcall (벡터화 컴파일러 버그)](#89)
48. [structure alignment seems broken when targeting windows (컴파일러 버그)](#90)
48. [Potential miscompilation for m2. (컴파일러 버그)](#91)
48. [Miscompile with -fglobal-isel, -ftrivial-auto-var-init=pattern, and thinlto (크로미움과 관련된 버그)](#92)
48. [Passing pointer to a local variable prevents TCO (최적화 누락)](#93)
48. [Trivially Default Constructible with `requires` + Structure Wrapping (컴파일러 버그)](#95)
48. [coroutines: miscompilation when using ternary operator and co_await (use after free) (코루틴 UAF 컴파일러 버그)](#96)
48. [clang trunk at -O2/3 misses a global-buffer-overflow (컴파일러 버그)](#97)
48. [Bad codegen after 8adfa29706e (NaN constant folding weirdness) (컴파일러 버그)](#98)
48. [Static array indices in function parameter declarations cause poor SIMD code-generation (웹어셈블리 컴파일러 버그)](#99)
48. [Incorrect codegen for unaligned load/store (ARM NEON) (컴파일러 버그)](#100)
48. [Poor code when a pointer is a global var, but good code for static or local var (컴파일러 버그)](#101)
48. [Incorrect codegen for int128 parameters with x64-systemv calling conv (컴파일러 버그)](#102)
48. [C, C11 and later: padding not set to “zero bits” in compound literal (컴파일러 버그)](#103)
48. [Constant tracking foiled by an escaping reference (컴파일러 버그, 두번 free되는 느낌?)](#104)
48. [[avr] Return values are promoted to (unsigned) int for no reason. (unsigned로 승격되는 컴파일러 버그)](#105)
48. [Friended struct with concept gives different output in clang/gcc/MSVC (컴파일러 버그)](#106)
48. [`__attribute__((pure))`/`__attribute__((const))` is a massive unchecked footgun (컴파일러 버그, 뭔가 clang이 예외 관련해서 착각하고있어 여러 개발자가 같이 문제를 해결해야함)](#107)
48. [The preferred global deallocation for the array whose element is of class type with non-trival destructor (컴파일러 버그)](#108)
48. [wrong code at -O1 and above (컴파일러 버그)](#109)
48. [Infinite self-recursion for functions renamed with __asm__, combined with inline specialization of it (컴파일러 버그)](#110)
48. [Miscompilation on i686 windows with opaque pointers + LTO (컴파일러  버그)](#111)
48. [Invalid object passed to coroutine's await_transform (윈도우 코루틴 버그)](#112)
48. [`rbp` clobber in inline assembly is not respected for functions with a frame pointer (백도어로 활용 가능할지도 ?? gcc에서는 컴파일 오류)](#113)
48. [Clang choosing copy constructor over initializer_list (컴파일러 버그)](#114)
48. [[coroutines] incorrect transformation removes co_await side effects in non-taken branch (코루틴 컴파일러 버그)](#115)
48. [Wrong code at -Os on x86_64-linux_gnu (LoopFlattenPass) (컴파일러 버그)](#116)
48. [`-fno-semantic-interposition` breaks code relying on address uniqueness of a function (컴파일러 버그)](#117)
48. [clang: x86 stdcall/thiscall with an empty object parameter yields ABI-incompatible code (컴파일러 버그)](#118)
48. [Wrong code at -Os on x86_64-linux_gnu (컴파일러 버그)](#119)
48. [Clang accepts invalid narrowing conversion (컴파일러 버그)](#120)
48. [](#121)
48. [](#)
48. [](#)
48. [](#)
48. [](#)
48. [](#)
48. [](#)
48. [](#)

## 컴파일 실패
16. [[C++17][clang:Frontend] Clang can't deduce the correct deduction guide.(컴파일 실패)](#16)
17. [Out of Line Definition Error for Constrained Function of Template Class (컴파일 실패)](#17)
19. [Clang crash: Assertion DT.dominates(RHead, LHead) && "No dominance between recurrences used by one SCEV?"' failed. (컴파일 실패)](#19)
20. [Worse code gen when integer is wrapped in struct (컴파일러 버그)](#20)
21. [Clang cuda functions not handling concepts correctly. (컴파일 실패)](#21)
22. [odd code generated for swapping... (컴파일 실패)](#22)
23. [clang places calls to operator delete even for noexcept constructors (컴파일 실패)](#23)
24. [Assertion failure with constrained parameter referring to previous parameter (컴파일 실패)](#24)
30. [Stateful failure to evaluate lambda concept constraint from conditional explicit specifier (컴파일 실패)](#30)
36. [clang dies with SIGBUS compiling gtest-all.cc on 32-bit SPARC (컴파일 실패)](#36)
37. [Clang crash: Assertion `(Op == Instruction::BitCast || Op == Instruction::PtrToInt || Op == Instruction::IntToPtr) && "InsertNoopCastOfTo cannot perform non-noop casts!" failed.` (컴파일 실패)](#37)
38. [Clang frontend C++ crash with capture-default in concept (컴파일 실패)](#38)
39. [Clang frontend C++ crash with atomic constraints (컴파일 실패)](#39)
40. [[clang] Issues with determining valid constant expressions in `cxx2b` (컴파일 실패)](#48)
41. [Clang incorrectly complains about default template argument not being reachable (컴파일 실패)](#49)
42. [[clang/c++/coroutines] -Wunused-parameter not working with coroutines. (컴파일 경고 누락)](#55)
43. [Failure to match alias template against template template parameter(컴파일 실패)](#58)
44. [clang: concept checking bug in out-of-line definitions of inner class member functions (컴파일 실패)](#59)
45. [Clang cannot use _Atomic qualified integer type as controlling expression in switch statement (컴파일 실패)](#60)
46. [Clang and GCC differ in instantiation strategy of constexpr and incomplete types (컴파일 실패)](#77)
48. [[coroutines] miscompilation in clang 16 trunk vs clang 15 (컴파일 실패 인듯 ?)](#94)
46. [](#)
46. [](#)
46. [](#)
46. [](#)
46. [](#)
46. [](#)
46. [](#)
46. [](#)
46. [](#)
46. [](#)
46. [](#)
46. [](#)
46. [](#)
46. [](#)
46. [](#)
46. [](#)
46. [](#)
. [](#)
. [](#)
. [](#)

## 1
### compiler : `LLVM`
### title : `wrong code at -O1 and above on x86_64-linux-gnu`
### open_at : `2023-10-22T16:48:45Z`
### link : https://github.com/llvm/llvm-project/issues/69885
### status : `open`
### tags : `miscompilation, llvm:optimizations, `
### content : 
This seems to be a recent regression.

Compiler Explorer: https://godbolt.org/z/T7ET4PWsW

```
[573] % clangtk -v
clang version 18.0.0 (https://github.com/llvm/llvm-project.git 00c8da615923974c6c91603555b723c600dbb5f2)
Target: x86_64-unknown-linux-gnu
Thread model: posix
InstalledDir: /local/suz-local/opfuzz/bin
Found candidate GCC installation: /usr/lib/gcc/x86_64-linux-gnu/10
Found candidate GCC installation: /usr/lib/gcc/x86_64-linux-gnu/11
Found candidate GCC installation: /usr/lib/gcc/x86_64-linux-gnu/9
Selected GCC installation: /usr/lib/gcc/x86_64-linux-gnu/11
Candidate multilib: .;@m64
Selected multilib: .;@m64
[574] % 
[574] % clangtk -O1 small.c
[575] % ./a.out
Aborted
[576] % cat small.c
#pragma pack(1)
struct {
  int : 2;
  int a : 2;
  int b : 30;
} c;
int d, e = -1;
int main() {
  int f = ~(e & 1);
  c.a = -(f | d) ^ -c.a;
  if (c.b != 0)
    __builtin_abort();
  return 0;
}
```


---

## 2
### compiler : `LLVM`
### title : `LoopVectorize Miscompilation with Aliases in clang 15+`
### open_at : `2023-10-20T17:53:21Z`
### link : https://github.com/llvm/llvm-project/issues/69744
### status : `open`
### tags : `miscompilation, vectorization, `
### content : 
We believe there is a problem in LoopAccessAnalysis or LoopVectorize that caused the following code snippet to produce wrong result.

LoopAccessAnalysis나 LoopVectorize에 문제가 있어서 아래의 코드 스니펫이 잘못된 결과를 생성한다고 생각합니다.

Compiler command 
```
clang -Xclang -target-cpu -Xclang haswell -Xclang -tune-cpu -Xclang skylake -O2 repro.c
```

repro.c
```c
#include <stdio.h>
#include <stdlib.h>

typedef struct {
  unsigned long long ref_count;
} MyObject;

static int mycount(MyObject** arr) {
  MyObject** old_arr = arr;
  while (*arr++)
    ;
  return (int)(arr - old_arr) - 1;
}

void my_inplace_repeat(MyObject** arr, int times) {
  int orig_elem_count = mycount(arr);
  int pos = orig_elem_count;
  for (int i = 1; i < times; i++) {
    for (int j = 0; j < orig_elem_count; j++) {
      MyObject* obj = arr[j];
      obj->ref_count++;
      arr[pos++] = obj;
    }
  }
  arr[pos] = 0; // NULL terminated list
}

MyObject* obj_alloc() {
  printf("allocating\n");
  MyObject* ret = malloc(sizeof(MyObject));
  ret->ref_count = 1;
  return ret;
}

int main() {
  MyObject** arr = malloc(sizeof(MyObject*) * 1000);
  arr[0] = obj_alloc();
  arr[1] = 0;

  my_inplace_repeat(arr, 4);
  my_inplace_repeat(arr, 2);

  int count = mycount(arr);
  printf("count = %d\n", count);
  for (int i = 0; i < count; i++) {
    if (arr[i]->ref_count != count) {
      printf("BUG: ref_count should be %d, but %llu was found.\n", count,
      arr[i]->ref_count); return 1;
    }
  }
  return 0;
} 
```

---

# 3
### compiler : `LLVM`
### title : `Failure to remove mask from shift amounts in unrolled loop`
### open_at : `2023-10-18T17:17:28Z`
### link : https://github.com/llvm/llvm-project/issues/69486
### status : `open`
### tags : `llvm:codegen, `
### content : 
This code generates unnecessary `and` instructions on the shift amounts when the loop is unrolled

```
#include <stddef.h>

void foo(unsigned *a, size_t n, unsigned x) {
  #pragma unroll(8)
  for (size_t i = 0; i != n; ++i)
    a[i] = x << (i & 31);
}
```

The computeKnownBits in the middle end is able to prove that some bits of the unrolled induction variable are 0 and that causes InstCombine to change the AND mask from 31, to 24, 25, 26, 27, etc.

SelectionDAG's computeKnownBits and AssertZExt nodes are unable to get the same known zero bits that InstCombine saw due to the phi recurrence. This prevents SelectionDAG from converting the AND mask back to 31 to remove it during instruction selection.

https://godbolt.org/z/cfGd7rWfz

cc: @nikic @RKSimon @efriedma-quic @goldsteinn `


---

# 4
### compiler : `LLVM`
### title : `Bug in mips64el: Varied Output by Clang Optimization Levels`
### open_at : `2023-10-17T13:20:53Z`
### link : https://github.com/llvm/llvm-project/issues/69328
### status : `open`
### tags : `backend:MIPS, llvm:optimizations, `
### content : 



## Proof of Concept
```
#include <stdio.h>

long long var_0 = 9129318035724831661LL;
unsigned long long var_6 = 15327265744474054469ULL;
int var_14 = 0;
unsigned int var_17 = 1;
unsigned int arr_0 [8];
unsigned char arr_1 [8] = { 0 };
unsigned long long arr_9 [8] [8] ;
unsigned long long  var_24 = 1;
signed char arr_4 [8] [8];
unsigned int arr_22 [20] [20] ;

void test(unsigned long long var_6, int var_14, unsigned int var_17, unsigned int arr_0 [8] , unsigned char arr_1 [8]) {
    for (unsigned int i_0 = var_14; i_0 < ((((unsigned int) var_0)) - (1626475429U))/*8*/; i_0 += 4) 
    {
        printf("var0: %d\n", ((unsigned int)(var_0)-(1626475429U)));
        arr_4[i_0][i_0] = arr_1 [i_0];

        for (int i_1 = (int)((( arr_0 [i_0])) - (2482776649ULL))/*2*/; i_1 < 4; i_1 += 2) 
        {
            printf("i_1: %llu\n", ((size_t)(2482776651U))-(2482776649ULL));
        }
    }
    var_24 = (int) ((var_6));
    for (long long int i_4 = 0; i_4 < 20; i_4 += 4) 
    {
        arr_22 [i_4] [i_4] = var_17;
    } 
}

int main() {
    for (size_t i_0 = 0; i_0 < 8; ++i_0) 
        arr_0 [i_0] = 2482776651U;

    test(var_6, var_14, var_17, arr_0 , arr_1 );
    printf("var_24 value: %llu\n", var_24);
}
```

### Expected Behavior


In the first for loop, the result of the condition expression `((((unsigned int) var_0)) - (1626475429U))` is 8. This is verified through the output of the following printf() function, which consequently determines the number of loop iterations.

In the second for loop, the calculation `(int)((( arr_0 [i_0])) - (2482776649ULL))` results in a value of 2 for i_1. This is also confirmed through the output of the printf() function, which aids in determining the number of times the loop will execute.

This code also performs unknown behavior.
Can you tell me why these results are coming out?`


---

# 5
### compiler : `LLVM`
### title : `Wrong code at -O1/2/s on x86_64-linux_gnu since 669ddd1`
### open_at : `2023-10-17T07:17:12Z`
### link : https://github.com/llvm/llvm-project/issues/69293
### status : `open`
### tags : `miscompilation, llvm:optimizations, `
### content : 
Clang at -O1/2/s produced the wrong code.

Bisected to 669ddd1e9b1226432b003dbba05b99f8e992285b, which was committed by @aeubanks 

Compiler explorer: https://godbolt.org/z/sGM1v4jd1

```console
% cat a.c
int printf(const char *, ...);
long a;
int b, c, e, g, i;
long *d, *h;
char f = -26;
int main() {
  long j;
  c = 0;
  for (; c != 7; ++c) {
      long k=0;
      long l = k;
          long **m = &d;
      for (; f + i!=0; i++)
        h = &l;
          g = h != (*m = &j);
      int *n = &b;
          *n = g;
      for (; e;)
        for (; a; a = a + 1)
            ;
        }
    printf("%d\n", b);
}
%
% clang -O0 a.c && ./a.out
1
%
% clang -fsanitize=address,undefined a.c && ./a.out
1
% clang -fsanitize=memory a.c && ./a.out
1
% clang -O1 a.c && ./a.out
0
%
```


---

# 6
### compiler : `LLVM`
### title : `wrong code at -O1 and above on x86_64-linux-gnu `
### open_at : `2023-10-16T14:18:38Z`
### link : https://github.com/llvm/llvm-project/issues/69210
### status : `open`
### tags : `miscompilation, llvm:optimizations, `
### content : 
It seems to be a recent regression. 

Compiler Explorer: https://godbolt.org/z/Ee8M1Ge3e

```
[535] % clangtk -v
clang version 18.0.0 (https://github.com/llvm/llvm-project.git f41ec27f7eba34548a280a4a4d7de2ef32837210)
Target: x86_64-unknown-linux-gnu
Thread model: posix
InstalledDir: /local/suz-local/opfuzz/bin
Found candidate GCC installation: /usr/lib/gcc/x86_64-linux-gnu/10
Found candidate GCC installation: /usr/lib/gcc/x86_64-linux-gnu/11
Found candidate GCC installation: /usr/lib/gcc/x86_64-linux-gnu/9
Selected GCC installation: /usr/lib/gcc/x86_64-linux-gnu/11
Candidate multilib: .;@m64
Selected multilib: .;@m64
[536] % 
[536] % clangtk -O0 small.c; ./a.out
0
[537] % clangtk -O1 small.c; ./a.out
2
[538] % cat small.c
int printf(const char *, ...);
#pragma pack(1)
struct {
  int : 1;
  int b : 18;
  int : 12;
  int c : 8;
  int : 23;
} d;
unsigned short a, e, f;
static long g = 1;
int h;
void l(long *i) {
  char j = f;
  h = ~(1 && g);
  d.b = ~((h ^ e) | j);
}
int main() {
  l(&g);
  for (; a < 1; a++)
    printf("%d\n", d.c);
  return 0;
}
```


---

# 7
### compiler : `LLVM`
### title : `Wrong code at -O2 on x86_64-linux_gnu since ca18e21`
### open_at : `2023-10-15T09:19:21Z`
### link : https://github.com/llvm/llvm-project/issues/69097
### status : `open`
### tags : `miscompilation, `
### content : 
Clang at -O2 produced the wrong code.

Bisected to ca18e21951a89f3115694fc64cd64a4b06cd5873, which was committed by @nikic 

Compiler explorer: https://godbolt.org/z/5Kvbqqjqd

```console
% cat a.c
int printf(const char *, ...);
int a = -6, b, c, e, f;
static unsigned char d;
short g;
static unsigned char *h = &d;
int *i = &b;
int j(int k) { return k << 2 & a; }
int main() {
  unsigned char **l[2];
  l[f] = &h;
  g = 4;
  for (; g != -15; g--) {
    *i = 0;
    c = 2;
    for (; j(10) - 40 + c >= -1; --c)
      ;
  }
  for (; c + *h + e != -1; ++e)
    ;
  printf("%d\n", e);
}
%
% clang -O0 a.c && ./a.out
1
% clang -O2 a.c && ./a.out
(Timeout)
%
```


---

# 8
### compiler : `LLVM`
### title : `Wrong code at -O2/3/s on x86_64-linux_gnu since 45ecfed`
### open_at : `2023-10-15T09:04:12Z`
### link : https://github.com/llvm/llvm-project/issues/69096
### status : `closed`
### tags : `miscompilation, llvm:analysis, `
### content : 
clang at -O2/3/s produced the wrong code.

Bisected to 45ecfed6c636d06f76bca0a44803e945cdae9506, which was committed by @FabianWolff 

Compiler explorer: https://godbolt.org/z/jT73jv5aG

```console
% cat a.c
int printf(const char *, ...);
int a, b;
short c;
unsigned short e = 65535;
static short f;
static char g[10][1][4];
static long h = -10;
unsigned short *i = &e;
long j(long k, long l) {
  long d = k + l;
  return k ? d - 1 : 9;
}
void n() {
  int m = 0;
  --g[0][0][2];
  c = 0;
  for (; c >= 0; c--)
    for (; h + *i - 65525 + m >= 0; m--) {
      f = 2;
      for (; f < 4; f++)
        g[(char)j(91, *i - 65625)][*i + c - 65535][f] = 5;
    }
}
int main() {
  n();
  printf("%d\n", g[0][0][2]);
}
%
% clang -O0 a.c && ./a.out
5
% clang -O2 a.c && ./a.out
-1
%
```


---

# 9
### compiler : `LLVM`
### title : `Wrong code at -Os on x86_64-linux_gnu since 5dde9c1`
### open_at : `2023-10-12T10:25:39Z`
### link : https://github.com/llvm/llvm-project/issues/68871
### status : `open`
### tags : `backend:X86, miscompilation, `
### content : 
Clang at -Os produced the wrong code.

Bisected to 5dde9c1286c9360cdc3aa07a1d69ff41f941e4f7, which was committed by @RKSimon 

Compiler explorer: https://godbolt.org/z/dnPaaoYfb

```console
% cat a.c
int printf(const char *, ...);
static int a = -3, b;
static char c;
int d;
int e(int f, int g) {
  if (f - g < 10000)
    return f;
  return f + 1 % -f;
}
int main() {
  int *h[] = {&a, &a};
  for (; c <= 37; ++c) {
    int *i = &b;
    *i |= e(a, 8) + d;
  }
  printf("%d\n", b);
}
%
% clang -O0 a.c && ./a.out
-3
% clang -Os a.c && ./a.out
-1
%
```


---

# 10
### compiler : `LLVM`
### title : `Clang's Optimization Introduces Unexpected Sign Extension in RISC-V Bit-Field Operations`
### open_at : `2023-10-12T06:46:11Z`
### link : https://github.com/llvm/llvm-project/issues/68855
### status : `closed`
### tags : `miscompilation, confirmed, llvm:SelectionDAG, `
### content : 
### **Environment:**

- Compiler: Clang-18
- Target Architecture: RISC-V
- Optimization Level: **`-O1`**, **`-O2`**, **`-O3`**
- OS: (Ubuntu 22.04.2)

### **Summary:**

While compiling code that deals with bit field operations and type casting, an unexpected behavior was noticed with optimization levels **`-O1`**, **`-O2`**, and **`-O3`** in Clang for the RISC-V architecture. The behavior deviates from the expected results based on the C language standard and is not observed in the **`-O0`** optimization level.

### **Steps to Reproduce:**

1. Compile the provided source code with Clang targeting RISC-V architecture.
2. Use optimization levels **`-O1`**, **`-O2`**, or **`-O3`**.
3. Execute the compiled binary.

### **Expected Result:**

```
resultValue1: ffff
resultValue2: 0
```

### **Actual Result:**

```
resultValue1: ffffffff
resultValue2: 0
```

### **Source Code to Reproduce:**

```c
#include<stdio.h>

typedef struct {
    unsigned int bitField : 13;
} CustomStruct;

unsigned int resultValue1 = 0;
short resultValue2 = 0;
CustomStruct customArray[2] = {{0U} , {0U}};

int main()
{
    resultValue1 = (unsigned int) ((unsigned short) (~(customArray[0].bitField)));
    printf("resultValue1: %x\n", resultValue1);

    resultValue2 = (short) (customArray[1].bitField);   
    printf("resultValue2: %x\n", resultValue2);
    return 0;
}
```

### **Observation:**

The value for **`customArray[0].bitField`** is a 13-bit unsigned integer defined as a bit field. When all bits of this field are inverted using the **`~`** operator, all 13 bits are set to 1, producing a value of 0x1FFF.

Casting this value to **`(unsigned short)`** results in a 16-bit (2 bytes) value, which should then be 0xFFFF.

Further casting this value to **`(unsigned int)`** should maintain the value at 0xFFFF. This is the expected behavior as per the C language standard for type casting.

However, in the provided code, while this is the case without optimization (-O0), with optimization the value unexpectedly becomes 0xFFFFFFFF. It seems that after the cast to **`unsigned short`**, the extension to **`unsigned int`** isn't carried out correctly, possibly sign-extending rather than zero-extending the value.

This unexpected behavior suggests a potential issue with either a specific implementation of the RISC-V architecture or with this version of the Clang compiler. Such an action deviates from the expected behavior of standard C, indicating a probable compiler bug.

### **Additional Information**:

- https://godbolt.org/z/Pv3Gaacv9
- The issue seems to stem from the **`slli`** and **`srli`** instructions used in succession in the optimized versions, resulting in sign-extension.

### **Recommendation**:

Please verify the behavior observed using the provided Godbolt link and investigate the underlying cause in the Clang compiler for RISC-V. It's essential to ensure consistent behavior across optimization levels and adherence to the C language standard.


---

# 11
### compiler : `LLVM`
### title : `Missed optimization: Reorder deallocations before allocations of unrelated memory`
### open_at : `2023-10-05T23:17:43Z`
### link : https://github.com/llvm/llvm-project/issues/68365
### status : `open`
### tags : `c++, llvm:optimizations, `
### content : 
Note: I am not certain which language standards allow this optimization, if any.

If we could move deallocations to occur before allocations of unrelated memory, it would reduce peak memory usage and potentially improve cache performance.

In other words, in the following example I would like to transform `bad` into `good`.

```cpp
int * bad(int * ptr) {
	auto temp = static_cast<int *>(operator new(10 * sizeof(int)));
	operator delete(ptr);
	return temp;
}

int * good(int * ptr) {
	operator delete(ptr);
	return static_cast<int *>(operator new(10 * sizeof(int)));
}
```

https://godbolt.org/z/WGq1jsdGd

With similar ability for things like `malloc` and `free`.`


---

# 12
### compiler : `LLVM`
### title : `Conversion of _Float16 for variadic functions doesn't seem to work`
### open_at : `2023-10-05T17:46:28Z`
### link : https://github.com/llvm/llvm-project/issues/68338
### status : `closed`
### tags : `backend:AArch64, backend:RISC-V, miscompilation, floating-point, `
### content : 
Converting `_Float16` to `double` to pass to a regular function looks fine, but doing the conversion for a variadic function (like `printf()` does not work.

That is to say, the instruction to convert the bit pattern from 16-bit to 64-bit is omitted when passing the register as a variadic argument, but that same operation _does_ happen when passing the value to a function expecting a double.

`__fp16` gets converted to `double` just fine in both cases.

https://godbolt.org/z/r5o7djxbd

Observed on RISC-V and aarch64.`


---

# 13
### compiler : `LLVM`
### title : `Clang fails to remove unnecessary loop`
### open_at : `2023-10-05T04:45:23Z`
### link : https://github.com/llvm/llvm-project/issues/68282
### status : `open`
### tags : `loopoptim, llvm:optimizations, missed-optimization, `
### content : 
The compiler seems to be pre-computing the result, but then it also doesnt remove the loop that was there to compute the value

컴파일 타임에 모두 평가되어야 하지만, 실제로 평가되지 못함

```cpp
#include <cstdint>

template<std::size_t Index>
static void testForLoop01(int32_t* valuesNew) {
    if constexpr (Index < 8) {
        *valuesNew += *valuesNew + Index;
        testForLoop01<Index + 1>(valuesNew);
    }
}

static void testForLoop02(int32_t* valuesNew) {
    for (uint64_t x = 0; x < 8; ++x) {
        *valuesNew += *valuesNew + x;
    }
}

int a() {
    int outputValue = 0;
    for (uint64_t x = 0; x < 1024 * 1024; ++x) {
        testForLoop01<0>(&outputValue);
    }
    return outputValue;
}
```

```x86asm
a():                                  # @a()
        mov     eax, 1048576
.LBB0_1:                                # =>This Inner Loop Header: Depth=1
        add     rax, -8
        jne     .LBB0_1
        mov     eax, -134744073
        ret
```

godbolt link: https://godbolt.org/z/ba4xox9fv


---

# 14
### compiler : `LLVM`
### title : `Wrong code at -O2 on x86_64-linux_gnu since 3ddd1ff`
### open_at : `2023-10-04T21:05:08Z`
### link : https://github.com/llvm/llvm-project/issues/68260
### status : `closed`
### tags : `miscompilation, llvm:SCEV, `
### content : 
clang at -O2 produced the wrong code.

Bisected to 3ddd1ffb721dd0ac3faa4a53c76b6904e862b7ab, which was committed by @nikic 

Compiler explorer: https://godbolt.org/z/rEv69ovMj

```console
% cat a.c
int printf(const char *, ...);
char *a;
long b, c, d, m;
int e, f, j, l;
short g;
int *k = &j;
int main() {
  int *n[] = {&f, &f, &f, &f, &f, &e};
  d = 0;
  for (; d <= 1; d++) {
    g = 0;
    for (; g <= 4; g++) {
      char h[] = {0, 0, 4};
      char *i = h;
      a = i;
      do {
        a++;
        b /= 10;
      } while (b);
      c = a - i;
      while (i < a){
        *i = *(i+1);
        i++;
      }
      *k ^= c;
      k = n[d + g];
      l ^= m;
    }
  }
  printf("%d\n", e);
}
%
% clang -O0 a.c && ./a.out
0
% clang -O2 a.c && ./a.out
1
%
```


---

# 15
### compiler : `LLVM`
### title : `Too aggresive C++23 static call operator optimization`
### open_at : `2023-10-02T11:36:14Z`
### link : https://github.com/llvm/llvm-project/issues/67976
### status : `open`
### tags : `bug, clang:frontend, clang:codegen, c++23, `
### content : 
Hello,

It looks like clang is too aggressive for C++23 static call optimization. Here is the simplified example of real code:

<!-- ```cpp
#include <functional>
#include <iostream>

template <typename Tag>
struct Wrapper {
    template <typename F, typename... Args>
    static void operator()(F&& callable, Args&&... args) {
        Invoke(std::forward<F>(callable), std::forward<Args>(args)...);
    }

    template <typename F, typename... Args>
    static void Invoke(F&& callable, Args&&... args) {
        std::invoke(std::forward<F>(callable), std::forward<Args>(args)...);
    }
};

struct Manager {
    template <typename SingletonClass>
    static SingletonClass& Get() {
        std::cout << "get call\n";
        static SingletonClass instance;
        return instance;
    }
};

struct Tag {};

int main()
{
    using TaggedWrapper = Wrapper<Tag>;
    Manager::Get<TaggedWrapper>()([] { std::cout << "Function\n"; });
}
``` -->

We assume that Manager::Get() will be called and `get call` will be printed, but it doesn't happen. If change call in main to `    Manager::Get<TaggedWrapper>().Invoke([] { std::cout << "Function\n"; });` it works as expected. `get cal` also will be printed if remove `static` from `operator()`. It reproducible even with `-O0`. clang-17.0.1

Reduced code: https://godbolt.org/z/q84zajYGs

```cpp
#include <iostream>

struct Wrapper {
    static void operator()() {
        std::cout << "Function\n";
    }
};

static Wrapper instance;
struct Manager {
    static Wrapper& Get() {
        std::cout << "get call\n";
        return instance;
    }
};

int main() {
    Manager::Get()();
    return 0;
}
```
The expression Manager::Get() is not evaluated.

---

# 16
### compiler : `LLVM`
### title : ` [C++17][clang:Frontend] Clang can't deduce the correct deduction guide.`
### open_at : `2023-10-02T08:33:02Z`
### link : https://github.com/llvm/llvm-project/issues/67959
### status : `closed`
### tags : `c++17, clang:frontend, `
### content : 
If there are two auto generated deduction guides from a templated and a non templated constructor we should choose the guide generated from the non-templated constructor. But clang can't deduce which one should we use. (gcc can)

즉, #1, #2가 모호하다고 판단 -> 버그

https://godbolt.org/z/ee3e9qG78

```cpp
template<class T>
struct A
{
    A(T, T, int);  //#1
 
    template<class U>
    A(int, T, U);  //#2
};                 
 
int main() {
    A x(1, 2, 3); // Should choose #1
}
```



---

# 17
### compiler : `LLVM`
### title : `Out of Line Definition Error for Constrained Function of Template Class`
### open_at : `2023-10-01T16:25:17Z`
### link : https://github.com/llvm/llvm-project/issues/67926
### status : `open`
### tags : `c++20, clang:frontend, `
### content : 
Very similar to #62003, except the constraint has an extra template parameter, which is passed from the class' member type.

FYI @alexander-shaposhnikov. [Example on godbolt](https://godbolt.org/#g:!((g:!((g:!((h:codeEditor,i:(filename:'1',fontScale:14,fontUsePx:'0',j:1,lang:c%2B%2B,selection:(endColumn:1,endLineNumber:16,positionColumn:1,positionLineNumber:16,selectionStartColumn:1,selectionStartLineNumber:16,startColumn:1,startLineNumber:16),source:'%0A%0Atemplate+%3Ctypename+A,+typename+T%3E%0Aconcept+constraint+%3D+true%3B%0A++++%0Atemplate+%3Ctypename+T%3E%0Astruct+Foo+%7B%0A++++struct+Bar+%7B%7D%3B%0A++++template+%3Cconstraint%3CBar%3E+U%3E%0A++++++++void+baz+(U+baz)%3B%0A%7D%3B%0A++++%0Atemplate+%3Ctypename+T%3E%0Atemplate+%3Cconstraint%3Ctypename+Foo%3CT%3E::Bar%3E+U%3E%0Avoid+Foo%3CT%3E::baz+(U+baz)+%7B%7D%0A'),l:'5',n:'0',o:'C%2B%2B+source+%231',t:'0')),k:52.47813411078717,l:'4',m:100,n:'0',o:'',s:0,t:'0'),(g:!((g:!((h:compiler,i:(compiler:clang_trunk,deviceViewOpen:'1',filters:(b:'0',binary:'1',binaryObject:'1',commentOnly:'0',debugCalls:'1',demangle:'0',directives:'0',execute:'1',intel:'0',libraryCode:'0',trim:'1'),flagsViewOpen:'1',fontScale:14,fontUsePx:'0',j:1,lang:c%2B%2B,libs:!(),options:'-std%3Dc%2B%2B20',overrides:!(),selection:(endColumn:1,endLineNumber:1,positionColumn:1,positionLineNumber:1,selectionStartColumn:1,selectionStartLineNumber:1,startColumn:1,startLineNumber:1),source:1),l:'5',n:'0',o:'+x86-64+clang+(trunk)+(Editor+%231)',t:'0')),header:(),k:44.584286803966435,l:'4',m:50,n:'0',o:'',s:0,t:'0'),(g:!((h:output,i:(compilerName:'x86-64+gcc+12.2',editorid:1,fontScale:14,fontUsePx:'0',j:1,wrap:'1'),l:'5',n:'0',o:'Output+of+x86-64+clang+(trunk)+(Compiler+%231)',t:'0')),header:(),l:'4',m:50,n:'0',o:'',s:0,t:'0')),k:47.52186588921283,l:'3',n:'0',o:'',t:'0')),l:'2',n:'0',o:'',t:'0')),version:4).

```cpp
template <typename A, typename T>
concept constraint = true;
    
template <typename T>
struct Foo {
    struct Bar {};
    template <constraint<Bar> U>
        void baz (U baz);
};
    
template <typename T>
template <constraint<typename Foo<T>::Bar> U>
void Foo<T>::baz (U baz) {}
```
```
error: out-of-line definition of 'baz' does not match any declaration in 'Foo<T>'
   15 | void Foo<T>::baz (U baz) {}
      |              ^~~
```


---

# 18
### compiler : `LLVM`
### title : `abs from cmath is not constexpr when it should be [C++23]`
### open_at : `2023-10-01T05:18:19Z`
### link : https://github.com/llvm/llvm-project/issues/67901
### status : `open`
### tags : `c++23, `
### content : 
https://eel.is/c++draft/c.math.abs
https://en.cppreference.com/w/cpp/numeric/math/abs (constexpr since C++23)
https://godbolt.org/z/bq5coPsMo <-- demonstrating abs is not usable in constant expressions
Tried it locally with version 17.0.1 as well, didn't work

```cpp
// -std=c++23
#include <cmath>
#include <iostream>

constexpr auto val = abs(12);
int main() {
    std::cout << val;
}
```

---

# 19
### compiler : `LLVM`
### title : `Clang crash: Assertion `DT.dominates(RHead, LHead) && "No dominance between recurrences used by one SCEV?"' failed.`
### open_at : `2023-09-29T11:58:55Z`
### link : https://github.com/llvm/llvm-project/issues/67794
### status : `open`
### tags : `backend:X86, llvm:codegen, llvm:crash, llvm:SCEV, `
### content : 
Clang at -O2 crashes.

Bisected to 7abe3497e72af3ddee789dfc62c63a981a25dbf6, which was committed by @davemgreen 

Compiler explorer: https://godbolt.org/z/hPTj849f6

```cpp
% cat a.c
int a, l;
short b, e;
unsigned c, d;
char f;
char *g;
static char **h = &g;
long j;
static signed char m(int);
void n() { m(0); }
signed char m(int t) {
  char o;
  char p[80];
  for (; t <= 3; t++) {
    int i = 0;
    for (; i < 2; i++)
      for (;;) {
        unsigned *q = &c, *r = &d;
        short *s = &e;
        l = ++*r;
        *q = (5 && l) / a;
        *s = c;
        if ((char)d + d)
          e = 0;
        o = *g;
        **h = o;
        break;
      }
    for (; f & 3;)
      for (; d <= 3; d++)
        for (; 127 + **h; j++)
          p[t + **h + j] && (b = 8);
    char ***k = &h;
    &k == 0;
  }
  return 0;
}
int main() {}
%
```

<details><summary>컴파일 오류</summary>
<p>

```
% clang -O2 a.c
<a.c>:33:6: warning: comparison of address of 'k' equal to a null pointer is always false [-Wtautological-pointer-compare]
   33 |     &k == 0;
      |      ^    ~
<a.c>:33:8: warning: equality comparison result unused [-Wunused-comparison]
   33 |     &k == 0;
      |     ~~~^~~~
clang: /root/llvm-project/llvm/lib/Analysis/ScalarEvolution.cpp:740: std::optional<int> CompareSCEVComplexity(llvm::EquivalenceClasses<const llvm::SCEV*>&, llvm::EquivalenceClasses<const llvm::Value*>&, const llvm::LoopInfo*, const llvm::SCEV*, const llvm::SCEV*, llvm::DominatorTree&, unsigned int): Assertion `DT.dominates(RHead, LHead) && "No dominance between recurrences used by one SCEV?"' failed.
PLEASE submit a bug report to https://github.com/llvm/llvm-project/issues/ and include the crash backtrace, preprocessed source, and associated run script.
Stack dump:
0.	Program arguments: /opt/compiler-explorer/clang-assertions-trunk/bin/clang -gdwarf-4 -g -o /app/output.s -S --gcc-toolchain=/opt/compiler-explorer/gcc-9.2.0 -fcolor-diagnostics -fno-crash-diagnostics -O2 <source>
1.	<eof> parser at end of file
2.	Code generation
3.	Running pass 'Function Pass Manager' on module '<source>'.
4.	Running pass 'Loop Pass Manager' on function '@n'
5.	Running pass 'Loop Strength Reduction' on basic block '%for.cond1.preheader.i'
 #0 0x000000000370a088 llvm::sys::PrintStackTrace(llvm::raw_ostream&, int) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+0x370a088)
 #1 0x0000000003707d4c llvm::sys::CleanupOnSignal(unsigned long) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+0x3707d4c)
 #2 0x00000000036509a8 CrashRecoverySignalHandler(int) CrashRecoveryContext.cpp:0:0
 #3 0x00007fce57d2f420 __restore_rt (/lib/x86_64-linux-gnu/libpthread.so.0+0x14420)
 #4 0x00007fce577f200b raise (/lib/x86_64-linux-gnu/libc.so.6+0x4300b)
 #5 0x00007fce577d1859 abort (/lib/x86_64-linux-gnu/libc.so.6+0x22859)
 #6 0x00007fce577d1729 (/lib/x86_64-linux-gnu/libc.so.6+0x22729)
 #7 0x00007fce577e2fd6 (/lib/x86_64-linux-gnu/libc.so.6+0x33fd6)
 #8 0x00000000028265bf CompareSCEVComplexity(llvm::EquivalenceClasses<llvm::SCEV const*, std::less<llvm::SCEV const*>>&, llvm::EquivalenceClasses<llvm::Value const*, std::less<llvm::Value const*>>&, llvm::LoopInfo const*, llvm::SCEV const*, llvm::SCEV const*, llvm::DominatorTree&, unsigned int) ScalarEvolution.cpp:0:0
 #9 0x000000000283989a void std::__merge_adaptive<llvm::SCEV const**, long, llvm::SCEV const**, __gnu_cxx::__ops::_Iter_comp_iter<GroupByComplexity(llvm::SmallVectorImpl<llvm::SCEV const*>&, llvm::LoopInfo*, llvm::DominatorTree&)::'lambda0'(llvm::SCEV const*, llvm::SCEV const*)>>(llvm::SCEV const**, llvm::SCEV const**, llvm::SCEV const**, long, long, llvm::SCEV const**, long, __gnu_cxx::__ops::_Iter_comp_iter<GroupByComplexity(llvm::SmallVectorImpl<llvm::SCEV const*>&, llvm::LoopInfo*, llvm::DominatorTree&)::'lambda0'(llvm::SCEV const*, llvm::SCEV const*)>) ScalarEvolution.cpp:0:0
#10 0x0000000002839ae8 void std::__stable_sort_adaptive<llvm::SCEV const**, llvm::SCEV const**, long, __gnu_cxx::__ops::_Iter_comp_iter<GroupByComplexity(llvm::SmallVectorImpl<llvm::SCEV const*>&, llvm::LoopInfo*, llvm::DominatorTree&)::'lambda0'(llvm::SCEV const*, llvm::SCEV const*)>>(llvm::SCEV const**, llvm::SCEV const**, llvm::SCEV const**, long, __gnu_cxx::__ops::_Iter_comp_iter<GroupByComplexity(llvm::SmallVectorImpl<llvm::SCEV const*>&, llvm::LoopInfo*, llvm::DominatorTree&)::'lambda0'(llvm::SCEV const*, llvm::SCEV const*)>) ScalarEvolution.cpp:0:0
#11 0x0000000002839fe0 GroupByComplexity(llvm::SmallVectorImpl<llvm::SCEV const*>&, llvm::LoopInfo*, llvm::DominatorTree&) ScalarEvolution.cpp:0:0
#12 0x0000000002855568 llvm::ScalarEvolution::getAddExpr(llvm::SmallVectorImpl<llvm::SCEV const*>&, llvm::SCEV::NoWrapFlags, unsigned int) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+0x2855568)
#13 0x0000000002857916 llvm::ScalarEvolution::getAddExpr(llvm::SmallVectorImpl<llvm::SCEV const*>&, llvm::SCEV::NoWrapFlags, unsigned int) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+0x2857916)
#14 0x0000000001926452 llvm::ScalarEvolution::getAddExpr(llvm::SCEV const*, llvm::SCEV const*, llvm::SCEV::NoWrapFlags, unsigned int) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+0x1926452)
#15 0x0000000002854b1c llvm::ScalarEvolution::getMinusSCEV(llvm::SCEV const*, llvm::SCEV const*, llvm::SCEV::NoWrapFlags, unsigned int) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+0x2854b1c)
#16 0x000000000353437b (anonymous namespace)::LSRInstance::NarrowSearchSpaceByPickingWinnerRegs() LoopStrengthReduce.cpp:0:0
#17 0x000000000355418e (anonymous namespace)::LSRInstance::LSRInstance(llvm::Loop*, llvm::IVUsers&, llvm::ScalarEvolution&, llvm::DominatorTree&, llvm::LoopInfo&, llvm::TargetTransformInfo const&, llvm::AssumptionCache&, llvm::TargetLibraryInfo&, llvm::MemorySSAUpdater*) LoopStrengthReduce.cpp:0:0
#18 0x000000000355544f ReduceLoopStrength(llvm::Loop*, llvm::IVUsers&, llvm::ScalarEvolution&, llvm::DominatorTree&, llvm::LoopInfo&, llvm::TargetTransformInfo const&, llvm::AssumptionCache&, llvm::TargetLibraryInfo&, llvm::MemorySSA*) LoopStrengthReduce.cpp:0:0
#19 0x0000000003558538 (anonymous namespace)::LoopStrengthReduce::runOnLoop(llvm::Loop*, llvm::LPPassManager&) LoopStrengthReduce.cpp:0:0
#20 0x000000000279adab llvm::LPPassManager::runOnFunction(llvm::Function&) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+0x279adab)
#21 0x000000000308fdc9 llvm::FPPassManager::runOnFunction(llvm::Function&) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+0x308fdc9)
#22 0x0000000003090001 llvm::FPPassManager::runOnModule(llvm::Module&) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+0x3090001)
#23 0x0000000003090822 llvm::legacy::PassManagerImpl::run(llvm::Module&) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+0x3090822)
#24 0x00000000039810f2 (anonymous namespace)::EmitAssemblyHelper::EmitAssembly(clang::BackendAction, std::unique_ptr<llvm::raw_pwrite_stream, std::default_delete<llvm::raw_pwrite_stream>>) BackendUtil.cpp:0:0
#25 0x0000000003981599 clang::EmitBackendOutput(clang::DiagnosticsEngine&, clang::HeaderSearchOptions const&, clang::CodeGenOptions const&, clang::TargetOptions const&, clang::LangOptions const&, llvm::StringRef, llvm::Module*, clang::BackendAction, llvm::IntrusiveRefCntPtr<llvm::vfs::FileSystem>, std::unique_ptr<llvm::raw_pwrite_stream, std::default_delete<llvm::raw_pwrite_stream>>) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+0x3981599)
#26 0x00000000049762bf clang::BackendConsumer::HandleTranslationUnit(clang::ASTContext&) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+0x49762bf)
#27 0x0000000005e71b09 clang::ParseAST(clang::Sema&, bool, bool) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+0x5e71b09)
#28 0x0000000004974a68 clang::CodeGenAction::ExecuteAction() (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+0x4974a68)
#29 0x00000000041d7bd9 clang::FrontendAction::Execute() (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+0x41d7bd9)
#30 0x000000000415898e clang::CompilerInstance::ExecuteAction(clang::FrontendAction&) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+0x415898e)
#31 0x00000000042b6dce clang::ExecuteCompilerInvocation(clang::CompilerInstance*) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+0x42b6dce)
#32 0x0000000000bdcd16 cc1_main(llvm::ArrayRef<char const*>, char const*, void*) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+0xbdcd16)
#33 0x0000000000bd45da ExecuteCC1Tool(llvm::SmallVectorImpl<char const*>&, llvm::ToolContext const&) driver.cpp:0:0
#34 0x0000000003fb6099 void llvm::function_ref<void ()>::callback_fn<clang::driver::CC1Command::Execute(llvm::ArrayRef<std::optional<llvm::StringRef>>, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char>>*, bool*) const::'lambda'()>(long) Job.cpp:0:0
#35 0x0000000003650e54 llvm::CrashRecoveryContext::RunSafely(llvm::function_ref<void ()>) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+0x3650e54)
#36 0x0000000003fb668f clang::driver::CC1Command::Execute(llvm::ArrayRef<std::optional<llvm::StringRef>>, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char>>*, bool*) const (.part.0) Job.cpp:0:0
#37 0x0000000003f7e9d5 clang::driver::Compilation::ExecuteCommand(clang::driver::Command const&, clang::driver::Command const*&, bool) const (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+0x3f7e9d5)
#38 0x0000000003f7f43d clang::driver::Compilation::ExecuteJobs(clang::driver::JobList const&, llvm::SmallVectorImpl<std::pair<int, clang::driver::Command const*>>&, bool) const (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+0x3f7f43d)
#39 0x0000000003f87365 clang::driver::Driver::ExecuteCompilation(clang::driver::Compilation&, llvm::SmallVectorImpl<std::pair<int, clang::driver::Command const*>>&) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+0x3f87365)
#40 0x0000000000bda1bc clang_main(int, char**, llvm::ToolContext const&) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+0xbda1bc)
#41 0x0000000000ad4f31 main (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+0xad4f31)
#42 0x00007fce577d3083 __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x24083)
#43 0x0000000000bd40be _start (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+0xbd40be)
clang: error: clang frontend command failed with exit code 134 (use -v to see invocation)
Compiler returned: 134
%
```
</p>
</details>



---

# 20
### compiler : `LLVM`
### title : `Worse code gen when integer is wrapped in struct`
### open_at : `2023-09-27T19:39:55Z`
### link : https://github.com/llvm/llvm-project/issues/67597
### status : `open`
### tags : `llvm:optimizations, `
### content : 
Compiling with `-std=c2x -O3`

```c
typedef struct {
	signed char m;
} schar;
typedef struct {
	unsigned char m;
} uchar;
bool a(signed char x, unsigned char y) {
	return x == y;
}
bool a2(schar x, uchar y) {
	return x.m == y.m;
}

typedef struct {
	short m;
} sshort;
typedef struct {
	unsigned short m;
} ushort;
bool b(short x, unsigned short y) {
	return x == y;
}
bool b2(sshort x, ushort y) {
	return x.m == y.m;
}

typedef struct {
	int m;
} sint;
typedef struct {
	unsigned m;
} uint;
bool c(int x, unsigned y) {
	return x == y;
}
bool c2(sint x, uint y) {
	return x.m == y.m;
}
```

causes clang to generate

```asm
a:                                      # @a
        cmp     edi, esi
        sete    al
        ret
a2:                                     # @a2
        movsx   eax, dil
        movzx   ecx, sil
        cmp     eax, ecx
        sete    al
        ret
b:                                      # @b
        cmp     edi, esi
        sete    al
        ret
b2:                                     # @b2
        movsx   eax, di
        movzx   ecx, si
        cmp     eax, ecx
        sete    al
        ret
c:                                      # @c
        cmp     edi, esi
        sete    al
        ret
c2:                                     # @c2
        cmp     edi, esi
        sete    al
        ret
```

See it live: https://godbolt.org/z/hbvEcjj6W

It's surprising to me that wrapping an integer in a struct causes worse code gen and hopefully this is just an optimization bug.`


---

# 21
### compiler : `LLVM`
### title : `Clang cuda functions not handling concepts correctly.`
### open_at : `2023-09-27T00:14:49Z`
### link : https://github.com/llvm/llvm-project/issues/67507
### status : `open`
### tags : `c++20, cuda, clang:frontend, `
### content : 
Take the example code posted below.

If I compile, I get this error
```
> clang++ -x cuda -c --cuda-gpu-arch=sm_70 -std=c++20 main.cc
clang++: warning: CUDA version is newer than the latest partially supported version 12.1 [-Wunknown-cuda-version]
root@3aa37681f2bd:/src/concept_bug# clang++ -x cuda -c --cuda-gpu-arch=sm_70 -std=c++20 main.cc
clang++: warning: CUDA version is newer than the latest partially supported version 12.1 [-Wunknown-cuda-version]
main.cc:116:3: error: no matching function for call to 'kernel'
  116 |   kernel<<<1, 1>>>(bucket_sums, generators, scalars, 0);
      |   ^~~~~~
main.cc:26:17: note: candidate template ignored: constraints not satisfied [with T = E]
   26 | __global__ void kernel(T* bucket_sums, const T* generators, const uint8_t* scalars,
      |                 ^
main.cc:25:11: note: because 'sxt::bascrv::element97' does not satisfy 'element'
   25 | template <bascrv::element T>
      |           ^
main.cc:13:3: note: because 'double_element(res, e)' would be invalid: no matching function for call to 'double_element'
   13 |   double_element(res, e);
      |   ^
1 error generated when compiling for sm_70.
```

But the concept element should be satified. In fact, if I uncomment the line
```
  // f(bucket_sums, generators, scalars, 0); // uncomment this line and things compile. ¯\_(ツ)_/
```
the compilation will succeed.

Here is the version of clang I'm using
```
clang++ --version
Ubuntu clang version 18.0.0 (++20230913042131+f3fdc967a87d-1~exp1~20230913042254.1182)
Target: x86_64-pc-linux-gnu
Thread model: posix
InstalledDir: /usr/bin
```


code:
```
#include <iostream>

// element.h
#include <cstdint>
#include <concepts>

namespace sxt::bascrv {
//--------------------------------------------------------------------------------------------------
// element
//--------------------------------------------------------------------------------------------------
template <class T>
concept element = requires(T& res, const T& e) {
  double_element(res, e);
  add(res, e, e);
  neg(res, e);
  add_inplace(res, res);
  { T::identity() } noexcept -> std::same_as<T>;
  mark(res);
  { is_marked(e) } noexcept -> std::same_as<bool>;
};
} // namespace sxt::bascrv

// kernel.h
namespace sxt::mtxbk {
template <bascrv::element T>
__global__ void kernel(T* bucket_sums, const T* generators, const uint8_t* scalars,
                       unsigned length) {
  (void)bucket_sums;
  (void)generators;
  (void)scalars;
  (void)length;
}

template <bascrv::element T>
void f(T* bucket_sums, const T* generators, const uint8_t* scalars, unsigned length) {
  (void)bucket_sums;
  (void)generators;
  (void)scalars;
  (void)length;
}
} // namespace sxt::mtxbk

// example_element.h
#include <cstdint>

namespace sxt::bascrv {
//--------------------------------------------------------------------------------------------------
// element97
//--------------------------------------------------------------------------------------------------
struct element97 {
  uint32_t value;
  bool marked = false;

  static element97 identity() noexcept {
    return {0};
  }

  bool operator==(const element97&) const noexcept = default;
};

//--------------------------------------------------------------------------------------------------
// double_element
//--------------------------------------------------------------------------------------------------
inline void double_element(element97& res, const element97& e) noexcept {
  res.value = (e.value + e.value) % 97u;
}

//--------------------------------------------------------------------------------------------------
// neg
//--------------------------------------------------------------------------------------------------
inline void neg(element97& res, const element97& e) noexcept {
  res.value = (97u - e.value) % 97u;
}

//--------------------------------------------------------------------------------------------------
// add
//--------------------------------------------------------------------------------------------------
inline void add(element97& res, const element97& x, const element97& y) noexcept {
  res.value = (x.value + y.value) % 97u;
}

//--------------------------------------------------------------------------------------------------
// add_inplace
//--------------------------------------------------------------------------------------------------
inline void add_inplace(element97& res, const element97& x) noexcept {
  res.value = (res.value + x.value) % 97u;
}

//--------------------------------------------------------------------------------------------------
// mark
//--------------------------------------------------------------------------------------------------
inline void mark(element97& res) noexcept {
  res.marked = true;
}

//--------------------------------------------------------------------------------------------------
// is_marked
//--------------------------------------------------------------------------------------------------
inline bool is_marked(const element97& e) noexcept {
  return e.marked;
}
} // namespace sxt::bascrv

// main
using namespace sxt;
using namespace sxt::mtxbk;

int main() {
  using E = bascrv::element97;
  E* bucket_sums = nullptr;
  const E* generators = nullptr;
  const uint8_t* scalars = nullptr;

  // f(bucket_sums, generators, scalars, 0); // uncomment this line and things compile. ¯\_(ツ)_/

  kernel<<<1, 1>>>(bucket_sums, generators, scalars, 0);

  return 0;
}
```


---

# 22
### compiler : `LLVM`
### title : `odd code generated for swapping...`
### open_at : `2023-09-26T22:30:29Z`
### link : https://github.com/llvm/llvm-project/issues/67497
### status : `open`
### tags : `llvm:optimizations, missed-optimization, `
### content : 
Clang has always had this odd detection for swapping - if you are swapping one register's worth of data (1,2,4,8, or 16 byte elements), it will detect this kind of code pattern:

int t = a; a = b; b = t;

But as soon as there are two registers worth of data (like a struct with 32 bytes - 2 16 byte regs, or a struct with 6 bytes - 1 int and short), it gives up and buffers the whole thing on the stack first and then moves things around.  GCC and MSVC both detect this swapping style code perfectly, no matter how big the struct it.

Here's a simple Compiler Explorer that shows the problem:

https://godbolt.org/z/Td63qr1r4

It's not a huge problem but I can measure it when sorting small structs.  And heck, even crappy 32-bit MSVC does this ok. 

```cpp
void swap32( void * a, void * b ) 
{ 
  typedef struct swapstruct { char t[ 32 ]; } swapstruct; 
  swapstruct tmp; 
  tmp = *(swapstruct*)a; 
  *(swapstruct*)a = *(swapstruct*)b; 
  *(swapstruct*)b = tmp; 
}

void swap6( void * a, void * b ) 
{ 
  typedef struct swapstruct { char t[ 6 ]; } swapstruct; 
  swapstruct tmp; 
  tmp = *(swapstruct*)a; 
  *(swapstruct*)a = *(swapstruct*)b; 
  *(swapstruct*)b = tmp; 
}

```

---

# 23
### compiler : `LLVM`
### title : `clang places calls to operator delete even for noexcept constructors`
### open_at : `2023-09-26T08:49:45Z`
### link : https://github.com/llvm/llvm-project/issues/67405
### status : `open`
### tags : `clang:codegen, `
### content : 
Unlike gcc, clang always turns compiler placed calls to operator delete for exception handling into hard errors if operator delete was marked deleted. gcc instead simply leaves out the call to operator delete in this situation. Issue of which compiler is conforming to the standard in this case aside, this is a huge problem for clang, because it is unable to see that noexcept constructors will never throw, which means you can't mark a constructor noexcept to prevent clang from putting that call to operator delete in there, which becomes a compilation breaking error if you want to delete operator delete for that class/struct:

https://godbolt.org/z/hvo8GY4nW

```cpp
#include <new>
#include <cinttypes>

struct Allocation {
    Allocation() noexcept;
    void operator delete(void*) = delete;
    void operator delete(void*, size_t) = delete;
};

int main() {
    Allocation* volatile pointer = new Allocation();
}
```

> clang++ -std=c++14 -emit-llvm -pedantic -c new.cpp

> new.cpp:11:40: error: attempt to use a deleted function
>     Allocation* volatile pointer = new Allocation();
>                        ^
> new.cpp:6:10: note: 'operator delete' has been explicitly marked deleted here
>     void operator delete(void*) = delete;
>          ^
> 1 error generated.


---

# 24
### compiler : `LLVM`
### title : `Assertion failure with constrained parameter referring to previous parameter`
### open_at : `2023-09-25T18:24:15Z`
### link : https://github.com/llvm/llvm-project/issues/67356
### status : `closed`
### tags : `c++20, concepts, confirmed, `
### content : 
The following valid C++ code

```cpp
template<typename, typename>
concept c = true;

template<typename T>
void a(T x, c<decltype(x)> auto) {
}

void b() {
	a(0, 0);
}
```
<details><summary>causes clang to crash with</summary>
<p>

```console
clang++: /root/llvm-project/clang/lib/AST/ItaniumMangle.cpp:5590: void {anonymous}::CXXNameMangler::mangleFunctionParam(const clang::ParmVarDecl*): Assertion `parmDepth < FunctionTypeDepth.getDepth()' failed.
PLEASE submit a bug report to https://github.com/llvm/llvm-project/issues/ and include the crash backtrace, preprocessed source, and associated run script.
Stack dump:
0.	Program arguments: /opt/compiler-explorer/clang-assertions-trunk/bin/clang++ -gdwarf-4 -g -o /app/output.s -mllvm --x86-asm-syntax=intel -S --gcc-toolchain=/opt/compiler-explorer/gcc-snapshot -fcolor-diagnostics -fno-crash-diagnostics -std=c++20 -w <source>
1.	<eof> parser at end of file
2.	<source>:8:6: LLVM IR generation of declaration 'b'
3.	<source>:8:6: Generating code for declaration 'b'
4.	<source>:5:6: Mangling declaration 'a'
 #0 0x00000000036f5d28 llvm::sys::PrintStackTrace(llvm::raw_ostream&, int) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+++0x36f5d28)
 #1 0x00000000036f39ec llvm::sys::CleanupOnSignal(unsigned long) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+++0x36f39ec)
 #2 0x000000000363c578 CrashRecoverySignalHandler(int) CrashRecoveryContext.cpp:0:0
 #3 0x00007fe4f43d1420 __restore_rt (/lib/x86_64-linux-gnu/libpthread.so.0+0x14420)
 #4 0x00007fe4f3e9400b raise (/lib/x86_64-linux-gnu/libc.so.6+0x4300b)
 #5 0x00007fe4f3e73859 abort (/lib/x86_64-linux-gnu/libc.so.6+0x22859)
 #6 0x00007fe4f3e73729 (/lib/x86_64-linux-gnu/libc.so.6+0x22729)
 #7 0x00007fe4f3e84fd6 (/lib/x86_64-linux-gnu/libc.so.6+0x33fd6)
 #8 0x00000000070e640c (anonymous namespace)::CXXNameMangler::mangleFunctionParam(clang::ParmVarDecl const*) ItaniumMangle.cpp:0:0
 #9 0x00000000070e2e43 (anonymous namespace)::CXXNameMangler::mangleExpression(clang::Expr const*, unsigned int, bool) ItaniumMangle.cpp:0:0
#10 0x00000000070d5213 (anonymous namespace)::CXXNameMangler::mangleType(clang::QualType) ItaniumMangle.cpp:0:0
#11 0x00000000070f11e0 (anonymous namespace)::CXXNameMangler::mangleTemplateArg(clang::TemplateArgument, bool) ItaniumMangle.cpp:0:0
#12 0x00000000070f0033 (anonymous namespace)::CXXNameMangler::mangleTemplateArgs(clang::TemplateName, llvm::ArrayRef<clang::TemplateArgument>) ItaniumMangle.cpp:0:0
#13 0x00000000070f1766 (anonymous namespace)::CXXNameMangler::mangleTemplateName(clang::TemplateDecl const*, llvm::ArrayRef<clang::TemplateArgument>) ItaniumMangle.cpp:0:0
#14 0x00000000070ef071 (anonymous namespace)::CXXNameMangler::mangleTypeConstraint(clang::ConceptDecl const*, llvm::ArrayRef<clang::TemplateArgument>) ItaniumMangle.cpp:0:0
#15 0x00000000070ef31b (anonymous namespace)::CXXNameMangler::mangleTypeConstraint(clang::TypeConstraint const*) ItaniumMangle.cpp:0:0
#16 0x00000000070ee6b8 (anonymous namespace)::CXXNameMangler::mangleTemplateArgs(clang::TemplateName, clang::TemplateArgumentList const&) ItaniumMangle.cpp:0:0
#17 0x00000000070d15de (anonymous namespace)::CXXNameMangler::mangleNameWithAbiTags(clang::GlobalDecl, llvm::SmallVector<llvm::StringRef, 4u> const*) ItaniumMangle.cpp:0:0
#18 0x00000000070d22a7 (anonymous namespace)::CXXNameMangler::mangleName(clang::GlobalDecl) ItaniumMangle.cpp:0:0
#19 0x00000000070e7cf8 (anonymous namespace)::CXXNameMangler::mangleFunctionEncoding(clang::GlobalDecl) ItaniumMangle.cpp:0:0
#20 0x00000000070e8fb7 (anonymous namespace)::CXXNameMangler::mangle(clang::GlobalDecl) ItaniumMangle.cpp:0:0
#21 0x00000000070eb8be (anonymous namespace)::ItaniumMangleContextImpl::mangleCXXName(clang::GlobalDecl, llvm::raw_ostream&) ItaniumMangle.cpp:0:0
#22 0x000000000710f183 clang::MangleContext::mangleName(clang::GlobalDecl, llvm::raw_ostream&) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+++0x710f183)
#23 0x0000000003ab9043 getMangledNameImpl(clang::CodeGen::CodeGenModule&, clang::GlobalDecl, clang::NamedDecl const*, bool) CodeGenModule.cpp:0:0
#24 0x0000000003abc02d clang::CodeGen::CodeGenModule::getMangledName(clang::GlobalDecl) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+++0x3abc02d)
#25 0x0000000003aea963 clang::CodeGen::CodeGenModule::GetAddrOfFunction(clang::GlobalDecl, llvm::Type*, bool, bool, clang::CodeGen::ForDefinition_t) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+++0x3aea963)
#26 0x0000000003de0ecc EmitFunctionDeclPointer(clang::CodeGen::CodeGenModule&, clang::GlobalDecl) CGExpr.cpp:0:0
#27 0x0000000003def38a EmitDirectCallee(clang::CodeGen::CodeGenFunction&, clang::GlobalDecl) CGExpr.cpp:0:0
#28 0x0000000003e0b156 clang::CodeGen::CodeGenFunction::EmitCallee(clang::Expr const*) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+++0x3e0b156)
#29 0x0000000003e0b0f7 clang::CodeGen::CodeGenFunction::EmitCallee(clang::Expr const*) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+++0x3e0b0f7)
#30 0x0000000003e0b832 clang::CodeGen::CodeGenFunction::EmitCallExpr(clang::CallExpr const*, clang::CodeGen::ReturnValueSlot) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+++0x3e0b832)
#31 0x0000000003e53309 (anonymous namespace)::ScalarExprEmitter::VisitCallExpr(clang::CallExpr const*) CGExprScalar.cpp:0:0
#32 0x0000000003e4a1c9 clang::StmtVisitorBase<std::add_pointer, (anonymous namespace)::ScalarExprEmitter, llvm::Value*>::Visit(clang::Stmt*) CGExprScalar.cpp:0:0
#33 0x0000000003e500ac clang::CodeGen::CodeGenFunction::EmitScalarExpr(clang::Expr const*, bool) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+++0x3e500ac)
#34 0x0000000003de8466 clang::CodeGen::CodeGenFunction::EmitAnyExpr(clang::Expr const*, clang::CodeGen::AggValueSlot, bool) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+++0x3de8466)
#35 0x0000000003e0939b clang::CodeGen::CodeGenFunction::EmitIgnoredExpr(clang::Expr const*) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+++0x3e0939b)
#36 0x0000000003a12a92 clang::CodeGen::CodeGenFunction::EmitStmt(clang::Stmt const*, llvm::ArrayRef<clang::Attr const*>) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+++0x3a12a92)
#37 0x0000000003a18f2c clang::CodeGen::CodeGenFunction::EmitCompoundStmtWithoutScope(clang::CompoundStmt const&, bool, clang::CodeGen::AggValueSlot) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+++0x3a18f2c)
#38 0x0000000003a76946 clang::CodeGen::CodeGenFunction::EmitFunctionBody(clang::Stmt const*) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+++0x3a76946)
#39 0x0000000003a89ada clang::CodeGen::CodeGenFunction::GenerateCode(clang::GlobalDecl, llvm::Function*, clang::CodeGen::CGFunctionInfo const&) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+++0x3a89ada)
#40 0x0000000003aeae33 clang::CodeGen::CodeGenModule::EmitGlobalFunctionDefinition(clang::GlobalDecl, llvm::GlobalValue*) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+++0x3aeae33)
#41 0x0000000003ae5f25 clang::CodeGen::CodeGenModule::EmitGlobalDefinition(clang::GlobalDecl, llvm::GlobalValue*) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+++0x3ae5f25)
#42 0x0000000003ae64eb clang::CodeGen::CodeGenModule::EmitGlobal(clang::GlobalDecl) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+++0x3ae64eb)
#43 0x0000000003aef963 clang::CodeGen::CodeGenModule::EmitTopLevelDecl(clang::Decl*) (.part.0) CodeGenModule.cpp:0:0
#44 0x0000000004960176 (anonymous namespace)::CodeGeneratorImpl::HandleTopLevelDecl(clang::DeclGroupRef) ModuleBuilder.cpp:0:0
#45 0x0000000004950d88 clang::BackendConsumer::HandleTopLevelDecl(clang::DeclGroupRef) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+++0x4950d88)
#46 0x0000000005e58a84 clang::ParseAST(clang::Sema&, bool, bool) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+++0x5e58a84)
#47 0x000000000495d028 clang::CodeGenAction::ExecuteAction() (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+++0x495d028)
#48 0x00000000041c3a49 clang::FrontendAction::Execute() (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+++0x41c3a49)
#49 0x000000000414479e clang::CompilerInstance::ExecuteAction(clang::FrontendAction&) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+++0x414479e)
#50 0x00000000042a2cce clang::ExecuteCompilerInvocation(clang::CompilerInstance*) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+++0x42a2cce)
#51 0x0000000000bdc3c6 cc1_main(llvm::ArrayRef<char const*>, char const*, void*) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+++0xbdc3c6)
#52 0x0000000000bd3c8a ExecuteCC1Tool(llvm::SmallVectorImpl<char const*>&, llvm::ToolContext const&) driver.cpp:0:0
#53 0x0000000003fa24e9 void llvm::function_ref<void ()>::callback_fn<clang::driver::CC1Command::Execute(llvm::ArrayRef<std::optional<llvm::StringRef>>, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char>>*, bool*) const::'lambda'()>(long) Job.cpp:0:0
#54 0x000000000363ca24 llvm::CrashRecoveryContext::RunSafely(llvm::function_ref<void ()>) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+++0x363ca24)
#55 0x0000000003fa2adf clang::driver::CC1Command::Execute(llvm::ArrayRef<std::optional<llvm::StringRef>>, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char>>*, bool*) const (.part.0) Job.cpp:0:0
#56 0x0000000003f6ae25 clang::driver::Compilation::ExecuteCommand(clang::driver::Command const&, clang::driver::Command const*&, bool) const (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+++0x3f6ae25)
#57 0x0000000003f6b88d clang::driver::Compilation::ExecuteJobs(clang::driver::JobList const&, llvm::SmallVectorImpl<std::pair<int, clang::driver::Command const*>>&, bool) const (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+++0x3f6b88d)
#58 0x0000000003f737b5 clang::driver::Driver::ExecuteCompilation(clang::driver::Compilation&, llvm::SmallVectorImpl<std::pair<int, clang::driver::Command const*>>&) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+++0x3f737b5)
#59 0x0000000000bd986c clang_main(int, char**, llvm::ToolContext const&) (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+++0xbd986c)
#60 0x0000000000ad49a1 main (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+++0xad49a1)
#61 0x00007fe4f3e75083 __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x24083)
#62 0x0000000000bd376e _start (/opt/compiler-explorer/clang-assertions-trunk/bin/clang+++0xbd376e)
clang++: error: clang frontend command failed with exit code 134 (use -v to see invocation)
Compiler returned: 134
```
</p>
</details> 

See it live: https://godbolt.org/z/5rev7119d

This worked as of trunk a week or two ago.`


---

# 25
### compiler : `LLVM`
### title : `Wrong code at -O2 on x86_64-linux_gnu since ddfee6d (recent regression)`
### open_at : `2023-09-25T07:13:42Z`
### link : https://github.com/llvm/llvm-project/issues/67287
### status : `closed`
### tags : `backend:X86, regression, miscompilation, `
### content : 
Clang at -O2 produced the wrong code.

Bisected to ddfee6d0b6979fc6e61fa5ac7424096c358746fb, which was committed by @goldsteinn 

Compiler explorer: https://godbolt.org/z/rhfGPe4x5

```console
% cat a.c
int printf(const char *, ...);
long a, b, i;
char c, f;
int d;
short e;
int *g = &d;
unsigned h;
char j[1];
int main() {
  short *k = &e;
  for (; *g;)
    ;
  for (; c <= 30; c++) {
    if (b > 4)
      i = a;
    else
      i = b;
    (int)i + 6 || (*k = j != &f);
    *g ^= h;
  }
  printf("%d\n", e);
}
%
% clang a.c -O0 && ./a.out
0
% clang a.c -O2 && ./a.out
1
%
```


---

# 26
### compiler : `LLVM`
### title : `[X86] Musttail calls involving unions with long double members are miscompiled at -O2`
### open_at : `2023-09-24T00:20:01Z`
### link : https://github.com/llvm/llvm-project/issues/67249
### status : `open`
### tags : `backend:X86, miscompilation, `
### content : 
On x86_64-linux-gnu, both Clang 14 (on my machine) and [Clang trunk (on Godbolt)](https://godbolt.org/z/37qcEWEPE) set to `-O2` compile `bar` in

```c
union u {
    long double ldbl;
};

void foo(union u acc);

void bar(union u acc) {
    __attribute__((musttail)) return foo(acc);
}
```

to

```asm
movaps  xmm0, xmmword ptr [rsp + 8]
movaps  xmmword ptr [rsp], xmm0
movaps  xmmword ptr [rsp + 8], xmm0
jmp     foo@PLT                         # TAILCALL
```

which is not only nonsensical but also a guaranteed segmentation violation, as it involves two consecutive MOVAPSes to addresses 8 bytes apart, when MOVAPS requires 16-byte alignment.


---

# 27
### compiler : `LLVM`
### title : `[WinEH] Model catch object write in MIR`
### open_at : `2023-09-22T09:55:34Z`
### link : https://github.com/llvm/llvm-project/issues/67110
### status : `open`
### tags : `llvm:codegen, platform:windows, `
### content : 
To capture the idea from https://github.com/llvm/llvm-project/pull/66988#discussion_r1333561055:

Currently, the potential write to the WinEH catch object at the point of the invoke is not properly modeled in MIR. We could fix this by adding a reference to all possible catch object frame indices to the corresponding call instructions. This would make stack coloring correct out of the box.

https://godbolt.org/z/1Wja4Yjdz

https://reviews.llvm.org/D86673

```cpp
#include <cstdio>
__attribute__((noinline,nothrow,weak)) void escape(int *p) { }
struct object {
  int i;
  object() {
    i = 1;
  }
  ~object() {
    // if "object" and "exp" are assigned to the same slot,
    // this assign will corrupt "exp".
    i = 0x42424242;
    escape(&i);
  }
};
inline void throwit() { throw 0x41414141; }

volatile int v;
inline void func() {
  try {
    object o;
    throwit();
  }
  // "exp" is written by the OS when the "throw" occurs.
  // Then the destructor is called, and the store-assign
  // clobbers the value of "exp".
  // The dereference of "exp" (with value 9999) causes a crash.
  catch (int &exp) {
    v = exp;
    printf("%d\n", v);
  }
}

int main() {
  func();
  return 0;
}
```


```
"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\Llvm\x64\bin\clang-cl.exe" -m32 -O2 -EHs .\exception.cpp -o exception.exe /Zi
```
![Random memory read](output/20231027_145032/image.png)

---

# 28
### compiler : `LLVM`
### title : `Wrong code under '-mcmodel=large -O1'`
### open_at : `2023-09-22T06:20:31Z`
### link : https://github.com/llvm/llvm-project/issues/67088
### status : `closed`
### tags : `miscompilation, llvm:optimizations, `
### content : 
I compiled the following code with clang at `-mcmodel=large -O1`, and it produces `Segmentation fault (core dumped)`.

```c
$ cat test.c
struct {
  unsigned long a;
} b;
int c, f, e, d;
int *g = &c;
void h(char aa, char bb, char i) {
j:
  for (;;) {
    unsigned int k;
    for (; b.a;)
      if (i)
        goto j;
    if (i)
      continue;
    if (g)
      break;
  }
}
int main() { h(f, e, d); }
$
$ clang-tk -mcmodel=large -O1 test.c; ./a.out
Segmentation fault (core dumped)
$
$ clang-tk -mcmodel=large -O2 test.c; ./a.out
$
$ clang-16.0.0 -mcmodel=large -O1 test.c; ./a.out
$
$ clang-tk --version
Ubuntu clang version 18.0.0 (++20230821052626+634b2fd2cac2-1~exp1~20230821172748.738)
Target: x86_64-pc-linux-gnu
Thread model: posix
$
$ clang-16.0.0 --version
clang version 16.0.0
Target: x86_64-unknown-linux-gnu
Thread model: posix
```


---


# 29
### compiler : `LLVM`
### title : `miscompile of store to element of <i1 x N>`
### open_at : `2023-09-21T20:35:49Z`
### link : https://github.com/llvm/llvm-project/issues/67060
### status : `closed`
### tags : `OpenCL, miscompilation, `
### content : 
LLVM is optimizing a store to an element of an `<i1 x N>` into an `i1` store, which then gets lowered to a byte store, clobbering adjacent vector elements.

[godbolt](https://godbolt.org/z/dPeKErroY):

```c++
typedef __attribute__((ext_vector_type(32))) bool v32bool;

v32bool v32b;

void set() {
    v32b[0] = true;
}
```

is lowered by Clang to

```llvm
@v32b = dso_local global i32 0, align 4

define dso_local void @set()() {
entry:
  %0 = load i32, ptr @v32b, align 4
  %1 = bitcast i32 %0 to <32 x i1>
  %vecins = insertelement <32 x i1> %1, i1 true, i32 0
  %2 = bitcast <32 x i1> %vecins to i32
  store i32 %2, ptr @v32b, align 4
  ret void
}
```

and then incorrectly optimized into

```llvm
define dso_local void @set()() local_unnamed_addr {
entry:
  store i1 true, ptr @v32b, align 4
  ret void
}
```

The transform would be correct if the vector elements were byte-aligned, but is not correct in this case.`


---

# 30
### compiler : `LLVM`
### title : `Stateful failure to evaluate lambda concept constraint from conditional explicit specifier`
### open_at : `2023-09-21T20:09:22Z`
### link : https://github.com/llvm/llvm-project/issues/67058
### status : `open`
### tags : `clang:frontend, concepts, confirmed, `
### content : 
Clang rejects-valid:
```c++
template<class T> concept Q = requires(T t) { [](int*){}(t); };
//static_assert(not Q<int>);
struct A { template<class T> explicit(Q<T>) A(T); };
A a = 1;
```
If the static_assert is uncommented, clang accepts.

If the constraint is inlined, clang accepts-invalid:
```c++
struct A { template<class T> explicit(requires(T t) { [](int*){}(t); }) A(T); };
A a = new int;
```


---

# 31
### compiler : `LLVM`
### title : `Compare operator not defined for recursive data types on C++20`
### open_at : `2023-09-21T19:56:54Z`
### link : https://github.com/llvm/llvm-project/issues/67056
### status : `open`
### tags : `c++20, clang:frontend, `
### content : 
Cross-posting https://gcc.gnu.org/bugzilla/show_bug.cgi?id=111504

The following code works on C++17 but not C++20:

```C++
#include <cstdint>
#include <type_traits>
#include <vector>

template <typename T1, typename T2>
static auto hasLessThanHelper(int)
    -> decltype(std::declval<T1>() < std::declval<T2>(), std::true_type{});

template <typename, typename>
static auto hasLessThanHelper(long) -> std::false_type;

template <typename T1, typename T2>
struct hasLessThan : decltype(hasLessThanHelper<T1, T2>(0)) {};

struct DynamicType {
  using T1 = int64_t;
  using T2 = std::vector<DynamicType>;
};

template <
    typename DT,
    typename = std::enable_if_t<
        (hasLessThan<typename DT::T1, typename DT::T1>::value ||
         hasLessThan<typename DT::T1, typename DT::T2>::value ||
         hasLessThan<typename DT::T2, typename DT::T1>::value ||
         hasLessThan<typename DT::T2, typename DT::T2>::value)>>
inline constexpr bool operator<(const DT& x, const DT& y) {
  // implementation omitted
  return true;
}

int main() {
  using DT = DynamicType;
  // This assert works on C++17, but fails on C++20
  static_assert(hasLessThan<std::vector<DT>, std::vector<DT>>::value);
}
```


---

# 32
### compiler : `LLVM`
### title : `-frounding-math is buggy at -O1 and above`
### open_at : `2023-09-21T15:06:48Z`
### link : https://github.com/llvm/llvm-project/issues/67028
### status : `open`
### tags : `llvm:optimizations, floating-point, `
### content : 
https://clang.llvm.org/docs/UsersManual.html says:
> The option -frounding-math forces the compiler to honor the dynamically-set rounding mode. This prevents optimizations which might affect results if the rounding mode changes or is different from the default; for example, it prevents floating-point operations from being reordered across most calls and prevents constant-folding when the result is not exactly representable.

But with Clang from 13 to 16, while it appears to make a difference at `-O0`, it seems ignored at higher optimization levels (assuming that `#pragma STDC FENV_ACCESS ON` is not used).

For instance, consider the following C program (similar to the one on https://gitlab.inria.fr/core-math/core-math/-/issues/8 but with this pragma removed):

https://godbolt.org/z/78jv57qfn

```
#include <stdio.h>
#include <fenv.h>

float foo (void) { return 0x1.fffffep127f * 0x1.fffffep127f; }

int main (void)
{
  fesetround (FE_TONEAREST);
  printf ("FE_TONEAREST: %a\n", foo ());
  fesetround (FE_TOWARDZERO);
  printf ("FE_TOWARDZERO: %a\n", foo ());
  fesetround (FE_UPWARD);
  printf ("FE_UPWARD: %a\n", foo ());
  fesetround (FE_DOWNWARD);
  printf ("FE_DOWNWARD: %a\n", foo ());
  return 0;
}
```

On an x86_64 Debian machine, with `-frounding-math` and `-O1` (or above), I get
```
FE_TONEAREST: inf
FE_TOWARDZERO: inf
FE_UPWARD: inf
FE_DOWNWARD: inf
```
instead of
```
FE_TONEAREST: inf
FE_TOWARDZERO: 0x1.fffffep+127
FE_UPWARD: inf
FE_DOWNWARD: 0x1.fffffep+127
```

Note: at least on this example, the pragma works at any optimization level, without the need of `-frounding-math`.`


---

# 33
### compiler : `LLVM`
### title : `Wrong code at -O3  on x86_64 [14 regression since 0d95b20]`
### open_at : `2023-09-21T07:25:42Z`
### link : https://github.com/llvm/llvm-project/issues/66986
### status : `closed`
### tags : `miscompilation, `
### content : 
clang at -O3 produced the wrong code.

Bisected to 0d95b20b63d7acc459dc0b2a7b2e4f9924c0adce, which was committed by @xortator 

Compiler explorer: https://godbolt.org/z/o9Mdccsfe

```console
% cat a.c
int printf(const char *, ...);
int a, b, c, d, e, g, h;
unsigned int f, i;
long j;
int k() {
  if (f < 2)
    return d;
  g = e / f;
  return g;
}
int main() {
  i = -1;
  for (; i>0; ++i) {
    h = 0;
    for (; h < 5; h++)
      j = 1;
    for (; k() + i + j <= 4; j++) {
      while (c)
        ;
      for (; b - 5 + h < 6;)
        ;
    }
  }
  printf("%d\n", a);
}
%
% clang -O2 a.c && ./a.out
0
% clang -O3 a.c && ./a.out
floating point exception
% clang -fsanitize=address,undefined a.c && ./a.out
0
%
```


---

# 34
### compiler : `LLVM`
### title : `avx register spill generates 20 extra instructions`
### open_at : `2023-09-19T23:03:25Z`
### link : https://github.com/llvm/llvm-project/issues/66837
### status : `open`
### tags : `backend:X86, llvm:optimizations, `
### content : 

https://godbolt.org/z/bWhxGb75h

Changing instruction order from:

```
const __m128i va0 = _mm_broadcastq_epi64(_mm_loadl_epi64((const __m128i*) a0));
const __m256i vxa0 = _mm256_cvtepi8_epi16(va0);
a0 += 8;
const __m128i va1 = _mm_broadcastq_epi64(_mm_loadl_epi64((const __m128i*) a1));
const __m256i vxa1 = _mm256_cvtepi8_epi16(va1);
a1 += 8;
const __m128i va2 = _mm_broadcastq_epi64(_mm_loadl_epi64((const __m128i*) a2));
const __m256i vxa2 = _mm256_cvtepi8_epi16(va2);
a2 += 8;
```

to this:

```
const __m128i va0 = _mm_broadcastq_epi64(_mm_loadl_epi64((const __m128i*) a0));
const __m128i va1 = _mm_broadcastq_epi64(_mm_loadl_epi64((const __m128i*) a1));
const __m128i va2 = _mm_broadcastq_epi64(_mm_loadl_epi64((const __m128i*) a2));
const __m256i vxa0 = _mm256_cvtepi8_epi16(va0);
a0 += 8;
const __m256i vxa1 = _mm256_cvtepi8_epi16(va1);
a1 += 8;
const __m256i vxa2 = _mm256_cvtepi8_epi16(va2);
a2 += 8;
```

Causes a microkernel to go from 46 instructions to 60 instructions, due to register spill (of 1 vector)
The generated code generates quite a few vmovdqa to shuffle register order

Attached is preprocessed source

[xnn_qd8_f32_qc8w_gemm_minmax_ukernel_3x8c8__avx2.txt](https://github.com/llvm/llvm-project/files/12667150/xnn_qd8_f32_qc8w_gemm_minmax_ukernel_3x8c8__avx2.txt)



---

# 35
### compiler : `LLVM`
### title : `Clang ssp-buffer-size misinterprets some IR-level padding as arrays`
### open_at : `2023-09-18T22:06:38Z`
### link : https://github.com/llvm/llvm-project/issues/66709
### status : `open`
### tags : `clang:codegen, `
### content : 
`-fstack-protector` inserts stack canaries into functions that have sufficiently large character buffers on the stack. I guess the idea is we don't want to pay for a stack protector on every function. So we say that, if the programmer (not the compiler) puts a character array somewhere, they are at risk of overflowing it, so it is worth adding a stack protector to just those functions.

However, Clang sometimes lowers structs to IR types that contain explicit padding in the form of arrays. The SSP implementation seems to look at IR types, not C types. It then misreads this padding as a C character array. The default threshold of 8 is large enough that this rarely happens, but if one passes `--param=ssp-buffer-size=4` to the compiler, it becomes more common.

동건 - 추가작성

https://godbolt.org/z/nzPcEWKWb

https://godbolt.org/z/WKnoPjW6e

관련된 크롬 버그

https://crbug.com/1484342

See godbolt links below:
https://godbolt.org/z/6nM453Kdh
https://godbolt.org/z/cvo1sh87s

Instead, it should only be looking at the C types. In so far as we believe large character stack buffers are more at risk of overflow, that heuristic should only apply to arrays from the programmer and not from the compiler.

(This seems to be the cause of at least some of the binary size regression that Chrome sees when switching from Abseil's `absl::optional` to libc++'s `std::optional`. Abseil uses `bool; T` while libc++ uses `T; bool`. The ordering change tickles this bug and so we burn binary size by adding more stack protectors. Not what I expected to find when starting down this journey!)

```cpp
#include <stdint.h>
#include <stdio.h>

void MightOverflow(void *arg) {
    short * data = (short *)arg;
    data[9999] = 30;
}

void CharBuffer() {
    char b[1024];
    MightOverflow(b);
}

void ShortBuffer() {
    short b[1024];
    MightOverflow(b);
}

int main() {
    ShortBuffer();
}

```

---

# 36
### compiler : `LLVM`
### title : `clang dies with SIGBUS compiling gtest-all.cc on 32-bit SPARC`
### open_at : `2023-09-18T09:50:31Z`
### link : https://github.com/llvm/llvm-project/issues/66620
### status : `open`
### tags : `clang, backend:Sparc, miscompilation, `
### content : 
<details><summary>오류 내용</summary>
<p>

When trying a 2-stage build on 32-bit Solaris/SPARC, `clang` dies in stage 2 compiling `gtest-all.cc`:
```
FAILED: projects/compiler-rt/lib/sanitizer_common/tests/SANITIZER_TEST_OBJECTS.gtest-all.cc.sparcv9.o /var/llvm/dist-sparc-release-stage2-A/tools/clang/stage2-bins/projects/compiler-rt/lib/sanitizer_common/tests/SANITIZER_TEST_OBJECTS.gtest-all.cc.sparcv9.o
cd /var/llvm/dist-sparc-release-stage2-A/tools/clang/stage2-bins/projects/compiler-rt/lib/sanitizer_common/tests && /var/llvm/dist-sparc-release-stage2-A/tools/clang/stage2-bins/./bin/clang -Wthread-safety -Wthread-safety-reference -Wthread-safety-beta -g -Wno-covered-switch-default -Wno-suggest-override -DGTEST_NO_LLVM_SUPPORT=1 -DGTEST_HAS_RTTI=0 -I/vol/llvm/src/llvm-project/dist/llvm/../third-party/unittest/googletest/include -I/vol/llvm/src/llvm-project/dist/llvm/../third-party/unittest/googletest -DGTEST_NO_LLVM_SUPPORT=1 -DGTEST_HAS_RTTI=0 -I/vol/llvm/src/llvm-project/dist/llvm/../third-party/unittest/googlemock/include -I/vol/llvm/src/llvm-project/dist/llvm/../third-party/unittest/googlemock -I/vol/llvm/src/llvm-project/dist/compiler-rt/include -I/vol/llvm/src/llvm-project/dist/compiler-rt/lib -I/vol/llvm/src/llvm-project/dist/compiler-rt/lib/sanitizer_common -DSANITIZER_COMMON_NO_REDEFINE_BUILTINS -fno-rtti -O2 -Werror=sign-compare -Wno-gnu-zero-variadic-macro-arguments -gline-tables-only -O0 -D_LARGEFILE_SOURCE=1 -D_FILE_OFFSET_BITS=64 -m32 -c -o SANITIZER_TEST_OBJECTS.gtest-all.cc.sparc.o /vol/llvm/src/llvm-project/dist/third-party/unittest/googletest/src/gtest-all.cc

Stack dump:
0.	Program arguments: /var/llvm/dist-sparc-release-stage2-A/tools/clang/stage2-bins/./bin/clang -Wthread-safety -Wthread-safety-reference -Wthread-safety-beta -g -Wno-covered-switch-default -Wno-suggest-override -DGTEST_NO_LLVM_SUPPORT=1 -DGTEST_HAS_RTTI=0 -I/vol/llvm/src/llvm-project/dist/llvm/../third-party/unittest/googletest/include -I/vol/llvm/src/llvm-project/dist/llvm/../third-party/unittest/googletest -DGTEST_NO_LLVM_SUPPORT=1 -DGTEST_HAS_RTTI=0 -I/vol/llvm/src/llvm-project/dist/llvm/../third-party/unittest/googlemock/include -I/vol/llvm/src/llvm-project/dist/llvm/../third-party/unittest/googlemock -I/vol/llvm/src/llvm-project/dist/compiler-rt/include -I/vol/llvm/src/llvm-project/dist/compiler-rt/lib -I/vol/llvm/src/llvm-project/dist/compiler-rt/lib/sanitizer_common -DSANITIZER_COMMON_NO_REDEFINE_BUILTINS -fno-rtti -O2 -Werror=sign-compare -Wno-gnu-zero-variadic-macro-arguments -gline-tables-only -D_LARGEFILE_SOURCE=1 -D_FILE_OFFSET_BITS=64 -m32 -c -o SANITIZER_TEST_OBJECTS.gtest-all.cc.sparc.o /vol/llvm/src/llvm-project/dist/third-party/unittest/googletest/src/gtest-all.cc
1.	/usr/include/sys/fcntl.h:26:1: current parser token 'extern'
2.	/vol/llvm/src/llvm-project/dist/llvm/../third-party/unittest/googletest/src/gtest.cc:141:11: LLVM IR generation of declaration 'testing'
3.	/vol/llvm/src/llvm-project/dist/llvm/../third-party/unittest/googletest/src/gtest.cc:523:23: Generating code for declaration 'testing::internal::UnitTestOptions::FilterMatchesTest'
Stack dump without symbol names (ensure you have llvm-symbolizer in your PATH or set the environment var `LLVM_SYMBOLIZER_PATH` to point to it):
0  clang-18  0x07af8604 llvm::sys::PrintStackTrace(llvm::raw_ostream&, int) + 36
1  clang-18  0x07af78bc llvm::sys::CleanupOnSignal(unsigned int) + 440
2  clang-18  0x07a49128 CrashRecoverySignalHandler(int) + 176
3  libc.so.1 0xfe9644d0 __sighndlr + 12
4  libc.so.1 0xfe956460 call_user_handler + 1044
5  libc.so.1 0xfe956814 sigacthandler + 172
6  clang-18  0x0822a208 clang::CodeGen::CodeGenFunction::pushLifetimeExtendedDestroy(clang::CodeGen::CleanupKind, clang::CodeGen::Address, clang::QualType, void (*)(clang::CodeGen::CodeGenFunction&, clang::CodeGen::Address, clang::QualType), bool) + 836
7  clang-18  0x0824b680 pushTemporaryCleanup(clang::CodeGen::CodeGenFunction&, clang::MaterializeTemporaryExpr const*, clang::Expr const*, clang::CodeGen::Address) + 868
8  clang-18  0x0824a6c8 clang::CodeGen::CodeGenFunction::EmitMaterializeTemporaryExpr(clang::MaterializeTemporaryExpr const*) + 2972
9  clang-18  0x08255048 clang::CodeGen::CodeGenFunction::EmitLValueHelper(clang::Expr const*, clang::CodeGen::KnownNonNull_t) + 2472
10 clang-18  0x08254d64 clang::CodeGen::CodeGenFunction::EmitLValueHelper(clang::Expr const*, clang::CodeGen::KnownNonNull_t) + 1732
11 clang-18  0x0824cf44 clang::CodeGen::CodeGenFunction::EmitReferenceBindingToExpr(clang::Expr const*) + 40
12 clang-18  0x082281cc clang::CodeGen::CodeGenFunction::EmitExprAsInit(clang::Expr const*, clang::ValueDecl const*, clang::CodeGen::LValue, bool) + 124
13 clang-18  0x08224f04 clang::CodeGen::CodeGenFunction::EmitAutoVarInit(clang::CodeGen::CodeGenFunction::AutoVarEmission const&) + 1836
14 clang-18  0x0821ef84 clang::CodeGen::CodeGenFunction::EmitVarDecl(clang::VarDecl const&) + 372
15 clang-18  0x0821ec08 clang::CodeGen::CodeGenFunction::EmitDecl(clang::Decl const&) + 1788
16 clang-18  0x07e21c04 clang::CodeGen::CodeGenFunction::EmitDeclStmt(clang::DeclStmt const&) + 252
17 clang-18  0x07e168a8 clang::CodeGen::CodeGenFunction::EmitSimpleStmt(clang::Stmt const*, llvm::ArrayRef<clang::Attr const*>) + 1016
18 clang-18  0x07e14fc4 clang::CodeGen::CodeGenFunction::EmitStmt(clang::Stmt const*, llvm::ArrayRef<clang::Attr const*>) + 132
19 clang-18  0x07e22ea8 clang::CodeGen::CodeGenFunction::EmitCompoundStmtWithoutScope(clang::CompoundStmt const&, bool, clang::CodeGen::AggValueSlot) + 312
20 clang-18  0x07e98f80 clang::CodeGen::CodeGenFunction::EmitFunctionBody(clang::Stmt const*) + 260
21 clang-18  0x07e99ff0 clang::CodeGen::CodeGenFunction::GenerateCode(clang::GlobalDecl, llvm::Function*, clang::CodeGen::CGFunctionInfo const&) + 2044
22 clang-18  0x07ecdd98 clang::CodeGen::CodeGenModule::EmitGlobalFunctionDefinition(clang::GlobalDecl, llvm::GlobalValue*) + 604
23 clang-18  0x07ec2550 clang::CodeGen::CodeGenModule::EmitGlobalDefinition(clang::GlobalDecl, llvm::GlobalValue*) + 724
24 clang-18  0x07ec7f2c clang::CodeGen::CodeGenModule::EmitGlobal(clang::GlobalDecl) + 1596
25 clang-18  0x07ec0d20 clang::CodeGen::CodeGenModule::EmitTopLevelDecl(clang::Decl*) + 1252
26 clang-18  0x07ed6ef8 clang::CodeGen::CodeGenModule::EmitDeclContext(clang::DeclContext const*) + 88
27 clang-18  0x07ec1000 clang::CodeGen::CodeGenModule::EmitTopLevelDecl(clang::Decl*) + 1988
28 clang-18  0x07ed6ef8 clang::CodeGen::CodeGenModule::EmitDeclContext(clang::DeclContext const*) + 88
29 clang-18  0x07ec1000 clang::CodeGen::CodeGenModule::EmitTopLevelDecl(clang::Decl*) + 1988
30 clang-18  0x08fed448 (anonymous namespace)::CodeGeneratorImpl::HandleTopLevelDecl(clang::DeclGroupRef) + 196
31 clang-18  0x08fe8e64 clang::BackendConsumer::HandleTopLevelDecl(clang::DeclGroupRef) + 216
32 clang-18  0x0a7b8a20 clang::ParseAST(clang::Sema&, bool, bool) + 1064
33 clang-18  0x086d83d8 clang::ASTFrontendAction::ExecuteAction() + 212
34 clang-18  0x08fe6efc clang::CodeGenAction::ExecuteAction() + 168
35 clang-18  0x086d79c8 clang::FrontendAction::Execute() + 100
36 clang-18  0x0861a930 clang::CompilerInstance::ExecuteAction(clang::FrontendAction&) + 976
37 clang-18  0x087e9df0 clang::ExecuteCompilerInvocation(clang::CompilerInstance*) + 640
38 clang-18  0x04af0100 cc1_main(llvm::ArrayRef<char const*>, char const*, void*) + 3044
39 clang-18  0x04aecd38 ExecuteCC1Tool(llvm::SmallVectorImpl<char const*>&, llvm::ToolContext const&) + 1284
40 clang-18  0x08447664 void llvm::function_ref<void ()>::callback_fn<clang::driver::CC1Command::Execute(llvm::ArrayRef<std::optional<llvm::StringRef>>, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char>>*, bool*) const::$_0>(int) + 16
41 clang-18  0x07a48da8 llvm::CrashRecoveryContext::RunSafely(llvm::function_ref<void ()>) + 200
42 clang-18  0x08446c20 clang::driver::CC1Command::Execute(llvm::ArrayRef<std::optional<llvm::StringRef>>, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char>>*, bool*) const + 324
43 clang-18  0x08404234 clang::driver::Compilation::ExecuteCommand(clang::driver::Command const&, clang::driver::Command const*&, bool) const + 696
44 clang-18  0x084045fc clang::driver::Compilation::ExecuteJobs(clang::driver::JobList const&, llvm::SmallVectorImpl<std::pair<int, clang::driver::Command const*>>&, bool) const + 140
45 clang-18  0x08423a38 clang::driver::Driver::ExecuteCompilation(clang::driver::Compilation&, llvm::SmallVectorImpl<std::pair<int, clang::driver::Command const*>>&) + 348
46 clang-18  0x04aec220 clang_main(int, char**, llvm::ToolContext const&) + 14192
47 clang-18  0x04afd2e4 main + 28
48 clang-18  0x04ae8468 _start + 92
```
This only happens with a `Release` (or `RelWithDebInfo`) build, not in a `Debug` build.  Likewise, a `gcc`-compiled `clang` in stage 1 is fine, too.

I could reduce the testcase to
```
$ cat gtest-all.ii
inline namespace __cxx11 {
struct basic_string {
  ~basic_string();
};
} // namespace __cxx11
basic_string GetOutputFormat() {
  const basic_string &output_format = GetOutputFormat();
}
$ clang -m32 -O2 -w gtset-all.ii
```
`gdb` shows this is an unaligned access:`
```
Thread 2 received signal SIGBUS, Bus error.
[Switching to Thread 1 (LWP 1)]
0x0822b328 in (anonymous namespace)::DestroyObject::DestroyObject (
    this=0xffbfacb4, type=..., 
    destroyer=0x82045e8 <clang::CodeGen::CodeGenFunction::destroyCXXObject(clang::CodeGen::CodeGenFunction&, clang::CodeGen::Address, clang::QualType)>, 
    addr=..., useEHCleanupForArray=<optimized out>)
    at /vol/llvm/src/llvm-project/dist/clang/lib/CodeGen/CGDecl.cpp:502
502	      : addr(addr), type(type), destroyer(destroyer),
1: x/i $pc
=> 0x822b328 <_ZN5clang7CodeGen15CodeGenFunction27pushLifetimeExtendedDestroyENS0_11CleanupKindENS0_7AddressENS_8QualTypeEPFvRS1_S3_S4_Eb+836>:	
    sttw  %i0, [ %i3 + 0x10 ]
(gdb) p/x $i3 + 0x10
$6 = 0xffbfacbc
```
The target isn't 8-byte aligned as it should.`
</p>
</details>


---

# 37
### compiler : `LLVM`
### title : `Clang crash: Assertion `(Op == Instruction::BitCast || Op == Instruction::PtrToInt || Op == Instruction::IntToPtr) && "InsertNoopCastOfTo cannot perform non-noop casts!"' failed.`
### open_at : `2023-09-18T07:14:54Z`
### link : https://github.com/llvm/llvm-project/issues/66616
### status : `open`
### tags : `miscompilation, llvm:SCEV, `
### content : 
Clang crashes at -O2.

Bisected to 20d798bd47ec5191de1b2a8a031da06a04e612e1, which was committed by @fhahn 

Compiler explorer: https://godbolt.org/z/jh7G19x8e

```console
% cat a.c
char *a;
char b;
long c;
unsigned char d;
static long e;
long *f;
int g;
short(h)(short i, short j) { return i + j; }
char k(int i) {
  while (i--)
    b += *a++;
  return i;
}
void l() {
  d = -10;
  for (; (char)e + d != 38; d = h(d, 8))
    c = (int)*f + g;
  for (; k(c) <= 7; e++)
    ;
}
int main() {}
```

<details><summary>컴파일 실패 내용</summary>
<p>

```bash
% clang -O2 a.c
clang-18: /tmp/tmpk5g_eggq/llvm/lib/Transforms/Utils/ScalarEvolutionExpander.cpp:161: llvm::Value *llvm::SCEVExpander::InsertNoopCastOfTo(llvm::Value *, llvm::Type *): Assertion (Op == Instruction::BitCast || Op == Instruction::PtrToInt || Op == Instruction::IntToPtr) && "InsertNoopCastOfTo cannot perform non-noop casts!" failed.
PLEASE submit a bug report to https://github.com/llvm/llvm-project/issues/ and include the crash backtrace, preprocessed source, and associated run script.
Stack dump:
0.      Program arguments: /zdata/shaoli/compilers/ccbuilder-compilers/clang-2f45b56728db10fa5c3ab0fe3652f6908ac9505d/bin/clang-18 -cc1 -triple x86_64-unknown-linux-gnu -emit-obj -dumpdir a- -disable-free -clear-ast-before-backend -main-file-name reduced.c -mrelocation-model pic -pic-level 2 -pic-is-pie -mframe-pointer=none -fmath-errno -ffp-contract=on -fno-rounding-math -mconstructor-aliases -funwind-tables=2 -target-cpu x86-64 -tune-cpu generic -debugger-tuning=gdb -fdebug-compilation-dir=/zdata/shaoli/realsmith/watchdir/reduced/case_jydTPMpX -fcoverage-compilation-dir=/zdata/shaoli/realsmith/watchdir/reduced/case_jydTPMpX -resource-dir /zdata/shaoli/compilers/ccbuilder-compilers/clang-2f45b56728db10fa5c3ab0fe3652f6908ac9505d/lib/clang/18 -I /zdata/shaoli/compilers/csmith/include -internal-isystem /zdata/shaoli/compilers/ccbuilder-compilers/clang-2f45b56728db10fa5c3ab0fe3652f6908ac9505d/lib/clang/18/include -internal-isystem /usr/local/include -internal-isystem /usr/lib/gcc/x86_64-linux-gnu/11/../../../../x86_64-linux-gnu/include -internal-externc-isystem /usr/include/x86_64-linux-gnu -internal-externc-isystem /include -internal-externc-isystem /usr/include -O2 -w -ferror-limit 19 -fgnuc-version=4.2.1 -fcolor-diagnostics -vectorize-loops -vectorize-slp -faddrsig -D__GCC_HAVE_DWARF2_CFI_ASM=1 -o /tmp/reduced-86a4de.o -x c reduced.c
1.      <eof> parser at end of file
2.      Optimizer
 #0 0x00007f1caba59f37 llvm::sys::PrintStackTrace(llvm::raw_ostream&, int) (/zdata/shaoli/compilers/ccbuilder-compilers/clang-2f45b56728db10fa5c3ab0fe3652f6908ac9505d/bin/../lib/libLLVM-18git.so+0x897f37)
 #1 0x00007f1caba57abe llvm::sys::RunSignalHandlers() (/zdata/shaoli/compilers/ccbuilder-compilers/clang-2f45b56728db10fa5c3ab0fe3652f6908ac9505d/bin/../lib/libLLVM-18git.so+0x895abe)
 #2 0x00007f1caba5a5ff SignalHandler(int) Signals.cpp:0:0
 #3 0x00007f1cb469f420 __restore_rt (/lib/x86_64-linux-gnu/libpthread.so.0+0x14420)
 #4 0x00007f1caac7900b raise /build/glibc-SzIz7B/glibc-2.31/signal/../sysdeps/unix/sysv/linux/raise.c:51:1
 #5 0x00007f1caac58859 abort /build/glibc-SzIz7B/glibc-2.31/stdlib/abort.c:81:7
 #6 0x00007f1caac58729 get_sysdep_segment_value /build/glibc-SzIz7B/glibc-2.31/intl/loadmsgcat.c:509:8
 #7 0x00007f1caac58729 _nl_load_domain /build/glibc-SzIz7B/glibc-2.31/intl/loadmsgcat.c:970:34
 #8 0x00007f1caac69fd6 (/lib/x86_64-linux-gnu/libc.so.6+0x33fd6)
 #9 0x00007f1cac9ea94f llvm::SCEVExpander::InsertNoopCastOfTo(llvm::Value*, llvm::Type*) (/zdata/shaoli/compilers/ccbuilder-compilers/clang-2f45b56728db10fa5c3ab0fe3652f6908ac9505d/bin/../lib/libLLVM-18git.so+0x182894f)
#10 0x00007f1cac9f2f2d llvm::SCEVVisitor<llvm::SCEVExpander, llvm::Value*>::visit(llvm::SCEV const*) (/zdata/shaoli/compilers/ccbuilder-compilers/clang-2f45b56728db10fa5c3ab0fe3652f6908ac9505d/bin/../lib/libLLVM-18git.so+0x1830f2d)
#11 0x00007f1cac9ecada llvm::SCEVExpander::expand(llvm::SCEV const*) (/zdata/shaoli/compilers/ccbuilder-compilers/clang-2f45b56728db10fa5c3ab0fe3652f6908ac9505d/bin/../lib/libLLVM-18git.so+0x182aada)
#12 0x00007f1cac9ec02e llvm::SCEVExpander::visitAddExpr(llvm::SCEVAddExpr const*) (/zdata/shaoli/compilers/ccbuilder-compilers/clang-2f45b56728db10fa5c3ab0fe3652f6908ac9505d/bin/../lib/libLLVM-18git.so+0x182a02e)
#13 0x00007f1cac9ecada llvm::SCEVExpander::expand(llvm::SCEV const*) (/zdata/shaoli/compilers/ccbuilder-compilers/clang-2f45b56728db10fa5c3ab0fe3652f6908ac9505d/bin/../lib/libLLVM-18git.so+0x182aada)
#14 0x00007f1cac9f2f8c llvm::SCEVVisitor<llvm::SCEVExpander, llvm::Value*>::visit(llvm::SCEV const*) (/zdata/shaoli/compilers/ccbuilder-compilers/clang-2f45b56728db10fa5c3ab0fe3652f6908ac9505d/bin/../lib/libLLVM-18git.so+0x1830f8c)
#15 0x00007f1cac9ecada llvm::SCEVExpander::expand(llvm::SCEV const*) (/zdata/shaoli/compilers/ccbuilder-compilers/clang-2f45b56728db10fa5c3ab0fe3652f6908ac9505d/bin/../lib/libLLVM-18git.so+0x182aada)
#16 0x00007f1cac9eb173 llvm::SCEVExpander::expandAddToGEP(llvm::SCEV const*, llvm::Type*, llvm::Value*) (/zdata/shaoli/compilers/ccbuilder-compilers/clang-2f45b56728db10fa5c3ab0fe3652f6908ac9505d/bin/../lib/libLLVM-18git.so+0x1829173)
#17 0x00007f1cac9ec0f7 llvm::SCEVExpander::visitAddExpr(llvm::SCEVAddExpr const*) (/zdata/shaoli/compilers/ccbuilder-compilers/clang-2f45b56728db10fa5c3ab0fe3652f6908ac9505d/bin/../lib/libLLVM-18git.so+0x182a0f7)
#18 0x00007f1cac9ecada llvm::SCEVExpander::expand(llvm::SCEV const*) (/zdata/shaoli/compilers/ccbuilder-compilers/clang-2f45b56728db10fa5c3ab0fe3652f6908ac9505d/bin/../lib/libLLVM-18git.so+0x182aada)
#19 0x00007f1cac9efebb llvm::SCEVExpander::expandCodeForImpl(llvm::SCEV const*, llvm::Type*, llvm::ilist_iterator<llvm::ilist_detail::node_options<llvm::Instruction, true, false, void>, false, false>) (/zdata/shaoli/compilers/ccbuilder-compilers/clang-2f45b56728db10fa5c3ab0fe3652f6908ac9505d/bin/../lib/libLLVM-18git.so+0x182debb)
#20 0x00007f1cac9ae2a2 expandBounds(llvm::RuntimeCheckingPtrGroup const*, llvm::Loop*, llvm::Instruction*, llvm::SCEVExpander&, bool) LoopUtils.cpp:0:0
#21 0x00007f1cac9aa71f llvm::addRuntimeChecks(llvm::Instruction*, llvm::Loop*, llvm::SmallVectorImpl<std::pair<llvm::RuntimeCheckingPtrGroup const*, llvm::RuntimeCheckingPtrGroup const*>> const&, llvm::SCEVExpander&, bool) (/zdata/shaoli/compilers/ccbuilder-compilers/clang-2f45b56728db10fa5c3ab0fe3652f6908ac9505d/bin/../lib/libLLVM-18git.so+0x17e871f)
#22 0x00007f1cad224780 (anonymous namespace)::GeneratedRTChecks::Create(llvm::Loop*, llvm::LoopAccessInfo const&, llvm::SCEVPredicate const&, llvm::ElementCount, unsigned int) LoopVectorize.cpp:0:0
#23 0x00007f1cad222b0d llvm::LoopVectorizePass::processLoop(llvm::Loop*) (/zdata/shaoli/compilers/ccbuilder-compilers/clang-2f45b56728db10fa5c3ab0fe3652f6908ac9505d/bin/../lib/libLLVM-18git.so+0x2060b0d)
#24 0x00007f1cad227d05 llvm::LoopVectorizePass::runImpl(llvm::Function&, llvm::ScalarEvolution&, llvm::LoopInfo&, llvm::TargetTransformInfo&, llvm::DominatorTree&, llvm::BlockFrequencyInfo*, llvm::TargetLibraryInfo*, llvm::DemandedBits&, llvm::AssumptionCache&, llvm::LoopAccessInfoManager&, llvm::OptimizationRemarkEmitter&, llvm::ProfileSummaryInfo*) (/zdata/shaoli/compilers/ccbuilder-compilers/clang-2f45b56728db10fa5c3ab0fe3652f6908ac9505d/bin/../lib/libLLVM-18git.so+0x2065d05)
#25 0x00007f1cad2286a6 llvm::LoopVectorizePass::run(llvm::Function&, llvm::AnalysisManager<llvm::Function>&) (/zdata/shaoli/compilers/ccbuilder-compilers/clang-2f45b56728db10fa5c3ab0fe3652f6908ac9505d/bin/../lib/libLLVM-18git.so+0x20666a6)
#26 0x00007f1cae43f98d llvm::detail::PassModel<llvm::Function, llvm::LoopVectorizePass, llvm::PreservedAnalyses, llvm::AnalysisManager<llvm::Function>>::run(llvm::Function&, llvm::AnalysisManager<llvm::Function>&) (/zdata/shaoli/compilers/ccbuilder-compilers/clang-2f45b56728db10fa5c3ab0fe3652f6908ac9505d/bin/../lib/libLLVM-18git.so+0x327d98d)
#27 0x00007f1cabc4f2e4 llvm::PassManager<llvm::Function, llvm::AnalysisManager<llvm::Function>>::run(llvm::Function&, llvm::AnalysisManager<llvm::Function>&) (/zdata/shaoli/compilers/ccbuilder-compilers/clang-2f45b56728db10fa5c3ab0fe3652f6908ac9505d/bin/../lib/libLLVM-18git.so+0xa8d2e4)
#28 0x00007f1cb1a88b7d llvm::detail::PassModel<llvm::Function, llvm::PassManager<llvm::Function, llvm::AnalysisManager<llvm::Function>>, llvm::PreservedAnalyses, llvm::AnalysisManager<llvm::Function>>::run(llvm::Function&, llvm::AnalysisManager<llvm::Function>&) (/zdata/shaoli/compilers/ccbuilder-compilers/clang-2f45b56728db10fa5c3ab0fe3652f6908ac9505d/bin/../lib/libclang-cpp.so.18git+0x1dbbb7d)
#29 0x00007f1cabc543de llvm::ModuleToFunctionPassAdaptor::run(llvm::Module&, llvm::AnalysisManager<llvm::Module>&) (/zdata/shaoli/compilers/ccbuilder-compilers/clang-2f45b56728db10fa5c3ab0fe3652f6908ac9505d/bin/../lib/libLLVM-18git.so+0xa923de)
#30 0x00007f1cb1a830ad llvm::detail::PassModel<llvm::Module, llvm::ModuleToFunctionPassAdaptor, llvm::PreservedAnalyses, llvm::AnalysisManager<llvm::Module>>::run(llvm::Module&, llvm::AnalysisManager<llvm::Module>&) (/zdata/shaoli/compilers/ccbuilder-compilers/clang-2f45b56728db10fa5c3ab0fe3652f6908ac9505d/bin/../lib/libclang-cpp.so.18git+0x1db60ad)
#31 0x00007f1cabc4df64 llvm::PassManager<llvm::Module, llvm::AnalysisManager<llvm::Module>>::run(llvm::Module&, llvm::AnalysisManager<llvm::Module>&) (/zdata/shaoli/compilers/ccbuilder-compilers/clang-2f45b56728db10fa5c3ab0fe3652f6908ac9505d/bin/../lib/libLLVM-18git.so+0xa8bf64)
#32 0x00007f1cb1a7fcf5 (anonymous namespace)::EmitAssemblyHelper::RunOptimizationPipeline(clang::BackendAction, std::unique_ptr<llvm::raw_pwrite_stream, std::default_delete<llvm::raw_pwrite_stream>>&, std::unique_ptr<llvm::ToolOutputFile, std::default_delete<llvm::ToolOutputFile>>&) BackendUtil.cpp:0:0
#33 0x00007f1cb1a76176 clang::EmitBackendOutput(clang::DiagnosticsEngine&, clang::HeaderSearchOptions const&, clang::CodeGenOptions const&, clang::TargetOptions const&, clang::LangOptions const&, llvm::StringRef, llvm::Module*, clang::BackendAction, llvm::IntrusiveRefCntPtr<llvm::vfs::FileSystem>, std::unique_ptr<llvm::raw_pwrite_stream, std::default_delete<llvm::raw_pwrite_stream>>) (/zdata/shaoli/compilers/ccbuilder-compilers/clang-2f45b56728db10fa5c3ab0fe3652f6908ac9505d/bin/../lib/libclang-cpp.so.18git+0x1da9176)
#34 0x00007f1cb1eb137e clang::BackendConsumer::HandleTranslationUnit(clang::ASTContext&) (/zdata/shaoli/compilers/ccbuilder-compilers/clang-2f45b56728db10fa5c3ab0fe3652f6908ac9505d/bin/../lib/libclang-cpp.so.18git+0x21e437e)
#35 0x00007f1cb06cfbe4 clang::ParseAST(clang::Sema&, bool, bool) (/zdata/shaoli/compilers/ccbuilder-compilers/clang-2f45b56728db10fa5c3ab0fe3652f6908ac9505d/bin/../lib/libclang-cpp.so.18git+0xa02be4)
#36 0x00007f1cb2b4d7c0 clang::FrontendAction::Execute() (/zdata/shaoli/compilers/ccbuilder-compilers/clang-2f45b56728db10fa5c3ab0fe3652f6908ac9505d/bin/../lib/libclang-cpp.so.18git+0x2e807c0)
#37 0x00007f1cb2abdd0f clang::CompilerInstance::ExecuteAction(clang::FrontendAction&) (/zdata/shaoli/compilers/ccbuilder-compilers/clang-2f45b56728db10fa5c3ab0fe3652f6908ac9505d/bin/../lib/libclang-cpp.so.18git+0x2df0d0f)
#38 0x00007f1cb2be1877 clang::ExecuteCompilerInvocation(clang::CompilerInstance*) (/zdata/shaoli/compilers/ccbuilder-compilers/clang-2f45b56728db10fa5c3ab0fe3652f6908ac9505d/bin/../lib/libclang-cpp.so.18git+0x2f14877)
#39 0x0000000000411bce cc1_main(llvm::ArrayRef<char const*>, char const*, void*) (/zdata/shaoli/compilers/ccbuilder-compilers/clang-2f45b56728db10fa5c3ab0fe3652f6908ac9505d/bin/clang-18+0x411bce)
#40 0x000000000040e7c1 ExecuteCC1Tool(llvm::SmallVectorImpl<char const*>&, llvm::ToolContext const&) driver.cpp:0:0
#41 0x000000000040daaa clang_main(int, char**, llvm::ToolContext const&) (/zdata/shaoli/compilers/ccbuilder-compilers/clang-2f45b56728db10fa5c3ab0fe3652f6908ac9505d/bin/clang-18+0x40daaa)
#42 0x000000000041d7b1 main (/zdata/shaoli/compilers/ccbuilder-compilers/clang-2f45b56728db10fa5c3ab0fe3652f6908ac9505d/bin/clang-18+0x41d7b1)
#43 0x00007f1caac5a083 __libc_start_main /build/glibc-SzIz7B/glibc-2.31/csu/../csu/libc-start.c:342:3
#44 0x000000000040ab3e _start (/zdata/shaoli/compilers/ccbuilder-compilers/clang-2f45b56728db10fa5c3ab0fe3652f6908ac9505d/bin/clang-18+0x40ab3e)
clang: error: unable to execute command: Aborted
clang: error: clang frontend command failed due to signal (use -v to see invocation)
clang version 18.0.0 (https://github.com/llvm/llvm-project.git 2f45b56728db10fa5c3ab0fe3652f6908ac9505d)
Target: x86_64-unknown-linux-gnu
Thread model: posix
InstalledDir: /zdata/shaoli/compilers/ccbuilder-compilers/clang-2f45b56728db10fa5c3ab0fe3652f6908ac9505d/bin
clang: note: diagnostic msg:
********************

PLEASE ATTACH THE FOLLOWING FILES TO THE BUG REPORT:
Preprocessed source(s) and associated run script(s) are located at:
clang: note: diagnostic msg: /tmp/reduced-16c667.c
clang: note: diagnostic msg: /tmp/reduced-16c667.sh
clang: note: diagnostic msg:

********************
```
</p>
</details>


---

# 38
### compiler : `LLVM`
### title : `Clang frontend C++ crash with capture-default in concept`
### open_at : `2023-09-18T06:11:25Z`
### link : https://github.com/llvm/llvm-project/issues/66614
### status : `open`
### tags : `clang:frontend, concepts, confirmed, lambda, `
### content : 
To quickly reproduce: https://gcc.godbolt.org/z/1jYx7cocf (assertion-trunk)

```cpp
#include <concepts>
#include <type_traits>

template <typename  A, typename  C>
concept l = requires(A a, C c) {
    {
        [&](A& a) -> decltype(a += c){}
    };
};
```

Compiling the above invalid code crashes clang `clang++ -x c++ --std=c++20 `, crashes locally using clang-17.0 (a10019a), also on trunk with assertion (see godbolt link) 

Note: after removing the default capture (i.e., &), the code compiles correctly `


---

# 39
### compiler : `LLVM`
### title : `Clang frontend C++ crash with atomic constraints`
### open_at : `2023-09-18T05:48:33Z`
### link : https://github.com/llvm/llvm-project/issues/66612
### status : `closed`
### tags : `clang:frontend, concepts, confirmed, `
### content : 
To quickly reproduce: https://gcc.godbolt.org/z/Gc1Y17PKf (assertion-trunk)

```cpp
#include <concepts>
#include <iostream>

template <typename T>
concept Iterator = requires(T a) {
  { a } -> std::same_as<T>;
};

template <typename T>
concept Container = requires(T a) {
  { std::end } -> Iterator;
};
```

Compiling the above code crashes clang `clang++ -x c++ --std=c++20 `, crashes locally using clang-17.0 (a10019a), also on trunk with assertion (see godbolt link) `


---

# 40
### compiler : `LLVM`
### title : `Behavior of overflowing floating-point to integer conversions`
### open_at : `2023-09-17T20:43:09Z`
### link : https://github.com/llvm/llvm-project/issues/66603
### status : `open`
### tags : `llvm:optimizations, undefined behaviour, `
### content : 
This issue is either:

a) a missed optimization in the x86-64 backend; or  
b) a wrong optimization in the aarch64 backend.

Consider the following code:

```c
#include<stdint.h>
#include<stdbool.h>
bool is_i8(double x) {
    return x == (int8_t) x;
}
bool is_i32(double x) {
    return x == (int32_t)x;
}
```

As per the C standard, these functions invoke undefined behavior if given arguments that, rounded to an integer, don't fit in the desired type. Thus, `is_i8` can always be replaced with `is_i32` ([alive2 proof](https://alive2.llvm.org/ce/z/TokdT9) from the optimized IR).

However, the x86-64 backend does not do this, and thus `is_i8` has an unnecessary `movsx eax, al` instruction that can be eliminated. The aarch64 backend does do this optimization. [compiler explorer](https://godbolt.org/z/Kj5hEjcq5).

GCC preserves the int8_t cast on both x86-64 and ARM64 (and everything else I tested in CE): https://godbolt.org/z/78MbdGbPz.

And while C does allow the optimization in question, it means that `x == (T)x` cannot be used as a check for whether the floating-point value `x` fits in the integer type `T` (even though it would work if the conversion gave any valid value of `T` in place of UB/poison). And, as far as I can tell, there is no alternative way to do a check like this anywhere near as performantly, without writing platform-specific assembly, which is, IMO, a quite problematic issue, though not really a clang-specific one.`


---

# 41
### compiler : `LLVM`
### title : `wrong type of ternary expression involving composite pointer type with array of unknown bound`
### open_at : `2023-09-17T16:08:56Z`
### link : https://github.com/llvm/llvm-project/issues/66599
### status : `open`
### tags : `c++, clang:frontend, `
### content : 
Version: clang 16.0.0
flags: `-std=c++20 -O2 -pedantic-errors`

### Observed behavior

```cpp
template <typename T>
void f();

void foo() {
    decltype(auto) ptr
    = true
      ? (int(*)[42])nullptr
      : (int(*)[])nullptr;
    f<decltype(ptr)>(); // calls f<int const (*) []>()
}
```

https://godbolt.org/z/TvaqEKr4v

### Expected behavior

The type of the ternary expression should be `int (*)[]`.

It seems that clang is overeager in applying https://timsong-cpp.github.io/cppwp/n4868/conv.qual#3.3 .
$P_1^3$ is different from one of the source $P_1$-s, which means that `const` is added for every $cv_k$ for $0 < k < 1$, which should be none of them. I think clang treats the right bound as inclusive here when the difference between the two types is in $P_i$.

### Notes

* GCC doesn't implement bringing ternary arguments to composite pointer type when array of unknown bound is involved https://gcc.gnu.org/bugzilla/show_bug.cgi?id=100189.
* The conversions with array of unknown bound were added in [P0388](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p0388r4.html).


---

# 42
### compiler : `LLVM`
### title : `Complex division doesn't respect pragma float_control`
### open_at : `2023-09-15T22:34:32Z`
### link : https://github.com/llvm/llvm-project/issues/66555
### status : `open`
### tags : `clang:codegen, floating-point, `
### content : 
If I am compiling with fast-math enabled, but use #pragma float_control(precise, on) for a function, complex division within that function is still represented as if fast math were enabled.

```
#pragma float_control(precise, on)
complex double foo(complex double x, complex double y) {
  return x / y;
}
```
https://godbolt.org/z/3sP44nEE5

This is happening because ComplexExprEmitter::EmitBinDiv() is checking CGF.getLangOpts().FastMath and not looking for the possibility that the option is being overridden by a pragma.


---

# 43
### compiler : `LLVM`
### title : Sanitizer `pointer-overflow` does not appear to function
### open_at : `2023-09-15T00:31:39Z`
### link : https://github.com/llvm/llvm-project/issues/66451
### status : `closed`
### tags : `clang:codegen, compiler-rt:ubsan, `
### content : 
Using `-fsanitize=pointer-overflow` doesn't appear to provide any checking on pointer math. GCC's implementation correctly triggers if `NULL` is operated on or if a value would wrap around.

https://godbolt.org/z/1c6ec9TTP

```
#include <stdlib.h>
#include <stdio.h>

/* Using stderr for all output or else godbolt doesn't intermix output. */
int main(int argc, char *argv[]) {
    void *p = NULL;

    fprintf(stderr, "%p (%zu)\n", p, (unsigned long)p);

    /* argc is a stand-in for "1" to avoid optimization */
    p -= argc;

    fprintf(stderr, "%p (%zu)\n", p, (unsigned long)p);

    p += argc;

    fprintf(stderr, "%p (%zu)\n", p, (unsigned long)p);

    return 0;
}
```

Clang just shows the value wrapping:

```
(nil) (0)
0xffffffffffffffff (18446744073709551615)
(nil) (0)
```

But GCC will catch it:

```
(nil) (0)
/app/example.c:11:7: runtime error: applying non-zero offset 18446744073709551615 to null pointer
0xffffffffffffffff (18446744073709551615)
/app/example.c:15:7: runtime error: applying non-zero offset to non-null pointer 0xffffffffffffffff produced null pointer
(nil) (0)
```


---

# 44
### compiler : `LLVM`
### title : `[Bug][AArch64] Ensure SVE function operands passed via memory are initialised.`
### open_at : `2023-09-14T13:04:19Z`
### link : https://github.com/llvm/llvm-project/issues/66370
### status : `closed`
### tags : `backend:AArch64, miscompilation, release:backport, SVE, `
### content : 
Taking the example below it can be seen that `j` is not initialised by `main` when calling `F9`, which means `F9` reads uninitialised stack space.

```
#include <arm_sve.h>
#include <assert.h>

__attribute((noinline)) void F9(double a, double b, double c, double d,
                                double e, double f, double g, double h,
                                double i, svfloat32_t j) {
  assert(!svptest_any(svptrue_b32(),
                      svcmpne_f32(svptrue_b32(), j, svdup_f32(2.0f))));
}

int main() {
  svfloat32_t j = svdup_f32(2.0f);
  F9(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, j);
  return 0;
}
```


---

# 45
### compiler : `LLVM`
### title : `[AArch64] Miscompilation when stack tagging is enabled in AArch64`
### open_at : `2023-09-14T08:14:52Z`
### link : https://github.com/llvm/llvm-project/issues/66338
### status : `open`
### tags : `backend:AArch64, llvm:codegen, miscompilation, `
### content : 

**이거랑 중복임 이거 확인하면 될듯**

https://github.com/llvm/llvm-project/issues/64309

Here is the reduced test : [https://godbolt.org/](https://godbolt.org/)
There is a **br** instruction (line 16) at end of the **entry** block which is suppose to **read the NZCV flag** edited by previous **cmp** instruction (line 14) and branch accordingly. But the **stg loop** gets in the way and edits the **nzcv flag** which is not handled properly.

This results in mis compiled assembly
```
  cmp     w0, #10  
LBB0_1:                                
  st2g    x9, [x9], #32  
  subs    x8, x8, #32   
  b.ne    .LBB0_1
  b.ge    .LBB0_4
```
        
Here b.ge jumps based on NZCV edited by subs instruction rather than from cmp instruction.

Run Command
```
llc -mtriple=aarch64 -mattr=+mte -aarch64-order-frame-objects=0 settag.ll
```
settag.ll
```
declare void @llvm.aarch64.settag(ptr %p, i64 %a)
; Function Attrs: nounwind
declare i32 @printf(ptr, ...) #0

@.str = private unnamed_addr constant [4 x i8] c"%d\0A\00", align 1

define i32 @stg_func(i32 %in) {
entry:

  %a = alloca i8, i32 16, align 16
  %b = alloca i8, i32 512, align 16
  %c = alloca i8, i32 16, align 16
  call void @llvm.aarch64.settag(ptr %a, i64 16)
  call void @llvm.aarch64.settag(ptr %b, i64 512)
  %cmp = icmp slt i32 %in, 10
  call void @llvm.aarch64.settag(ptr %c, i64 16)
  br i1 %cmp, label %return0, label %return1

return0:                                           ; preds = %entry
  %call = call i32 (ptr, ...) @printf(ptr @.str, i32 10) #1
  ret i32 0

return1:
  ret i32 1
}
```

This is observed after the patch : [5e612bc](https://github.com/llvm/llvm-project/commit/5e612bc291347d364f1d47c37f0d34eb6474b9b5)
As this patch expands stg loops to b.ne instead of Bcc used earlier



---

# 46
### compiler : `LLVM`
### title : `[clang] Main Function Missing Due to Incorrect Infinite Loop Optimization`
### open_at : `2023-09-14T00:52:45Z`
### link : https://github.com/llvm/llvm-project/issues/66307
### status : `closed`
### tags : `clang:codegen, `
### content : 
We are submitting this report to bring to your attention an issue that I have encountered while using clang compiler, specifically related to compiler optimization. While working with clang compiler, I have observed an error that seems to be related to optimization levels `O1`, `O2`, and `O3`. Although I had expected an infinite loop to occur when applying these optimization options, I have instead encountered an unexpected termination of the main function.

I have conducted extensive research and testing to pinpoint the root cause of this problem, but unfortunately, my efforts have not yielded a conclusive solution. Given the complexity of LLVM and its extensive code base, I believe that your expertise and resources can shed light on this issue and help clarify its underlying causes.

# Extended Description
### **Proof of Concept to trigger the bug**
```C
#include <stdint.h>

uint8_t uint8_sub(uint8_t ui1, uint8_t ui2) {
  return ui1 - ui2;
}

int main() {
    int32_t i;
    for(i = 0; i > (-22); i = uint8_sub(i, 1)) { }
    return 0;
}
```
While it was anticipated that an infinite loop would ensue when employing all optimization options, the principal function becomes non-existent, leading to anomalous termination across `O1`, `O2`, and `O3` optimization levels.
### Expected Result
```bash
# version
$ clang-18 --version
clang version 18.0.0 (https://github.com/llvm/llvm-project.git 4706251a3186c34da0ee8fd894f7e6b095da8fdc)
Target: x86_64-unknown-linux-gnu
Thread model: posix
InstalledDir: /home/dongFiles/compiler_trunk/llvm-project/build/bin

# compile with O0 optimization
$ clang-18 target.c -o clang_O0 -O0 

# correct result: infinite loop
$ ./clang_O0 # Infinite loop                                                                     
^C
```
### Clang Result (incorrect)
- **clang x64 (incorrect)**
```bash
$ clang-18 --version
clang version 18.0.0 (https://github.com/llvm/llvm-project.git 4706251a3186c34da0ee8fd894f7e6b095da8fdc)
Target: x86_64-unknown-linux-gnu
Thread model: posix
InstalledDir: /home/dongFiles/compiler_trunk/llvm-project/build/bin

$ clang-18 target.c -o clang_O1 -O1
$ clang-18 target.c -o clang_O2 -O2
$ clang-18 target.c -o clang_O3 -O3

$ ./clang_O1 
$ echo $?   # Abnormal termination
64
$ ./clang_O2 
$ echo $?   # Abnormal termination
64
$ ./clang_O3 
$ echo $?   # Abnormal termination
64
```
- **clang aarch64 (incorrect)**
```bash
$ clang-18 --target=aarch64-linux-gnu target.c -o clang_O0_aarch64 -O0
$ clang-18 --target=aarch64-linux-gnu target.c -o clang_O1_aarch64 -O1
$ clang-18 --target=aarch64-linux-gnu target.c -o clang_O2_aarch64 -O2
$ clang-18 --target=aarch64-linux-gnu target.c -o clang_O3_aarch64 -O3

$ ./clang_O1_aarch64 
$ echo $?    # Abnormal termination
1
$ ./clang_O2_aarch64 
$ echo $?    # Abnormal termination
1
$ ./clang_O3_aarch64 
$ echo $?    # Abnormal termination
1
```
- **clang x64 O0, O1, O2, O3 : https://godbolt.org/z/sKsh6Tdv1**
- **clang aarch64 O0, O1, O2, O3 : https://godbolt.org/z/PTG47q6v9**
### Comparison to GCC Result (correct)
```bash
$ gcc-trunk --version                                                    
gcc-trunk (GCC) 14.0.0 20230913 (experimental)
Copyright (C) 2023 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

$ gcc-trunk target.c -o gcc_O0 -O0 
$ gcc-trunk target.c -o gcc_O1 -O1
$ gcc-trunk target.c -o gcc_O2 -O2
$ gcc-trunk target.c -o gcc_O3 -O3 
$ ./gcc_O0   # Infinite loop   
^C
$ ./gcc_O1   # Infinite loop   
^C
$ ./gcc_O2   # Infinite loop   
^C
$ ./gcc_O3   # Infinite loop
^C
```
- **gcc x64 O0, O1, O2, O3 : https://godbolt.org/z/5YM9r56EM**
- **gcc aarch64 O0, O1, O2, O3 : https://godbolt.org/z/TGdvGP9Ws**


---

# 47
### compiler : `LLVM`
### title : `SSP Strong with `-fexceptions` causing code-gen change on a C compilation with a `noreturn` attribute`
### open_at : `2023-09-13T23:04:16Z`
### link : https://github.com/llvm/llvm-project/issues/66303
### status : `open`
### tags : `clang:codegen, regression, `
### content : 
When compiled with SSP Strong (`-fstack-protector-strong`), the following C test-case produces different code depending on whether Exception Handling is enabled:

    extern void my_exit(void) __attribute__((__noreturn__));
    extern void bar(int *);

    void foo(void) {
      int buf[10];
      bar(buf);
      my_exit();
    }

Here is what happens with a modern x86_64 Clang (tested with `main` 3755ea93b4f7):

```
$ clang -S -O2 -fstack-protector-strong -o test.O2.s test.c
$ clang -S -O2 -fstack-protector-strong -fexceptions -o test.O2.eh.s test.c
$ diff test.O2.s test.O2.eh.s
9,10c9,12
<       subq    $40, %rsp
<       .cfi_def_cfa_offset 48
---
>       subq    $56, %rsp
>       .cfi_def_cfa_offset 64
>       movq    %fs:40, %rax
>       movq    %rax, 48(%rsp)
12a15,18
>       movq    %fs:40, %rax
>       cmpq    48(%rsp), %rax
>       jne     .LBB0_2
> # %bb.1:                                # %SP_return
13a20,21
> .LBB0_2:                                # %CallStackCheckFailBlk
>       callq   __stack_chk_fail@PLT
20a29
>       .addrsig_sym __stack_chk_fail
$
```

Enabling Exception Handling in C compilations shouldn't change the generated code.  More directly, the problem here is that in compiling a `noreturn` C function with `-fexceptions`, we are enabling the generation of the SSP canary, due to the concern of a security hole in exception-handling-unwinding, described in:
https://bugs.chromium.org/p/llvm/issues/detail?id=30

But there isn't any unwinding in a C program, regardless of whether `-fexceptions` was specified.  So that SSP support isn't needed.  And more generally, turning on `-fexceptions` should be a no-op in compiling C code.  Is this a wider (and latent) Clang issue for C compilations, in that we normally tag C functions as `nounwind`, and turning on `-fexceptions` shouldn't change that?

This is a regression in llvm16 (initially related to d656ae280957), and as noted above it still exists in `main`.  (A related aspect was partially addressed in llvm17 fc4494dffa54.  And that was cherry-picked to the llvm16 release (bf80902fdd43).)


---

# 48
### compiler : `LLVM`
### title : [clang] Issues with determining valid constant expressions in `cxx2b`
### open_at : `2023-09-13T17:31:50Z`
### link : https://github.com/llvm/llvm-project/issues/66262
### status : `closed`
### tags : `c++20, clang:frontend, clang:diagnostics, `
### content : 
C++23 permits a variable of non-literal type to be defined in a constant expression scope, but clang seems to have a hard time handling it. The following code does not compile with `-std=cxx2b` on latest clang:
```cpp
struct A { int y; };
struct B : virtual public A {};
struct X : public B {};

constexpr void foo() {
  X x;
  x.B::y = 1;
}
```
Godbolt: https://godbolt.org/z/rTdaf545e.


---


# 49
### compiler : `LLVM`
### title : `Clang incorrectly complains about default template argument not being reachable `
### open_at : `2023-09-13T17:17:42Z`
### link : https://github.com/llvm/llvm-project/issues/66255
### status : `open`
### tags : `c++20, clang:modules, `
### content : 
Run a compiler on this code:
```cpp
// --- foo.cppm
export module foo;

export struct partial {};
export template <class T, class Cat = partial> concept is_comparable = true;

// --- bar.cppm
export module bar;

import foo;
template <class T>
void func() requires is_comparable<T> {}
```

The exact commands are:
```sh
$ clang++ -std=c++20 --precompile foo.cppm
$ clang++ -std=c++20 --precompile bar.cppm -fmodule-file=foo.pcm
```

Expected results: code compiles with no errors.
Actual: Clang produces the following error when compiling the module `bar`:
```sh
bar.cppm:6:22: error: default argument of 'is_comparable' must be imported from module 'foo' before it is required
void func() requires is_comparable<T> {}
                     ^
foo.cppm:5:39: note: default argument declared here is not reachable
export template <class T, class Cat = partial> concept is_comparable = true;
                                      ^
1 error generated.
```


---

# 50
### compiler : `LLVM`
### title : `SLPVectorizer incorrectly reorders select operands`
### open_at : `2023-09-13T07:10:49Z`
### link : https://github.com/llvm/llvm-project/issues/66176
### status : `closed`
### tags : `miscompilation, llvm:SLPVectorizer, `
### content : 
clang at -O2/3 produced the wrong code.

Bisected to d01aec4c769d50fb92e86decd41d077c94105841, which was committed by @nikic 

Compiler explorer: https://godbolt.org/z/9bhhc5rGM

```console
% cat a.c
int printf(const char *, ...);
int a, c;
long b, g;
static int d[1] = {5};
unsigned h;
long *i() {
  c = 0;
  for (; c <= 2; c++) {
    for (;;) {
      char e[1] = {97};
      char f = *e + c;
      
      if (d[f - 97]) {
        int *j[] = {&d[0], &d[0]};
        h++;
        break;
      }
      return &b;
    }
    for (; h <= 2;)
      return &g;
  }
  for (;;)
    ;
}
int main() {
  i();
  printf("%d\n", a);
}
%
% clang -O0 a.c && ./a.out
0
% clang -O2 a.c
% ./a.out
(Timeout)
%
```


---


# 51
### compiler : `LLVM`
### title : `[clang][vectorize] -O2 vectorize will get wrong result`
### open_at : `2023-09-13T01:21:35Z`
### link : https://github.com/llvm/llvm-project/issues/66163
### status : `open`
### tags : `miscompilation, vectorization, `
### content : 
clang: 15.0.4 arm64be
#### demo.c

```
#include <stdio.h>
#define N 32
int a[N]={0};
int b[N]={0,0,1,0,
          0,0,1,0,
          0,0,1,0,
          0,0,1,0,
          0,0,1,0,
          0,0,1,0,
          0,0,1,0,
          0,0,1,0};
int k[N];

int main () {
    for (int i = 0; i < N/4; i++) {
        k[4*i] = a[4*i] < b[4*i] ? 1 : 0;
        k[4*i+1] = a[4*i+1] < b[4*i+1] ? 1 : 0;
        k[4*i+2] = a[4*i+2] < b[4*i+2] ? 1 : 0;
        k[4*i+3] = a[4*i+3] < b[4*i+3] ? 1 : 0;
    }

    for (int i = 0; i < N/4; i++) {
        printf("%d, %d, %d, %d\n",k[4*i],k[4*i+1],k[4*i+2],k[4*i+3]);
    }
    return 0;
}
```

#### compile command

```
clang demo.c -o demo.exe -static -O2
```

#### output

wrong：

```
1, 0, 1, 0
1, 0, 1, 0
1, 0, 1, 0
1, 0, 1, 0
1, 0, 1, 0
1, 0, 1, 0
1, 0, 1, 0
1, 0, 1, 0
```
It's a vectorize problem : with`-fno-vectorize` option，get result right

```
0, 0, 1, 0
0, 0, 1, 0
0, 0, 1, 0
0, 0, 1, 0
0, 0, 1, 0
0, 0, 1, 0
0, 0, 1, 0
0, 0, 1, 0
```

through  `-mllvm -opt-bisect-limit=` command can locate the pass that caused the error is `InstCombinePass`



---

# 52
### compiler : `LLVM`
### title : `The combination of -fno-rtti -fexceptions is very brittle`
### open_at : `2023-09-12T17:46:39Z`
### link : https://github.com/llvm/llvm-project/issues/66117
### status : `open`
### tags : `clang, c++, `
### content : 
The combination of `-fno-rtti` and `-fexceptions` is not supported very well, and we've seen several issues related to that internally at Apple. This bug report captures an analysis of this issue I did years ago to try to make it visible to the larger community.

Current behaviour
================
When both these options are specified, we don't generate RTTI for types, except when a type is thrown, at which point we generate some minimal RTTI in the TU where it is thrown (I am not sure whether the "minimal RTTI is exactly the same as "normal RTTI"). Also note that we don't generate RTTI even in the place where a key function exists, and similarly we don't assume that other TUs have a definition of the RTTI when a key function exists.

Problem with the current approach
=================================
Let's say some TU `a.cpp` built with `-fno-rtti -fexceptions` calls a function (defined in some other TU) that can throw a type `E`, and tries to catch `E`. Then, let's say that function is defined in some other TU `b.cpp` built with `-frtti -fexceptions` throws a type `E`. Let's also assume that another TU `c.cpp` built with `-frtti -fexceptions` defines the RTTI for E (through a key function, for example). The problem here is that in `a.cpp`, we'll generate minimal RTTI for E, and in `b.cpp` we'll use the normal RTTI assumed to be in `c.cpp` (because there's a key function). Since the two RTTIs don't get de-duplicated, we get a type identity mismatch in `a.cpp` and `b.cpp`, and the exception isn't caught.

Here's a minimal working example:

```cpp
#/usr/bin/env bash

cat <<EOF > a.cpp
struct E { virtual ~E(); };
extern void f();
int main() {
    try {
        f();
    } catch (E const&) { // tries catching E with RTTI from a.o

    }
}
EOF

cat <<EOF > b.cpp
struct E { virtual ~E(); };
extern void f() { throw E{}; } // throws E with RTTI from c.o
EOF

cat <<EOF > c.cpp
struct E { virtual ~E(); };
E::~E() { } // key function
EOF

clang++ a.cpp -fno-rtti -fexceptions -std=c++11 -c -o a.o
clang++ b.cpp -frtti -fexceptions -std=c++11 -c -o b.o
clang++ c.cpp -frtti -fexceptions -std=c++11 -c -o c.o
clang++ b.o c.o -shared -o b.dylib
clang++ a.o b.dylib -o a.exe
nm a.o b.o c.o a.exe b.dylib | c++filt
./a.exe
```

To map this example to reality, imagine that `E` is something like `std::exception` (or a derived class), that `b.dylib` is `libc++.dylib`, and that `a.exe` is a user program built with `-fno-rtti -fexceptions`. It becomes clear why people are having problems with the feature.

I once discussed this issue with @dexonsmith and we had discussed this potential solution:
* Add an attribute __generate_rtti__ (name TBD)
* When you’d normally generate RTTI for a type and currently suppress the RTTI generation based on whether -fno-rtti is present, instead check whether the type has the attribute and still generate full RTTI if it has it.
* When you try to throw a type with `-fno-rtti -fexceptions`, you get:
    * a warning if the type doesn’t have the attribute, and minimal RTTI gets generated (like today, for backwards compatibility)
    * the normal behaviour (like when -fno-rtti is not specified) if the type has the attribute. In particular, this means that no RTTI is generated if we can tell it’s somewhere else (e.g. when there’s a key function), and full RTTI (that the linker can dedupe) is generated when we can’t tell for sure.


rdar://58055046`


---

# 53
### compiler : `LLVM`
### title : `Wrong code at -Os on x86_64 (recent regression since 6ed152a) `
### open_at : `2023-09-12T10:31:56Z`
### link : https://github.com/llvm/llvm-project/issues/66066
### status : `closed`
### tags : `miscompilation, llvm:SCEV, `
### content : 
Clang at -Os produced the wrong code.

Bisected to 6ed152aff4aab6307ecaab64a544d0524ea5f50e, which was committed by @caojoshua 

Compiler explorer: https://godbolt.org/z/aMEWqd9dP

```cpp
% cat a.c
int printf(const char *, ...);
int a, b, c;
long d;
const unsigned *e;
const unsigned **f[3];
static char(g)(unsigned h, int j) { return h > j ? h : h << j; }
static short k() {
  char l = 1;
  b = 0;
  for (; b <= 3; b++) {
    char *m = &l;
    int *n = &c;
    int i = 0;
    for (; i < 3; i++)
      f[i] = &e;
    *n = g((*m)--, 7);
    if (*n)
      ;
    else {
      for (; i < 9; i++)
        f[0] || (d = 2);
      if (0 < *n)
        ;
      else
        return 0;
    }
    printf("%d\n", *n);
  }
  return 1;
}
int main() {
  k();
}
%
% clang -O0 a.c && ./a.out
-128
0
% clang -Os a.c && ./a.out
-128
0
-128
0
%
```


---

# 54
### compiler : `LLVM`
### title : `[Inliner] Should we inline callee containing llvm.frameaddress?`
### open_at : `2023-09-12T09:31:26Z`
### link : https://github.com/llvm/llvm-project/issues/66059
### status : `open`
### tags : `llvm:optimizations, `
### content : 
For code
```c++
#include <iostream>

void foo() {
  std::cout << __builtin_frame_address(0) << std::endl;
}

int main() {
  std::cout << __builtin_frame_address(0) << std::endl;
  foo();
  return 0;
}
```
Using trunk's clang, with `-O2`, the output is
```
0x7ffd0501a2c0
0x7ffd0501a2a0
```
With `-O3`, the output is
```
0x7ffd97138270
0x7ffd97138270
```
We have `InlinerPass` enabled at `O3`, which inlines callee(`foo`)'s `llvm.frameaddress`. The different behaviors at `O2` and `O3` affects IBM OpenXL C/C++ compiler when compiling and running `compiler-rt/test/asan/TestCases/Posix/stack-overflow.cpp`.

```cpp
// stack-overflow.cpp
// Test ASan detection of stack-overflow condition.

// RUN: %clangxx_asan -O0 %s -DSMALL_FRAME -pthread -o %t && %env_asan_opts=use_sigaltstack=1 not %run %t 2>&1 | FileCheck %s
// RUN: %clangxx_asan -O3 %s -DSMALL_FRAME -pthread -o %t && %env_asan_opts=use_sigaltstack=1 not %run %t 2>&1 | FileCheck %s
// RUN: %clangxx_asan -O0 %s -DSAVE_ALL_THE_REGISTERS -pthread -o %t && %env_asan_opts=use_sigaltstack=1 not %run %t 2>&1 | FileCheck %s
// RUN: %clangxx_asan -O3 %s -DSAVE_ALL_THE_REGISTERS -pthread -o %t && %env_asan_opts=use_sigaltstack=1 not %run %t 2>&1 | FileCheck %s
// RUN: %clangxx_asan -O0 %s -pthread -o %t && %env_asan_opts=use_sigaltstack=1 not %run %t 2>&1 | FileCheck %s
// RUN: %clangxx_asan -O3 %s -pthread -o %t && %env_asan_opts=use_sigaltstack=1 not %run %t 2>&1 | FileCheck %s

// RUN: %clangxx_asan -O0 %s -DTHREAD -DSMALL_FRAME -pthread -o %t && %env_asan_opts=use_sigaltstack=1 not %run %t 2>&1 | FileCheck %s
// RUN: %clangxx_asan -O3 %s -DTHREAD -DSMALL_FRAME -pthread -o %t && %env_asan_opts=use_sigaltstack=1 not %run %t 2>&1 | FileCheck %s
// RUN: %clangxx_asan -O0 %s -DTHREAD -DSAVE_ALL_THE_REGISTERS -pthread -o %t && %env_asan_opts=use_sigaltstack=1 not %run %t 2>&1 | FileCheck %s
// RUN: %clangxx_asan -O3 %s -DTHREAD -DSAVE_ALL_THE_REGISTERS -pthread -o %t && %env_asan_opts=use_sigaltstack=1 not %run %t 2>&1 | FileCheck %s
// RUN: %clangxx_asan -O0 %s -DTHREAD -pthread -o %t && %env_asan_opts=use_sigaltstack=1 not %run %t 2>&1 | FileCheck %s
// RUN: %clangxx_asan -O3 %s -DTHREAD -pthread -o %t && %env_asan_opts=use_sigaltstack=1 not %run %t 2>&1 | FileCheck %s
// RUN: not %run %t 2>&1 | FileCheck %s
// REQUIRES: stable-runtime

// UNSUPPORTED: ios

#include <assert.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>
#include <sys/time.h>
#include <sys/resource.h>
#include <sanitizer/asan_interface.h>

const int BS = 1024;
volatile char x;
volatile int y = 1;
volatile int z0, z1, z2, z3, z4, z5, z6, z7, z8, z9, z10, z11, z12, z13;

void recursive_func(uintptr_t parent_frame_address) {
#if defined(SMALL_FRAME)
  char *buf = 0;
#elif defined(SAVE_ALL_THE_REGISTERS)
  char *buf = 0;
  int t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13;
  t0 = z0;
  t1 = z1;
  t2 = z2;
  t3 = z3;
  t4 = z4;
  t5 = z5;
  t6 = z6;
  t7 = z7;
  t8 = z8;
  t9 = z9;
  t10 = z10;
  t11 = z11;
  t12 = z12;
  t13 = z13;

  z0 = t0;
  z1 = t1;
  z2 = t2;
  z3 = t3;
  z4 = t4;
  z5 = t5;
  z6 = t6;
  z7 = t7;
  z8 = t8;
  z9 = t9;
  z10 = t10;
  z11 = t11;
  z12 = t12;
  z13 = t13;
#else
  char buf[BS];
  // Check that the stack grows in the righ direction, unless we use fake stack.
  assert(parent_frame_address > (uintptr_t)__builtin_frame_address(0));
  buf[rand() % BS] = 1;
  buf[rand() % BS] = 2;
  x = buf[rand() % BS];
#endif
  if (y)
    recursive_func((uintptr_t)__builtin_frame_address(0));
  x = 1; // prevent tail call optimization
  // CHECK: {{stack-overflow on address 0x.* \(pc 0x.* bp 0x.* sp 0x.* T.*\)}}
  // If stack overflow happens during function prologue, stack trace may be
  // corrupted. Unwind tables are not always 100% exact there.
  // For this reason, we don't do any further checks.
}

void *ThreadFn(void* unused) {
  recursive_func((uintptr_t)__builtin_frame_address(0));
  return 0;
}

void LimitStackAndReexec(int argc, char **argv) {
  struct rlimit rlim;
  int res = getrlimit(RLIMIT_STACK, &rlim);
  assert(res == 0);
  if (rlim.rlim_cur == RLIM_INFINITY) {
    rlim.rlim_cur = 256 * 1024;
    res = setrlimit(RLIMIT_STACK, &rlim);
    assert(res == 0);

    execv(argv[0], argv);
    assert(0 && "unreachable");
  }
}

int main(int argc, char **argv) {
  LimitStackAndReexec(argc, argv);
#ifdef THREAD
  pthread_t t;
  pthread_create(&t, 0, ThreadFn, 0);
  pthread_join(t, 0);
#else
  recursive_func((uintptr_t)__builtin_frame_address(0));
#endif
  return 0;
}


```


---

# 55
### compiler : `LLVM`
### title : [clang/c++/coroutines] `-Wunused-parameter` not working with coroutines.
### open_at : `2023-09-11T16:03:15Z`
### link : https://github.com/llvm/llvm-project/issues/65971
### status : `open`
### tags : `clang:diagnostics, coroutines, `
### content : 
Given some coroutine return type `task<T>`, the following:
```cpp
task<int> foo( int a ) {
  co_return 42;
}
```
when compiled with `-Wunused-parameter`, will not warn that `a` is unused.  I suspect that it is because `a` is used during setup of the coroutine frame/promise... but I think most users would not expect that to count as "used."

**Actual behavior**: no warning.
**Expected behavior**: `warning: unused parameter 'a' [-Wunused-parameter]` (when that warning is enabled)

Note that GCC _does_ warn in this scenario.  In my coroutine-heavy code base I am thus forced to compile with GCC to find all of my unused parameters.`


---

# 56
### compiler : `LLVM`
### title : `[AArch64] neon big endian miscompiled `
### open_at : `2023-09-10T10:02:14Z`
### link : https://github.com/llvm/llvm-project/issues/65884
### status : `open`
### tags : `backend:AArch64, miscompilation, `
### content : 
https://godbolt.org/z/vWMz5K34r

```
#include <arm_neon.h>

extern void abort (void);

__attribute__((noinline)) uint8x16_t
wrap_vld1q_lane_u8 (const uint8_t *load, uint8x16_t vec) {
  return vld1q_lane_u8 (load, vec, 12);
}

int test_vld1q_lane_u8(const uint8_t *data) {
  uint8_t out[16];
  uint8_t overwrite = 7;
  int j;
  uint8x16_t in = vld1q_u8 (data);
  in = wrap_vld1q_lane_u8 (&overwrite, in);
  vst1q_u8 (out, in);
  for (j = 0; j < 13; j++)
    if (out[j] != (j == 12 ? overwrite : data[j])) {
      abort();
    }
  return 0;
}

int main (int argc, char **argv)
{
  uint64_t orig_data[2] = {0x1234567890abcdefULL, 0x13579bdf02468aceULL};
  test_vld1q_lane_u8((const uint8_t *)orig_data);
  return 0;
}
```

this code fail, when `-O3 -fno-inline`.

I see the https://llvm.org/docs/BigEndianNEON.html , but I still confuse about the asm:

```
        rev64   v0.16b, v0.16b
        ext     v0.16b, v0.16b, v0.16b, #8
        rev64   v0.16b, v0.16b
        ext     v0.16b, v0.16b, v0.16b, #8
```

this code seem do nothing, but appear many times. 

Can anyone give me some clue about this fail? Or just narrow this problem?

I opt bisect it, it's fail in `SLPVectorizerPass`, but I guess it just introduced this problem, but not the main point. 


---

# 57
### compiler : `LLVM`
### title : `Incorrect value of requires expression involving discarded value`
### open_at : `2023-09-09T10:13:35Z`
### link : https://github.com/llvm/llvm-project/issues/65846
### status : `open`
### tags : `clang:frontend, concepts, `
### content : 
https://godbolt.org/z/63bf61Esd

```cpp
template <typename T>
bool foo(T x) {
    (int(*)[((void)x, 1)])nullptr; // valid

    return requires {
            (int(*)[((void)x, 1)])nullptr; // clangs returns false
    };
}
bool b = foo(0);
```

When foo a function, `b` is true, if it's a template, `b` becomes false.

replacing `((void)x, 1)` by `1` makes `b` true. but `(void)b` is a discarded value expression so `((void)x, 1)` is a valid constant.
clang is also happy with that expression outside of requires expressions, included in constant evaluated and unevaluated context



---

# 58
### compiler : `LLVM`
### title : `Failure to match alias template against template template parameter`
### open_at : `2023-09-09T07:49:51Z`
### link : https://github.com/llvm/llvm-project/issues/65843
### status : `open`
### tags : `c++, clang:frontend, rejects-valid, `
### content : 
```c++
template<template<class T> class> struct A {};
template<class T> struct Q {};
template<class T> using R = Q<T>;
int f(A<R>);
int g(A<Q> a) { return f(a); }
```
GCC accepts (since 4.9.0), Clang rejects with:
```console
<source>:5:24: error: no matching function for call to 'f'
int g(A<Q> a) { return f(a); }
                       ^
<source>:4:5: note: candidate function not viable: no known conversion from 'A<template Q>' to 'A<template R>' for 1st argument
int f(A<R>);
    ^
```
`-frelaxed-template-template-args` doesn't seem to help in any recent major.


---

# 59
### compiler : `LLVM`
### title : `clang: concept checking bug in out-of-line definitions of inner class member functions`
### open_at : `2023-09-08T21:23:16Z`
### link : https://github.com/llvm/llvm-project/issues/65810
### status : `closed`
### tags : `c++20, clang:frontend, concepts, `
### content : 
This code:

```cpp
template<typename Param>
concept TrivialConcept =
  requires(Param param) {
    (void)param;
  };

template <typename T>
struct Base {
    class InnerClass;
};

template <typename T>
class Base<T>::InnerClass {
    template <typename Param>
    requires TrivialConcept<Param> 
    int func(Param param) const;
};

template <typename T>
template <typename Param>
requires TrivialConcept<Param>
int Base<T>::InnerClass::func(Param param) const {
    return 0;
}
```

Works on clang-16 and gcc trunk, fails on clang trunk. I believe it should be allowed per C++20 and above.

Bisecting points to 6db007a0654e as the likely culprit (this got reverted a couple of times previously for similar issues; this one slipped past).

Tagging a few interested people from the diff and from #63782, which points to the same commit:
@alexander-shaposhnikov @erichkeane @shafik 


---

# 60
### compiler : `LLVM`
### title : `Clang cannot use _Atomic qualified integer type as controlling expression in switch statement`
### open_at : `2023-09-07T00:54:59Z`
### link : https://github.com/llvm/llvm-project/issues/65557
### status : `closed`
### tags : `c, clang:frontend, confirmed, `
### content : 
Clang cannot use _Atomic qualified integer type as controlling expression in switch statement.
Minimal example program that will fail to compile:
```c
#include <stdatomic.h>
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    _Atomic int x = 0;
    switch(x) {
        default:
            break;
    }
    return EXIT_SUCCESS;
}
```
Building with Clang 16.0.6 results in build error with following message:
```
main.c:7:5: error: statement requires expression of integer type ('_Atomic(int)' invalid)
    switch(x) {
    ^      ~
```


---

# 61
### compiler : `LLVM`
### title : `Assumptions not working with complex conditionals`
### open_at : `2023-09-06T17:21:01Z`
### link : https://github.com/llvm/llvm-project/issues/65504
### status : `open`
### tags : `llvm:optimizations, missed-optimization, `
### content : 
https://godbolt.org/z/h14s5TGc5 is an example where a `__builtin_assume` containing an `||` conditional isn't working as expected. I wanted to assert that a value was in a particular range, and the expectation was that the `__builtin_assume` would result in the cases for 21 and 28 being optimized out. Removing the `||`, as in https://godbolt.org/z/ja5xsxoMo, does work as expected. See https://discourse.llvm.org/t/builtin-assume-with-complex-condition-not-working/73267 for more discussion.`

```cpp
int systemGetVer() __attribute__((pure));
int getVer() {
    int i = systemGetVer();
    __builtin_assume(i == -1 || i >= 29);
    return i;
}

void foo(int);
void baz() {
    switch (getVer()) {
    case -1:
        foo(100);
        break;
    case 21:
        foo(121);
        break;
    case 28:
        foo(128);
        break;
    case 29:
        foo(129);
        break;
    case 31:
        foo(131);
        break;
    }
}
```

---

# 62
### compiler : `LLVM`
### title : `Possible incorrect code generation when using variable templates`
### open_at : `2023-01-30T01:50:28Z`
### link : https://github.com/llvm/llvm-project/issues/60373
### status : `open`
### tags : `clang:frontend, miscompilation, `
### content : 
Hello,

I'm encountering an issue with member variables not being initialised properly after moving from GCC to Clang. I managed to boil it down to the following minimal example:

```cpp
template <typename T>
struct A{
    int x = 10;
};

template <typename T>
struct B{
    A<T> a;
};

template <typename T>
A<T> a;

template <typename T>
auto aa = a<T>;

template <typename T>
B<T> b = {
    aa<T>
};

int main(){
    return b<float>.a.x;
}
```

[Same example on the compiler explorer](https://godbolt.org/z/5aG8TWzTx)

I'm expecting it to return `10` (which GCC does) but Clang returns `0`

Best regards!
Jonas`


---

# 63
### compiler : `LLVM`
### title : `Missed function specialization (Clang vs GCC)`
### open_at : `2023-01-29T19:09:27Z`
### link : https://github.com/llvm/llvm-project/issues/60368
### status : `open`
### tags : `llvm:optimizations, missed-optimization, `
### content : 
```c
int __attribute__ ((noinline))
foo (int arg)
{
  return 2 * arg;
}

int
bar (int arg)
{
  return foo (5);
}

```

Since Func Specialization pass was enabled, I would expect GCC-like codegen:
```asm
foo.constprop.0:
        mov     eax, 10
        ret
foo:
        lea     eax, [rdi+rdi]
        ret
bar:
        jmp     foo.constprop.0 // or just  mov     eax, 10
```

Current codegen:
```asm
foo:                                    # @foo
        lea     eax, [rdi + rdi]
        ret
bar:                                    # @bar
        mov     edi, 5
        jmp     foo                             # TAILCALL
```

https://godbolt.org/z/Yod4rfhvs


---

# 64
### compiler : `LLVM`
### title : `if-conversion creating dead references to removed MachineBasicBlocks in INLINEASM_BR`
### open_at : `2023-01-28T00:27:13Z`
### link : https://github.com/llvm/llvm-project/issues/60346
### status : `closed`
### tags : `llvm:codegen, regression, release:backport, invalid-code-generation, release:merged, `
### content : 
via @arndb :
```c
_Bool arch_static_branch_branch;

inline _Bool arch_static_branch() {
  asm goto(".word b, %l[l_yes], %c0\n\t"
           :
           : "i"(&arch_static_branch_branch)
           :
           : l_yes);
  return 0;
l_yes:
  return 1;
}

void __dynamic_dev_dbg(char *, ...);
static void tusb1210_chg_det_set_type(int type) {
  if (arch_static_branch())
    __dynamic_dev_dbg("", type);
}

void tusb1210_chg_det_work(char v) {
  if (v)
    tusb1210_chg_det_set_type(1);
  else
    tusb1210_chg_det_set_type(0);
}
```
`-O2 --target=arm-linux-gnueabi` produces an invalid `.long   ".LBB0_-1"` where before it would produce `.long   .Ltmp2`.

Bisection converged on https://reviews.llvm.org/D130316.

This specific test case seems specific to the arm backend; x86 and aarch64 don't repro.  Will dig more next week.

cc @nikic @bwendling @efriedma-quic @jyknight 


---

# 65
### compiler : `LLVM`
### title : `[Clang] [Concepts] Regression between 15.x and trunk: satisfaction of constraint depends on itself`
### open_at : `2023-01-27T00:46:06Z`
### link : https://github.com/llvm/llvm-project/issues/60323
### status : `closed`
### tags : `clang:frontend, regression, concepts, `
### content : 
https://godbolt.org/z/vEb55MGrM is a reproducer that occurs at least in 0d6b26b4d3e3991da16f5b7f53e397b0051e8598 and on current trunk, but did not occur in 7520d187cf0dedcf5085f71bc1a5472c75cc8dbb as far as I can tell.  It would be good to fix this and get it into LLVM 16 before the release.

The bug here seems to be that Clang is looking at the textual form of the requires-clause and deciding that "requires { go(t); } depends on requires { go(t); }"; but the two requires-clauses are in different class scopes, where the word go refers to completely different member functions.

Explicitly specifying which `go` we're referring to by using `this` is a workaround as you can see in https://godbolt.org/z/Gccahddnf


---

# 66
### compiler : `LLVM`
### title : `machine-cse pass breaks __builtin_setjmp on powerpc`
### open_at : `2023-01-26T23:37:54Z`
### link : https://github.com/llvm/llvm-project/issues/60320
### status : `open`
### tags : `llvm:optimizations, `
### content : 
The following code is simplified from a program in which `__builtin_setjmp` always returns 0 (at optimization level -Og, not all optimization levels tested).
```cpp
typedef enum memory_order {
  memory_order_relaxed = 0,
  memory_order_consume = 1,
  memory_order_acquire = 2,
  memory_order_release = 3,
  memory_order_acq_rel = 4,
  memory_order_seq_cst = 5
} memory_order;

struct G {
    volatile _Atomic(_Bool) init;
    void *ctx[5];
};

extern void first(void), second(void);

void bad_setjmp(struct G *g) {

    __c11_atomic_store(&g->init, 1, memory_order_release);

    if (__builtin_setjmp(g->ctx) == 0) {
        first();
    } else {
        second();
    }
}
```

In the assembly code I find
```asm
	bcl 20, 31, .LBB0_5
	#EH_SjLj_Setup	.LBB0_5
```

This is wrong.  The correct code, which you get if you change the constant `1` to `0` in the `__c11_atomic_store` call, is
```asm
	bcl 20, 31, .LBB0_3
	li 3, 1
	#EH_SjLj_Setup	.LBB0_3
```

The `bcl` instruction saves the address of the following instruction in a register.  A call to `__builtin_longjmp` resumes at that address.  The instruction there should set the return value of `__builtin_setjmp` to 1.  The instruction was moved out of place by the machine-cse pass, which took
```
  SYNC 1
  %1:gprc = LI 1
  STB killed %1:gprc, 0, %0:g8rc_and_g8rc_nox0 :: (volatile store monotonic (s8) into %ir.g, align 8)
  ...
  BCLalways %bb.4, <regmask $zero $zero8>, implicit-def $lr, implicit $rm
  %8:gprc = LI 1
  EH_SjLj_Setup %bb.4
  B %bb.5
```
and eliminated the set of `%8` in favor of reusing `%1`:
```
  SYNC 1
  %1:gprc = LI 1
  STB %1:gprc, 0, %0:g8rc_and_g8rc_nox0 :: (volatile store monotonic (s8) into %ir.g, align 8)
  ...
  BCLalways %bb.4, <regmask $zero $zero8>, implicit-def $lr, implicit $rm
  EH_SjLj_Setup %bb.4
  B %bb.5
```
This transformation is invalid.  The instruction after BCLalways is reachable by __builtin_longjmp and moving the instruction earlier causes it not to execute at the right time.

The instruction description for this particular `bcl` may need to indicate that the instruction overwrites all registers and memory (except SP, FP, BP, and TOC, which revert to their saved values).

An IR file for testing is attached.
[invoke.txt](https://github.com/llvm/llvm-project/files/10514256/invoke.txt)



---

# 67
### compiler : `LLVM`
### title : `clang c++20: Associated constraints added to a default constructor are excessively checked`
### open_at : `2023-01-25T16:47:21Z`
### link : https://github.com/llvm/llvm-project/issues/60293
### status : `open`
### tags : `c++20, clang:frontend, `
### content : 
In the following code snippet, the declaration of typedef-name `CW` is accepted by msvc and gcc, but rejected by clang. [Godbolt link](https://godbolt.org/z/bGMdTh8qs).

I think clang is probably buggy here. When determining whether `decltype(ConstrainedWrapper<Wrapped>{std::declval<Wrapped>()})` is well-formed, clang seemly excessively requires the associated constraints of the default constructor to be satisfied, even if the default constructor is not selected.

```C++
#include <concepts>
#include <cstddef>
#include <utility>

struct NoDefaultCtor {
    constexpr explicit NoDefaultCtor(std::nullptr_t) {}
};

template<class T>
struct Wrapper {
    Wrapper() = default;
    constexpr explicit Wrapper(T x) : val(std::move(x)) {}

    T val{};
};

template<class T>
struct ConstrainedWrapper {
    ConstrainedWrapper() requires std::default_initializable<T> = default;

    constexpr explicit ConstrainedWrapper(T x) : val(std::move(x)) {}

    T val{};
};

using Wrapped             = Wrapper<NoDefaultCtor>;
using W [[maybe_unused]]  = decltype(Wrapper<Wrapped>{std::declval<Wrapped>()});
using CW [[maybe_unused]] = decltype(ConstrainedWrapper<Wrapped>{std::declval<Wrapped>()}); // <- clang is buggy here
```


---

# 68
### compiler : `LLVM`
### title : `[clang] Multiple destructor calls emitted with consteval usage in switch statement`
### open_at : `2023-01-24T07:44:01Z`
### link : https://github.com/llvm/llvm-project/issues/60249
### status : `open`
### tags : `c++20, clang:frontend, needs-reduction, `
### content : 
I have the following source (haven't managed to reduce this further with multiple approaches, so sorry this is a bit long, maybe someone can help me?) which seems to generate the wrong assembly:

```c++
namespace {
std::shared_ptr<spdlog::logger> qml_logger    = nullptr;

void
qmlMessageHandler(QtMsgType type, const QMessageLogContext &context, const QString &msg)
{
    std::string localMsg = msg.toStdString();
    const char *file     = context.file ? context.file : "";
    const char *function = context.function ? context.function : "";

    if (
      msg.endsWith(QStringLiteral("Both point size and pixel size set. Using pixel size.")))
        return;

    switch (type) {
    case QtDebugMsg:
        nhlog::qml()->debug("{} ({}:{}, {})", localMsg, file, context.line, function);
        break;
    case QtInfoMsg:
        nhlog::qml()->info("{} ({}:{}, {})", localMsg, file, context.line, function);
        break;
    case QtWarningMsg:
        nhlog::qml()->warn("{} ({}:{}, {})", localMsg, file, context.line, function);
        break;
    case QtCriticalMsg:
        nhlog::qml()->critical("{} ({}:{}, {})", localMsg, file, context.line, function);
        break;
    case QtFatalMsg:
        nhlog::qml()->critical("{} ({}:{}, {})", localMsg, file, context.line, function);
        break;
    }
}
}

namespace nhlog {
std::shared_ptr<spdlog::logger>
qml()
{
    return qml_logger;
}
}
```

Full context: https://github.com/Nheko-Reborn/nheko/blob/8835040db61d039af4bab34e36b1e634bb9d1d1f/src/Logging.cpp

To my understanding, this is legal code and I ran this with undefined sanitizer. It however causes a crash and triggers the address sanitizer:

<details><summary>output</summary>
<p>

```console
==29161==ERROR: AddressSanitizer: stack-use-after-scope on address 0x7fd44a03b518 at pc 0x55ec7d083e2e bp 0x7fffc5a7c090 sp 0x7fffc5a7c088
READ of size 8 at 0x7fd44a03b518 thread T0
    #0 0x55ec7d083e2d in std::__shared_count<(__gnu_cxx::_Lock_policy)2>::~__shared_count() /usr/lib/gcc/x86_64-pc-linux-gnu/12/include/g++-v12/bits/shared_ptr_base.h:1070:6
    #1 0x55ec7da9d22c in std::__shared_ptr<spdlog::logger, (__gnu_cxx::_Lock_policy)2>::~__shared_ptr() /usr/lib/gcc/x86_64-pc-linux-gnu/12/include/g++-v12/bits/shared_ptr_base.h:1524:31
    #2 0x55ec7da80568 in std::shared_ptr<spdlog::logger>::~shared_ptr() /usr/lib/gcc/x86_64-pc-linux-gnu/12/include/g++-v12/bits/shared_ptr.h:175:11
    #3 0x55ec7f4410f9 in (anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&) /home/nicolas/Dokumente/devel/open-source/nheko/src/Logging.cpp:62:5
    #4 0x7fd4501a49b7 in qt_message_print /usr/src/debug/dev-qt/qtcore-5.15.8-r1/qtbase-everywhere-src-5.15.8/src/corelib/global/qlogging.cpp:1843:57
    #5 0x7fd4501a608f in qt_message_output(QtMsgType, QMessageLogContext const&, QString const&) /usr/src/debug/dev-qt/qtcore-5.15.8-r1/qtbase-everywhere-src-5.15.8/src/corelib/global/qlogging.cpp:1924:21
    #6 0x7fd4502a202f in QDebug::~QDebug() /usr/src/debug/dev-qt/qtcore-5.15.8-r1/qtbase-everywhere-src-5.15.8/src/corelib/io/qdebug.cpp:154:30
    #7 0x7fd4517ac4cf in dumpwarning /usr/src/debug/dev-qt/qtdeclarative-5.15.8-r2/qtdeclarative-everywhere-src-5.15.8/src/qml/qml/qqmlengine.cpp:2073:55
    #8 0x7fd4517c2d44 in QQmlComponentPrivate::complete(QQmlEnginePrivate*, QQmlComponentPrivate::ConstructionState*) /usr/src/debug/dev-qt/qtdeclarative-5.15.8-r2/qtdeclarative-everywhere-src-5.15.8/src/qml/qml/qqmlcomponent.cpp:1008:36
    #9 0x7fd4517c2d44 in QQmlComponentPrivate::complete(QQmlEnginePrivate*, QQmlComponentPrivate::ConstructionState*) /usr/src/debug/dev-qt/qtdeclarative-5.15.8-r2/qtdeclarative-everywhere-src-5.15.8/src/qml/qml/qqmlcomponent.cpp:996:6
    #10 0x7fd4517c4e2f in QQmlComponentPrivate::completeCreate() /usr/src/debug/dev-qt/qtdeclarative-5.15.8-r2/qtdeclarative-everywhere-src-5.15.8/src/qml/qml/qqmlcomponent.cpp:1092:17
    #11 0x7fd4517c4fe5 in QQmlComponent::completeCreate() /usr/src/debug/dev-qt/qtdeclarative-5.15.8-r2/qtdeclarative-everywhere-src-5.15.8/src/qml/qml/qqmlcomponent.cpp:1079:22
    #12 0x7fd4517c4fe5 in QQmlComponent::create(QQmlContext*) /usr/src/debug/dev-qt/qtdeclarative-5.15.8-r2/qtdeclarative-everywhere-src-5.15.8/src/qml/qml/qqmlcomponent.cpp:825:23
    #13 0x7fd451d24c9b in QQuickView::continueExecute() /usr/src/debug/dev-qt/qtdeclarative-5.15.8-r2/qtdeclarative-everywhere-src-5.15.8/src/quick/items/qquickview.cpp:492:55
    #14 0x55ec7f491a60 in MainWindow::MainWindow(QWindow*) /home/nicolas/Dokumente/devel/open-source/nheko/src/MainWindow.cpp:93:5
    #15 0x55ec7f77e6f6 in main /home/nicolas/Dokumente/devel/open-source/nheko/src/main.cpp:341:16
    #16 0x7fd44f834305 in __libc_start_call_main /usr/src/debug/sys-libs/glibc-2.36-r6/glibc-2.36/csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #17 0x7fd44f8343c7 in __libc_start_main /usr/src/debug/sys-libs/glibc-2.36-r6/glibc-2.36/csu/../csu/libc-start.c:381:3
    #18 0x55ec7ce3b940 in _start (/home/nicolas/Dokumente/devel/open-source/nheko/build-clang-san/nheko+0x72cf940)
```

This is with libfmt 9.1.0 and spdlog 1.11.0.

The following assembly is generated for the `qmlMessageHandler` function:

```objdump
00000000000008a0 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)>:
{
 8a0:	55                   	push   rbp
 8a1:	48 89 e5             	mov    rbp,rsp
 8a4:	48 81 ec 70 01 00 00 	sub    rsp,0x170
 8ab:	64 48 8b 04 25 28 00 00 00 	mov    rax,QWORD PTR fs:0x28
 8b4:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
 8b8:	89 bd 64 ff ff ff    	mov    DWORD PTR [rbp-0x9c],edi
 8be:	48 89 b5 58 ff ff ff 	mov    QWORD PTR [rbp-0xa8],rsi
 8c5:	48 89 95 50 ff ff ff 	mov    QWORD PTR [rbp-0xb0],rdx
    std::string localMsg = msg.toStdString();
 8cc:	48 8b b5 50 ff ff ff 	mov    rsi,QWORD PTR [rbp-0xb0]
 8d3:	48 8d 7d d8          	lea    rdi,[rbp-0x28]
 8d7:	e8 00 00 00 00       	call   8dc <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x3c>	8d8: R_X86_64_PLT32	QString::toStdString[abi:cxx11]() const-0x4
    const char *file     = context.file ? context.file : "";
 8dc:	48 8b 85 58 ff ff ff 	mov    rax,QWORD PTR [rbp-0xa8]
 8e3:	48 83 78 08 00       	cmp    QWORD PTR [rax+0x8],0x0
 8e8:	0f 84 17 00 00 00    	je     905 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x65>
 8ee:	48 8b 85 58 ff ff ff 	mov    rax,QWORD PTR [rbp-0xa8]
 8f5:	48 8b 40 08          	mov    rax,QWORD PTR [rax+0x8]
 8f9:	48 89 85 e8 fe ff ff 	mov    QWORD PTR [rbp-0x118],rax
 900:	e9 13 00 00 00       	jmp    918 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x78>
 905:	48 8d 05 00 00 00 00 	lea    rax,[rip+0x0]        # 90c <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x6c>	908: R_X86_64_PC32	.L.str.15-0x4
 90c:	48 89 85 e8 fe ff ff 	mov    QWORD PTR [rbp-0x118],rax
 913:	e9 00 00 00 00       	jmp    918 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x78>
 918:	48 8b 85 e8 fe ff ff 	mov    rax,QWORD PTR [rbp-0x118]
 91f:	48 89 45 d0          	mov    QWORD PTR [rbp-0x30],rax
    const char *function = context.function ? context.function : "";
 923:	48 8b 85 58 ff ff ff 	mov    rax,QWORD PTR [rbp-0xa8]
 92a:	48 83 78 10 00       	cmp    QWORD PTR [rax+0x10],0x0
 92f:	0f 84 17 00 00 00    	je     94c <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0xac>
 935:	48 8b 85 58 ff ff ff 	mov    rax,QWORD PTR [rbp-0xa8]
 93c:	48 8b 40 10          	mov    rax,QWORD PTR [rax+0x10]
 940:	48 89 85 e0 fe ff ff 	mov    QWORD PTR [rbp-0x120],rax
 947:	e9 13 00 00 00       	jmp    95f <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0xbf>
 94c:	48 8d 05 00 00 00 00 	lea    rax,[rip+0x0]        # 953 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0xb3>	94f: R_X86_64_PC32	.L.str.15-0x4
 953:	48 89 85 e0 fe ff ff 	mov    QWORD PTR [rbp-0x120],rax
 95a:	e9 00 00 00 00       	jmp    95f <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0xbf>
 95f:	48 8b 85 e0 fe ff ff 	mov    rax,QWORD PTR [rbp-0x120]
 966:	48 89 45 c8          	mov    QWORD PTR [rbp-0x38],rax
      msg.endsWith(QStringLiteral("Both point size and pixel size set. Using pixel size.")))
 96a:	48 8b 85 50 ff ff ff 	mov    rax,QWORD PTR [rbp-0xb0]
 971:	48 89 85 c8 fe ff ff 	mov    QWORD PTR [rbp-0x138],rax
 978:	48 8d 7d c0          	lea    rdi,[rbp-0x40]
 97c:	48 89 bd d0 fe ff ff 	mov    QWORD PTR [rbp-0x130],rdi
 983:	48 8d 75 b8          	lea    rsi,[rbp-0x48]
 987:	e8 54 05 00 00       	call   ee0 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)::$_0::operator()() const>
 98c:	48 8b bd c8 fe ff ff 	mov    rdi,QWORD PTR [rbp-0x138]
 993:	48 8b b5 d0 fe ff ff 	mov    rsi,QWORD PTR [rbp-0x130]
 99a:	ba 01 00 00 00       	mov    edx,0x1
 99f:	e8 00 00 00 00       	call   9a4 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x104>	9a0: R_X86_64_PLT32	QString::endsWith(QString const&, Qt::CaseSensitivity) const-0x4
 9a4:	88 85 df fe ff ff    	mov    BYTE PTR [rbp-0x121],al
 9aa:	e9 00 00 00 00       	jmp    9af <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x10f>
 9af:	48 8d 7d c0          	lea    rdi,[rbp-0x40]
 9b3:	e8 00 00 00 00       	call   9b8 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x118>	9b4: R_X86_64_PLT32	QString::~QString()-0x4
 9b8:	8a 85 df fe ff ff    	mov    al,BYTE PTR [rbp-0x121]
 9be:	a8 01                	test   al,0x1
 9c0:	0f 85 05 00 00 00    	jne    9cb <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x12b>
 9c6:	e9 2f 00 00 00       	jmp    9fa <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x15a>
 9cb:	c7 85 40 ff ff ff 01 00 00 00 	mov    DWORD PTR [rbp-0xc0],0x1
        return;
 9d5:	e9 cb 03 00 00       	jmp    da5 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x505>
 9da:	48 89 c1             	mov    rcx,rax
}
 9dd:	89 d0                	mov    eax,edx
 9df:	48 89 8d 48 ff ff ff 	mov    QWORD PTR [rbp-0xb8],rcx
 9e6:	89 85 44 ff ff ff    	mov    DWORD PTR [rbp-0xbc],eax
      msg.endsWith(QStringLiteral("Both point size and pixel size set. Using pixel size.")))
 9ec:	48 8d 7d c0          	lea    rdi,[rbp-0x40]
 9f0:	e8 00 00 00 00       	call   9f5 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x155>	9f1: R_X86_64_PLT32	QString::~QString()-0x4
 9f5:	e9 d3 03 00 00       	jmp    dcd <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x52d>
    switch (type) {
 9fa:	8b 85 64 ff ff ff    	mov    eax,DWORD PTR [rbp-0x9c]
 a00:	48 89 85 c0 fe ff ff 	mov    QWORD PTR [rbp-0x140],rax
 a07:	48 83 e8 04          	sub    rax,0x4
 a0b:	0f 87 8a 03 00 00    	ja     d9b <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x4fb>
 a11:	48 8b 85 c0 fe ff ff 	mov    rax,QWORD PTR [rbp-0x140]
 a18:	48 8d 0d 00 00 00 00 	lea    rcx,[rip+0x0]        # a1f <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x17f>	a1b: R_X86_64_PC32	.rodata-0x4
 a1f:	48 63 04 81          	movsxd rax,DWORD PTR [rcx+rax*4]
 a23:	48 01 c8             	add    rax,rcx
 a26:	ff e0                	jmp    rax
 a28:	48 8d 7d a8          	lea    rdi,[rbp-0x58]
 a2c:	48 89 bd b8 fe ff ff 	mov    QWORD PTR [rbp-0x148],rdi
        nhlog::qml()->debug("{} ({}:{}, {})", localMsg, file, context.line, function);
 a33:	e8 00 00 00 00       	call   a38 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x198>	a34: R_X86_64_PLT32	nhlog::qml()-0x4
 a38:	48 8b bd b8 fe ff ff 	mov    rdi,QWORD PTR [rbp-0x148]
 a3f:	e8 00 00 00 00       	call   a44 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x1a4>	a40: R_X86_64_PLT32	std::__shared_ptr_access<spdlog::logger, (__gnu_cxx::_Lock_policy)2, false, false>::operator->() const-0x4
 a44:	48 89 c7             	mov    rdi,rax
 a47:	48 8d 05 00 00 00 00 	lea    rax,[rip+0x0]        # a4e <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x1ae>	a4a: R_X86_64_PC32	.L.str.16-0x4
 a4e:	48 89 85 30 ff ff ff 	mov    QWORD PTR [rbp-0xd0],rax
 a55:	48 c7 85 38 ff ff ff 0e 00 00 00 	mov    QWORD PTR [rbp-0xc8],0xe
 a60:	4c 8b 8d 58 ff ff ff 	mov    r9,QWORD PTR [rbp-0xa8]
 a67:	49 83 c1 04          	add    r9,0x4
 a6b:	48 8b b5 30 ff ff ff 	mov    rsi,QWORD PTR [rbp-0xd0]
 a72:	48 8b 95 38 ff ff ff 	mov    rdx,QWORD PTR [rbp-0xc8]
 a79:	48 89 e0             	mov    rax,rsp
 a7c:	48 8d 4d c8          	lea    rcx,[rbp-0x38]
 a80:	48 89 08             	mov    QWORD PTR [rax],rcx
 a83:	48 8d 4d d8          	lea    rcx,[rbp-0x28]
 a87:	4c 8d 45 d0          	lea    r8,[rbp-0x30]
 a8b:	e8 00 00 00 00       	call   a90 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x1f0>	a8c: R_X86_64_PLT32	void spdlog::logger::debug<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >&, char const*&, int const&, char const*&>(fmt::v9::basic_format_string<char, fmt::v9::type_identity<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >&>::type, fmt::v9::type_identity<char const*&>::type, fmt::v9::type_identity<int const&>::type, fmt::v9::type_identity<char const*&>::type>, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >&, char const*&, int const&, char const*&)-0x4
 a90:	e9 00 00 00 00       	jmp    a95 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x1f5>
 a95:	c7 85 40 ff ff ff 02 00 00 00 	mov    DWORD PTR [rbp-0xc0],0x2
        break;
 a9f:	e9 db 02 00 00       	jmp    d7f <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x4df>
 aa4:	48 89 c1             	mov    rcx,rax
}
 aa7:	89 d0                	mov    eax,edx
 aa9:	48 89 8d 48 ff ff ff 	mov    QWORD PTR [rbp-0xb8],rcx
 ab0:	89 85 44 ff ff ff    	mov    DWORD PTR [rbp-0xbc],eax
 ab6:	e9 d2 02 00 00       	jmp    d8d <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x4ed>
 abb:	48 8d 7d 98          	lea    rdi,[rbp-0x68]
 abf:	48 89 bd b0 fe ff ff 	mov    QWORD PTR [rbp-0x150],rdi
        nhlog::qml()->info("{} ({}:{}, {})", localMsg, file, context.line, function);
 ac6:	e8 00 00 00 00       	call   acb <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x22b>	ac7: R_X86_64_PLT32	nhlog::qml()-0x4
 acb:	48 8b bd b0 fe ff ff 	mov    rdi,QWORD PTR [rbp-0x150]
 ad2:	e8 00 00 00 00       	call   ad7 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x237>	ad3: R_X86_64_PLT32	std::__shared_ptr_access<spdlog::logger, (__gnu_cxx::_Lock_policy)2, false, false>::operator->() const-0x4
 ad7:	48 89 c7             	mov    rdi,rax
 ada:	48 8d 05 00 00 00 00 	lea    rax,[rip+0x0]        # ae1 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x241>	add: R_X86_64_PC32	.L.str.16-0x4
 ae1:	48 89 85 20 ff ff ff 	mov    QWORD PTR [rbp-0xe0],rax
 ae8:	48 c7 85 28 ff ff ff 0e 00 00 00 	mov    QWORD PTR [rbp-0xd8],0xe
 af3:	4c 8b 8d 58 ff ff ff 	mov    r9,QWORD PTR [rbp-0xa8]
 afa:	49 83 c1 04          	add    r9,0x4
 afe:	48 8b b5 20 ff ff ff 	mov    rsi,QWORD PTR [rbp-0xe0]
 b05:	48 8b 95 28 ff ff ff 	mov    rdx,QWORD PTR [rbp-0xd8]
 b0c:	48 89 e0             	mov    rax,rsp
 b0f:	48 8d 4d c8          	lea    rcx,[rbp-0x38]
 b13:	48 89 08             	mov    QWORD PTR [rax],rcx
 b16:	48 8d 4d d8          	lea    rcx,[rbp-0x28]
 b1a:	4c 8d 45 d0          	lea    r8,[rbp-0x30]
 b1e:	e8 00 00 00 00       	call   b23 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x283>	b1f: R_X86_64_PLT32	void spdlog::logger::info<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >&, char const*&, int const&, char const*&>(fmt::v9::basic_format_string<char, fmt::v9::type_identity<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >&>::type, fmt::v9::type_identity<char const*&>::type, fmt::v9::type_identity<int const&>::type, fmt::v9::type_identity<char const*&>::type>, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >&, char const*&, int const&, char const*&)-0x4
 b23:	e9 00 00 00 00       	jmp    b28 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x288>
 b28:	c7 85 40 ff ff ff 02 00 00 00 	mov    DWORD PTR [rbp-0xc0],0x2
        break;
 b32:	e9 2c 02 00 00       	jmp    d63 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x4c3>
 b37:	48 89 c1             	mov    rcx,rax
}
 b3a:	89 d0                	mov    eax,edx
 b3c:	48 89 8d 48 ff ff ff 	mov    QWORD PTR [rbp-0xb8],rcx
 b43:	89 85 44 ff ff ff    	mov    DWORD PTR [rbp-0xbc],eax
 b49:	e9 23 02 00 00       	jmp    d71 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x4d1>
 b4e:	48 8d 7d 88          	lea    rdi,[rbp-0x78]
 b52:	48 89 bd a8 fe ff ff 	mov    QWORD PTR [rbp-0x158],rdi
        nhlog::qml()->warn("{} ({}:{}, {})", localMsg, file, context.line, function);
 b59:	e8 00 00 00 00       	call   b5e <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x2be>	b5a: R_X86_64_PLT32	nhlog::qml()-0x4
 b5e:	48 8b bd a8 fe ff ff 	mov    rdi,QWORD PTR [rbp-0x158]
 b65:	e8 00 00 00 00       	call   b6a <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x2ca>	b66: R_X86_64_PLT32	std::__shared_ptr_access<spdlog::logger, (__gnu_cxx::_Lock_policy)2, false, false>::operator->() const-0x4
 b6a:	48 89 c7             	mov    rdi,rax
 b6d:	48 8d 05 00 00 00 00 	lea    rax,[rip+0x0]        # b74 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x2d4>	b70: R_X86_64_PC32	.L.str.16-0x4
 b74:	48 89 85 10 ff ff ff 	mov    QWORD PTR [rbp-0xf0],rax
 b7b:	48 c7 85 18 ff ff ff 0e 00 00 00 	mov    QWORD PTR [rbp-0xe8],0xe
 b86:	4c 8b 8d 58 ff ff ff 	mov    r9,QWORD PTR [rbp-0xa8]
 b8d:	49 83 c1 04          	add    r9,0x4
 b91:	48 8b b5 10 ff ff ff 	mov    rsi,QWORD PTR [rbp-0xf0]
 b98:	48 8b 95 18 ff ff ff 	mov    rdx,QWORD PTR [rbp-0xe8]
 b9f:	48 89 e0             	mov    rax,rsp
 ba2:	48 8d 4d c8          	lea    rcx,[rbp-0x38]
 ba6:	48 89 08             	mov    QWORD PTR [rax],rcx
 ba9:	48 8d 4d d8          	lea    rcx,[rbp-0x28]
 bad:	4c 8d 45 d0          	lea    r8,[rbp-0x30]
 bb1:	e8 00 00 00 00       	call   bb6 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x316>	bb2: R_X86_64_PLT32	void spdlog::logger::warn<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >&, char const*&, int const&, char const*&>(fmt::v9::basic_format_string<char, fmt::v9::type_identity<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >&>::type, fmt::v9::type_identity<char const*&>::type, fmt::v9::type_identity<int const&>::type, fmt::v9::type_identity<char const*&>::type>, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >&, char const*&, int const&, char const*&)-0x4
 bb6:	e9 00 00 00 00       	jmp    bbb <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x31b>
 bbb:	c7 85 40 ff ff ff 02 00 00 00 	mov    DWORD PTR [rbp-0xc0],0x2
        break;
 bc5:	e9 7d 01 00 00       	jmp    d47 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x4a7>
 bca:	48 89 c1             	mov    rcx,rax
}
 bcd:	89 d0                	mov    eax,edx
 bcf:	48 89 8d 48 ff ff ff 	mov    QWORD PTR [rbp-0xb8],rcx
 bd6:	89 85 44 ff ff ff    	mov    DWORD PTR [rbp-0xbc],eax
 bdc:	e9 74 01 00 00       	jmp    d55 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x4b5>
 be1:	48 8d bd 78 ff ff ff 	lea    rdi,[rbp-0x88]
 be8:	48 89 bd a0 fe ff ff 	mov    QWORD PTR [rbp-0x160],rdi
        nhlog::qml()->critical("{} ({}:{}, {})", localMsg, file, context.line, function);
 bef:	e8 00 00 00 00       	call   bf4 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x354>	bf0: R_X86_64_PLT32	nhlog::qml()-0x4
 bf4:	48 8b bd a0 fe ff ff 	mov    rdi,QWORD PTR [rbp-0x160]
 bfb:	e8 00 00 00 00       	call   c00 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x360>	bfc: R_X86_64_PLT32	std::__shared_ptr_access<spdlog::logger, (__gnu_cxx::_Lock_policy)2, false, false>::operator->() const-0x4
 c00:	48 89 c7             	mov    rdi,rax
 c03:	48 8d 05 00 00 00 00 	lea    rax,[rip+0x0]        # c0a <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x36a>	c06: R_X86_64_PC32	.L.str.16-0x4
 c0a:	48 89 85 00 ff ff ff 	mov    QWORD PTR [rbp-0x100],rax
 c11:	48 c7 85 08 ff ff ff 0e 00 00 00 	mov    QWORD PTR [rbp-0xf8],0xe
 c1c:	4c 8b 8d 58 ff ff ff 	mov    r9,QWORD PTR [rbp-0xa8]
 c23:	49 83 c1 04          	add    r9,0x4
 c27:	48 8b b5 00 ff ff ff 	mov    rsi,QWORD PTR [rbp-0x100]
 c2e:	48 8b 95 08 ff ff ff 	mov    rdx,QWORD PTR [rbp-0xf8]
 c35:	48 89 e0             	mov    rax,rsp
 c38:	48 8d 4d c8          	lea    rcx,[rbp-0x38]
 c3c:	48 89 08             	mov    QWORD PTR [rax],rcx
 c3f:	48 8d 4d d8          	lea    rcx,[rbp-0x28]
 c43:	4c 8d 45 d0          	lea    r8,[rbp-0x30]
 c47:	e8 00 00 00 00       	call   c4c <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x3ac>	c48: R_X86_64_PLT32	void spdlog::logger::critical<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >&, char const*&, int const&, char const*&>(fmt::v9::basic_format_string<char, fmt::v9::type_identity<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >&>::type, fmt::v9::type_identity<char const*&>::type, fmt::v9::type_identity<int const&>::type, fmt::v9::type_identity<char const*&>::type>, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >&, char const*&, int const&, char const*&)-0x4
 c4c:	e9 00 00 00 00       	jmp    c51 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x3b1>
 c51:	c7 85 40 ff ff ff 02 00 00 00 	mov    DWORD PTR [rbp-0xc0],0x2
        break;
 c5b:	e9 c5 00 00 00       	jmp    d25 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x485>
 c60:	48 89 c1             	mov    rcx,rax
}
 c63:	89 d0                	mov    eax,edx
 c65:	48 89 8d 48 ff ff ff 	mov    QWORD PTR [rbp-0xb8],rcx
 c6c:	89 85 44 ff ff ff    	mov    DWORD PTR [rbp-0xbc],eax
 c72:	e9 bf 00 00 00       	jmp    d36 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x496>
 c77:	48 8d bd 68 ff ff ff 	lea    rdi,[rbp-0x98]
 c7e:	48 89 bd 98 fe ff ff 	mov    QWORD PTR [rbp-0x168],rdi
        nhlog::qml()->critical("{} ({}:{}, {})", localMsg, file, context.line, function);
 c85:	e8 00 00 00 00       	call   c8a <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x3ea>	c86: R_X86_64_PLT32	nhlog::qml()-0x4
 c8a:	48 8b bd 98 fe ff ff 	mov    rdi,QWORD PTR [rbp-0x168]
 c91:	e8 00 00 00 00       	call   c96 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x3f6>	c92: R_X86_64_PLT32	std::__shared_ptr_access<spdlog::logger, (__gnu_cxx::_Lock_policy)2, false, false>::operator->() const-0x4
 c96:	48 89 c7             	mov    rdi,rax
 c99:	48 8d 05 00 00 00 00 	lea    rax,[rip+0x0]        # ca0 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x400>	c9c: R_X86_64_PC32	.L.str.16-0x4
 ca0:	48 89 85 f0 fe ff ff 	mov    QWORD PTR [rbp-0x110],rax
 ca7:	48 c7 85 f8 fe ff ff 0e 00 00 00 	mov    QWORD PTR [rbp-0x108],0xe
 cb2:	4c 8b 8d 58 ff ff ff 	mov    r9,QWORD PTR [rbp-0xa8]
 cb9:	49 83 c1 04          	add    r9,0x4
 cbd:	48 8b b5 f0 fe ff ff 	mov    rsi,QWORD PTR [rbp-0x110]
 cc4:	48 8b 95 f8 fe ff ff 	mov    rdx,QWORD PTR [rbp-0x108]
 ccb:	48 89 e0             	mov    rax,rsp
 cce:	48 8d 4d c8          	lea    rcx,[rbp-0x38]
 cd2:	48 89 08             	mov    QWORD PTR [rax],rcx
 cd5:	48 8d 4d d8          	lea    rcx,[rbp-0x28]
 cd9:	4c 8d 45 d0          	lea    r8,[rbp-0x30]
 cdd:	e8 00 00 00 00       	call   ce2 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x442>	cde: R_X86_64_PLT32	void spdlog::logger::critical<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >&, char const*&, int const&, char const*&>(fmt::v9::basic_format_string<char, fmt::v9::type_identity<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >&>::type, fmt::v9::type_identity<char const*&>::type, fmt::v9::type_identity<int const&>::type, fmt::v9::type_identity<char const*&>::type>, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >&, char const*&, int const&, char const*&)-0x4
 ce2:	e9 00 00 00 00       	jmp    ce7 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x447>
 ce7:	c7 85 40 ff ff ff 02 00 00 00 	mov    DWORD PTR [rbp-0xc0],0x2
    }
 cf1:	48 8d bd 68 ff ff ff 	lea    rdi,[rbp-0x98]
 cf8:	e8 00 00 00 00       	call   cfd <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x45d>	cf9: R_X86_64_PLT32	std::shared_ptr<spdlog::logger>::~shared_ptr()-0x4
 cfd:	e9 23 00 00 00       	jmp    d25 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x485>
 d02:	48 89 c1             	mov    rcx,rax
}
 d05:	89 d0                	mov    eax,edx
 d07:	48 89 8d 48 ff ff ff 	mov    QWORD PTR [rbp-0xb8],rcx
 d0e:	89 85 44 ff ff ff    	mov    DWORD PTR [rbp-0xbc],eax
    }
 d14:	48 8d bd 68 ff ff ff 	lea    rdi,[rbp-0x98]
 d1b:	e8 00 00 00 00       	call   d20 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x480>	d1c: R_X86_64_PLT32	std::shared_ptr<spdlog::logger>::~shared_ptr()-0x4
 d20:	e9 11 00 00 00       	jmp    d36 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x496>
 d25:	48 8d bd 78 ff ff ff 	lea    rdi,[rbp-0x88]
 d2c:	e8 00 00 00 00       	call   d31 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x491>	d2d: R_X86_64_PLT32	std::shared_ptr<spdlog::logger>::~shared_ptr()-0x4
 d31:	e9 11 00 00 00       	jmp    d47 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x4a7>
 d36:	48 8d bd 78 ff ff ff 	lea    rdi,[rbp-0x88]
 d3d:	e8 00 00 00 00       	call   d42 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x4a2>	d3e: R_X86_64_PLT32	std::shared_ptr<spdlog::logger>::~shared_ptr()-0x4
 d42:	e9 0e 00 00 00       	jmp    d55 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x4b5>
 d47:	48 8d 7d 88          	lea    rdi,[rbp-0x78]
 d4b:	e8 00 00 00 00       	call   d50 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x4b0>	d4c: R_X86_64_PLT32	std::shared_ptr<spdlog::logger>::~shared_ptr()-0x4
 d50:	e9 0e 00 00 00       	jmp    d63 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x4c3>
 d55:	48 8d 7d 88          	lea    rdi,[rbp-0x78]
 d59:	e8 00 00 00 00       	call   d5e <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x4be>	d5a: R_X86_64_PLT32	std::shared_ptr<spdlog::logger>::~shared_ptr()-0x4
 d5e:	e9 0e 00 00 00       	jmp    d71 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x4d1>
 d63:	48 8d 7d 98          	lea    rdi,[rbp-0x68]
 d67:	e8 00 00 00 00       	call   d6c <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x4cc>	d68: R_X86_64_PLT32	std::shared_ptr<spdlog::logger>::~shared_ptr()-0x4
 d6c:	e9 0e 00 00 00       	jmp    d7f <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x4df>
 d71:	48 8d 7d 98          	lea    rdi,[rbp-0x68]
 d75:	e8 00 00 00 00       	call   d7a <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x4da>	d76: R_X86_64_PLT32	std::shared_ptr<spdlog::logger>::~shared_ptr()-0x4
 d7a:	e9 0e 00 00 00       	jmp    d8d <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x4ed>
 d7f:	48 8d 7d a8          	lea    rdi,[rbp-0x58]
 d83:	e8 00 00 00 00       	call   d88 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x4e8>	d84: R_X86_64_PLT32	std::shared_ptr<spdlog::logger>::~shared_ptr()-0x4
 d88:	e9 0e 00 00 00       	jmp    d9b <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x4fb>
 d8d:	48 8d 7d a8          	lea    rdi,[rbp-0x58]
 d91:	e8 00 00 00 00       	call   d96 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x4f6>	d92: R_X86_64_PLT32	std::shared_ptr<spdlog::logger>::~shared_ptr()-0x4
 d96:	e9 32 00 00 00       	jmp    dcd <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x52d>
}
 d9b:	c7 85 40 ff ff ff 00 00 00 00 	mov    DWORD PTR [rbp-0xc0],0x0
 da5:	48 8d 7d d8          	lea    rdi,[rbp-0x28]
 da9:	e8 00 00 00 00       	call   dae <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x50e>	daa: R_X86_64_PLT32	std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >::~basic_string()-0x4
 dae:	64 48 8b 04 25 28 00 00 00 	mov    rax,QWORD PTR fs:0x28
 db7:	48 8b 4d f8          	mov    rcx,QWORD PTR [rbp-0x8]
 dbb:	48 39 c8             	cmp    rax,rcx
 dbe:	0f 85 1e 00 00 00    	jne    de2 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x542>
 dc4:	48 81 c4 70 01 00 00 	add    rsp,0x170
 dcb:	5d                   	pop    rbp
 dcc:	c3                   	ret
 dcd:	48 8d 7d d8          	lea    rdi,[rbp-0x28]
 dd1:	e8 00 00 00 00       	call   dd6 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x536>	dd2: R_X86_64_PLT32	std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >::~basic_string()-0x4
 dd6:	48 8b bd 48 ff ff ff 	mov    rdi,QWORD PTR [rbp-0xb8]
 ddd:	e8 00 00 00 00       	call   de2 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x542>	dde: R_X86_64_PLT32	_Unwind_Resume-0x4
 de2:	e8 00 00 00 00       	call   de7 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x547>	de3: R_X86_64_PLT32	__stack_chk_fail-0x4
 de7:	66 0f 1f 84 00 00 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
```

To me this looks like multiple destructor calls are generated for the temporary `shared_ptr`. You can "fix" that by getting rid of the `qml()` call and accessing the `shared_ptr` directly or by putting the logging calls inside a scope. From my understanding, this happens because of the `consteval` constructor for the libfmt arguments. Without the libfmt calls, the destructors seem to happen in the normal places. Specifically that part of the assembly then looks like this:

```objdump
    switch (type) {
 975:   8b 85 74 ff ff ff       mov    eax,DWORD PTR [rbp-0x8c]
 97b:   48 89 85 30 ff ff ff    mov    QWORD PTR [rbp-0xd0],rax
 982:   48 83 e8 04             sub    rax,0x4
 986:   0f 87 8b 00 00 00       ja     a17 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x177>
 98c:   48 8b 85 30 ff ff ff    mov    rax,QWORD PTR [rbp-0xd0]
 993:   48 8d 0d 00 00 00 00    lea    rcx,[rip+0x0]        # 99a <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0xfa> 996: R_X86_64_PC32      .rodata-0x4
 99a:   48 63 04 81             movsxd rax,DWORD PTR [rcx+rax*4]
 99e:   48 01 c8                add    rax,rcx
 9a1:   ff e0                   jmp    rax
        nhlog::qml();
 9a3:   48 8d 7d b8             lea    rdi,[rbp-0x48]
 9a7:   e8 00 00 00 00          call   9ac <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x10c>       9a8: R_X86_64_PLT32     nhlog::qml()-0x4
 9ac:   48 8d 7d b8             lea    rdi,[rbp-0x48]
 9b0:   e8 00 00 00 00          call   9b5 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x115>       9b1: R_X86_64_PLT32     std::shared_ptr<spdlog::logger>::~shared_ptr()-0x4
        break;
 9b5:   e9 5d 00 00 00          jmp    a17 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x177>
        nhlog::qml();
 9ba:   48 8d 7d a8             lea    rdi,[rbp-0x58]
 9be:   e8 00 00 00 00          call   9c3 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x123>       9bf: R_X86_64_PLT32     nhlog::qml()-0x4
 9c3:   48 8d 7d a8             lea    rdi,[rbp-0x58]
 9c7:   e8 00 00 00 00          call   9cc <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x12c>       9c8: R_X86_64_PLT32     std::shared_ptr<spdlog::logger>::~shared_ptr()-0x4
        break;
 9cc:   e9 46 00 00 00          jmp    a17 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x177>
        nhlog::qml();
 9d1:   48 8d 7d 98             lea    rdi,[rbp-0x68]
 9d5:   e8 00 00 00 00          call   9da <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x13a>       9d6: R_X86_64_PLT32     nhlog::qml()-0x4
 9da:   48 8d 7d 98             lea    rdi,[rbp-0x68]
 9de:   e8 00 00 00 00          call   9e3 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x143>       9df: R_X86_64_PLT32     std::shared_ptr<spdlog::logger>::~shared_ptr()-0x4
        break;
 9e3:   e9 2f 00 00 00          jmp    a17 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x177>
        nhlog::qml();
 9e8:   48 8d 7d 88             lea    rdi,[rbp-0x78]
 9ec:   e8 00 00 00 00          call   9f1 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x151>       9ed: R_X86_64_PLT32     nhlog::qml()-0x4
 9f1:   48 8d 7d 88             lea    rdi,[rbp-0x78]
 9f5:   e8 00 00 00 00          call   9fa <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x15a>       9f6: R_X86_64_PLT32     std::shared_ptr<spdlog::logger>::~shared_ptr()-0x4
        break;
 9fa:   e9 18 00 00 00          jmp    a17 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x177>
        nhlog::qml();
 9ff:   48 8d bd 78 ff ff ff    lea    rdi,[rbp-0x88]
 a06:   e8 00 00 00 00          call   a0b <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x16b>       a07: R_X86_64_PLT32     nhlog::qml()-0x4
 a0b:   48 8d bd 78 ff ff ff    lea    rdi,[rbp-0x88]
 a12:   e8 00 00 00 00          call   a17 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x177>       a13: R_X86_64_PLT32     std::shared_ptr<spdlog::logger>::~shared_ptr()-0x4
}
 a17:   c7 85 50 ff ff ff 00 00 00 00   mov    DWORD PTR [rbp-0xb0],0x0
 a21:   48 8d 7d d8             lea    rdi,[rbp-0x28]
 a25:   e8 00 00 00 00          call   a2a <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x18a>       a26: R_X86_64_PLT32     std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >::~basic_string()-0x4
 a2a:   64 48 8b 04 25 28 00 00 00      mov    rax,QWORD PTR fs:0x28
 a33:   48 8b 4d f8             mov    rcx,QWORD PTR [rbp-0x8]
 a37:   48 39 c8                cmp    rax,rcx
 a3a:   0f 85 15 00 00 00       jne    a55 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x1b5>
 a40:   48 81 c4 d0 00 00 00    add    rsp,0xd0
 a47:   5d                      pop    rbp
 a48:   c3                      ret
 a49:   48 8b bd 58 ff ff ff    mov    rdi,QWORD PTR [rbp-0xa8]
 a50:   e8 00 00 00 00          call   a55 <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x1b5>       a51: R_X86_64_PLT32     _Unwind_Resume-0x4
 a55:   e8 00 00 00 00          call   a5a <(anonymous namespace)::qmlMessageHandler(QtMsgType, QMessageLogContext const&, QString const&)+0x1ba>       a56: R_X86_64_PLT32     __stack_chk_fail-0x4
 a5a:   66 0f 1f 44 00 00       nop    WORD PTR [rax+rax*1+0x0]
 ```

</p>
</details>

Here is the [Preprocessed source file](https://github.com/llvm/llvm-project/files/10487282/Logging.cpp.txt).

Sorry this is a bit long. If you have any suggestions on how I could simplify this report, I will try that. We are now using this workaround: https://github.com/Nheko-Reborn/nheko/commit/4c34f4bfee284f0065f4b72c5a12649d664acf43 Original issue: https://github.com/Nheko-Reborn/nheko/issues/1292

There is a good chance I am triggering undefined behaviour, however GCC compiles it fine without warnings and I don't see any sanitizer warnings about it apart from the obvious crash from the bad code. I apologize if this is actually an issue with our code.

I tested this in Clang 15.0.7 and 14.0.6 from the Gentoo repos, haven't had a change to test 16 yet. This is with libstdc++, not libc++.


---

# 69
### compiler : `LLVM`
### title : comparison with short (< 16 chars) local `const std::string` is slower when it is `static`
### open_at : `2023-01-20T13:23:42Z`
### link : https://github.com/llvm/llvm-project/issues/60165
### status : `open`
### tags : `llvm:optimizations, `
### content : 
Split from #58002.

```cpp
#include <string>

#define LITERAL_S "012345678901234"
#define LITERAL_L "0123456789012345"

bool cmp3_s(const std::string& s)
{
    const std::string s_s(LITERAL_S);
    return s == s_s;
}

bool cmp4_s(const std::string& s)
{
    static const std::string s_s(LITERAL_S);
    return s == s_s;
}

bool cmp3_l(const std::string& s)
{
    const std::string s_s(LITERAL_L);
    return s == s_s;
}

bool cmp4_l(const std::string& s)
{
    static const std::string s_s(LITERAL_L);
    return s == s_s;
}
```
https://quick-bench.com/q/A3FPfNV6Cds2TwwBvSRwT6klxLg

This applies to all strings with less than 16 characters.

This does not happen with GCC where `static` is always faster no matter the length: 
https://quick-bench.com/q/hPor-y8JDwcMBEnT_oOv79nF43g
https://quick-bench.com/q/4Ef2dOfaBuhCd0QkKBRVVCXamjI`


---


# 70
### compiler : `LLVM`
### title : `Terminate handler generated for noexcept method using try/catch(...)`
### open_at : `2023-01-19T05:16:36Z`
### link : https://github.com/llvm/llvm-project/issues/60139
### status : `open`
### tags : `enhancement, llvm:optimizations, missed-optimization, `
### content : 
```c++
void mayThrow();

void bar() noexcept {
    try {
        mayThrow();
    } catch (...) {}
}
```

`bar()` 함수는 내부에서 예외가 발생할 수 있는 `mayThrow()` 함수를 호출합니다. 만약 예외가 발생하면, 그것을 잡아서 아무것도 하지 않고 넘어가려고 합니다. 그런데 Clang를 사용해서 이 코드를 컴파일하면, 예외가 발생했을 때 프로그램이 종료되는 부가적인 코드가 생성됩니다. 이것은 원치 않는 동작이며 불필요한 코드가 추가된 것입니다.

This code generates a call to `__clang_call_terminate` which seems like unnecessary code bloat (https://godbolt.org/z/eKbGq9xjP) 
The same code with GCC doesn't generate the call to terminate (https://godbolt.org/z/bT1vMa7a3)

According to cppreference, `catch(...)` should guarantee that no exception escapes the function so this `__clang_call_terminate` code section shouldn't be required.

https://en.cppreference.com/w/cpp/language/try_catch

> Catch-all block may be used to ensure that no uncaught exceptions can possibly escape from a function that offers nothrow exception guarantee.



---

# 71
### compiler : `LLVM`
### title : `[clang] Miscompiled atomic ordering at -O1 (clang-14 onwards)`
### open_at : `2023-01-18T22:15:49Z`
### link : https://github.com/llvm/llvm-project/issues/60131
### status : `closed`
### tags : `miscompilation, llvm:optimizations, `
### content : 
Hi LLVM,

please have a look at the following code:

``` cpp
#include <utility>
#include <atomic>
#include <cstdint>

std::pair<std::size_t *, std::size_t> load(
    std::atomic<std::int64_t>& m_beginChange,
    std::atomic<std::int64_t>& m_endChange,
    const std::pair<std::size_t*, std::size_t>& p)
{
    while (true)
    {
        std::int64_t changeNumber = m_endChange.load(std::memory_order_seq_cst);

        std::size_t *array = p.first;
        std::size_t length = p.second;

        if (changeNumber == m_beginChange.load(std::memory_order_seq_cst))
        {
            return { array, length };
        }
    }
}
```

At -O2 clang-13 and onwards generate the following code:

``` asm
        mov     r8, qword ptr [rsi]
        mov     rax, qword ptr [rdx]
        mov     r9, qword ptr [rdx + 8]
        mov     rcx, qword ptr [rdi]
        cmp     r8, rcx
        jne     .LBB0_1
        mov     rdx, r9
        ret
```

This looks correct to me in regards to ordering.

At -01 clang-13 generates the same code.

Starting with clang-14 we get the following code generation at -O1:

``` asm
        mov     r8, qword ptr [rsi]
        mov     rcx, qword ptr [rdi]
        cmp     r8, rcx
        cmove   rax, qword ptr [rdx]
        cmove   r9, qword ptr [rdx + 8]
        jne     .LBB0_1
        mov     rdx, r9
        ret
```

This looks wrong to me. The loads from the pair have now been reordered to after the comparison. If I am not mistaken that is against sequential consistent ordering rules which prevent any reordering across atomic operations (read,write,modify).

Indeed, at -O2 clang-14 and later do again generate the what I believe is the correct code as shown in the first snippet without the conditional moves.

Can you confirm whether this is a bug or indeed allowed by the standard?

Please see here for a godbolt link: https://gcc.godbolt.org/z/1MW6e6dh6

This originally came up in an Aeron issue. See https://github.com/real-logic/aeron/issues/1411 for more details but above should be the minimal example.

Thanks,
Stephan 

---

# 72
### compiler : `LLVM`
### title : `Wrongful cleanup for `trivial_abi` parameter after passing it to callee`
### open_at : `2023-01-17T22:11:49Z`
### link : https://github.com/llvm/llvm-project/issues/60112
### status : `open`
### tags : `clang:codegen, miscompilation, `
### content : 
Invoking `caller` in the following code leads to double destruction:

```c++
struct __attribute__((trivial_abi)) trivial {
  trivial() = default;
  trivial(const trivial &) noexcept;
  ~trivial();
  int* p = nullptr;
};

struct other {
  other() = default;
  other(const other&) noexcept;
  ~other();
};

void callee(trivial f, other) { throw 0; }

bool b = true;

void caller() {
  trivial f;
  other n;
  b ? callee(f, n) : void();
}
```

Since `trivial` has a `trivial_abi` attribute, it must generally be cleaned up by the callee (except if initialization of another parameter fails, which cannot happen here due to the `noexcept` on the `other` copy constructor). But the code around the call looks like this:

```llvm
define dso_local void @_Z6callerv() #0 personality ptr @__gxx_personality_v0 {
entry:
  ; ... setting up locals
  store i1 false, ptr %cleanup.cond, align 1
  store i1 false, ptr %cleanup.cond2, align 1
  br i1 %tobool, label %cond.true, label %cond.false

cond.true:                                        ; preds = %entry
  call void @_ZN7trivialC1ERKS_(ptr noundef nonnull align 8 dereferenceable(8) %agg.tmp, ptr noundef nonnull align 8 dereferenceable(8) %f) #3
  store i1 true, ptr %cleanup.cond, align 1
  call void @_ZN5otherC1ERKS_(ptr noundef nonnull align 1 dereferenceable(1) %agg.tmp1, ptr noundef nonnull align 1 dereferenceable(1) %n) #3
  store i1 true, ptr %cleanup.cond2, align 1
  %coerce.dive = getelementptr inbounds %struct.trivial, ptr %agg.tmp, i32 0, i32 0
  %1 = load ptr, ptr %coerce.dive, align 8
  invoke void @_Z6callee7trivial5other(ptr %1, ptr noundef %agg.tmp1)
          to label %invoke.cont unwind label %lpad

lpad:                                             ; preds = %cond.true
  %2 = landingpad { ptr, i32 }
          cleanup
  ; ... exception logistics
  %cleanup.is_active3 = load i1, ptr %cleanup.cond2, align 1       ; = true
  br i1 %cleanup.is_active3, label %cleanup.action4, label %cleanup.done5

cleanup.action4:                                  ; preds = %lpad
  call void @_ZN5otherD1Ev(ptr noundef nonnull align 1 dereferenceable(1) %agg.tmp1) #3
  br label %cleanup.done5

cleanup.done5:                                    ; preds = %cleanup.action4, %lpad
  %cleanup.is_active6 = load i1, ptr %cleanup.cond, align 1        ; = true
  br i1 %cleanup.is_active6, label %cleanup.action7, label %cleanup.done8

cleanup.action7:                                  ; preds = %cleanup.done5
  call void @_ZN7trivialD1Ev(ptr noundef nonnull align 8 dereferenceable(8) %agg.tmp) #3
  br label %cleanup.done8

cleanup.done8:                                    ; preds = %cleanup.action7, %cleanup.done5
  call void @_ZN5otherD1Ev(ptr noundef nonnull align 1 dereferenceable(1) %n) #3
  call void @_ZN7trivialD1Ev(ptr noundef nonnull align 8 dereferenceable(8) %f) #3
  br label %eh.resume

eh.resume:                                        ; preds = %cleanup.done8
  ; ... exception logistics
  resume { ptr, i32 } %lpad.val9
}
```
So if `caller` throws, we destruct both parameters (and both locals). But we don't own the first parameter anymore after the call. Inspecting `callee` shows that it calls `_ZN7trivialD1Ev` on unwinding the exception that it has thrown. So we destruct the first parameter twice.

If we drop the ternary and unconditionally call `callee`, all is fine. We get:
```llvm
define dso_local void @_Z6callerv() #0 personality ptr @__gxx_personality_v0 {
entry:
  ; ... setting up locals
  call void @_ZN7trivialC1ERKS_(ptr noundef nonnull align 8 dereferenceable(8) %agg.tmp, ptr noundef nonnull align 8 dereferenceable(8) %f) #3
  call void @_ZN5otherC1ERKS_(ptr noundef nonnull align 1 dereferenceable(1) %agg.tmp1, ptr noundef nonnull align 1 dereferenceable(1) %n) #3
  %coerce.dive = getelementptr inbounds %struct.trivial, ptr %agg.tmp, i32 0, i32 0
  %0 = load ptr, ptr %coerce.dive, align 8
  invoke void @_Z6callee7trivial5other(ptr %0, ptr noundef %agg.tmp1)
          to label %invoke.cont unwind label %lpad

lpad:                                             ; preds = %entry
  %1 = landingpad { ptr, i32 }
          cleanup
  ; ... exception logistics
  call void @_ZN5otherD1Ev(ptr noundef nonnull align 1 dereferenceable(1) %agg.tmp1) #3
  call void @_ZN5otherD1Ev(ptr noundef nonnull align 1 dereferenceable(1) %n) #3
  call void @_ZN7trivialD1Ev(ptr noundef nonnull align 8 dereferenceable(8) %f) #3
  br label %eh.resume

eh.resume:                                        ; preds = %lpad
  ; ... exception logistics
  resume { ptr, i32 } %lpad.val2
}
```

It gets more interesting if we drop `noexcept` from `other`'s copy constructor:
```llvm
define dso_local void @_Z6callerv() #0 personality ptr @__gxx_personality_v0 {
entry:
  ; ... setting up locals
  store i1 false, ptr %cleanup.cond, align 1
  store i1 false, ptr %cleanup.cond2, align 1
  br i1 %tobool, label %cond.true, label %cond.false

cond.true:                                        ; preds = %entry
  call void @_ZN7trivialC1ERKS_(ptr noundef nonnull align 8 dereferenceable(8) %agg.tmp, ptr noundef nonnull align 8 dereferenceable(8) %f) #4
  store i1 true, ptr %cleanup.cond, align 1
  invoke void @_ZN5otherC1ERKS_(ptr noundef nonnull align 1 dereferenceable(1) %agg.tmp1, ptr noundef nonnull align 1 dereferenceable(1) %n)
          to label %invoke.cont unwind label %lpad

invoke.cont:                                      ; preds = %cond.true
  store i1 true, ptr %cleanup.cond2, align 1
  %coerce.dive = getelementptr inbounds %struct.trivial, ptr %agg.tmp, i32 0, i32 0
  %1 = load ptr, ptr %coerce.dive, align 8
  store i1 false, ptr %cleanup.cond, align 1                         ; !!!
  invoke void @_Z6callee7trivial5other(ptr %1, ptr noundef %agg.tmp1)
          to label %invoke.cont4 unwind label %lpad3

lpad:                                             ; preds = %cond.true
  %2 = landingpad { ptr, i32 }
          cleanup
  ; ... exception logistics
  br label %ehcleanup

lpad3:                                            ; preds = %invoke.cont
  %5 = landingpad { ptr, i32 }
          cleanup
  ; ... exception logistics
  %cleanup.is_active5 = load i1, ptr %cleanup.cond2, align 1      ; = true
  br i1 %cleanup.is_active5, label %cleanup.action6, label %cleanup.done7

cleanup.action6:                                  ; preds = %lpad3
  call void @_ZN5otherD1Ev(ptr noundef nonnull align 1 dereferenceable(1) %agg.tmp1) #4
  br label %cleanup.done7

cleanup.done7:                                    ; preds = %cleanup.action6, %lpad3
  br label %ehcleanup

ehcleanup:                                        ; preds = %cleanup.done7, %lpad
  %cleanup.is_active8 = load i1, ptr %cleanup.cond, align 1       ; = phi i1 [ false, %cleanup.done7 ], [ true, %lpad ]
  br i1 %cleanup.is_active8, label %cleanup.action9, label %cleanup.done10

cleanup.action9:                                  ; preds = %ehcleanup
  call void @_ZN7trivialD1Ev(ptr noundef nonnull align 8 dereferenceable(8) %agg.tmp) #4
  br label %cleanup.done10

cleanup.done10:                                   ; preds = %cleanup.action9, %ehcleanup
  call void @_ZN5otherD1Ev(ptr noundef nonnull align 1 dereferenceable(1) %n) #4
  call void @_ZN7trivialD1Ev(ptr noundef nonnull align 8 dereferenceable(8) %f) #4
  br label %eh.resume

eh.resume:                                        ; preds = %cleanup.done10
  ; ... exception logistics
  resume { ptr, i32 } %lpad.val13
}
```
So after having initialized the second parameter, and before handing ownership of the `trivial_abi` object into the callee, we write `false` into `cleanup.cond`. So we only clean up if initializing the second parameter failed and we couldn't pass on the object.`


---

# 73
### compiler : `LLVM`
### title : `Constant propagation makes a register value forgotten`
### open_at : `2023-01-17T15:08:37Z`
### link : https://github.com/llvm/llvm-project/issues/60103
### status : `open`
### tags : `llvm:optimizations, missed-optimization, `
### content : 
```cpp
template <unsigned X>
int go(int) noexcept;

int sw(int arg)
{
    switch (arg)
    {
        case 0: return go<0>(arg);
        case 1: return go<1>(arg);
        case 2: return go<2>(arg);
        case 3: return go<3>(arg);
        case 4: return go<4>(arg);
    }

    return 0;
}
```

In this example `arg` argument is forwarded to `go` calls. Although the value is already in the right register the register is re-assigned because on the IR level the usage is converted to constant.

```asm
.LBB0_3:
        mov     edi, 1
        jmp     int go<1u>(int)                   # TAILCALL
```

https://godbolt.org/z/cczTP5v1q


---

# 74
### compiler : `LLVM`
### title : `Thrown exception in `nothrow` function not detected`
### open_at : `2023-01-16T21:17:21Z`
### link : https://github.com/llvm/llvm-project/issues/60086
### status : `open`
### tags : `c++, clang:diagnostics, `
### content : 
If an exception is thrown in a function marked with `nothrow` clang usually reports a warning.

In the following example however an exception is thrown but clang fails to detect it and the 
warning is not reported at all.

```c++
void foo() noexcept {
  try {
    double *a[2][3];
    throw a;
  } catch (const double *const(*)[3]) {
  }
}
```

What makes this more interesting is that on [cppreference](https://en.cppreference.com/w/cpp/language/try_catch) the following can be seen:
```
When an exception is thrown by any statement in compound-statement, the exception object of type E is 
matched against the types of the formal parameters T of each catch-clause in handler-seq, in the order in 
which the catch clauses are listed. The exception is a match if any of the following is true:

...
- T is (possibly cv-qualified) U or const U& (since C++14), and U is a pointer or pointer to member type, and
  E is also a pointer or pointer to member type that is implicitly convertible to U by one or more of
  - a standard pointer conversion other than one to a private, protected, or ambiguous base class
  - **a qualification conversion**
  - a function pointer conversion (since C++17)
...
```
While the [qualification conversion section](https://en.cppreference.com/w/cpp/language/implicit_conversion#Qualification_conversions) lists a number of rules that describe when can 
the said conversion be performed, it gives the following example:
```c++
double *a[2][3];
double const * const (*ap)[3] = a; // OK
```
So technically the thrown type in `foo()` can be converted to the type in the handler, which
is the reason for clang not reporting a warning but the exception is thrown regardless. 

See the example on [godbolt](https://godbolt.org/z/sEz8eYeP1). Note that MSVC is able to detect the thrown exception.`


---

# 75
### compiler : `LLVM`
### title : `[Clang]: Incorrect inheritance of protected (default) constructor`
### open_at : `2023-01-13T10:11:59Z`
### link : https://github.com/llvm/llvm-project/issues/59996
### status : `open`
### tags : `c++17, clang:frontend, confirmed, `
### content : 
The snippet
```cpp
#include <iostream>
#include <type_traits>

class Foo {
protected:
   Foo() = default; 
};

class Bar : public Foo {
public:
    using Foo::Foo;

    Bar(const Bar &) = default;
};

int main() {
    std::cout << std::boolalpha << "Is default constructible: "
        << std::is_default_constructible_v< Bar > << std::endl;
    
    Bar b;
}
```
compiles fines with Clang (trunk and older), whereas it fails to compile with GCC and MSVC because `Bar` has no public default constructor.

If the line `Bar b;` is commented out, the program compiled with Clang will report `true` whereas GCC and MSVC report `false`. I suspect that Clang's behavior here is related to the abovementioned problem.

Note: If the visibility of `Bar`'s constructor is changed to `private`, then everything works as expected.

[Godbolt](https://godbolt.org/z/ex3eWoh5z)

I am not nearly competent enough to look up the expected behavior in the C++ standard, but given that GCC  and MSVC seem to agree on what the result should be, I figured that this is likely a bug in Clang :shrug: 


---

# 76
### compiler : `LLVM`
### title : wrong type for `auto&` parameter when deducing a class template partial specialization
### open_at : `2023-01-13T01:14:19Z`
### link : https://github.com/llvm/llvm-project/issues/59981
### status : `open`
### tags : `c++17, clang:frontend, rejects-valid, `
### content : 
Clang rejects this valid code:

```c++
template<auto &X, int> struct A;
template<auto &X> struct A<X, 0> {};

const int n = 0;
A<n, 0> a;
```

... apparently because it thinks that the expression `X` in `struct A<X, 0>` is an lvalue of type `int`, not an lvalue of type `const int`, when considering partial specializations of `A<n, 0>`.`


---


# 77
### compiler : `LLVM`
### title : `Clang and GCC differ in instantiation strategy of constexpr and incomplete types`
### open_at : `2023-01-12T13:46:01Z`
### link : https://github.com/llvm/llvm-project/issues/59966
### status : `open`
### tags : `c++20, clang:frontend, `
### content : 
Consider this code compiled in C++20 mode:
```cpp
#include <vector>

struct X{
    struct Inner;
    unsigned size() { return children.size(); }
    std::vector<Inner> children;
};

struct X::Inner {
    int a;
};
```
MSVC and GCC will succeed, but Clang (trunk, WIP version 16 at the time of writing) [produces an error](https://gcc.godbolt.org/z/jY4coE9aq):
```console
/lib/gcc/x86_64-linux-gnu/13.0.0/../../../../include/c++/13.0.0/bits/stl_vector.h:988:50: error: arithmetic on a pointer to an incomplete type 'X::Inner'
      { return size_type(this->_M_impl._M_finish - this->_M_impl._M_start); }
```

This boils down to different approaches when instantiating `constexpr` functions:
```cpp
template <class T>
struct vector {
    T* ptr;
    constexpr unsigned size() { return ptr - ptr; }
};

struct X{
    struct Inner;
    unsigned size() { return children.size(); }
    vector<Inner> children;
};

struct X::Inner {
    int a;
};
```
Clang instantiates the bodies of `constexpr` functions eagerly, other compilers seem to [delay](https://gcc.godbolt.org/z/fxxovcP68) the instantiation until the end of the TU, e.g. this code [fails](https://gcc.godbolt.org/z/cfTbdGhbd) in all compilers:
```cpp
template <class T>
struct vector {
    T* ptr;
    constexpr unsigned size() { return ptr - ptr; }
};

struct X{
    struct Inner;
    static constexpr int a = vector<Inner>().size();
    vector<Inner> children;
};

struct X::Inner {
    int a;
};
```

We have observed that this pattern is used in much of the existing code and I believe Clang should follow the GCC's and MSVC's approach here, even though it is not mandated by the standard:
- it avoids breaking code that worked in C++17 when migrating to C++20.
- it allows to compile future C++20 code written for GCC and MSVC with Clang with no changes.`


---


# 78
### compiler : `LLVM`
### title : `[LoopReroll] with multiple roots incorrectly reorders instructions with side effects`
### open_at : `2023-01-05T13:19:42Z`
### link : https://github.com/llvm/llvm-project/issues/59841
### status : `open`
### tags : `miscompilation, loopoptim, `
### content : 

이버그 재현이 안됨

https://godbolt.org/z/11E3zcsbz

The test below doesn't use contiguous IV increments, so it can't be rerolled that easily. Source iteration uses iv, iv+1, +2, +4, +5, +4 (skips + 3).
Plus the IV multiplication by 3 isn't taken into account.

Alive2 output:
```llvm
; Transforms/LoopReroll/extra_instr.ll
define void @rerollable2() {
%entry:
  br label %loop

%loop:
  %iv = phi i32 [ 0, %entry ], [ %iv.next, %loop ]
  %iv.mul3 = mul nsw nuw i32 %iv, 3
  %iv.scaled = add nsw nuw i32 %iv.mul3, 20
  %iv.scaled.div5 = udiv i32 %iv.scaled, 5
  call void @bar(i32 %iv.scaled.div5)
  %iv.scaled.add1 = add nsw nuw i32 %iv.scaled, 1
  %iv.scaled.add1.div5 = udiv i32 %iv.scaled.add1, 5
  call void @bar(i32 %iv.scaled.add1.div5)
  %iv.scaled.add2 = add nsw nuw i32 %iv.scaled, 2
  %iv.scaled.add2.div5 = udiv i32 %iv.scaled.add2, 5
  call void @bar(i32 %iv.scaled.add2.div5)
  %iv.scaled.add4 = add nsw nuw i32 %iv.scaled, 4
  %iv.scaled.add4.div5 = udiv i32 %iv.scaled.add4, 5
  call void @bar(i32 %iv.scaled.add4.div5)
  %iv.scaled.add5 = add nsw nuw i32 %iv.scaled, 5
  %iv.scaled.add5.div5 = udiv i32 %iv.scaled.add5, 5
  call void @bar(i32 %iv.scaled.add5.div5)
  %iv.scaled.add6 = add nsw nuw i32 %iv.scaled, 6
  %iv.scaled.add6.div5 = udiv i32 %iv.scaled.add6, 5
  call void @bar(i32 %iv.scaled.add6.div5)
  %iv.next = add nsw nuw i32 %iv, 1
  %cmp = icmp ult i32 %iv.next, 3
  br i1 %cmp, label #sink, label %exit

%exit:
  ret void
}
=>
define void @rerollable2() {
%entry:
  br label %loop

%loop:
  %iv = phi i32 [ 0, %entry ], [ %iv.next, %loop ]
  %0 = add i32 %iv, 24
  %1 = add i32 %iv, 20
  %iv.scaled.div5 = udiv i32 %1, 5
  call void @bar(i32 %iv.scaled.div5)
  %iv.scaled.add4.div5 = udiv i32 %0, 5
  call void @bar(i32 %iv.scaled.add4.div5)
  %iv.next = add nsw nuw i32 %iv, 1
  %exitcond = icmp eq i32 %iv, 8
  br i1 %exitcond, label %exit, label %loop#2

%loop#2:
  %iv#2 = phi i32 [ %iv.next, %loop ]
  %0#2 = add i32 %iv#2, 24
  %1#2 = add i32 %iv#2, 20
  %iv.scaled.div5#2 = udiv i32 %1#2, 5
  call void @bar(i32 %iv.scaled.div5#2)
  %iv.scaled.add4.div5#2 = udiv i32 %0#2, 5
  call void @bar(i32 %iv.scaled.add4.div5#2)
  %iv.next#2 = add nsw nuw i32 %iv#2, 1
  %exitcond#2 = icmp eq i32 %iv#2, 8
  br i1 %exitcond#2, label %exit, label #sink

%exit:
  ret void
}
Transformation doesn't verify! (unsound)
ERROR: Source is more defined than target

Example:

Source:
  >> Jump to %loop
i32 %iv = #x00000000 (0)
i32 %iv.mul3 = #x00000000 (0)
i32 %iv.scaled = #x00000014 (20)
i32 %iv.scaled.div5 = #x00000004 (4)
Function @bar returned
i32 %iv.scaled.add1 = #x00000015 (21)
i32 %iv.scaled.add1.div5 = #x00000004 (4)
Function @bar returned
i32 %iv.scaled.add2 = #x00000016 (22)
i32 %iv.scaled.add2.div5 = #x00000004 (4)
Function @bar returned
i32 %iv.scaled.add4 = #x00000018 (24)
i32 %iv.scaled.add4.div5 = #x00000004 (4)
Function @bar returned
i32 %iv.scaled.add5 = #x00000019 (25)
i32 %iv.scaled.add5.div5 = #x00000005 (5)
Function @bar returned
i32 %iv.scaled.add6 = #x0000001a (26)
i32 %iv.scaled.add6.div5 = #x00000005 (5)
...


Target:
  >> Jump to %loop
i32 %iv = #x00000000 (0)
i32 %0 = #x00000018 (24)
i32 %1 = #x00000014 (20)
i32 %iv.scaled.div5 = #x00000004 (4)
Function @bar returned
i32 %iv.scaled.add4.div5 = #x00000004 (4)
Function @bar returned
i32 %iv.next = #x00000001 (1)
i1 %exitcond = #x0 (0)
  >> Jump to %loop#2
i32 %iv#2 = #x00000001 (1)
i32 %0#2 = #x00000019 (25)
i32 %1#2 = #x00000015 (21)
i32 %iv.scaled.div5#2 = #x00000004 (4)
Function @bar returned
i32 %iv.scaled.add4.div5#2 = #x00000005 (5)
Function @bar triggered UB
i32 %iv.next#2 = UB triggered!
```


---

# 79
### compiler : `LLVM`
### title : `A miscompile in instcombine, opt pass.`
### open_at : `2023-01-05T04:52:33Z`
### link : https://github.com/llvm/llvm-project/issues/59836
### status : `closed`
### tags : `miscompilation, llvm:instcombine, `
### content : 
Test case:
https://llvm.godbolt.org/z/6W61azGsn
```llvm
define i1 @pr4917_4(i32 %x) {
entry:
  %r = zext i32 %x to i64
  %0 = trunc i64 %r to i34
  %new0 = mul i34 %0, %0
  ;3363831808 * 3363831808 % 2^34 == 0, thus new0 is 0
  %last = zext i34 %new0 to i64
  %overflow = icmp ule i64 %last, 4294967295 ;FFFFFFFF
  ret i1 %overflow
}
```
This test case is a mutated version of https://github.com/llvm/llvm-project/blob/main/llvm/test/Transforms/InstCombine/overflow-mul.ll#L77

Conisder input `x=3363831808`, the original function returns 1 baceuse `3363831808^2 % 2^34 ==0`. However, the optmized function returns 0.
https://alive2.llvm.org/ce/z/5nNo_z
The ouput is verified by `lli` with following test driver:
```cpp
#include <iostream>

bool f(unsigned int x);

int main(){
  unsigned int a=3363831808;
  std::cout<<f(a)<<"\n";
}
```
So the miscompile does exist.
@regehr @nunoplopes 


---


# 80
### compiler : `LLVM`
### title : `clang 15 built kernel crashes w. "BUG: kernel NULL pointer dereference, address: 00000000", gcc 12 built kernel with same config boots fine (6.1-rc7, x86_32)`
### open_at : `2022년 12월 1일`
### link : https://github.com/ClangBuiltLinux/linux/issues/1766
### status : `closed`
### tags : `[ARCH] x86, [BUG] llvm, [FIXED][LLVM] 15, [FIXED][LLVM] 16`
### content :

https://godbolt.org/z/oWjEs7do3

This is an interesting one!

Gave 6.1-rc7 a test ride on ye goode olde Pentium 4 box and noticed while the kernel boots just fine when built with gcc 12 toolchain it crashes at boot when it is built with clang 15 toolchain, same kernel .config used.

This is reproducable and happens everytime at boot on this machine;
```bash
[...]
BUG: kernel NULL pointer dereference, address: 00000000
#PF: supervisor write access in kernel mode
#PF: error_code(0x0002) - not-present page
*pde = 00000000 
Oops: 0002 [#1] SMP DEBUG_PAGEALLOC
CPU: 1 PID: 1 Comm: init Not tainted 6.1.0-rc7-P4 #3
Hardware name:  /FS51, BIOS 6.00 PG 12/02/2003
EIP: mast_split_data+0x198/0x260
Code: 84 e3 00 00 00 89 fa c7 45 ec 00 00 00 00 31 db 81 e2 00 ff ff ff 0f b6 f9 8b 4d ec 25 00 ff ff ff 8a 6d f3 09 da d3 e7 09 d7 <89> 38 8b 7e 10 8b 46 08 8b 50 0c 8b 7f 0c fe c5 8b 46 04 8b 70 0c
EAX: 00000000 EBX: 00000006 ECX: 00000003 EDX: c123bd06
ESI: c11ffbf0 EDI: c123bd06 EBP: c11ff94c ESP: c11ff934
DS: 007b ES: 007b FS: 00d8 GS: 0000 SS: 0068 EFLAGS: 00010286
CR0: 80050033 CR2: 00000000 CR3: 0276a000 CR4: 000006d0
Call Trace:
 mas_wr_modify+0xc76/0x18c0
 mas_wr_store_entry+0x235/0x2b0
 mas_store_prealloc+0xb8/0x100
 vma_mas_store+0x57/0xd0
 __vma_adjust+0x3f0/0x5b0
 ? rcu_read_lock_sched_held+0xa/0x70
 __split_vma+0xc3/0x120
 do_mas_align_munmap+0x1c8/0x460
 mmap_region+0x260/0x8a0
 ? rcu_read_lock_sched_held+0xa/0x70
 ? arch_get_unmapped_area_topdown+0x12/0x20
 do_mmap+0x33d/0x4b0
 ? prep_transhuge_page+0x20/0x20
 vm_mmap_pgoff+0x7f/0x100
 ksys_mmap_pgoff+0x129/0x170
 __ia32_sys_mmap_pgoff+0x1c/0x30
 do_int80_syscall_32+0x53/0x80
 entry_INT80_32+0xf0/0xf0
EIP: 0xb7f19fad
Code: 00 f7 d8 89 82 38 0a 00 00 b8 ff ff ff ff c3 66 90 66 90 66 90 66 90 66 90 66 90 66 90 53 57 55 8b 1f 8b 6f 08 8b 7f 04 cd 80 <5d> 5f 5b c3 e8 cf 01 00 00 81 c1 16 e0 00 00 8b 44 24 04 3d 85 00
EAX: ffffffda EBX: b787a000 ECX: 00004000 EDX: 00000005
ESI: 00000812 EDI: 00000003 EBP: 00000002 ESP: bfb43eb0
DS: 007b ES: 007b FS: 0000 GS: 0000 SS: 007b EFLAGS: 00000202
Modules linked in:
CR2: 0000000000000000
---[ end trace 0000000000000000 ]---
EIP: mast_split_data+0x198/0x260
Code: 84 e3 00 00 00 89 fa c7 45 ec 00 00 00 00 31 db 81 e2 00 ff ff ff 0f b6 f9 8b 4d ec 25 00 ff ff ff 8a 6d f3 09 da d3 e7 09 d7 <89> 38 8b 7e 10 8b 46 08 8b 50 0c 8b 7f 0c fe c5 8b 46 04 8b 70 0c
EAX: 00000000 EBX: 00000006 ECX: 00000003 EDX: c123bd06
ESI: c11ffbf0 EDI: c123bd06 EBP: c11ff94c ESP: c11ff934
DS: 007b ES: 007b FS: 00d8 GS: 0000 SS: 0068 EFLAGS: 00010286
CR0: 80050033 CR2: 00000000 CR3: 0276a000 CR4: 000006d0
Kernel panic - not syncing: Attempted to kill init! exitcode=0x00000009
Kernel Offset: disabled
Rebooting in 40 seconds..
Some data about the machine:

 # inxi -bZ
System:
  Kernel: 6.1.0-rc7-P4 arch: i686 bits: 32 Console: pty pts/0
    Distro: Gentoo Base System release 2.9
Machine:
  Type: Desktop Mobo: Shuttle model: FS51 serial: N/A BIOS: Phoenix
    v: 6.00 PG date: 12/02/2003
CPU:
  Info: single core Intel Pentium 4 [MT] speed (MHz): avg: 3063
Graphics:
  Device-1: AMD RV350 [Radeon 9550/9600/X1050 Series] driver: radeon
    v: kernel
  Display: x11 server: X.Org v: 21.1.1 driver: X: loaded: radeon
    unloaded: fbdev,modesetting gpu: radeon resolution: 1400x900~60Hz
  OpenGL: renderer: llvmpipe (LLVM 14.0.6 128 bits) v: 4.5 Mesa 22.1.7
Network:
  Device-1: Ralink RT2500 Wireless 802.11bg driver: rt2500pci
  Device-2: Realtek RTL-8100/8101L/8139 PCI Fast Ethernet Adapter
    driver: 8139too
If you think it would be a good idea I could mail a bug report to linux-mm too.
dmesg_61-rc7_p4_clang.txt
dmesg_61-rc7_p4_gcc.txt
config_61-rc7_p4-clang.txt
config_61-rc7_p4-gcc.txt
```

---

# 81
### compiler : `LLVM`
### title : clang-15: May produce invalid code when -O1 (or higher) is used with `-fzero-call-used-regs=all`
### open_at : `2022년 9월 12일`
### link : https://github.com/llvm/llvm-project/issues/57692
### status : `closed`
### tags : `llvm:codegen, miscompilation, release:backport, release:merged`
### content :

https://github.com/llvm/llvm-project/issues/59242

This report is copied from https://bugs.gentoo.org/869839

Description:
When building binaries using `-O1` (or higher) and the `-fzero-call-used-regs=all` the resultant object files may create a broken binary when linked to.

Reproducible:
Always

Steps to Reproduce:
Create a file named `get_progname.c`
Paste the following into `get_progname.c`:
```c
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

char *ssh_get_progname(char *argv0)
{
  char *p, *q;
  extern char *__progname;

  p = __progname;
  if ((q = strdup(p)) == NULL) {
      perror("strdup");
      exit(1);
  }
  return q;
}
```
Execute `clang -O1 -ggdb -fzero-call-used-regs=all -c get_progname.c`
Create a file named `test.c`
Paste the following into `test.c`:
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <syslog.h>

extern char *__progname;

char *ssh_get_progname(char *);

int main(int argc, char **argv)
{
  __progname = ssh_get_progname(argv[0]);
  openlog(argv[0], 1, LOG_USER);
  return 0;
}
```

Execute `clang -O1 -ggdb -fzero-call-used-regs=all -c test.c`
Execute `clang -o test test.o get_progname.o`
run `./test`

### Actual Results:
`./test` segfaults due to `argv[0]` being incorrectly set to NULL during execution

### Expected Results:
`./test` should run and exit successfully.

<details><summary>Additional Info</summary>
<p>

```
Portage 3.0.35 (python 3.10.7-final-0, default/linux/amd64/17.1/desktop, gcc-12.2.0, glibc-2.35-r8, 5.18.14-gentoo x86_64)
=================================================================
System uname: [Linux-5.18.14-gentoo-x86_64-Intel-R-_Core-TM-_i7-4771_CPU_@_3.50GHz-with-glibc2.35](mailto:Linux-5.18.14-gentoo-x86_64-Intel-R-_Core-TM-_i7-4771_CPU_@_3.50GHz-with-glibc2.35)
KiB Mem:    32557860 total,   7752032 free
KiB Swap:    2097148 total,   2045904 free
Timestamp of repository gentoo: Mon, 12 Sep 2022 06:57:44 +0000
Head commit of repository gentoo: 3661d51653661eea567088e6e80385d8a14432c4

Timestamp of repository brother-overlay: Sun, 04 Sep 2022 19:46:50 +0000
Head commit of repository brother-overlay: 2c208f0df5aa5f9f967c361f0e3ad514e50422d0

Head commit of repository magpie: 10f020019b514442260050d216608c67910099cb

sh bash 5.1_p16-r2
ld GNU ld (Gentoo 2.39 p4) 2.39.0
app-misc/pax-utils:        1.3.5::gentoo
app-shells/bash:           5.1_p16-r2::gentoo
dev-java/java-config:      2.3.1::gentoo
dev-lang/perl:             5.36.0::gentoo
dev-lang/python:           3.10.7::gentoo, 3.11.0_rc1_p2::gentoo
dev-lang/rust:             1.63.0::magpie
dev-util/cmake:            3.24.1::gentoo
dev-util/meson:            0.63.2::gentoo
sys-apps/baselayout:       2.8-r2::gentoo
sys-apps/openrc:           0.45.2::gentoo
sys-apps/sandbox:          2.29::gentoo
sys-devel/autoconf:        2.13-r2::gentoo, 2.71-r2::gentoo
sys-devel/automake:        1.16.5::gentoo
sys-devel/binutils:        2.39-r2::gentoo
sys-devel/binutils-config: 5.4.1::gentoo
sys-devel/clang:           14.0.6-r1::gentoo, 15.0.0::gentoo
sys-devel/gcc:             12.2.0::gentoo
sys-devel/gcc-config:      2.5-r1::gentoo
sys-devel/libtool:         2.4.7::gentoo
sys-devel/lld:             15.0.0::gentoo
sys-devel/llvm:            14.0.6-r2::gentoo, 15.0.0::gentoo
sys-devel/make:            4.3::gentoo
sys-kernel/linux-headers:  5.19::gentoo (virtual/os-headers)
sys-libs/glibc:            2.35-r8::gentoo
Repositories:

gentoo
    location: /var/db/repos/gentoo
    sync-type: git
    sync-uri: https://github.com/gentoo-mirror/gentoo.git
    priority: -1000
    sync-git-verify-commit-signature: true

brother-overlay
    location: /var/db/repos/brother-overlay
    sync-type: git
    sync-uri: https://github.com/gentoo-mirror/brother-overlay.git
    masters: gentoo

magpie
    location: /var/db/repos/magpie
    sync-type: git
    sync-uri: https://github.com/nvinson/magpie.git
    masters: gentoo

ACCEPT_KEYWORDS="amd64 ~amd64"
ACCEPT_LICENSE="* -@EULA"
AR="llvm-ar"
CBUILD="x86_64-pc-linux-gnu"
CC="clang"
CFLAGS="-march=native -O2 -pipe -D_FORTIFY_SOURCE=3 -fstack-protector-strong -flto=thin"
CHOST="x86_64-pc-linux-gnu"
CONFIG_PROTECT="/etc /opt/brother/scanner/brscan4/brsanenetdevice4.cfg /usr/lib64/libreoffice/program/sofficerc /usr/share/gnupg/qualified.txt"
CONFIG_PROTECT_MASK="/etc/ca-certificates.conf /etc/dconf /etc/env.d /etc/fonts/fonts.conf /etc/gconf /etc/gentoo-release /etc/revdep-rebuild /etc/sandbox.d /etc/terminfo
 /etc/texmf/language.dat.d /etc/texmf/language.def.d /etc/texmf/updmap.d /etc/texmf/web2c"
CXX="clang++"
CXXFLAGS="-march=native -O2 -pipe -D_FORTIFY_SOURCE=3 -fstack-protector-strong -flto=thin"
DISTDIR="/var/cache/portage/distfiles"
EMERGE_DEFAULT_OPTS="--quiet-build"
ENV_UNSET="CARGO_HOME DBUS_SESSION_BUS_ADDRESS DISPLAY GOBIN GOPATH PERL5LIB PERL5OPT PERLPREFIX PERL_CORE PERL_MB_OPT PERL_MM_OPT XAUTHORITY XDG_CACHE_HOME XDG_CONFIG_HO
ME XDG_DATA_HOME XDG_RUNTIME_DIR"
FCFLAGS="-march=native -O2 -pipe"
FEATURES="assume-digests binpkg-docompress binpkg-dostrip binpkg-logs binpkg-multi-instance buildpkg-live config-protect-if-modified distlocks ebuild-locks fixlafiles ipc
-sandbox merge-sync multilib-strict network-sandbox news parallel-fetch pid-sandbox preserve-libs protect-owned qa-unresolved-soname-deps sandbox sfperms strict unknown-f
eatures-warn unmerge-logs unmerge-orphans userfetch userpriv usersandbox usersync xattr"
FFLAGS="-march=native -O2 -pipe"
GENTOO_MIRRORS="http://distfiles.gentoo.org/"
LANG="en_US.utf8"
LDFLAGS="-Wl,-O1 -Wl,--as-needed -fuse-ld=lld -rtlib=compiler-rt -unwindlib=libunwind"
MAKEOPTS="-j8"
NM="llvm-nm"
PKGDIR="/var/cache/binpkgs"
PORTAGE_CONFIGROOT="/"
PORTAGE_RSYNC_OPTS="--recursive --links --safe-links --perms --times --omit-dir-times --compress --force --whole-file --delete --stats --human-readable --timeout=180 --ex
clude=/distfiles --exclude=/local --exclude=/packages --exclude=/.git"
PORTAGE_TMPDIR="/var/tmp"
RANLIB="llvm-ranlib"
SHELL="/bin/zsh"
USE="X a52 aac acl acpi alsa amd64 branding bzip2 cairo cdda cdr clang cleartype cli corefonts crypt cups dbus dri dts dvd dvdr elogind encode exif flac fortran gdbm gif 
glamor gpm gtk gui iconv icu ipv6 jpeg lcms libglvnd libnotify libtirpc mad mng mp3 mp4 mpeg multilib ncurses nls nptl ogg opengl openmp pam pango pcre pdf png policykit 
ppds qt5 readline sdl seccomp spell split-usr ssl startup-notification svg theora tiff truetype udev udisks unicode upower usb vaapi vorbis vpx wxwidgets x264 xattr xcb x
ml xv xvid zlib" ABI_X86="64" ADA_TARGET="gnat_2020" APACHE2_MODULES="authn_core authz_core socache_shmcb unixd actions alias auth_basic authn_alias authn_anon authn_dbm 
authn_default authn_file authz_dbm authz_default authz_groupfile authz_host authz_owner authz_user autoindex cache cgi cgid dav dav_fs dav_lock deflate dir disk_cache env
 expires ext_filter file_cache filter headers include info log_config logio mem_cache mime mime_magic negotiation rewrite setenvif speling status unique_id userdir usertr
ack vhost_alias" CALLIGRA_FEATURES="karbon sheets words" COLLECTD_PLUGINS="df interface irq load memory rrdtool swap syslog" CPU_FLAGS_X86="aes avx avx2 fma3 mmx mmxext p
opcnt sse sse2 sse3 sse4 sse4_1 sse4_2 ssse3" ELIBC="glibc" GPSD_PROTOCOLS="ashtech aivdm earthmate evermore fv18 garmin garmintxt gpsclock greis isync itrax mtk3301 nmea
 ntrip navcom oceanserver oldstyle oncore rtcm104v2 rtcm104v3 sirf skytraq superstar2 timing tsip tripmate tnt ublox ubx" INPUT_DEVICES="libinput" KERNEL="linux" L10N="en
-US en" LCD_DEVICES="bayrad cfontz cfontz633 glk hd44780 lb216 lcdm001 mtxorb ncurses text" LIBREOFFICE_EXTENSIONS="presenter-console presenter-minimizer" LUA_SINGLE_TARG
ET="lua5-1" LUA_TARGETS="lua5-1" OFFICE_IMPLEMENTATION="libreoffice" PHP_TARGETS="php7-4 php8-0" POSTGRES_TARGETS="postgres12 postgres13" PYTHON_SINGLE_TARGET="python3_10
" PYTHON_TARGETS="python3_10" RUBY_TARGETS="ruby27" USERLAND="GNU" VIDEO_CARDS="intel i965" XTABLES_ADDONS="quota2 psd pknock lscan length2 ipv4options ipset ipp2p iface 
geoip fuzzy condition tee tarpit sysrq proto steal rawnat logmark ipmark dhcpmac delude chaos account"
Unset:  ADDR2LINE, ARFLAGS, AS, ASFLAGS, CCLD, CONFIG_SHELL, CPP, CPPFLAGS, CTARGET, CXXFILT, ELFEDIT, EXTRA_ECONF, F77FLAGS, FC, GCOV, GPROF, INSTALL_MASK, LC_ALL, LD, L
EX, LFLAGS, LIBTOOL, LINGUAS, MAKE, MAKEFLAGS, OBJCOPY, OBJDUMP, PORTAGE_BINHOST, PORTAGE_BUNZIP2_COMMAND, PORTAGE_COMPRESS, PORTAGE_COMPRESS_FLAGS, PORTAGE_RSYNC_EXTRA_O
PTS, READELF, RUSTFLAGS, SIZE, STRINGS, STRIP, YACC, YFLAGS
```

</p>
</details>


---

# 82
### compiler : `LLVM`
### title : `[clang] incorrect code generation when building gawk 5.2.1 using -O2/-O3`
### open_at : `2023-01-02T21:15:52Z`
### link : https://github.com/llvm/llvm-project/issues/59792
### status : `closed`
### tags : `clang:frontend, miscompilation, release:backport, `
### content : 
It was found that when building gawk 5.2.1 with `-O2` or `-O3`, incorrect machine code is generated which is causing differing runtime behavior than expected.

# Background
Originally I ran into this when upgrading gawk on my personal Gentoo systems to 5.2.1. There is a particular regex[1] used in plymouth which was suddenly erroring that did not previously. Downgrading to gawk 5.1.1, building it with gcc, or disabling compiler optimizations would work around the issue.

This issue is being submitted after some discussion[2] on the gawk-bug mailing list, particularly because of these findings[3].

A simple test case is this command:
```shell
head /dev/zero | awk 'BEGIN { RS="[[][:blank:]]" }'
```
When running this command, the expected behavior is no output and a clean exit. However, when building gawk 5.2.1 with clang and `-O2` or `-O3`, we see this error (and a non-zero exit code):
```console
awk: cmd. line:1: fatal: invalid character class
```

[1] https://gitlab.freedesktop.org/plymouth/plymouth/-/blob/main/scripts/plymouth-set-default-theme.in#L50

[2] https://lists.gnu.org/archive/html/bug-gawk/2022-12/msg00010.html

[3] https://lists.gnu.org/archive/html/bug-gnulib/2023-01/msg00002.html

This is a serious bug in Clang: it generates incorrect machine code.

The code that Clang generates for the following (`gawk/support/dfa.c` lines `1141-1143`):
```c
    ((dfa->syntax.dfaopts & DFA_CONFUSING_BRACKETS_ERROR
      ? dfaerror : dfawarn)
     (_("character class syntax is [[:space:]], not [:space:]")));
```
is immediately followed by the code generated for the following (`gawk/support/dfa.c` line `1015`):
```c
  dfaerror (_("invalid character class"));
```
and this is incorrect because the two source code regions are not connected with each other.

You can see the bug in the attached (compressed) file dfa.s which contains the assembly language output. Here's the dfa.s file starting with line 6975:

```bash
  6975          testb   $4, 456(%r12)
  6976          movl    $dfawarn, %eax
  6977          movl    $dfaerror, %ebx
  6978          cmoveq  %rax, %rbx
  6979          movl    $.L.str.26, %esi
  6980          xorl    %edi, %edi
  6981          movl    $5, %edx
  6982          callq   dcgettext
  6983          movq    %rax, %rdi
  6984          callq   *%rbx
  6985  .LBB34_144:
  6986          movl    $.L.str.25, %esi
  6987          xorl    %edi, %edi
  6988          movl    $5, %edx
  6989          callq   dcgettext
  6990          movq    %rax, %rdi
  6991          callq   dfaerror
```

Line 6984, which is source lines `1141-1143` call to either `dfaerror` or `dfawarn`, is immediately followed by the code for source line 1015. This means that at runtime when `dfawarn` returns the code immediately calls `dfaerror`, which is incorrect.

My guess is that Clang got confused because `dfaerror` is declared _Noreturn, so Clang mistakenly assumed that `dfawarn` is also `_Noreturn`, which it is not.

I worked around the Clang bug by installed the attached patch into Gnulib. Please give it a try with Gawk.

Incorrect code generation is a serious bug in Clang; can you please report it to the Clang folks? I am considering using a bigger hammer, and doing this:
```c
   #define _Noreturn /*empty*/
```
whenever Clang is used, until the bug is fixed.

This is because if the bug occurs here it's likely that similar bugs will occur elsewhere and this sort of thing can be really subtle and hard to catch or work around in general. Clang really needs to get this fixed.

Thanks.

---

# 83
### compiler : `LLVM`
### title : Clang mistakenly elides coroutine allocation resulting in a segfault and `stack-use-after-return` from `AddressSanitizer`
### open_at : `2022-12-27T18:58:41Z`
### link : https://github.com/llvm/llvm-project/issues/59723
### status : `closed`
### tags : `miscompilation, release:backport, release:merged, coroutines, `
### content : 

https://llvm.godbolt.org/z/4ebqEGnPf

The problem was submitted in https://github.com/llvm/llvm-project/issues/56513 and https://github.com/llvm/llvm-project/issues/56455 but there were no responses.
I thought it was specific to Windows, but it turned out to happen also on Linux with Clang 15.0.6 with optimization level `-O3` the address sanitizer detects the access of stack after the coroutine returns.
The code in the [#56513](https://github.com/llvm/llvm-project/issues/56513) had a race condition problem in `final_suspend` but it was not the cause of the problem.

Compile the following code with:
```shell
clang++-15 clangcorobug.cpp -std=c++20 -O3 -g -fsanitize=address -lpthread -o corobug
```

```cpp
#include <atomic>
#include <thread>
#include <condition_variable>
#include <coroutine>
#include <variant>
#include <deque>
#include <cassert>

// executor and operation base

class bug_any_executor;

struct bug_async_op_base {
	void invoke() {
		invoke_operation();
	}

protected:

	~bug_async_op_base() = default;

	virtual void invoke_operation() = 0;
};

class bug_any_executor {
	using op_type = bug_async_op_base;

public:

	virtual ~bug_any_executor() = default;

	// removing noexcept enables clang to find that the pointer has escaped
	virtual void post(op_type& op) noexcept = 0;

	virtual void wait() noexcept = 0;
};

class bug_thread_executor : public bug_any_executor {
	void work_thd() {
		while (!ops_.empty()) {
			std::unique_lock<std::mutex> lock{ lock_ };
			cv_.wait(lock, [this] { return !ops_.empty(); });

			while (!ops_.empty()) {
				bug_async_op_base* op = ops_.front();
				ops_.pop_front();
				op->invoke();
			}
		}

		cv_.notify_all();
	}

	std::mutex lock_;
	std::condition_variable cv_;
	std::deque<bug_async_op_base*> ops_;
	std::thread thd_;

public:

	void start() {
		thd_ = std::thread(&bug_thread_executor::work_thd, this);
	}

	~bug_thread_executor() {
		if (thd_.joinable())
			thd_.join();
	}

	// although this implementation is not realy noexcept due to allocation but I have a real one that is and required to be noexcept
	virtual void post(bug_async_op_base& op) noexcept override {
		{
			std::unique_lock<std::mutex> lock{ lock_ };
			ops_.push_back(&op);
		}
		cv_.notify_all();
	}

	virtual void wait() noexcept override {
		std::unique_lock<std::mutex> lock{ lock_ };
		cv_.wait(lock, [this] { return ops_.empty(); });
	}
};

// task and promise

struct bug_final_suspend_notification {
	virtual std::coroutine_handle<> get_waiter() = 0;
};

class bug_task;

class bug_resume_waiter {
public:
	bug_resume_waiter(std::variant<std::coroutine_handle<>, bug_final_suspend_notification*> waiter) noexcept : waiter_{ waiter } {}

	constexpr bool await_ready() const noexcept { return false; }

	std::coroutine_handle<> await_suspend(std::coroutine_handle<>) noexcept {
		return waiter_.index() == 0 ? std::get<0>(waiter_) : std::get<1>(waiter_)->get_waiter();
	}

	constexpr void await_resume() const noexcept {}

private:
	std::variant<std::coroutine_handle<>, bug_final_suspend_notification*> waiter_;
};

class bug_task_promise {
	friend bug_task;
public:

	bug_task get_return_object() noexcept;

	constexpr std::suspend_always initial_suspend() noexcept { return {}; }

	bug_resume_waiter final_suspend() noexcept {
		return bug_resume_waiter{ waiter_ };
	}

	void unhandled_exception() noexcept {
		ex_ptr = std::current_exception();
	}

	constexpr void return_void() const noexcept {}

	void get_result() const {
		if (ex_ptr)
			std::rethrow_exception(ex_ptr);
	}

	std::variant<std::monostate, std::exception_ptr> result_or_error() const noexcept {
		if (ex_ptr)
			return ex_ptr;
		return {};
	}

private:
	std::variant<std::coroutine_handle<>, bug_final_suspend_notification*> waiter_;
	std::exception_ptr ex_ptr = nullptr;
};

class bug_task {
	friend bug_task_promise;
	using handle = std::coroutine_handle<>;
	using promise_t = bug_task_promise;

	bug_task(handle coro, promise_t* p) noexcept : this_coro{ coro }, this_promise{ p } {
		//printf("task(%p) coroutine(%p) promise(%p)\n", this, this_coro.address(), this_promise);
	}

public:

	using promise_type = bug_task_promise;

	bug_task(bug_task&& other) noexcept
		: this_coro{ std::exchange(other.this_coro, nullptr) }, this_promise{ std::exchange(other.this_promise, nullptr) } { 
		printf("task(task&&: %p) coroutine(%p) promise(%p)\n", this, this_coro.address(), this_promise); 
	}

	~bug_task() {
		if (this_coro) {
			//printf("~task(%p) coroutine(%p) promise(%p)\n", this, this_coro.address(), this_promise);
			this_coro.destroy();
		}
	}

	constexpr bool await_ready() const noexcept {
		return false;
	}

	handle await_suspend(handle waiter) noexcept {
		assert(this_coro != nullptr && this_promise != nullptr);
		this_promise->waiter_ = waiter;
		return this_coro;
	}

	void await_resume() {
		return this_promise->get_result();
	}

	bool is_valid() const noexcept {
		return this_promise != nullptr && this_coro != nullptr;
	}

	void start_coro(bug_final_suspend_notification& w) noexcept {
		assert(this_promise != nullptr && this_coro != nullptr);
		this_promise->waiter_ = &w;
		this_coro.resume(); // never throws since all exceptions are caught by the promise
	}

private:
	handle this_coro;
	promise_t* this_promise;
};

bug_task bug_task_promise::get_return_object() noexcept {
	return { std::coroutine_handle<bug_task_promise>::from_promise(*this), this };
}

// spawn operation and spawner

template<class Handler>
class bug_spawn_op final : public bug_async_op_base, bug_final_suspend_notification {
	Handler handler;
	bug_task task_;

public:

	bug_spawn_op(Handler handler, bug_task&& t)
		: handler { handler }, task_{ std::move(t) } {}

	virtual void invoke_operation() override {
		printf("starting the coroutine\n");
		task_.start_coro(*this);
		printf("started the coroutine\n");
	}

	virtual std::coroutine_handle<> get_waiter() override {
                auto handler2 = std::move(handler);
                delete this;
		handler2();
		return std::noop_coroutine();
	}
};

struct dummy_spawn_handler_t {
	constexpr void operator()() const noexcept {}
};

void bug_spawn(bug_any_executor& ex, bug_task&& t) {
	using op_t = bug_spawn_op<dummy_spawn_handler_t>;
	op_t* op = new op_t{ dummy_spawn_handler_t{}, std::move(t) };
	ex.post(*op);
}

class bug_spawner;

struct bug_spawner_awaiter {
	bug_spawner& s;
	std::coroutine_handle<> waiter;

	bug_spawner_awaiter(bug_spawner& s) : s{ s } {}

	bool await_ready() const noexcept;

	void await_suspend(std::coroutine_handle<> coro);

	void await_resume() {}
};

class bug_spawner {
	friend bug_spawner_awaiter;

	struct final_handler_t {
		bug_spawner& s;

		void operator()() {
			s.on_spawn_finished();
		}
	};

public:

	bug_spawner(bug_any_executor& ex) : ex_{ ex } {}

	void spawn(bug_task&& t) {
		using op_t = bug_spawn_op<final_handler_t>;
		// move task into ptr
		op_t* ptr = new op_t(final_handler_t{ *this }, std::move(t));
		++count_;
		ex_.post(*ptr); // ptr escapes here thus task escapes but clang can't deduce that unless post() is not noexcept
	}

	bug_spawner_awaiter wait() noexcept { return { *this }; }

	void on_spawn_finished()
	{
		if (!--count_ && awaiter_)
		{
			auto a = std::exchange(awaiter_, nullptr);
			a->waiter.resume();
		}
	}

private:

	bug_any_executor& ex_; // if bug_thread_executor& is used instead enables clang to detect the escape of the promise
	bug_spawner_awaiter* awaiter_ = nullptr;
	std::atomic<std::size_t> count_ = 0;
};

bool bug_spawner_awaiter::await_ready() const noexcept {
	return s.count_ == 0;
}

void bug_spawner_awaiter::await_suspend(std::coroutine_handle<> coro) {
	waiter = coro;
	s.awaiter_ = this;
}

template<std::invocable<bug_spawner&> Fn>
bug_task scoped_spawn(bug_any_executor& ex, Fn fn) {
	bug_spawner s{ ex };
	std::exception_ptr ex_ptr;

	try
	{
		fn(s);
	}
	catch (const std::exception& ex) // ex instead of ... to observe the address of ex
	{
		printf("caught an exception from fn(s): %p\n", std::addressof(ex));
		ex_ptr = std::current_exception();
	}

	co_await s.wait();
	if (ex_ptr)
		std::rethrow_exception(ex_ptr);
}

// forked task to start the coroutine from sync code

struct bug_forked_task_promise;

class bug_forked_task {
	friend struct bug_forked_task_promise;
	bug_forked_task() = default;
public:
	using promise_type = bug_forked_task_promise;
};

struct bug_forked_task_promise {
	bug_forked_task get_return_object() noexcept { return {}; }

	constexpr std::suspend_never initial_suspend() noexcept { return {}; }

	constexpr std::suspend_never final_suspend() noexcept { return {}; }

	void unhandled_exception() noexcept {
		std::terminate();
	}

	constexpr void return_void() const noexcept {}
};

// test case

bug_task bug_spawned_task(int id, int inc, std::atomic<int>& n) {
	int result = n += inc;
	std::string msg = "count in coro (" + std::to_string(id) + ") = " + std::to_string(result);
	printf("%s\n", msg.c_str());
	co_return;
}

// using bug_thread_executor& instead of bug_any_executor& resolves the problem
bug_forked_task run_coros(bug_any_executor& ex) {
	std::atomic<int> count = 0;
	auto throwing_fn = [&](bug_spawner& s) {
		int frame_ptr = 0;
		printf("frame ptr ptr: %p\n", std::addressof(frame_ptr));
		s.spawn(bug_spawned_task(1, 2, count)); // the coroutine frame is allocated on the stack !
		s.spawn(bug_spawned_task(2, 3, count));
		s.spawn(bug_spawned_task(3, 5, count));
                // commenting the following line hides the problem
		throw std::runtime_error{ "catch this !" }; // on windows allocated on the stack as required by msvc c++ abi
	};

	try {
		co_await scoped_spawn(ex, throwing_fn);
	}
	catch (const std::exception& ex) {
		printf("scoped_spawn propagated exception: %s\n", ex.what());
	}

	printf("count after scoped_spawn: %d\n", count.load());
}


int main() {
	int var = 0;
	bug_thread_executor ex;
	printf("stack address: %p\n", std::addressof(var));
	run_coros(ex);
	ex.start();
	ex.wait();
	return 0;
}
```
the run `./corobug` and you will get something like this `AddressSanitizer: stack-use-after-return on address 0x7fb1ba9f9338 at pc 0x7fb1bd4d3b58 bp 0x7fb1ba1efd40 sp 0x7fb1ba1efd38`
without the address sanitizer a segfault is received.`


---

# 84
### compiler : `LLVM`
### title : `NTTP of structural class types pass values literally when used directly (should: invoke copy constructors) in Clang 15 (C++)`
### open_at : `2022-12-26T02:40:12Z`
### link : https://github.com/llvm/llvm-project/issues/59699
### status : `open`
### tags : `c++20, clang:frontend, `
### content : 
The Clang C++ compiler produces the wrong output for the following valid C++20 source code:
    
```c++
/*
 * @author{Jelle Hellings}.
 */
#include <iostream>
#include <functional>


/*
 * A function object that returns the input.
 */
constexpr static inline std::identity id = {};


/*
 * A structural class type that keeps track of copies: if a value of this type
 * with copy count @{copy_count} is copied, then the resulting copy will have a
 * copy count of @{copy_count + 1}.
 */
struct copy_counter
{
    /* The copy count. */
    unsigned copy_count;


    /*
     * Create a copy counter: start at zero by default.
     */
    constexpr copy_counter(unsigned init = 0u) noexcept : copy_count{init} {}

    /*
     * The copy constructor: increases the count by one.
     */
    constexpr copy_counter(const copy_counter& other) noexcept :
            copy_count(other.copy_count + 1u) {}
};


/*
 * A template that takes a copy counter @{C} as a non-type template parameter
 * and prints it to standard output. In addition, print the expected value
 * provided by @{expected}.
 */
template<copy_counter C>
void print_nttp(const auto& expected)
{
    std::cout << C.copy_count
              << " (expected: " << expected.copy_count << ")" << std::endl;
}


/*
 * A template that takes a copy counter @{C} as a non-type template parameter
 * and passes it to the above print function in a few different ways.
 */
template<copy_counter C>
void test_cases()
{
    constexpr const copy_counter D = {C.copy_count};
    static_assert(C.copy_count == D.copy_count);

    print_nttp<C>(static_cast<copy_counter>(C));
    print_nttp<D>(static_cast<copy_counter>(D));
    print_nttp<(C)>(static_cast<copy_counter>((C)));
    print_nttp<(C, C)>(static_cast<copy_counter>((C, C)));
    print_nttp<id(C)>(static_cast<copy_counter>(id(C)));
    print_nttp<copy_counter{C}>(static_cast<copy_counter>(copy_counter{C}));
}


/*
 * Entry-point of the program.
 */
int main()
{
    test_cases<copy_counter{}>();
}
```

We have used both the Clang C++ compiler 15.0.1 of Visual Studio 17.4.3 and the x86-64 Clang 15.0.0 compiler  (with `-std=c++20` and `-std=c++2b`) on Compiler Explorer.

According to the C++20 standard, the above code should output:
```console
1 (expected: 1)
1 (expected: 1)
1 (expected: 1)
1 (expected: 1)
1 (expected: 1)
1 (expected: 1)
```

When compiled with both versions of Clang we tried, the above code _incorrectly_ outputs:
```console
0 (expected: 1)
1 (expected: 1)
0 (expected: 1)
1 (expected: 1)
1 (expected: 1)
1 (expected: 1)
```

Note specifically that Clang currently generates different instantiations of `print_nttp` even in cases where _identical_ template arguments are provided (the first two cases).

We refer to the article https://jhellings.nl/article?articleid=1 for a full analysis of what this program should do. In short:

Clause 8 in Section [temp.param] of the C++ standard says:

> An id-expression naming a non-type template-parameter of class type T denotes a static storage duration object of type const T known as a template parameter object, whose value is that of the corresponding template argument after it has been converted to the type of the template-parameter. ...
    
In this case, a conversion of an expression e used as a template argument to type copy_counter will _always_ invoke the copy-constructor, the result of which can be verified via static_cast<copy_counter>(e) according to Clause 1 of Section [expr.static.ast] (The result of the expression static_cast<T>(v) is the result of converting the expression v to type T. ... )


---


# 85
### compiler : `LLVM`
### title : `Miscompilation with noalias and pointer equality`
### open_at : `2022-12-23T16:50:18Z`
### link : https://github.com/llvm/llvm-project/issues/59679
### status : `open`
### tags : `miscompilation, `
### content : 
Reproducer

https://godbolt.org/z/h3zvvxbfE

```c
// test.c
#include <stdio.h>

int x;

__attribute__((noinline))
int test(int * restrict ptr) {
    *ptr = 1;
    if (ptr == &x) {
        *ptr = 2;
    }
    return *ptr;
}

int main() {
    printf("%d\n", test(&x));
}
```
```
$ clang -O3  test.c
$ ./a.out
1
```
Tested with clang 15.0.0 and trunk

The issue appears to be that Clang's constant propagation replaces `*ptr = 2` with `x = 2`, which breaks the noalias *based on* analysis and allows the `return *ptr` to be simplified to `return 1`.


---


# 86
### compiler : `LLVM`
### title : `[LoopVectorizePass] Miscompilation of default vectorization vs no vectorization`
### open_at : `2022-12-22T01:26:55Z`
### link : https://github.com/llvm/llvm-project/issues/59650
### status : `closed`
### tags : `miscompilation, vectorization, `
### content : 
https://gcc.godbolt.org/z/4dfjo4z8v

Correct result is 0 0 0 0. Clang-15 started to have 0 3 0 0 which is miscompilation.

We bisected it to https://github.com/llvm/llvm-project/commit/cedfd7a2e536d2ff6da44e89a024baa402dc3e58, adding @fhahn who is the author of the change

Code:

compile flags `-O3 -msse4.2`

```cpp
#include <optional>
#include <string>
#include <string_view>
#include <iostream>

__attribute__((always_inline)) static inline unsigned char constant_time_ge_8(unsigned int a, unsigned int b) {
  return ~(((unsigned int)(a - b)) >> 15);
}

__attribute__((noinline)) unsigned char CheckPadding(unsigned char *data, unsigned int length)
{
    unsigned int padding_length = data[length - 1];
    unsigned char res = 0;

    for (unsigned int i = 0; i < length - 1; i++) {
        unsigned char mask = constant_time_ge_8(padding_length, i);
        unsigned char b = data[length - 1 - i];
        res |= mask & (padding_length ^ b);
    }

    return res;
}

__attribute__((noinline)) unsigned char CheckPaddingNoVec(unsigned char *data, unsigned int length)
{
    unsigned int padding_length = data[length - 1];
    unsigned char res = 0;

#pragma clang loop vectorize(disable)
    for (unsigned int i = 0; i < length - 1; i++) {
        unsigned char mask = constant_time_ge_8(padding_length, i);
        unsigned char b = data[length - 1 - i];
        res |= mask & (padding_length ^ b);
    }

    return res;
}

__attribute__((aligned(16))) unsigned char data_length41[41] = {
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x03, 0x03, 0x03, 0x03};

__attribute__((aligned(16))) unsigned char data_length40[40] = {
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0x03, 0x03, 0x03};

int main() {
    std::cout << (int)CheckPadding(data_length40, sizeof(data_length40)) << std::endl;
    std::cout << (int)CheckPadding(data_length41, sizeof(data_length41)) << std::endl;
    std::cout << (int)CheckPaddingNoVec(data_length40, sizeof(data_length40)) << std::endl;
    std::cout << (int)CheckPaddingNoVec(data_length41, sizeof(data_length41)) << std::endl;
}
```

If we apply back

```diff
--- a/llvm-project/llvm/lib/Transforms/Vectorize/VPlanTransforms.cpp
+++ b/llvm-project/llvm/lib/Transforms/Vectorize/VPlanTransforms.cpp
@@ -419,7 +419,12 @@ void VPlanTransforms::optimizeInductions
 
     VPScalarIVStepsRecipe *Steps = new VPScalarIVStepsRecipe(ID, BaseIV, Step);
     HeaderVPBB->insert(Steps, IP);
-
+    // If there are no vector users of IV, simply update all users to use Step
+    // instead.
+    if (!WideIV->needsVectorIV()) {
+      WideIV->replaceAllUsesWith(Steps);
+      continue;
+    }
     // Update scalar users of IV to use Step instead. Use SetVector to ensure
     // the list of users doesn't contain duplicates.
     SetVector<VPUser *> Users(WideIV->user_begin(), WideIV->user_end());
```

Then it passes


---

# 87
### compiler : `LLVM`
### title : `Incorrect sign-extension of load's index generated on armv8 under UBSAN`
### open_at : `2022-12-21T02:31:38Z`
### link : https://github.com/llvm/llvm-project/issues/59630
### status : `closed`
### tags : `llvm:optimizations, `
### content : 
Compiling the following on armv8 with `-fsanitize=undefined` results in a UBSan complaint:
```cpp
#include <cstdint>

int main(){
  uint8_t n = 128;
  void *ptrs[200];
  ptrs[(int)n];
  return 0;
}
```

Which reports:
```console
test.cpp:6:3: runtime error: index -128 out of bounds for type 'void *[200]'
SUMMARY: UndefinedBehaviorSanitizer: undefined-behavior test.cpp:6:3 in
```

I believe there is a signed byte load being incorrectly generated instead of an unsigned load in this case, and the resulting sign extension results in an overflow that ubsan detects: https://godbolt.org/z/7Y3f7oxGs

Changing the cast from `(int)` to `(unsigned)` appears to hide the issue.


---

# 88
### compiler : `LLVM`
### title : `miscompilation? with 3010f60381bcd828d1b409cfaa576328bcd05bbc on RISCV`
### open_at : `2022-12-19T16:45:12Z`
### link : https://github.com/llvm/llvm-project/issues/59594
### status : `closed`
### tags : `llvm:codegen, regression, miscompilation, `
### content : 
With 3010f60381bcd828d1b409cfaa576328bcd05bbc the following code seems to yield unexpected results:

https://godbolt.org/z/vKTPrxWrb

```c
void Fill(unsigned char* buffer, int n) {
  for (int i = 0; i < n; i++)
    buffer[i] = (i & 0xff);
}
```

This behavioural change only appears on optimized builds with the v extension).

BB2 seems to loose the advancement of the indicies value (`vadd.vx v8, v8, a3`).

Before:
```asm
_Z4FillPhi:
        blez    a1, .LBB0_3
        li      a2, 0
        csrr    a3, vlenb
        add     a4, a3, a1
        addi    a4, a4, -1
        neg     a5, a3
        and     a4, a4, a5
        vsetvli a5, zero, e8, m1, ta, ma
        vid.v   v8
        vsetvli zero, zero, e64, m8, ta, ma
        vid.v   v16
.LBB0_2:
        vsetvli zero, zero, e64, m8, ta, ma
        vsaddu.vx       v24, v16, a2
        vmsltu.vx       v0, v24, a1
        add     a5, a0, a2
        vse8.v  v8, (a5), v0.t
        add     a2, a2, a3
        vsetvli zero, zero, e8, m1, ta, ma
        vadd.vx v8, v8, a3
        bne     a4, a2, .LBB0_2
.LBB0_3:
        ret
.Lfunc_end0:
        .size   _Z4FillPhi, .Lfunc_end0-_Z4FillPhi
```

After:
```asm
_Z4FillPhi:
        blez    a1, .LBB0_3
        li      a2, 0
        csrr    a3, vlenb
        add     a4, a3, a1
        addi    a4, a4, -1
        neg     a5, a3
        and     a4, a4, a5
        vsetvli a5, zero, e8, m1, ta, ma
        vid.v   v8
        vsetvli zero, zero, e64, m8, ta, ma
        vid.v   v16
.LBB0_2:
        vsaddu.vx       v24, v16, a2
        vmsltu.vx       v0, v24, a1
        add     a5, a0, a2
        add     a2, a2, a3
        vse8.v  v8, (a5), v0.t
        bne     a4, a2, .LBB0_2
.LBB0_3:
        ret
.Lfunc_end0:
        .size   _Z4FillPhi, .Lfunc_end0-_Z4FillPhi
```

The removals of the `vsetvli` should be harmless as the vtype is not changing (questionable if it is correct due to the tail handling, but lets ignore that).  The `add a2, a2, a3` is being scheduled differently but that should be save as the `vse8.v` is not impacted by that.  At that point, the only difference is the `vadd.vx v8, v8, a3`, where `a3` is `vlenb` which would be the stride, and thus is simply forwarding the index base by the stride which is being unrolled here through the vector unit.


---

# 89
### compiler : `LLVM`
### title : `clang-cl 32 bit vectorcall doesn't match msvc 32 bit vectorcall`
### open_at : `2022-12-16T22:01:05Z`
### link : https://github.com/llvm/llvm-project/issues/59561
### status : `open`
### tags : `backend:X86, clang:codegen, ABI, `
### content : 
I got an abi incompatibility between msvc and clang on i686-pc-windows-msvc target using version 15.0.6.

Take this function:
```cpp
float __vectorcall test(
    int ecx, int edx, float xmm0, float xmm1, float xmm2, float xmm3, float xmm4, float xmm5,
    int stack1, float stack2, int stack3
) {
    return stack2;
}
```

In msvc the `stack2` parameter is passed by value, but in clang it is passed by reference. [Godbolt link](https://godbolt.org/z/Gj4Y4WdY3)

The definition for [__vectorcall from Microsoft Docs](https://learn.microsoft.com/en-us/cpp/cpp/vectorcall?view=msvc-170) actually say "seventh and subsequent vector type arguments are passed on the stack by reference to memory allocated by the caller" for x86, but msvc itself does not follow this and passes by value instead.  Msvc only seems to pass by value if the argument is float or double (edit: and long double) but not the other vector types like __m128. `


---

# 90
### compiler : `LLVM`
### title : `structure alignment seems broken when targeting windows`
### open_at : `2022-12-13T02:16:45Z`
### link : https://github.com/llvm/llvm-project/issues/59486
### status : `open`
### tags : `clang:codegen, ABI, `
### content : 
When I put a 16-byte, 4 byte aligned field in a structure, the structure becomes 16 byte aligned. This only happens when the target is `x86_64-pc-windows` (i.e. it does not happen on `x86_64-pc`). It seems to have started in Clang 3.6.
```cpp
typedef __attribute__((__ext_vector_type__(4),__aligned__(4))) float V;
static_assert(alignof(V)==4, "?");

struct S {
	V	v;
};
static_assert(alignof(S)==4, "?");
```
gives
```console
error: static assertion failed due to requirement 'alignof(S) == 4': ?
```


---

# 91
### compiler : `LLVM`
### title : `Potential miscompilation for m2.`
### open_at : `2022-12-12T22:25:30Z`
### link : https://github.com/llvm/llvm-project/issues/59483
### status : `closed`
### tags : `llvm:optimizations, `
### content : 
Hi

This function gives different results with 03 and without (for a sertain combination of options).
I believe that O3 version is incorrect.

```cpp
std::pair<int, int> get_mask(uint8x8_t a) {
    a = vand_u8(a, vdup_n_u64(0x8080898983838181));
    auto desc = vaddv_u16(vpaddl_u8(a));
    return { desc & 0x1f, desc >> 7};
}
```

Complete test case with options to reproduce

https://gist.github.com/DenisYaroshevskiy/85ec7af1d4f283bdb579ae2f49c3284e


<details><summary>전체 코드</summary>
<p>

</p>
</details>


---

# 92
### compiler : `LLVM`
### title : `Miscompile with -fglobal-isel, -ftrivial-auto-var-init=pattern, and thinlto`
### open_at : `2022-12-07T17:22:52Z`
### link : https://github.com/llvm/llvm-project/issues/59376
### status : `closed`
### tags : `miscompilation, llvm:globalisel, LTO, `
### content : 
Repro:

1. Download and gunzip attachment at https://bugs.chromium.org/p/chromium/issues/detail?id=1383873#c53
2.
```shell
bin/clang++ -fno-delete-null-pointer-checks -fno-ident -fno-strict-aliasing -fstack-protector -fcolor-diagnostics -fmerge-all-constants -ffp-contract=off -flto=thin -fsplit-lto-unit -fwhole-program-vtables -fcomplete-member-pointers -arch arm64 -ffile-compilation-dir=. -no-canonical-prefixes -ftrivial-auto-var-init=pattern -fno-omit-frame-pointer -mmacos-version-min=10.13 -O2 -std=c++20 -fno-exceptions -fno-rtti repro.ii -shared -o librepro.dylib -fuse-ld=lld -Wl,-undefined,dynamic_lookup -w -isysroot $(xcrun -show-sdk-path) -fno-global-isel
```
3.
```shell
bin/clang++ -fno-delete-null-pointer-checks -fno-ident -fno-strict-aliasing -fstack-protector -fcolor-diagnostics -fmerge-all-constants -ffp-contract=off -flto=thin -fsplit-lto-unit -fwhole-program-vtables -fcomplete-member-pointers -arch arm64 -ffile-compilation-dir=. -no-canonical-prefixes -ftrivial-auto-var-init=pattern -fno-omit-frame-pointer -mmacos-version-min=10.13 -O2 -std=c++20 -fno-exceptions -fno-rtti repro.ii -shared -o librepro.dylib -fuse-ld=lld -Wl,-undefined,dynamic_lookup -w -isysroot $(xcrun -show-sdk-path) -fglobal-isel
```
4. Compare disassembly for function `__ZN5blink22NGFragmentItemsBuilder17ConvertToPhysicalERKNS_12PhysicalSizeE`

(The only difference between commands 2 and 3 is `-fno-global-isel` vs `-fglobal-isel`.)

The good dylib has this sequence:

```console
% otool -tV librepro.good.dylib | rg -A 233 __ZN5blink22NGFragmentItemsBuilder17ConvertToPhysicalERKNS_12PhysicalSizeE: | rg -A 3 csinc
0000000000002f80	csinc	w8, w8, wzr, ne
0000000000002f84	strh	w8, [sp, #0x38]
0000000000002f88	str	wzr, [sp, #0x40]
0000000000002f8c	ldr	x0, [x24]
```

The bad dylib has this sequence:

```console
% otool -tV librepro.bad.dylib | rg -A 233 __ZN5blink22NGFragmentItemsBuilder17ConvertToPhysicalERKNS_12PhysicalSizeE: | rg -A 3 csinc
0000000000003110	csinc	w8, w8, wzr, ne
0000000000003114	strh	w8, [sp, #0x30]
0000000000003118	mov	w9, #-0x55555556
000000000000311c	str	x9, [sp, #0x30]
```

In the bad dylib, we store something to `sp+0x30`, and then clobber it with `0xaaaaaaaa` (the `-ftrivial-auto-var-init=pattern` pattern) immediately.

This is reduced from https://crbug.com/1383873


---

# 93
### compiler : `LLVM`
### title : `Passing pointer to a local variable prevents TCO`
### open_at : `2022-11-29T23:10:18Z`
### link : https://github.com/llvm/llvm-project/issues/59256
### status : `open`
### tags : `llvm:optimizations, `
### content : 
LLVM optimisation passes fail to convert a tail recursive function into a loop when a stack allocated variable is passed by reference into another function and then falls out of scope before the function recurses.

```cpp

void s(int&);

void foo() {
    {
        int i;
        s(i);
    }
    foo();
}

```

https://godbolt.org/z/1h3o3sMj4


---

# 94
### compiler : `LLVM`
### title : `[coroutines] miscompilation in clang 16 trunk vs clang 15`
### open_at : `2022-11-27T21:29:58Z`
### link : https://github.com/llvm/llvm-project/issues/59221
### status : `closed`
### tags : `miscompilation, llvm:optimizations, coroutines, `
### content : 
I was experimenting with coroutines and symmetric transfer. 

https://compiler-explorer.com/z/457fqjbG8

I expected the coroutine to return 42 instead some random garbage.  Or at least 123 which is set when promise is created, it seems that optimiser is too eager. Other compilers (GCC and MSVC) are correcting expected value.

For some reason it optimises away ASM lines 17 & 18 which contains `return_value` function.

Commit of the clang 16 is `bf0bd85f9d823216501dcc09ae5461c2cf633ccf`



---

# 95
### compiler : `LLVM`
### title : `Trivially Default Constructible with `requires` + Structure Wrapping`
### open_at : `2022-11-25T21:57:40Z`
### link : https://github.com/llvm/llvm-project/issues/59206
### status : `open`
### tags : `c++20, clang:frontend, ABI, concepts, `
### content : 
Consider the following semi-minimal example:
```cpp
//Compile with -std=c++20

#include <type_traits>

template<int n>
struct Foo {
	constexpr Foo() = default;

	template<class... Ts>
	Foo(Ts... vals) requires(sizeof...(Ts)==n) {}
};

struct Bar {
	Foo<4> foo;
};

static_assert(std::is_trivially_default_constructible_v< Foo<4> >); //Fine
static_assert(std::is_trivially_default_constructible_v< Bar    >); //Fails???
```
The first `static_assert` passes, indicating that `Foo<4>` is trivially default constructible. However, we now wrap `Foo<4>` in a class `Bar` which does nothing, and suddenly the type is no longer trivially default constructible and the second `static_assert` fails:

```console
<source>:18:1: error: static assertion failed due to requirement 'std::is_trivially_default_constructible_v<Bar>'
static_assert(std::is_trivially_default_constructible_v< Bar    >);
^             ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1 error generated.
Compiler returned: 1
```

I believe that this is incorrect behavior. We can verify that `Foo<4>` is indeed trivially default-constructible per [the definition](https://en.cppreference.com/w/cpp/language/default_constructor#Trivial_default_constructor), and of course by the `static_assert` passing. Even if `Foo<4>` didn't fully constrain the constructors, the non-templated defaulted constructor should be selected preferentially. Next, wrapping `Foo<4>` in `Bar` should do nothing; if anything it should ensure that *only* the default constructor is accessible. And finally, GCC, MSVC, and even Intel Compiler (now based on LLVM) accept this code without complaint.

The tested version:

```console
clang version 16.0.0 (https://github.com/llvm/llvm-project.git 437ccf5af9c2aec915a68a164a95d506fbac2324)
```

Note that this is a regression. E.g. Clang 15 accepts the code.`


---

# 96
### compiler : `LLVM`
### title : `coroutines: miscompilation when using ternary operator and co_await (use after free)`
### open_at : `2022-11-24T01:37:10Z`
### link : https://github.com/llvm/llvm-project/issues/59181
### status : `closed`
### tags : `miscompilation, coroutines, `
### content : 
https://godbolt.org/z/avrxq5zb9

```cpp
res ok(bool cond) {
    if (cond) {
        co_return res{co_await foo_error()};
    } else {
        co_return res{5};
    }
}

res notok(bool cond) {
    co_return cond ? res{co_await foo_error()} : res{5};
}

int main() {
    ok(false);    //ok
    ok(true);     //ok
    notok(false); //ok
    notok(true);  //crash
}
```

results in:
```bash
=================================================================
==1==ERROR: AddressSanitizer: heap-use-after-free on address 0x6070000001ae at pc 0x5555f4f0091e bp 0x7fff81013350 sp 0x7fff81013348
READ of size 1 at 0x6070000001ae thread T0
    #0 0x5555f4f0091d in notok(bool) /app/example.cpp:104:26
    #1 0x5555f4f013e5 in main /app/example.cpp:111:5
    #2 0x7f9da9a28082 in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x24082) (BuildId: 1878e6b475720c7c51969e69ab2d276fae6d1dee)
    #3 0x5555f4e2739d in _start (/app/output.s+0x1f39d)

0x6070000001ae is located 62 bytes inside of 72-byte region [0x607000000170,0x6070000001b8)
freed by thread T0 here:
    #0 0x5555f4efd30d in operator delete(void*) /root/llvm-project/compiler-rt/lib/asan/asan_new_delete.cpp:152:3
    #1 0x5555f4f05442 in notok(bool) (.destroy) /app/example.cpp:103:5
    #2 0x5555f4f0a8f4 in std::__1::coroutine_handle<void>::destroy[abi:v160000]() const /opt/compiler-explorer/clang-trunk-20221123/bin/../include/c++/v1/__coroutine/coroutine_handle.h:84:9
    #3 0x5555f4f07554 in res_promise_type::await_transform(res)::Suspension::await_suspend(std::__1::coroutine_handle<void>) /app/example.cpp:73:22
    #4 0x5555f4f008da in notok(bool) /app/example.cpp:104:26
    #5 0x5555f4f013e5 in main /app/example.cpp:111:5
    #6 0x7f9da9a28082 in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x24082) (BuildId: 1878e6b475720c7c51969e69ab2d276fae6d1dee)

previously allocated by thread T0 here:
    #0 0x5555f4efcaad in operator new(unsigned long) /root/llvm-project/compiler-rt/lib/asan/asan_new_delete.cpp:95:3
    #1 0x5555f4f00017 in notok(bool) /app/example.cpp:103:5
    #2 0x5555f4f013e5 in main /app/example.cpp:111:5
    #3 0x7f9da9a28082 in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x24082) (BuildId: 1878e6b475720c7c51969e69ab2d276fae6d1dee)

SUMMARY: AddressSanitizer: heap-use-after-free /app/example.cpp:104:26 in notok(bool)
Shadow bytes around the buggy address:
  0x606fffffff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x606fffffff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x607000000000: fa fa fa fa fd fd fd fd fd fd fd fd fd fa fa fa
  0x607000000080: fa fa fd fd fd fd fd fd fd fd fd fa fa fa fa fa
  0x607000000100: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fd fd
=>0x607000000180: fd fd fd fd fd[fd]fd fa fa fa fa fa fa fa fa fa
  0x607000000200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x607000000280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x607000000300: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x607000000380: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x607000000400: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==1==ABORTING
```


---

# 97
### compiler : `LLVM`
### title : `clang trunk at -O2/3 misses a global-buffer-overflow`
### open_at : `2022-11-23T17:20:30Z`
### link : https://github.com/llvm/llvm-project/issues/59169
### status : `open`
### tags : `compiler-rt:asan, llvm:optimizations, `
### content : 
For the following code, `clang-trunk -O2 -fsanitize=address` (or `-O3`) misses the global-buffer-overflow, while `clang-trunk -Ox -fsanitize=address` (x=0,1, or s) can detect it.

GCC can detect it at all optimization levels.

The overflow happens at ` a=a+2; i[0]; *a=1`, which overflows variable `c`. I checked the assembly code of `-O2/3`, which did not optimize away these codes. I believe this should be a sanitizer implementation bug.

I have reported a few other sanitizer implementation issues to GCC team (an example: https://gcc.gnu.org/bugzilla/show_bug.cgi?id=106558) and they confirmed and fixed these bugs. 
Such issues caused ASAN to miss certain kinds of bugs and may lead to false negatives in practice. ASAN and other sanitizers are extremely popular and have been widely used to find security flaws in many critical software, I believe such issues should be properly handled to avoid missing of bugs.

Compiler explorer: https://godbolt.org/z/nvhM4j9h6

```cpp
% cat .c
struct {
  short b
}  g, i[8];
int c;
unsigned j;
int o() {
  int *a = &c;
  for (j=-9; j > 0; j = j + 1) {
    a = a + 2;
    i[0];
    *a = 1;
  }
  return *a;
}
int main() { 
  int a = o(); 
  __builtin_printf("a=%d\n", a);
}
% clang-tk -O2 -fsanitize=address a.c && ./a.out
a=1
%
% clang-tk -O1 -fsanitize=address a.c && ./a.out
=================================================================
==1==ERROR: AddressSanitizer: global-buffer-overflow on address 0x55a65d87c668 at pc 0x55a65ccf31d8 bp 0x7fff997c47b0 sp 0x7fff997c47a8
WRITE of size 4 at 0x55a65d87c668 thread T0
    #0 0x55a65ccf31d7 in o /app/a.c:11:8
    #1 0x55a65ccf31d7 in main /app/a.c:16:11
    #2 0x7f11300e8082 in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x24082) (BuildId: 1878e6b475720c7c51969e69ab2d276fae6d1dee)
    #3 0x55a65cc1da4d in _start (/app/output.s+0x1da4d)

0x55a65d87c668 is located 56 bytes before global variable 'i' defined in '/app/example.c:3' (0x55a65d87c6a0) of size 16
0x55a65d87c668 is located 24 bytes before global variable 'j' defined in '/app/example.c:5' (0x55a65d87c680) of size 4
0x55a65d87c668 is located 4 bytes after global variable 'c' defined in '/app/example.c:4' (0x55a65d87c660) of size 4
SUMMARY: AddressSanitizer: global-buffer-overflow /app/example.c:11:8 in o
Shadow bytes around the buggy address:
  0x55a65d87c380: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x55a65d87c400: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x55a65d87c480: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x55a65d87c500: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x55a65d87c580: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x55a65d87c600: 00 00 00 00 00 00 00 00 00 00 00 00 04[f9]f9 f9
  0x55a65d87c680: 04 f9 f9 f9 00 00 f9 f9 02 f9 f9 f9 00 00 00 00
  0x55a65d87c700: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x55a65d87c780: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x55a65d87c800: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x55a65d87c880: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==1==ABORTING
%
```


---

# 98
### compiler : `LLVM`
### title : `Bad codegen after 8adfa29706e (NaN constant folding weirdness)`
### open_at : `2022-11-22T05:02:10Z`
### link : https://github.com/llvm/llvm-project/issues/59122
### status : `closed`
### tags : `regression, miscompilation, llvm:optimizations, incomplete, `
### content : 
We have an internal test that recently started to fail which I bisected back to 8adfa29706e5407b62a4726e2172894e0dfdc1e8.

I was able to reduce the test a little bit to the following:
```c++
extern "C" void printf(...);
typedef float __m128 __attribute__((__vector_size__(16)));
typedef int __v8su __attribute__((__vector_size__(32)));
typedef float __m256 __attribute__((__vector_size__(32)));
__m256 _mm256_max_ps___b, _mm256_hadd_ps___b, _mm256_hsub_ps___b,
    test89___trans_tmp_15, test89___trans_tmp_14, test89___trans_tmp_13,
    test89___trans_tmp_12, test89___trans_tmp_11, test89___trans_tmp_10,
    test89___trans_tmp_8, test89___trans_tmp_7, test89___trans_tmp_6,
    test89___trans_tmp_5, test89___trans_tmp_4, test89___trans_tmp_3,
    test89_id18854, test89_id18860, test89_id18872, test89_id18873;
template <typename T> T zero_upper(T in, unsigned) { return in; }
void init(char pred, void *data, unsigned size) {
  unsigned char *bytes = (unsigned char *)data;
  for (unsigned i = 0; i != size; ++i)
    bytes[i] = pred + i;
}
typedef long __attribute__((ext_vector_type(2))) ll2;
ll2 test89_id18839 = -1964383749;
__m128 test89_id18845, test89_id18879, test89_id18881;
void test89() {
  test89___trans_tmp_3 = __builtin_ia32_vcvtph2ps256(test89_id18839);
  init(69, &test89_id18845, sizeof(test89_id18845));
  test89___trans_tmp_4 = __builtin_shufflevector(test89_id18845, test89_id18845,
                                                 0, 1, 2, 3, 1, 1, 1, 1);
  __m256 id18844, id18870;
  test89___trans_tmp_5 = __builtin_ia32_rcpps256(id18844);
  test89___trans_tmp_6 =
      __builtin_ia32_maxps256(test89___trans_tmp_5, _mm256_max_ps___b);
  init(211, &test89_id18854, sizeof(test89_id18854));
  test89___trans_tmp_7 = (__v8su)test89___trans_tmp_6 & (__v8su)test89_id18854;
  init(205, &test89_id18860, sizeof(test89_id18860));
  test89___trans_tmp_8 =
      __builtin_ia32_hsubps256(test89_id18860, _mm256_hsub_ps___b);
  for (int id18871_idx = 0; id18871_idx < 92; ++id18871_idx) {
    init(220, &test89_id18872, sizeof(test89_id18872));
    id18870 *= test89_id18872;
  }
  init(220, &test89_id18873, sizeof(test89_id18873));
  __m128 id18878;
  init(252, &id18878, sizeof(id18878));
  for (int id18880_idx = 0; id18880_idx < 31; ++id18880_idx)
    test89_id18879 -= test89_id18881;
  __m128 __a = id18878;
  __a[0] += test89_id18881[0];
  test89___trans_tmp_10 =
      __builtin_shufflevector(__a, __a, 0, 1, 2, 3, 1, 1, 1, 1);
  __m256 id18874(zero_upper(test89___trans_tmp_10, 8));
  test89___trans_tmp_11 =
      __builtin_ia32_blendvps256(id18870, test89_id18873, id18874);
  test89___trans_tmp_12 = __builtin_shufflevector(
      test89___trans_tmp_8, test89___trans_tmp_11, 0, 8, 1, 1, 4, 2, 1, 1);
  test89___trans_tmp_13 =
      __builtin_ia32_haddps256(test89___trans_tmp_12, _mm256_hadd_ps___b);
  test89___trans_tmp_14 =
      ~(__v8su)test89___trans_tmp_7 & (__v8su)test89___trans_tmp_13;
  test89___trans_tmp_15 =
      (__v8su)test89___trans_tmp_3 | (__v8su)test89___trans_tmp_14;
  printf("%f\n", test89___trans_tmp_15[0]);
}
int main() { test89(); }
```
When the above code is compiled with optimizations targeting btver2 (`-O2 -march=btver2`), it generates a different value after 8adfa29706e5407b62a4726e2172894e0dfdc1e8:
```console
$ ~/src/upstream/ffe1661fabc9cf379a10a0bf15268c6549e4836f-linux/bin/clang++ -O2 -march=btver2 test.cpp -o test.good.elf
$ ./test.good.elf
-268361104.000000
$ ~/src/upstream/8adfa29706e5407b62a4726e2172894e0dfdc1e8-linux/bin/clang++ -O2 -march=btver2 test.cpp -o test.bad.elf
$ ./test.bad.elf
-3701730859659994532950310912.000000
```
Here is a link to godbolt showing the output difference between trunk and LLVM 15: https://godbolt.org/z/E63hbbTfs`


---

# 99
### compiler : `LLVM`
### title : `Static array indices in function parameter declarations cause poor SIMD code-generation`
### open_at : `2022-11-22T00:03:31Z`
### link : https://github.com/llvm/llvm-project/issues/59120
### status : `open`
### tags : `llvm:optimizations, `
### content : 
Static array indices in function parameter declarations poorly interfere with lowering of SIMD load-and-splat instructions, causing Clang/LLVM to generate separate full-vector load + vector-to-vector broadcast instructions. Here's the simplest example ([repro in Compiler Explorer](https://gcc.godbolt.org/z/hW5r4ehhK)):

```c
#include <stddef.h>

#include <wasm_simd128.h>

struct minmax_params {
  float min[2];
  float max[2];
};

v128_t f(const struct minmax_params params[1])
{
    // Generates v128.load64_splat as expected
    return wasm_v128_load64_splat(&params->min);
}

v128_t g(const struct minmax_params params[static 1])
{
    // Generates two instructions: v128.load + i8x16.shuffle
    return wasm_v128_load64_splat(&params->min);
}
```

The example above is for WebAssembly SIMD, but this issue is not specific to this backend and can be reproduced at least on ARM as well.


---

# 100
### compiler : `LLVM`
### title : `Incorrect codegen for unaligned load/store (ARM NEON)`
### open_at : `2022-11-19T06:19:42Z`
### link : https://github.com/llvm/llvm-project/issues/59081
### status : `open`
### tags : `backend:ARM, llvm:codegen, miscompilation, `
### content : 
https://clang.godbolt.org/z/nEfsT961d

```c
#include <arm_neon.h>
#include <stdint.h>

void double32(uint8_t* data) {
    uint8x16x2_t x = vld1q_u8_x2(data);
    uint8x16_t y0 = vaddq_u8(x.val[0], x.val[0]);
    uint8x16_t y1 = vaddq_u8(x.val[1], x.val[1]);
    uint8x16x2_t y = {y0, y1};
    vst1q_u8_x2(data, y);
}
```

```asm
double32:
        vld1.8  {d16, d17, d18, d19}, [r0:256] ; <- should be [r0]
        vshl.i8 q11, q9, #1
        vshl.i8 q10, q8, #1
        vst1.8  {d20, d21, d22, d23}, [r0:256] ; <- should be [r0]
        bx      lr
```

https://developer.arm.com/documentation/den0018/a/NEON-Instruction-Set-Architecture/Alignment

It seems that there is no way to generate unaligned load/store instructions.


---

# 101
### compiler : `LLVM`
### title : `Poor code when a pointer is a global var, but good code for static or local var`
### open_at : `2022-11-16T22:38:19Z`
### link : https://github.com/llvm/llvm-project/issues/59043
### status : `open`
### tags : `llvm:optimizations, `
### content : 
If you add `static` before `ptr` below, or make it a local var in function `main()` it generates 3 store instruction storing constant integer data. If you leave it as-is it generates pretty poor code. Every element in each struct is written to and there is no padding in any struct so I don't see why it would behave differently for a global.

```c
#include "stdlib.h"
#include "stdint.h"

typedef union reg1_t {
  uint32_t val;
  struct {
    uint32_t name1 :13;
    uint32_t name2 :6;
    uint32_t name3 :9;
    uint32_t name4 :4;
  } field;
} reg1_t; 

typedef union reg2_t {
  uint32_t val;
  struct {
    uint32_t name1 :7;
    uint32_t name2 :13;
    uint32_t name3 :12;
  } field;
} reg2_t; 

typedef union reg3_t {
  uint32_t val;
  struct{
    uint32_t name1 :13;
    uint32_t name2 :6;
    uint32_t name3 :9;
    uint32_t name4 :4;
  } field;
} reg3_t; 

typedef struct hw_reg {
  reg1_t reg1;
  reg2_t reg2;
  reg3_t reg3;
} hw_reg;

hw_reg *ptr = (hw_reg*) 0x90000000;

int main() {
  ptr->reg1.field.name1=3;
  ptr->reg1.field.name2=3;
  ptr->reg1.field.name3=3;
  ptr->reg1.field.name4=3;

  ptr->reg2.field.name1=3;
  ptr->reg2.field.name2=3;
  ptr->reg2.field.name3=3;

  ptr->reg3.field.name1=3;
  ptr->reg3.field.name2=3;
  ptr->reg3.field.name3=3;
  ptr->reg3.field.name4=3;
  return 0;
}
```


---

# 102
### compiler : `LLVM`
### title : `Incorrect codegen for int128 parameters with x64-systemv calling conv`
### open_at : `2022-11-16T00:15:09Z`
### link : https://github.com/llvm/llvm-project/issues/59011
### status : `open`
### tags : `clang:codegen, `
### content : 
## Description

When compiling C/C++ code that takes an __int128 as its sixth argument, llvm splits it into two 64bit ints that get passed in a register and on the stack. According to the SysV ABI __int128 should be treated like a struct of two 64bit ints and therefore be passed completely in memory in that case.

## Reproduction
[https://godbolt.org/z/o8MMMYdY6](https://godbolt.org/z/o8MMMYdY6)

Input C++:
```cpp
using uint128_t = unsigned __int128;

unsigned long long tmpfn(uint64_t, uint64_t, uint64_t, uint64_t, uint64_t, uint128_t t) {
    return (t >> 64) & 0xFFFFFFFFFFFFFFFF;
}

unsigned long long tmpfn2(uint64_t, uint64_t, uint64_t, uint64_t, uint64_t, uint128_t t) {
    return t & 0xFFFFFFFFFFFFFFFF;
}
```

Output from clang 15:
```assembly
tmpfn:
        mov     rax, qword ptr [rsp + 8]
        ret
tmpfn2:
        mov     rax, r9
        ret
```
        
Output from gcc 12:
```assembly
tmpfn:
        mov     rax, QWORD PTR [rsp+16]
        ret
tmpfn2:
        mov     rax, QWORD PTR [rsp+8]
        ret
```


---

# 103
### compiler : `LLVM`
### title : `C, C11 and later: padding not set to “zero bits” in compound literal`
### open_at : `2022-11-11T20:07:11Z`
### link : https://github.com/llvm/llvm-project/issues/58945
### status : `open`
### tags : `c11, c17, `
### content : 
Consider the C program:
```c
#include <stdint.h>
#include <string.h>
#include <stdio.h>

struct record {
  uint64_t id;
  uint32_t gold_coins;
};

__attribute__((noinline))
void sink(void*p) {
    static const struct record ref = {1};
    if (memcmp(&ref, p, sizeof ref))
      printf("different\n");
    else
      printf("identical\n");
}

int main(void) {
    struct record a = {1};
    sink(&a);

    void *p = &(struct record){1};
    sink(p);
}
```
The program above compiled with Clang 15.0.0 using `clang -std=c17 -O2` prints:
```console
identical
different
```
[Compiler Explorer link](https://gcc.godbolt.org/z/KqsMaevcj)

The “different” output shows that the padding of the compound literal was not set to 0. Here's the relevant snippet of the generated assembly:
```asm
        movq    $1, (%rsp)
        movl    $0, 8(%rsp)
        movq    %rsp, %rdi
        callq   sink
```

This might indicate a bug in Clang, depending on how one interprets the words “the remainder of the aggregate” in [C17 6.7.9:21](https://cigix.me/c17#6.7.9.p21):

> If there are fewer initializers in a brace-enclosed list than there are elements or members of an aggregate, or fewer characters in a string literal used to initialize an array of known size than there are elements in the array, the remainder of the aggregate shall be initialized implicitly the same as objects that have static storage duration.

If “the remainder of the aggregate” is taken to include padding, then the padding should be zeroed in the compound literal in my example according to C17 6.7.9:10, which applies in this case per the phrase “the same as objects that have static storage duration” in 6.7.9:21.

If “the remainder of the aggregate” is taken not to include padding, then Clang needlessly generates and copies zero bits in the case of the automatic variable `a`. From the assembly output:
```s
.L__const.main.a:
        .quad   1                               # 0x1
        .long   0                               # 0x0
        .zero   4
```


---

# 104
### compiler : `LLVM`
### title : `Constant tracking foiled by an escaping reference`
### open_at : `2022-11-09T15:53:06Z`
### link : https://github.com/llvm/llvm-project/issues/58899
### status : `open`
### tags : `llvm:optimizations, `
### content : 
Something weird happens to Clang's tracking a variable's value once it is passed by reference - __builtin_assume-ing its value afterwards or even actually reassigning it does not help the compiler 'get its head together'.

Both __builtin_constant_p and the enable_if attribute then fail to 'detect' the 'obviously constant value' (which the compiler also obviously knows at compile-time since it generates code which stores the constant value directly into the function argument register ??).

https://godbolt.org/z/3M8nx6qE7

Tthis issue actually causes significant binary bloat (useless object cleanups being called for already destroyed objects)  in our production code which relies heavily on generated and generic C++ code.


---

# 105
### compiler : `LLVM`
### title : `[avr] Return values are promoted to (unsigned) int for no reason.`
### open_at : `2022-11-08T12:02:43Z`
### link : https://github.com/llvm/llvm-project/issues/58877
### status : `closed`
### tags : `clang:codegen, `
### content : 
Compile with `--target=avr -mmcu=atmega8 -Os -save-temps` the following code:
```c++
char func (char c)
{
    return c;
}
```
The generated assembly reads:
```asm
func:
	mov	r25, r24
	lsl	r25
	sbc	r25, r25
	ret
```
which just wastes 3 cycles and 6 bytes for integer promotion that's not required.


---

# 106
### compiler : `LLVM`
### title : `Friended struct with concept gives different output in clang/gcc/MSVC `
### open_at : `2022-11-06T21:46:51Z`
### link : https://github.com/llvm/llvm-project/issues/58833
### status : `open`
### tags : `c++20, concepts, `
### content : 
GCC bug report: https://gcc.gnu.org/bugzilla/show_bug.cgi?id=107544

I don't know which compiler is right, but all three give a different output.

https://godbolt.org/z/7Pq3eWhc8

```cpp
#include <compare>
#include <concepts>
#include <iostream>

template <class T>
concept HasTag = requires {
    T::Tag;
    requires std::same_as<decltype(T::Tag), const bool>;
};

template <class T>
struct check_tag final {
    static constexpr bool value()
        requires(!HasTag<T>)
    {
        return false;
    }

    static constexpr bool value()
        requires(HasTag<T>)
    {
        return T::Tag;
    };
};

struct S {
   private:
    template <class T>
    friend struct check_tag;
    static constexpr bool Tag = true;
};

int main() {
    std::cout << HasTag<S> << "\n";
    std::cout << check_tag<S>::value() << "\n";
}
```

Clang output (the concept sees private data if used in friend):
```console
0
1
```

GCC output (the concept always sees private data):
```console
1
1
```

MSVC output (the concept never sees private data):
```console
0
0
```


---

# 107
### compiler : `LLVM`
### title : `__attribute__((pure))`/`__attribute__((const))` is a massive unchecked footgun
### open_at : `2022-11-03T21:47:09Z`
### link : https://github.com/llvm/llvm-project/issues/58798
### status : `open`
### tags : `clang:codegen, compiler-rt:ubsan, `
### content : 
This originates from https://oss-fuzz.com/testcase-detail/5834828872548352

Consider (somewhat reduced from the original source):
```cpp
#include <vector>

std::vector<int> handle() {
  std::vector<int> v(42, 42); // this somehow leaks
  return v;
}

__attribute__((pure)) // double yikes
std::vector<int> footgun(int argc) {
  std::vector<int> v(24, 24);
  if(argc != 42)
    throw int(0); // yikes
  return v;
}

int main(int argc, char* argv[]) {
    try {
        auto v = handle();
        auto v2 = footgun(argc);
    } catch(...) {}
    return 0;
}
```
https://godbolt.org/z/zdavdKnfa

Not a single diagnostic is triggered by this.
Yet this is completely broken.

In oss-fuzz issue, this manifested as an obscure leak,
exception got optimized away, so this took a bit to understand...

```cpp
    // 'const', 'pure' and 'noalias' attributed functions are also nounwind.
    if (TargetDecl->hasAttr<ConstAttr>()) {
      FuncAttrs.addAttribute(llvm::Attribute::ReadNone);
      FuncAttrs.addAttribute(llvm::Attribute::NoUnwind);
      // gcc specifies that 'const' functions have greater restrictions than
      // 'pure' functions, so they also cannot have infinite loops.
      FuncAttrs.addAttribute(llvm::Attribute::WillReturn);
    } else if (TargetDecl->hasAttr<PureAttr>()) {
      FuncAttrs.addAttribute(llvm::Attribute::ReadOnly);
      FuncAttrs.addAttribute(llvm::Attribute::NoUnwind);
      // gcc specifies that 'pure' functions cannot have infinite loops.
      FuncAttrs.addAttribute(llvm::Attribute::WillReturn);
```

Which means functions with these attributes *can* can call non-returning functions,
or functions that throw exceptions, but the exception must be handled within the function.
Yet we fail to catch that at all, even in UBSan.

I think at least 4 things are missing:
* we should infer `nothrow` attribute (and manifest in AST!) upon seeing `const`/`pure`.
  that would catch the simplified snippet: https://godbolt.org/z/nM6PM6Msc
* ubsan really should catch exception escape out of `noexcept` fn https://godbolt.org/z/z553KbPz4
* we lack `willthrow` clang attribute. (maybe also `maythrow`?)
  * we should add it, infer it from `throw` stmts
  * and propagate it in obvious cases through call stack
* we should diagnose calls to `willthrow` functions from `nothrow` functions :)

CC @AaronBallman @regehr 


---


# 108
### compiler : `LLVM`
### title : `The preferred global deallocation for the array whose element is of class type with non-trival destructor`
### open_at : `2022-11-03T14:08:49Z`
### link : https://github.com/llvm/llvm-project/issues/58786
### status : `open`
### tags : `c++, clang:frontend, `
### content : 
```cpp
void* operator new[](std::size_t N){
    auto ptr = malloc(sizeof(char)* N);
    std::cout<<"new\n";
    return ptr;
}
void operator delete[](void* ptr,std::size_t N) noexcept{  // #1
    std::cout<<"delete\n";
    free(ptr);
}

struct A{
  ~A(){}
};
int main(){
   auto ptr = new A[2];
   delete [] ptr;
}
```
The found deallocation for the delete-expression should be `#1` and these implicitly declared ones in global scope
>  - void operator delete[](void*) noexcept;
> - void operator delete[](void*, std::align_val_t) noexcept;
> - void operator delete[](void*, std::size_t, std::align_val_t) noexcept;

In this example, clang does not select `#1` but it should be the preferred one as per [expr.delete] p10
> If more than one deallocation function is found, the function to be called is selected as follows: 
>> - [...]
>> - If the deallocation functions **belong to a class scope**, the one without a parameter of type std​::​size_­t is selected.
>> - If the type is complete and if, for an array delete expression only, the operand is a pointer to a class type with a non-trivial destructor or a (possibly multi-dimensional) array thereof, the function with a parameter of type std​::​size_­t is selected.  

The second bullet does not apply here since the found declarations belong to global scope. The third bullet should apply here. For single object delete expression, clang also does not select the one with `std::size_t` but it should be.

```cpp
void* operator new(std::size_t N){
    auto ptr = malloc(sizeof(char)* N);
    std::cout<<"single new "<< (long long int) ptr<<std::endl;
    return ptr;
}

void operator delete(void* ptr,std::size_t N) noexcept{
    std::cout<<"single delete "<< (long long int) ptr<<std::endl;
    free(ptr);
}
struct A{
  // ~A(){}
};
int main(){
    auto p = new A;
    delete p;
}
```
The one with parameter `std::size_t` should be selected regardless of whether the destructor of `A` is trivial or non-trivial according to third bullet. GCC is correct in two cases https://godbolt.org/z/5G41dP3P8`


---

# 109
### compiler : `LLVM`
### title : `wrong code at -O1 and above`
### open_at : `2022-11-02T12:44:44Z`
### link : https://github.com/llvm/llvm-project/issues/58765
### status : `open`
### tags : `backend:X86, llvm:codegen, miscompilation, `
### content : 
This appears to be a recent regression as 15.0.0 compiles the test correctly.

Compiler Explorer: https://godbolt.org/z/6MG54GarG

```cpp
% clangtk -v
clang version 16.0.0 (https://github.com/llvm/llvm-project.git 0c1f9b3f17bcb0639d5f2684771ef21c9508632c)
Target: x86_64-unknown-linux-gnu
Thread model: posix
InstalledDir: /local/suz-local/opfuzz/bin
Found candidate GCC installation: /usr/lib/gcc/i686-linux-gnu/8
Found candidate GCC installation: /usr/lib/gcc/x86_64-linux-gnu/10
Found candidate GCC installation: /usr/lib/gcc/x86_64-linux-gnu/11
Found candidate GCC installation: /usr/lib/gcc/x86_64-linux-gnu/6
Found candidate GCC installation: /usr/lib/gcc/x86_64-linux-gnu/6.5.0
Found candidate GCC installation: /usr/lib/gcc/x86_64-linux-gnu/7
Found candidate GCC installation: /usr/lib/gcc/x86_64-linux-gnu/7.5.0
Found candidate GCC installation: /usr/lib/gcc/x86_64-linux-gnu/8
Selected GCC installation: /usr/lib/gcc/x86_64-linux-gnu/11
Candidate multilib: .;@m64
Selected multilib: .;@m64
% 
% clangtk -O0 small.c; ./a.out
0
% clangtk -O1 small.c
% ./a.out
0
Floating point exception
% cat small.c
int printf(const char *, ...);
int a;
short b = 5, c;
int main() {
  short e = -1;
  unsigned short f;
  char g = 25;
  long h = 0;
  if (a) {
    h = -1;
    g = 0;
  }
  short i = ~g;
  unsigned j = g;
  if (b) {
    f = (h | (i | (583 | j))) ^ ~(~(g & 5L) / e);
    c = 22 / (8UL - (f - 0));
    if (f > 0)
      printf("0\n");
  }
  int k = h % c;
  short l = f ^ 5L;
  if (l)
    a = k;
  return 0;
}
```


---

# 110
### compiler : `LLVM`
### title : `Infinite self-recursion for functions renamed with __asm__, combined with inline specialization of it`
### open_at : `2022-11-01T10:14:19Z`
### link : https://github.com/llvm/llvm-project/issues/58724
### status : `open`
### tags : `c, clang:codegen, `
### content : 
(This relates to similar code patterns as in https://reviews.llvm.org/D137073.)

One may want to redirect a well known public function name to a specific implementation name with `__asm__`.

One may also want to specialize that function with an inline version of it, which may (or may not) do special extra checks on the inputs, and fall back on the base implementation for the heavy lifting. This pattern with extra inline specializations is used e.g. for `_FORTIFY_SOURCE` macros.

This may look something like this:
```c
#ifdef _WIN64
typedef unsigned long long size_t;
#elif defined(_WIN32)
typedef unsigned int size_t;
#else
typedef unsigned long size_t;
#endif

//#define public_func_name strlen

size_t func_impl(const char *);

// Redirect use of public_func_name to func_impl. The declaration above
// is only necessary to allow calling it directly.
size_t public_func_name(const char *) __asm__("func_impl");

// Provide an inline version of public_func_name, which might or might not
// do some extra checks, and finally falls back on calling func_impl.
extern __inline__ __attribute__((__always_inline__, __gnu_inline__))
size_t public_func_name(const char *a) { 
  return func_impl(a);
}

void call(void) {
  public_func_name("foo");
}
```

If this is compiled with current Clang (e.g. 2390bb2347703bf500333fcd4d8c1b513a6e1740, Nov 1 2022), it produces an infinite loop:
```console
$ clang -target x86_64-linux-gnu -S -o - -O2 clang-rename-inline.c
call:
.LBB0_1:
        jmp     .LBB0_1
```

If the function `public_func_name` is renamed to a function which Clang knows as a builtin, e.g. by uncommenting `#define public_func_name strlen`, then Clang successfully compiles this as one would have hoped:
```console
$ clang -target x86_64-linux-gnu -S -o - -O2 clang-rename-inline.c
call:
        leaq    .L.str(%rip), %rdi
        jmp     func_impl@PLT
```

This can be tested online at https://gcc.godbolt.org/z/b814Y9Tjb too.

Note that this seems to have changed recently. With `#define public_func_name strlen`; Clang 13 produces the same infinite recursion still. Clang 14 and 15 produce a bogus call to `jmp strlen.inline`, while current Clang 16 seems to do the right thing.

(Also, doing such things for `strlen` is a bit unexpected - `strlen` was picked just for simplicity for the code example. Actual uses of such patterns do arise for e.g. printf style functions together with `_FORTIFY_SOURCE`.)### compiler : `LLVM`
### title : `Miscompilation on i686 windows with opaque pointers + LTO`
### open_at : `2022-11-01T07:46:57Z`
### link : https://github.com/llvm/llvm-project/issues/58718
### status : `closed`
### tags : `miscompilation, ipo, release:backport, release:merged, `
### content : 
(For some reason, it doesn't happen outside LTO)
This function call: https://searchfox.org/mozilla-central/rev/2809416b216b498ec3d8b0e65c25a135f4f5f37d/js/src/frontend/Parser.cpp#537-538
(declaration in: https://searchfox.org/mozilla-central/rev/2809416b216b498ec3d8b0e65c25a135f4f5f37d/js/src/frontend/ErrorReporter.h#111-112)
ends up compiled as:
```asm
movl    %edi, 4(%ebx)
movl    %esi, (%ebx)
movl    12(%ebp), %ecx
movl    %ecx, 8(%ebx)
movl    $32, 12(%ebx)
movl    %eax, 16(%ebx)
movl    -56(%ebp), %eax
movl    %eax, 20(%ebx)
pushl   %ebx
calll   0x14f73040
```
(where `%ebx` has a copy of `%esp`)
The same code, compiled with opaque pointer disabled, is compiled as:
```asm
movl    %edi, 4(%ebx)
movl    %esi, (%ebx)
movl    12(%ebp), %ecx
movl    %ecx, 8(%ebx)
movl    $32, 12(%ebx)
movl    %eax, 16(%ebx)
movl    -56(%ebp), %eax
movl    %eax, 20(%ebx)
calll   0x14faf0a0
```
Note the `push` is not there.

At the IR level, it looks like this (with opaque pointers):
```ll
 %46 = alloca inalloca <{ ptr, %"class.mozilla::UniquePtr.84", i32, i32, ptr, ptr }>, align 4
  %47 = load ptr, ptr %7, align 4
  %48 = call noundef ptr @"?DeclarationKindString@frontend@js@@YAPBDW4DeclarationKind@12@@Z"(i8 noundef zeroext %2) #7
  %49 = getelementptr inbounds <{ ptr, %"class.mozilla::UniquePtr.84", i32, i32, ptr, ptr }>, ptr %46, i32 0, i32 1
  store ptr %25, ptr %49, align 4
  store ptr %0, ptr %46, align 4
  %50 = getelementptr inbounds <{ ptr, %"class.mozilla::UniquePtr.84", i32, i32, ptr, ptr }>, ptr %46, i32 0, i32 2
  store i32 %3, ptr %50, align 4
  %51 = getelementptr inbounds <{ ptr, %"class.mozilla::UniquePtr.84", i32, i32, ptr, ptr }>, ptr %46, i32 0, i32 3
  store i32 32, ptr %51, align 4
  %52 = getelementptr inbounds <{ ptr, %"class.mozilla::UniquePtr.84", i32, i32, ptr, ptr }>, ptr %46, i32 0, i32 4
  store ptr %48, ptr %52, align 4
  %53 = getelementptr inbounds <{ ptr, %"class.mozilla::UniquePtr.84", i32, i32, ptr, ptr }>, ptr %46, i32 0, i32 5
  store ptr %47, ptr %53, align 4
  call void (ptr, ...) @"?errorWithNotesAt@ErrorReportMixin@frontend@js@@QBAXV?$UniquePtr@VJSErrorNotes@@U?$DeletePolicy@VJSErrorNotes@@@JS@@@mozilla@@IIZZ"(ptr nonnull inalloca(<{ ptr, %"class.mozilla::UniquePtr.84", i32, i32, ptr, ptr }>) %46)
```
For some reason, after `GlobalOptPass`, the call is transformed to:
```ll
  call void (ptr, ...) @"?errorWithNotesAt@ErrorReportMixin@frontend@js@@QBAXV?$UniquePtr@VJSErrorNotes@@U?$DeletePolicy@VJSErrorNotes@@@JS@@@mozilla@@IIZZ"(ptr nonnull %46)
```
(it lost the `inalloca`)
and it's when starting to lower to assembly that the push is inserted, presumably because it now thinks it's calling the function as if `%46` was the first argument and the vararg was empty.

The reason it requires LTO is probably that LTO brings in the full declaration of `errorWithNotesAt` and that has an effect on the `Function` the passes see.

Cc: @nikic


---

CC @lhmouse


---

# 111
### compiler : `LLVM`
### title : `Miscompilation on i686 windows with opaque pointers + LTO`
### open_at : `2022-11-01T07:46:57Z`
### link : https://github.com/llvm/llvm-project/issues/58718
### status : `closed`
### tags : `miscompilation, ipo, release:backport, release:merged, `
### content : 
(For some reason, it doesn't happen outside LTO)
This function call: https://searchfox.org/mozilla-central/rev/2809416b216b498ec3d8b0e65c25a135f4f5f37d/js/src/frontend/Parser.cpp#537-538
(declaration in: https://searchfox.org/mozilla-central/rev/2809416b216b498ec3d8b0e65c25a135f4f5f37d/js/src/frontend/ErrorReporter.h#111-112)
ends up compiled as:
```asm
movl    %edi, 4(%ebx)
movl    %esi, (%ebx)
movl    12(%ebp), %ecx
movl    %ecx, 8(%ebx)
movl    $32, 12(%ebx)
movl    %eax, 16(%ebx)
movl    -56(%ebp), %eax
movl    %eax, 20(%ebx)
pushl   %ebx
calll   0x14f73040
```
(where `%ebx` has a copy of `%esp`)
The same code, compiled with opaque pointer disabled, is compiled as:
```asm
movl    %edi, 4(%ebx)
movl    %esi, (%ebx)
movl    12(%ebp), %ecx
movl    %ecx, 8(%ebx)
movl    $32, 12(%ebx)
movl    %eax, 16(%ebx)
movl    -56(%ebp), %eax
movl    %eax, 20(%ebx)
calll   0x14faf0a0
```
Note the `push` is not there.

At the IR level, it looks like this (with opaque pointers):
```ll
 %46 = alloca inalloca <{ ptr, %"class.mozilla::UniquePtr.84", i32, i32, ptr, ptr }>, align 4
  %47 = load ptr, ptr %7, align 4
  %48 = call noundef ptr @"?DeclarationKindString@frontend@js@@YAPBDW4DeclarationKind@12@@Z"(i8 noundef zeroext %2) #7
  %49 = getelementptr inbounds <{ ptr, %"class.mozilla::UniquePtr.84", i32, i32, ptr, ptr }>, ptr %46, i32 0, i32 1
  store ptr %25, ptr %49, align 4
  store ptr %0, ptr %46, align 4
  %50 = getelementptr inbounds <{ ptr, %"class.mozilla::UniquePtr.84", i32, i32, ptr, ptr }>, ptr %46, i32 0, i32 2
  store i32 %3, ptr %50, align 4
  %51 = getelementptr inbounds <{ ptr, %"class.mozilla::UniquePtr.84", i32, i32, ptr, ptr }>, ptr %46, i32 0, i32 3
  store i32 32, ptr %51, align 4
  %52 = getelementptr inbounds <{ ptr, %"class.mozilla::UniquePtr.84", i32, i32, ptr, ptr }>, ptr %46, i32 0, i32 4
  store ptr %48, ptr %52, align 4
  %53 = getelementptr inbounds <{ ptr, %"class.mozilla::UniquePtr.84", i32, i32, ptr, ptr }>, ptr %46, i32 0, i32 5
  store ptr %47, ptr %53, align 4
  call void (ptr, ...) @"?errorWithNotesAt@ErrorReportMixin@frontend@js@@QBAXV?$UniquePtr@VJSErrorNotes@@U?$DeletePolicy@VJSErrorNotes@@@JS@@@mozilla@@IIZZ"(ptr nonnull inalloca(<{ ptr, %"class.mozilla::UniquePtr.84", i32, i32, ptr, ptr }>) %46)
```
For some reason, after `GlobalOptPass`, the call is transformed to:
```ll
  call void (ptr, ...) @"?errorWithNotesAt@ErrorReportMixin@frontend@js@@QBAXV?$UniquePtr@VJSErrorNotes@@U?$DeletePolicy@VJSErrorNotes@@@JS@@@mozilla@@IIZZ"(ptr nonnull %46)
```
(it lost the `inalloca`)
and it's when starting to lower to assembly that the push is inserted, presumably because it now thinks it's calling the function as if `%46` was the first argument and the vararg was empty.

The reason it requires LTO is probably that LTO brings in the full declaration of `errorWithNotesAt` and that has an effect on the `Function` the passes see.

Cc: @nikic


---

# 112
### compiler : `LLVM`
### title : `Invalid object passed to coroutine's await_transform`
### open_at : `2022-10-23T10:28:30Z`
### link : https://github.com/llvm/llvm-project/issues/58556
### status : `open`
### tags : `platform:windows, coroutines, `
### content : 
compiler: clang-cl from main, target=i686-windows-msvc, c++ lib = libcxx

When running [this](https://github.com/chriskohlhoff/asio/blob/master/asio/src/examples/cpp20/coroutines/refactored_echo_server.cpp) example in debug mode [this](https://github.com/chriskohlhoff/asio/blob/master/asio/include/asio/impl/awaitable.hpp#L164) await_transform receives argument 'a' with invalid address, it was never created. With emit-llvm i can see that this argument has inalloca attribute. I thought it was a bug in asio, [here is related issue](https://github.com/chriskohlhoff/asio/issues/1141) in asio bug tracker.

https://github.com/4e4o/clang_cl_crash/blob/main/example2.cpp

---

# 113
### compiler : `LLVM`
### title : `rbp` clobber in inline assembly is not respected for functions with a frame pointer
### open_at : `2022-10-21T15:12:12Z`
### link : https://github.com/llvm/llvm-project/issues/58528
### status : `open`
### tags : `backend:X86, llvm:codegen, miscompilation, `
### content : 

인라인 어셈블리 코드에서 "rbp"를 clobbered list에 넣는 것은, 이 코드가 실행되는 동안 rbp 레지스터의 값이 변할 수 있다는 것을 컴파일러에게 알리는 것입니다. 즉, 컴파일러는 이 정보를 바탕으로 rbp 레지스터를 안전하게 다루어야 합니다.

그런데 문제는, 실제로 생성된 어셈블리 코드를 보면, 컴파일러가 rbp 레지스터의 값이 인라인 어셈블리 코드에 의해 변하지 않을 것이라고 가정하고 코드를 생성했다는 것입니다. 이로 인해, 만약 인라인 어셈블리 코드에서 rbp 레지스터를 변경한다면, 그 변경이 프로그램의 다른 부분에 영향을 미칠 수 있습니다.

간단히 말해, 프로그래머는 "주의해! rbp가 변할 수 있어!"라고 컴파일러에게 알렸지만, 컴파일러는 이를 무시하고 rbp가 변하지 않을 것이라고 가정한 코드를 생성한 것입니다. 이로 인해 버그가 발생할 수 있습니다.

https://godbolt.org/z/reM9vb8WP

https://godbolt.org/z/Er54MnxWc

The `rbp` register can be clobbered by inline assembly, like so:

```c
void simplenop(void) {
    asm volatile("nop" : : : "rbp");
}
```

This results in the following expected assembly:

```asm
simplenop():                          # @simplenop()
        push    rbp
        nop
        pop     rbp
        ret
```

However, when a frame pointer is forced, this clobber constraint is not respected:

```c
void buffernop(int size) {
    char buf[size];
    asm volatile("nop" : : "r"(buf): "rbp");
}
```

```asm
buffernop(int):                          # @buffernop(int)
        push    rbp
        mov     rbp, rsp
        mov     eax, edi
        mov     rcx, rsp
        add     rax, 15
        and     rax, -16
        sub     rcx, rax
        mov     rsp, rcx
        nop
        mov     rsp, rbp
        pop     rbp
        ret
```

As you can see, the generated code clearly expects the `rbp` to not be clobbered after the inline assembly.
Godbolt link: https://godbolt.org/z/osMEb1Kcj

This resulted in an actual bug in https://github.com/tinygo-org/tinygo/pull/3103#issuecomment-1287052017 where I try to call functions with a custom ABI via inline assembly.
Ideally the X86 backend should save the `rbp` register somewhere else (for example, on the stack: `rsp` is not clobbered) or just throw an error. Silently miscompiling results in bugs.`


---

# 114
### compiler : `LLVM`
### title : `Clang choosing copy constructor over initializer_list`
### open_at : `2022-10-21T08:48:52Z`
### link : https://github.com/llvm/llvm-project/issues/58520
### status : `open`
### tags : `c++, clang:frontend, confirmed, `
### content : 

https://godbolt.org/z/5rrxGj4EM

The following short program returns '3' with clang, but '30' with GCC and '12' with MSVC.
The issue is that in lines (3) and (4), both the copy-constructor (1) and the initializer_list constructor (2) could be called.
According to cppreference.com, (2) should be called.
However, clang chooses (1) on both instances. (Interestingly, MSVC chooses (2) on (3) and (1) on (4).

This error also accurs if the constructor of S takes an initializer_list of another type T, which can be implicitly contructed from S, this is how I encountered the bug in real code.

```c++
#include <initializer_list>

struct S {
    S() = default;
    S(const S& other): i_(1) {} // (1)
    S(const std::initializer_list<S> args): i_(10) {} // (2)

    int i_;
};

struct T {
    //Clang: calls (1)
    //GCC, MSVC: calls (2)
    T(const S& s) : s_{s} {}       // (3)

    S s_;
};

int main() {
    S s;
    T t(s);

    //Clang, MSVC: calls  (1)
    //GCC: calls (2)
    S s2{s};        // (4)

    return t.s_.i_ + 2*s2.i_;
}
```


---

# 115
### compiler : `LLVM`
### title : `[coroutines] incorrect transformation removes co_await side effects in non-taken branch`
### open_at : `2022-10-19T05:34:52Z`
### link : https://github.com/llvm/llvm-project/issues/58459
### status : `closed`
### tags : `miscompilation, coroutines, `
### content : 
Here is a simple program that contains a chain of two coroutines, with one awaiting the other. The awaiter returned by `await_transform` calls an external function (`SomeExternalFunc`) in its `await_suspend` method:

```c++
#include <coroutine>
#include <cstddef>

// A function defined in another translaiton unit.
void SomeExternalFunc();

struct MyTask{
  struct promise_type {
    MyTask get_return_object() { return {std::coroutine_handle<promise_type>::from_promise(*this)}; }
    std::suspend_always initial_suspend() { return {}; }

    void unhandled_exception();
    void return_void() {} 

    auto await_transform(MyTask task) {
      struct Awaiter {
        bool await_ready() { return false; }

        // Resume the lazy coroutine, first calling the external function.
        std::coroutine_handle<promise_type> await_suspend(std::coroutine_handle<promise_type> h) {
          callee.resume_when_done = h;
          SomeExternalFunc();
          return std::coroutine_handle<promise_type>::from_promise(callee);
        }

        // Clean up and then evaluate to null.
        std::nullptr_t await_resume() {
          std::coroutine_handle<promise_type>::from_promise(callee).destroy();
          return nullptr;
        }

        promise_type& caller;
        promise_type& callee;
      };

      return Awaiter{*this, task.handle.promise()};
    }
    
    // Resume the coroutine that started us when we're done.
    auto final_suspend() noexcept {
      struct Awaiter {
        bool await_ready() noexcept { return false; }
        std::coroutine_handle<promise_type> await_suspend(std::coroutine_handle<promise_type> h) noexcept {
          return to_resume;
        }

        void await_resume() noexcept;

        std::coroutine_handle<promise_type> to_resume;
      };

      return Awaiter{resume_when_done};
    }

    // The coroutine to resume when we're done.
    std::coroutine_handle<promise_type> resume_when_done;
  };

  // A handle for the coroutine that returned this task.
  std::coroutine_handle<promise_type> handle;
};

MyTask DoSomethingElse() {
  co_return;
}

// A coroutines that awaits a call to another.
MyTask DoSomething() {
  co_await DoSomethingElse();
  co_return;
}
```

When [compiled](https://godbolt.org/z/e9Mrz9hEa) with `-std=c++20 -O1`, this correctly generates a call to `SomeExternalFunc` from `DoSomething.resume`:

```asm
DoSomething() [clone .resume]:                # @DoSomething() [clone .resume]
[...]
        call    SomeExternalFunc()@PLT
[...]
```

However if we [change](https://godbolt.org/z/WGbdG9r8c) the `co_await DoSomethingElse();` statement to be a branch:

```c++
if (co_await DoSomethingElse() != nullptr) {}
```

then all mentions of `SomeExternalFunc` are gone from the [generated code](https://gist.github.com/jacobsa/c6f5515f4ed66c93aae56627279b91a6).

**I believe clang is wrong to eliminate this branch.** Although it's true that the branch can never be taken, evaluating the `co_await` expression may have a side effect through the call to `SomeExternalFunc`. (Indeed I found this bug because clang incorrectly removed such side effects in a real codebase.)`


---

# 116
### compiler : `LLVM`
### title : `Wrong code at -Os on x86_64-linux_gnu (LoopFlattenPass)`
### open_at : `2022-10-18T13:59:56Z`
### link : https://github.com/llvm/llvm-project/issues/58441
### status : `closed`
### tags : `miscompilation, loopoptim, `
### content : 
```cpp
% clang-tk -v
clang version 16.0.0 (https://github.com/llvm/llvm-project.git faf0e1fbf90f14a92042a83f6cb1239791674412)
Target: x86_64-unknown-linux-gnu
Thread model: posix
InstalledDir: /zdata/shaoli/compilers/ccbuilder-compilers
Found candidate GCC installation: /usr/lib/gcc/x86_64-linux-gnu/11
Found candidate GCC installation: /usr/lib/gcc/x86_64-linux-gnu/9
Selected GCC installation: /usr/lib/gcc/x86_64-linux-gnu/11
Candidate multilib: .;@m64
Selected multilib: .;@m64
%
% clang-tk -w -O0 a.c && ./a.out
6
% clang-tk -w -Os a.c && ./a.out
1
% cat a.c
void printf();
int c;
int a(int b) {
    int t = 0;
    while (t < 7 && b) t++;
    return t;
}
int e() {
    int l;
    for (l = 0; l < 6; l = l + 1)
        for (c = 0; c < 6; c = (a(6) ^ 7) + c + 1)
            ;
}
int main() {
    e();
    printf("%d\n", c);
}
%
```
Compiler explorer: https://godbolt.org/z/x1jvrPj9a
`opt-bisect-limit` suggests that the issue might be in `LoopFlattenPass`.`


---

# 117
### compiler : `LLVM`
### title : `fno-semantic-interposition breaks code relying on address uniqueness of a function`
### open_at : `2022-10-11T16:25:38Z`
### link : https://github.com/llvm/llvm-project/issues/58295
### status : `open`
### tags : `clang:codegen, `
### content : 
```cpp
// a.cpp
#include <functional>
#include <cassert>
int foo(int x) { return x + 42; }

bool bar(std::function<int(int)> F) {
  auto f = F.target<int(*)(int)>();
  return f && *f == foo;
}
```
```cpp
// b.cpp
#include <functional>
int foo(int x);

bool bar(std::function<int(int)> F);

int main() {
  return bar(foo);
}
```
```bash
$ /usr/bin/clang++ -std=c++17 -fPIC -fno-semantic-interposition a.cpp -shared -o liba.so
$ /usr/bin/clang++ -std=c++17 b.cpp -L. -la
$ LD_LIBRARY_PATH=. ./a.out ; echo $?
0
$ /usr/bin/clang++ -std=c++17 -fPIC a.cpp -shared -o liba.so
$ LD_LIBRARY_PATH=. ./a.out ; echo $?
1
```

GCC is consistent with/without the option.

I'm not sure if that is a bug or desired behavior, but https://gcc.gnu.org/bugzilla/show_bug.cgi?id=100483#c2 suggests that the case above doesn't use *semantic* interposition and so should work with the option. I'm not unlikely to misread/misunderstand it though.


---

# 118
### compiler : `LLVM`
### title : `clang: x86 stdcall/thiscall with an empty object parameter yields ABI-incompatible code`
### open_at : `2022-10-09T23:46:01Z`
### link : https://github.com/llvm/llvm-project/issues/58255
### status : `open`
### tags : `backend:X86, clang:codegen, ABI, `
### content : 
Reproducer: https://godbolt.org/z/4havqnxxj

Note the difference of `ret` operand for `T::x` -- gcc returns by 12 where clang returns by 8, and each caller computes the stack size for the respective return size. It's easy to see that if you try to mix the code generated between two the stack gets corrupted and the program crashes. Changing thiscall to stdcall yields a similar result, just with `this` added to the parameter size for each.

My concrete case involves a 32 bit mingw app which [defaults the member functions to thiscall](https://github.com/llvm/llvm-project/blob/fee8f561bdc9317eee13b8f1866ca0dc778c1dc5/clang/lib/AST/ItaniumCXXABI.cpp#L239). The program immediately crashes as soon as it tries to copy a single `std::string` when built with -O0.`


---

# 119
### compiler : `LLVM`
### title : `Wrong code at -Os on x86_64-linux_gnu`
### open_at : `2022-10-07T09:00:55Z`
### link : https://github.com/llvm/llvm-project/issues/58223
### status : `closed`
### tags : `miscompilation, llvm:optimizations, `
### content : 
```console
% clang-tk -v
clang version 16.0.0 (https://github.com/llvm/llvm-project.git 0c1a3da8ea1f0e024ebfd85c7532926f26c6bde5)
Target: x86_64-unknown-linux-gnu
Thread model: posix
InstalledDir: /zdata/shaoli/compilers/ccbuilder-compilers
Found candidate GCC installation: /usr/lib/gcc/x86_64-linux-gnu/11
Found candidate GCC installation: /usr/lib/gcc/x86_64-linux-gnu/9
Selected GCC installation: /usr/lib/gcc/x86_64-linux-gnu/11
Candidate multilib: .;@m64
Selected multilib: .;@m64
%
% clang-tk -w -O0 a.c && ./a.out
1
% clang-tk -w -Os a.c && ./a.out
0
%
% cat a.c
void printf();
int a = 1;
int *b = &a, *c = &b;
short d;
char e, f = 1;
static int *g = &a;
static int ***h = &c;
char *i = &f;
static char *j = &e;
long k;
short l[1];
short *m;
int main() {
  int ***n = &c;
  m = l;
  for (;;) {
    d = 0;
    for (; d <= 1; d++) {
      k = ***n;
      if (m)
        *g = *j = 0;
    }
    ***n && (*i = 0);
    if (**h)
      break;
  }
  printf("%d\n", f);
}
%
```
Compiler explorer: https://godbolt.org/z/z8Gnz514T

I have reported another bug before :https://github.com/llvm/llvm-project/issues/58140, but I don't think they are the same after I did `opt-bisect-limit`.`


---

# 120
### compiler : `LLVM`
### title : `Clang accepts invalid narrowing conversion`
### open_at : `2022-10-06T15:55:51Z`
### link : https://github.com/llvm/llvm-project/issues/58200
### status : `closed`
### tags : `c++17, clang:frontend, accepts-invalid, `
### content : 
The following invalid program is accepted by x86-64 clang 13.0.1 with C++17. [Demo](https://godbolt.org/z/hso9rG7as). 

```
void f() noexcept(5) //compiles with x86-64 clang 13.0.1 with C++17
{

}
```


---


# 121
### compiler : `LLVM`
### title : `[clang++] Clang-15 vs Clang-14 local static init guards`
### open_at : `2022-10-06T11:33:16Z`
### link : https://github.com/llvm/llvm-project/issues/58184
### status : `closed`
### tags : `clang:codegen, `
### content : 
I'm using Clang++ to compile for a Cortex-M0+ target, and in moving from version 14 to version 15 I've found a difference in the code generated for guard variables for local statics.

So, for example:
```cpp
int main()
{
    static knl::QueueN<uint32_t, 8> valQueue;
    ...
}
```
Clang-14 generates the following:
```asm
ldr r0, .LCPI0_4
ldrb    r0, [r0]
dmb sy
lsls    r0, r0, #31
beq .LBB0_8
```
Clang-15 now generates:
```asm
ldr r0, .LCPI0_4
movs    r1, #2
bl  __atomic_load_1
lsls    r0, r0, #31
beq .LBB0_8
```

An important consequence of this is that the second case actually requires an implementation of `__atomic_load_1` to be provided from somewhere external to the compiler (e.g. `-latomic`?), whereas the first doesn't.  

Note that the source code doesn't explicitly use atomics, only the implied usage by the statics (which can of course be disabled with `-fno-threadsafe-statics`).


---