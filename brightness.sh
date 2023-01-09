#!/bin/bash
# Pimoroni Hyperpixel Brightness Adjuster
# Matt Gray | mattg.co.uk | @MattGrayYes
#
# Call this script with a brightness percentage <0-100>
# brightness.sh 50

# if we've got one argument
if [ $# -eq 1 ];
then
    # if the argument is an integer
    if [[ $1 == ?(-)+([0-9]) ]];
    then
        b=$1
        # if the integer is between 0-100
        if [ "$b" -le 100 ] && [ "$b" -ge 0 ];
        then
            echo "Setting Hyperpixel brightness to $b percent"
            # Convert percentage to 0-1023
            let b=$((b*1023/100))
            # Turn on PWM to emable dimming, set value.
            gpio -g mode 19 pwm
            gpio -g pwm 19 $b
        else
            echo "Number not between 0 and 100."
            echo "Call this script with a brightness percentage <0-100>"
        echo "$0 50"
            exit
        fi
     else
        echo "Not a number."
        echo "Call this script with a brightness percentage <0-100>"
        echo "$0 50"
     fi
else
    echo "Pimoroni Hyperpixel Brightness Adjuster"
    echo "Call this script with a brightness percentage <0-100>"
    echo "$0 50"
fi
