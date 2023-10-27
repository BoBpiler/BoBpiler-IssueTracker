## LLVM 목차

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
16. [[C++17][clang:Frontend] Clang can't deduce the correct deduction guide.(컴파일 실패)](#16)
17. [Out of Line Definition Error for Constrained Function of Template Class (컴파일 실패)](#17)
18. [abs from cmath is not constexpr when it should be [C++23]](#18)
19. [Clang crash: Assertion DT.dominates(RHead, LHead) && "No dominance between recurrences used by one SCEV?"' failed. (컴파일 실패)](#19)
20. [Worse code gen when integer is wrapped in struct (컴파일러 버그)](#20)
21. [Clang cuda functions not handling concepts correctly. (컴파일 실패)](#21)
22. [odd code generated for swapping... (컴파일 실패)](#22)
23. [clang places calls to operator delete even for noexcept constructors (컴파일 실패)](#23)
24. [Assertion failure with constrained parameter referring to previous parameter (컴파일 실패)](#24)
25. [Wrong code at -O2 on x86_64-linux_gnu since ddfee6d (recent regression) (컴파일러 버그)](#25)
26. [[X86] Musttail calls involving unions with long double members are miscompiled at -O2 (컴파일러 버그)(이거 뭔가 취약점으로 잘 쓸수 있을지도 !)](#26)
27. [](#27)
28. [](#28)
29. [](#29)
30. [](#30)
31. [](#31)
32. [](#32)
33. [](#33)
34. [](#34)
35. [](#35)

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

```console
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
````


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