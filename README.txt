miniLanding3D is a spaceflight simulation game in which
you take control of a lunar lander at the final phases
of its landing burn. You will have to cancel your velocity
and make a soft touchdown before you run out of propellant
(or overshoot the landing zone :)).

Required Python packages:

 - pyopengl
 - pygame
 - pywavefront
 - keyboard

How To Run:

a) Running main_ext_view.py starts the game in external 
   view (third person) mode.
   
b) Running main_cabin_view.py starts the game in commander's
   POV, looking out of the lander's window

Controls:

   W, A, S, D, Q, E keys to adjust angular velocity (via
   reaction control thruster pulses)
   
   U & J keys to respectively increase and decrease throttle
   (throttle below about 17% is not allowed since it would be
   impossible to sustain combustion)
   
   T & G keys to respectively activate and deactivate
   descent-rate autothrottle
   
   Y & H keys to respectively increase and decrease autothrottle
   descent-rate setting
   
   R & F keys to respectively start and shutdown the main
   engine
   
   Hold the X key to kill all rotation (panic button)
