import time

class RotaryEncoder:
    def __init__(self, clk_pin, dt_pin, sw_pin, event_bus):
        """
        Initialize the RotaryEncoder.

        Args:
            clk_pin: A configured Pin instance for the CLK pin.
            dt_pin: A configured Pin instance for the DT pin.
            sw_pin: A configured Pin instance for the SW (switch) pin.
            event_bus: The event bus to emit events to.
            irq_trigger: The trigger value for the IRQ (e.g., IRQ_FALLING).
        """
        self.clk = clk_pin
        self.dt = dt_pin
        self.sw = sw_pin
        self.event_bus = event_bus

        # Monitors state changes
        self.last_clk = self.clk.value()

        # Triggers self.handle_click if switch button is clicked
        self.sw.irq(trigger=self.sw.IRQ_FALLING, handler=self.handle_click)

        # Variables for debouncing
        self.last_click_time = 0  # Track the last click time
        self.debounce_time = 10

    def handle_click(self, pin):
        """
        Handle the switch click event with debouncing.
        """
        current_time = time.ticks_ms()
        if current_time - self.last_click_time > self.debounce_time:  # Debounce check
            self.last_click_time = current_time
            self.event_bus.emit("click")

    def read(self):
        """Verify the direction of encoder rotation and emits right and left events"""
        current_clk = self.clk.value()
        current_dt = self.dt.value()

        if current_clk != self.last_clk:  # Detects change in the clock
            # If DT value is equal to clock, it's moving right
            if current_dt == current_clk:
                self.event_bus.emit("right")
            else:
                self.event_bus.emit("left")

        # Updates last clock value
        self.last_clk = current_clk