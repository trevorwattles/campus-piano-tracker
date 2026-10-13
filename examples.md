# More Examples

More runs from `run_eval.py` (`gpt-4o-mini`, temperature 0). Each one shows the question, the SQL, the rows and the friendly answer. When the strategies disagreed, I show the difference. I checked every verdict by hand against `setupData.sql`. Full output is in `results/`.

---

## 1. Which pianos have never been tuned? ✅ (all three)

```sql
SELECT p.brand, p.model, p.serial_number
FROM piano p
LEFT JOIN tuning t ON p.piano_id = t.piano_id
WHERE t.tuning_id IS NULL;
```
**Rows**: `[('Yamaha','P-125','YM-D77120'), ('Steinway & Sons','Model M','ST-071122'), ('Roland','FP-30X','RL-D55671')]`

**Answer**: The pianos that have never been tuned are a Yamaha P-125, a Steinway & Sons Model M, and a Roland FP-30X.

Correct. These are the two digital pianos and the one in storage. (Single-domain had this exact question as one of its examples, so it wasn't really a test for that strategy.)

---

## 2. Which technicians are not certified, and which pianos did they tune? ✅ (all three)

```sql
SELECT t.name AS technician_name, p.brand AS piano_brand, p.model AS piano_model, tu.tuning_date
FROM technician t
JOIN tuning tu ON t.technician_id = tu.technician_id
JOIN piano p ON tu.piano_id = p.piano_id
WHERE t.is_certified = 0;
```
**Answer** (zero-shot): The technician who is not certified is Tom Alvarez. He tuned: Baldwin Hamilton on May 14, 2024; Young Chang G-157 on November 2, 2025; Baldwin Acrosonic on September 9, 2023.

Correct. It read the `-- 1 = Registered Piano Technician, 0 = not` comment in the schema and used `is_certified = 0`.

---

## 3. How many pianos are in each building? ✅ (all three)

```sql
SELECT b.name AS building_name, COUNT(p.piano_id) AS piano_count
FROM building b
LEFT JOIN room r ON b.building_id = r.building_id
LEFT JOIN piano p ON r.room_id = p.room_id
GROUP BY b.building_id, b.name;
```
**Answer**: Harris Fine Arts Center: 6, Wilkinson Student Center: 2, Harold B. Lee Library: 1, Joseph Smith Building: 2, Brimhall Building: 2.

Correct, and all three strategies wrote identical SQL. It used `LEFT JOIN`s, so a building with zero pianos would still show up.

---

## 4. Which students have reserved a piano that currently needs repair? ✅ (all three)

```sql
SELECT s.name AS student_name, s.email AS student_email, p.brand AS piano_brand, p.model AS piano_model
FROM reservation r
JOIN piano p ON r.piano_id = p.piano_id
JOIN student s ON r.student_id = s.student_id
WHERE p.status = 'needs repair';
```
**Answer**: Ben Okafor has reserved a Yamaha U1 piano that currently needs repair.

Correct. This is a 3-table join through the reservation table.

---

## 5. Which pianos are in storage? ✅ (all three)

```sql
SELECT p.brand, p.model, p.piano_type, p.serial_number, p.year_made, p.status
FROM piano p
WHERE p.room_id IS NULL;
```
**Answer**: The only piano in storage is a Steinway & Sons Model M baby grand, serial number ST-071122, made in 1989, and it is retired.

Correct. The word "storage" doesn't appear anywhere in the data. The model got it purely from my schema comment `-- NULL means the piano is in storage`. Schema comments are worth writing!

---

## 6. Which students have reported more than one repair request? ✅ (all three)

```sql
SELECT s.student_id, s.name, COUNT(rr.request_id) AS request_count
FROM student s
JOIN repair_request rr ON s.student_id = rr.student_id
GROUP BY s.student_id, s.name
HAVING COUNT(rr.request_id) > 1;
```
**Rows**: `[]`

**Answer**: No matching records were found.

Correct. Every student has filed exactly one request. The SQL (`GROUP BY` + `HAVING`) is right. The answer is technically accurate but it reads exactly like the *wrong* empty answers elsewhere (see the Steinway question in the post), so you can't tell a real "none" from a bad query.

---

## 7. Which pianos need repair, and where are they? ✅ zero-shot / cross-domain, ❌ single-domain

**Cross-domain (correct)**:
```sql
SELECT p.brand, p.model, r.room_number, b.name AS building_name
FROM piano p
JOIN room r ON p.room_id = r.room_id
JOIN building b ON r.building_id = b.building_id
WHERE p.status = 'needs repair';
```
**Answer**: A Yamaha U1 in room C-302 of the Harris Fine Arts Center and a Baldwin Hamilton in the Lobby of the Wilkinson Student Center.

**Single-domain (wrong)**:
```sql
SELECT p.piano_id, p.brand, p.model, r.room_number, b.name AS building_name
FROM piano p
JOIN repair_request rr ON p.piano_id = rr.piano_id
JOIN room r ON p.room_id = r.room_id
JOIN building b ON r.building_id = b.building_id
WHERE rr.status != 'resolved' AND rr.reported_date <= '2026-10-12';
```
**Answer**: 1. Yamaha U1 in room C-302 … 3. **Young Chang in room G-157**, Joseph Smith Building …

It used unresolved repair requests instead of `piano.status`, so it listed 4 pianos (one of them twice). Then the answer step mixed up columns: G-157 is the Young Chang's *model*, not a room (it's actually in B-101). That's two separate mistakes in one question.

---

## 8. Which piano has the most open repair requests? ⚠️ (all three, partly right)

```sql
SELECT p.brand, p.model, COUNT(rr.request_id) AS open_requests
FROM piano p
JOIN repair_request rr ON p.piano_id = rr.piano_id
WHERE rr.status = 'open'
GROUP BY p.piano_id
ORDER BY open_requests DESC
LIMIT 1;
```
**Answer**: The piano with the most open repair requests is a Young Chang G-157, with 1 open request.

Misleading. Three pianos are tied at 1 open request (Yamaha U1, Baldwin Hamilton, Young Chang), and `LIMIT 1` hides the tie. Also, if you count `'in progress'` requests as open, the Yamaha U1 has 2 and is the clear answer. No strategy thought about either issue.

---

## 9. Can I reserve a piano in the Brimhall Building? ✅ cross-domain, ❌ zero-shot / single-domain

**Cross-domain (reasonable)**: it looked for active pianos in Brimhall with no reservation today, using `NOT EXISTS`.

**Answer**: Yes, you can reserve a piano in the Brimhall Building. There is an active piano available in room 120.

**Zero-shot (wrong)**:
```sql
... WHERE b.name = 'Brimhall Building'
  AND res.start_time > '2026-10-12'
  AND res.end_time < '2026-10-12';
```
This filter can never be true (a reservation can't start after it ends). It returned no rows, and the answer was "No matching records were found."

**Single-domain (wrong)**: it copied the `b.abbreviation = 'HFAC'` pattern from its example and guessed `'BB'`. The real abbreviation is `'BRMB'`, so it returned no rows and "No matching records were found."

The question is vague (reserve *when*?). Only cross-domain turned it into something sensible.
