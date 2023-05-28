$fn=50;
cm = 10;

in_w = 7*cm;
in_d = 5.4*cm;
wall = 1;

front_h = 1.25*cm;
back_h  = 4.25*cm;

post_dia = .40*cm;
post_rad = post_dia / 2;
post_h   = (back_h - 1.25*cm) - 4;
// a^2 + b^2 = c^2
// temp = front_h^2 + back_h^2;
// hyp = sqrt(temp);

plug_w = 1.25*cm;
plug_h = 0.75*cm;

difference () {
    box(in_w, in_d, back_h, wall);

    translate([-wall, 0, front_h])
        rotate([30, 0, 0])
            cube([in_w+(wall*4), in_d*1.2, back_h]);

    translate([-1, (in_d/2)+3, 3.5])
        rotate([30,0,0])
            cube([3, plug_w, plug_h]);
}

// echo(str("PostRad = ", post_rad));
// left post
translate([wall + post_rad + 0.1, in_d-(post_rad/2), wall])
    cylinder(d=post_dia, h=post_h);

// right post
translate([(wall + in_w)-post_rad-.1, in_d-(post_rad/2), wall])
    cylinder(d=post_dia, h=post_h);


module box(w,d,h,wall=1) {
    difference() {
        cube([wall+w+wall,wall+d+wall,h]);

        translate([wall,wall,wall])
            cube([w,d,h]);
    }

}
