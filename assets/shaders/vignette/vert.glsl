// https://github.com/totex/Panda3D-shaders/blob/main/shaders/vignette-vert.glsl

#version 330

// Vertex inputs
in vec4 p3d_Vertex;


// Uniform inputs
uniform mat4 p3d_ModelViewProjectionMatrix;


// the main function
void main() {
    gl_Position = p3d_ModelVieProjectionMatrix * p3d_Vertex;
}