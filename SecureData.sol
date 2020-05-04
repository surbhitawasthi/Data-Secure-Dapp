pragma solidity ^0.6.2;

import 'github.com/OpenZeppelin/openzeppelin-contracts/contracts/access/AccessControl.sol';

contract SecureData is AccessControl {
    address admin;
    bytes32 public constant DOCTOR_ROLE = keccak256("DOCTOR_ROLE");
    
    struct userDetails {
        string username;
        bytes32 roleName;
        bytes32 adminRoleName;
    }
    
    struct fileDetails {
        string filename;
        string fileIPFSHash;
    }
    
    mapping(address => userDetails) private userUserDetailsMapping;
    mapping(address => fileDetails[]) userFilesDetailMapping;
    
    constructor() public {
        admin = msg.sender;
        _setupRole(DEFAULT_ADMIN_ROLE, admin);
    }
    
    modifier isAdmin() {
        require(msg.sender == admin, 'SecureData: Not system admin');
        _;
    }
    
    modifier isUsersAdminRole(address _userAddress) {
        require(hasRole(userUserDetailsMapping[_userAddress].adminRoleName, _userAddress), 'SecureData: User not roles admin');
        _;
    }
    
    modifier isDoctor(address _address) {
        require(hasRole(DOCTOR_ROLE, _address), 'SecureData: Not a doctor');
        _;
    }
    
    modifier isAuthorised(address _externalAddress, address _ownerAddress) {
        require(hasRole(userUserDetailsMapping[_ownerAddress].roleName, _externalAddress), 'SecureData: Not Authorised');
        _;
    }
    
    function addNewUser(address _userAddress, string calldata _username, bool _isDoc) external isAdmin() {
        // Convert useraddress to bytes
        bytes memory _b = new bytes(21);
        for (uint i = 0; i < 20; i++)
            _b[i] = byte(uint8(uint(_userAddress) / (2**(8*(19 - i)))));
        
        _b[20] = byte(uint8(uint(0) / (2**(0))));
        bytes32 userRole = keccak256(_b);
        _b[20] = byte(uint8(uint(1) / (2**(0))));
        bytes32 userkaAdminRole = keccak256(_b);
        
        _setRoleAdmin(userRole, userkaAdminRole);
        _setupRole(userkaAdminRole, _userAddress);
        _setupRole(userRole, _userAddress);
        userUserDetailsMapping[_userAddress] = userDetails(_username, userRole, userkaAdminRole);
        
        if (_isDoc == true) {
            _setupRole(DOCTOR_ROLE, _userAddress);
        }
    }
    
    function addFile(string calldata _filename, string calldata _fileIPFSHash) external isUsersAdminRole(msg.sender) {
        userFilesDetailMapping[msg.sender].push(fileDetails(_filename, _fileIPFSHash));
    }
    
    function addFileByDoctor(
        address patientAddress,
        address doctorAddress,
        string calldata _filename,
        string calldata _fileIPFSHash
        ) external isDoctor(doctorAddress) {
        userFilesDetailMapping[patientAddress].push(fileDetails(_filename, _fileIPFSHash));
    }
    
    function grantPermission(address _externalUserAddress) external isUsersAdminRole(msg.sender) {
        grantRole(userUserDetailsMapping[msg.sender].roleName, _externalUserAddress);
    }
    
    function revokePermission(address _externalUserAddress) external isUsersAdminRole(msg.sender) {
        revokeRole(userUserDetailsMapping[msg.sender].roleName, _externalUserAddress);
    }
    
    function getNumberOfFiles(
        address _userKaAddress
        ) external view isAuthorised(msg.sender, _userKaAddress) returns (uint files) {
            return userFilesDetailMapping[_userKaAddress].length;
    }
    
    function viewFileOfAParticularUser(
        address _userKaAddress,
        uint id
        ) external view isAuthorised(msg.sender, _userKaAddress) returns (string memory, string memory) {
        string memory _filename = userFilesDetailMapping[_userKaAddress][id].filename;
        string memory _fileIPFSHash = userFilesDetailMapping[_userKaAddress][id].fileIPFSHash;
        
        return (_filename, _fileIPFSHash);
    }
    
    function getCountOfMembersInMyRole() external view isUsersAdminRole(msg.sender) returns(uint) {
        return getRoleMemberCount(userUserDetailsMapping[msg.sender].roleName);
    }
    
    function getMemberOfMyRoleById(uint256 index) external view isUsersAdminRole(msg.sender) returns(address, string memory) {
        address _userAddress = getRoleMember(userUserDetailsMapping[msg.sender].roleName, index);
        string memory _username = userUserDetailsMapping[_userAddress].username;
        
        return (_userAddress, _username);
    }
}
