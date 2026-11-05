import pandas as pd
import numpy as np

# ===== 설정: 본인 파일 경로로 수정 =====
FILE_PATH = "파일명.csv"

# ===== 1. 데이터 불러오기 =====
# 한글 CSV는 인코딩 문제가 잦아서 utf-8 실패 시 cp949로 다시 시도
try:
    df = pd.read_csv(FILE_PATH, encoding="utf-8")
    print("인코딩: utf-8")
except UnicodeDecodeError:
    df = pd.read_csv(FILE_PATH, encoding="cp949")
    print("인코딩: cp949")

# ===== 2. 기본 구조 확인 =====
print("\n[행, 열 개수]", df.shape)
print("\n[컬럼명과 자료형]")
print(df.dtypes)
print("\n[상위 5행]")
display(df.head())  # Jupyter/Colab에서는 display, 일반 파이썬이면 print

# ===== 3. 결측치와 중복 확인 =====
print("\n[결측치 개수 (0보다 큰 컬럼만)]")
missing = df.isnull().sum()
print(missing[missing > 0] if (missing > 0).any() else "결측치 없음")
print("\n[완전히 동일한 중복 행 개수]", df.duplicated().sum())

# ===== 4. 핵심 컬럼 후보 찾기 =====
# 컬럼명에 특정 단어가 들어간 것을 자동으로 찾아 보여줌 (실제 컬럼명은 눈으로 확인할 것)
def find_cols(keywords):
    return [c for c in df.columns if any(k in str(c) for k in keywords)]

print("\n[분기/기준 시점 후보]", find_cols(["분기", "기준", "년월", "연도"]))
print("[자치구/지역 후보]", find_cols(["자치구", "구", "지역", "행정동"]))
print("[업종 후보]", find_cols(["업종"]))
print("[매출액 후보]", find_cols(["매출금액", "매출액", "매출"]))

# ===== 5. 분기, 자치구, 업종 고유값 확인 =====
# 위 후보를 보고 실제 컬럼명을 아래에 입력한 뒤 사용
QUARTER_COL = None   # 예: "기준_년분기_코드"
DISTRICT_COL = None  # 예: "자치구_코드_명"
INDUSTRY_COL = None  # 예: "서비스_업종_코드_명"
SALES_COL = None     # 예: "당월_매출_금액"

if all([QUARTER_COL, DISTRICT_COL, INDUSTRY_COL, SALES_COL]):
    print("\n[분기 고유값]", sorted(df[QUARTER_COL].unique()))
    print("[자치구 수]", df[DISTRICT_COL].nunique())
    print("[업종 수]", df[INDUSTRY_COL].nunique())

    # 같은 (분기, 자치구, 업종)이 여러 행인지 확인 (2단계 라벨 계산 전에 꼭 필요)
    key_dup = df.duplicated(subset=[QUARTER_COL, DISTRICT_COL, INDUSTRY_COL]).sum()
    print("[(분기, 자치구, 업종) 키 중복 행 개수]", key_dup)

    # 매출액 기초통계와 0값 개수
    print("\n[매출액 기초통계]")
    print(df[SALES_COL].describe())
    print("[매출액 0 이하 행 개수]", (df[SALES_COL] <= 0).sum())
else:
    print("\n※ 위 후보를 참고해 QUARTER_COL, DISTRICT_COL, INDUSTRY_COL, SALES_COL을 채운 뒤 다시 실행하세요.")
