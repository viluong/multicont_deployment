# Multicont_deployment
- ReactJS for frontend in **client** folder
- FastApi application in **server** folder
- Pubsub messages system is written by Python in **worker** folder.
- Setup nginx in **nginx** folder
- Using Github Actions to build CI/CD in [this file](https://github.com/viluong/multicont_deployment/blob/master/.github/workflows/deploy.yaml).
  
**My diagram:**

![diagrams-01 - catchup](https://github.com/user-attachments/assets/3de4d343-0333-4aac-bc54-beed6512b759)


**Elastic Beanstalk Application Creation**

1. Go to AWS Management Console and use Find Services to search for Elastic Beanstalk

2. Click “Create Application”

3. Set Application Name to 'multi-docker'

4. Scroll down to Platform and select Docker

5. Verify that "Single Instance (free tier eligible)" has been selected

6. Click the "Next" button.

7. In the "Service Role" section, verify that "Use an Existing service role" is selected.

8. Verify that aws-elasticbeanstalk-service-role has been auto-selected for the service role.

9. Verify that aws-elasticbeanstalk-ec2-role has been auto-selected for the instance profile.

10. Click "Skip to review" button.

11. Click the "Submit" button.

You may need to refresh, but eventually, you should see a green checkmark underneath Health.

**RDS Database Creation**

1. Go to AWS Management Console and use Find Services to search for RDS

2. Click Create database button

3. Select PostgreSQL

4. In Templates, check the Free tier box.

5. Scroll down to Settings.

6. Set DB Instance identifier to multi-docker-postgres

7. Set Master Username to postgres

8. Set Master Password to postgrespassword and confirm.

9. Scroll down to Connectivity. Make sure VPC is set to Default VPC

10. Scroll down to Additional Configuration and click to unhide.

11. Set Initial database name to fibvalues

12. Scroll down and click Create Database button

**ElastiCache Redis Creation**

1. Go to AWS Management Console and use Find Services to search for ElastiCache

2. In the sidebar under Resources, click Redis OSS caches

3. Click the Create Redis OSS caches button

4. Select Design your own cache and Cluster cache

5. Make sure Cluster Mode is DISABLED.

6. Scroll down to Cluster info and set Name to multi-docker-redis

7. Scroll down to Cluster settings and change Node type to cache.t3.micro

8. Change Number of Replicas to 0 (Ignore the warning about Multi-AZ)

9. Scroll down to Subnet group. Select Create a new subnet group if not already selected.

10. Enter a name for the Subnet Group such as redis.

11. Scroll down and click the Next button

12. Scroll down and click the Next button again.

13. Scroll down and click the Create button.

14. After the cache has been fully created (green Available status), click the new multi-docker-redis cache name. Then, click Modify.

15. Scroll down to Security and locate the Transit encryption mode setting. Change this setting from Required to Preferred. This is very important, otherwise, you will not see your Calculated Values in the client form.

16. Scroll down and click Preview changes, then click Modify.

17. You will need to wait for the cache to apply the changes and restart (green Available status) which could take around 5 minutes or more.

**Creating a Custom Security Group**

1. Go to AWS Management Console and use Find Services to search for VPC

2. Find the Security section in the left sidebar and click Security Groups

3. Click Create Security Group button

4. Set Security group name to multi-docker

5. Set Description to multi-docker

6. Make sure VPC is set to your default VPC

7. Scroll down and click the Create Security Group button.

8. After the security group has been created, find the Edit inbound rules button.

9. Click Add Rule

10. Set Port Range to 5432-6379

11. Click in the box next to Source and start typing 'sg' into the box. Select the Security Group you just created.

12. Click the Save rules button

**Applying Security Groups to ElastiCache**

1. Go to AWS Management Console and use Find Services to search for ElastiCache

2. Under Resources, click Redis clusters in Sidebar

3. Check the box next to your Redis cluster

4. Click Actions and click Modify

5. Scroll down to find Selected security groups and click Manage

6. Tick the box next to the new multi-docker group and click Choose

7. Scroll down and click Preview Changes

8. Click the Modify button.

**Applying Security Groups to RDS**

1. Go to AWS Management Console and use Find Services to search for RDS

2. Click Databases in Sidebar and check the box next to your instance

3. Click Modify button

4. Scroll down to Connectivity and add select the new multi-docker security group

5. Scroll down and click the Continue button

6. Click Modify DB instance button

**Applying Security Groups to Elastic Beanstalk**

1. Go to AWS Management Console and use Find Services to search for Elastic Beanstalk

2. Click Environments in the left sidebar.

3. Click MultiDocker-env

4. Click Configuration

5. In the Instances row, click the Edit button.

6. Scroll down to EC2 Security Groups and tick the box next to multi-docker

7. Click Apply and Click Confirm

8. After all the instances restart and go from No Data to Severe, you should see a green checkmark under Health.

**Setting Environment Variables**

1. Go to Parameters Store

2. Click create parameter.

3. Set /multicont-deployment/server/.env/PG_DATABASE into the name.

   Note: We will write variables into /server/.env file in github actions. Please look at https://github.com/viluong/multicont_deployment/blob/master/.github/workflows/deploy.yaml#L68-L78.
   so the meaning of name "/multicont-deployment/server/.env/PG_DATABASE" is we will write PG_DATABASE=value in /server/.env
   
5. Tick SecureString in Type

6. Set value for variable

7. Click Create parameter.
 
8. Do these steps with another variables: **/multicont-deployment/server/.env/PG_HOST**, **/multicont-deployment/server/.env/PG_PASSWORD**, **/multicont-deployment/server/.env/PG_PORT**, **/multicont-deployment/server/.env/PG_USER**,
**/multicont-deployment/server/.env/REDIS_HOST**, **/multicont-deployment/server/.env/REDIS_PORT**, **/multicont-deployment/worker/.env/REDIS_HOST**, **/multicont-deployment/worker/.env/REDIS_PORT**. 
These variables correspond to the variables in the /server/.env.example and /multicont-deployment/worker/.env.example files.

**IAM Keys for Deployment**

You can use the same IAM User's access and secret keys from the single container app we created earlier, or, you can create a new IAM user for this application:

1. Search for the "IAM Security, Identity & Compliance Service"

2. Click "Create Individual IAM Users" and click "Manage Users"

3. Click "Add User"

4. Enter any name you’d like in the "User Name" field.

eg: docker-multi-ci

5. Click "Next"

6. Click "Attach Policies Directly"

7. Search for "beanstalk"

8. Tick the box next to "AdministratorAccess-AWSElasticBeanstalk"

9. Click "Next"

10. Click "Create user"

11. Select the IAM user that was just created from the list of users

12. Click "Security Credentials"

13. Scroll down to find "Access Keys"

14. Click "Create access key"

15. Select "Command Line Interface (CLI)"

16. Scroll down and tick the "I understand..." check box and click "Next"

Copy and/or download the Access Key ID and Secret Access Key to use in the Github Actions Setup.

**Setting Repository secrets in Github repository setting**

1. Set **AWS_ACCESS_KEY_ID**, **AWS_SECRET_ACCESS_KEY**. You already download or copy when creating IAM key.
2. Set **AWS_REGION**
3. Set **DB_HOST_TEST**, **DB_PORT_TEST**, **DB_PW_TEST**, **DB_TEST**, **DB_USER_TEST**, **REDIS_HOST_TEST**, **REDIS_PORT_TEST** for testing postgres database when we run unit test in Github Actions.
4. Set **DOCKER_HUB_TOKEN**, **DOCKER_HUB_USERNAME**. These variables get from https://hub.docker.com/

**Deploying App**

Make a small change to your src/App.js file in the greeting text.

In the project root, in your terminal run:

git add.
git commit -m “testing deployment"
git push origin main
Go to your Travis Dashboard and check the status of your build.

The status should eventually return with a green checkmark and show "build passing"

Go to your AWS Elastic Beanstalk application

It should say "Elastic Beanstalk is updating your environment"

It should eventually show a green checkmark under "Health". You will now be able to access your application at the external URL provided under the environment name.
