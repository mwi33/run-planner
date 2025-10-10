# FEATURE-001 — Run Plans v1 (Create & Retrieve)
**Owner:** TBD  
**Status:** Ready for Dev  
**Linked Issue:** #TBD  
**Flag:** `RUN_PLANS_V1` (default OFF)

## 1) Context / Problem
Race engineers need a fast, reproducible way to turn basic run inputs (car, track, weather, driver, objective, laps/pace, fuel burn) into a computed plan (laps possible, total fuel required, pit/refuel need, timings) and to persist that plan.

## 2) Outcomes / Success Criteria
- Can POST a run plan and receive computed fuel/time metrics.
- Plan is persisted and retrievable by ID.
- Basic validation prevents impossible runs (negative/NaN, contradictory inputs).
- Computation is deterministic (same inputs → same outputs).
- Rollback path exists (DB migration reverses cleanly; feature can be toggled off).

## 3) User Stories
- As a race engineer, I can create a run plan from car/track/weather inputs and target pace so I know fuel needs and feasibility.
- As a race engineer, I can retrieve a stored plan by ID to review or share.

## 4) Acceptance Criteria (Given/When/Then)
- **Create success**
  - Given valid inputs with `required_laps`, when I POST `/run-plans`, then I receive `201` with `{id, inputs, result}` including `total_fuel_required_l`, `laps_possible`, `pit_stops_required`.
- **Create by duration**
  - Given valid inputs with `run_duration_min` and `target_pace_s`, when I POST, then the server infers `estimated_laps = floor(run_duration_min*60 / target_pace_s)` and computes fuel accordingly.
- **Retrieve**
  - Given a valid plan ID, when I GET `/run-plans/{id}`, then I receive the persisted inputs and computed result exactly as returned at creation time.
- **Validation**
  - Given invalid inputs (e.g., negative laps, missing burn + no way to infer it), when I POST, then I receive `422` with field errors.
- **Idempotency**
  - Given the same request payload, when I POST twice, then two plans may be created (v1 is not a deduping API).

## 5) Scope / Non-Goals
**In:** single-run planning; single/multi-stint inference limited to fuel-only logic; persistence; simple validation; JSON API.  
**Out (v1):** tyre degradation modeling, weather evolution, driver swaps, pit timing windows, UI, auth/multi-tenancy, advanced strategy optimization.

## 6) Data / Schema Changes
Create `run_plans` table (Postgres recommended).

Proposed (normalized-enough) schema:
- `id` UUID PK (server generated)
- `title` TEXT NULL
- `objective` TEXT NULL (e.g., "baseline", "tyre_life_test", "qualy_long_run", "practice_run")
- `inputs` JSONB NOT NULL — validated at API boundary (see OpenAPI)
- `result` JSONB NOT NULL — computed fields (see below)
- `status` VARCHAR(20) NOT NULL DEFAULT 'computed'
- `created_at` TIMESTAMPTZ NOT NULL DEFAULT now()
- `updated_at` TIMESTAMPTZ NOT NULL DEFAULT now()

Indexes:
- `idx_run_plans_created_at` (BTREE)
- `idx_run_plans_inputs_gin` (GIN on `inputs`)
- `idx_run_plans_result_gin` (GIN on `result`) — optional

**Alembic:** one forward migration creating table + indexes; one-step downgrade drops them. Use SQLAlchemy UUID with server_default via `gen_random_uuid()` (pgcrypto) or application-side `uuid.uuid4()` if extension not available.

## 7) API / UI Notes
- Spec at `docs/api/run-plans.yaml`
- Endpoints (v1):
  - `POST /run-plans` — create & compute
  - `GET /run-plans/{id}` — retrieve
- Authentication: none (v1, local/staging only). Add auth in a future feature.
- Content type: `application/json` UTF-8.

## 8) Computation (Working Spec)
Inputs (minimum viable):
- `required_laps` **or** `run_duration_min`
- `target_pace_s` (seconds per lap) — required if `run_duration_min` provided
- `fuel_burn_l_per_lap` — required unless a separate inference module exists (v1: required)
- `starting_fuel_l` — optional (defaults to `tank_capacity_l` if provided, else equals `total_fuel_required_l` in v1)
- Optional context: `car.tank_capacity_l`, `track.length_km`, `track.pit_lane_loss_s`, `weather.*`, `driver.name`

Derived:
- If `required_laps` given:  
  `total_fuel_required_l = required_laps * fuel_burn_l_per_lap`
- If `run_duration_min` given:  
  `estimated_laps = floor((run_duration_min * 60) / target_pace_s)`  
  `total_fuel_required_l = estimated_laps * fuel_burn_l_per_lap`
- Single-stint feasibility (if `tank_capacity_l` present):  
  `laps_possible = floor(starting_fuel_l / fuel_burn_l_per_lap)`  
  `pit_stops_required = 0 if total_fuel_required_l <= tank_capacity_l else ceil(total_fuel_required_l / tank_capacity_l) - 1`
- Time estimates:  
  `estimated_total_time_s = (required_laps or estimated_laps) * target_pace_s` (if `target_pace_s` given)

Result payload (v1):
```json
{
  "estimated_laps": 25,
  "total_fuel_required_l": 63.0,
  "laps_possible": 22,
  "pit_stops_required": 1,
  "stints": [
    { "stint_no": 1, "laps": 22, "fuel_start_l": 60.0, "fuel_end_l": 60.0 - 22*2.7, "refuel_l": 0.0 },
    { "stint_no": 2, "laps": 3,  "fuel_start_l": 10.0, "fuel_end_l": 10.0 - 3*2.7,  "refuel_l": 10.0 }
  ],
  "estimated_total_time_s": 2265.0,
  "notes": []
}
```

## 9) Validation Rules (v1)
- `required_laps` ≥ 1 if provided.

- `run_duration_min` ≥ 1 if provided.

- One of `required_laps` or `run_duration_min` must be provided.

- `fuel_burn_l_per_lap` > 0.

- If `run_duration_min` provided, `target_pace_s` > 0.

- `starting_fuel_l` ≥ 0 if provided.

- If `tank_capacity_l` provided, must be ≥ `starting_fuel_l`.

## 10) Test Plan
### Unit:
- Fuel calc with `required_laps`.
- Duration→laps inference and rounding.
- Stint feasibility with/without `tank_capacity_l`.
- Validation error on missing/invalid fields.
### Integration (API):
- POST happy path returns 201 + expected structure.
- POST invalid returns 422 + field messages.
- GET by valid ID returns the created resource.
- GET unknown ID returns 404.
### Regression:
Alembic `upgrade head` & `downgrade -1` on disposable DB.
## 11) Rollout / Ops
- Feature behind `RUN_PLANS_V1` flag (config/env). Default OFF.
- CI runs tests + migration.
- Staging deploy: flag ON for smoke; Prod deploy: flag OFF until ready.
- Rollback: turn flag OFF, `alembic downgrade -1` if the DB change must be reverted; redeploy previous image tag.
## 12) Observability / Metrics / Logs
- Logs: create + retrieve attempts, validation failures, computed totals.
- Metrics (names TBD): `run_plan.create.success`, `run_plan.create.validation_error`, `run_plan.create.duration_ms`.
- Health: no new endpoint; reuse app healthcheck.
## 13) Security / Permissions
- v1: no auth; local/staging use. Validate & sanitize all inputs. No raw SQL.
## 14) Open Questions / Future
Multi-driver constraints, tyre model coupling, auth & tenancy, richer pit modeling, UI flows.