from OpenGL.GL.shaders import compileProgram, compileShader
from OpenGL.GL import *

VERTEX_SHADER = """
varying vec3 v_Normal;
varying vec3 v_FragPos;
varying vec2 v_TexCoord;

void main() {
    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
    v_TexCoord = gl_MultiTexCoord0.xy;
    v_Normal = normalize(gl_NormalMatrix * gl_Normal);
    v_FragPos = vec3(gl_ModelViewMatrix * gl_Vertex);
}
"""

FRAGMENT_SHADER = """
varying vec3 v_Normal;
varying vec3 v_FragPos;
varying vec2 v_TexCoord;

uniform sampler2D dayTex;
uniform sampler2D nightTex;

void main() {
    vec3 norm = normalize(v_Normal);
    vec3 lightDir = normalize(gl_LightSource[0].position.xyz - v_FragPos);
    
    // Góc chiếu sáng vật lý không gian thuần túy
    float diff = dot(norm, lightDir);

    // [TINH CHỈNH BẦU KHÍ QUYỂN]: 
    // Cộng thêm 0.25 để ánh sáng "tràn" qua ranh giới hoàng hôn/bình minh.
    // Giúp lúc 6h-7h sáng và 16h-17h chiều trời vẫn sáng sủa (hiệu ứng Golden Hour).
    float atm_diff = diff + 0.25;

    vec4 dayColor = texture2D(dayTex, v_TexCoord);
    vec4 nightColor = texture2D(nightTex, v_TexCoord);

    // Mở rộng dải Blend để ranh giới ngày/đêm mềm mại, giống lớp sương mù rìa Trái Đất
    float blend = smoothstep(-0.1, 0.3, atm_diff);
    
    // Tính toán màu sắc cuối cùng với độ sáng đã được bù đắp
    vec4 diffuse = dayColor * max(atm_diff, 0.0);
    vec4 finalColor = mix(nightColor, diffuse, blend);

    gl_FragColor = finalColor;
}
"""

def create_earth_shader():
    return compileProgram(
        compileShader(VERTEX_SHADER, GL_VERTEX_SHADER),
        compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
    )