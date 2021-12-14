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
                                      - - - - - - - - - - - -
                                - - -                         - - -
                          - - -         - - - - - - - - - -         - - -
                        - -       - - -                     - - -       - -
                      -     - - -                                 - - -     -
                  - -     -             - - - - - - - - - -             -     - -
                -       -         - - -                     - - -         -       -
              -     - -       - -         - - - - - - - -         - -       - -     -
            -     -         -       - - -                 - - -       -         -     -
          - -   - -     - -     - -         - - - - - -         - -     - -     - -   - -
        -     -       -       -       - - -             - - -       -       -       -     -
        -     -     -     - -     - -                         - -     - -     -     -     -
      -     -     -     -       -           - -   - - -           -       -     -     -     █A
      -   -       -     -   - -         - - -         - - -         - -   -     -       █A  -
    -     -     -   - -   -         - -       2             - -         -   - -   -     -     -
    -   -     -     -     -       -         - - - - - -         -       -     -     █A    -   -
  -     -     -   -     -       -       - -             - -       -       -     █A  -     -     -
  -   -     -     -   -       -     - -       - - - -       - -     -       █A3*-     -     -   -
  -   -     -   -     -     -       -     - -         - -     -       █A    -     -   -     -   -
-     -   -     -   -       -     -   - -                 - -   -     -       -   -     -   -     -
-     -   -     -   -     -     -     -     - - - - - -     -     █A    -     -   -     -   -     -
-   -     -   -     -     -     -   -     -             -     █A  -     -     -     -   -     -   -
-   -     -   -   -     - -   -     -   -     - - - -     █A  -     -   - -     -   -   -     -   -
-   -     -   -   -     -     -     -   -   -         █A  -   -     -     -     -   -   -     -   -
-   -     -   -   -     -     -   -     -   -         -   -     -   -           -   -   -     -   -
-   -     -   -   -           -   -     -   -     0*  -   -     -   -     -     -   -   -     -   -
-   -     -   -   -     -     -   -     -   -         -   -     -   -     -     -   -   -     -   -
-   -     -   -   -     - -   -     -   -     -   - -     -   -     -   - -     -   -   -     -   -
-   -     -   -     -     -     -   -     -             -     -   -     -     -     -   -     -   -
-   -     -     -   -     -     -     -     - -     - -     -     -     -     -   -     -     -   -
-     -     -   -   -       -     -     -         -       -     -     -       -   -   -     -     -
  -   -     -   -     -     -     - -     - - -     - - -     - -     -     -     -   -     -   -
  -   -     -     -   -       -       -       -   - -       -       -       -   -     -     -   -
  -     -     -   -     -       -       - - -         - - -       -       -     -   -     -     -
    -   -     -     -   - -       -           -   - -           -       - -   -     -     -   -
    -     -     -     -     -       - -                     - -       -     -     -     -     -
      -   -     - -   -     -           - - -         - - -           -     -   - -     -   -
      -     -     -     - -   - -           - -   - - -           - -   - -     -     -     -
        -   -       -     -       - -                         - -     1 -     -       -   -
          -   - -     - -   - -       - - -             - - -       - -   - -     - -   -
          -     -       -       - -         - -   - - -         - -       -       -     -
            -     - -     - -       - - -                 - - -       - -     - -     -
              -       -       - -         - - -   - - - -         - -       -       -
                -     - -         - - -                     - - -         - -     -
                  - -     - -           - - - -   - - - - -           - -     - -
                    - -       - -                                 - -       - -
                        - -       - - - -                 - - - -       - -
                            - -           - - -   - - - -           - -
                                - - - -                     - - - -
                                        - - - -   - - - - -

[time]              19.45ms

[wasted]            16.12ms
[throughput]        370.18 kbps
[throughput rate]   ███░░░░░░░░░░░░░░░░░ 17.14% 370.18/2160.00

[collision rate]    ████████░░░░░░░░░░░░ 40.00% 2/5
[on air frames]      1

[node details]
  ID |     send |     recv |   c |   s |   r |                        sending |                      receiving |     detected |  backoff |     difs |     sifs |  timeout |      nav | allocate |
[ 0] | █A░░░░░░ | ░░░░░░░░ |   0 |   1 |   2 | ██████████████░░░░░░ 74.25%    |                                |              |        0 |        0 |        0 |          |          |          |
[ 1] | █R░░░░░░ | ░░░░░░░░ |   1 |   1 |   2 |                                |                                |   ACK 0 -> 3 |      750 |        0 |        0 |          |     1216 |          |
[ 2] | █R░░░░░░ | ░░░░░░░░ |   1 |   1 |   2 |                                |                                |   ACK 0 -> 3 |      500 |      750 |        0 |          |     1191 |          |
[ 3] | ░░░░░░░░ | █A░░░░░░ |   0 |   2 |   1 |                                | █████████████░░░░░░░ 69.00%    |   ACK 0 -> 3 |        0 |        0 |        0 |     1466 |          |     6841 |
```
