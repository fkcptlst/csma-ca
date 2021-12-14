# CSMA/CA

## Usage

```bash
$ pip install -r requirements.txt
$ python3 main.py
```

## Configuration

config.env

```
STATION_COUNT=4
STATION_FRAME_PROBABILITY=0.05
STATION_DETECT_RANGE=25

AREA_SIZE=50

FRAME_SIZE=800
FRAME_RATE=300

BACKOFF_MINIMUM=4
BACKOFF_MAXIMUM=1024

TIMELINE_INTERVAL=0.05

STAR_TOPOLOGY=False
USE_RTS_CTS=True
```

## Example

4 Stations with star topology

```
- - - - - - - - - - - - -
                          - - -
- - - - - - - - - - - -         - -
-                       - - -     - -
                              - -     - 1
- - - - - - - - - - - -           -       - -
-                       - - -       - -     -
  - - - - - - - - - -         - -       - -   - -
-                     - - -     - -       -     -
                            - -     -       -     -
  - - - -   - - - - -         - -     - -     -     █D
-                     - -         -     -       █D0*- -
    - - -   - - - -       - -       - -   -       -   -                                     3
- -                 - -       - -     -     █D    -     -
-                       - -     -       █D    -     -   -
    - - -   - - - -         - -   -     -     -     -     -
- -                 - -       -     █D    -     -     -   -
-   - - - - - - - -     -       █D    -     -   -     -   -
  -                 -     -     -     -     -   -     -     -
-                     -     █D    -   -       -   -     -   -
-     - - - - - -       █D  -     -     -     -   -     -   -
-   -             -     -     -     -   -     -   -     -   -
  -     - - - -     █D    -   -     -   -     -   -     -   -
  -   -         █D  -     -   -     -   -     -   -     -   -
  -   -         -   -     -   -         -     -   -     -   -
  -   -     2*  -   -     -   -     -   -     -   -     -   -
  -   -         -   -     -   -     -   -     -   -     -   -
  -     -   - -     -     -   -     -   -     -   -     -   -
    -             -       -   -     -   -     -   -     -   -
-     - -     - -       -   -     -     -     -   -     -   -
-           -         -     -     -   -     -     -     -   -
  - -             - -     -     -     -     -     -   -     -
-     - - - - - -       -       -     -     -   -     -   -
- -                 - -       -     -     -   - -     -   -
    - - -     - - -         - -   -       -   -     -   - -
-           -           - -     -       -   -       -   -

[time]              33.88ms

[wasted]            0.00ms
[throughput]        850.18 kbps
[throughput rate]   ███████░░░░░░░░░░░░░ 39.36% 850.18/2160.00

[wasted]            0.00ms
[throughput]        0.00 kbps
[throughput rate]   ░░░░░░░░░░░░░░░░░░░░ 0.00% 0.00/2160.00

[collision rate]    ██████████████░░░░░░ 72.73% 8/11
[on air frames]      1

[node details]
  ID |   send-queue |   recv-queue | col |                        sending |                      receiving |     detected |  backoff |     difs |     sifs |  timeout |      nav | allocate |
[ 0] | ░░░░░░░░░░░░ | █D░░░░░░░░░░ |   0 |                                | █████████████████░░░ 87.75%    |  DATA 2 -> 0 |        0 |        0 |        0 |      791 |          |          |
[ 1] | █R░░░░░░░░░░ | ░░░░░░░░░░░░ |   3 |                                |                                |  DATA 2 -> 0 |     2750 |      450 |        0 |          |     4466 |          |
[ 2] | █D░░░░░░░░░░ | ░░░░░░░░░░░░ |   2 | ██████████████████░░ 94.50%    |                                |              |        0 |        0 |        0 |     4791 |          |     7741 |
[ 3] | █R░░░░░░░░░░ | ░░░░░░░░░░░░ |   3 |                                |                                |              |        0 |        0 |        0 |      791 |          |          |
```
