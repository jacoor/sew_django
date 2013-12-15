module.exports = function(grunt) {

    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),

        sass: {
            dist: {
                options: {
                    style: 'compressed',
                    debugInfo : true
                },
                files: {
                    'sew_django/static/.sass-cache/livereload/main.css': 'sew_django/static/scss/main.scss'
                }
            } 
        },
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
    grunt.registerTask('default', [ 'sass', 'watch']);
};
