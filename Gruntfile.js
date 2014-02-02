module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    coffee: {
      compile:  {
        expand: true,     // Enable dynamic expansion.
        cwd: 'interface/src/coffee',      // Src matches are relative to this path.
        src: ['**/*.coffee', '**/*.litcoffee'], // Actual pattern(s) to match.
        dest: 'interface/build/js',   // Destination path prefix.
        ext: '.js',   // Dest filepaths will have this extension.
      }
    },
    less: {
      compile:  {
        expand: true,     // Enable dynamic expansion.
        cwd: 'interface/src/less/',      // Src matches are relative to this path.
        src: [
          'cyti/*.less',
          'sidebars/*.less',
          'themes/*.less',
          'slideshows/*.less',
          '*.less',
        ],
        dest: 'interface/build/css',   // Destination path prefix.
        ext: '.css',   // Dest filepaths will have this extension.
      }
    },
    copy: {
      main: {
        files: [
          // includes files within path and its sub-directories
          {
            expand: true,
            cwd: 'interface/lib/',      // Src matches are relative to this path.
            src: [
              '**'
            ],
            dest: 'interface/build/'
          },
        ]
      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-coffee');
  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks('grunt-contrib-copy');

  grunt.registerTask('default', ['coffee', 'less', 'copy']);
};
