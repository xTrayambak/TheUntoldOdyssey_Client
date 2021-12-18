// https://github.com/totex/Panda3D-shaders/blob/main/shaders/vignette-frag.glsl

#version 330

uniform vec2 resolution;

out vec4 outColor;

const float outerRadius = 0.65;
const float innerRadius = 0.3;
const float intensity = 0.6;

// can be created on one line
// const float outerRadius = 0.65, innerRadius = 0.3, intensity = 0.6;

void main() {

    vec4 color = vec4(1.0);
    vec2 relativePosition = gl_FragCoord.xy / resolution - 0.5;
    float len = length(relativePosition);
    float vignette = smoothstep(outerRadius, innerRadius, len);
    color.rgb = mix(color.rgb, color.rgb * vignette, intensity);

    outColor = color;
}