config = {
    'HOST_TO_PING': '8.8.8.8',

    # in seconds (this is also time between ping starts)
    'PING_TIMEOUT': 0.5,

    # to mark as disconnection and take action
    'MAX_ALLOWED_TIMEOUTS_COUNT': 3,

    # smaller value decreases visual monitor latency
    'GUI_MS_BETWEEN_REDRAWS': 50,

    # number of pings to show white dot after detected disconnection
    'RECOVERY_PINGS_COUNT': 120,

    # Round trip time ranges converted to icon color
    'MAX_BLUE_RTT': 100,
    'MAX_GREEN_RTT': 200,
    'MAX_YELLOW_RTT': 350,
}
