'''
Created on Nov 6, 2016

@author: VSZM
'''
import argparse
import math
import svgwrite

fractal_line_points = [(0,0)]

actual_point = (0,0)
direction_angle = 0

def Koch(depth, inward, length):
    angle_modifier = 0
    if inward == True:
        angle_modifier = 1
    else:
        angle_modifier = -1
    
    if depth == 0:
        Forward(length)
    else:
        Koch(depth-1, inward, length/3)
        Left(angle_modifier * 60)
        Koch(depth-1, inward, length/3)
        Right(angle_modifier * 120)
        Koch(depth-1, inward, length/3)
        Left(angle_modifier * 60)
        Koch(depth-1, inward, length/3)

def Forward(length):
    global fractal_line_points, actual_point, direction_angle
    actual_point = actual_point[0] + length * math.cos(math.radians(direction_angle)), actual_point[1] + length * math.sin(math.radians(direction_angle))
    fractal_line_points.append(actual_point)
    
def Left(angle):
    global direction_angle
    direction_angle = direction_angle - angle

def Right(angle):
    global direction_angle
    direction_angle = direction_angle + angle

def Draw_Fractal(size):
    global fractal_line_points
    dwg = svgwrite.Drawing('Koch.svg', profile='tiny',fill=svgwrite.rgb(0, 0, 0, '%'))
    
    dwg.add(dwg.polyline(fractal_line_points, fill='none', stroke=svgwrite.rgb(100, 0, 0, '%'), stroke_width=size*0.01))
    
    xs = [ xy[0] for xy in fractal_line_points ]
    ys = [ xy[1] for xy in fractal_line_points ]

    left = min(xs)
    right = max(xs)
    top = max(ys)
    bottom = min(ys)
    
    dwg.viewbox(left, bottom, right-left, top-bottom)
    
    dwg.save()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--iterations', type=int, required=True,
                       help='How many iterations should there be for the fractal generation')
    parser.add_argument('--inward', default=False, required=False, choices=['True', 'False'],
                       help='Does the Koch Curve goes inward to the triangle? Default is false')
    parser.add_argument('--sidelength', default=1, required=False, type=float, 
                       help='How long is a side of the triangle')
    
    
    args = parser.parse_args()
    Koch(args.iterations, args.inward == "True", args.sidelength)
    Left(120)
    Koch(args.iterations, args.inward == "True", args.sidelength)
    Left(120)
    Koch(args.iterations, args.inward == "True", args.sidelength)
    
    Draw_Fractal(args.sidelength / max(args.iterations,1))
