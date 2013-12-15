module.exports = function(grunt) {

       grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),

        sass: {
            dist: {
                options: {
                    style: 'compressed'
                },
                files: {
                    'css/build/normalize.css': 'sew_django/static/libs/foundation-5.0.2/scss/foundation.scss',
                    'css/build/foundation.css': 'sew_django/static/libs/foundation-5.0.2/scss/foundation.scss'
                }
            } 
        }
        watch: {
            css: {
                files: ['css/*.scss'],
                tasks: ['sass'],
                options: {
                    spawn: false
                }
            }
        }

    });

    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-sass');
    grunt.registerTask('default', ['sass', 'watch']);
};
