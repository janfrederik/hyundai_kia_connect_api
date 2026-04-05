export BLUELINK_USERNAME="$(pass bluelink/username)"
export BLUELINK_PASSWORD="$(pass bluelink/refresh_token)"
export BLUELINK_PIN="$(pass bluelink/pin)"

bl() {
    bluelink --region Europe --brand Hyundai "$@"; 
}
