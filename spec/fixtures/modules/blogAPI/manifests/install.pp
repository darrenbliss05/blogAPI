class blogapi::install inherits blogapi {

   # Create installation directory used by this application.
   file { "$install_path":
    ensure => 'directory',
    owner => "$blogapiuser",
    group => $blogapigroup,
    mode => '0640',
   }

file { "$install_path/blogapi.py":
    ensure => file,
    owner => $blogapiuser,
    group => $blogapigroup,
    mode => '0740',
    source => "puppet:///modules/blogapi/blogapi.py",
}

   # Ensure that all of the modules required by python are installed.
   package { "daemonize": 
    ensure  => latest,
    provider => pip,
  }
   package { "flask": 
    ensure  => latest,
    provider => pip,
  }
  package { "flask_sqlalchemy":
    ensure  => latest,
    provider => pip,
  }
  package { "sqlalchemy":
    ensure  => latest,
    provider => pip,
  }
  package { "flask_marshmallow":
    ensure  => latest,
    provider => pip,
  }
  package { "marshmallow-sqlalchemy":
    ensure  => latest,
    provider => pip,
  }
}
