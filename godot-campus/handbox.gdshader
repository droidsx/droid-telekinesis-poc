shader_type spatial;



void vertex() {
	// Called for every vertex the material is visible on.
}

//void light() {
	// Called for every pixel for every light affecting the material.
	// Uncomment to replace the default light processing function with this one.
//}

uniform vec4 color0 = vec4(1.0, 0.0, 0.0, 1.0); // Red
uniform vec4 color1 = vec4(0.0, 1.0, 0.0, 1.0); // Green
uniform vec4 color2 = vec4(0.0, 0.0, 1.0, 1.0); // Blue
uniform vec4 color3 = vec4(1.0, 1.0, 0.0, 1.0); // Yellow
uniform vec4 color4 = vec4(1.0, 0.0, 1.0, 1.0); // Magenta
uniform vec4 color5 = vec4(0.0, 1.0, 1.0, 1.0); // Cyan

void fragment() {
    vec3 norm = abs(NORMAL);
    vec4 color = vec4(1.0, 1.0, 1.0, 1.0);

    if (norm.x > norm.y && norm.x > norm.z) {
        color = color0; // X-axis sides
    } else if (norm.y > norm.x && norm.y > norm.z) {
        color = color1; // Y-axis sides
    } else if (norm.z > norm.x && norm.z > norm.y) {
        color = color2; // Z-axis sides
    }

    if (NORMAL.x < 0.0) {
        color = color3; // -X-axis side
    } else if (NORMAL.y < 0.0) {
        color = color4; // -Y-axis side
    } else if (NORMAL.z < 0.0) {
        color = color5; // -Z-axis side
    }

    ALBEDO = color.rgb;
    ALPHA = color.a;
}
