

# Seif 백엔드 API 개발

## 개요
**Seif 앱** 백엔드는 시설 안전 관리 강화를 위한 **중대재해처벌법** 준수를 지원하기 위해 개발되었습니다. 이 앱은 시설 점검 프로세스를 간소화하고, 안전 보고서를 자동화하며, 점검 완료된 조직의 세부 보고서를 생성 및 다운로드할 수 있도록 지원하여 법적 준수를 보장합니다.

## 주요 기능
- **API 개발**: 프론트엔드와 원활히 연동되는 백엔드 API를 설계하고, Swagger를 통해 명확하고 사용하기 쉬운 문서를 제공.(drf_spectacular)
- **자동 보고서 생성**: `openpyxl`을 사용해 점검 결과를 요약한 Excel 보고서를 자동으로 생성하여 클릭 한 번으로 문서를 준비.
- **Django 프레임워크**: 확장 가능하고 안전한 서비스 기반을 제공하는 Django를 활용해 백엔드 개발.

## 핵심 기술
- **Python**: 백엔드 개발에 사용된 주요 프로그래밍 언어.
- **Django**: 확장 가능하고 유지보수가 용이한 백엔드 API 구축을 위한 핵심 프레임워크.
- **Swagger**: API 문서화를 통해 개발자가 엔드포인트를 쉽게 이해하고 활용 가능하도록 지원.
- **Openpyxl**: 자동화된 Excel 보고서 생성 기능 제공.
- **JWT 인증**: 사용자 데이터를 안전하게 보호하기 위해 백엔드는 JSON Web Token(JWT)을 인증 수단으로 사용합니다. 사용자가 로그인하면 토큰이 생성되어 클라이언트로 전송됩니다. 이후 모든 API 요청에는 이 토큰이 필요하며, 이를 통해 인증된 사용자만 보호된 엔드포인트에 접근할 수 있습니다. 토큰은 사용자별 클레임을 포함하며, 변조를 방지하기 위해 안전하게 서명됩니다. 보안 강화를 위해 토큰 만료 및 갱신 정책도 구현되어 있습니다.
![image](https://github.com/user-attachments/assets/30a0cf67-e976-432c-bb47-265f85d7d95a)


![image](https://github.com/user-attachments/assets/aa8bf9cc-3294-4c97-9a3c-2ebe87587cbc)

## 설명서
[관리자용 설명서.pdf](https://github.com/user-attachments/files/18137437/default.pdf)

[담당자용 사용설명서.pdf](https://github.com/user-attachments/files/18137438/default.pdf)

[대표자용 설명서.pdf](https://github.com/user-attachments/files/18137439/default.pdf)

[책임자용사용설명서.pdf](https://github.com/user-attachments/files/18137440/default.pdf)

[설명서_전체_ver01.pdf](https://github.com/user-attachments/files/18137441/_._ver01.pdf)

[출력설명_ver02.pdf](https://github.com/user-attachments/files/18137442/_ver02.pdf)
