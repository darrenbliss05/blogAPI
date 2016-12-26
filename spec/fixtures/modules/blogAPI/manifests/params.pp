class blogapi::params {

 case $::osfamily {
  'RedHat': {
     $install_path = hiera('blogapi::install_path','/opt/blogapi')
     $logfile_path = hiera('blogapi::logfile_path','/opt/blogapi')
     $pidfile_path = hiera('blogapi::pidfile_path','/opt/blogapi')
     $database_file = hiera('blogapi::database_file','blog.db')
     $blogapiuser = hiera('blogapi::user','root')
     $blogapigroup = hiera('blogapi::group','root')
  } 
  default: {
      fail("The blogapi module is not supported on an ${::operatingsystem} distribution.")
  }
 }
}
