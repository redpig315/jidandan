package shoudan;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Iterator;
import java.util.List;
import java.util.Properties;
import java.util.Vector;




import com.jcraft.jsch.Channel;
import com.jcraft.jsch.ChannelSftp;
import com.jcraft.jsch.JSch;
import com.jcraft.jsch.JSchException;
import com.jcraft.jsch.Session;
import com.jcraft.jsch.SftpATTRS;
import com.jcraft.jsch.SftpException;
import com.jcraft.jsch.ChannelSftp.LsEntry;

public class GetSD {


	public static void main(String[] args)
	  {
		GetSD ftp = new GetSD();
		String chkdate=null;
	    
		if (args.length < 6) {
	        System.out.println("用法：Getchk.jar ip port  username password remotedir localdir [chkdate]");
	    	System.exit(0);
	    }
		
		if(args.length ==6){
			 chkdate=ftp.getYesterday();; // 取文件日期
			 System.out.println("获取 "+chkdate+"日 网联收单对账文件...");
		}else
		{
			chkdate=args[6].trim();
		    System.out.println("获取 "+chkdate+"日 网联收单对账文件...");
		}
		
		
		
	    String host = args[0].trim();
	    int port = Integer.parseInt(args[1]);
	    String username = args[2].trim();
	    String password = args[3].trim();
	    String remotedir = args[4].trim();
	    String localdir = args[5].trim();
	    Boolean flag=true;
	    Vector dirls=new Vector();
	    
	    File localfile=new File(localdir+chkdate);
	    if(!localfile.exists()){
	    	localfile.mkdir();
	    }
	    

        remotedir=remotedir+chkdate;
		//连接数据库
	    ChannelSftp sftp = ftp.connect(host, port, username, password);
	    
	     dirls=ftp.listFiles(remotedir, sftp);
	    for(int i=0;i<dirls.size();i++){
	    	
	        Object v=dirls.get(i);
	    	String filename=((com.jcraft.jsch.ChannelSftp.LsEntry)v).getFilename();
	    	if (!filename.equals("..")&&!filename.equals(".")){
	    	flag=ftp.download(remotedir, filename, localdir+chkdate+"/"+filename, sftp);
	    	if(flag){
	    		System.out.println("download file "+filename+" is ok ...");
	    		System.out.println("local file "+localdir+chkdate+"/"+filename+" is ok ...");
	    		
	    		}
	    	else{
	    		System.out.println("download file "+filename+" is failed!!! ...");
	    		System.out.println("local file "+localdir+chkdate+"\\"+filename+" is failed ...");
	    		
	    	}
	    	}
	    
	    }
	    try
	    {
	      sftp.cd(remotedir);
		  
	    }
	    catch (SftpException e)
	    {
	      e.printStackTrace();
	    }
	    finally
	    {
	      try
	      {
	        sftp.getSession().disconnect();
	      }
	      catch (JSchException e)
	      {
	        e.printStackTrace();
	      }
	      sftp.disconnect();
	      sftp.exit();
	    }
	  }
	  
	  public ChannelSftp connect(String host, int port, String username, String password)
	  {
	    ChannelSftp csftp = null;
	    JSch jsch = new JSch();
	    try
	    {
	      Session sshSession = jsch.getSession(username, host, port);
	      

	      sshSession.setPassword(password);
	      Properties sshConfig = new Properties();
	      sshConfig.put("StrictHostKeyChecking", "no");
	      sshSession.setConfig(sshConfig);
	      sshSession.connect();
	      

	      Channel channel = sshSession.openChannel("sftp");
	      channel.connect();
	      
	      csftp = (ChannelSftp)channel;
	    }
	    catch (JSchException e)
	    {
	      e.printStackTrace();
	    }
	    return csftp;
	  }
	  
	  public boolean upload(String directory, String uploadFile, ChannelSftp sftp)
	  {
	    File file = new File(uploadFile);
	    try
	    {
	      sftp.cd(directory);
	      sftp.put(new FileInputStream(file), file.getName());
	    }
	    catch (Exception e)
	    {
	      e.printStackTrace();
	      return false;
	    }
	    return true;
	  }
	  
	  public boolean download(String directory, String downloadFile, String saveFile, ChannelSftp sftp)
	  {
	    File file = new File(saveFile);
	    try
	    {
	      sftp.cd(directory);
	      sftp.get(downloadFile, new FileOutputStream(file));
	    }
	    catch (FileNotFoundException e)
	    {
	      e.printStackTrace();
	      return false;
	    }
	    catch (SftpException e)
	    {
	      e.printStackTrace();
	      return false;
	    }
	    return true;
	  }
	  
	  public boolean delete(String directory, String deleteFile, ChannelSftp sftp)
	  {
	    try
	    {
	      sftp.cd(directory);
	      sftp.rm(deleteFile);
	    }
	    catch (SftpException e)
	    {
	      e.printStackTrace();
	      return false;
	    }
	    return true;
	  }
	  
	  public Vector<?> listFiles(String directory, ChannelSftp sftp)
	  {
	    try
	    {
	      return sftp.ls(directory);
	    }
	    catch (SftpException e)
	    {
	      e.printStackTrace();
	    }
	    return null;
	  }
	  
	  
	 public String getYesterday(){
			  SimpleDateFormat df = new SimpleDateFormat("yyyyMMdd");
			  Calendar c=Calendar.getInstance();
			  int day=c.get(Calendar.DATE);
			  c.set(Calendar.DATE, day-1);
			  return df.format(c.getTime());
			 }
	 
	
}
