#!/data/data/com.termux/files/usr/bin/bash

set -u

if [ "$#" -lt 1 ]; then
    printf 'Usage: %s PID [cpu-list]\n' "$0" >&2
    exit 2
fi

PID="$1"
CPU_LIST="${2:-0,2,4,6}"

CHECK_SECONDS="${OPENMIND_THERMAL_CHECK_SECONDS:-10}"
ROTATE_SECONDS="${OPENMIND_THERMAL_ROTATE_SECONDS:-180}"

CPU_WARM=60
CPU_THROTTLE=66
CPU_HOT=72
CPU_RESUME=63

BATTERY_WARM=42
BATTERY_HOT=45
BATTERY_RESUME=40

LOG='results/runtime/openmind_thermal_governor.log'

IFS=',' read -r -a CPUS <<< "$CPU_LIST"

if [ "${#CPUS[@]}" -eq 0 ]; then
    printf 'ERROR: empty CPU list\n' >&2
    exit 2
fi

read_cpu_temp()
{
    local max_milli=-999000
    local type=''
    local raw=''
    local milli=0
    local zone=''

    for zone in /sys/class/thermal/thermal_zone*
    do
        [ -r "$zone/type" ] || continue
        [ -r "$zone/temp" ] || continue

        IFS= read -r type < "$zone/type" \
          || continue

        case "$type" in
            cpu-[0-9]-*|cpullc-*)
                ;;
            *)
                continue
                ;;
        esac

        IFS= read -r raw < "$zone/temp" \
          || continue

        if ! [[ "$raw" =~ ^-?[0-9]+$ ]]
        then
            continue
        fi

        if [ "$raw" -gt 1000 ]
        then
            milli="$raw"
        else
            milli=$((raw * 1000))
        fi

        if [ "$milli" -gt "$max_milli" ]
        then
            max_milli="$milli"
        fi
    done

    awk \
      -v milli="$max_milli" \
      'BEGIN {
          printf "%.3f\n", milli / 1000
      }'
}


read_battery_temp()
{
    local type=''
    local raw=''
    local milli=0
    local zone=''

    for zone in /sys/class/thermal/thermal_zone*
    do
        [ -r "$zone/type" ] || continue
        [ -r "$zone/temp" ] || continue

        IFS= read -r type < "$zone/type" \
          || continue

        [ "$type" = "battery" ] \
          || continue

        IFS= read -r raw < "$zone/temp" \
          || continue

        if ! [[ "$raw" =~ ^-?[0-9]+$ ]]
        then
            continue
        fi

        if [ "$raw" -gt 1000 ]
        then
            milli="$raw"
        else
            milli=$((raw * 1000))
        fi

        awk \
          -v milli="$milli" \
          'BEGIN {
              printf "%.3f\n", milli / 1000
          }'

        return
    done

    printf '%s\n' '-999'
}


log()
{
    printf '%s %s\n' \
      "$(date -Is)" \
      "$*" \
      | tee -a "$LOG"
}

if ! kill -0 "$PID" 2>/dev/null; then
    printf 'ERROR: PID %s is not running\n' "$PID" >&2
    exit 1
fi

INDEX=0
CURRENT_CPU="${CPUS[$INDEX]}"

taskset -pc "$CURRENT_CPU" "$PID" >/dev/null

LAST_ROTATE=$(date +%s)
PAUSED=0

log \
  "START pid=$PID cpus=$CPU_LIST cpu=$CURRENT_CPU"

while kill -0 "$PID" 2>/dev/null
do
    CPU_TEMP=$(read_cpu_temp)
    BAT_TEMP=$(read_battery_temp)

    NOW=$(date +%s)

    STATE='NORMAL'

    if awk \
      -v cpu="$CPU_TEMP" \
      -v bat="$BAT_TEMP" \
      -v ch="$CPU_HOT" \
      -v bh="$BATTERY_HOT" \
      'BEGIN {
          exit !(cpu >= ch || bat >= bh)
      }'
    then
        STATE='HOT'

        if [ "$PAUSED" -eq 0 ]; then
            kill -STOP "$PID" 2>/dev/null || true
            PAUSED=1

            log \
              "PAUSE cpu=${CPU_TEMP}C battery=${BAT_TEMP}C"
        fi

    elif [ "$PAUSED" -eq 1 ]; then

        if awk \
          -v cpu="$CPU_TEMP" \
          -v bat="$BAT_TEMP" \
          -v cr="$CPU_RESUME" \
          -v br="$BATTERY_RESUME" \
          'BEGIN {
              exit !(cpu <= cr && bat <= br)
          }'
        then
            kill -CONT "$PID" 2>/dev/null || true
            PAUSED=0
            LAST_ROTATE="$NOW"

            log \
              "RESUME cpu=${CPU_TEMP}C battery=${BAT_TEMP}C"
        else
            STATE='COOLING'
        fi

    elif awk \
      -v cpu="$CPU_TEMP" \
      -v bat="$BAT_TEMP" \
      -v ct="$CPU_THROTTLE" \
      -v bw="$BATTERY_WARM" \
      'BEGIN {
          exit !(cpu >= ct || bat >= bw)
      }'
    then
        STATE='THROTTLE'

        kill -STOP "$PID" 2>/dev/null || true
        sleep 3
        kill -CONT "$PID" 2>/dev/null || true

    elif awk \
      -v cpu="$CPU_TEMP" \
      -v cw="$CPU_WARM" \
      'BEGIN {
          exit !(cpu >= cw)
      }'
    then
        STATE='WARM'
    fi

    ROTATE_AFTER="$ROTATE_SECONDS"

    if [ "$STATE" = 'WARM' ]; then
        ROTATE_AFTER=90
    fi

    if [ "$STATE" = 'THROTTLE' ]; then
        ROTATE_AFTER=60
    fi

    if [ "$PAUSED" -eq 0 ] \
       && [ $((NOW - LAST_ROTATE)) -ge "$ROTATE_AFTER" ]
    then
        INDEX=$(( (INDEX + 1) % ${#CPUS[@]} ))

        CURRENT_CPU="${CPUS[$INDEX]}"

        taskset -pc \
          "$CURRENT_CPU" \
          "$PID" \
          >/dev/null 2>&1 \
          || true

        LAST_ROTATE="$NOW"

        log \
          "ROTATE cpu=$CURRENT_CPU temp=${CPU_TEMP}C state=$STATE"
    fi

    log \
      "STATUS pid=$PID cpu=$CURRENT_CPU cpu_temp=${CPU_TEMP}C battery=${BAT_TEMP}C state=$STATE paused=$PAUSED"

    sleep "$CHECK_SECONDS"
done

log \
  "EXIT pid=$PID process-finished"

exit 0
