from math import sin, cos

def double_pendulum(state):
    """
    Computes the derivatives of the state vector.
    
    Arguments:
    state -- a 4-element array containing the angles and angular velocities of the two pendulums
    t -- time
    
    Returns:
    A 4-element array containing the derivatives of the state vector.
    """
    g = 9.81  # acceleration due to gravity (m/s^2)
    m1 = 1.0  # mass of pendulum 1 (kg)
    m2 = 1.0  # mass of pendulum 2 (kg)
    L1 = 1.0  # length of pendulum 1 (m)
    L2 = 1.0  # length of pendulum 2 (m)
    theta1, omega1, theta2, omega2 = state

    # Equations of motion
    alpha = m1 + m2
    beta = m2 * L1 * cos(theta1 - theta2)
    delta = m2 * L2 * cos(theta1 - theta2)
    epsilon = -m2 * L2 * omega2 **2 * sin(theta1 - theta2) - g * (m1 + m2) * sin(theta1)
    zeta = m2 * L1 * omega1**2 * sin(theta1 - theta2) - m2 * g *sin(theta2)
    
    theta1_dot = omega1
    omega1_dot = (epsilon * delta - beta * zeta) / (alpha * delta**2 - beta**2)
    theta2_dot = omega2
    omega2_dot = (alpha * zeta - beta * epsilon) / (alpha * delta**2 - beta**2)

    temp = [theta1_dot, omega1_dot, theta2_dot, omega2_dot]
    return [int(abs(num)) for num in temp]


print(double_pendulum([65,38,116,94]))