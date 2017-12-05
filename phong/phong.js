var vertexShader = `
  varying vec3 normalInterp;
  varying vec3 vertPos;

  void main(){
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      vec4 vertPos4 = modelViewMatrix * vec4(position, 1.0);
      vertPos = vec3(vertPos4) / vertPos4.w;
      normalInterp = normalMatrix * normal;
  }
`;

var fragmentShader = `
  precision mediump float; 

  varying vec3 normalInterp;
  varying vec3 vertPos;

  uniform vec3 lightPos;
  uniform float ka;
  uniform float ks;
  uniform float kd;

  const vec3 ambientColor = vec3(0.3, 0.0, 0.0);
  const vec3 diffuseColor = vec3(0.5, 0.0, 0.0);
  const vec3 specColor = vec3(1.0, 1.0, 1.0);

  void main() {
      vec3 normal = normalize(normalInterp);
      vec3 lightDir = normalize(lightPos - vertPos);
      vec3 reflectDir = reflect(-lightDir, normal);
      vec3 viewDir = normalize(-vertPos);

      float lambertian = max(dot(lightDir,normal), 0.0);
      float specular = 0.0;

      if(lambertian > 0.0) {
        float specAngle = max(dot(reflectDir, viewDir), 0.0);
        specular = pow(specAngle, 80.0);
      }
      gl_FragColor = vec4(ka*ambientColor +
                        kd*lambertian*diffuseColor +
                        ks*specular*specColor, 1.0);
  }
`;

function Props() {
  this.lightPosX = 100;
  this.lightPosY = 100;
  this.lightPosZ = 100;
  this.ka = 1.0;
  this.ks = 1.0;
  this.kd = 1.0;
}

var props = new Props();

window.addEventListener('load', function() {
  var gui = new dat.GUI();
  gui.add(props, 'lightPosX').onChange(v => uniforms.lightPos.value.x = v);
  gui.add(props, 'lightPosY').onChange(v => uniforms.lightPos.value.y = v);
  gui.add(props, 'lightPosZ').onChange(v => uniforms.lightPos.value.z = v);
  gui.add(props, 'ka', 0, 1).onChange(v => uniforms.ka.value = v);
  gui.add(props, 'ks', 0, 1).onChange(v => uniforms.ks.value = v);
  gui.add(props, 'kd', 0, 1).onChange(v => uniforms.kd.value = v);
})

// document.addEventListener('mousemove', (event) => {
//   uniforms.lightPos.value.x = event.clientX - window.innerWidth/2;
//   uniforms.lightPos.value.y = - event.clientY + window.innerHeight/2;
// });

var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera( 75, window.innerWidth/window.innerHeight, 0.1, 1000 );

var renderer = new THREE.WebGLRenderer();
renderer.setSize( window.innerWidth, window.innerHeight );
document.body.appendChild( renderer.domElement );

var uniforms = {
  lightPos: new THREE.Uniform( new THREE.Vector3(props.lightPosX, props.lightPosY, props.lightPosZ) ),
  ka: new THREE.Uniform( props.ka ),
  ks: new THREE.Uniform( props.ks ),
  kd: new THREE.Uniform( props.kd ),
};

var sphereGeometry = new THREE.SphereGeometry( 15, 32, 32 );
var planeGeometry = new THREE.PlaneGeometry( 20, 20 );
var material = new THREE.ShaderMaterial( {
  uniforms,
  vertexShader,
  fragmentShader,
} );

var sphere = new THREE.Mesh( sphereGeometry, material );
var plane = new THREE.Mesh( planeGeometry, material );
scene.add( sphere );

camera.position.z = 50;

var animate = function () {
  requestAnimationFrame( animate );

  sphere.rotation.x += 0.1;
  sphere.rotation.y += 0.1;

  renderer.render(scene, camera);
};

animate();