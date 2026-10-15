# Complete source-bank recipe mapping

Each row preserves one original full value; forward/reverse profiles are selected intact. Unrated q-59295 has an independently inferred key only, never a captured key.

## q-102200

| Original answer UUID | Exact full value | Type | Parameterized recipe |
|---|---|---|---|
| 1b3d8a45-fe13-581e-9e3f-055e9482e906 | `[-10,3)` | :answer.type/math | include lower/exclude upper |
| 2eee8041-f4fa-545a-a3f7-4d63c35b6ba8 | `(-10,3)` | :answer.type/math | exclude both |
| 3dacba62-f7cd-5fb4-b7ac-b6a55cdc2a73 | `(-10,3]` | :answer.type/math | exclude lower/include upper |
| 982b05bc-9e84-5fbb-95ab-465cc3b39a18 | `(-\infty ,3]` | :answer.type/math | drop lower bound and include upper |
| b9d2aab1-6872-5e77-8697-9067584fdf64 | `[-10,3]` | :answer.type/math | include both (source key) |

## q-59295

| Original answer UUID | Exact full value | Type | Parameterized recipe |
|---|---|---|---|
| 8f4fcf20-b761-5c35-9cb9-bc13442a9247 | `-2 \le x < 1` | :answer.type/math | include lower/exclude upper |
| 294058c7-dbb2-5a13-b2a1-2c9f829d7bfb | `-2 < x < 1` | :answer.type/math | exclude both |
| 29ba0508-5e1c-5e13-bfd5-eb18298c3eda | `-2 < x \le 1` | :answer.type/math | exclude lower/include upper |
| 2a3384f8-cacb-59a2-bba4-1fe80c835cd5 | `-2 \le x \le 1` | :answer.type/math | include both (supported inferred key) |
| 7eb49550-8e55-5c30-a78d-936a6b38052c | `$x < - 2$ or $x > 1$` | :answer.type/text | strict outside rays: v<a or v>b |

## q-154728

| Original answer UUID | Exact full value | Type | Parameterized recipe |
|---|---|---|---|
| 75a68108-a8cc-5fb7-90d8-d305c41c4fae | `-7<x\le 0` | :answer.type/math | exclude lower/include upper |
| 943f78de-1311-5dd7-ac1a-856ec0cb4c99 | `-7\le x\le 0` | :answer.type/math | include both (source key) |
| a18f6b94-6b53-545a-a37a-bd11450bb699 | `-7\le x<0` | :answer.type/math | include lower/exclude upper |
| a3a2c334-25f5-5b4f-b754-81cc023155a0 | `-7<x<0` | :answer.type/math | exclude both |
| aefb8691-5a94-57f6-a7c9-d4669ca141d5 | `$x\le -7$ or $x\ge 0$` | :answer.type/text | inclusive outside rays: v≤a or v≥b |

