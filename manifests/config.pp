class blogapi::config inherits blogapi {

  file { "$install_path/configfile":
    ensure => file,
    owner => $blogapiuser,
    group => $blogapigroup,
    mode => '0640',
#    content => epp('blogapi/configfile',{ mycode => "foo"})
    content => epp('blogapi/configfile.epp',{ 
            install_path_tag  => $install_path, 
            pidfile_path_tag  => $pidfile_path, 
            logfile_path_tag  => $logfile_path, 
            database_file_tag => $database_file}),
}
  file { "$install_path/blog.db":
    ensure => file,
    owner => $blogapiuser,
    group => $blogapigroup,
    mode => '0640',
    source => "puppet:///modules/blogapi/blog.db.master",
}
}
